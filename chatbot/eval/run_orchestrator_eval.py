"""
run_orchestrator_eval.py — End-to-end eval for the full 4-agent crew.

Runs each query in orchestrator_queries.yaml through the live Orchestrator
(`agents.orchestrator.run_query`-equivalent, but with verbose tracing
captured so delegation + tool counts are observable) and applies four
assertion types:

  1. expected_substrings    — every listed substring (case-insensitive)
                              MUST appear in the Orchestrator's final answer.
  2. forbidden_substrings   — none of these may appear in the final answer.
                              Catches known hallucination patterns.
  3. must_delegate_to       — each listed sub-agent role MUST have been
                              delegated to by the Orchestrator. Verified
                              by parsing the verbose log for the
                              `'coworker': '<role>'` arg patterns.
  4. budget                 — total tool dispatches and wall time must
                              stay under per-query caps.

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

import yaml

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
    """Build a fresh 4-agent crew, run the query verbose, capture metrics.

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
    from agents.news import make_news_agent  # noqa: E402
    from agents.orchestrator import make_orchestrator  # noqa: E402
    from agents.university_programs import make_university_programs_agent  # noqa: E402

    analyst = make_analyst()
    univ = make_university_programs_agent()
    news = make_news_agent()
    orch = make_orchestrator()
    for a in (orch, analyst, univ, news):
        a.verbose = True

    task = Task(
        description=case["query"],
        expected_output=DEFAULT_EXPECTED_OUTPUT,
        agent=orch,
    )
    crew = Crew(
        agents=[orch, analyst, univ, news],
        tasks=[task],
        verbose=True,
    )

    buf = io.StringIO()
    t0 = time.time()
    answer = ""
    error: str | None = None
    try:
        # contextlib.redirect_stdout catches `print()`. CrewAI's rich
        # console output also goes through stdout, so this captures
        # both. If a future CrewAI version moves to direct tty writes,
        # we'll need to switch to subprocess.
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            answer = str(crew.kickoff())
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        traceback.print_exc(file=buf)
    elapsed = time.time() - t0

    log = buf.getvalue()
    tool_calls = len(re.findall(r"Tool Execution Started", log))
    delegated_to: set[str] = set()
    # Both delegation tools share the same Args shape; capture both.
    for m in re.finditer(r"'coworker':\s*'([^']+)'", log):
        delegated_to.add(m.group(1))

    return {
        "answer": answer,
        "verbose_log": log,
        "wall_time_sec": elapsed,
        "tool_calls": tool_calls,
        "delegated_to": delegated_to,
        "error": error,
    }


def grade_case(case: dict, result: dict) -> list[str]:
    """Return a list of failure reasons (empty list = PASS)."""
    failures: list[str] = []
    answer_lc = result["answer"].lower()

    # 1. expected_substrings — all must appear
    expected = case.get("expected_substrings", []) or []
    missing = [s for s in expected if s.lower() not in answer_lc]
    if missing:
        failures.append(f"missing expected substrings: {missing}")

    # 2. forbidden_substrings — none may appear
    forbidden = case.get("forbidden_substrings", []) or []
    found_forbidden = [s for s in forbidden if s.lower() in answer_lc]
    if found_forbidden:
        failures.append(f"forbidden substrings appeared: {found_forbidden}")

    # 3. must_delegate_to — all listed roles must have been delegated to
    expected_delegations = set(case.get("must_delegate_to", []) or [])
    actual = result["delegated_to"]
    if expected_delegations:
        missing_delegations = expected_delegations - actual
        if missing_delegations:
            failures.append(
                f"missing delegations: {sorted(missing_delegations)} "
                f"(actual: {sorted(actual)})"
            )
    else:
        # Empty must_delegate_to means "no delegation expected"
        # (used by off-scope queries — Orchestrator should redirect,
        # not fan out). If actual delegations fired, that's a fail.
        if actual:
            failures.append(
                f"unexpected delegations for no-delegation query: {sorted(actual)}"
            )

    # 4. budget
    budget = case.get("budget", {}) or {}
    max_tools = budget.get("max_tool_calls")
    if max_tools is not None and result["tool_calls"] > max_tools:
        failures.append(
            f"tool budget exceeded: {result['tool_calls']} > {max_tools}"
        )
    max_time = budget.get("max_wall_time_sec")
    if max_time is not None and result["wall_time_sec"] > max_time:
        failures.append(
            f"wall time exceeded: {result['wall_time_sec']:.1f}s > {max_time}s"
        )

    # Any uncaught exception from the run is a failure
    if result["error"]:
        failures.append(f"runtime error: {result['error']}")

    return failures


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
    failures: list[list[str]],
) -> str:
    today = date.today().isoformat()
    slug = _safe_slug(model_slug())
    path = os.path.join(_HERE, f"orchestrator_baseline_{today}_{slug}.md")

    n_total = len(cases)
    n_pass = sum(1 for fs in failures if not fs)
    n_fail = n_total - n_pass

    body: list[str] = [
        f"# Orchestrator end-to-end baseline — {today}",
        "",
        "## Run config",
        f"- model: `{model_slug()}`",
        f"- queries run: {n_total}",
        f"- PASS: {n_pass}",
        f"- FAIL: {n_fail}",
        "",
        f"Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py`",
        "",
        "## Per-query summary",
        "",
        "| ID | verdict | delegations | tool calls | wall (s) |",
        "|---|---|---|---|---|",
    ]
    for case, result, fs in zip(cases, results, failures):
        verdict = "PASS" if not fs else "FAIL"
        body.append(
            f"| {case['id']} | {verdict} "
            f"| {sorted(result['delegated_to'])} "
            f"| {result['tool_calls']} "
            f"| {result['wall_time_sec']:.1f} |"
        )

    body.append("")
    body.append("---")
    body.append("")

    for case, result, fs in zip(cases, results, failures):
        verdict = "PASS" if not fs else "FAIL"
        body += [
            f"## [{case['id']}] **{verdict}**",
            "",
            f"**Category:** {case.get('category', '—')}",
            "",
            f"**Query:**",
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
        if fs:
            body.append("**Failures:**")
            for f in fs:
                body.append(f"- {f}")
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
    args = parser.parse_args()

    if args.provider:
        os.environ["LLM_PROVIDER"] = args.provider
    if args.model:
        os.environ["LLM_MODEL"] = args.model

    from dotenv import load_dotenv  # noqa: E402
    load_dotenv(os.path.join(_CHATBOT_DIR, ".env"))

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

    results: list[dict] = []
    failures: list[list[str]] = []
    for i, case in enumerate(cases, 1):
        print(f"\n[{i}/{len(cases)}] {case['id']} — running...")
        result = run_single_query(case)
        fs = grade_case(case, result)
        results.append(result)
        failures.append(fs)
        verdict = "PASS" if not fs else "FAIL"
        print(f"  {verdict}  "
              f"wall={result['wall_time_sec']:.1f}s, "
              f"tools={result['tool_calls']}, "
              f"delegated={sorted(result['delegated_to'])}")
        if fs:
            for f in fs:
                print(f"    - {f}")

    snapshot_path = write_snapshot(cases, results, failures)
    print()
    print("=" * 72)
    n_pass = sum(1 for fs in failures if not fs)
    print(f"SUMMARY: {n_pass}/{len(cases)} PASS")
    print(f"Snapshot: {snapshot_path}")


if __name__ == "__main__":
    main()
