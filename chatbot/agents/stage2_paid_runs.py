"""stage2_paid_runs.py — Part C Stage 2: five production runs on Anthropic/claude-sonnet-4-6.

Pre-conditions:
  - chatbot/.env must have ANTHROPIC_API_KEY set.
  - Run from repo root: python chatbot/agents/stage2_paid_runs.py

Steps performed:
  1. Switch .env to LLM_PROVIDER=anthropic / LLM_MODEL=claude-sonnet-4-6.
  2. Confirm provider + model.
  3. Direct tool smoke-test (news RAG + web search, NO LLM).
  4. Run five queries via run_query_worker.py subprocesses, each with its own
     preflight (including new membership-confidence check).  F2022 run gets
     all alt-wave env vars.
  5. After each run, parse the run record for cost; abort before next run if
     any single run exceeds $1.50 or the running total would exceed $6.
  6. On any failure: STOP and report; do NOT auto-retry.
  7. After all runs (success or failure): restore .env to the dev lane.

Labels: v60-A2-W2026, v60-A2-F2022, v60-MMAI, v60-agentic, v60-finance
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
import time

_HERE         = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR  = os.path.dirname(_HERE)
_PROJECT_ROOT = os.path.dirname(_CHATBOT_DIR)
_WORKER          = os.path.join(_HERE, "run_query_worker.py")
_ENV_FILE        = os.path.join(_CHATBOT_DIR, ".env")
_RUN_RECORDS_DIR = os.path.join(_CHATBOT_DIR, "run_records")

_VENV_PYTHON = os.path.join(_CHATBOT_DIR, ".venv", "Scripts", "python.exe")
if not os.path.exists(_VENV_PYTHON):
    _VENV_PYTHON = sys.executable

# ── production provider/model ─────────────────────────────────────────────────
_PROD_PROVIDER = "anthropic"
_PROD_MODEL    = "claude-sonnet-4-6"

# ── dev-lane originals (restored on exit) ────────────────────────────────────
_DEV_PROVIDER = "ollama-cloud"
_DEV_MODEL    = "gpt-oss:120b"

# ── cost caps ─────────────────────────────────────────────────────────────────
_CAP_PER_RUN = 1.50
_CAP_TOTAL   = 6.00

# ── F2022 env overrides ───────────────────────────────────────────────────────
_F2022_ENV = {
    "CLUSTER_RESULTS_FILE_OVERRIDE":
        "chatbot/data/alt_wave_F2022/clust_ensembled_results_F2022.csv",
    "LIFT_TABLE_FILE_OVERRIDE":
        "chatbot/data/alt_wave_F2022/skill_lift_table_F2022.csv",
    "FREQ_WAVE_OVERRIDE": "F2022",
    "DATA_WAVE_LABEL": "Fall 2022 (F2022)",
    "MEMBERSHIP_CONFIDENCE_FILE_OVERRIDE":
        "chatbot/data/alt_wave_F2022/cluster_membership_confidence_F2022.csv",
    "CLUSTER_THEMES_OVERRIDE_JSON": (
        '{"1": "Life Sciences & Clinical Research", '
        '"2": "Emerging Niche AI Tooling & Health Informatics '
        '(near-zero frequency in Fall 2022)", '
        '"3": "Deep Learning, Computer Vision & ML Engineering", '
        '"4": "Python, Machine Learning, Data Science & Statistics", '
        '"5": "Data Storytelling, Analytics & Business Intelligence", '
        '"6": "Strategy, Consulting & Customer-Facing Business", '
        '"7": "Business Analysis, Requirements & Office Tools", '
        '"8": "SQL Databases, BI Tools & Data Management", '
        '"9": "Niche Engineering & Software Terms (heterogeneous)", '
        '"10": "Data Engineering, Cloud & Software Development"}'
    ),
}

# ── queries ───────────────────────────────────────────────────────────────────
Q_A2 = (
    "Design a graduate AI/ML curriculum of about 8-10 courses grounded in "
    "the most recent wave of labour-market demand. Use the demand skill "
    "clusters as the backbone, and for each course give a title, the "
    "cluster(s) and key skills it covers, and a brief rationale grounded in "
    "how distinctively those skills are demanded."
)
Q_MMAI = (
    "Compare the Queen's MMAI programme against current labour-market demand: "
    "which in-demand skills does it cover, which is it missing, and which of "
    "its topics look weakly supported by current demand?"
)
Q_AGENTIC = (
    "I'm updating my AI/ML Master's curriculum and want to know whether "
    "agentic AI warrants its own dedicated course rather than a module inside "
    "the existing machine-learning course. Using the market data: which skills "
    "are most distinctively in demand for agentic AI (report lift and "
    "statistical significance, not just raw frequency); which existing "
    "analyst/BI-oriented skills is agentic AI actually not associated with; "
    "how do peer programs currently cover agentic AI; and what recent industry "
    "developments should shape the course? Give concrete, grounded "
    "recommendations."
)
Q_FIN = (
    "Design a finance-focused AI/ML Master's curriculum grounded in the "
    "market data. Cover both the core agentic-AI skills every such program "
    "needs and the finance-specific skills this sector distinctively demands. "
    "Report lift and statistical significance (z) for the skills you cite, "
    "and give concrete course recommendations."
)
# ── §4.6 re-run queries (v60 Part D, 2026-11-03) ─────────────────────────────
Q_SECTOR = (
    "Using the sector-specific demand analysis, what agentic-AI skills are "
    "distinctively in demand for finance roles versus healthcare roles? For "
    "each sector, show the shared core skills and the sector-specific "
    "additions, and state whether that sector sits at, above, or below the "
    "overall market rate for agentic AI."
)
Q_AGENTIC_CL = (
    "We're considering how to teach agentic AI. Based on current "
    "labour-market demand, what skills most distinguish agentic-AI roles "
    "from AI roles generally, and should agentic AI be its own course or "
    "folded into an existing machine-learning or cloud/DevOps course?"
)

# (label, query, use_f2022)
RUNS = [
    ("v60-A2-W2026",   Q_A2,         False),
    ("v60-A2-F2022",   Q_A2,         True),
    ("v60-MMAI",       Q_MMAI,       False),
    ("v60-agentic",    Q_AGENTIC,    False),
    ("v60-finance",    Q_FIN,        False),
    # Part D additions (2026-11-03):
    ("v60-sector-cl",  Q_SECTOR,     False),
    ("v60-agentic-cl", Q_AGENTIC_CL, False),
]


# ── .env helpers ──────────────────────────────────────────────────────────────

def _read_env() -> str:
    with open(_ENV_FILE, encoding="utf-8") as fh:
        return fh.read()


def _set_env_value(content: str, key: str, value: str) -> str:
    """Replace the first non-commented `KEY=...` line with KEY=VALUE."""
    pattern = re.compile(rf"^({re.escape(key)}=)(.*)$", re.MULTILINE)
    new, count = pattern.subn(rf"\g<1>{value}", content, count=1)
    if count == 0:
        raise ValueError(f"Key {key!r} not found in .env — cannot patch.")
    return new


def _switch_env(provider: str, model: str) -> None:
    content = _read_env()
    content = _set_env_value(content, "LLM_PROVIDER", provider)
    content = _set_env_value(content, "LLM_MODEL",    model)
    with open(_ENV_FILE, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  [env] LLM_PROVIDER={provider}  LLM_MODEL={model}", flush=True)


def _confirm_env(expected_provider: str, expected_model: str) -> bool:
    content = _read_env()
    m_p = re.search(r"^LLM_PROVIDER=(.+)$", content, re.MULTILINE)
    m_m = re.search(r"^LLM_MODEL=(.+)$",    content, re.MULTILINE)
    got_p = m_p.group(1).strip() if m_p else "(not found)"
    got_m = m_m.group(1).strip() if m_m else "(not found)"
    ok_p  = got_p == expected_provider
    ok_m  = got_m == expected_model
    icon_p = "✓" if ok_p else "✗"
    icon_m = "✓" if ok_m else "✗"
    print(f"  [{icon_p}] provider : got {got_p!r}  expected {expected_provider!r}")
    print(f"  [{icon_m}] model    : got {got_m!r}  expected {expected_model!r}")
    return ok_p and ok_m


# ── pre-call tool smoke-test (no LLM) ────────────────────────────────────────

def _check_tools() -> bool:
    """Directly call news RAG and web-search tools; return True if both work."""
    print(f"\n{'─'*64}")
    print("TOOL SMOKE-TEST (no LLM)")
    print(f"{'─'*64}")
    sys.path.insert(0, _CHATBOT_DIR)
    from dotenv import load_dotenv
    load_dotenv(_ENV_FILE, override=False)

    ok = True

    # News RAG
    try:
        from tools.news_tool import retrieve as news_retrieve
        results = news_retrieve("agentic AI", k=3)
        if results:
            print(f"  [✓] news_tool: {len(results)} results"
                  f"  first: {results[0].get('title','')[:55]!r}")
        else:
            print("  [✗] news_tool: returned 0 results")
            ok = False
    except Exception as exc:
        print(f"  [✗] news_tool error: {exc}")
        ok = False

    # Web search
    try:
        from tools.web_search_tool import web_search
        raw = web_search("Queen's MMAI curriculum")
        # web_search returns a list of result dicts (or an empty list on failure)
        n = len(raw) if isinstance(raw, (list, tuple)) else (1 if raw else 0)
        if n > 0:
            preview = str(raw)[:100]
            print(f"  [✓] web_search: got {n} results  preview: {preview!r}")
        else:
            print(f"  [✗] web_search: returned 0 results  raw={raw!r}")
            ok = False
    except Exception as exc:
        print(f"  [✗] web_search error: {exc}")
        ok = False

    status = "TOOL SMOKE-TEST PASS ✓" if ok else "TOOL SMOKE-TEST FAIL ✗"
    print(f"\n  {status}")
    print(f"{'─'*64}\n")
    return ok


# ── cost parsing ──────────────────────────────────────────────────────────────

def _parse_cost(run_record_path: str) -> float | None:
    """Extract the 'Approx. cost: $X.XX' line from a run record. Returns None if absent."""
    try:
        with open(run_record_path, encoding="utf-8") as fh:
            text = fh.read()
        m = re.search(r"Approx\. cost:\s*\$([0-9]+\.[0-9]+)", text)
        return float(m.group(1)) if m else None
    except OSError:
        return None


# ── subprocess runner ─────────────────────────────────────────────────────────

def _run_one(label: str, query: str, use_f2022: bool) -> tuple[bool, float | None]:
    """Spawn a fresh Python process for one query.
    Returns (success, cost_usd).  cost_usd is None if not parseable.
    """
    print(f"\n{'='*72}")
    print(f"RUN: {label}  {'[F2022]' if use_f2022 else '[W2026]'}")
    print(f"{'='*72}\n")

    env = os.environ.copy()
    env["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    env["PYTHONIOENCODING"]     = "utf-8"
    # Do NOT set LLM_PROVIDER/LLM_MODEL here — let the worker read them from .env
    if use_f2022:
        env.update(_F2022_ENV)
    else:
        for k in _F2022_ENV:
            env.pop(k, None)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                     delete=False, encoding="utf-8") as tf:
        tf.write(query)
        query_file = tf.name

    # Snapshot run records before the call to identify the new file
    before = set(os.listdir(_RUN_RECORDS_DIR)) if os.path.isdir(_RUN_RECORDS_DIR) else set()

    try:
        cmd = [_VENV_PYTHON, _WORKER, "--label", label, "--query-file", query_file]
        t0     = time.time()
        result = subprocess.run(cmd, env=env, cwd=_PROJECT_ROOT)
        elapsed = time.time() - t0
        success = (result.returncode == 0)
        print(f"\n[{'OK' if success else 'FAIL'}] {label}  exit={result.returncode}  "
              f"wall={elapsed:.0f}s")
    finally:
        try:
            os.unlink(query_file)
        except OSError:
            pass

    # Parse cost from the newly written run record
    cost = None
    if os.path.isdir(_RUN_RECORDS_DIR):
        after   = set(os.listdir(_RUN_RECORDS_DIR))
        new     = sorted(after - before)
        for fname in new:
            if label in fname:
                c = _parse_cost(os.path.join(_RUN_RECORDS_DIR, fname))
                if c is not None:
                    cost = c
                    break
        if cost is not None:
            print(f"  cost: ${cost:.2f}")
        else:
            print("  cost: not parseable from run record")

    return success, cost


# ── secret scan ───────────────────────────────────────────────────────────────

def _secret_scan() -> bool:
    """Scan new run records for obvious API-key patterns. Returns True if clean."""
    print(f"\n{'─'*64}")
    print("SECRET SCAN")
    print(f"{'─'*64}")
    from agents.orchestrator import _RUN_RECORDS_DIR
    patterns = [
        re.compile(r"sk-ant-api[0-9A-Za-z\-]{20,}"),
        re.compile(r"sk-[A-Za-z0-9]{40,}"),
    ]
    flagged = []
    try:
        for fname in sorted(os.listdir(_RUN_RECORDS_DIR)):
            if not fname.startswith("run_"):
                continue
            # Only scan files written today (run_20261102…) plus any v60- records
            if not ("20261102" in fname or "v60-" in fname):
                continue
            path = os.path.join(_RUN_RECORDS_DIR, fname)
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
            for pat in patterns:
                if pat.search(text):
                    flagged.append(fname)
                    break
    except OSError as e:
        print(f"  [WARN] could not scan run_records: {e}")
        return True  # non-fatal

    if flagged:
        print(f"  [✗] POSSIBLE SECRETS in: {flagged}")
        return False
    print("  [✓] no API-key patterns found in today's run records")
    print(f"{'─'*64}\n")
    return True


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", default=None,
                        help="Run only the run with this label.")
    args = parser.parse_args()

    runs_to_do = [r for r in RUNS if args.only is None or r[0] == args.only]
    if not runs_to_do:
        print(f"[ERROR] --only={args.only!r} did not match any label.")
        sys.exit(1)

    print(f"\n{'='*72}")
    print("STAGE 2 — PRODUCTION RUNS (Anthropic/claude-sonnet-4-6)")
    print(f"{'='*72}\n")

    # ── step 1: switch .env to production ────────────────────────────────────
    print("Step 1: switching .env to production …")
    _switch_env(_PROD_PROVIDER, _PROD_MODEL)

    aborted = False
    results = []
    total_cost = 0.0

    try:
        # ── step 2: confirm provider + model ─────────────────────────────────
        print("\nStep 2: confirming provider + model in .env …")
        if not _confirm_env(_PROD_PROVIDER, _PROD_MODEL):
            print("\n[ABORT] .env confirmation failed — cannot proceed.")
            aborted = True
            return

        # ── step 3: tool smoke-test (no LLM) ─────────────────────────────────
        print("\nStep 3: tool smoke-test …")
        sys.path.insert(0, _CHATBOT_DIR)
        if not _check_tools():
            print("\n[ABORT] tool smoke-test failed — no paid calls made.")
            aborted = True
            return

        # ── step 4: production runs ───────────────────────────────────────────
        print("\nStep 4: production runs …")
        for label, query, use_f2022 in runs_to_do:
            success, cost = _run_one(label, query, use_f2022)
            results.append((label, success, cost))

            if not success:
                print(f"\n[ABORT] {label} failed (non-zero exit). Stopping.")
                aborted = True
                break

            if cost is not None:
                if cost > _CAP_PER_RUN:
                    print(f"\n[ABORT] {label} cost ${cost:.2f} exceeds per-run cap "
                          f"${_CAP_PER_RUN:.2f}. Stopping before next run.")
                    aborted = True
                    break
                total_cost += cost
                if total_cost > _CAP_TOTAL:
                    print(f"\n[ABORT] running total ${total_cost:.2f} exceeds total cap "
                          f"${_CAP_TOTAL:.2f}. Stopping.")
                    aborted = True
                    break

    finally:
        # ── step 5: restore .env regardless of outcome ───────────────────────
        print("\nStep 5: restoring .env to dev lane …")
        try:
            _switch_env(_DEV_PROVIDER, _DEV_MODEL)
            _confirm_env(_DEV_PROVIDER, _DEV_MODEL)
        except Exception as e:
            print(f"  [ERROR] could not restore .env: {e}")
            print("  ACTION REQUIRED: manually set LLM_PROVIDER=ollama-cloud "
                  "and LLM_MODEL=gpt-oss:120b in chatbot/.env")

    # ── step 6: secret scan ───────────────────────────────────────────────────
    _secret_scan()

    # ── summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*72}")
    print("STAGE 2 SUMMARY")
    print(f"{'='*72}")
    for label, ok, cost in results:
        cost_str = f"${cost:.2f}" if cost is not None else "cost=n/a"
        print(f"  {'✓' if ok else '✗'}  {label}  {cost_str}")
    if results:
        parseable = [c for _, _, c in results if c is not None]
        if parseable:
            print(f"\n  Total cost (parseable runs): ${sum(parseable):.2f}")
    if aborted:
        print("\n  [ABORTED] — see log above for reason.")
    else:
        not_run = [r[0] for r in RUNS if r[0] not in {r[0] for r in results}]
        if not_run:
            print(f"\n  Not run (--only filter): {not_run}")
    print()


if __name__ == "__main__":
    main()
