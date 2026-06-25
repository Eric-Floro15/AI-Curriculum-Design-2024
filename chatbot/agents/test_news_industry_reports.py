"""
test_news_industry_reports.py — Agent-level end-to-end test for the
industry-reports corpus (added 2026-06-17) flowing through the LIVE News
agent, not just the offline FAISS index.

Why this exists, and how it differs from the other two News-agent tests
already in this codebase:

  - chatbot/eval/run_news_tests.py's approach_1_reports() tests the
    RETRIEVAL LAYER directly (FAISS.similarity_search(), no LLM, no
    agent) — it answers "does the new corpus rank well in isolation?".
    It also tests the OPPOSITE direction at the agent layer: approach_2()
    runs 5 OFF-CORPUS probes checking the agent is HONEST when the corpus
    has nothing relevant (no fabricated URLs/org names).
  - chatbot/agents/test_news.py is a single generic smoke test (one broad
    "AI agents" query, no grading — just prints the answer for a human to
    eyeball) and was never designed to target the report rows specifically.

Neither of those exercises the actual end-to-end path THIS script checks:
given a question an on-corpus report row should answer well, does the
live agent (a) actually call AI News RAG, (b) get back a chunk tagged
doc_type="industry_report" from the real embedding model (not just from
the offline substring scan already done in approach_1_reports — this is
the live mxbai-embed-large ranking, the thing the offline check
explicitly could NOT validate), and (c) write a final answer that is
actually GROUNDED in the real report figures rather than fabricating
plausible-sounding ones. This is the on-corpus mirror of approach_2's
off-corpus fabrication probes — same anti-hallucination concern, opposite
corpus-coverage condition.

DEFAULT_QUERIES (4 cases, one per report in the corpus):
  - wef-job-creation-displacement   (WEF Future of Jobs 2025)
  - mckinsey-ebit-scaling-gap       (McKinsey State of AI 2025)
  - stanford-swebench-technical-performance (Stanford HAI AI Index 2026)
  - coursera-genai-agentic-demand   (Coursera Job Skills Report 2026)

Each case's `expected_signals` and `report_name_signals` reuse the SAME
real, already-verified anchor terms as
chatbot/eval/test_report_anchors.csv (e.g. "170 million new jobs",
"less than 5% of EBIT", "SWE-bench Verified", "14 enrollments per
minute") — not new invented checks — consistent with this project's
anti-hallucination discipline for test fixtures.

Tool-call detection (2 signals, simpler than test_university_programs.py
since the News agent has only ONE tool — no tool-ORDER question, just
"was it called, and what doc_types came back"):
  - direct function-level patch (PRIMARY, authoritative) on
    tools/news_tool.py's module-level retrieve() — see
    _wrap_retrieve_function. Records every call's query AND the doc_type
    of every result returned, so grading can check directly whether the
    real embedding model surfaced industry_report content for these
    queries (the offline approach_1_reports() check cannot answer this —
    it doesn't use the real Ollama embedding model end-to-end the way a
    live agent run does).
  - verbose-log "[REPORT]" tag scan (secondary cross-check only) —
    confirms the report tag actually appeared in the rendered tool output
    the LLM saw, independent of the direct-patch signal.

Grading is HARD-FAIL on: runtime error, zero tool calls, zero
industry_report doc_types returned across all calls, or a final answer
that contains none of the case's expected_signals (not grounded in real
figures). It's soft INSPECT on: the report not being named/attributed in
the final answer, or the two tool-detection signals disagreeing. A human
should still skim the snapshot's full final-answer text for subtler
fabrication this substring-based grading can't catch (e.g. a slightly
WRONG number that still contains a true substring) — that's why the full
answer is always written to the snapshot, same convention as
test_university_programs.py.

Hits the configured LLM (Anthropic by default) for 4 real queries.
Estimated cost: roughly $0.50-1.00 on Sonnet 4.6 (similar order to
run_news_tests.py's approach_2, same LLM, similar query count).

Run:
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_news_industry_reports.py
"""

import contextlib
import io
import os
import re
import sys
import time
import traceback
from datetime import date

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from dotenv import load_dotenv  # noqa: E402
load_dotenv(os.path.join(_CHATBOT_DIR, ".env"))

# Must be set BEFORE any `from crewai import ...` — CrewAI initialises its
# telemetry client on first import; setting these after that point has no effect.
os.environ.setdefault("CREWAI_TELEMETRY_OPT_OUT", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")

from crewai import Crew, Task  # noqa: E402

from agents.news import make_news_agent  # noqa: E402
from llm import describe_llm_config  # noqa: E402

# Imported as a module (not `from tools.news_tool import retrieve`) so the
# direct function-level patch below can reassign the MODULE ATTRIBUTE —
# news_rag_tool's body calls `retrieve(...)` as a bare name, which Python
# resolves against this module's globals at CALL time, not at decoration
# time. Same technique as test_university_programs.py's
# _wrap_retrieval_functions — see that file's docstring for the full
# reasoning on why this is more trustworthy than patching the CrewAI Tool
# object itself.
import tools.news_tool as _news_tool_module  # noqa: E402

NEWS_TOOL_NAME = "AI News RAG"

DEFAULT_QUERIES = [
    {
        "id": "wef-job-creation-displacement",
        "query": (
            "How many new jobs is AI projected to create globally by 2030, "
            "and how many jobs are expected to be displaced? Please cite "
            "the specific source report and figures."
        ),
        "target_entry_id": "wef-future-of-jobs-2025-net-job-creation",
        "expected_signals": ["170 million", "92 million"],
        "report_name_signals": ["world economic forum", "wef", "future of jobs"],
    },
    {
        "id": "mckinsey-ebit-scaling-gap",
        "query": (
            "Most companies now say they use AI regularly, but how many are "
            "actually seeing real financial returns (EBIT impact) from it, "
            "based on recent enterprise AI adoption survey data?"
        ),
        "target_entry_id": "mckinsey-state-of-ai-2025-adoption-scaling-gap",
        "expected_signals": ["5% of ebit", "5%"],
        "report_name_signals": ["mckinsey", "state of ai"],
    },
    {
        "id": "stanford-swebench-technical-performance",
        "query": (
            "How much have AI systems' coding/software-engineering "
            "benchmark scores improved recently, according to research "
            "tracking AI technical performance and adoption?"
        ),
        "target_entry_id": "stanford-ai-index-2026-technical-performance",
        "expected_signals": ["swe-bench"],
        "report_name_signals": ["stanford", "ai index", "hai"],
    },
    {
        "id": "coursera-genai-agentic-demand",
        "query": (
            "What does recent online-learning enrollment data say about "
            "student demand for generative AI and agentic AI courses?"
        ),
        "target_entry_id": "coursera-job-skills-report-2026-genai-agentic-ai",
        "expected_signals": ["14 enrollments per minute", "agentic ai"],
        "report_name_signals": ["coursera", "job skills"],
    },
]


# ── Verbose-log cleanup (secondary signal only) ───────────────────────────
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[mGKHFABCDJsu]")
_BOX_RE = re.compile(r"[│╭╰╮╯─├┤┬┴┼╔╗╚╝╠╣╦╩╬═║╴╶╸╺]+")


def _clean_log(text: str) -> str:
    text = _ANSI_RE.sub("", text)
    text = _BOX_RE.sub(" ", text)
    return text


def _wrap_retrieve_function(calls: list[dict]):
    """Monkey-patch tools/news_tool.py's module-level retrieve(), recording
    every call's query plus the doc_type of every result it returns. This is
    the PRIMARY, authoritative tool-use signal — see module docstring.

    Unlike test_university_programs.py's analogous helper, there is only
    ONE tool here, so there is no call-order question — just "did it get
    called, and what doc_types came back" (the thing the offline
    approach_1_reports() check in run_news_tests.py cannot answer, since
    that check never runs the real agent or the real live embedding-model
    ranking end-to-end).

    Returns a zero-arg restore() callable. ALWAYS call it (e.g. in a
    `finally` block) — retrieve() is a shared module-level singleton, not
    rebuilt per agent/case, so a patch left in place leaks into every later
    case in this process.
    """
    orig_retrieve = _news_tool_module.retrieve

    def _tracked_retrieve(query, k=_news_tool_module.DEFAULT_K):
        results = orig_retrieve(query, k=k)
        calls.append({
            "query": query,
            "doc_types": [r.get("doc_type") for r in results],
            "titles": [r.get("title", "")[:60] for r in results],
        })
        return results

    _news_tool_module.retrieve = _tracked_retrieve

    def restore() -> None:
        _news_tool_module.retrieve = orig_retrieve

    return restore


def run_one(agent, case: dict) -> dict:
    task = Task(
        description=case["query"],
        expected_output=(
            "A data-grounded answer citing specific figures and the source "
            "report by name, drawn from the indexed news/industry-report "
            "corpus."
        ),
        agent=agent,
    )

    retrieval_calls: list[dict] = []
    crew = Crew(agents=[agent], tasks=[task], verbose=True)

    buf = io.StringIO()
    t0 = time.time()
    answer = ""
    error: str | None = None
    restore_retrieve = _wrap_retrieve_function(retrieval_calls)
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            answer = str(crew.kickoff())
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        traceback.print_exc(file=buf)
    finally:
        # Must always run — retrieve() is a shared module-level singleton,
        # not rebuilt per case, so a patch left in place would leak into
        # every later case in this process.
        restore_retrieve()
    elapsed = time.time() - t0

    cleaned_log = _clean_log(buf.getvalue())
    report_tag_seen_in_log = "[REPORT]" in cleaned_log

    return {
        "answer": answer,
        "retrieval_calls": retrieval_calls,
        "report_tag_seen_in_log": report_tag_seen_in_log,
        "verbose_log": cleaned_log,
        "wall_time_sec": elapsed,
        "error": error,
    }


def grade(case: dict, result: dict) -> dict:
    """Returns {"verdict": PASS|INSPECT|FAIL, "hard": [...], "soft": [...],
    "info": [...]}.

    `info` notes are purely descriptive (e.g. "N industry_report hits
    returned") and never influence the verdict — keep them out of `soft`,
    since `soft` non-empty caps the verdict at INSPECT. An earlier version
    of this function put the report-hit-count note in `soft`, which meant
    every single genuinely-correct case was capped at INSPECT and could
    never show as PASS (same failure mode documented for
    test_university_programs.py's INSPECT-capped verbose_log_fallback
    signal in CLAUDE.md) — fixed 2026-06-22 after a live run confirmed it.
    """
    hard: list[str] = []
    soft: list[str] = []
    info: list[str] = []

    if result["error"]:
        hard.append(f"runtime error: {result['error']}")

    calls = result["retrieval_calls"]
    if not calls:
        hard.append(
            f"{NEWS_TOOL_NAME} was never called — the agent answered "
            "without retrieving anything, so this case can't have been "
            "grounded in the corpus at all"
        )
    else:
        all_doc_types = [dt for c in calls for dt in c["doc_types"]]
        n_report_hits = sum(1 for dt in all_doc_types if dt == "industry_report")
        if n_report_hits == 0:
            hard.append(
                f"{NEWS_TOOL_NAME} was called {len(calls)} time(s), but NONE "
                "of the returned results were tagged doc_type='industry_report' "
                "— the real embedding model did not surface any report "
                "content for this on-corpus query (the offline "
                "approach_1_reports() check in run_news_tests.py can't catch "
                "this, since it doesn't exercise the live retrieval ranking "
                "the way an actual agent run does)"
            )
        else:
            info.append(
                f"{n_report_hits} industry_report-tagged result(s) returned "
                f"across {len(calls)} call(s) — see retrieval_calls in the "
                "snapshot for per-call doc_type breakdown"
            )
        if not result["report_tag_seen_in_log"] and n_report_hits > 0:
            soft.append(
                "the direct-patch signal saw industry_report doc_types "
                "returned, but the verbose log never showed the '[REPORT]' "
                "tag text — worth a manual look (could mean format_results() "
                "isn't tagging consistently, or just a log-capture quirk)"
            )
        if len(calls) > 3:
            soft.append(
                f"{len(calls)} tool calls — above the backstory's stated "
                "3-call budget (framework max_iter=6 should prevent runaway "
                "cost regardless, but worth a glance)"
            )
        # Diversity check, added 2026-06-22 after a live run showed a single
        # long article's chunks (VentureBeat's ~14k-char bodies get split
        # into many chunks by build_news_index.py) occupying most/all of one
        # call's top-k, crowding out an otherwise-relevant industry_report
        # chunk. retrieve() does plain similarity_search() with no per-source
        # dedup (tools/news_tool.py, retrieve()) so this is a real, reachable
        # failure mode, not a hypothetical — flag it whenever it's severe
        # enough to plausibly be the cause of a miss.
        for c in calls:
            titles = c.get("titles", [])
            if not titles:
                continue
            most_common_title, most_common_count = max(
                ((t, titles.count(t)) for t in set(titles)), key=lambda x: x[1]
            )
            if most_common_count >= max(3, (len(titles) // 2) + 1):
                soft.append(
                    f"low source diversity in one retrieval call: "
                    f"{most_common_count}/{len(titles)} results were the same "
                    f"article ({most_common_title!r}) — likely that article's "
                    "chunks crowding out other relevant content in the top-k "
                    "(retrieve() has no per-source dedup; see tools/news_tool.py)"
                )

    answer_lc = result["answer"].lower()
    expected = case["expected_signals"]
    grounded = any(sig.lower() in answer_lc for sig in expected)
    if not grounded:
        hard.append(
            f"final answer contains none of the expected real figures "
            f"{expected!r} — either not grounded in the retrieved report "
            "content, or (more concerning) the real figure was paraphrased/"
            "altered. Read the full answer in the snapshot."
        )

    named = any(sig.lower() in answer_lc for sig in case["report_name_signals"])
    if grounded and not named:
        soft.append(
            f"final answer cites the right figures but never names the "
            f"source report (expected one of {case['report_name_signals']!r}) "
            "— content is grounded but attribution is weak"
        )

    if hard:
        verdict = "FAIL"
    elif soft:
        verdict = "INSPECT"
    else:
        verdict = "PASS"
    return {"verdict": verdict, "hard": hard, "soft": soft, "info": info}


def _safe_slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", s)


def write_snapshot(cases, results, grades) -> str:
    today = date.today().isoformat()
    llm_slug = _safe_slug(describe_llm_config())[:60]
    path = os.path.join(_HERE, f"news_industry_reports_smoketest_{today}_{llm_slug}.md")

    n_total = len(cases)
    n_pass = sum(1 for g in grades if g["verdict"] == "PASS")
    n_inspect = sum(1 for g in grades if g["verdict"] == "INSPECT")
    n_fail = sum(1 for g in grades if g["verdict"] == "FAIL")

    body: list[str] = [
        f"# News agent — industry-report grounding smoke test — {today}",
        "",
        "## Run config",
        f"- LLM: `{describe_llm_config()}`",
        f"- cases run: {n_total}",
        f"- PASS: {n_pass}",
        f"- INSPECT: {n_inspect}  _(grounded but weak attribution, or signal "
        "disagreement — review manually)_",
        f"- FAIL: {n_fail}",
        "",
        "Verdict key: **PASS** tool called, real industry_report content "
        "retrieved, answer grounded in the real figures and named the "
        "source report · **INSPECT** grounded but didn't name the report, "
        "or a soft signal-disagreement note · **FAIL** tool never called, "
        "no industry_report content surfaced by the live embedding model, "
        "the answer didn't contain the expected real figures, or a runtime "
        "error.",
        "",
        "Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_news_industry_reports.py`",
        "",
        "## Per-case summary",
        "",
        "| ID | verdict | tool calls | report hits | wall (s) |",
        "|---|---|---|---|---|",
    ]
    for case, result, grade_r in zip(cases, results, grades):
        n_calls = len(result["retrieval_calls"])
        n_report_hits = sum(
            1 for c in result["retrieval_calls"] for dt in c["doc_types"]
            if dt == "industry_report"
        )
        body.append(
            f"| {case['id']} | {grade_r['verdict']} | {n_calls} "
            f"| {n_report_hits} | {result['wall_time_sec']:.1f} |"
        )

    body += ["", "---", ""]

    for case, result, grade_r in zip(cases, results, grades):
        verdict = grade_r["verdict"]
        body += [
            f"## [{case['id']}] **{verdict}**",
            "",
            f"**Target report row:** `{case['target_entry_id']}`",
            f"**Expected signals (any one ⇒ grounded):** {case['expected_signals']!r}",
            f"**Report-name signals (any one ⇒ attributed):** {case['report_name_signals']!r}",
            "",
            "**Query:**",
            "",
            "```",
            case["query"].strip(),
            "```",
            "",
            f"**Wall time:** {result['wall_time_sec']:.1f}s",
            f"**Retrieval calls:** {len(result['retrieval_calls'])}",
            "",
        ]
        if result["retrieval_calls"]:
            body.append("**Per-call doc_type breakdown:**")
            for i, c in enumerate(result["retrieval_calls"], 1):
                body.append(
                    f"- call {i}: query={c['query']!r}, "
                    f"doc_types={c['doc_types']!r}"
                )
                for t, dt in zip(c["titles"], c["doc_types"]):
                    body.append(f"    - [{dt}] {t}")
            body.append("")
        if grade_r["hard"]:
            body.append("**Hard failures (FAIL):**")
            for msg in grade_r["hard"]:
                body.append(f"- {msg}")
            body.append("")
        if grade_r["soft"]:
            body.append("**Soft notes (INSPECT):**")
            for msg in grade_r["soft"]:
                body.append(f"- {msg}")
            body.append("")
        if grade_r.get("info"):
            body.append("**Info (does not affect verdict):**")
            for msg in grade_r["info"]:
                body.append(f"- {msg}")
            body.append("")
        body += [
            "**Agent's final answer:**",
            "",
            result["answer"] or "*(no answer produced — see error/verbose_log)*",
            "",
            "<details><summary>Cleaned verbose log (secondary cross-check "
            "only)</summary>",
            "",
            "```",
            result["verbose_log"][:8000] or "(empty)",
            "```",
            "",
            "</details>",
            "",
            "---",
            "",
        ]

    with open(path, "w") as f:
        f.write("\n".join(body))
    return path


def main() -> None:
    print(describe_llm_config())
    print()

    cases = DEFAULT_QUERIES
    results = []
    grades = []
    for i, case in enumerate(cases, 1):
        print(f"[{i}/{len(cases)}] {case['id']} — running...")
        agent = make_news_agent()  # fresh agent per case
        result = run_one(agent, case)
        grade_r = grade(case, result)
        results.append(result)
        grades.append(grade_r)

        symbol = {"PASS": "✅", "INSPECT": "\U0001f50d", "FAIL": "❌"}.get(
            grade_r["verdict"], "?"
        )
        n_report_hits = sum(
            1 for c in result["retrieval_calls"] for dt in c["doc_types"]
            if dt == "industry_report"
        )
        print(
            f"  {symbol} {grade_r['verdict']}  "
            f"calls={len(result['retrieval_calls'])}  "
            f"report_hits={n_report_hits}  "
            f"wall={result['wall_time_sec']:.1f}s"
        )
        for msg in grade_r["hard"]:
            print(f"    ❌ [hard] {msg}")
        for msg in grade_r["soft"]:
            print(f"    \U0001f50d [soft] {msg}")
        print()

    snapshot_path = write_snapshot(cases, results, grades)
    n_pass = sum(1 for g in grades if g["verdict"] == "PASS")
    n_inspect = sum(1 for g in grades if g["verdict"] == "INSPECT")
    n_fail = sum(1 for g in grades if g["verdict"] == "FAIL")

    print("=" * 72)
    print(f"SUMMARY: {n_pass} PASS  |  {n_inspect} INSPECT  |  {n_fail} FAIL  (out of {len(cases)})")
    print(f"Snapshot: {snapshot_path}")


if __name__ == "__main__":
    main()
