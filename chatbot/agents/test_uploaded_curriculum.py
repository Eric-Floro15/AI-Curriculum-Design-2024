"""
test_uploaded_curriculum.py — agent-level end-to-end test for the
professor-uploaded-curriculum feature (added 2026-06-23).

This is the agent-level counterpart to tools/test_upload_extract.py (which
only tests extract_text()/build_uploaded_document_block() in isolation, no
LLM). This script instead exercises the LIVE Orchestrator + University AI
Programs Researcher path the same way chatbot/eval/run_orchestrator_eval.py
and agents/test_university_programs.py do for their respective features:
build the full 5-agent Crew, run a real Task through Crew.kickoff(), and
check what actually happened — not just whether the code is syntactically
wired correctly (already confirmed via a stub-based dry run during
implementation; that dry run could NOT confirm whether the live LLM (a)
actually reads the injected block instead of ignoring it, (b) actually
delegates to the right specialist with the block intact, and (c) actually
cites it correctly as unverified per the new backstory rules — that needs
a real model, which is the entire point of this script).

WHY A SYNTHETIC, FICTIONAL UPLOADED PROGRAM:
The test fixture describes "Rivendale Institute of Technology" — an
institution that does not exist — with a deliberately unusual, made-up
required course, "AI 742: Cognitive Load-Aware Tutoring Systems". Both are
chosen so a correct answer mentioning them is unambiguous proof the model
actually read the INJECTED block rather than recalling something from its
own training data, the local program_and_curriculum corpus, or a live web
search (none of which can possibly contain a fictional course at a
fictional institution). This mirrors the anchor-term technique already
used in chatbot/eval/test_report_anchors.csv for the News agent's
industry-reports corpus.

WHY A REAL PDF, NOT HAND-WRITTEN TEXT:
The fixture is generated with reportlab (test-only dependency, same as
tools/test_upload_extract.py — not added to chatbot/requirements.txt) and
run through the REAL tools/upload_extract.extract_text() +
build_uploaded_document_block(), so this test exercises the actual
extraction pipeline end-to-end, not a shortcut around it.

WHAT IS AND ISN'T CHECKED:
  - delegated_to University AI Programs Researcher (via step_callback,
    same robust version-agnostic technique run_orchestrator_eval.py uses —
    see that script's "Delegation detection via step_callback" comment for
    why parsing the verbose log for delegation args was rejected as
    brittle). This proves the Orchestrator's new "HANDLING AN ATTACHED
    UPLOADED CURRICULUM DOCUMENT" rule actually routes to the right
    specialist, not just that the prompt text asks it to.
  - the anchor course name appears in the FINAL answer. This is the
    strongest available signal that the block's content actually flowed
    Orchestrator → (verbatim in the delegation context, per the new
    backstory rule) → University AI Programs Researcher → back into the
    synthesised answer. It is deliberately an end-to-end behavioural
    check, not an inspection of the delegation tool's internal arguments —
    test_university_programs.py's module docstring explains why patching
    CrewAI's delegation tool object directly was rejected as too
    version-fragile for THAT script's narrower tool-order question; the
    same reasoning applies here, and the anchor-substring check sidesteps
    it entirely by checking an observable behavioural outcome instead.
  - a forbidden-fabrication check: the final answer must NOT contain an
    invented URL/domain for the fictional institution. There is no real
    page for "Rivendale Institute of Technology" — by construction, since
    it doesn't exist — so any URL-shaped guess for it is a hallucination,
    not a citation.
  - soft (non-blocking) check that the answer's phrasing distinguishes the
    uploaded content from a verified source (e.g. "uploaded document",
    "professor-provided", "not independently verified").

Costs real LLM budget (delegates to 1-3 specialists depending on case,
same order of magnitude as run_orchestrator_eval.py — roughly $0.50-2 on
Sonnet 4.6 for both cases). Requires network + a configured LLM endpoint;
cannot run in this project's offline/Ollama-unreachable sandbox — see
CLAUDE.md's standing note on this. Run on a machine with Ollama serving
mxbai-embed-large (if the local corpus also gets queried) and/or a
configured ANTHROPIC_API_KEY.

Run:
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_uploaded_curriculum.py
"""

import contextlib
import io
import os
import re
import sys
import tempfile
import time
import traceback
from datetime import date

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from dotenv import load_dotenv  # noqa: E402
load_dotenv(os.path.join(_CHATBOT_DIR, ".env"))

# Must be set BEFORE any `from crewai import ...` — see test_university_programs.py.
os.environ.setdefault("CREWAI_TELEMETRY_OPT_OUT", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")

from crewai import Crew, Task  # noqa: E402

from agents.analyst import make_analyst  # noqa: E402
from agents.cluster_interpreter import make_cluster_interpreter  # noqa: E402
from agents.news import make_news_agent  # noqa: E402
from agents.orchestrator import make_orchestrator  # noqa: E402
from agents.university_programs import make_university_programs_agent  # noqa: E402
from llm import describe_llm_config  # noqa: E402
from tools.upload_extract import build_uploaded_document_block, extract_text  # noqa: E402

UNIV_ROLE = "University AI Programs Researcher"
ANALYST_ROLE = "Skills Taxonomy Analyst"
NEWS_ROLE = "AI Industry News Researcher"

# ── Synthetic uploaded-curriculum fixture ──────────────────────────────────
# See module docstring for why these specific strings were chosen.
_FICTIONAL_INSTITUTION = "Rivendale Institute of Technology"
_ANCHOR_COURSE = "Cognitive Load-Aware Tutoring Systems"
_FORBIDDEN_FABRICATED_DOMAINS = ["rivendale.edu", "rivendaleinstitute", "rivendale.ac"]

_FIXTURE_LINES = [
    f"DRAFT — {_FICTIONAL_INSTITUTION}",
    "Department of Computer & Data Science",
    "Master of Applied Artificial Intelligence — Draft Curriculum",
    "(Internal draft, not yet approved by Senate, not published online)",
    "",
    "Required Courses:",
    "AI 701: Foundations of Machine Learning",
    f"AI 742: {_ANCHOR_COURSE}",
    "AI 750: Ethics and Governance of Autonomous Systems",
    "",
    "Elective Courses:",
    "AI 770: Federated Learning for Edge Devices",
    "AI 781: Generative Audio Synthesis Lab",
    "",
    "Notes: Capstone structure and admissions targets still under review.",
]


def _build_fixture_block(tmpdir: str) -> str:
    """Render the fixture as a real PDF, extract it through the real
    pipeline, and wrap it exactly the way chatbot/app.py's on_message does
    for a live upload."""
    from reportlab.pdfgen import canvas

    pdf_path = os.path.join(tmpdir, "rivendale_draft_curriculum.pdf")
    c = canvas.Canvas(pdf_path, pagesize=(612, 792))
    c.setFont("Helvetica", 11)
    y = 740
    for line in _FIXTURE_LINES:
        c.drawString(72, y, line)
        y -= 18
    c.showPage()
    c.save()

    text = extract_text(pdf_path)
    return build_uploaded_document_block("rivendale_draft_curriculum.pdf", text)


DEFAULT_CASES = [
    {
        "id": "uploaded-vs-single-peer",
        "question": (
            "Compare the attached uploaded draft curriculum against "
            "Queen's University's MMAI program. What required courses are "
            "we missing relative to Queen's?"
        ),
        "expect_delegated": {UNIV_ROLE},
        "category": "single-topic (should NOT fan out to Analyst/News per "
                     "orchestrator's own delegation rules)",
    },
    {
        "id": "uploaded-full-review",
        "question": (
            "We're trying to modernise the attached draft program for "
            "current industry demand and recent AI developments. What "
            "should we add or change?"
        ),
        "expect_delegated": {UNIV_ROLE},  # hard-required; Analyst/News are soft-checked below
        "category": "broad curriculum-design query (orchestrator's "
                     "backstory says consult all three core specialists — "
                     "checked as a soft signal, not hard, since that rule "
                     "isn't what THIS feature is testing)",
    },
]

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[mGKHFABCDJsu]")
_BOX_RE = re.compile(r"[│╭╰╮╯─├┤┬┴┼╔╗╚╝╠╣╦╩╬═║╴╶╸╺]+")


def _clean_log(text: str) -> str:
    text = _ANSI_RE.sub("", text)
    text = _BOX_RE.sub(" ", text)
    return text


def run_one(case: dict, upload_block: str) -> dict:
    """Build a fresh 5-agent crew (same composition as app.py's
    _kickoff_crew), inject the uploaded-document block ahead of the
    professor's question exactly as app.py does, and run it for real."""
    analyst = make_analyst()
    univ = make_university_programs_agent()
    news = make_news_agent()
    cluster_interp = make_cluster_interpreter()
    orch = make_orchestrator()

    delegated_to: set[str] = set()

    def _make_tracker(role: str):
        def _tracker(_output) -> None:
            delegated_to.add(role)
        return _tracker

    analyst.step_callback = _make_tracker(ANALYST_ROLE)
    univ.step_callback = _make_tracker(UNIV_ROLE)
    news.step_callback = _make_tracker(NEWS_ROLE)
    # cluster_interp intentionally untracked — not relevant to this feature.

    full_query = f"{upload_block}\n\n{case['question']}"

    task = Task(
        description=full_query,
        expected_output=(
            "A concise, data-grounded recommendation comparing the "
            "uploaded draft curriculum against peer programs and/or "
            "market demand, naming specific courses, and citing the "
            "uploaded document distinctly from any verified source."
        ),
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
    except Exception as e:  # noqa: BLE001
        error = f"{type(e).__name__}: {e}"
        traceback.print_exc(file=buf)
    elapsed = time.time() - t0

    log = _clean_log(buf.getvalue())
    tool_calls = len(re.findall(r"Tool Execution Started", log))

    return {
        "answer": answer,
        "verbose_log": log,
        "wall_time_sec": elapsed,
        "tool_calls": tool_calls,
        "delegated_to": delegated_to,
        "error": error,
    }


def grade(case: dict, result: dict) -> dict:
    hard: list[str] = []
    soft: list[str] = []
    answer = result["answer"]
    answer_lc = answer.lower()

    if result["error"]:
        hard.append(f"runtime error: {result['error']}")

    # Hard: the specialist that actually reads the upload must be reached.
    if UNIV_ROLE not in result["delegated_to"]:
        hard.append(
            f"{UNIV_ROLE!r} was never delegated to — the uploaded document "
            "could not have been analyzed at all this run"
        )

    # Hard: the anchor course name from the uploaded PDF must show up in
    # the final answer — the strongest available proof the injected block
    # actually flowed through delegation into the synthesised answer (see
    # module docstring for why this, not a delegation-arg inspection, is
    # the check here).
    if _ANCHOR_COURSE.lower() not in answer_lc:
        hard.append(
            f"anchor course {_ANCHOR_COURSE!r} (unique to the synthetic "
            "uploaded fixture, cannot exist in any real corpus/web result) "
            "did not appear in the final answer — the uploaded content "
            "likely never reached the agent that produced this answer, or "
            "was ignored"
        )

    # Hard: must not fabricate a URL/domain for the fictional institution.
    fabricated = [d for d in _FORBIDDEN_FABRICATED_DOMAINS if d in answer_lc]
    if fabricated:
        hard.append(
            f"answer contains a fabricated-looking domain for the "
            f"fictional {_FICTIONAL_INSTITUTION!r} (which has no real "
            f"page by construction): {fabricated}"
        )

    # Hard: must not attribute specific findings to a specialist that was
    # never actually delegated to this run. Added 2026-06-24 in response to
    # a real live FAIL (case "uploaded-full-review", qwen3:14b): the final
    # answer cited specific-sounding stats/articles to "Skills Taxonomy
    # Analyst" and "AI Industry News Researcher" by name, even though
    # delegated_to only contained University AI Programs Researcher — i.e.
    # those two specialists were never actually consulted. This is distinct
    # from (and more serious than) the existing case-2-only soft "didn't
    # also delegate" note below, which treats non-delegation as an allowed
    # breadth choice; this check instead catches the model CLAIMING to have
    # consulted someone it didn't — something orchestrator.py's own
    # backstory already explicitly forbids ("Do NOT claim to have
    # consulted a specialist you did not actually delegate to"), violated
    # anyway on that live run. Cluster Interpreter is deliberately excluded
    # — it is NOT tracked via step_callback (see run_one()'s comment), so
    # we cannot tell whether it was really consulted; including it here
    # would risk false positives, not catch a real problem.
    for role in (ANALYST_ROLE, NEWS_ROLE):
        if role.lower() in answer_lc and role not in result["delegated_to"]:
            hard.append(
                f"final answer names {role!r} as a source of specific "
                "findings, but step_callback shows it was never actually "
                "delegated to this run — likely a fabricated citation, "
                "not a real consulted specialist"
            )

    # Soft: distinct-citation phrasing for the uploaded content.
    distinct_phrases = [
        "uploaded document",
        "professor-provided",
        "professor provided",
        "not independently verified",
        "provided by the professor",
    ]
    if not any(p in answer_lc for p in distinct_phrases):
        soft.append(
            "none of the expected distinct-citation phrases "
            f"{distinct_phrases} appeared — the answer may not be "
            "clearly flagging the uploaded content as unverified, "
            "professor-provided input (check phrasing manually; the "
            "model may have used an equivalent phrase not in this list)"
        )

    # Soft (case-specific): for the broad-review case, the orchestrator's
    # OWN backstory rule (unrelated to this feature) says it should also
    # consult Analyst/News — informational only, not this feature's job.
    if case["id"] == "uploaded-full-review":
        also_expected = {ANALYST_ROLE, NEWS_ROLE}
        missing = also_expected - result["delegated_to"]
        if missing:
            soft.append(
                f"broad curriculum-review query did not also delegate to "
                f"{sorted(missing)} — allowed/orthogonal to this feature, "
                "but worth a manual glance per the orchestrator's existing "
                "delegation rules"
            )

    if hard:
        verdict = "FAIL"
    elif soft:
        verdict = "INSPECT"
    else:
        verdict = "PASS"
    return {"verdict": verdict, "hard": hard, "soft": soft}


def _safe_slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", s)


def write_snapshot(cases, results, grades) -> str:
    today = date.today().isoformat()
    llm_slug = _safe_slug(describe_llm_config())[:60]
    path = os.path.join(_HERE, f"uploaded_curriculum_smoketest_{today}_{llm_slug}.md")

    n_total = len(cases)
    n_pass = sum(1 for g in grades if g["verdict"] == "PASS")
    n_inspect = sum(1 for g in grades if g["verdict"] == "INSPECT")
    n_fail = sum(1 for g in grades if g["verdict"] == "FAIL")

    body: list[str] = [
        f"# Uploaded-curriculum feature — agent-level smoke test — {today}",
        "",
        "## Run config",
        f"- LLM: `{describe_llm_config()}`",
        f"- fictional fixture institution: {_FICTIONAL_INSTITUTION!r}",
        f"- anchor course (proof-of-flow string): {_ANCHOR_COURSE!r}",
        f"- cases run: {n_total}",
        f"- PASS: {n_pass}",
        f"- INSPECT: {n_inspect}  _(soft/phrasing notes only — review manually)_",
        f"- FAIL: {n_fail}",
        "",
        "Verdict key: **PASS** uploaded content reached the right "
        "specialist and was cited correctly · **INSPECT** soft phrasing "
        "note only · **FAIL** delegation never happened, anchor content "
        "missing from the final answer, a fabricated URL appeared, or a "
        "runtime error.",
        "",
        "Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_uploaded_curriculum.py`",
        "",
        "## Per-case summary",
        "",
        "| ID | verdict | delegated_to | tool calls | wall (s) |",
        "|---|---|---|---|---|",
    ]
    for case, result, grade_r in zip(cases, results, grades):
        body.append(
            f"| {case['id']} | {grade_r['verdict']} "
            f"| {sorted(result['delegated_to'])} "
            f"| {result['tool_calls']} "
            f"| {result['wall_time_sec']:.1f} |"
        )

    body += ["", "---", ""]

    # Inline preview cap for the verbose log embedded in the .md itself.
    # Raised 2026-06-24 from the original 8000 to 20000 — the original cap
    # was found (while diagnosing the real "uploaded-full-review" FAIL
    # above) to cut off during crew startup / the first Task/Agent-Started
    # panels, before reaching ANY of the actual delegation calls, sub-agent
    # answers, or final-synthesis reasoning — i.e. before any of the detail
    # actually needed to diagnose a content-dropped-somewhere-in-the-
    # pipeline failure. The FULL untruncated log is now also always saved
    # to a sibling .log file per case (see below) regardless of this cap,
    # since even 20000 chars can still be insufficient for a long
    # multi-agent run with retries.
    _LOG_PREVIEW_CHARS = 20_000

    for case, result, grade_r in zip(cases, results, grades):
        verdict = grade_r["verdict"]
        body += [
            f"## [{case['id']}] **{verdict}**",
            "",
            f"**Category:** {case['category']}",
            "",
            "**Question (appended after the uploaded-document block):**",
            "",
            "```",
            case["question"].strip(),
            "```",
            "",
            f"**Wall time:** {result['wall_time_sec']:.1f}s",
            f"**Tool calls:** {result['tool_calls']}",
            f"**Delegated to:** {sorted(result['delegated_to']) or '(none)'}",
            "",
        ]
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

        # Always save the FULL untruncated log to a sibling .log file —
        # added 2026-06-24 alongside the preview-cap raise above, same
        # rationale: a fixed inline cap (any size) can still be exceeded
        # by a long multi-agent run with retries, and silently losing the
        # tail of the log is exactly what made the first real FAIL on this
        # script hard to diagnose.
        full_log = result["verbose_log"] or "(empty)"
        log_filename = (
            f"uploaded_curriculum_smoketest_{today}_{llm_slug}"
            f"_{_safe_slug(case['id'])}.log"
        )
        with open(os.path.join(_HERE, log_filename), "w") as lf:
            lf.write(full_log)

        preview = full_log[:_LOG_PREVIEW_CHARS]
        truncation_note = (
            f"\n\n... [truncated for inline preview — {len(full_log)} total "
            f"chars; full untruncated log saved to {log_filename}]"
            if len(full_log) > _LOG_PREVIEW_CHARS
            else ""
        )

        body += [
            "**Final answer:**",
            "",
            result["answer"] or "*(no answer produced — see verbose log)*",
            "",
            f"Full verbose log saved to `{log_filename}` "
            f"({len(full_log)} chars).",
            "",
            "<details><summary>Cleaned verbose log (preview)</summary>",
            "",
            "```",
            preview + truncation_note,
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

    with tempfile.TemporaryDirectory() as tmpdir:
        upload_block = _build_fixture_block(tmpdir)

        cases = DEFAULT_CASES
        results = []
        grades = []
        for i, case in enumerate(cases, 1):
            print(f"[{i}/{len(cases)}] {case['id']} — running...")
            result = run_one(case, upload_block)
            grade_r = grade(case, result)
            results.append(result)
            grades.append(grade_r)

            symbol = {"PASS": "✅", "INSPECT": "\U0001f50d", "FAIL": "❌"}.get(
                grade_r["verdict"], "?"
            )
            print(
                f"  {symbol} {grade_r['verdict']}  "
                f"delegated={sorted(result['delegated_to'])}  "
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
