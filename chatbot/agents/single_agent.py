"""
single_agent.py — Single-agent (SA) ablation arm (#6).

Additive: does NOT alter make_orchestrator(), build_crew(), run_query(),
any specialist, or any specialist prompt.

One claude-sonnet-4-6 agent with ALL tools from the four specialists
attached, and a merged backstory. max_iter=30 = sum of the four
specialists' individual budgets (Analyst 10 + Univ Programs 6 + News 6
+ Cluster Interpreter 8 = 30), so SA is not starved relative to MA.

DELEGATION INSTRUCTIONS REMOVED from the Orchestrator backstory section
(not applicable; SA has no sub-agents to delegate to):
  - "YOUR FOUR SPECIALISTS" block (describes what sub-agents do — irrelevant
    when there are no sub-agents)
  - "CRITICAL TOOL-USE RULES" about "INVOKE the delegate_work_to_coworker"
  - "CRITICAL DELEGATION RULES" section
  - "MANDATORY ROUTING RULES" section
  - Hard delegation budget: "delegate exactly ONCE per specialist"
  - "IMPORTANT COOPERATION PATTERN" / "FROM-SCRATCH CURRICULUM DESIGN
    COOPERATION PATTERN" delegation steps (delegation language removed;
    the workflow advice about which tools to use in which order is
    preserved in the specialist-tool sections)
KEPT: ANTI-FABRICATION RULE, OUTPUT FORMAT (adapted to use "tool call"
instead of "specialist"), and all citation / synthesis rules.

Guards (all five run):
  Guards #1 and #4 (attribution, delegation-claim) run with delegated_to=[].
  Guards #2 and #3 (numeric, content-attribution) use ToolCallCapture's
  per-tool-call outputs assembled via _build_sa_step_log() — an honest
  grounding pool built from what the SA agent actually queried this run.

CLI:
  python -m chatbot.agents.single_agent "<query>"          # SA mode
  python -m chatbot.agents.single_agent --mode ma "<query>"  # MA run_query()
"""

import argparse
import hashlib  # v62 pilot:
import math     # v62 pilot:
import os
import pickle   # v62 pilot:
import sys
import time
from datetime import datetime, timezone

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from crewai import Agent, Crew, Task  # noqa: E402

from agents.analyst import ANALYST_BACKSTORY  # noqa: E402
from agents.cluster_interpreter import CLUSTER_INTERPRETER_BACKSTORY  # noqa: E402
from agents.news import NEWS_BACKSTORY  # noqa: E402
from agents.university_programs import UNIVERSITY_PROGRAMS_BACKSTORY  # noqa: E402
from agents.orchestrator import (  # noqa: E402
    _RUN_RECORDS_DIR,
    _SPECIALIST_ROLES,
    _detect_content_attribution_flags,
    _detect_delegation_claim_flags,
    _detect_fabrication_flags,
    _detect_numeric_fabrication_flags,
    _format_cost_section,
    _format_step,
    _is_tool_call,
)
from llm import describe_llm_config, get_llm  # noqa: E402
from tools.cluster_tool import CLUSTER_TOOLS, FOCUSED_CLUSTERS, data_wave_override_notice  # noqa: E402  # v62 pilot: FOCUSED_CLUSTERS
from tools.tool_capture import ToolCallCapture  # noqa: E402
from tools.compose_tool import COMPOSE_TOOLS, SECTOR_WRAP_TOOLS  # noqa: E402
from tools.csv_tool import CSV_TOOLS  # noqa: E402
from tools.lift_tool import LIFT_TOOLS, focal_associations  # noqa: E402  # v62 pilot: focal_associations
from tools.news_tool import news_rag_tool  # noqa: E402
from tools.program_rag_tool import program_rag_tool  # noqa: E402
from tools.rag_tool import skills_rag_tool  # noqa: E402
from tools.web_search_tool import web_search_tool  # noqa: E402
from tools.pair_verify import format_pair_verify_section, run_pair_verify  # v62 pilot4:


# ── Synthetic step_log adapter for SA guards #2/#3 ────────────────────────────
# Guards #2 (_detect_numeric_fabrication_flags) and #3
# (_detect_content_attribution_flags) both call _build_consulted_text()
# internally, which extracts step["output"].output for each step whose role
# is in _SPECIALIST_ROLES and also in delegated_to.  For SA we have no
# real specialist steps, but we DO have captured tool call outputs from
# ToolCallCapture.  This adapter synthesises a single "specialist" step
# (role = _SPECIALIST_ROLES[0]) whose output is the concatenation of all
# captured tool outputs — giving the guards an honest grounding pool built
# from what the single agent ACTUALLY queried this run.

class _MockOutput:
    """Minimal object whose .output attribute _build_consulted_text() reads."""
    __slots__ = ("output",)

    def __init__(self, text: str) -> None:
        self.output = text


def _build_sa_step_log(
    tool_call_log: list[dict],
) -> tuple[list[dict], list[str]]:
    """Return a synthetic (step_log, delegated_to) for SA guards #2/#3.

    Concatenates every captured tool output into one text block and wraps it
    in a single step entry whose role is the first entry in _SPECIALIST_ROLES
    ("Skills Taxonomy Analyst").  _build_consulted_text() will include that
    step because its role is in _SPECIALIST_ROLES AND in delegated_to.

    The resulting grounding pool contains exactly the information the SA
    agent actually retrieved — no more and no less.
    """
    consulted = "\n\n".join(
        f"[Tool: {c['tool']}]\n{c['output']}" for c in tool_call_log
    )
    synthetic_role = _SPECIALIST_ROLES[0]  # "Skills Taxonomy Analyst"
    step_log = [{"role": synthetic_role, "output": _MockOutput(consulted)}]
    delegated_to = [synthetic_role]
    return step_log, delegated_to


# ── Synthesis rules (adapted from ORCHESTRATOR_BACKSTORY) ─────────────────────
# Delegation-specific language removed; "specialist you delegated to" →
# "tool call you made"; specialist-name attribution explicitly forbidden
# (no specialists exist in this arm).

_SA_SYNTHESIS_RULES = """\
ANTI-FABRICATION RULE — READ THIS BEFORE OUTPUT FORMAT BELOW, IT CONDITIONS
THE LIFT/SIGNIFICANCE PREFERENCE.
Rules, no exceptions:
- You may state a numeric metric (lift, z, frequency, posting count,
  composed lift) ONLY if that EXACT value was returned by a tool call
  YOU MADE IN THIS RUN. Never generate, estimate, interpolate, round to a
  "plausible" figure, recall a number from training data, or convert one
  metric into another (e.g. never invent a lift/z pair to accompany a
  frequency-only result, and never invent a frequency to accompany a
  lift-only result).
- The "prefer lift/z over frequency" instruction in OUTPUT FORMAT below
  applies ONLY when lift tools were actually called AND returned lift/z
  values this run. If lift tools were not called and the only grounded
  metric you have is the cluster tool's market frequency, PRESENT THAT
  FREQUENCY, clearly labelled "(market frequency)" — do NOT manufacture
  lift/z just to match the preferred format. A correctly-labelled
  frequency number is honest; an invented lift/z pair is not, even if it
  "looks more rigorous."
- If a recommended skill has no tool-returned metric, present it as a
  qualitative gap/recommendation with no number, rather than inventing one.
- Do NOT attribute findings to a "Skills Taxonomy Analyst," "University
  AI Programs Researcher," "AI Industry News Researcher," "Cluster
  Interpreter," or any other named specialist — no specialists exist in
  this run configuration; you called the tools directly. Do NOT write
  sentences like "identified by the Skills Taxonomy Analyst" or "the
  University AI Programs Researcher reports." Do NOT claim to have
  "consulted" a specialist you never delegated to — delegation is not
  available in this run.

OUTPUT FORMAT for your final answer:
- Open with a 2-3 sentence executive summary of the recommendation.
- Then a structured body with concrete picks (skills to add, topics
  to emphasise, courses to update). Cite the evidence from ALL tools
  ACTUALLY called this run (see ANTI-FABRICATION RULE above — never cite
  a metric or attribution from a tool you did not call):
    * IF lift tools were called and returned lift/significance data:
      Lift (×) and significance (z), e.g. "Large Language Models (lift
      6.17×, z=9.56)" — this is the grounding metric: what's DISTINCTIVELY
      co-demanded, not merely popular. Raw frequency (e.g. "4,278
      postings") may appear as secondary scale/context but must never be
      the only number attached to a recommended skill.
    * IF lift tools were NOT called this run: do NOT include a lift/z
      line at all. Cite whatever grounded metric the tools you DID call
      returned — e.g. the cluster tool's market frequency, clearly
      labelled "(market frequency)" — and do not describe it as "lift"
      or "significance."
    * Peer-program course names + URLs (from program_rag_tool /
      web_search_tool).
    * Recent article titles + sources + dates (from news_rag_tool).
  If a tool was not called (because the query truly didn't need it),
  say so explicitly rather than leaving the section blank — and never
  manufacture the numbers that tool would have provided.
- Close with the trade-off or caveat the professor should consider.
"""

# v62 pilot: read SA_PROCEDURE at import time (plain or structured; default plain)
# v62 pilot2: also supports "general" (multi-part request procedure)
_SA_PROCEDURE: str = os.environ.get("SA_PROCEDURE", "plain")

# v62 pilot2: full capture flag — when set, write complete tool outputs to main .md
_CAPTURE_FULL_OUTPUT: bool = os.environ.get("CAPTURE_FULL_OUTPUT", "").strip() == "1"

_SA_PLAIN_BACKSTORY = (
    "===== SKILLS TAXONOMY ANALYST TOOLS =====\n"
    + ANALYST_BACKSTORY
    + "\n\n===== UNIVERSITY AI PROGRAMS RESEARCHER TOOLS =====\n"
    + UNIVERSITY_PROGRAMS_BACKSTORY
    + "\n\n===== AI INDUSTRY NEWS RESEARCHER TOOLS =====\n"
    + NEWS_BACKSTORY
    + "\n\n===== CLUSTER INTERPRETER TOOLS =====\n"
    + CLUSTER_INTERPRETER_BACKSTORY
    + "\n\n===== SYNTHESIS AND OUTPUT RULES =====\n"
    + _SA_SYNTHESIS_RULES
)

# v62 pilot: pinned hash of the plain backstory — asserted in test_single_agent.py
_SA_PLAIN_BACKSTORY_HASH: str = "f0a10a8206ae4a4712cb4b6dd9e5175efb2f6fd6cce9efb0d1c1cd0814dfe700"

# v62 pilot: step-by-step working procedure appended when SA_PROCEDURE=structured
_SA_PROCEDURE_TEXT: str = (
    "\n\n===== WORKING PROCEDURE =====\n"
    "WORKING PROCEDURE FOR CURRICULUM-DESIGN REQUESTS (follow in order):\n"
    "1. Call All Clusters Overview once to get the demand-cluster scaffold.\n"
    "2. Draft the course list (each course's title and the cluster or clusters it draws on) "
    "before writing any course in full.\n"
    "3. For EACH course, choose the one skill that best names that course's own area "
    "(its focal skill: the course's core method, tool or topic; use agentic AI only for a "
    "course about agentic AI) and call Skill Lift / Differential Analysis with that focal "
    "skill before writing the course. Use a different focal skill for each course unless "
    "two courses genuinely share one.\n"
    "4. In each course's rationale, cite lift and z values only from that course's own "
    "focal-skill call, and name the focal skill.\n"
    "5. Use Cluster Detail for any cluster whose skills you need in more detail. Use "
    "University Program RAG only if the request asks for a comparison with existing programs, "
    "and AI News RAG for current industry signal.\n"
    "6. Do not state any number that did not come from a tool output in this run."
)

# v62 pilot2: working procedure for multi-part requests appended when SA_PROCEDURE=general
_SA_GENERAL_PROCEDURE_TEXT: str = (
    "\n\n===== WORKING PROCEDURE =====\n"
    "WORKING PROCEDURE FOR MULTI-PART REQUESTS (follow in order):\n"
    "1. Before calling any tool, list every part the request asks for.\n"
    "2. For each part, call the tools that hold its evidence before writing that part: "
    "peer programs → University Program RAG (web search only if the program is not in "
    "the corpus); demand structure and gaps → All Clusters Overview / Cluster Detail and "
    "Skill Lift / Differential Analysis; anything about a sector → the sector compose or "
    "sector wrap tools; recent developments → AI News RAG.\n"
    "3. When you propose a course, call Skill Lift / Differential Analysis for that course's "
    "own focal skill and cite its values for that course.\n"
    "4. State only numbers, course codes, URLs and institution names that came from a tool "
    "output in this run.\n"
    "5. Answer every part under its own heading, in the order the request gave them."
)

# v62 pilot5: step appended when SA_PROCEDURE=sequenced (after general steps 1-5)
_SA_SEQUENCED_STEP_TEXT: str = (
    "\n6. Order: first call University Program RAG and the cluster tools, and settle "
    "the gaps and the two courses you will propose. Only then call Skill Lift / "
    "Differential Analysis, once for each proposed course's own focal skill, and the "
    "sector tools. Do not call Skill Lift / Differential Analysis before the gaps and "
    "proposed courses are settled."
)  # v62 pilot5:

# v62 pilot: SA_BACKSTORY is extended with the relevant procedure text when
# SA_PROCEDURE=structured or SA_PROCEDURE=general; byte-identical to
# _SA_PLAIN_BACKSTORY otherwise.  # v62 pilot2: added general branch; v62 pilot5: added sequenced
SA_BACKSTORY: str = (
    _SA_PLAIN_BACKSTORY + _SA_GENERAL_PROCEDURE_TEXT + _SA_SEQUENCED_STEP_TEXT
    if _SA_PROCEDURE == "sequenced"  # v62 pilot5:
    else (
        _SA_PLAIN_BACKSTORY + _SA_PROCEDURE_TEXT
        if _SA_PROCEDURE == "structured"
        else (
            _SA_PLAIN_BACKSTORY + _SA_GENERAL_PROCEDURE_TEXT
            if _SA_PROCEDURE == "general"  # v62 pilot2:
            else _SA_PLAIN_BACKSTORY
        )
    )
)

# v62 pilot2: pinned hashes for structured and general backstories
# Computed by: hashlib.sha256(SA_BACKSTORY.encode()).hexdigest() with each SA_PROCEDURE value.
# Update when the corresponding procedure text changes.
_SA_STRUCTURED_BACKSTORY_HASH: str = "eca9b063b9b5bd569aac19a998288b184e82bd069e2212d3ab3748f9f240570d"  # v62 pilot2:
_SA_GENERAL_BACKSTORY_HASH: str = "db06f4850506ed02099f9db9ab61656cc2e7f39f944aacb84bd744aea9c7a23e"    # v62 pilot2:
_SA_SEQUENCED_BACKSTORY_HASH: str = "126954bc48469a009b137a3374369ed0fd88ba673dcdf7a591bbcbc89dc0ac95"  # v62 pilot5:

# Exact union of all four specialists' tool lists, same tool objects.
_SA_TOOLS = [
    skills_rag_tool,
    *CSV_TOOLS,
    *LIFT_TOOLS,
    *SECTOR_WRAP_TOOLS,
    *COMPOSE_TOOLS,
    program_rag_tool,
    web_search_tool,
    news_rag_tool,
    *CLUSTER_TOOLS,
]


def _run_sa_preflight() -> bool:  # v62 pilot:
    """Check data-integrity invariants before each v62 SA run.

    Five checks (all required):
    1. Lift table: Agentic AI → Large Language Models lift≈4.76 / z≈9.39
    2. FOCUSED_CLUSTERS == {1, 2, 3, 5, 6}
    3. FAISS skills index: ntotal=962, 0 Unknown/empty level1 docs
    4. Queen's MMAI document is in the program index  # v62 pilot2:
    5. Finance sector compose tool returns >=1 row for focal Agentic AI  # v62 pilot2:

    Returns True if all pass. Prints status for each check.
    """
    import faiss as _faiss  # v62 pilot: lazy import, same lib LangChain uses

    _EXP_FOCAL   = "Agentic AI"
    _EXP_PARTNER = "Large Language Models"
    _EXP_LIFT    = 4.76
    _EXP_Z       = 9.39
    _EXP_FOCUSED = frozenset({1, 2, 3, 5, 6})
    _EXP_NTOTAL  = 962

    ok = True
    print(f"\n{'─'*64}")
    print("PREFLIGHT [v62 SA]")
    print(f"{'─'*64}")

    # ── check 1: lift table ───────────────────────────────────────────────────
    assocs = focal_associations(_EXP_FOCAL, z_min=0.0)
    partner_row = next(
        (a for a in assocs if a.get("skill", "").lower() == _EXP_PARTNER.lower()),
        None,
    )
    if partner_row is None:
        print(f"\n  [X] lift check: no '{_EXP_PARTNER}' row for focal '{_EXP_FOCAL}'")
        ok = False
    else:
        got_lift = float(partner_row.get("lift", 0))
        got_z    = float(partner_row.get("z", 0))
        match_l  = math.isclose(got_lift, _EXP_LIFT, rel_tol=0.005)
        match_z  = math.isclose(got_z,   _EXP_Z,    rel_tol=0.005)
        print(f"\n  [{'OK' if match_l else 'X'}] lift: got {got_lift}  expected {_EXP_LIFT}")
        print(f"  [{'OK' if match_z else 'X'}] z   : got {got_z}     expected {_EXP_Z}")
        if not (match_l and match_z):
            ok = False

    # ── check 2: FOCUSED_CLUSTERS ─────────────────────────────────────────────
    match_fc = FOCUSED_CLUSTERS == _EXP_FOCUSED
    print(f"\n  [{'OK' if match_fc else 'X'}] FOCUSED_CLUSTERS: "
          f"got {sorted(FOCUSED_CLUSTERS)}  expected {sorted(_EXP_FOCUSED)}")
    if not match_fc:
        ok = False

    # ── check 3: FAISS index ntotal + 0 Unknown ──────────────────────────────
    _idx_path = os.path.join(_CHATBOT_DIR, "faiss_index", "index.faiss")
    _pkl_path = os.path.join(_CHATBOT_DIR, "faiss_index", "index.pkl")
    try:
        raw_idx = _faiss.read_index(_idx_path)
        ntotal  = raw_idx.ntotal
        match_n = ntotal == _EXP_NTOTAL
        print(f"\n  [{'OK' if match_n else 'X'}] index ntotal: got {ntotal}  expected {_EXP_NTOTAL}")
        if not match_n:
            ok = False
        with open(_pkl_path, "rb") as _pf:
            _docstore, _id_map = pickle.load(_pf)
        n_unknown = sum(
            1 for doc in _docstore._dict.values()
            if doc.metadata.get("level1", "") in ("", "Unknown")
        )
        match_u = n_unknown == 0
        print(f"  [{'OK' if match_u else 'X'}] Unknown level1 docs: {n_unknown}  expected 0")
        if not match_u:
            ok = False
    except Exception as _e:
        print(f"\n  [X] FAISS index check failed: {_e}")
        ok = False

    # ── check 4: Queen's MMAI in program index  # v62 pilot2: ───────────────────
    try:
        from tools.program_rag_tool import retrieve as _prog_retrieve
        hits = _prog_retrieve("Queen's MMAI Master of Management Artificial Intelligence")
        queens_found = any(
            "queen" in (h.get("content", "") + h.get("title", "") + h.get("source", "")).lower()
            for h in hits
        )
        print(f"\n  [{'OK' if queens_found else 'X'}] Queen's MMAI in program index: "
              f"{'found' if queens_found else 'NOT FOUND'} in top results")
        if not queens_found:
            ok = False
    except Exception as _e:
        print(f"\n  [X] Queen's MMAI program index check failed: {_e}")
        ok = False

    # ── check 5: finance sector compose returns rows  # v62 pilot2: ─────────────
    try:
        from tools.compose_tool import composed_curriculum as _compose
        rows = _compose("finance")
        n_rows = len(rows)
        match_compose = n_rows >= 1
        print(f"\n  [{'OK' if match_compose else 'X'}] Finance sector compose rows: "
              f"got {n_rows}  expected >=1")
        if not match_compose:
            ok = False
    except Exception as _e:
        print(f"\n  [X] Finance sector compose check failed: {_e}")
        ok = False

    # ── check 6: pair_verify.py frozen SHA-256 (v62 pilot5) ───────────────────
    _PV_FROZEN_HASH = "c0c66fa02a51b512ce52ec1f82e0f7fe07a56117b29f503acea064ea1672e2fb"
    try:
        import hashlib as _hl
        _pv_path = os.path.join(_CHATBOT_DIR, "tools", "pair_verify.py")
        with open(_pv_path, "rb") as _pv_f:
            _pv_hash = _hl.sha256(_pv_f.read()).hexdigest()
        match_pv = _pv_hash == _PV_FROZEN_HASH
        print(f"\n  [{'OK' if match_pv else 'X'}] pair_verify.py SHA-256: {_pv_hash}")
        if not match_pv:
            ok = False
    except Exception as _e:
        print(f"\n  [X] pair_verify.py hash check failed: {_e}")
        ok = False

    # ── check 7: Georgia Tech MSCS AI in program index (v62 pilot5) ───────────
    try:
        from tools.program_rag_tool import retrieve as _prog_retrieve2
        _gt_hits = _prog_retrieve2("Georgia Tech MS CS Artificial Intelligence specialization")
        _gt_chunks = sum(
            1 for h in _gt_hits
            if "georgia" in (h.get("file", "") + h.get("program", "")).lower()
        )
        match_gt = _gt_chunks >= 1
        print(f"\n  [{'OK' if match_gt else 'X'}] Georgia Tech in program index: "
              f"{_gt_chunks} chunk(s) in top results")
        if not match_gt:
            ok = False
    except Exception as _e:
        print(f"\n  [X] Georgia Tech program index check failed: {_e}")
        ok = False

    # ── check 8: healthcare sector_wrap returns rows (v62 pilot5) ─────────────
    try:
        from tools.compose_tool import sector_wrap as _sector_wrap
        _hw_rows = _sector_wrap("healthcare")
        match_hw = len(_hw_rows) >= 1
        print(f"\n  [{'OK' if match_hw else 'X'}] sector_wrap_tool(healthcare) rows: "
              f"got {len(_hw_rows)}  expected >=1")
        if not match_hw:
            ok = False
    except Exception as _e:
        print(f"\n  [X] sector_wrap healthcare check failed: {_e}")
        ok = False

    # ── check 9: healthcare composed_curriculum returns rows (v62 pilot5) ─────
    try:
        from tools.compose_tool import composed_curriculum as _compose_hc
        _hc_rows = _compose_hc("healthcare")
        match_hc = len(_hc_rows) >= 1
        print(f"\n  [{'OK' if match_hc else 'X'}] composed_sector_tool(healthcare) rows: "
              f"got {len(_hc_rows)}  expected >=1")
        if not match_hc:
            ok = False
    except Exception as _e:
        print(f"\n  [X] composed_curriculum healthcare check failed: {_e}")
        ok = False

    print(f"\n  {'PREFLIGHT PASS' if ok else 'PREFLIGHT FAIL -- aborting'}")
    print(f"{'─'*64}\n")
    return ok


def make_single_agent() -> Agent:
    """Build the SA ablation agent — one agent, all specialist tools."""
    return Agent(
        role="Curriculum Advisor (single agent)",
        goal=(
            "Answer the professor's curriculum-design question by calling "
            "all necessary tools directly — skills-demand RAG and lift/z "
            "analysis, compose/sector tools, university-program RAG and "
            "web search, news RAG, cluster overview and detail — and "
            "synthesising a single coherent, fully-grounded recommendation."
        ),
        backstory=SA_BACKSTORY,
        tools=_SA_TOOLS,
        llm=get_llm(),
        verbose=False,
        allow_delegation=False,
        # Combined budget of the four specialists:
        # Analyst 10 + Univ Programs 6 + News 6 + Cluster Interpreter 8 = 30.
        max_iter=30,
        max_retry_limit=1,
    )


def _write_sa_run_record(
    query: str,
    step_log: list[dict],
    wall_time_sec: float,
    answer: str | None,
    error: Exception | None,
    usage_metrics: object | None = None,
    tool_call_log: list[dict] | None = None,
    label: str = "",  # v62 pilot:
    pair_verify_summary: dict | None = None,  # v62 pilot4:
) -> str:
    """Write a durable run record for a SA ablation run.

    Filename includes '_single-agent' so SA and MA records are
    distinguishable at a glance in run_records/.

    Guard design:
    - Guards #1 and #4 (attribution + delegation-claim): always run with
      delegated_to=[] — flags any answer that names a specialist as a
      source or claims to have consulted one.
    - Guards #2 and #3 (numeric + content-attribution): run when
      tool_call_log is provided (non-empty).  The tool outputs captured
      via ToolCallCapture are assembled via _build_sa_step_log() into a
      synthetic step_log whose consulted_text is the concatenation of
      everything the SA agent actually queried — an honest grounding pool.
      Skipped (with a note) when tool_call_log is None or empty, to avoid
      flagging every number/URL against an empty pool.
    """
    os.makedirs(_RUN_RECORDS_DIR, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    status = "failure" if error is not None else "success"
    _label_part = f"{label}_" if label else ""  # v62 pilot:
    path = os.path.join(
        _RUN_RECORDS_DIR, f"run_{ts}_{_label_part}{status}_single-agent.md"
    )
    full_path = path[: -len(".md")] + "_full.md"

    tool_call_count = sum(1 for step in step_log if _is_tool_call(step))
    captured_count = len(tool_call_log) if tool_call_log else 0

    # Guards #1 + #4 — always run with delegated_to=[]
    flags_1_4 = (
        _detect_fabrication_flags(answer, delegated_to=[])
        + _detect_delegation_claim_flags(answer, delegated_to=[])
        if answer
        else []
    )

    # Guards #2 + #3 — run when we have captured tool call outputs
    flags_2_3: list[str] = []
    guards_2_3_status: str
    if answer and tool_call_log:
        sa_step_log, sa_delegated_to = _build_sa_step_log(tool_call_log)
        flags_2_3 = (
            _detect_numeric_fabrication_flags(answer, sa_step_log, sa_delegated_to)
            + _detect_content_attribution_flags(
                answer, query, sa_step_log, sa_delegated_to
            )
        )
        guards_2_3_status = f"{flags_2_3 or '[]'}"
    else:
        guards_2_3_status = (
            "SKIPPED — "
            + ("no captured tool calls (ToolCallCapture returned 0)" if answer else "no answer produced")
        )

    all_flags = flags_1_4 + flags_2_3

    lines = [
        f"# Single-agent run — {ts} — {status.upper()}",
        "",
        f"**Query:** {query}",
        "",
        f"**Model:** {describe_llm_config()}",
        f"**SA_PROCEDURE:** {_SA_PROCEDURE}",  # v62 pilot:
        f"**CAPTURE_FULL_OUTPUT:** {'1' if _CAPTURE_FULL_OUTPUT else '0'}",  # v62 pilot2:
        "",
        "## Metrics",
        f"- **Status:** {status}",
        f"- **Error:** {f'{type(error).__name__}: {error}' if error else 'None'}",
        "- **Arm:** single-agent (SA ablation #6)",
        f"- **Tool calls (step_callback):** {tool_call_count}",
        f"- **Tool calls (ToolCallCapture):** {captured_count}",
        f"- **Wall time:** {wall_time_sec:.1f}s",
        f"- **fabrication_flags (guards #1+#4):** {flags_1_4 or '[]'}",
        f"- **fabrication_flags (guards #2+#3):** {guards_2_3_status}",
        "",
    ]
    lines += _format_cost_section(usage_metrics)

    if all_flags:
        lines += [
            "## ⚠️ FABRICATION WARNING ⚠️",
            "",
            "One or more guards flagged the final answer. Guards #1+#4: "
            "specialist-name attribution or affirmative delegation claim with "
            "delegated_to=[]. Guards #2+#3 (when run): numeric or content "
            "value not grounded in any captured tool output. "
            "FLAG-don't-strip throughout — nothing below was removed, only flagged:",
            "",
        ]
        for flag in all_flags:
            lines.append(f"- {flag}")
        lines.append("")

    # ── Tool Calls section (from ToolCallCapture) ─────────────────────────────
    # Track split point so full_lines can use untruncated tool outputs while
    # lines shares the common prefix.
    tc_header = [
        f"## Tool Calls (ToolCallCapture — {captured_count} call(s))",
        "",
    ]
    tc_lines: list[str] = []
    tc_full_lines: list[str] = []
    if tool_call_log:
        for i, c in enumerate(tool_call_log, 1):
            # Summary record: input + first 400 chars of output
            tc_lines.append(f"### {i}. {c['tool']}")
            tc_lines.append(f"**Input:** `{c['input']}`")
            out_preview = c["output"][:400].replace("\n", " ")
            tc_lines.append(
                f"**Output ({c['output_len']} chars total):** {out_preview}…"
                if c["output_len"] > 400 else
                f"**Output ({c['output_len']} chars):** {c['output']}"
            )
            tc_lines.append("")
            # Full record: complete output in fenced block
            tc_full_lines.append(f"### {i}. {c['tool']}")
            tc_full_lines.append(f"**Input:** `{c['input']}`")
            tc_full_lines.append(f"**Output ({c['output_len']} chars):**")
            tc_full_lines.append("```")
            tc_full_lines.append(c["output"])
            tc_full_lines.append("```")
            tc_full_lines.append("")
    else:
        no_cap = "_(ToolCallCapture returned 0 calls — tools ran via an unpatched path)_"
        tc_lines = [no_cap, ""]
        tc_full_lines = [no_cap, ""]

    split_idx = len(lines)  # index in lines[] where TC section will start
    # v62 pilot2: when CAPTURE_FULL_OUTPUT=1, main .md also uses full output
    main_tc_lines = tc_full_lines if _CAPTURE_FULL_OUTPUT else tc_lines
    lines += tc_header + main_tc_lines

    # full_lines: identical prefix, then tc_full_lines instead of tc_lines
    full_lines: list[str] = list(lines[:split_idx]) + tc_header + tc_full_lines

    # ── Final Answer + step trace (appended to both) ───────────────────────────
    tail: list[str] = [
        "## Final Answer"
        if error is None
        else "## Partial Answer (run failed before completion)",
        "",
        answer if answer else "_(none — failed before any answer was produced)_",
        "",
    ]
    tail += format_pair_verify_section(pair_verify_summary)  # v62 pilot4: ([] when summary is None)
    tail += [
        f"## Per-Agent Tool-Call Trace ({len(step_log)} step(s))",
        "",
    ]
    if step_log:
        tail.append(
            f"Traces capped at 20,000 chars for readability — full trace "
            f"always in: `{os.path.basename(full_path)}`."
        )
        tail.append("")
    lines += tail
    full_lines += tail

    if step_log:
        by_role: dict[str, int] = {}
        for step in step_log:
            role = step["role"]
            by_role[role] = by_role.get(role, 0) + 1
            header = [f"### {role} — step {by_role[role]}", ""]
            lines += header + _format_step(step) + [""]
            full_lines += header + _format_step(step, max_chars=None) + [""]
    else:
        lines.append("_(no steps completed)_")
        full_lines.append("_(no steps completed)_")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    with open(full_path, "w", encoding="utf-8") as f:
        f.write("\n".join(full_lines))
    return path


def run_query_single(query: str, label: str = "") -> str:  # v62 pilot: label
    """Run a single professor query end-to-end in single-agent mode.

    Mirrors run_query() from orchestrator.py in structure, but with one
    Agent holding all specialist tools instead of five agents in a
    hub-and-spoke topology.  Every run — success or failure — is written
    as a durable record via _write_sa_run_record().
    """
    # v62 pilot: preflight must pass before any LLM call
    if not _run_sa_preflight():
        raise RuntimeError("SA preflight failed — aborting run. See output above.")

    # Same data-wave override injection point as run_query().
    _wave_notice = data_wave_override_notice()
    if _wave_notice:
        query = f"{_wave_notice}\n\n{query}"

    agent = make_single_agent()
    step_log: list[dict] = []

    def _tracker(output) -> None:
        step_log.append({"role": "Curriculum Advisor (single agent)", "output": output})

    agent.step_callback = _tracker

    task = Task(
        description=query,
        expected_output=(
            "A single coherent recommendation for the professor. Open with "
            "a 2-3 sentence executive summary. Then a structured body of "
            "concrete recommendations. ANTI-FABRICATION (non-negotiable): "
            "every number you cite (lift, z, frequency, posting count) "
            "must be a value actually returned by a tool call you made "
            "this run — never invented, estimated, or converted. Do NOT "
            "attribute findings to a named specialist (Skills Taxonomy "
            "Analyst, University AI Programs Researcher, AI Industry News "
            "Researcher, Cluster Interpreter) — no specialists exist in "
            "this run; you called the tools directly. "
            "IF lift tools were called and returned lift/z data, cite "
            "specific skills with their lift (×) and significance (z). "
            "IF lift tools were NOT called, cite the cluster tool's market "
            "frequency instead, clearly labelled as frequency, not lift. "
            "Also cite: peer-program courses with URLs (from program_rag_tool "
            "/ web_search_tool), recent articles with titles + sources (from "
            "news_rag_tool), and — where relevant — a cluster-level gap "
            "analysis or scaffold with priority recommendations (from cluster "
            "tools). Close with a trade-off or caveat."
        ),
        agent=agent,
    )
    crew = Crew(agents=[agent], tasks=[task], verbose=False)
    t0 = time.time()
    with ToolCallCapture(tools=_SA_TOOLS, max_output_chars=10**9 if _CAPTURE_FULL_OUTPUT else 3_000) as cap:  # v62 pilot2:
        try:
            answer = str(crew.kickoff())
        except Exception as e:
            wall_time = time.time() - t0
            usage_metrics = getattr(crew, "usage_metrics", None)
            path = _write_sa_run_record(
                query, step_log, wall_time,
                answer=None, error=e, usage_metrics=usage_metrics,
                tool_call_log=cap.calls, label=label,
                pair_verify_summary=None,  # v62 pilot4:
            )
            raise RuntimeError(
                f"{type(e).__name__}: {e}\n\n"
                f"Partial SA output ({len(step_log)} step(s) completed "
                f"before failure) saved to: {path}"
            ) from e
    wall_time = time.time() - t0
    usage_metrics = getattr(crew, "usage_metrics", None)
    # v62 pilot4: opt-in pair verification (no-op when PAIR_VERIFY=0)
    _pv_evidence = [
        line
        for call in cap.calls
        for line in str(call.get("output", "")).split("\n")
        if line.strip()
    ]
    answer, _pv_summary = run_pair_verify(answer, _pv_evidence, llm=get_llm())
    path = _write_sa_run_record(
        query, step_log, wall_time,
        answer=answer, error=None, usage_metrics=usage_metrics,
        tool_call_log=cap.calls, label=label,
        pair_verify_summary=_pv_summary,  # v62 pilot4:
    )
    return answer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run a curriculum-design query in the SA or MA arm."
    )
    parser.add_argument(
        "query",
        nargs="+",
        help="Professor's query (multiple words are joined into one string).",
    )
    parser.add_argument(
        "--mode",
        choices=["sa", "ma"],
        default="sa",
        help="'sa' = single-agent ablation (default); 'ma' = multi-agent run_query().",
    )
    args = parser.parse_args()
    q = " ".join(args.query)
    if args.mode == "ma":
        from agents.orchestrator import run_query  # noqa: E402
        result = run_query(q)
    else:
        result = run_query_single(q)
    print(result)
