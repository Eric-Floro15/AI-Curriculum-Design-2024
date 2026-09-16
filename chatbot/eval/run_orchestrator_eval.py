"""
run_orchestrator_eval.py — End-to-end eval for the full 5-agent crew.

2026-09-16 (SUITE_step2_harness-fix-and-devsmoke.md): REFACTORED onto the
production, persisting run_query() path (agents/orchestrator.py) — the
SAME path RUN2E/RUN2F's real Sonnet sector deliverables used. Previously
this harness built its own separate Crew/Task and never called
run_query(), never wrote chatbot/run_records/, never ran the five
fabrication guards, and never captured cost — so running the §4.6
battery through it would have validated a different, unguarded system
than the one described in the paper, and produced no flag or cost data.

Each case now:
  - calls run_query() directly (same agents, same Task, same guards,
    same _write_run_record() call this project's production/paper runs
    use);
  - locates the run_records/ entry that call just wrote (by directory-
    listing diff — run_query() returns only the answer string, not the
    path, so the harness recovers it the same way this session's own
    ad hoc "re-scan a saved run record" work did) and reads back its
    Metrics + Cost/Usage sections from the _full.md companion;
  - grades on what's reliably checkable from that record: must_delegate_to
    and expected_substrings (soft -> INSPECT) plus forbidden_substrings
    (hard -> FAIL, the pre-existing known-junk-pattern check, distinct
    from and complementary to the five guards). Guard flags and cost are
    recorded and reported PER CASE but deliberately do NOT drive the
    verdict — "a legitimate case can draw a false-positive or a benign
    comment" (spec) — review them, don't gate on them.

Consequence of running through run_query() (verbose=False internally, no
console tool-call log exposed to the caller): the OLD max_tool_calls
budget check is no longer measurable from here and has been dropped —
the per-Agent max_iter caps in agents/*.py remain the real backstop
against a runaway/expensive loop. max_wall_time_sec is still measured
(the harness times the run_query() call itself) and still enforced.

Applies, per case:
  1. expected_substrings    — every listed substring (case-insensitive)
                              MUST appear in the answer. Comma-normalised
                              numeric matching preserved ("39,040" ==
                              "39040").
  2. forbidden_substrings   — none of these may appear. Known-junk-pattern
                              check, kept as a hard failure (a cheap
                              complement to, not a replacement for, the
                              five structural fabrication guards).
  3. must_delegate_to       — each listed sub-agent role MUST appear in
                              the run record's "Delegated to:" line.
  4. max_wall_time_sec      — still enforced (harness-timed).

Guard flags (all five: attribution, numeric, content-attribution,
delegation-claim, plus required_specialist_missing) and cost/usage are
read from the run record and reported per case — informational, not
pass/fail.

Writes a dated snapshot Markdown file next to this script with each
query's full answer, PASS/INSPECT/FAIL grade, guard flags, and cost.
Re-running with the same model on a different day produces a new dated
snapshot.

THIS SCRIPT INTENTIONALLY RUNS THE LIVE LLM. Cost on Sonnet 4.6 is
approximately $0.30-0.66 per query depending on how many specialists get
delegated to (see SUITE_step1's per-case cost estimate). The hard
`max_iter` caps in the Agent constructors bound the worst case (see
chatbot/agents/*.py).

Run:
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py --only data-eng-curriculum-update
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py --provider anthropic --model claude-sonnet-4-6

    # Local Ollama (slow on CPU — skip the wall-time budget check):
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py \\
        --provider ollama --model qwen2.5:14b --no-time-check
"""

import argparse
import glob
import os
import re
import sys
import threading
import time
from datetime import date

# ── LangSmith tracing — must be configured BEFORE any LangChain/CrewAI import ─
# Load .env first so LANGSMITH_API_KEY is available, then set the LangChain
# tracing vars. Doing this here (module level) rather than inside main() or
# llm.py ensures LangChain picks them up during its own module-level init.
_here_eval = os.path.dirname(os.path.abspath(__file__))
_chatbot_dir = os.path.dirname(_here_eval)
sys.path.insert(0, _chatbot_dir)

from dotenv import load_dotenv as _load_dotenv  # noqa: E402
_load_dotenv(os.path.join(_chatbot_dir, ".env"))

os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
os.environ.setdefault("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
os.environ.setdefault("LANGCHAIN_PROJECT", "mitacs-agents-research")

_ls_key = os.getenv("LANGSMITH_API_KEY") or os.getenv("LANGCHAIN_API_KEY")
if _ls_key:
    os.environ["LANGCHAIN_API_KEY"] = _ls_key
else:
    print("⚠️  WARNING: LANGSMITH_API_KEY not found in chatbot/.env — LangSmith tracing disabled.")

# ── Silence CrewAI's telemetry / "Tracing is disabled" banner ─────────────
# Use direct assignment (not setdefault) so these always win, even if
# .env or the shell environment has conflicting values. CrewAI checks
# CREWAI_TELEMETRY_OPT_OUT at Telemetry() call time; OTEL_SDK_DISABLED
# shuts down the OpenTelemetry SDK before any tracer is registered.
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

# ── Helpers ────────────────────────────────────────────────────────────────


def _substring_match(needle: str, haystack: str) -> bool:
    """Case-insensitive substring check with number-comma normalisation.

    Treats '39,040' and '39040' as equivalent so models that format
    numbers without comma separators still pass numeric assertions.
    Both needle and haystack have commas stripped before comparison,
    but only when the needle itself contains a digit (avoids over-
    normalising non-numeric strings that happen to contain commas).
    """
    needle_lc = needle.lower()
    haystack_lc = haystack.lower()
    if needle_lc in haystack_lc:
        return True
    if any(c.isdigit() for c in needle):
        if needle_lc.replace(",", "") in haystack_lc.replace(",", ""):
            return True
    return False


import yaml
import litellm
from langsmith.run_trees import RunTree

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

QUERIES_FILE = os.path.join(_HERE, "orchestrator_queries.yaml")


# ── Run-record parsing (reads back what run_query() just wrote) ───────────
# run_query() (agents/orchestrator.py) returns only the final answer
# string — it doesn't hand the caller a path, delegated_to, guard flags,
# or usage_metrics directly. Rather than change that production function's
# public signature (used by chatbot/app.py too), this harness recovers
# everything it needs the same way this session's own ad hoc "re-scan a
# saved run record" work did: find the run_records/ entry the call just
# wrote (directory-listing diff) and parse its Metrics / Cost-Usage
# sections back out. _write_run_record()'s own format is the parsing
# target, not a guess — see agents/orchestrator.py for the exact fields.

_RECORD_FIELD_RE = {
    "delegated_to": re.compile(r"\*\*Delegated to:\*\* (\[.*?\]|\(none\))"),
    "required_specialist_missing": re.compile(r"\*\*required_specialist_missing:\*\* (\[.*?\])"),
    "fabrication_flags": re.compile(r"\*\*fabrication_flags:\*\* (\[.*\])\s*\n"),
    "model_line": re.compile(r"\*\*Model:\*\* (.+)"),
    "prompt_tokens": re.compile(r"\*\*Prompt tokens:\*\* ([\d,]+)"),
    "completion_tokens": re.compile(r"\*\*Completion tokens:\*\* ([\d,]+)"),
    "total_tokens": re.compile(r"\*\*Total tokens:\*\* ([\d,]+)"),
    "approx_cost": re.compile(r"\*\*Approx\. cost:\*\* \$([\d.]+) USD"),
}


def _list_run_record_files(run_records_dir: str) -> set:
    return set(glob.glob(os.path.join(run_records_dir, "run_*.md")))


def parse_run_record(main_path: str) -> dict:
    """Read back one run_records/ entry (preferring its _full.md
    companion, for the complete untruncated answer text) into the fields
    this harness needs for grading + reporting.
    """
    full_path = main_path[:-len(".md")] + "_full.md"
    read_path = full_path if os.path.exists(full_path) else main_path
    with open(read_path, encoding="utf-8") as f:
        content = f.read()

    def _search(pattern):
        m = pattern.search(content)
        return m.group(1) if m else None

    delegated_raw = _search(_RECORD_FIELD_RE["delegated_to"])
    delegated_to = (
        set(eval(delegated_raw))  # noqa: S307 - trusted local file this process just wrote
        if delegated_raw and delegated_raw != "(none)" else set()
    )
    missing_raw = _search(_RECORD_FIELD_RE["required_specialist_missing"])
    required_missing = eval(missing_raw) if missing_raw else []  # noqa: S307
    flags_raw = _search(_RECORD_FIELD_RE["fabrication_flags"])
    fabrication_flags = eval(flags_raw) if flags_raw else []  # noqa: S307

    answer = ""
    for heading in ("## Final Answer", "## Partial Answer"):
        if heading in content:
            start = content.index(heading) + content[content.index(heading):].index("\n")
            rest = content[start:]
            end_marker = "## Per-Agent Tool-Call Trace"
            answer = (rest[:rest.index(end_marker)] if end_marker in rest else rest).strip()
            break

    return {
        "delegated_to": delegated_to,
        "required_specialist_missing": required_missing,
        "fabrication_flags": fabrication_flags,
        "model_line": _search(_RECORD_FIELD_RE["model_line"]) or "",
        "prompt_tokens": _search(_RECORD_FIELD_RE["prompt_tokens"]),
        "completion_tokens": _search(_RECORD_FIELD_RE["completion_tokens"]),
        "total_tokens": _search(_RECORD_FIELD_RE["total_tokens"]),
        "approx_cost_usd": _search(_RECORD_FIELD_RE["approx_cost"]),
        "answer": answer,
        "record_path": main_path,
    }


def run_single_query(case: dict, hard_timeout_sec: float = 2700) -> dict:
    """Run one case through the production, persisting run_query() path
    and read back what it wrote.

    Returns a dict with:
        answer                      str
        wall_time_sec                float
        delegated_to                 set[str]
        required_specialist_missing  list[str]
        fabrication_flags            list[str]
        model_line / prompt_tokens / completion_tokens / total_tokens /
        approx_cost_usd              str | None (as rendered in the record)
        record_path                  str | None
        error                        str | None

    hard_timeout_sec: a hard kill-switch around run_query(), carried
    forward from the pre-refactor harness's own incident response (a
    qwen3:14b run once sat silent for ~1 hour with no result and no way
    to recover short of killing the process) — wrapped around
    run_query() now instead of a locally-built crew.kickoff(), since
    that's the call that can hang. run_query() runs with verbose=False
    internally, so there's no console log to capture/suppress here
    (the old contextlib.redirect_stdout machinery is gone).
    Default 2700s (45 min), same rationale as before. Python cannot
    forcibly kill a thread blocked inside a network/LLM call, so on
    timeout the worker thread is abandoned (daemon=True — won't block
    process exit, but may keep running in the background until it
    finishes or errors on its own). This unblocks the EVAL LOOP, which
    is the actual goal, not a true kill of the underlying call.
    """
    from agents.orchestrator import run_query  # noqa: E402
    from agents.orchestrator import _RUN_RECORDS_DIR  # noqa: E402

    os.makedirs(_RUN_RECORDS_DIR, exist_ok=True)
    before = _list_run_record_files(_RUN_RECORDS_DIR)

    result_box: dict = {}

    def _kickoff() -> None:
        try:
            result_box["answer"] = run_query(case["query"])
        except Exception as e:
            result_box["error"] = f"{type(e).__name__}: {e}"

    t0 = time.time()
    worker = threading.Thread(target=_kickoff, daemon=True)
    worker.start()
    no_timeout = hard_timeout_sec is None or hard_timeout_sec <= 0
    worker.join(timeout=None if no_timeout else hard_timeout_sec)
    timed_out = (not no_timeout) and worker.is_alive()
    elapsed = time.time() - t0

    after = _list_run_record_files(_RUN_RECORDS_DIR)
    new_files = sorted(f for f in (after - before) if not f.endswith("_full.md"))

    error = None
    if timed_out:
        error = (
            f"TimeoutError: run_query() did not return within the hard "
            f"timeout of {hard_timeout_sec:.0f}s — most likely hung, not "
            f"just slow. Abandoning this query so the eval loop can "
            f"continue; the worker thread may still be running in the "
            f"background."
        )
    elif "error" in result_box:
        error = result_box["error"]

    record: dict | None = None
    if new_files:
        # run_query() writes exactly one main + one _full.md per call;
        # sequential (non-concurrent) case execution means at most one
        # new main file is expected per case — take the newest if >1.
        record = parse_run_record(new_files[-1])
    elif not timed_out:
        # run_query()'s own except clause is deliberately narrow (Gemini
        # quota / API errors only) and still calls _write_run_record()
        # before re-raising in those cases. A genuinely UNCAUGHT
        # exception from crew.kickoff() (e.g. a raw Anthropic/litellm
        # error) propagates with NO record written at all — surface
        # that plainly rather than silently reporting empty fields.
        note = "no run_records/ entry was written for this case"
        error = f"{error} — {note}" if error else note

    return {
        "wall_time_sec": elapsed,
        "delegated_to": record["delegated_to"] if record else set(),
        "required_specialist_missing": record["required_specialist_missing"] if record else [],
        "fabrication_flags": record["fabrication_flags"] if record else [],
        "answer": record["answer"] if record else (result_box.get("answer") or ""),
        "model_line": record["model_line"] if record else "",
        "prompt_tokens": record["prompt_tokens"] if record else None,
        "completion_tokens": record["completion_tokens"] if record else None,
        "total_tokens": record["total_tokens"] if record else None,
        "approx_cost_usd": record["approx_cost_usd"] if record else None,
        "record_path": record["record_path"] if record else None,
        "error": error,
    }


def grade_case(case: dict, result: dict, check_time: bool = True) -> dict:
    """Return a grading dict with three-state verdict.

    2026-09-16 (SUITE_step2): verdict basis changed to what's reliably
    checkable now that this harness reads a real run_records/ entry
    rather than a hand-parsed verbose log. Guard flags (the five
    fabrication guards + required_specialist_missing, all read from the
    record) are reported per case but deliberately do NOT affect the
    verdict — "a legitimate case can draw a false-positive or a benign
    comment" (spec); review them, don't gate on them. Tool-call budget
    checking is gone (not measurable via run_query()'s return value) —
    the per-Agent max_iter caps remain the real backstop.

    Verdict logic:
        PASS    — all assertions met.
        INSPECT — only soft assertions failed (expected_substrings missing
                  or partial delegation). The answer may still be valid; a
                  human should confirm.
        FAIL    — a hard assertion failed: forbidden_substrings appeared
                  (known-junk-pattern check), wall time exceeded, or a
                  genuine runtime/timeout error.
    """
    hard: list[str] = []
    soft: list[str] = []
    answer = result["answer"]

    # ── Soft: expected_substrings ──────────────────────────────────────
    expected = case.get("expected_substrings", []) or []
    missing = [s for s in expected if not _substring_match(s, answer)]
    if missing:
        soft.append(f"missing expected substrings: {missing}")

    # ── Hard: forbidden_substrings ─────────────────────────────────────
    forbidden = case.get("forbidden_substrings", []) or []
    found_forbidden = [s for s in forbidden if _substring_match(s, answer)]
    if found_forbidden:
        hard.append(f"forbidden substrings appeared: {found_forbidden}")

    # ── Soft: must_delegate_to ─────────────────────────────────────────
    expected_delegations = set(case.get("must_delegate_to", []) or [])
    actual = result["delegated_to"]
    if expected_delegations:
        missing_delegations = expected_delegations - actual
        if missing_delegations:
            soft.append(
                f"missing delegations: {sorted(missing_delegations)} "
                f"(actual: {sorted(actual)})"
            )
    else:
        if actual:
            soft.append(
                f"unexpected delegations for no-delegation query: {sorted(actual)}"
            )

    # ── Hard: wall-time budget ─────────────────────────────────────────
    budget = case.get("budget", {}) or {}
    if check_time:
        max_time = budget.get("max_wall_time_sec")
        if max_time is not None and result["wall_time_sec"] > max_time:
            hard.append(
                f"wall time exceeded: {result['wall_time_sec']:.1f}s > {max_time}s"
            )

    # ── Hard: runtime error ────────────────────────────────────────────
    if result["error"]:
        hard.append(f"runtime error: {result['error']}")

    # ── Verdict ─────────────────────────────────────────────────────────
    if hard:
        verdict = "FAIL"
    elif soft:
        verdict = "INSPECT"
    else:
        verdict = "PASS"

    return {"verdict": verdict, "hard": hard, "soft": soft}


def model_slug() -> str:
    """Short identifier for the snapshot filename."""
    provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
    if provider == "anthropic":
        return os.getenv("LLM_MODEL", "claude-sonnet-4-6")
    if provider == "openai":
        return os.getenv("LLM_MODEL", "gpt-4o")
    if provider == "gemini":
        return os.getenv("LLM_MODEL", "gemini-1.5-pro")
    if provider == "ollama":
        return f"ollama-{os.getenv('LLM_MODEL', 'llama3.1:8b')}"
    if provider == "ollama-cloud":
        return f"ollama-cloud-{os.getenv('LLM_MODEL', 'gpt-oss:120b')}"
    return f"{provider}-{os.getenv('LLM_MODEL', 'default')}"


def _safe_slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", s)


def write_snapshot(
    cases: list[dict],
    results: list[dict],
    grades: list[dict],
) -> str:
    today = date.today().isoformat()
    slug = _safe_slug(model_slug())
    path = os.path.join(_HERE, f"orchestrator_baseline_{today}_{slug}.md")

    n_total = len(cases)
    n_pass    = sum(1 for g in grades if g["verdict"] == "PASS")
    n_inspect = sum(1 for g in grades if g["verdict"] == "INSPECT")
    n_fail    = sum(1 for g in grades if g["verdict"] == "FAIL")
    n_flagged = sum(1 for r in results if r["fabrication_flags"])

    body: list[str] = [
        f"# Orchestrator end-to-end baseline — {today}",
        "",
        "## Run config",
        f"- model: `{model_slug()}`",
        f"- queries run: {n_total}",
        f"- PASS: {n_pass}",
        f"- INSPECT: {n_inspect}  _(soft failures only — review manually)_",
        f"- FAIL: {n_fail}",
        f"- cases with >=1 guard flag: {n_flagged}  _(informational — does not affect verdict; review manually)_",
        "",
        "Verdict key: **PASS** all assertions met · "
        "**INSPECT** only soft assertions failed (check phrasing/delegation) · "
        "**FAIL** hard assertion violated (known-junk pattern / budget / runtime error)",
        "",
        "Every case ran through the persisting `run_query()` path "
        "(chatbot/agents/orchestrator.py) — each has a real "
        "`chatbot/run_records/` entry + `_full.md` companion, was "
        "evaluated by the five fabrication guards in FLAG mode, and has "
        "real token/USD cost captured. Guard flags are reported below "
        "per case but do NOT drive the verdict.",
        "",
        f"Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py`",
        "",
        "## Per-query summary",
        "",
        "| ID | verdict | delegations | guard flags | cost (USD) | wall (s) |",
        "|---|---|---|---|---|---|",
    ]
    for case, result, grade in zip(cases, results, grades):
        cost = result["approx_cost_usd"]
        cost_str = f"${cost}" if cost else ("n/a" if result["total_tokens"] else "unavailable")
        body.append(
            f"| {case['id']} | {grade['verdict']} "
            f"| {sorted(result['delegated_to'])} "
            f"| {len(result['fabrication_flags'])} "
            f"| {cost_str} "
            f"| {result['wall_time_sec']:.1f} |"
        )

    body.append("")
    body.append("---")
    body.append("")

    for case, result, grade in zip(cases, results, grades):
        verdict = grade["verdict"]
        cost = result["approx_cost_usd"]
        body += [
            f"## [{case['id']}] **{verdict}**",
            "",
            f"**Category:** {case.get('category', '—')}",
            "",
            "**Query:**",
            "",
            "```",
            case["query"].strip(),
            "```",
            "",
            f"**Wall time:** {result['wall_time_sec']:.1f}s",
            f"**Delegated to:** {sorted(result['delegated_to']) or '(none)'}",
            f"**required_specialist_missing:** {result['required_specialist_missing'] or '[]'}",
            f"**Model:** {result['model_line'] or '(unavailable — no run record)'}",
            f"**Tokens:** prompt={result['prompt_tokens']}, "
            f"completion={result['completion_tokens']}, "
            f"total={result['total_tokens']}",
            f"**Approx. cost:** {'$' + cost + ' USD' if cost else 'not estimated / usage unavailable'}",
            f"**Run record:** {result['record_path'] or '(none written)'}",
            "",
        ]
        if grade["hard"]:
            body.append("**Hard failures (FAIL):**")
            for msg in grade["hard"]:
                body.append(f"- {msg}")
            body.append("")
        if grade["soft"]:
            body.append("**Soft failures (INSPECT):**")
            for msg in grade["soft"]:
                body.append(f"- {msg}")
            body.append("")
        if result["fabrication_flags"]:
            body.append(
                f"**Guard flags ({len(result['fabrication_flags'])}, informational — "
                f"does not affect verdict, review manually):**"
            )
            for flag in result["fabrication_flags"]:
                body.append(f"- {flag}")
            body.append("")
        body += [
            "**Orchestrator's final answer:**",
            "",
            result["answer"] or "*(no answer produced — see the run record, if any, for details)*",
            "",
            "---",
            "",
        ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(body))
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="End-to-end Orchestrator eval.")
    parser.add_argument(
        "--only",
        type=str,
        default=None,
        help="Run only the query with this id (or comma-separated list).",
    )
    parser.add_argument(
        "--provider",
        type=str,
        default=None,
        help="Override LLM_PROVIDER for this run.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Override LLM_MODEL for this run.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse the queries file and print what would run, then exit.",
    )
    parser.add_argument(
        "--no-time-check",
        action="store_true",
        help=(
            "Skip the wall-time budget assertion. Recommended for local "
            "Ollama models running on CPU (e.g. qwen2.5:14b) where latency "
            "is a hardware constraint, not a quality signal."
        ),
    )
    parser.add_argument(
        "--hard-timeout-sec",
        type=float,
        default=2700.0,
        help=(
            "Hard kill-switch (in seconds) around each query's run_query() "
            "call. Default 2700s (45 min). Lower this for fast-fail "
            "debugging. Pass 0 (or any value <= 0) to DISABLE the "
            "kill-switch entirely and block forever — use this if you "
            "deliberately want to let a known-slow (not hung) run finish "
            "on its own. See run_single_query()'s docstring for the full "
            "rationale."
        ),
    )
    args = parser.parse_args()

    if args.provider:
        os.environ["LLM_PROVIDER"] = args.provider
    if args.model:
        os.environ["LLM_MODEL"] = args.model

    # dotenv already loaded at module level (top of file) before LangChain init.

    with open(QUERIES_FILE, encoding="utf-8") as f:
        all_cases = yaml.safe_load(f)
    # Strip any anchor-only entries (those start with underscore).
    cases = [c for c in all_cases if not str(c.get("id", "")).startswith("_")]

    if args.only:
        wanted = set(s.strip() for s in args.only.split(","))
        cases = [c for c in cases if c["id"] in wanted]
        if not cases:
            sys.exit(f"No queries matched --only {args.only!r}")

    print(f"Loaded {len(cases)} queries from {os.path.basename(QUERIES_FILE)}.")
    print(f"LLM: provider={os.getenv('LLM_PROVIDER', 'anthropic')}, "
          f"model={model_slug()}.")
    print("Each case runs through the persisting run_query() path — "
          "writes run_records/ + _full.md, runs the 5 fabrication guards "
          "in FLAG mode, captures cost.")
    if args.hard_timeout_sec <= 0:
        print("Hard timeout per query: DISABLED (--hard-timeout-sec <= 0) — "
              "will block forever on a hang.")
    else:
        print(f"Hard timeout per query: {args.hard_timeout_sec:.0f}s "
              f"(override with --hard-timeout-sec, or pass 0 to disable).")

    if args.dry_run:
        print("\n--dry-run: would run these queries:")
        for c in cases:
            ed = c.get("must_delegate_to", []) or []
            print(f"  [{c['id']:35s}] {c.get('category', '?'):15s} "
                  f"must_delegate_to={ed} "
                  f"budget={c.get('budget', {})}")
        return

    # ── LangSmith: eval-level parent run ──────────────────────────────────────
    # Wraps the entire script execution as one top-level run in LangSmith.
    # Structure: eval run → query run (per case) → LLM calls (via LiteLLM cb)
    # Gracefully disabled when LANGCHAIN_API_KEY is absent.
    _ls_enabled = bool(os.getenv("LANGCHAIN_API_KEY"))
    eval_run: "RunTree | None" = None
    if _ls_enabled:
        eval_run = RunTree(
            name=f"eval / {date.today().isoformat()} / {model_slug()}",
            run_type="chain",
            inputs={
                "model": model_slug(),
                "case_ids": [c["id"] for c in cases],
            },
            project_name=os.getenv("LANGCHAIN_PROJECT", "mitacs-agents-research"),
        )
        eval_run.post()

    results: list[dict] = []
    grades: list[dict] = []
    for i, case in enumerate(cases, 1):
        print(f"\n[{i}/{len(cases)}] {case['id']} — running...")

        # ── LangSmith: query-level child run ──────────────────────────────────
        query_run: "RunTree | None" = None
        if eval_run is not None:
            query_run = eval_run.create_child(
                name=case["id"],
                run_type="chain",
                inputs={
                    "query": case["query"].strip(),
                    "category": case.get("category", ""),
                },
            )
            query_run.post()
            litellm.metadata = {"parent_run_id": str(query_run.id)}

        try:
            result = run_single_query(case, hard_timeout_sec=args.hard_timeout_sec)
            grade = grade_case(case, result, check_time=not args.no_time_check)
        finally:
            litellm.metadata = {}

        results.append(result)
        grades.append(grade)

        if query_run is not None:
            query_run.end(outputs={
                "verdict": grade["verdict"],
                "answer": result["answer"],
                "wall_time_sec": round(result["wall_time_sec"], 1),
                "delegated_to": sorted(result["delegated_to"]),
                "fabrication_flags": result["fabrication_flags"],
                "approx_cost_usd": result["approx_cost_usd"],
                "hard_failures": grade["hard"],
                "soft_failures": grade["soft"],
            })
            query_run.patch()

        verdict = grade["verdict"]
        symbol = {"PASS": "✅", "INSPECT": "🔍", "FAIL": "❌"}.get(verdict, "?")
        cost = result["approx_cost_usd"]
        print(f"  {symbol} {verdict}  "
              f"wall={result['wall_time_sec']:.1f}s, "
              f"delegated={sorted(result['delegated_to'])}, "
              f"flags={len(result['fabrication_flags'])}, "
              f"cost={'$' + cost if cost else 'n/a'}")
        for msg in grade["hard"]:
            print(f"    ❌ [hard] {msg}")
        for msg in grade["soft"]:
            print(f"    🔍 [soft] {msg}")
        if result["fabrication_flags"]:
            print(f"    ⚠️  {len(result['fabrication_flags'])} guard flag(s) — see snapshot for detail")

    snapshot_path = write_snapshot(cases, results, grades)
    n_pass    = sum(1 for g in grades if g["verdict"] == "PASS")
    n_inspect = sum(1 for g in grades if g["verdict"] == "INSPECT")
    n_fail    = sum(1 for g in grades if g["verdict"] == "FAIL")
    n_flagged = sum(1 for r in results if r["fabrication_flags"])

    if eval_run is not None:
        eval_run.end(outputs={
            "n_pass": n_pass,
            "n_inspect": n_inspect,
            "n_fail": n_fail,
            "n_flagged": n_flagged,
            "summary": f"{n_pass} PASS | {n_inspect} INSPECT | {n_fail} FAIL",
        })
        eval_run.patch()

    print()
    print("=" * 72)
    print(f"SUMMARY: {n_pass} PASS  |  {n_inspect} INSPECT  |  {n_fail} FAIL  "
          f"(out of {len(cases)})  |  {n_flagged} case(s) with guard flags")
    print(f"Snapshot: {snapshot_path}")


if __name__ == "__main__":
    main()
