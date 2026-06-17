"""
test_university_programs.py — Standalone smoke test for the University
Programs agent's RAG-first / web-search-fallback TOOL-USE behavior.

This is deliberately different from chatbot/eval/run_program_rag_eval.py:
that script tests retrieve() directly (no LLM, no agent) and scores ranking
quality. This script tests whether the live AGENT actually obeys its
backstory's tool-order rule ("ALWAYS call University Program RAG first;
only call Web Search after it misses") when given a real task through
Crew.kickoff(). The backstory is a soft, LLM-readable constraint, not
hard-coded control flow — the only way to know whether it actually holds is
to run it and watch what tools get called, in what order.

DEFAULT_QUERIES (2 cases):
  1. queens-rag-hit       — Queen's MMAI is in the local corpus and should
                             retrieve a clean, low-distance match. Expect:
                             University Program RAG called, and it should
                             be the FIRST tool call. Web Search may still
                             fire for a sub-question the local hit didn't
                             cover (allowed per backstory) — that's flagged
                             INSPECT, not FAIL.
  2. fallback-clean-miss  — Johns Hopkins' Master of Public Health program.
                             Chosen deliberately OUTSIDE the agent's AI/ML
                             domain entirely (not just "a different
                             institution") so the local corpus misses
                             cleanly and unambiguously. Expect: University
                             Program RAG called first, then Web Search.

                             NOTE: a same-domain "AI program not yet in the
                             corpus" query (e.g. the project's existing
                             negative-control-uw case, "University of
                             Washington ... Artificial Intelligence track")
                             is intentionally NOT used here as the default
                             fallback case. program_rag_tool has a known,
                             documented false-positive issue for exactly
                             that kind of query — see
                             tools/program_rag_tool.py's module docstring,
                             "Hybrid-retrieval history", and
                             chatbot/eval/program_baseline_*.md's
                             negative-control-uw result (0/1, still
                             unresolved as of 2026-06-16). Using it here
                             would conflate two different questions: "does
                             the fallback MECHANISM work" (what this script
                             checks) vs. "does retrieve() correctly detect a
                             miss for a near-duplicate-topic query" (a
                             retrieval-ranking question, already tracked
                             separately). If you want to probe THAT specific
                             known issue at the agent level too — e.g. to
                             see whether the agent ends up confidently
                             citing the wrong university's URL — add a third
                             case reusing that exact query string and expect
                             a hard-to-predict outcome that needs a manual
                             read of the answer, not a clean PASS/FAIL.

Detects tool usage THREE ways (a third signal added 2026-06-17 — see
below for why the first two weren't enough on their own):
  - direct function-level patch (PRIMARY signal as of 2026-06-17, used for
    grading whenever non-empty — see _wrap_retrieval_functions): monkey-
    patches the plain Python functions program_rag_tool/web_search_tool
    actually delegate to — tools/program_rag_tool.py's retrieve() and
    tools/web_search_tool.py's web_search() — so a call is recorded the
    moment either one really executes. Deliberately does NOT touch the
    CrewAI Tool objects themselves (their @tool-decorated internals aren't
    confirmed for this CrewAI version, and they're very likely pydantic
    models that would reject an arbitrary instance-attribute overwrite);
    patching the plain function one level below sidesteps that entirely,
    since Python resolves a bare-name call like `retrieve(...)` from its
    DEFINING MODULE's globals at call time, not at def time. This is the
    only one of the three signals that instruments the real call site
    directly rather than trying to infer it from a step object or log
    text, so it's treated as fully trustworthy (PASS-eligible) — added
    after the two signals below both turned out to have real gaps on live
    runs (qwen2.5:14b, then qwen3:14b).
  - step_callback (used for grading only when the direct patch above is
    empty — kept in case a future CrewAI version starts routing tool
    steps through it): CrewAI invokes this after every agent step. When a
    step is a tool invocation, the step object normally exposes the tool
    name via a `.tool` or `.action.tool` attribute (LangChain AgentAction-
    style). Recorded in call order. This mirrors the version-agnostic
    pattern chatbot/eval/run_orchestrator_eval.py uses for delegation
    detection — but note the analogy is weaker than it first looks: that
    script only needs to know WHETHER a specialist's step_callback fired
    at all (coarse — true even if it only fires on the final AgentFinish),
    while this script needs the actual SEQUENCE of tool names across
    intermediate steps (fine-grained). Every real run so far (2026-06-16
    qwen2.5:14b; 2026-06-16/17 qwen3:14b) has shown step_callback firing
    exactly once per case, on AgentFinish only — never on a tool-call step
    — so the "already validated" claim only ever covered the coarse case.
  - verbose-log fallback (used for grading only when BOTH signals above
    are empty — see _extract_tool_calls_from_log): parses CrewAI's own
    structured "Tool: <name>" line from inside its "🔧 Tool Execution
    Started"/"✅ Tool Execution Completed" panels. This is NOT the same as
    a bare substring scan of the whole log for "University Program RAG"/
    "Web Search" text — the backstory repeats those display strings dozens
    of times (tool policy + worked examples), which is exactly the false-
    positive risk that kept this signal out of grading originally. The
    structured "Tool: <name>" line only appears when CrewAI itself
    announces a real tool execution, and (confirmed from a real captured
    log) prints a snake_case SLUG of the tool's display name, e.g.
    "university_program_rag" for the tool registered as @tool("University
    Program RAG") — not the underlying Python function name.
    _slug()/_KNOWN_TOOL_SLUGS normalizes this back to the same
    RAG_TOOL_NAME/WEB_TOOL_NAME constants the other two signals use. Still
    treated as lower-confidence than the two above — using it caps the
    verdict at INSPECT even when it successfully recovers the correct
    order, since it depends on CrewAI's rendered log text staying in this
    exact shape across versions.

The verbose-log signal is now ALWAYS computed, even on runs where the
direct patch already has an answer — purely as a cross-check. If the two
disagree, that's surfaced as a soft INSPECT note worth a manual look
(a disagreement between two independently-implemented signals could mean
either one has a bug), without downgrading the verdict to FAIL on its own.

If NONE of the three signals records a tool call for a case, the case is
graded INSPECT (not FAIL) — most likely cause is this CrewAI version
exposing a different step/log shape than the step_callback/verbose-log
extractors expect (the direct patch should not normally miss a real call;
if IT comes back empty too, that's worth investigating on its own — see
_wrap_retrieval_functions's docstring), not the agent skipping tools
entirely (unless a runtime error is also present, which IS graded FAIL).
The raw per-step repr and all three raw signals are saved to the snapshot
so the extraction helpers can be tightened further against real data.

Writes a dated snapshot Markdown file next to this script
(university_programs_smoketest_<date>.md) — same convention as
chatbot/eval/run_program_rag_eval.py's program_baseline_*.md and
chatbot/eval/run_orchestrator_eval.py's orchestrator_baseline_*.md.

Hits the configured LLM AND the live DuckDuckGo endpoint (for the fallback
case), so it costs real API budget and depends on network — keep the query
set small. Cost: roughly a few cents to ~$0.20 on Sonnet 4.6 for both cases
combined (2 tool calls + 1 short final answer, well inside the agent's
max_iter=6 cap).

Run:
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_university_programs.py
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

from agents.university_programs import make_university_programs_agent  # noqa: E402
from llm import describe_llm_config  # noqa: E402

# Imported as modules (not `from ... import retrieve`) so the direct
# function-level patch in _wrap_retrieval_functions can reassign the
# MODULE ATTRIBUTE — see that function's docstring for why this is the
# part that actually makes the patch visible to the already-decorated
# @tool() wrappers in these two modules.
import tools.program_rag_tool as _program_rag_module  # noqa: E402
import tools.web_search_tool as _web_search_module  # noqa: E402


RAG_TOOL_NAME = "University Program RAG"
WEB_TOOL_NAME = "Web Search"

DEFAULT_QUERIES = [
    {
        "id": "queens-rag-hit",
        "query": (
            "What courses does the Queen's University MMAI program offer, "
            "and what topics are emphasised? Cite URLs for the program pages."
        ),
        "expect_web_search": False,
    },
    {
        "id": "fallback-clean-miss",
        "query": (
            "What courses does Johns Hopkins University's Master of Public "
            "Health program require, and what topics are emphasised in the "
            "curriculum? Cite URLs for the program pages."
        ),
        "expect_web_search": True,
    },
]


# ── Verbose-log cleanup (secondary signal only) ───────────────────────────
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[mGKHFABCDJsu]")
_BOX_RE = re.compile(r"[│╭╰╮╯─├┤┬┴┼╔╗╚╝╠╣╦╩╬═║╴╶╸╺]+")


def _clean_log(text: str) -> str:
    """Strip ANSI escape codes and rich panel border chars. Plain text only,
    used for human cross-checking — never parsed for grading (see module
    docstring for why)."""
    text = _ANSI_RE.sub("", text)
    text = _BOX_RE.sub(" ", text)
    return text


def _slug(s: str) -> str:
    """Normalize a tool name/display-string to a comparable slug, e.g.
    'University Program RAG' -> 'university_program_rag'. Needed because
    CrewAI's own structured log output (see _extract_tool_calls_from_log)
    prints tool names as a snake_case slug, not the literal display string
    passed to @tool() — confirmed from a real captured run on 2026-06-16
    (qwen2.5:14b), where the log read 'Tool: university_program_rag' for
    the tool registered as @tool("University Program RAG")."""
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


_TOOL_LINE_RE = re.compile(r"^\s*Tool:\s*(.+?)\s*$", re.MULTILINE)

_KNOWN_TOOL_SLUGS = {
    _slug(RAG_TOOL_NAME): RAG_TOOL_NAME,
    _slug(WEB_TOOL_NAME): WEB_TOOL_NAME,
}


def _extract_tool_calls_from_log(cleaned_log: str) -> list[str]:
    """Fallback tool-call-order extraction for when step_callback records
    nothing.

    Added 2026-06-16 after a live smoke-test run (qwen2.5:14b) showed
    step_callback's raw_steps containing ONLY a final AgentFinish object —
    never an AgentAction — even though the verbose log clearly showed a
    tool executing (a "🔧 Tool Execution Started" panel with a real
    "Tool: university_program_rag" / "Args: {...}" / "Output: ..." body).
    That strongly suggests this CrewAI version's native-tool-calling code
    path (the one behind the "call_llm_native_tools" flow listener seen in
    that same log) never routes intermediate tool steps through
    Agent.step_callback at all in this version — only the final answer
    does. Confirmed against ONE real log; not yet proven as a general rule
    across CrewAI versions, so step_callback stays the PRIMARY signal and
    this is a fallback, not a replacement.

    Parses CrewAI's own structured "Tool: <name>" line from inside its
    "Tool Execution Started"/"Tool Execution Completed" panels — narrower
    and more reliable than a bare substring scan of the whole log, since
    it only matches CrewAI's own tool-execution announcements, not the
    agent's backstory/thought text (the original false-positive risk noted
    in the module docstring). Each tool call prints this line twice
    (Started + Completed panels); consecutive duplicates are collapsed.
    """
    calls: list[str] = []
    for m in _TOOL_LINE_RE.finditer(cleaned_log):
        raw = m.group(1).strip()
        name = _KNOWN_TOOL_SLUGS.get(_slug(raw), raw)
        if not calls or calls[-1] != name:
            calls.append(name)
    return calls


_KNOWN_TOOL_SLUGS = {
    _slug(RAG_TOOL_NAME): RAG_TOOL_NAME,
    _slug(WEB_TOOL_NAME): WEB_TOOL_NAME,
}


def _extract_tool_name(step_output) -> str | None:
    """Best-effort, version-tolerant extraction of the tool name associated
    with one agent step.

    Tries known attribute shapes first (LangChain/CrewAI AgentAction-style
    objects commonly expose `.tool`, sometimes nested under `.action.tool`).
    Falls back to a substring scan of THIS SINGLE STEP's repr only — scoping
    to one step (not the whole multi-thousand-line verbose log) avoids the
    backstory-text false-positive risk described in the module docstring,
    though it isn't completely immune if a step's "thought" text happens to
    quote the backstory. Treat this fallback path as lower-confidence than
    the attribute path.
    """
    for path in ("tool", "action.tool"):
        obj = step_output
        ok = True
        for attr in path.split("."):
            obj = getattr(obj, attr, None)
            if obj is None:
                ok = False
                break
        if ok and isinstance(obj, str) and obj.strip():
            return obj.strip()

    text = repr(step_output)
    if RAG_TOOL_NAME in text:
        return RAG_TOOL_NAME
    if WEB_TOOL_NAME in text:
        return WEB_TOOL_NAME
    return None


def _wrap_retrieval_functions(calls: list[str]):
    """Monkey-patch the plain Python functions the two @tool()-decorated
    wrappers actually delegate to, so a call is recorded the moment either
    one really executes. Added 2026-06-17 as a THIRD, independent tool-call
    detection signal — see the module docstring for why step_callback and
    the verbose-log fallback weren't enough on their own.

    Patches:
      - tools/program_rag_tool.py's module-level `retrieve()` (called from
        inside the `@tool("University Program RAG")`-decorated function's
        body as `retrieve(query, k=DEFAULT_K)`).
      - tools/web_search_tool.py's module-level `web_search()` (called from
        inside the `@tool("Web Search")`-decorated function's body as
        `web_search(query, max_results=max_results)`).

    Deliberately does NOT monkey-patch the CrewAI Tool objects
    (program_rag_tool / web_search_tool) themselves. CrewAI's own docs
    (https://docs.crewai.com/en/learn/create-custom-tools) confirm tool
    objects expose a `_run` method, but not what attribute the @tool()
    decorator stores the original function under internally, and two
    GitHub raw-source fetches for crewai/tools/base_tool.py (both at tag
    v1.14.6 and on main) returned no usable content, so that internal
    shape is still unconfirmed for this CrewAI version. These objects are
    also very likely pydantic models, which reject plain instance-attribute
    overwrites for anything that isn't a declared field — patching `._run`
    directly could raise at runtime depending on the exact version, and
    there was no way to verify that risk away with the research tools
    available.

    Patching the plain functions one level BELOW the CrewAI tool wrapper
    sidesteps all of that uncertainty: both wrapper bodies call `retrieve`
    / `web_search` as bare names, and Python resolves a bare-name call
    against its DEFINING MODULE's globals at CALL time, not at function-
    definition/decoration time. So reassigning `_program_rag_module.retrieve`
    / `_web_search_module.web_search` here is picked up by the
    already-constructed @tool() closures the next time they run, with zero
    need to understand or touch CrewAI's internal tool-object class
    structure. Because this instruments the real call site directly rather
    than inferring a tool call from a step object's attributes or rendered
    log text, it's treated as the most trustworthy of the three signals
    (see grade()/run_one()) — a confirmed order from this signal is
    PASS-eligible, not capped at INSPECT.

    `calls` collapses consecutive duplicates the same way
    _extract_tool_calls_from_log does, so the recorded order is comparable
    to that signal's output.

    Returns a zero-arg restore() callable. ALWAYS call it (e.g. in a
    `finally` block) once the run is done — `retrieve` and `web_search` are
    shared module-level singletons, imported once at process start, NOT
    rebuilt per agent/Crew instance, so a patch left in place would leak
    into every later case in the same test-script process.
    """
    orig_retrieve = _program_rag_module.retrieve
    orig_web_search = _web_search_module.web_search

    def _tracked_retrieve(*args, **kwargs):
        if not calls or calls[-1] != RAG_TOOL_NAME:
            calls.append(RAG_TOOL_NAME)
        return orig_retrieve(*args, **kwargs)

    def _tracked_web_search(*args, **kwargs):
        if not calls or calls[-1] != WEB_TOOL_NAME:
            calls.append(WEB_TOOL_NAME)
        return orig_web_search(*args, **kwargs)

    _program_rag_module.retrieve = _tracked_retrieve
    _web_search_module.web_search = _tracked_web_search

    def restore() -> None:
        _program_rag_module.retrieve = orig_retrieve
        _web_search_module.web_search = orig_web_search

    return restore


def run_one(agent, case: dict) -> dict:
    """Run one case through Crew.kickoff(), capturing tool-call order via
    all three signals: a direct function-level patch (primary — see
    _wrap_retrieval_functions), step_callback, and a cleaned verbose log
    (used as a fallback and, when the direct patch also fired, as a
    cross-check against it)."""
    task = Task(
        description=case["query"],
        expected_output=(
            "A concise data-grounded answer (3-6 bullet points or a short "
            "paragraph) summarising the program, naming specific courses "
            "or topics where possible, and citing the URL(s) used."
        ),
        agent=agent,
    )

    tool_calls: list[str] = []
    raw_steps: list[str] = []
    direct_calls: list[str] = []

    def _tracker(step_output) -> None:
        raw_steps.append(repr(step_output)[:500])
        name = _extract_tool_name(step_output)
        if name:
            tool_calls.append(name)

    agent.step_callback = _tracker
    agent.verbose = True

    crew = Crew(agents=[agent], tasks=[task], verbose=True)

    buf = io.StringIO()
    t0 = time.time()
    answer = ""
    error: str | None = None
    restore_retrieval = _wrap_retrieval_functions(direct_calls)
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            answer = str(crew.kickoff())
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        traceback.print_exc(file=buf)
    finally:
        # Must always run — retrieve()/web_search() are shared module-level
        # singletons, not rebuilt per case, so a patch left in place would
        # leak into every later case in this process (see
        # _wrap_retrieval_functions's docstring).
        restore_retrieval()
    elapsed = time.time() - t0

    cleaned_log = _clean_log(buf.getvalue())

    # Always computed, even when direct_calls already has an answer — cheap
    # (one regex pass over an in-memory string) and useful purely as a
    # cross-check against the direct-patch signal (see grade()).
    verbose_log_calls = _extract_tool_calls_from_log(cleaned_log)

    # Signal priority, most to least trustworthy (see module docstring and
    # _wrap_retrieval_functions's docstring for the full reasoning):
    #   1. direct_calls         — instruments the real call site directly.
    #   2. tool_calls           — step_callback; silent on tool steps in
    #                             this CrewAI version as of 2026-06-16/17,
    #                             kept first-after-direct in case a future
    #                             CrewAI version starts routing tool steps
    #                             through it.
    #   3. verbose_log_calls    — regex over CrewAI's own rendered log text;
    #                             works, but depends on that text staying in
    #                             a stable shape across CrewAI versions.
    if direct_calls:
        tool_calls_final = direct_calls
        tool_calls_source = "direct_function_patch"
    elif tool_calls:
        tool_calls_final = tool_calls
        tool_calls_source = "step_callback"
    elif verbose_log_calls:
        tool_calls_final = verbose_log_calls
        tool_calls_source = "verbose_log_fallback"
    else:
        tool_calls_final = []
        tool_calls_source = "step_callback"

    crosscheck_mismatch = None
    if direct_calls and verbose_log_calls and direct_calls != verbose_log_calls:
        crosscheck_mismatch = (
            f"cross-check disagreement: the direct function-level patch "
            f"recorded {direct_calls!r}, but the verbose-log fallback "
            f"independently recorded {verbose_log_calls!r} for the same "
            "run. The direct-patch order is graded as authoritative (it "
            "instruments the real call site), but a disagreement between "
            "two independently-implemented signals is worth a manual look "
            "— it could mean either extractor has a bug."
        )

    return {
        "answer": answer,
        "tool_calls": tool_calls_final,
        "tool_calls_source": tool_calls_source,
        "tool_calls_direct": direct_calls,
        "tool_calls_step_callback": tool_calls,
        "tool_calls_verbose_log": verbose_log_calls,
        "tool_calls_crosscheck_mismatch": crosscheck_mismatch,
        "raw_steps": raw_steps,
        "verbose_log": cleaned_log,
        "wall_time_sec": elapsed,
        "error": error,
    }


def grade(case: dict, result: dict) -> dict:
    """Grade from the tool_calls signal — the direct function-level patch
    when it fired (most trustworthy, PASS-eligible), else step_callback,
    else the verbose-log fallback (lower-confidence, caps the verdict at
    INSPECT — see _extract_tool_calls_from_log and
    _wrap_retrieval_functions for the full reasoning behind this priority
    order).
    Returns {"verdict": PASS|INSPECT|FAIL, "hard": [...], "soft": [...]}.
    """
    hard: list[str] = []
    soft: list[str] = []
    calls = result["tool_calls"]

    if result["error"]:
        hard.append(f"runtime error: {result['error']}")

    if result.get("tool_calls_crosscheck_mismatch"):
        soft.append(result["tool_calls_crosscheck_mismatch"])

    if not calls:
        soft.append(
            "no tool calls detected via the direct function-level patch, "
            "step_callback, OR the verbose-log fallback regex — this "
            "likely means the agent's call path doesn't match what any of "
            "the three signals expects, NOT that the agent skipped tools "
            "(unless 'error' above shows a runtime crash before any tool "
            "could run). If even the direct patch came back empty, that's "
            "the most surprising of the three and worth checking first — "
            "see _wrap_retrieval_functions's docstring. Check raw_steps "
            "and verbose_log in this snapshot by hand."
        )
    else:
        if result.get("tool_calls_source") == "verbose_log_fallback":
            soft.append(
                "tool-call order recovered via the verbose-log fallback "
                "regex, NOT step_callback (step_callback recorded zero "
                "steps this run — see _extract_tool_calls_from_log's "
                "docstring). The verdict below is still graded on this "
                "signal since it comes from CrewAI's own structured "
                "'Tool: <name>' log lines, not free text, but treat it as "
                "slightly lower-confidence than a step_callback-confirmed "
                "run until cross-checked against the verbose log."
            )
        if calls[0] != RAG_TOOL_NAME:
            hard.append(
                f"first tool call was {calls[0]!r}, not {RAG_TOOL_NAME!r} — "
                "the backstory's ALWAYS-RAG-first rule was violated"
            )
        web_called = WEB_TOOL_NAME in calls
        if case["expect_web_search"] and not web_called:
            hard.append(
                "expected the local-corpus miss to trigger a Web Search "
                "fallback, but Web Search was never called"
            )
        if not case["expect_web_search"] and web_called:
            soft.append(
                "Web Search was called even though this query should hit "
                "the local corpus cleanly — allowed per backstory ('for "
                "sub-questions it didn't cover'), but worth a manual look "
                "at the answer/verbose_log to confirm that's really why"
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
    path = os.path.join(_HERE, f"university_programs_smoketest_{today}_{llm_slug}.md")

    n_total = len(cases)
    n_pass = sum(1 for g in grades if g["verdict"] == "PASS")
    n_inspect = sum(1 for g in grades if g["verdict"] == "INSPECT")
    n_fail = sum(1 for g in grades if g["verdict"] == "FAIL")

    body: list[str] = [
        f"# University Programs agent — RAG-first/web-search-fallback smoke test — {today}",
        "",
        "## Run config",
        f"- LLM: `{describe_llm_config()}`",
        f"- cases run: {n_total}",
        f"- PASS: {n_pass}",
        f"- INSPECT: {n_inspect}  _(tool-call detection inconclusive, or allowed-but-notable behavior — review manually)_",
        f"- FAIL: {n_fail}",
        "",
        "Verdict key: **PASS** RAG tried first, fallback behavior matched "
        "expectation · **INSPECT** detection signal empty/ambiguous, or a "
        "soft (allowed) deviation worth a human glance · **FAIL** RAG-first "
        "rule violated, expected fallback never fired, or a runtime error.",
        "",
        "Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_university_programs.py`",
        "",
        "## Per-case summary",
        "",
        "| ID | verdict | tool call order | source | wall (s) |",
        "|---|---|---|---|---|",
    ]
    for case, result, grade_r in zip(cases, results, grades):
        body.append(
            f"| {case['id']} | {grade_r['verdict']} "
            f"| {' → '.join(result['tool_calls']) or '(none detected)'} "
            f"| {result.get('tool_calls_source', 'step_callback')} "
            f"| {result['wall_time_sec']:.1f} |"
        )

    body += ["", "---", ""]

    for case, result, grade_r in zip(cases, results, grades):
        verdict = grade_r["verdict"]
        body += [
            f"## [{case['id']}] **{verdict}**",
            "",
            f"**expect_web_search:** {case['expect_web_search']}",
            "",
            "**Query:**",
            "",
            "```",
            case["query"].strip(),
            "```",
            "",
            f"**Wall time:** {result['wall_time_sec']:.1f}s",
            f"**Tool call order ({result.get('tool_calls_source', 'step_callback')}):** "
            f"{' → '.join(result['tool_calls']) or '(none detected)'}",
            "",
            "**All three signals (debug):**",
            f"- direct_function_patch: "
            f"{' → '.join(result.get('tool_calls_direct') or []) or '(none)'}",
            f"- step_callback: "
            f"{' → '.join(result.get('tool_calls_step_callback') or []) or '(none)'}",
            f"- verbose_log_fallback: "
            f"{' → '.join(result.get('tool_calls_verbose_log') or []) or '(none)'}",
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
        body += [
            "**Agent's final answer:**",
            "",
            result["answer"] or "*(no answer produced — see error/verbose_log)*",
            "",
        ]
        if not result["tool_calls"] or result.get("tool_calls_source") != "step_callback":
            body += [
                "**Raw step_callback objects (debug — first 500 chars each):**",
                "",
                "```",
                *(result["raw_steps"] or ["(no steps recorded at all)"]),
                "```",
                "",
            ]
        body += [
            "<details><summary>Cleaned verbose log (secondary cross-check "
            "only — do not trust raw tool-name counts in here, see module "
            "docstring)</summary>",
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
        agent = make_university_programs_agent()  # fresh agent per case
        result = run_one(agent, case)
        grade_r = grade(case, result)
        results.append(result)
        grades.append(grade_r)

        symbol = {"PASS": "✅", "INSPECT": "\U0001f50d", "FAIL": "❌"}.get(
            grade_r["verdict"], "?"
        )
        print(
            f"  {symbol} {grade_r['verdict']}  "
            f"tools={' -> '.join(result['tool_calls']) or '(none)'}  "
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
