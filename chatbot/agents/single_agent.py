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
import os
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
from tools.cluster_tool import CLUSTER_TOOLS, data_wave_override_notice  # noqa: E402
from tools.tool_capture import ToolCallCapture  # noqa: E402
from tools.compose_tool import COMPOSE_TOOLS, SECTOR_WRAP_TOOLS  # noqa: E402
from tools.csv_tool import CSV_TOOLS  # noqa: E402
from tools.lift_tool import LIFT_TOOLS  # noqa: E402
from tools.news_tool import news_rag_tool  # noqa: E402
from tools.program_rag_tool import program_rag_tool  # noqa: E402
from tools.rag_tool import skills_rag_tool  # noqa: E402
from tools.web_search_tool import web_search_tool  # noqa: E402


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

SA_BACKSTORY = (
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
    path = os.path.join(
        _RUN_RECORDS_DIR, f"run_{ts}_{status}_single-agent.md"
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
    lines += tc_header + tc_lines

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


def run_query_single(query: str) -> str:
    """Run a single professor query end-to-end in single-agent mode.

    Mirrors run_query() from orchestrator.py in structure, but with one
    Agent holding all specialist tools instead of five agents in a
    hub-and-spoke topology.  Every run — success or failure — is written
    as a durable record via _write_sa_run_record().
    """
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
    with ToolCallCapture(tools=_SA_TOOLS) as cap:
        try:
            answer = str(crew.kickoff())
        except Exception as e:
            wall_time = time.time() - t0
            usage_metrics = getattr(crew, "usage_metrics", None)
            path = _write_sa_run_record(
                query, step_log, wall_time,
                answer=None, error=e, usage_metrics=usage_metrics,
                tool_call_log=cap.calls,
            )
            raise RuntimeError(
                f"{type(e).__name__}: {e}\n\n"
                f"Partial SA output ({len(step_log)} step(s) completed "
                f"before failure) saved to: {path}"
            ) from e
    wall_time = time.time() - t0
    usage_metrics = getattr(crew, "usage_metrics", None)
    path = _write_sa_run_record(
        query, step_log, wall_time,
        answer=answer, error=None, usage_metrics=usage_metrics,
        tool_call_log=cap.calls,
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
