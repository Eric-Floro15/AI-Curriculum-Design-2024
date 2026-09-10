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
import re
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
    task:     "What skills are significantly co-demanded (lift + z) with
               data engineering, and which are the top attested (z>=2)
               picks for a curriculum?"
    context:  "A professor asked: 'What data engineering skills should
               my AI/ML Master's cover?' I need market-demand data,
               grounded in lift/significance, not raw frequency."
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
- When you delegate a curriculum-recommendation question to the Skills
  Taxonomy Analyst, frame it around LIFT/SIGNIFICANCE, not frequency —
  that's this project's grounding metric (what's distinctively
  co-demanded, not merely popular). Good: "What skills are significantly
  co-demanded (lift + z, z>=2) with data engineering?" Bad: "What are the
  top 10 most in-demand data engineering skills by frequency?" (frequency
  framing is fine for a pure scale question, e.g. "how many postings
  mention data engineering", just not for "what should we teach"). Also
  bad, for any specialist: "Tell me about data engineering" (too vague).
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

MANDATORY ROUTING RULES — added 2026-09-10 after a real incident: two
dev-lane dry runs under-delegated and the Senior Curriculum Advisor
gap-filled an entire peer-program section from nothing — one invented
9 Queen's/CMU course codes and 2 URLs, the other invented a full
6-peer-program comparison using SIX WRONG INSTITUTIONS (not even this
project's actual curated peer-program corpus) with neither University AI
Programs Researcher nor Cluster Interpreter ever consulted. These rules
are mandatory, not a preference — a deterministic code-level check also
enforces them independently of whether you follow this text (see
agents/orchestrator.py's `_detect_required_specialists()` and
`STRICT_DELEGATION` mode), so skipping the required delegation may cause
this run to hard-fail rather than silently return an unverified answer:
- If the query mentions peer programs, specific universities, courses,
  curricula, or "which programs teach/cover X" → you MUST delegate to
  the University AI Programs Researcher. Do NOT produce any
  peer-program, course-list, course-code, URL, or program-comparison
  content in your final answer unless that specialist was ACTUALLY
  consulted this run. If you cannot consult it (budget exhausted,
  tool failure), say so explicitly — "peer-program data unavailable
  this run" — rather than inventing course codes, URLs, or program
  names to fill the gap.
- If the query mentions clusters, gap analysis, "which clusters",
  "missing", "underrepresented", or coverage → you MUST delegate to
  the Cluster Interpreter (and to the Skills Taxonomy Analyst for any
  lift/z figures).
- Never attribute a section of your answer to a specialist that was
  not actually consulted this run. Never invent course codes, URLs,
  or program/institution names under any heading, labeled or not —
  fabrication doesn't require naming a specialist to still be
  fabrication.

ANTI-FABRICATION RULE — READ THIS BEFORE OUTPUT FORMAT BELOW, IT CONDITIONS
THE LIFT/SIGNIFICANCE PREFERENCE. This project had a real incident: a
gap-analysis run (Cluster Interpreter + University Programs only, Analyst
NOT delegated to) still produced a final answer with invented lift/z
numbers attributed to "the Skills Taxonomy Analyst" — because the OUTPUT
FORMAT rule below said to lead with lift/z, and no real lift/z existed
that run. That is fabrication in a deliverable and must never happen
again. Rules, no exceptions:
- You may state a numeric metric (lift, z, frequency, posting count,
  composed lift) ONLY if that EXACT value was returned by a tool call
  made by a specialist you ACTUALLY delegated to in THIS run. Never
  generate, estimate, interpolate, round to a "plausible" figure, recall
  a number from training data, or convert one metric into another (e.g.
  never invent a lift/z pair to accompany a frequency-only result, and
  never invent a frequency to accompany a lift-only result).
- The "prefer lift/z over frequency" instruction in OUTPUT FORMAT below
  applies ONLY when the Skills Taxonomy Analyst was actually delegated to
  AND returned lift/z values this run. If the Analyst did not run this
  turn (e.g. the gap-analysis routing above, which is Cluster Interpreter
  + University Programs only) and the only grounded metric you actually
  have is the Cluster Interpreter's market frequency, PRESENT THAT
  FREQUENCY, clearly labelled "(market frequency)" — do NOT manufacture
  lift/z just to match the preferred format. A correctly-labelled
  frequency number is honest; an invented lift/z pair is not, even if it
  "looks more rigorous."
- If a recommended skill has no tool-returned metric attached to it at
  all, present it as a qualitative gap/recommendation with no number,
  rather than inventing one to fill the space.
- Attribute every metric strictly to the specialist that actually
  produced it THIS run. Before writing a sentence like "identified by
  the Skills Taxonomy Analyst," check that the Skills Taxonomy Analyst
  is actually in your own delegation history this run — if it isn't,
  do not write that attribution, and do not write it for any other
  specialist you did not actually delegate to either.

OUTPUT FORMAT for your final answer:
- Open with a 2-3 sentence executive summary of the recommendation.
- Then a structured body with concrete picks (skills to add, topics
  to emphasise, courses to update). Cite the evidence from ALL
  specialists ACTUALLY consulted this run (see ANTI-FABRICATION RULE
  above — never cite a metric or attribution from a specialist you did
  not delegate to):
    * IF the Skills Taxonomy Analyst was delegated to and returned lift/
      significance data: Lift (×) and significance (z) from the Skills
      Taxonomy Analyst, e.g. "Large Language Models (lift 6.17×,
      z=9.56)" — this is the grounding metric: what's DISTINCTIVELY
      co-demanded, not merely popular. Raw frequency (e.g. "4,278
      postings") may appear as secondary scale/context but must never be
      the only number attached to a recommended skill, and never the
      stated reason a skill was picked. (Frequency alone is fine when
      the Analyst was answering a pure scale/inventory question rather
      than "what should we add".)
    * IF the Skills Taxonomy Analyst was NOT delegated to this run: do
      NOT include a lift/z line at all. Cite whatever grounded metric
      the specialists you DID consult actually returned instead — e.g.
      the Cluster Interpreter's market frequency, clearly labelled
      "(market frequency)" — and do not describe it as "lift" or
      "significance."
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
  need them), say so explicitly rather than leaving the section blank —
  and never manufacture the numbers that specialist would have provided.
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


def _truncate(text: str, max_chars: int | None) -> str:
    """`text`, capped at `max_chars` with a trailing note — or the
    complete, untouched `text` when `max_chars` is None. Centralises the
    truncation decision so the main record and the full-audit companion
    file (see _write_run_record()) differ only in what they pass here."""
    if max_chars is None or len(text) <= max_chars:
        return text
    return (
        text[:max_chars]
        + f"\n... [TRUNCATED — {len(text) - max_chars} more characters; "
        "see the companion _full.md file for the complete text]"
    )


def _format_step(step: dict, max_chars: int | None = 20_000) -> list[str]:
    """Render one captured step_callback payload as markdown lines.

    CrewAI's step_callback receives an AgentAction (one tool call: .tool,
    .tool_input, .result) or an AgentFinish (that agent's own final
    answer: .output) — crewai.agents.parser. Duck-typed on attribute
    presence rather than isinstance() so this doesn't break if CrewAI
    renames/moves these dataclasses across versions; falls back to
    str(output) for anything else so a shape change degrades gracefully
    instead of losing the record.

    2026-09-10 (GUARD_TUNEUP_sonnet.md Item 1): `max_chars` used to be a
    hardcoded 4000, unconditionally. Sonnet's specialist outputs run
    considerably longer than gpt-oss:120b's ever did, so real content —
    including the exact numbers several fabrication-guard flags pointed
    at — routinely fell past that cutoff in the SAVED record, making
    those flags impossible to audit from disk even though the live guard
    computed them against the true, complete text. Default raised to
    20,000 (generous headroom for a readable main record); pass
    max_chars=None (via _truncate above) to get the full, uncapped text
    for the companion audit file _write_run_record() now always writes
    alongside the main record.
    """
    output = step["output"]
    if hasattr(output, "tool") and hasattr(output, "tool_input"):
        return [
            f"**Tool call:** `{output.tool}`",
            f"**Input:** `{output.tool_input}`",
            "",
            "**Result:**",
            "```",
            _truncate(str(getattr(output, "result", "")), max_chars),
            "```",
        ]
    if hasattr(output, "output"):
        return [
            "**Final answer for this agent's (sub-)task:**",
            "```",
            _truncate(str(output.output), max_chars),
            "```",
        ]
    return ["```", _truncate(str(output), max_chars), "```"]


def _is_tool_call(step: dict) -> bool:
    output = step["output"]
    return hasattr(output, "tool") and hasattr(output, "tool_input")


# The four specialist role strings step_callback trackers are registered
# under in run_query() below — deliberately excludes "Senior Curriculum
# Advisor" (the Orchestrator itself; checking it against itself is
# meaningless). Kept as one list so a future 5th specialist only needs
# adding here, not in every call site.
_SPECIALIST_ROLES = [
    "Skills Taxonomy Analyst",
    "University AI Programs Researcher",
    "AI Industry News Researcher",
    "Cluster Interpreter",
]


def _build_consulted_text(step_log: list[dict], delegated_to: list[str]) -> str:
    """Concatenated text of every ACTUALLY-CONSULTED specialist's own
    captured output this run — the shared "ground truth" reference text
    every content-level guard (numeric, course-code, URL, institution)
    checks the Advisor's final answer against. Restricted to roles in
    _SPECIALIST_ROLES that are also in delegated_to (the Orchestrator's
    own steps are excluded: comparing the final answer against itself
    would be circular and prove nothing).

    2026-09-10: factored out of _detect_numeric_fabrication_flags (which
    used to build this inline) so the content-attribution guard added the
    same day can reuse the identical, already-validated technique rather
    than a second hand-rolled copy.
    """
    return "\n".join(
        str(getattr(step["output"], "output", ""))
        for step in step_log
        if step["role"] in _SPECIALIST_ROLES and step["role"] in delegated_to
    )


def _detect_fabrication_flags(answer: str, delegated_to: list[str]) -> list[str]:
    """Production attribution-level anti-fabrication guard.

    2026-09-09: generalises the "fabricated specialist attribution" check
    validated in agents/test_uploaded_curriculum.py's grade() (see that
    file's comment dated 2026-06-24) from a test-only assertion into a
    runtime scan on every real run_query() call. Motivated by a live
    incident the same day this was added: a gap-analysis run (Cluster
    Interpreter + Orchestrator only, delegated_to confirms neither
    University Programs nor News ran) still produced a final answer with
    a full "Recent Industry Signals (AI Industry News Researcher)"
    section of invented articles, and separately a fabricated Queen's
    MMAI course list attributed to a fetch that never happened — despite
    orchestrator.py's own backstory already explicitly forbidding this
    ("Do NOT claim to have consulted a specialist you did not actually
    delegate to"). A prompt-only rule was demonstrably insufficient, so
    this is a structural, code-level check on top of it.

    Deliberately FLAGS rather than strips or silently drops anything —
    per explicit instruction, the fabrication rate is itself data worth
    seeing and counting across run_records, not something to hide.

    Signal used: `delegated_to` (from step_callback, one tracker per
    agent, firing at least once whenever that agent is actually invoked
    this run) — NOT the per-tool-call trace. The tool-call trace is
    already known-unreliable in this CrewAI version (see _is_tool_call's
    callers / the "Tool calls" metric — it undercounts to ~0 because
    CrewAI's native-tool-calling flow doesn't invoke step_callback on
    intermediate AgentAction steps, only on each agent's terminal
    AgentFinish). delegated_to has no such gap: it's populated by that
    same terminal AgentFinish firing, which is exactly the "was this
    agent invoked at all this run" question this check needs answered,
    not "how many tool calls did it make."

    Unlike the test-only version this generalises, Cluster Interpreter
    IS included here — that test excluded it because its harness didn't
    trust delegated_to for it, but run_query() below registers a
    step_callback tracker for cluster_interp exactly the same way as the
    other three specialists, and this session's own live verification
    runs confirmed 'Cluster Interpreter' reliably appears in delegated_to
    when it actually runs. No reason to carve it out here.

    Only a name-string match — cannot verify individual facts/numbers
    within a section are correct, only whether the section's claimed
    source was actually consulted this run. See STEP 4 in the
    2026-09-09 conversation for the numeric/raw-output layers this does
    NOT cover.

    2026-09-10 (SONNET_delegation-check.md Step 1): a role mention is
    NOT flagged if it is HONEST DISCLOSURE — the answer saying the
    specialist "could not be reached" / "was not consulted" /
    "unavailable within the tool budget" — rather than presenting that
    specialist as an actual source of content. A real stage-2 run
    ("the University AI Programs Researcher could not retrieve
    structured course lists...") got flagged under the old rule purely
    for HONESTLY disclosing the gap — exactly the behavior
    orchestrator.py's own backstory asks for ("if you cannot consult it,
    say so explicitly") — which made a genuinely well-behaved answer
    look no different from a real fabrication in this guard's output.
    Checked per-occurrence via _is_exempt_mention() (honest disclosure OR
    capability-listing, see that function): a role is exempted only if
    EVERY mention of it in the answer is exempt-shaped; a role mentioned
    once as exempt and once as a real citation still flags, since that
    second mention is exactly the fabrication this guard exists to
    catch.
    """
    answer_lc = answer.lower()
    flags = []
    for role in _SPECIALIST_ROLES:
        if role.lower() in answer_lc and role not in delegated_to:
            if _is_exempt_mention(answer, role):
                continue
            flags.append(
                f"'{role}' is named/cited in the final answer but is NOT "
                f"in this run's delegated_to ({delegated_to or '(none)'}) "
                "— likely a fabricated citation, not a specialist actually "
                "consulted this run."
            )
    return flags


# Phrasing this project's own backstories/answers actually use to
# disclose that a specialist wasn't reached or wasn't needed (confirmed
# against real stage-2 AND sonnet run wording, not guessed) —
# deliberately not an exhaustive NLP-grade classifier, same "best-effort,
# low-noise" bias as the other guards' extraction.
#
# 2026-09-10 (GUARD_TUNEUP_sonnet.md Item 2): broadened from the
# SONNET_delegation-check.md Step 1 version, which only covered Ollama's
# "could not be reached/retrieve" style. Sonnet disclosed the SAME
# honest thing — a specialist wasn't consulted — using a DIFFERENT,
# equally honest vocabulary: proactive routing rationale ("...are not
# required this turn", "was not needed") rather than reactive failure
# language ("could not be reached"). Added "not required", "not needed",
# "isn't required", "wasn't needed", "not necessary", "was skipped" to
# cover this without assuming any one model's specific phrasing is the
# only honest way to say it.
_HONEST_DISCLOSURE_RE = re.compile(
    r"could not be reached|was not consulted|were not consulted"
    r"|not consulted|unavailable within the tool budget"
    r"|could not retrieve|couldn't retrieve|could not fetch"
    r"|not delegated|did not consult|wasn't consulted"
    r"|no\s+\S+\s+was\s+consulted"
    r"|not required|isn't required|wasn't required|was not required"
    r"|not needed|isn't needed|wasn't needed|was not needed"
    r"|not necessary|wasn't necessary|was not necessary"
    r"|was skipped|were skipped",
    re.IGNORECASE,
)

# 2026-09-10 (GUARD_TUNEUP_sonnet.md Item 2b): a DIFFERENT exemption
# shape than honest disclosure — the answer introducing/describing the
# SYSTEM'S OWN roster of specialists (e.g. a refusal's "My four
# specialists are: ...") rather than disclosing a gap in THIS run. Real
# example (Sonnet A5, a restaurant question correctly refused): "My four
# specialists are:\n- **Skills Taxonomy Analyst** – AI/ML job market
# skill demand\n- ..." — each bullet is its own newline-bounded
# "sentence" under _is_exempt_mention's sentence check, so the intro
# phrase sitting one line ABOVE never shares a sentence with the role
# name it introduces; a bare disclosure check alone still flagged all
# four. Checked with a wider, non-sentence-bounded LOOKBACK (see
# _CAPABILITY_LISTING_LOOKBACK_CHARS) specifically because a listing's
# intro phrase is structurally separated from each item it introduces,
# unlike a disclosure sentence, which contains the role name directly.
_CAPABILITY_LISTING_RE = re.compile(
    r"my\s+\w*\s*specialists?\s+(?:are|include)"
    r"|specialists?\s+(?:are|include)\s*:"
    r"|I\s+coordinate\s+(?:the\s+following\s+)?specialists?"
    r"|(?:the\s+)?following\s+specialists?",
    re.IGNORECASE,
)
_CAPABILITY_LISTING_LOOKBACK_CHARS = 400


def _is_exempt_mention(answer: str, role: str) -> bool:
    """True iff EVERY mention of `role` in `answer` is either (a) honest
    disclosure in its own sentence, or (b) part of a capability-listing
    block describing the system's own roster — i.e. never presented as
    an actual source of content. A role with zero mentions returns True
    (vacuous; callers already gate on the role appearing before calling
    this).

    (a) is bounded to the containing SENTENCE, not a fixed character
    window — a flat window (e.g. ±100/150 chars) can "bleed" disclosure
    language from an ADJACENT sentence into a nearby real citation's
    window. Caught via a unit test: "The <role> could not be reached
    this run. Still, per the <role>, Queen's MMAI offers MMAI-902..." —
    the second, real-citation mention's fixed window reached backward
    far enough to see the first sentence's "could not be reached" and
    was wrongly exempted. Sentence-bounding fixes this precisely because
    each mention is judged only by its own sentence.

    (b) deliberately uses a WIDER, non-sentence-bounded lookback instead
    — a capability-listing intro phrase sits in its OWN sentence/line,
    structurally separate from each specialist it introduces (see
    _CAPABILITY_LISTING_RE's docstring), so sentence-bounding (correct
    for (a)) would never find it for (b).
    """
    pattern = re.compile(re.escape(role), re.IGNORECASE)
    for m in pattern.finditer(answer):
        starts = [answer.rfind(c, 0, m.start()) for c in ".!?\n"]
        sentence_start = max(starts, default=-1) + 1
        ends = [p for p in (answer.find(c, m.end()) for c in ".!?\n") if p != -1]
        sentence_end = (min(ends) + 1) if ends else len(answer)
        sentence = answer[sentence_start:sentence_end]
        if _HONEST_DISCLOSURE_RE.search(sentence):
            continue
        lookback = answer[max(0, m.start() - _CAPABILITY_LISTING_LOOKBACK_CHARS): m.start()]
        if _CAPABILITY_LISTING_RE.search(lookback):
            continue
        return False
    return True


# --- Numeric grounding guard (2026-09-10) ---------------------------------
# Closes the gap the attribution guard above doesn't cover: a specialist
# that WAS actually delegated to, but whose lift/z/frequency numbers the
# Advisor altered or invented while writing the final synthesis (rather
# than fabricating an entire uninvoked section). Scope is deliberately
# narrow — market-statistic numbers only (lift, z, posting
# frequency/count) — NOT curriculum-design numbers (credits, weeks,
# course counts), which are the Advisor's own legitimate synthesis and
# would just be false-positive noise here.
#
# Each regex is anchored on a keyword (lift/z/freq/postings) or a
# domain-specific marker within a short window of the number, rather
# than scanning for bare digits — this is what keeps false-positive risk
# down for short numbers (a lone "9" or "5" is everywhere in normal
# prose; "z=9" or "9 postings" is not). One capture group per pattern.
#
# Lift specifically does NOT require the literal word "lift" adjacent to
# the number — tried that first, and it produced both false negatives
# and misleading context on a live run (2026-09-10, run_20260909T181136Z):
# markdown tables put "lift" only in the column header ("Composed lift
# (×) | Agentic lift (×) / z | ..."), 15+ chars away from each row's
# actual number ("22.39×"), so the keyword-adjacent version failed to
# extract real, correctly-cited table values from BOTH the answer and
# the grounding pool (same failure on both sides), producing spurious
# flags. Every real example seen this session — inline prose and table
# cells alike — writes lift as "<number><×-or-immediately-adjacent-x>"
# with nothing else in this project's domain using that notation, so a
# bare number immediately followed by × (or non-word-boundary-terminated
# "x") is itself a strong, low-noise signal here — no keyword needed.
_LIFT_NUM_RE = re.compile(r"(\d[\d,]*\.?\d*)\s?[×x](?!\w)", re.IGNORECASE)
# Separator after "z" is OPTIONAL — real observed output writes both
# "z=9.56" / "z = 9.2" AND bare "z 4.65" (no "=" at all, e.g. "AutoGen
# lift 12.6x, z 4.65" from a live run). \bz requires a word boundary
# before the z (so it won't match mid-word, e.g. the "z" in "size"),
# which is what keeps this safe to make the separator optional.
_Z_NUM_RE = re.compile(r"\bz\s*[=:]?\s*(-?\d[\d,]*\.?\d*)", re.IGNORECASE)
# "k" (thousands) suffix must be INSIDE the capture group — it needs to
# reach _normalize_market_num() so "56 k" -> 56000.0, not 56.0.
_FREQ_NUM_RE = re.compile(
    r"(?:freq(?:uency)?\s*[=:]\s*(\d[\d,]*\.?\d*\s*k?))"
    r"|(?:(\d[\d,]*\.?\d*\s*k?)\s*(?:postings?|job[- ]postings?))",
    re.IGNORECASE,
)
# Grounding-pool-only fallback: a markdown table cell containing NOTHING
# but a number (optionally bold-wrapped), e.g. "| 22.39 |" or "| **10.33** |".
# Added 2026-09-10 after a live false positive: a "Composed lift (×)"
# table column had the "×" only in the header, and each row's own cell
# was a bare number ("| AutoGen | 12.6 × | ... | 22.39 |") — the keyword/
# marker-anchored patterns above correctly extracted the adjacent-× cells
# in that same row (12.6×, 1.78×) but had nothing to anchor on for the
# bare 22.39 cell. Used ONLY when building the grounded pool from
# specialist text, never for extracting claims from the Advisor's answer
# — widening what counts as "grounded" can only reduce false positives,
# never cause new ones, whereas widening what counts as a "claim" in the
# answer would reintroduce exactly the noise the keyword anchoring exists
# to prevent.
#
# Trailing "|" is a lookahead, NOT consumed — adjacent cells in the same
# table row share a delimiter ("| 0.40 | 22.39 |"), and finditer's
# non-overlapping matches would otherwise consume the "|" between two
# numeric cells as part of the first match, leaving nothing to serve as
# the opening "|" for the next cell (found via a live false positive on
# the first version of this pattern: 8 of 9 real, correctly-grounded
# composed-lift values were still missed, all in rows with 2+ adjacent
# bare-number cells).
_TABLE_CELL_NUM_RE = re.compile(r"\|\s*\**\s*(-?\d[\d,]*\.?\d*)\s*\**\s*(?=\|)")

# kind -> (regex, group-indices to try in order, relative tolerance)
# Lift/z are floats copied verbatim from a frozen CSV — any deviation
# beyond formatting (e.g. "6.3" vs "6.30", which are equal once parsed)
# is suspicious, so tolerance is effectively zero. Frequency numbers are
# often summed/rounded by the Advisor from several real per-skill
# figures (e.g. "Total Frequency (sum of top-3 skills)" seen in a real
# run) or abbreviated with a "k" suffix — both legitimate arithmetic on
# real numbers, not fabrication — so frequency gets a wider relative
# tolerance to avoid flagging that as if it were invented.
_MARKET_NUM_KINDS = {
    "lift": (_LIFT_NUM_RE, [0], 1e-6),
    "z-score": (_Z_NUM_RE, [0], 1e-6),
    "frequency": (_FREQ_NUM_RE, [0, 1], 0.10),
}


def _normalize_market_num(raw: str) -> float:
    """'1,435' / '56k' / '6.30' -> float, tolerant of commas and a 'k'
    (thousands) suffix. Deliberately float-parse-and-compare rather than
    reusing eval/run_orchestrator_eval.py's _substring_match() (a plain
    comma-stripped substring check) — substring matching risks a short
    number wrongly matching inside a longer one (e.g. "1.5" as a
    substring of "21.5" or "1.56"); parsing to float and comparing
    numerically is the correct generalisation of the same
    comma-normalisation idea for this use case.
    """
    raw = raw.strip()
    is_k = raw.lower().endswith("k")
    if is_k:
        raw = raw[:-1]
    val = float(raw.replace(",", ""))
    return val * 1000 if is_k else val


def _extract_market_numbers(text: str) -> list[tuple[str, float, str, int, int]]:
    """Return [(raw_matched_number, normalized_float, kind, start, end), ...]
    for every lift/z/frequency number found in text, anchored on the
    keyword/marker regexes above. start/end are the character offsets of
    the CAPTURED NUMBER (not the whole match) within `text`, needed by
    callers that report an accurate context snippet — a plain
    `text.find(raw)` after the fact is wrong whenever the same short
    digit string (e.g. "18", "2") occurs earlier elsewhere in the text
    for an unrelated reason (a live run on 2026-09-10 hit exactly this:
    a flagged "'2'" reported context from an unrelated numbered list
    item, "(2) mirror the proven...", instead of the real match's
    location in a "lift ≈ 2×" phrase).

    Best-effort pattern matching, not a full parser — deliberately
    biased toward under-extraction (missing an oddly-formatted number)
    over over-extraction (flagging noise), consistent with "flag, don't
    strip": a missed number costs nothing here since this guard only
    warns, while a false extraction could produce a spurious flag.
    """
    found = []
    for kind, (pattern, group_idxs, _tol) in _MARKET_NUM_KINDS.items():
        for m in pattern.finditer(text):
            # Single-group patterns (lift, z) have group_idxs=[0] -> just
            # m.group(1). The two-alternative freq pattern has
            # group_idxs=[0, 1] -> try m.group(1) then m.group(2),
            # whichever of the two alternatives actually matched (the
            # other is None).
            for gi in group_idxs:
                raw = m.group(gi + 1)
                if raw is None:
                    continue
                try:
                    val = _normalize_market_num(raw)
                except ValueError:
                    continue
                found.append((raw, val, kind, m.start(gi + 1), m.end(gi + 1)))
    return found


def _detect_numeric_fabrication_flags(
    answer: str, step_log: list[dict], delegated_to: list[str]
) -> list[str]:
    """Numeric grounding guard: every market-statistic number (lift, z,
    frequency/posting count) in the final answer must appear in some
    ACTUALLY-CONSULTED specialist's own captured output this run — not
    just be attributed to a real specialist name (that's the attribution
    guard above), but be a real number that specialist's own text
    contains. Catches the Advisor altering or inventing a number inside
    a section it otherwise correctly attributes.

    Ground truth is each specialist's own AgentFinish text already
    captured in step_log (the same text rendered in the run record's
    "Per-Agent Tool-Call Trace" section) — restricted to roles in
    _SPECIALIST_ROLES that are actually in delegated_to this run (the
    Orchestrator's own steps are excluded: comparing the final answer
    against itself would be circular and prove nothing).

    Deliberately does NOT require the matched kind (lift vs z vs
    frequency) to line up between the answer and the specialist text
    beyond both being extracted by the same keyword-anchored patterns —
    the two-pass, keyword-anchored extraction on both sides is itself
    the false-positive control (see _extract_market_numbers), not an
    exact-kind cross-check.
    """
    if not step_log:
        return []
    grounded_text = _build_consulted_text(step_log, delegated_to)
    grounded_numbers: dict[str, list[float]] = {}
    for _raw, val, kind, _s, _e in _extract_market_numbers(grounded_text):
        grounded_numbers.setdefault(kind, []).append(val)
    # Fallback pool: bare numeric table cells (see _TABLE_CELL_NUM_RE) —
    # kind-agnostic since formatting alone can't tell us which kind a
    # bare cell represents, so it's checked against every kind bucket.
    bare_table_numbers = []
    for m in _TABLE_CELL_NUM_RE.finditer(grounded_text):
        try:
            bare_table_numbers.append(_normalize_market_num(m.group(1)))
        except ValueError:
            continue

    flags = []
    seen = set()  # avoid duplicate flags for the same raw number repeated in the answer
    for raw, val, kind, start, end in _extract_market_numbers(answer):
        if (raw, kind) in seen:
            continue
        # Exempt approximate/threshold phrasing ("lift ≈ 11–13×", "lift
        # ≥ 18×", "≈ 30× total"). Added 2026-09-10 after 4/4 of a live
        # finance rerun's remaining flags (post the extraction fixes
        # above) were all this exact shape — a legitimate qualitative
        # range/threshold the Advisor derived across several real
        # numbers, not a specific value copied from a tool. Checked only
        # against a short window immediately before the match (not the
        # whole answer) to avoid accidentally exempting an unrelated
        # later number that happens to follow one of these symbols
        # somewhere earlier in the text. The optional
        # "<number><dash>" tail handles a range's END number ("13" in
        # "≈ 11–13×") — the symbol precedes the range START, not the
        # matched number itself.
        preceding = answer[max(0, start - 25): start]
        if re.search(
            r"(?:[≈~≥≤><]|approx(?:imately)?|about|roughly)\s*"
            r"(?:\d[\d,]*\.?\d*\s*[-–—]\s*)?$",
            preceding,
            re.IGNORECASE,
        ):
            continue
        _pattern, _idxs, tol = _MARKET_NUM_KINDS[kind]
        pool = grounded_numbers.get(kind, []) + bare_table_numbers
        if any(abs(val - g) <= max(tol * abs(g), tol) for g in pool):
            continue
        seen.add((raw, kind))
        # Snippet built from this exact match's own position (start/end
        # from _extract_market_numbers), NOT answer.find(raw) — a plain
        # find() would grab the FIRST occurrence of the raw digit string
        # anywhere in the answer, which is wrong whenever that short
        # string also appears earlier for an unrelated reason (see
        # _extract_market_numbers' docstring for the live example this
        # fixed).
        snippet = answer[max(0, start - 30): end + 30].replace("\n", " ").strip()
        flags.append(
            f"{kind} value '{raw}' in the final answer does not match any "
            f"number in the consulted specialists' own captured output "
            f"this run — possibly invented or altered. Context: "
            f"\"...{snippet}...\""
        )
    return flags


# --- Content-attribution guard (2026-09-10) --------------------------------
# The attribution guard (_detect_fabrication_flags) only fires when a
# specialist ROLE NAME appears in the final answer but not in
# delegated_to. The numeric guard only fires on lift/z/frequency NUMBERS.
# Neither catches an under-delegated run where the Advisor gap-fills an
# entire peer-program section (course codes, URLs, institution names)
# under a neutral heading with no role name and no market-stat number —
# confirmed on two real Set A dry-run records: A1 (soft-skills) invented
# 9 Queen's/CMU course codes + 2 URLs with University AI Programs
# Researcher never delegated to; A4 (data-engineer clusters) invented a
# full 6-peer-program JSON structure (course codes, URLs, and — worse —
# the WRONG six programs entirely: Toronto/Edinburgh/Imperial/a generic
# MIT MicroMasters/CMU MS-ML/Stanford AI Certificate, none of which are
# this project's actual 6 curated peer programs) with NEITHER University
# AI Programs Researcher NOR Cluster Interpreter delegated to. This guard
# closes that gap with three checks, all using the same verbatim-trace
# technique as the numeric guard: is this specific claim actually present
# in _build_consulted_text()'s output, i.e. something a delegated
# specialist actually said this run?

# Allowlist of alpha-number tokens that look like course codes but
# aren't, checked case-insensitively before any code-shaped candidate is
# flagged.
_COURSE_CODE_ALLOWLIST = {
    "gpt-4", "gpt-4o", "gpt-5", "gpt4", "gpt4o", "gpt5",
    "llama", "claude", "3d", "s3", "ec2", "h100", "co2",
}

# Course-code candidates take two shapes in real output: an uppercase
# alpha prefix (2-5 letters) + a number that may carry dots/hyphens/a
# trailing letter ("MMAI-902", "CS330", "CS 224N", "PH 140.651",
# "CSC2515", "AI-301", "CSE 6242", "DATA 514"), OR a bare
# department-number.course-number pair with no alpha prefix at all
# ("11-651", "6.7960", "10-601", "15-619" — real MIT/CMU formats).
# Deliberately case-SENSITIVE (no IGNORECASE) on the alpha branch — real
# course codes in this project's output are always rendered uppercase;
# loosening this would start matching ordinary lowercase words that
# happen to end in digits.
#
# The dash class below is NOT just ASCII "-": this project's actual
# model output consistently renders what should be a plain ASCII hyphen
# as U+2011 (non-breaking hyphen) throughout — confirmed directly in a
# real Set A record ("MMAI\u2011902"), where an ASCII-only hyphen class
# silently missed every single course code with a hyphen separator.
# Covers the common Unicode dash variants a markdown-generating LLM
# might use: U+2010 hyphen, U+2011 non-breaking hyphen, U+2012 figure
# dash, U+2013 en dash, U+2014 em dash, plus the ASCII hyphen-minus.
# Built from explicit \uXXXX escapes (not raw pasted characters) so the
# intent is unambiguous in source, and the ASCII hyphen is escaped
# (`\-`) rather than merely repositioned — a raw "-" between two other
# class members is a RANGE in a character class, not a literal hyphen
# (e.g. "[ -\u2010]" silently matches almost the entire ASCII printable
# range, from space through U+2010 — caught this exact mistake in a
# throwaway smoke test before it shipped).
_DASH_CHARS = "\\-\u2010\u2011\u2012\u2013\u2014"
_COURSE_CODE_RE = re.compile(
    r"\b(?:[A-Z]{2,5}[ " + _DASH_CHARS + r"]?\d[\d." + _DASH_CHARS + r"]*[A-Z]?"
    r"|\d{1,2}[." + _DASH_CHARS + r"]\d{3,4}[A-Za-z]?)\b"
)

# 2026-09-10 (GUARD_TUNEUP_sonnet.md Item 3a): a report/publication
# citation shaped as "ACRONYM YEAR" — "WEF 2025", "Stanford HAI 2026",
# "McKinsey 2025" — structurally matches the alpha-prefix branch above
# (2-5 uppercase letters + a separator + digits) and got mis-flagged as
# unattributed_course_code on real Sonnet output ('WEF 2025', 'HAI
# 2026' x2 across the sonnet run records). A bare 4-digit number in the
# 1900s/2000s with NO other characters (no dot continuation, no
# trailing letter — the things a REAL course code almost always has,
# per this project's actual corpus: "6.7960", "CS 224N", "MMAI-902")
# is a year, not a course number; real course numbers in this domain
# don't happen to also look like a calendar year with nothing attached.
_REPORT_YEAR_CITATION_RE = re.compile(
    r"^[A-Z]{2,5}[ " + _DASH_CHARS + r"]?(?:19|20)\d{2}$"
)


def _is_report_year_citation(code: str) -> bool:
    return bool(_REPORT_YEAR_CITATION_RE.match(code))


# 2026-09-10 (GUARD_TUNEUP_sonnet.md Item 3b): real identifiers for this
# project's own curated peer programs (chatbot/data/program_and_
# curriculum/*.txt — confirmed by reading the actual files, not
# guessed) that happen to be short/numeric enough to structurally match
# _COURSE_CODE_RE's alpha-prefix branch. Currently just MIT's: the
# "6-4" track in "MEng in 6-4: Artificial Intelligence and Decision
# Making" is genuinely MIT's own program identifier (source:
# mit-eecs-meng-ai-decision-making.txt), and "MIT 6-4" got flagged as
# unattributed_course_code on real Sonnet output the same way "MIT
# 6.7960" (a real course WITHIN that program) did in an earlier Ollama
# batch — an institution name glued onto a genuinely real identifier,
# not a fabrication. The other 5 curated programs' short names (MSAII,
# MMAI, MMA, "MS CS") don't have a bare numeric-suffix form that
# _COURSE_CODE_RE would extract in the first place (no digit follows),
# so nothing to allowlist for them here — MMAI-902 (a fabricated COURSE
# within the real MMAI program) still correctly matches and flags.
_COURSE_CODE_ALLOWLIST.update({"mit 6-4", "6-4"})

# URLs: standard http(s) scheme, stop at whitespace or a markdown-link
# closing character.
_URL_RE = re.compile(r"https?://[^\s)\]}>\"'`|]+")


def _normalize_url(url: str) -> str:
    """Lowercase host, strip a trailing slash and trailing punctuation a
    sentence/markdown context tends to leave attached ('.', ',', ')',
    ']')."""
    url = url.rstrip(".,;:)]}>\"'")
    url = url.rstrip("/")
    m = re.match(r"(https?://)([^/]+)(.*)", url, re.IGNORECASE)
    if not m:
        return url.lower()
    scheme, host, rest = m.groups()
    return f"{scheme.lower()}{host.lower()}{rest}"


# This project's actual, human-curated peer-program corpus (see
# chatbot/data/program_and_curriculum/*.txt) plus common short aliases.
# Johns Hopkins is deliberately excluded from this always-recognized set
# — per the spec this guard implements, JHU is only "in scope" when the
# PROFESSOR'S OWN QUERY named it (handled in
# _detect_content_attribution_flags via the `query` argument), not
# whenever it happens to appear in an answer.
_RECOGNIZED_INSTITUTIONS = [
    "carnegie mellon", "cmu",
    "stanford",
    "mit", "massachusetts institute of technology",
    "georgia tech", "georgia institute of technology",
    "queen's", "queen's university", "queens university", "mmai",
]
# "University of Toronto" / "UofT" / "Rotman" deliberately NOT included
# here, even though UofT Rotman MMA is genuinely one of this project's
# 6 curated peer programs. "University of Toronto" is exactly the
# phrase _GENERIC_INSTITUTION_RE would independently extract from a
# "University of X" construction — pre-exempting it by literal string
# match would blind this check to EXACTLY the case a real Set A record
# exposed: A4 fabricated a "University of Toronto – MEng in Artificial
# Intelligence" program (not the real Rotman MMA) attributed to nothing
# delegated. A genuine Rotman mention, when the specialist actually said
# it, is still correctly exempted by the verbatim consulted_text check
# below — that check alone is sufficient and doesn't have this blind
# spot, so no separate pre-exemption is needed or wanted here.

# Light "University of X" / "X University" / "Y College (London)"
# matcher for institution names NOT in the recognized/curated list —
# this is what catches A4's fabricated Toronto/Edinburgh/Imperial
# mentions generically, without having to enumerate every possible
# fabricated institution name in advance.
# The negative lookaheads on the "X University" branch matter: without
# the first, a sentence like "The University of Cambridge also has..."
# gets mis-matched as just "The University" — "The" satisfies
# [A-Z][a-zA-Z]+ and is immediately followed by " University", so that
# alternative matches (and consumes) "The University" BEFORE the regex
# engine ever reaches the correct "University of Cambridge" starting
# position, since finditer takes the first alternative that matches at
# each position and "University" is now already consumed. It rejects
# "X University" whenever immediately followed by " of <Capitalized>" —
# in that shape the true institution name is "University of Y", not
# "<leading filler word> University" — found via a real unit-test
# failure, not just theorized.
#
# The second lookahead is a live Stage-2 finding, not a unit-test one:
# a real run's prose admitted "The University AI Programs Researcher
# could not be reached" (correctly disclosing the specialist was never
# delegated to) — but the SPECIALIST ROLE NAME itself starts with
# "University", so "The University" matched again, this time as a
# false institution candidate for a sentence that was actually about a
# role name, not a place. Rejects "X University" whenever immediately
# followed by " AI Programs Researcher" (the one role name this
# ambiguity can arise from — the other three role names in
# _SPECIALIST_ROLES don't start with "University").
_GENERIC_INSTITUTION_RE = re.compile(
    r"\b(?:University of [A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)?"
    r"|[A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)? University"
    r"(?!\s+of\s+[A-Z]|\s+AI\s+Programs\s+Researcher)"
    r"|Imperial College(?: London)?)\b"
)


def _detect_content_attribution_flags(
    answer: str, query: str, step_log: list[dict], delegated_to: list[str]
) -> list[str]:
    """Content-attribution guard: course codes, URLs, and institution
    names in the final answer must each trace verbatim to something a
    delegated specialist's own captured output actually said this run.

    Three checks (A1/A2/A3), each against the same `consulted_text`
    reference built the same way as the numeric guard's grounding pool.
    The verbatim-trace test is the primary false-positive control here,
    same as the numeric guard: anything a delegated specialist actually
    produced appears in consulted_text and is never flagged, regardless
    of how "suspicious" it might look in isolation.

    Deliberately does NOT try to detect whether a course code sits
    inside a fenced code block that's quoted verbatim from a specialist
    — if it's genuinely quoted from a specialist that ran, it's already
    in consulted_text and the verbatim check exempts it for free; if
    it's quoted-looking content from a specialist that did NOT run,
    that's exactly the fabrication this guard exists to catch, fenced or
    not, so no separate code-fence carve-out is needed or wanted.
    """
    if not answer:
        return []
    consulted_text = _build_consulted_text(step_log, delegated_to)
    consulted_lc = consulted_text.lower()
    flags: list[str] = []

    # A1 — course codes.
    seen_codes = set()
    for m in _COURSE_CODE_RE.finditer(answer):
        code = m.group(0)
        code_norm = re.sub(r"\s+", " ", code).strip().lower()
        if code_norm in _COURSE_CODE_ALLOWLIST or code_norm in seen_codes:
            continue
        if _is_report_year_citation(code):
            continue
        # Whitespace-normalized, case-insensitive verbatim check —
        # matches the spec's "appear verbatim (case-insensitive,
        # whitespace-normalized)" requirement exactly.
        if code_norm in consulted_lc:
            continue
        seen_codes.add(code_norm)
        idx = m.start()
        snippet = answer[max(0, idx - 30): idx + len(code) + 30].replace("\n", " ").strip()
        flags.append(
            f"unattributed_course_code: '{code}' in the final answer does "
            f"not appear in any delegated specialist's own captured "
            f"output this run — possibly a fabricated course code. "
            f"Context: \"...{snippet}...\""
        )

    # A2 — URLs.
    seen_urls = set()
    consulted_urls = {_normalize_url(u) for u in _URL_RE.findall(consulted_text)}
    for m in _URL_RE.finditer(answer):
        url = m.group(0)
        url_norm = _normalize_url(url)
        if url_norm in seen_urls or url_norm in consulted_urls:
            continue
        seen_urls.add(url_norm)
        idx = m.start()
        snippet = answer[max(0, idx - 30): idx + len(url) + 10].replace("\n", " ").strip()
        flags.append(
            f"unattributed_url: '{url}' in the final answer does not "
            f"appear (normalized) in any delegated specialist's own "
            f"captured output this run — possibly a fabricated URL. "
            f"Context: \"...{snippet}...\""
        )

    # A3 — institutions. Candidates come from two sources: the curated
    # recognized-institution aliases (substring match) and the generic
    # "University of X" / "X University" pattern (for names NOT in our
    # corpus — this is what catches a fabricated peer institution we've
    # never heard of).
    query_lc = (query or "").lower()
    recognized = set(_RECOGNIZED_INSTITUTIONS)

    # "johns hopkins"/"jhu" always searched for in the answer (not in
    # _RECOGNIZED_INSTITUTIONS, so not pre-exempted) — whether a mention
    # gets flagged depends on the per-candidate query-echo check below,
    # generalised from JHU specifically (per the spec: "Johns Hopkins,
    # only in scope when the query names it") to any institution.
    answer_lc = answer.lower()
    candidates: dict[str, tuple[int, int]] = {}
    for name in _RECOGNIZED_INSTITUTIONS + ["johns hopkins", "jhu"]:
        for m in re.finditer(r"\b" + re.escape(name) + r"\b", answer_lc):
            candidates.setdefault(name, m.span())
    for m in _GENERIC_INSTITUTION_RE.finditer(answer):
        name_norm = re.sub(r"\s+", " ", m.group(0)).strip().lower()
        candidates.setdefault(name_norm, m.span())

    seen_institutions = set()
    for name_norm, (start, end) in candidates.items():
        if name_norm in recognized or name_norm in seen_institutions:
            continue
        if name_norm in consulted_lc:
            continue
        # An institution the PROFESSOR'S OWN QUERY already named is not
        # suspicious merely for being echoed back — e.g. an off-scope
        # refusal that repeats "...restaurants near the University of
        # Toronto" from the query itself is not a fabricated
        # peer-program claim. Confirmed via a real Set A false positive
        # (A5, a pure refusal quoting the query's own institution
        # mention). Course codes and URLs attributed to that
        # institution are still independently checked by A1/A2
        # regardless of this exemption — this only covers the bare
        # institution-name-level flag.
        if name_norm in query_lc:
            continue
        seen_institutions.add(name_norm)
        snippet = answer[max(0, start - 30): end + 30].replace("\n", " ").strip()
        flags.append(
            f"unattributed_institution: '{answer[start:end]}' in the "
            f"final answer is not a recognized peer institution for "
            f"this project and does not appear in any delegated "
            f"specialist's own captured output this run — possibly a "
            f"fabricated institution. Context: \"...{snippet}...\""
        )

    return flags


# --- Delegation enforcement (2026-09-10, Part B) ----------------------------
# The three guards above are all post-hoc content checks — they catch a
# fabrication once it's already in the final answer. This is the
# structural backstop: detect from the QUERY ITSELF which specialists a
# defensible answer requires, independent of what the Advisor actually
# produced, and flag (or, in STRICT_DELEGATION mode, hard-fail) when a
# required specialist was never delegated to. Deterministic keyword
# matching, not LLM-dependent — this is meant to hold even when the
# backstory-level routing rules (see ORCHESTRATOR_BACKSTORY's MANDATORY
# ROUTING RULES section) get ignored by the model, which is exactly what
# happened on A1/A4.
_PEER_PROGRAM_INTENT_RE = re.compile(
    r"(?i:peer[ -]?program|which (?:program|university|universities)"
    r"|programs? (?:teach|cover|include|offer)|curricul(?:um|a)\b"
    r"|\bcourses?\b|\bteach(?:es)?\b|\boffers?\b|\bcompares?\b"
    r"|fetch (?:the|our|current) course)"
    # Degree-token alternatives are deliberately OUTSIDE the (?i:...)
    # scope, so they only match their real uppercase abbreviation form
    # ("MMAI", "MPH") — this keeps "MS" from also matching stray
    # lowercase "ms" occurrences case-insensitively.
    r"|\bMMAI\b|\bMSAII\b|\bMEng\b|\bMSc\b|\bMPH\b|\bMS\b"
)
_CLUSTER_GAP_INTENT_RE = re.compile(
    r"\bclusters?\b|gap analysis|which clusters|\bmissing\b"
    r"|underrepresented|under-represented|\bcoverage\b",
    re.IGNORECASE,
)


def _detect_required_specialists(query: str) -> set[str]:
    """Deterministic, keyword-based required-specialist detection from
    the query text alone. Two intents:
      - peer-program / course / curriculum COMPARISON intent ->
        University AI Programs Researcher must be delegated.
      - cluster / gap-analysis / coverage intent -> Cluster Interpreter
        must be delegated (a gap analysis is meaningless without it).

    2026-09-10 (Stage 2 refinement): this used to ALSO require the
    specialist whenever the query merely NAMED an institution (the
    recognized list, or the generic "University of X" pattern) with no
    other qualifying language — that was wrong. A real Set A5 query,
    "Can you tell me about the best restaurants near the University of
    Toronto?", named an institution but had zero program/comparison
    intent, and wrongly fired required_specialist_missing on a pure
    off-scope refusal. A3's JHU query ("...how it compares to AI/ML
    programs") is the correctly-required case, and the difference is
    INTENT, not the presence of a university/city name — so the
    bare-institution-name triggers were removed entirely; detection now
    relies solely on _PEER_PROGRAM_INTENT_RE, which already covers real
    peer-program queries via intent language (program/course/curriculum/
    teach/offer/compare) OR a degree-token mention (MMAI, MSAII, MEng,
    MSc, MPH, MS) — both of which co-occur with genuine peer-program
    asks without needing a separate institution-name check.

    Deliberately conservative/best-effort, not a full intent classifier
    — false negatives (missing a real peer-program ask) just mean this
    backstop doesn't fire for that query, same "flag less than you
    could" bias as the numeric guard's extraction. False positives here
    are low-cost: if the specialist WAS delegated to anyway (the common
    case for genuine peer-program queries), no flag is produced either
    way.
    """
    required: set[str] = set()
    if _PEER_PROGRAM_INTENT_RE.search(query):
        required.add("University AI Programs Researcher")
    if _CLUSTER_GAP_INTENT_RE.search(query):
        required.add("Cluster Interpreter")
    return required


def _strict_delegation_enabled() -> bool:
    """STRICT_DELEGATION mode (env var, default off): when a required
    specialist (per _detect_required_specialists) is missing from
    delegated_to, run_query() hard-fails instead of returning the
    at-risk answer as a deliverable. Default is FLAG-only (this stays
    off) so dev-lane exploration/debugging isn't interrupted — wire this
    on for the Sonnet-phase production/paper runs, where a fabricated
    answer must never silently become a deliverable.
    """
    return os.environ.get("STRICT_DELEGATION", "").strip().lower() in ("1", "true", "yes")


class RequiredSpecialistMissingError(RuntimeError):
    """Raised by run_query() in STRICT_DELEGATION mode when the query's
    detected intent required a specialist that was never actually
    delegated to this run (see _detect_required_specialists) — the
    crew's answer is at high risk of fabricated peer-program or cluster
    content and must not be handed to the caller as a deliverable."""


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
    required_specialists = _detect_required_specialists(query)
    required_missing = sorted(required_specialists - set(delegated_to))
    fabrication_flags = (
        (
            _detect_fabrication_flags(answer, delegated_to)
            + _detect_numeric_fabrication_flags(answer, step_log, delegated_to)
            + _detect_content_attribution_flags(answer, query, step_log, delegated_to)
        )
        if answer else []
    )

    lines = [
        f"# Orchestrator run — {ts} — {status.upper()}",
        "",
        f"**Query:** {query}",
        "",
        f"**Model:** {describe_llm_config()}",
        "",
        "## Metrics",
        # required_specialist_missing is placed first/at the top of
        # Metrics, ahead of even Status — this is the deterministic,
        # query-derived delegation-enforcement backstop (Part B2): it
        # doesn't depend on what the Advisor's answer says, only on
        # whether the query's detected intent (peer-program / cluster-gap)
        # was actually satisfied by a real delegation this run.
        f"- **required_specialist_missing:** {required_missing or '[]'}",
        f"- **Status:** {status}",
        f"- **Error:** {f'{type(error).__name__}: {error}' if error else 'None'}",
        f"- **Delegated to:** {delegated_to or '(none)'}",
        f"- **Tool calls:** {tool_call_count}",
        f"- **Wall time:** {wall_time_sec:.1f}s",
        f"- **fabrication_flags:** {fabrication_flags or '[]'}",
        "",
    ]
    if required_missing:
        lines += [
            "## 🚨 REQUIRED SPECIALIST NOT DELEGATED 🚨",
            "",
            "This query's detected intent (peer-program/course/curriculum, "
            "and/or cluster/gap-analysis — see `_detect_required_specialists()` "
            "in agents/orchestrator.py) required a specialist that was "
            "**never actually delegated to this run**. Any peer-program, "
            "course, URL, or cluster-gap content in the final answer below "
            "should be treated as HIGH fabrication risk regardless of "
            "whether the content-attribution guard also flagged it "
            "individually:",
            "",
        ]
        for role in required_missing:
            lines.append(f"- required_specialist_missing:{role}")
        lines.append("")
    if fabrication_flags:
        lines += [
            "## ⚠️⚠️⚠️ FABRICATION WARNING ⚠️⚠️⚠️",
            "",
            "One or more of this run's four content guards flagged the "
            "final answer: attribution (a specialist NAME cited but not "
            "in `delegated_to`, `_detect_fabrication_flags()`), numeric "
            "(a lift/z/frequency NUMBER absent from any consulted "
            "specialist's output, `_detect_numeric_fabrication_flags()`), "
            "and/or content-attribution (a course CODE, URL, or "
            "INSTITUTION absent from any consulted specialist's output, "
            "`_detect_content_attribution_flags()`) — all in "
            "agents/orchestrator.py. FLAG-don't-strip throughout: nothing "
            "below was removed, only flagged. Treat every number, URL, "
            "course, institution, or citation named in a flag below as "
            "UNVERIFIED for this run:",
            "",
        ]
        for flag in fabrication_flags:
            lines.append(f"- {flag}")
        lines.append("")
    full_path = path[:-len(".md")] + "_full.md"
    lines += [
        "## Final Answer" if error is None else "## Partial Answer (run failed before completion)",
        "",
        answer if answer else "_(none — failed before any answer was produced)_",
        "",
        f"## Per-Agent Tool-Call Trace ({len(step_log)} step(s))",
        "",
    ]
    if step_log:
        lines.append(
            f"Traces below are capped at 20,000 characters each for "
            f"readability — every guard flag above was computed against "
            f"the COMPLETE, uncapped text, which is always recoverable "
            f"from the companion file: `{os.path.basename(full_path)}`."
        )
        lines.append("")
    full_lines = list(lines)  # same header/metrics/answer, full-length traces below
    if step_log:
        by_role: dict[str, int] = {}
        for step in step_log:
            role = step["role"]
            by_role[role] = by_role.get(role, 0) + 1
            header = [f"### {role} — step {by_role[role]}", ""]
            lines += header + _format_step(step) + [""]
            full_lines += header + _format_step(step, max_chars=None) + [""]
    else:
        lines.append("_(no specialist steps completed)_")
        full_lines.append("_(no specialist steps completed)_")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    # 2026-09-10 (GUARD_TUNEUP_sonnet.md Item 1): companion file with the
    # COMPLETE, never-truncated text of every step, written for EVERY run
    # (not just long ones) so "is this run's trace long enough to need
    # the companion" is never a judgment call anyone has to make later —
    # it's just always there.
    with open(full_path, "w", encoding="utf-8") as f:
        f.write("\n".join(full_lines))
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
            "concrete recommendations. ANTI-FABRICATION (non-negotiable): "
            "every number you cite (lift, z, frequency, posting count) "
            "must be a value actually returned by a tool call from a "
            "specialist you actually delegated to this run — never "
            "invented, estimated, or converted from one metric to "
            "another, and never attributed to a specialist you did not "
            "delegate to. IF the Skills Taxonomy Analyst was delegated to "
            "and returned lift/significance data, cite specific skills "
            "with their lift (×) and significance (z) (from the Analyst) "
            "— the grounding metric for what to recommend (distinctively "
            "co-demanded, not merely popular); raw frequency may appear "
            "as secondary scale context but never as the sole justification "
            "for a recommended skill. IF the Analyst was NOT delegated to "
            "this run (e.g. a gap-analysis query routed only through the "
            "University Programs Researcher and Cluster Interpreter), do "
            "NOT include any lift/z figures — cite the Cluster "
            "Interpreter's market frequency instead, clearly labelled as "
            "frequency, not lift. Also cite: peer-program courses with "
            "URLs (from the University Programs researcher), recent "
            "articles with titles + sources (from the News researcher), "
            "and — where relevant — a structured curriculum course list "
            "with source URL and a cluster-level gap analysis with "
            "priority recommendations (both from the University Programs "
            "Researcher and Cluster Interpreter respectively). MANDATORY "
            "ROUTING (non-negotiable): if the query mentions peer "
            "programs, specific universities, courses, curricula, or "
            "which programs teach/cover something, you MUST delegate to "
            "the University AI Programs Researcher — do NOT produce any "
            "peer-program, course-list, course-code, URL, or "
            "program-comparison content unless that specialist was "
            "actually consulted this run; if you cannot consult it, say "
            "so explicitly instead of inventing course codes, URLs, or "
            "program names. If the query mentions clusters, gap "
            "analysis, which clusters, missing, underrepresented, or "
            "coverage, you MUST delegate to the Cluster Interpreter (and "
            "to the Skills Taxonomy Analyst for any lift/z). Close with "
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
        path = _write_run_record(query, step_log, wall_time, answer=answer, error=None)
        # STRICT_DELEGATION (Part B2 deterministic backstop, 2026-09-10):
        # the run record above is ALWAYS written first — even in strict
        # mode, the actual (at-risk) answer stays on disk for audit — but
        # the answer is withheld from the caller when the query's
        # detected intent required a specialist that was never actually
        # delegated to. Default off (see _strict_delegation_enabled());
        # wire it on for Sonnet-phase production/paper runs so a
        # fabricated peer-program/cluster answer can never silently
        # become a deliverable the way A1/A4 did on the dev lane.
        delegated_to = sorted({step["role"] for step in step_log})
        required_missing = sorted(_detect_required_specialists(query) - set(delegated_to))
        if required_missing and _strict_delegation_enabled():
            raise RequiredSpecialistMissingError(
                f"STRICT_DELEGATION is on and this query's detected intent "
                f"required {required_missing}, which was/were never "
                f"delegated to this run — refusing to return the answer "
                f"as a deliverable (high fabrication risk for peer-program "
                f"or cluster-gap content). The full run record, including "
                f"the actual (unverified) answer the crew produced, was "
                f"still saved for audit to: {path}"
            )
        return answer
