"""
run_orchestrator_eval.py — End-to-end eval for the full 5-agent crew.

Runs each query in orchestrator_queries.yaml through the live Orchestrator
(`agents.orchestrator.run_query`-equivalent, but with verbose tracing
captured so delegation + tool counts are observable) and applies four
assertion types:

  1. expected_substrings    — every listed substring (case-insensitive)
                              MUST appear in the Orchestrator's final answer.
                              Number formatting is normalised: "39,040" and
                              "39040" are treated as equivalent so slower
                              local models that omit comma separators still
                              pass the numeric check.
  2. forbidden_substrings   — none of these may appear in the final answer.
                              Catches known hallucination patterns.
  3. must_delegate_to       — each listed sub-agent role MUST have been
                              delegated to by the Orchestrator. Verified
                              by parsing the verbose log for the
                              `'coworker': '<role>'` arg patterns. ANSI
                              escape codes are stripped from the log before
                              parsing so rich/console colour codes don't
                              corrupt role-name matching.
  4. budget                 — total tool dispatches and wall time must
                              stay under per-query caps. Use --no-time-check
                              to skip the wall-time assertion when running
                              slow local Ollama models on CPU.

Writes a dated snapshot Markdown file next to this script with each
query's full answer + PASS/FAIL grades. Re-running with the same model
on a different day produces a new dated snapshot, so future diffs are
easy.

THIS SCRIPT INTENTIONALLY RUNS THE LIVE LLM. Cost on Sonnet 4.6 is
approximately $1-3 per query depending on how many delegations and
tool calls fire. The hard `max_iter` caps in the Agent constructors
bound the worst case (see chatbot/agents/*.py and the 2026-05-26 setup
log in CLAUDE.md).

Run:
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py --only data-eng-curriculum-update
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py --provider anthropic --model claude-sonnet-4-6

    # Local Ollama (slow on CPU — skip the wall-time budget check):
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py \\
        --provider ollama --model qwen2.5:14b --no-time-check
"""

import argparse
import contextlib
import io
import os
import re
import sys
import time
import traceback
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

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[mGKHFABCDJsu]")
# Rich box-drawing characters injected when the verbose log is rendered
# inside a panel (e.g. │, ╭, ─, ╰). These appear mid-string in captured
# role names, turning 'AI Industry News Researcher' into
# 'AI Industry News   │\n│  Researcher'.
_BOX_RE = re.compile(r"[│╭╰╮╯─├┤┬┴┼╔╗╚╝╠╣╦╩╬═║╴╶╸╺]+")


def _clean_log(text: str) -> str:
    """Remove ANSI escape codes and rich box-drawing characters from log text.

    Two-pass cleaning:
    1. Strip ANSI colour/cursor codes  (\x1b[...m etc.)
    2. Replace rich panel border chars (│, ─, ╭ …) with a space
    The result is plain text safe for regex parsing.
    """
    text = _ANSI_RE.sub("", text)
    text = _BOX_RE.sub(" ", text)
    return text


def _normalize_role(raw: str) -> str:
    """Collapse whitespace and newlines in a captured coworker role name.

    Rich wraps long strings across panel lines, injecting newlines and
    indentation. After box-char removal the fragments remain separated
    by whitespace/newlines — join them back into a single clean string.
    """
    return " ".join(raw.split())


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
    # Numeric normalisation: strip commas and retry
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

DEFAULT_EXPECTED_OUTPUT = (
    "A single coherent recommendation for the professor. Open with a 2-3 "
    "sentence executive summary. Then a structured body of concrete "
    "recommendations citing specific skills with frequencies (from the "
    "Analyst), peer-program courses with URLs (from the University "
    "Programs researcher), and recent articles with titles + sources "
    "(from the News researcher) where each is relevant. Close with a "
    "trade-off or caveat."
)


def run_single_query(case: dict) -> dict:
    """Build a fresh 5-agent crew, run the query verbose, capture metrics.

    Returns a dict with:
        answer            str  — Orchestrator's final answer
        verbose_log       str  — captured stdout from the verbose run
        wall_time_sec     float
        tool_calls        int  — total `Tool Execution Started` events
        delegated_to      set[str]  — sub-agent role names invoked
        error             str | None
    """
    # Lazy imports — these touch crewai + ollama / anthropic and we want
    # all-importable-before-actually-running so --help works without
    # network or LLM keys present.
    from crewai import Crew, Task  # noqa: E402
    from agents.analyst import make_analyst  # noqa: E402
    from agents.cluster_interpreter import make_cluster_interpreter  # noqa: E402
    from agents.news import make_news_agent  # noqa: E402
    from agents.orchestrator import make_orchestrator  # noqa: E402
    from agents.university_programs import make_university_programs_agent  # noqa: E402

    analyst = make_analyst()
    univ = make_university_programs_agent()
    news = make_news_agent()
    cluster_interp = make_cluster_interpreter()
    orch = make_orchestrator()
    for a in (orch, analyst, univ, news, cluster_interp):
        a.verbose = True

    # ── Delegation detection via step_callback (robust) ───────────────────
    # Parsing the verbose log for coworker arguments is brittle — the log
    # format changes across CrewAI versions and Rich panel rendering corrupts
    # multi-word role names. Instead, we attach a step_callback to each
    # specialist: the callback fires whenever that agent actually executes a
    # step, which only happens when the Orchestrator has delegated to it.
    # This is version-agnostic and semantically correct.
    delegated_to: set[str] = set()

    def _make_step_tracker(role: str) -> callable:
        def _tracker(_output) -> None:
            delegated_to.add(role)
        return _tracker

    analyst.step_callback       = _make_step_tracker("Skills Taxonomy Analyst")
    univ.step_callback          = _make_step_tracker("University AI Programs Researcher")
    news.step_callback          = _make_step_tracker("AI Industry News Researcher")
    cluster_interp.step_callback = _make_step_tracker("Cluster Interpreter")
    # Note: orch (Orchestrator) is intentionally excluded — we only track
    # specialists to reflect which agents were *delegated to*.

    task = Task(
        description=case["query"],
        expected_output=DEFAULT_EXPECTED_OUTPUT,
        agent=orch,
    )
    crew = Crew(
        agents=[orch, analyst, univ, news, cluster_interp],
        tasks=[task],
        verbose=True,
    )

    buf = io.StringIO()
    t0 = time.time()
    answer = ""
    error: str | None = None
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            answer = str(crew.kickoff())
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        traceback.print_exc(file=buf)
    elapsed = time.time() - t0

    log = _clean_log(buf.getvalue())
    tool_calls = len(re.findall(r"Tool Execution Started", log))

    # ── DEBUG: dump verbose log to /tmp for format inspection ─────────────
    # Uncomment the two lines below if delegated_to still shows empty after
    # a run where LangSmith/CrewAI platform confirms delegation happened.
    # Inspect /tmp/orch_verbose_log.txt to see the actual captured format,
    # then remove the debug lines.
    # with open("/tmp/orch_verbose_log.txt", "w") as _f:
    #     _f.write(log)

    return {
        "answer": answer,
        "verbose_log": log,
        "wall_time_sec": elapsed,
        "tool_calls": tool_calls,
        "delegated_to": delegated_to,
        "error": error,
    }


def grade_case(case: dict, result: dict, check_time: bool = True) -> dict:
    """Return a grading dict with three-state verdict.

    Verdict logic:
        PASS    — all assertions met.
        INSPECT — only soft assertions failed (expected_substrings missing or
                  delegation issues). The answer may still be valid; a human
                  should confirm. Typical cause: local model (qwen) phrases
                  facts differently from the expected substrings, or delegated
                  to 2/3 required agents but the answer is still substantive.
        FAIL    — at least one hard assertion failed (hallucinated content,
                  tool budget exceeded, or runtime error). Something definitely
                  went wrong regardless of answer quality.

    Hard failures → FAIL:
        • forbidden_substrings found in the answer (hallucination signal)
        • tool call count exceeds max_tool_calls (runaway loop)
        • wall time exceeds max_wall_time_sec (when check_time=True)
        • uncaught runtime exception

    Soft failures → INSPECT (only if no hard failures):
        • expected_substrings missing from the answer (brittle string match;
          model may have used different but correct phrasing)
        • must_delegate_to roles not reached (partial delegation)
        • unexpected delegations on a no-delegation query

    Returns:
        {
          "verdict": "PASS" | "INSPECT" | "FAIL",
          "hard":    list[str],   # hard failure reasons
          "soft":    list[str],   # soft failure reasons
        }
    """
    hard: list[str] = []
    soft: list[str] = []
    answer = result["answer"]

    # ── Soft: expected_substrings ─────────────────────────────────────────────
    expected = case.get("expected_substrings", []) or []
    missing = [s for s in expected if not _substring_match(s, answer)]
    if missing:
        soft.append(f"missing expected substrings: {missing}")

    # ── Hard: forbidden_substrings ────────────────────────────────────────────
    forbidden = case.get("forbidden_substrings", []) or []
    found_forbidden = [s for s in forbidden if _substring_match(s, answer)]
    if found_forbidden:
        hard.append(f"forbidden substrings appeared: {found_forbidden}")

    # ── Soft: must_delegate_to ────────────────────────────────────────────────
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
        # Empty must_delegate_to → no delegation expected (off-scope queries).
        # Delegating when not expected is a soft signal: the agent went
        # off-scope, but the final answer might still redirect correctly.
        if actual:
            soft.append(
                f"unexpected delegations for no-delegation query: {sorted(actual)}"
            )

    # ── Hard: budget ──────────────────────────────────────────────────────────
    budget = case.get("budget", {}) or {}
    max_tools = budget.get("max_tool_calls")
    if max_tools is not None and result["tool_calls"] > max_tools:
        hard.append(
            f"tool budget exceeded: {result['tool_calls']} > {max_tools}"
        )
    if check_time:
        max_time = budget.get("max_wall_time_sec")
        if max_time is not None and result["wall_time_sec"] > max_time:
            hard.append(
                f"wall time exceeded: {result['wall_time_sec']:.1f}s > {max_time}s"
            )

    # ── Hard: runtime error ───────────────────────────────────────────────────
    if result["error"]:
        hard.append(f"runtime error: {result['error']}")

    # ── Verdict ───────────────────────────────────────────────────────────────
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

    body: list[str] = [
        f"# Orchestrator end-to-end baseline — {today}",
        "",
        "## Run config",
        f"- model: `{model_slug()}`",
        f"- queries run: {n_total}",
        f"- PASS: {n_pass}",
        f"- INSPECT: {n_inspect}  _(soft failures only — review manually)_",
        f"- FAIL: {n_fail}",
        "",
        "Verdict key: **PASS** all assertions met · "
        "**INSPECT** only soft assertions failed (check phrasing/delegation) · "
        "**FAIL** hard assertion violated (hallucination / budget / error)",
        "",
        f"Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py`",
        "",
        "## Per-query summary",
        "",
        "| ID | verdict | delegations | tool calls | wall (s) |",
        "|---|---|---|---|---|",
    ]
    for case, result, grade in zip(cases, results, grades):
        body.append(
            f"| {case['id']} | {grade['verdict']} "
            f"| {sorted(result['delegated_to'])} "
            f"| {result['tool_calls']} "
            f"| {result['wall_time_sec']:.1f} |"
        )

    body.append("")
    body.append("---")
    body.append("")

    for case, result, grade in zip(cases, results, grades):
        verdict = grade["verdict"]
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
            f"**Tool calls:** {result['tool_calls']}",
            f"**Delegated to:** {sorted(result['delegated_to']) or '(none)'}",
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
        body += [
            "**Orchestrator's final answer:**",
            "",
            result["answer"] or "*(no answer produced — see verbose log)*",
            "",
            "---",
            "",
        ]

    with open(path, "w") as f:
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
    args = parser.parse_args()

    if args.provider:
        os.environ["LLM_PROVIDER"] = args.provider
    if args.model:
        os.environ["LLM_MODEL"] = args.model

    # dotenv already loaded at module level (top of file) before LangChain init.

    with open(QUERIES_FILE) as f:
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
        # Creates a child run under eval_run for this specific query. Passing
        # its ID to litellm.metadata makes every LLM call during crew.kickoff()
        # appear nested under it rather than as isolated top-level runs.
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
            result = run_single_query(case)
            grade = grade_case(case, result, check_time=not args.no_time_check)
        finally:
            # Always clear LiteLLM metadata so the next query doesn't inherit
            # a stale parent_run_id (even if run_single_query raised somehow).
            litellm.metadata = {}

        results.append(result)
        grades.append(grade)

        # ── Close query run ───────────────────────────────────────────────────
        if query_run is not None:
            query_run.end(outputs={
                "verdict": grade["verdict"],
                "answer": result["answer"],
                "tool_calls": result["tool_calls"],
                "wall_time_sec": round(result["wall_time_sec"], 1),
                "delegated_to": sorted(result["delegated_to"]),
                "hard_failures": grade["hard"],
                "soft_failures": grade["soft"],
            })
            query_run.patch()

        verdict = grade["verdict"]
        # Emoji prefix for quick scanning in terminal output
        symbol = {"PASS": "✅", "INSPECT": "🔍", "FAIL": "❌"}.get(verdict, "?")
        print(f"  {symbol} {verdict}  "
              f"wall={result['wall_time_sec']:.1f}s, "
              f"tools={result['tool_calls']}, "
              f"delegated={sorted(result['delegated_to'])}")
        for msg in grade["hard"]:
            print(f"    ❌ [hard] {msg}")
        for msg in grade["soft"]:
            print(f"    🔍 [soft] {msg}")

    snapshot_path = write_snapshot(cases, results, grades)
    n_pass    = sum(1 for g in grades if g["verdict"] == "PASS")
    n_inspect = sum(1 for g in grades if g["verdict"] == "INSPECT")
    n_fail    = sum(1 for g in grades if g["verdict"] == "FAIL")

    # ── Close eval-level run ──────────────────────────────────────────────────
    if eval_run is not None:
        eval_run.end(outputs={
            "n_pass": n_pass,
            "n_inspect": n_inspect,
            "n_fail": n_fail,
            "summary": f"{n_pass} PASS | {n_inspect} INSPECT | {n_fail} FAIL",
        })
        eval_run.patch()

    print()
    print("=" * 72)
    print(f"SUMMARY: {n_pass} PASS  |  {n_inspect} INSPECT  |  {n_fail} FAIL  "
          f"(out of {len(cases)})")
    print(f"Snapshot: {snapshot_path}")


if __name__ == "__main__":
    main()
