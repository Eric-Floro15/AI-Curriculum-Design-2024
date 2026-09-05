"""
orchestrator.py — The Orchestrator agent + multi-agent crew assembly.

Role: receives the professor's natural-language query, decides which
sub-agents to consult, and synthesises their outputs into a single
coherent recommendation.

Crew composition (5 agents total):
  Orchestrator + Skills Taxonomy Analyst + University AI Programs
  Researcher + AI Industry News Researcher + Cluster Interpreter.

The University AI Programs Researcher handles BOTH comparative-program
queries AND structured curriculum-fetch tasks (for gap analysis).
The old Curriculum Architect agent has been merged into it.

Delegation pattern: the Orchestrator has `allow_delegation=True`, which
in CrewAI auto-injects two tools — "Delegate work to coworker" and
"Ask question to coworker" — pointed at the other agents in the same
Crew. The LLM decides when to call them.
"""

import os
import sys
import time
from datetime import datetime, timezone

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from crewai import Agent, Crew, Task  # noqa: E402

from agents.analyst import make_analyst  # noqa: E402
from agents.cluster_interpreter import make_cluster_interpreter  # noqa: E402
from agents.news import make_news_agent  # noqa: E402
from agents.university_programs import make_university_programs_agent  # noqa: E402
from llm import describe_llm_config, get_llm  # noqa: E402


ORCHESTRATOR_BACKSTORY = """\
You are a senior curriculum advisor coordinating four specialist
researchers to help a university professor design or update an AI/ML
Master's program. You do NOT answer the professor directly from your
own knowledge — you delegate to your specialists and synthesise their
outputs.

YOUR FOUR SPECIALISTS:

1. **Skills Taxonomy Analyst** — knows what skills are in demand in
   the AI/ML job market. Backed by 10,600+ job postings, ~871 canonical
   skills, 10 ensemble clusters. Use when the question touches market
   demand, skill frequencies, in-demand topics, or cluster themes.

2. **University AI Programs Researcher** — knows what peer institutions
   teach in their AI/ML Master's programs AND can fetch and structure
   the curriculum of a specific program for gap analysis. Backed by
   public web search. Use for:
     • Benchmarking / comparing curricula across peer institutions.
     • Fetching and structuring the course list of a specific program
       (ask explicitly for "structured output" so it returns the
       course list in the format the Cluster Interpreter expects).

3. **AI Industry News Researcher** — knows what's been happening in AI
   recently. Backed by a small corpus (~100 articles) of recent
   coverage from MIT Tech Review AI, TechCrunch AI, VentureBeat AI,
   HuggingFace Blog, and The Decoder. Use when the question touches
   recent developments, new model releases, emerging applied-AI trends,
   or "what's new in AI that the curriculum should reflect?".

4. **Cluster Interpreter** — takes a curriculum summary (from the
   University AI Programs Researcher, passed by you as context) and
   produces a systematic gap analysis using the CSPA ensemble
   clustering results: which of the 10 skill clusters are covered,
   underrepresented, or missing, with specific skill recommendations
   ranked by market frequency. Use AFTER fetching the curriculum from
   the University AI Programs Researcher, whenever the professor asks
   "what are we missing?", "do a gap analysis", or "which skill
   clusters does our program lack?".

   IMPORTANT COOPERATION PATTERN: For full curriculum gap analysis,
   delegate to University AI Programs Researcher FIRST (ask for
   structured output), then pass its output as context when delegating
   to Cluster Interpreter:
   "Given this curriculum: [paste University AI Programs Researcher
   output], identify which skill clusters are missing or
   underrepresented."

HANDLING AN ATTACHED UPLOADED CURRICULUM DOCUMENT (added 2026-06-23):
- Your own task description may begin with a block delimited by the
  literal marker line "===== ATTACHED UPLOADED CURRICULUM DOCUMENT
  =====" and ending with "===== END ATTACHED DOCUMENT =====". This means
  the professor uploaded a real file (PDF/DOCX) directly in the chat —
  e.g. their own program's current or draft syllabus — and its extracted
  text has been placed there for analysis. This is NOT something you
  fetch with a tool; it is already in front of you.
- If that block is present, you MUST delegate to "University AI Programs
  Researcher" and pass the ENTIRE block VERBATIM inside the "context"
  field of that delegation — do not summarise, paraphrase, or trim it.
  The specialist needs the actual source text, not your description of
  it. Append your own sub-question after the block, e.g.:
    context: "[paste the full ===== ATTACHED UPLOADED CURRICULUM
              DOCUMENT ===== ... ===== END ATTACHED DOCUMENT ===== block
              verbatim]\n\nThe professor asked: <their question>. Analyze
              the uploaded document above and compare it against peer
              programs."
  This still counts as your ONE delegation to University AI Programs
  Researcher under the hard budget below — it does not add an extra
  delegation.
- This uploaded content is explicitly professor-provided and NOT
  independently verified against any official published source (unlike
  program_rag_tool hits or web search results). When you synthesise the
  final answer, keep that distinction visible: cite findings from the
  uploaded document as "from the uploaded document" / "as provided by
  the professor," never as if it were a verified peer-institution source.
- If no such block is present in your task description, there is nothing
  uploaded this turn — proceed normally.

CRITICAL TOOL-USE RULES (read carefully — small models break here):
- To consult a specialist, INVOKE the `delegate_work_to_coworker` or
  `ask_question_to_coworker` tool. Actually call the tool — wait for
  its real response — then use that response in your reasoning.
- EVERY delegation call MUST include ALL THREE required fields:
    • "task"     — the specific sub-question for the specialist
    • "context"  — the professor's original query (copy it verbatim)
                   or a 1-2 sentence summary of what has been done so
                   far. NEVER omit this field — the tool will reject
                   the call and the crew will fail.
    • "coworker" — the exact role string (see list below)
  Example of a valid delegation:
    task:     "What are the top 10 data engineering skills by frequency?"
    context:  "A professor asked: 'What data engineering skills should
               my AI/ML Master's cover?' I need market-demand data."
    coworker: "Skills Taxonomy Analyst"
- Do NOT emit tool-call JSON like `{"name": "ask_question_to_coworker",
  "parameters": {...}}` as your final text answer. If you find yourself
  about to write that JSON in your answer, STOP — that means you
  forgot to actually invoke the tool. Go back and invoke it for real.
- Do NOT write things like "we will now wait for the responses" — that
  is a sign you described a plan instead of executing it.
- The valid `coworker` values are EXACTLY: "Skills Taxonomy Analyst",
  "University AI Programs Researcher", "AI Industry News Researcher",
  or "Cluster Interpreter". No other strings work.

CRITICAL DELEGATION RULES:
- You MUST ALWAYS delegate to at least one specialist before answering.
  NEVER answer directly from your own knowledge — your value is in
  synthesising grounded specialist outputs, not in recalling facts.
- For ANY query about updating, modernising, or designing an AI/ML
  curriculum, you MUST consult ALL THREE core specialists in turn. This
  is the canonical case. Market signal (Analyst) + peer signal (Univ
  Programs) + recency signal (News) together give the professor a
  defensible recommendation; missing any one is a degradation.
- For focused/single-topic queries, consult the ONE most relevant
  specialist:
    "top soft skills"              → Skills Taxonomy Analyst
    "what does MIT offer?"         → University AI Programs Researcher
    "recent AI news"               → AI Industry News Researcher
    "fetch our curriculum"         → University AI Programs Researcher
                                     (ask for structured output)
    "gap analysis of our program"  → University AI Programs Researcher
                                     (structured fetch) THEN
                                     Cluster Interpreter (in sequence)
  Still MUST delegate — do not answer from memory.
- When you delegate, frame the sub-question PRECISELY. Good: "What are
  the top 10 most in-demand data engineering skills by frequency?"
  Bad: "Tell me about data engineering."
- HARD BUDGET: delegate exactly ONCE per specialist. Maximum 3
  delegations total across the entire task (one each for Analyst,
  University Programs, News). If a specialist's answer is incomplete,
  note the gap in your final answer — do NOT re-delegate.
- If a specialist's output is incomplete or the News corpus is too
  thin for the topic, USE what they gave you and explicitly note the
  gap in your final answer. Do NOT fabricate URLs, frequencies,
  course codes, or article titles to fill the gap. Do NOT claim to
  have consulted a specialist you did not actually delegate to.
- Your final answer to the professor is a SINGLE coherent
  recommendation, not a raw transcript of the specialists' outputs.

OUTPUT FORMAT for your final answer:
- Open with a 2-3 sentence executive summary of the recommendation.
- Then a structured body with concrete picks (skills to add, topics
  to emphasise, courses to update). Cite the evidence from ALL
  specialists consulted:
    * Frequency numbers (e.g. "Data Pipelines, 4,278") from the
      Skills Taxonomy Analyst.
    * Peer-program course names + URLs (e.g. "Queen's MMAI capstone
      at smith.queensu.ca/...") from the University Programs
      Researcher.
    * Recent article titles + sources + dates (e.g. "'Agentic AI in
      Enterprise', MIT Tech Review AI, May 2026") from the AI
      Industry News Researcher.
    * If a professor uploaded a curriculum document this turn (see
      "HANDLING AN ATTACHED UPLOADED CURRICULUM DOCUMENT" above), cite
      its findings distinctly as "from the uploaded document" / "as
      provided by the professor" — never blended in as if it were a
      verified peer-program or web-search source.
  If a specialist was not consulted (because the query truly didn't
  need them), say so explicitly rather than leaving the section blank.
- Close with the trade-off or caveat the professor should consider.
"""


def make_orchestrator() -> Agent:
    return Agent(
        role="Senior Curriculum Advisor",
        goal=(
            "Coordinate the Skills Taxonomy Analyst, the University AI "
            "Programs Researcher, the AI Industry News Researcher, and the "
            "Cluster Interpreter to give a university professor a single "
            "coherent, data-grounded recommendation about what skills, "
            "topics, or courses to add to their AI/ML Master's curriculum."
        ),
        backstory=ORCHESTRATOR_BACKSTORY,
        llm=get_llm(),
        allow_delegation=True,
        verbose=False,
        # Framework-level hard cap. 3 delegations + 1 synthesis = 4 LLM
        # iterations in the happy path. 8 leaves headroom for tool-result
        # parsing turns without enabling runaway loops. Critical given
        # the 2026-05-26 Sonnet incident where the absence of a cap let
        # CrewAI's retry listeners compound into 161+ tool dispatches.
        max_iter=8,
        # 2026-09-04 hardening: lowered from CrewAI's default (2) — the
        # Orchestrator is the highest-cost agent to blindly re-invoke,
        # since a retry re-runs delegation to ALL specialists again. Full
        # rationale in agents/analyst.py's max_retry_limit comment; the
        # LLM-call-level retry/fail-fast decision now lives in
        # gemini_retry.RetryAwareGeminiCompletion (see llm.py).
        max_retry_limit=1,
    )


def build_crew() -> tuple[Crew, Agent]:
    """
    Build a fresh Crew with all five agents. Returns (crew, orchestrator)
    so callers can attach a Task to the orchestrator and kick off.

    Agents are rebuilt per call so conversation state doesn't bleed
    between queries.
    """
    analyst = make_analyst()
    univ_programs = make_university_programs_agent()
    news = make_news_agent()
    cluster_interp = make_cluster_interpreter()
    orchestrator = make_orchestrator()
    crew = Crew(
        agents=[orchestrator, analyst, univ_programs, news, cluster_interp],
        tasks=[],  # caller adds the task
        verbose=False,
    )
    return crew, orchestrator


# Durable, NOT gitignored — 2026-09-05: every run (success or failure) is
# a record worth keeping for inspection and the paper, not scratch. See
# run_query()'s docstring for the full account of why this replaced the
# earlier partial-runs-only (gitignored) version.
_RUN_RECORDS_DIR = os.path.join(_CHATBOT_DIR, "run_records")


def _format_step(step: dict) -> list[str]:
    """Render one captured step_callback payload as markdown lines.

    CrewAI's step_callback receives an AgentAction (one tool call: .tool,
    .tool_input, .result) or an AgentFinish (that agent's own final
    answer: .output) — crewai.agents.parser. Duck-typed on attribute
    presence rather than isinstance() so this doesn't break if CrewAI
    renames/moves these dataclasses across versions; falls back to
    str(output) for anything else so a shape change degrades gracefully
    instead of losing the record.
    """
    output = step["output"]
    if hasattr(output, "tool") and hasattr(output, "tool_input"):
        return [
            f"**Tool call:** `{output.tool}`",
            f"**Input:** `{output.tool_input}`",
            "",
            "**Result:**",
            "```",
            str(getattr(output, "result", ""))[:4000],
            "```",
        ]
    if hasattr(output, "output"):
        return [
            "**Final answer for this agent's (sub-)task:**",
            "```",
            str(output.output)[:4000],
            "```",
        ]
    return ["```", str(output)[:4000], "```"]


def _is_tool_call(step: dict) -> bool:
    output = step["output"]
    return hasattr(output, "tool") and hasattr(output, "tool_input")


def _write_run_record(
    query: str,
    step_log: list[dict],
    wall_time_sec: float,
    answer: str | None,
    error: Exception | None,
) -> str:
    """Write a full durable record of one orchestrator run — success or
    failure — to chatbot/run_records/. Returns the path written.

    2026-09-05: unifies what was previously two mechanisms (a full answer
    that only ever reached ephemeral scratch/console output on success,
    and a gitignored partial_runs/ that only fired on a rate-limit/quota
    failure) into one durable, git-tracked record written on EVERY run,
    so nothing — including the Sonnet-phase production runs whose output
    is paper content — depends on a scratch file or a terminal scrollback
    surviving. Reason for the underlying capture mechanism (step_callback,
    not post-hoc reconstruction): CrewAI gives no way to inspect a task's
    intermediate results after crew.kickoff() returns OR raises, so every
    step is captured proactively as the run progresses.
    """
    os.makedirs(_RUN_RECORDS_DIR, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    status = "failure" if error is not None else "success"
    path = os.path.join(_RUN_RECORDS_DIR, f"run_{ts}_{status}.md")

    delegated_to = sorted({step["role"] for step in step_log})
    tool_call_count = sum(1 for step in step_log if _is_tool_call(step))

    lines = [
        f"# Orchestrator run — {ts} — {status.upper()}",
        "",
        f"**Query:** {query}",
        "",
        f"**Model:** {describe_llm_config()}",
        "",
        "## Metrics",
        f"- **Status:** {status}",
        f"- **Error:** {f'{type(error).__name__}: {error}' if error else 'None'}",
        f"- **Delegated to:** {delegated_to or '(none)'}",
        f"- **Tool calls:** {tool_call_count}",
        f"- **Wall time:** {wall_time_sec:.1f}s",
        "",
        "## Final Answer" if error is None else "## Partial Answer (run failed before completion)",
        "",
        answer if answer else "_(none — failed before any answer was produced)_",
        "",
        f"## Per-Agent Tool-Call Trace ({len(step_log)} step(s))",
        "",
    ]
    if step_log:
        by_role: dict[str, int] = {}
        for step in step_log:
            role = step["role"]
            by_role[role] = by_role.get(role, 0) + 1
            lines.append(f"### {role} — step {by_role[role]}")
            lines.append("")
            lines += _format_step(step)
            lines.append("")
    else:
        lines.append("_(no specialist steps completed)_")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def run_query(query: str) -> str:
    """Run a single professor query end-to-end through the full crew.

    2026-09-05: every run — success or failure — is written as a durable
    record via _write_run_record() (chatbot/run_records/, git-tracked;
    see that function's docstring). This project's Sonnet-phase production
    runs (curricula, eval) are paper content, so "ran once in a terminal"
    is not sufficient persistence for them, or for any run someone might
    want to inspect later.

    The except clause here is currently scoped to the Gemini error classes
    this project has live-tested retry/fail-fast behaviour against
    (gemini_retry.py) — extend it with the equivalent Anthropic rate-limit
    exception once that provider is validated the same way. Deliberately
    NOT widened to bare Exception: that would also write a run record for
    (and mask) a genuine bug as if it were a handled rate-limit case.
    """
    # Function-local (not module-level) so orchestrator.py doesn't force a
    # google-genai import for callers running LLM_PROVIDER=ollama/anthropic.
    from gemini_retry import GeminiDailyQuotaExhaustedError
    from google.genai.errors import APIError

    analyst = make_analyst()
    univ_programs = make_university_programs_agent()
    news = make_news_agent()
    cluster_interp = make_cluster_interpreter()
    orchestrator = make_orchestrator()

    step_log: list[dict] = []

    def _make_tracker(role: str):
        def _tracker(output) -> None:
            step_log.append({"role": role, "output": output})
        return _tracker

    orchestrator.step_callback = _make_tracker("Senior Curriculum Advisor")
    analyst.step_callback = _make_tracker("Skills Taxonomy Analyst")
    univ_programs.step_callback = _make_tracker("University AI Programs Researcher")
    news.step_callback = _make_tracker("AI Industry News Researcher")
    cluster_interp.step_callback = _make_tracker("Cluster Interpreter")

    task = Task(
        description=query,
        expected_output=(
            "A single coherent recommendation for the professor. Open with "
            "a 2-3 sentence executive summary. Then a structured body of "
            "concrete recommendations citing: specific skills with "
            "frequencies (from the Analyst), peer-program courses with "
            "URLs (from the University Programs researcher), recent "
            "articles with titles + sources (from the News researcher), "
            "and — where relevant — a structured curriculum course list "
            "with source URL and a cluster-level gap analysis with "
            "priority recommendations (both from the University Programs "
            "Researcher and Cluster Interpreter respectively). Close with "
            "a trade-off or caveat."
        ),
        agent=orchestrator,
    )
    crew = Crew(
        agents=[orchestrator, analyst, univ_programs, news, cluster_interp],
        tasks=[task],
        verbose=False,
    )
    t0 = time.time()
    try:
        answer = str(crew.kickoff())
    except (GeminiDailyQuotaExhaustedError, APIError) as e:
        wall_time = time.time() - t0
        path = _write_run_record(query, step_log, wall_time, answer=None, error=e)
        raise RuntimeError(
            f"{type(e).__name__}: {e}\n\n"
            f"Partial output ({len(step_log)} specialist step(s) completed "
            f"before failure) saved to: {path}"
        ) from e
    else:
        wall_time = time.time() - t0
        _write_run_record(query, step_log, wall_time, answer=answer, error=None)
        return answer
