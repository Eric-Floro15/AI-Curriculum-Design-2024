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

import math
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

4. **Cluster Interpreter** — has TWO modes, use the right one for the
   query shape:

   MODE A (gap analysis, existing program) — takes a curriculum summary
   (from the University AI Programs Researcher, passed by you as
   context) and produces a systematic gap analysis using the CSPA
   ensemble clustering results: which of the 10 skill clusters are
   covered, underrepresented, or missing, with specific skill
   recommendations ranked by market frequency. Use AFTER fetching the
   curriculum from the University AI Programs Researcher, whenever the
   professor asks "what are we missing?", "do a gap analysis", or
   "which skill clusters does our program lack?" about a NAMED EXISTING
   program.

   MODE B (curriculum scaffold, from-scratch design) — takes NO
   existing-program input at all, and returns the cluster-backed
   STRUCTURE (theme + top demand skills per coherent cluster) to build a
   brand-new curriculum around. Use when the professor asks you to
   DESIGN/BUILD a curriculum FROM SCRATCH, grounded in market demand or
   demand clusters, with NO existing program named and NO comparison
   requested — see "FROM-SCRATCH CURRICULUM DESIGN COOPERATION PATTERN"
   below for the full routing rule. Do NOT fetch a curriculum from
   University AI Programs Researcher first for this mode — there is
   nothing to fetch, and doing so would wrongly turn a from-scratch
   design task into a peer-comparison task (that is a separate ask,
   see below).

   IMPORTANT COOPERATION PATTERN (MODE A, gap analysis — unchanged): For
   full curriculum gap analysis against an EXISTING named program,
   delegate to University AI Programs Researcher FIRST (ask for
   structured output), then pass its output as context when delegating
   to Cluster Interpreter:
   "Given this curriculum: [paste University AI Programs Researcher
   output], identify which skill clusters are missing or
   underrepresented."

   FROM-SCRATCH CURRICULUM DESIGN COOPERATION PATTERN (MODE B, new
   2026-09-24): When the professor asks you to design/build a curriculum
   FROM SCRATCH — grounded in market demand or demand clusters, naming
   NO existing program and requesting NO comparison — use this pattern
   instead of the canonical three-specialist pattern below:
     1. Delegate to Cluster Interpreter for the CLUSTER SCAFFOLD
        (structure) — Mode B, no existing curriculum passed as context.
     2. Delegate to Skills Taxonomy Analyst for lift/z on the scaffold's
        key skills (the evidentiary weight — frame the ask around what's
        DISTINCTIVELY demanded within each cluster's top skills, not raw
        frequency).
     3. Build ~8-10 courses CLUSTER-BY-CLUSTER: each course is grounded
        in one cluster (or a merged pair of closely-related clusters),
        titled and justified by that cluster's lift/z-attested skills.
   Do NOT delegate to University AI Programs Researcher for this
   pattern, and do NOT produce any peer-program, course-code, URL, or
   program-comparison content in the final answer — a from-scratch
   design is grounded in clusters + demand evidence only; peer
   benchmarking against an existing program is a categorically separate
   ask (Appendix G.3-style), not part of designing something new.
   AI Industry News Researcher is OPTIONAL here, for light recency
   rationale only — never fabricate a citation to fill it in if you
   skip it or its corpus is thin.

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

HANDLING A DATA WAVE OVERRIDE NOTICE (added 2026-09-25): Your own task
description may begin with a block delimited by the literal marker line
"===== DATA WAVE OVERRIDE NOTICE =====" and ending with "===== END DATA
WAVE OVERRIDE NOTICE =====". This means the underlying market data for
this run has been switched to a labour-market wave OTHER than your
backstory's default — the notice will name which one.
- If that block is present, you MUST relay it VERBATIM inside the
  "context" field whenever you delegate to Cluster Interpreter AND
  whenever you delegate to Skills Taxonomy Analyst this run (both read
  wave-specific data), in addition to your normal context for that
  delegation — do not summarise, paraphrase, or drop it. It still counts
  as your ONE delegation to each specialist under the hard budget below.
- The notice explicitly tells you to trust the LIVE tool output (cluster
  themes, focused-cluster markers, sizes, lift/z figures) over anything
  your own backstory says by default, including any specific wave/year
  your backstory names — a different wave's data can disagree with your
  backstory's usual description, and the live tool output is correct for
  THIS run, your backstory's default framing is not. Your own final
  synthesis must also describe the wave correctly (as the notice names
  it), not default to whatever wave your backstory normally assumes.
- If no such block is present in your task description, there is no
  override this turn — proceed normally, using your backstory's default
  framing exactly as before.

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
- For ANY query about updating, modernising, or improving an EXISTING
  AI/ML curriculum (the professor names or implies their own current
  program — "my curriculum," "our program," "should I add a module to
  my Master's"), you MUST consult ALL THREE core specialists in turn.
  This is the canonical case. Market signal (Analyst) + peer signal
  (Univ Programs) + recency signal (News) together give the professor a
  defensible recommendation; missing any one is a degradation.
- EXCEPTION — designing a curriculum FROM SCRATCH: if the professor
  instead asks you to design/build a NEW curriculum from nothing —
  grounded in market demand or demand clusters, naming NO existing
  program and requesting NO comparison — use the FROM-SCRATCH
  CURRICULUM DESIGN COOPERATION PATTERN under specialist 4 above
  (Cluster Interpreter for scaffold + Skills Taxonomy Analyst for
  lift/z; do NOT delegate to University AI Programs Researcher; News
  optional) instead of the three-specialist canonical case. The
  distinguishing signal is simple: is there an existing program to
  update/benchmark, or is this being built from nothing? If the
  professor's own query never references an existing program of theirs,
  treat it as from-scratch.
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
    "design a curriculum from      → Cluster Interpreter (scaffold) THEN
     scratch, grounded in demand"    Skills Taxonomy Analyst (lift/z) —
                                     see the FROM-SCRATCH pattern above,
                                     NOT University AI Programs Researcher
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
  the Cluster Interpreter (Mode A if an existing program is named for
  comparison, Mode B — the curriculum scaffold — if not) and to the
  Skills Taxonomy Analyst for any lift/z figures.
- FROM-SCRATCH DESIGN — a from-scratch curriculum query (design/build a
  NEW curriculum grounded in demand or demand clusters, no existing
  program named, no comparison requested) is a DIFFERENT case from the
  bullet above's gap-analysis case, even though both involve clusters:
  you MUST delegate to Cluster Interpreter (Mode B) AND Skills Taxonomy
  Analyst, and you must NOT delegate to University AI Programs
  Researcher for this query. Do NOT produce any peer-program,
  course-code, URL, or program-comparison content in your final answer
  for a from-scratch design — that specialist and that content belong
  to a categorically separate ask (benchmarking against an EXISTING
  named program, e.g. Appendix G.3-style), not to designing something
  new. If the professor's query never names or implies an existing
  program of their own, treat it as from-scratch.
- Never attribute a section of your answer to a specialist that was
  not actually consulted this run. Never invent course codes, URLs,
  or program/institution names under any heading, labeled or not —
  fabrication doesn't require naming a specialist to still be
  fabrication.
- TABLE-ROW ATTRIBUTION — a real incident this rule still allowed
  (2026-09-17, dev-lane run_20260917T224109Z, a from-scratch curriculum
  query): a "Specialist | Evidence Provided | How It Informs..." table
  named "University AI Programs Researcher" as the source of "structured
  course lists from five peer programs" with specific invented titles
  (Stanford, MIT, CMU, UW, Toronto) — even though `delegated_to` for
  that run confirms it was NEVER consulted. This slipped past because
  the bullets above describe prose attribution ("according to X", a
  "(Role)" heading) — a table row naming a non-delegated specialist as
  its subject is the SAME fabrication, just a different shape, and is
  just as forbidden:
    WRONG (fabrication): `| **University AI Programs Researcher** |
    Structured course lists from five peer programs... |` when that
    specialist never ran this turn.
    RIGHT (honest): either omit the row entirely, or write
    `| **University AI Programs Researcher** | ❌ Not consulted this
    run — no peer-program data available. |` — the same honest-absence
    disclosure this project already uses correctly elsewhere (see
    curriculum-fetch-mmai's own clean "❌ Not consulted" pattern).

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

    Only a pattern match — cannot verify individual facts/numbers within
    a section are correct, only whether the section's claimed source was
    actually consulted this run. See the numeric guard below for the
    layer that DOES check individual values.

    2026-09-10 (POLISH_attribution-flip_and_cost-tracking.md Item A):
    INVERTED from a blocklist-of-exemptions to a positive detector of
    the actual bad pattern. The exemption-based version (flag a
    non-delegated role's mention unless it matched a growing allowlist
    of honest-disclosure/capability-listing phrasings) was structural
    whack-a-mole: every richer Sonnet answer found a new BENIGN way to
    mention a non-delegated specialist that the allowlist hadn't
    anticipated yet — three real false-positive rounds in a row (Ollama
    "could not retrieve" style, Sonnet "not required this turn" style,
    Sonnet capability-listing refusals, and finally a hypothetical
    future-routing sentence on Run 1, d126756, that fit neither existing
    exemption). Chasing exemption phrasings is an unbounded problem;
    recognizing the actual fabrication SHAPE is bounded. Now flags a
    non-delegated role ONLY when the answer presents it as the SOURCE OF
    SPECIFIC CONTENT — a section header crediting it
    ("### Gap Analysis (Cluster Interpreter)", a "(Role)" tag on a
    heading, a bare "— Role" source line), or a citation verb
    ("According to <role>", "per the <role>", "<role> found/identified/
    reported/recommends/says/shows/...", "<role>'s analysis shows").
    A bare mention, an honest disclosure, a capability listing, or a
    hypothetical/conditional future-routing sentence naturally doesn't
    match any of these — no exemption list to maintain, because nothing
    about "not consulted" or "my four specialists are" or "I'll route it
    through X next time" ever looked like a citation to begin with.
    """
    flags = []
    for role in _SPECIALIST_ROLES:
        if role in delegated_to:
            continue
        m = _build_content_attribution_pattern(role).search(answer)
        if m:
            idx = m.start()
            snippet = answer[max(0, idx - 30): idx + len(m.group(0)) + 30].replace("\n", " ").strip()
            flags.append(
                f"'{role}' is presented as the source of specific content in "
                f"the final answer but is NOT in this run's delegated_to "
                f"({delegated_to or '(none)'}) — likely a fabricated "
                f"citation, not a specialist actually consulted this run. "
                f"Context: \"...{snippet}...\""
            )
        flags.extend(_detect_table_attribution_flags(answer, role, delegated_to))
    return flags


# 2026-09-19 (CLOSELOOP B1): a fourth attribution shape the checks above
# don't cover — a markdown TABLE ROW naming a non-delegated role as its
# subject, e.g. "| **University AI Programs Researcher** | Structured
# course lists from five peer programs... |". None of
# _build_content_attribution_pattern's three shapes match this: there's
# no "(Role)" heading, no dash-prefixed source line, and no citation verb
# immediately adjacent to the role name (the table's "Evidence Provided"
# wording lives in the HEADER row, not per-row next to the role). Real
# incident: run_20260917T224109Z (a from-scratch curriculum query, dev
# lane) — a "Specialist | Evidence Provided | How It Informs..." table
# credited University AI Programs Researcher with specific invented peer
# institutions (Stanford, MIT, CMU, UW, Toronto) despite `delegated_to`
# confirming it never ran that turn. 0 flags were raised at the time —
# this closes that gap.
#
# Deliberately NOT "any table row naming a non-delegated role" — this
# project already has a validated, honest pattern of a table row that
# names a non-delegated role specifically to disclose it wasn't
# consulted (e.g. curriculum-fetch-mmai's own clean "| Cluster
# Interpreter | ❌ Not consulted | No gap analysis was requested... |").
# Flagging that would reproduce the exact "exemption list is unbounded"
# trap _detect_fabrication_flags' own docstring already warns about, just
# inverted. So this checks the REST OF THAT SAME ROW for a negation/
# disclosure cue before flagging — mirrors the negation-aware design in
# eval/run_orchestrator_eval.py's _forbidden_match_is_disclaimer_only()
# (SUITE_step5), same principle applied to a different guard.
_TABLE_ATTRIBUTION_NEGATION_CUES = (
    "❌", "not consulted", "not delegated", "not requested",
    "no ", "n't ", "none", "unavailable", "was not", "were not",
)


def _build_table_role_cell_pattern(role: str) -> re.Pattern:
    """Matches the start of a markdown table row whose first cell is
    (optionally bold-wrapped) `role` — e.g. "| **Role** |" — capturing
    the rest of that line so the caller can check it for a negation cue
    before deciding whether this is a real attribution claim or an
    honest "not consulted" disclosure row.
    """
    r = re.escape(role)
    return re.compile(
        r"^[ \t]*\|[ \t]*\**" + r + r"\**[ \t]*\|(?P<rest>[^\n]*)$",
        re.IGNORECASE | re.MULTILINE,
    )


def _detect_table_attribution_flags(answer: str, role: str, delegated_to: list[str]) -> list[str]:
    """Table-row variant of the attribution check — see the module-level
    comment above `_TABLE_ATTRIBUTION_NEGATION_CUES` for the real
    incident this closes. Only called for roles already confirmed absent
    from `delegated_to` by the caller.
    """
    flags = []
    for m in _build_table_role_cell_pattern(role).finditer(answer):
        rest = m.group("rest").lower()
        if any(cue in rest for cue in _TABLE_ATTRIBUTION_NEGATION_CUES):
            continue  # honest disclosure row, not a claim
        idx = m.start()
        snippet = answer[max(0, idx - 10): idx + len(m.group(0)) + 60].replace("\n", " ").strip()
        flags.append(
            f"'{role}' appears as the subject of a table row presenting "
            f"specific content in the final answer but is NOT in this "
            f"run's delegated_to ({delegated_to or '(none)'}) — likely a "
            f"fabricated attribution table row, not a specialist actually "
            f"consulted this run. Context: \"...{snippet}...\""
        )
    return flags


# Verbs/phrases this project's own outputs actually use to CITE a
# specialist as the source of a specific claim (confirmed against real
# fabrication examples — the A2-style "Gap Analysis (Cluster
# Interpreter)" header and "According to <specialist>, <claim>" — not
# guessed). Deliberately the POSITIVE pattern the guard flags on, not a
# negative exemption list: see _detect_fabrication_flags' 2026-09-10
# docstring for why this direction is more robust.
_CONTENT_ATTRIBUTION_VERBS = (
    r"found|identified|reported|recommends?|recommended|says?|said"
    r"|shows?|showed|indicates?|indicated|notes?|noted|states?|stated"
    r"|confirms?|confirmed|reveals?|revealed|provides?|provided|returned"
)


def _build_content_attribution_pattern(role: str) -> re.Pattern:
    """A citation-shaped mention of `role`: a heading crediting it, a
    bare '— Role' source line, or a citing verb phrase. MULTILINE so the
    heading/source-line alternatives' ^/$ anchor to individual lines,
    not the whole answer.

    Reuses _DASH_CHARS (defined further down, safe to reference here —
    Python resolves module-level names at call time, not definition
    order) rather than a fresh hand-typed dash class: a raw "-" between
    two other class members is a RANGE, not a literal, and an early
    draft of this exact function had that bug (a coincidentally-correct
    one, since U+2010-U+2014 happens to be the same 5 dashes intended —
    still fixed before shipping, since correctness-by-coincidence isn't
    something to leave in the code once the actual mistake is spotted).
    """
    r = re.escape(role)
    return re.compile(
        r"^#{1,6}[^\n]*\(\s*" + r + r"\s*\)\s*$"            # "### ... (Role)"
        r"|^\s*[" + _DASH_CHARS + r"]\s*" + r + r"\s*[:.]?\s*$"  # bare "— Role" source line
        r"|\baccording to (?:the )?" + r + r"\b"
        r"|\bper (?:the )?" + r + r"\b"
        r"|\b" + r + r"'s\s+analysis\s+shows?\b"
        r"|\b" + r + r"(?:'s)?\s+(?:" + _CONTENT_ATTRIBUTION_VERBS + r")\b",
        re.IGNORECASE | re.MULTILINE,
    )


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
# 2026-09-25 (§5.1 F2022 PUSHTHROUGH, Part A2/A3): two real gaps found on a
# live gpt-oss:120b F2022 dev-lane run (run_20260925T164511Z):
#
# A2 — the model formatted its OWN specialist-trace frequency numbers with
# U+202F (narrow no-break space) as the thousands separator AND as the
# spacer around "=" — e.g. "freq = 2 387" for "freq = 2,387".
# The old digit class [\d,]* only recognises ASCII comma as a separator, so
# extraction from the GROUNDED side truncated at the first space ("2" instead
# of "2387"), corrupting the grounding pool and producing 8 false positives
# on genuinely-real, correctly-cited numbers (2,387 / 15,171 / 2,769 / 46 x2
# / 34 / the 1,600-7,500 range endpoints). Same precedent as _DASH_CHARS'
# Unicode-hyphen handling for course codes — a real, observed model habit,
# not a hypothetical. _THOUSANDS_SEP_CHARS below adds U+202F (narrow no-break
# space), U+00A0 (no-break space), U+2009 (thin space), and the ordinary
# ASCII space to the character class recognised INSIDE a digit run.
#
# A3 — the same run also produced a genuine, undetected fabrication:
# "Distributed Data Processing (frequency ≈ 800)" — invented, appears in
# neither specialist's real output — evaded this guard entirely because the
# old pattern only recognised "=" or ":" as the freq-value separator, not
# "≈" (approximately) or "~". Widened the separator class below to
# [=:≈~] so this exact shape is now extracted and checked like any other
# frequency claim. Deliberately NOT adding a bare, unanchored "≈N"/"~N"
# branch (no "freq"/"frequency" word required at all) — that would match any
# qualitative approximation in prose ("roughly 3 electives", "~10 weeks") far
# beyond frequency claims, a much larger false-positive surface than the
# "postings"-anchored branch already needs. The "postings"-anchored
# alternative below already catches "≈800 postings"-shaped claims
# unconditionally (it never cared what symbol preceded the digit run), so the
# only real gap was the freq(?:uency)-prefixed, no-"postings" shape — now
# closed without widening scope beyond the observed failure.
#
# Built from explicit \uXXXX escapes (not raw pasted characters) so the
# intent is unambiguous in source — same discipline as _DASH_CHARS above.
# ASCII comma, U+202F (narrow no-break space, the actual character gpt-oss
# used), U+00A0 (no-break space), U+2009 (thin space), ordinary ASCII space.
_THOUSANDS_SEP_CHARS = ',    '
# "k" (thousands) suffix must be INSIDE the capture group — it needs to
# reach _normalize_market_num() so "56 k" -> 56000.0, not 56.0.
_FREQ_NUM_RE = re.compile(
    r"(?:freq(?:uency)?\s*[=:≈~]\s*(\d[\d" + _THOUSANDS_SEP_CHARS + r"]*\.?\d*\s*k?))"
    r"|(?:(\d[\d" + _THOUSANDS_SEP_CHARS + r"]*\.?\d*\s*k?)\s*(?:postings?|job[- ]postings?))",
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


# --- Item A (GUARD_POLISH_batch, 2026-09-14): rounded prose ranges --------
# A summary sentence like "lift values ranging from 6x to 13x" paraphrases
# several real, individually-grounded numbers as a rounded span — a real
# run grounded at 6.17x/13.14x got flagged for the bare "6"/"13" since
# neither is an EXACT match to a grounded float. Detected as a distinct
# "A<sep>B" range construct (not a single specific claim), and exempted
# ONLY when each endpoint is a plausible rounding (floor or nearest-
# integer) of some real grounded lift — narrow enough that a fabricated
# range ("5x to 99x") still gets its bad endpoint flagged normally, since
# a single specific claim (not part of a recognised range) is untouched.
#
# 2026-09-17 (SUITE_step5, Item 3): the leading "[×x]" is now OPTIONAL —
# was previously required on BOTH endpoints ("A×–B×"), which missed the
# equally common single-trailing-symbol prose shape "A–B×" (one × after
# only the range's end, e.g. "12–13×"). Real false positive on a live
# paid-Sonnet run (SUITE_step4, 2026-09-17): "the highest in the dataset
# (12–13×)" summarizing three real, individually-cited values (LangGraph
# 12.25×, CrewAI 13.14×, AutoGen 12.60×) never matched the old regex at
# all, so its "13" endpoint fell straight through to the normal flag
# logic. Still safe to broaden: the groundedness check below
# (_range_endpoint_grounded against the real lift pool) is the actual
# false-positive control, not the regex shape — a fabricated range still
# needs a real grounded value near EACH endpoint to be exempted, so
# broadening what counts as "a range construct" can only ever let MORE
# genuinely-grounded prose through, never mask a fabrication.
_RANGE_LIFT_RE = re.compile(
    r"(\d[\d,]*\.?\d*)\s?[×x]?\s*(?:[" + "\\-\u2010\u2011\u2012\u2013\u2014" + r"]|to)\s*"
    r"(\d[\d,]*\.?\d*)\s?[×x](?!\w)",
    re.IGNORECASE,
)


def _range_endpoint_grounded(val: float, pool: list[float]) -> bool:
    """True if `val` is a plausible rounding (floor or nearest-integer) of
    some grounded value in `pool` -- e.g. val=6 grounded by a real 6.17 or
    6.63 (both floor to 6); val=13 grounded by a real 13.11 or 13.14
    (both floor to 13). Deliberately NOT a wide/fuzzy tolerance: a
    fabricated endpoint (e.g. 99) needs an actual grounded value in the
    ~[99, 100) window to pass, which real market data won't coincidentally
    provide."""
    return any(math.floor(g) == val or round(g) == val for g in pool)


def _normalize_market_num(raw: str) -> float:
    """'1,435' / '2 387' / '56k' / '6.30' -> float, tolerant of ASCII
    comma, the Unicode thousands-separator whitespace variants in
    _THOUSANDS_SEP_CHARS (2026-09-25, A2), and a 'k' (thousands) suffix.
    Deliberately float-parse-and-compare rather than reusing
    eval/run_orchestrator_eval.py's _substring_match() (a plain
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
    for sep in _THOUSANDS_SEP_CHARS:
        raw = raw.replace(sep, "")
    val = float(raw)
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

    # Item A range-summary exemption: identify "A<sep>B" range constructs
    # in the answer whose BOTH endpoints are a plausible rounding of a
    # real grounded lift value, and record their exact (start, end)
    # spans so the per-number loop below skips them without loosening
    # the check for any other (non-range, specific) claim.
    range_exempt_spans: set[tuple[int, int]] = set()
    lift_pool = grounded_numbers.get("lift", []) + bare_table_numbers
    for rm in _RANGE_LIFT_RE.finditer(answer):
        try:
            v1 = _normalize_market_num(rm.group(1))
            v2 = _normalize_market_num(rm.group(2))
        except ValueError:
            continue
        if _range_endpoint_grounded(v1, lift_pool) and _range_endpoint_grounded(v2, lift_pool):
            range_exempt_spans.add((rm.start(1), rm.end(1)))
            range_exempt_spans.add((rm.start(2), rm.end(2)))

    flags = []
    seen = set()  # avoid duplicate flags for the same raw number repeated in the answer
    for raw, val, kind, start, end in _extract_market_numbers(answer):
        if (raw, kind) in seen:
            continue
        if kind == "lift" and (start, end) in range_exempt_spans:
            continue
        # Exempt approximate/threshold phrasing ("lift ≈ 11–13×", "lift
        # ≥ 18×", "≈ 30× total", "over 20×", "more than 9×"). Added
        # 2026-09-10 after 4/4 of a live finance rerun's remaining flags
        # (post the extraction fixes above) were all this exact shape —
        # a legitimate qualitative range/threshold the Advisor derived
        # across several real numbers, not a specific value copied from
        # a tool. Checked only against a short window immediately before
        # the match (not the whole answer) to avoid accidentally
        # exempting an unrelated later number that happens to follow one
        # of these symbols somewhere earlier in the text. The optional
        # "<number><dash>" tail handles a range's END number ("13" in
        # "≈ 11–13×") — the symbol precedes the range START, not the
        # matched number itself.
        #
        # 2026-09-17 (SUITE_step5, Item 3): TIGHTENED from an
        # unconditional skip to a groundedness-gated one, and the
        # qualifier list widened to cover "over"/"more than"/"greater
        # than"/"upwards of"/"in excess of"/"up to"/"at least" — the
        # original 2026-09-10 version trusted ANY number preceded by one
        # of the (narrower) qualifier words, with no check that the
        # value was actually grounded in anything. Real false positives
        # on a live paid-Sonnet run (SUITE_step4, 2026-09-17): "over 20×"
        # for a real, grounded 20.14× (Jax->Pytorch) and "over 9×" for a
        # real, grounded 9.03× (Mlops->Responsible Ai) both got flagged,
        # since "over" wasn't in the old qualifier list at all. Reusing
        # _range_endpoint_grounded (the same floor/nearest-integer test
        # Item A already uses for range endpoints) instead of a blanket
        # trust keeps the still-catches guarantee: a genuinely fabricated
        # threshold ("over 90×" with nothing near it) has no grounded
        # value that floors/rounds to 90, so it still falls through to
        # the normal flag logic below.
        preceding = answer[max(0, start - 25): start]
        if re.search(
            r"(?:[≈~≥≤><]|approx(?:imately)?|about|roughly|over|"
            r"more\s+than|greater\s+than|upwards?\s+of|in\s+excess\s+of|"
            r"up\s+to|at\s+least)\s*"
            r"(?:\d[\d,]*\.?\d*\s*[-–—]\s*)?$",
            preceding,
            re.IGNORECASE,
        ):
            pool_for_kind = grounded_numbers.get(kind, []) + bare_table_numbers
            if _range_endpoint_grounded(val, pool_for_kind):
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
# Item D (GUARD_POLISH_batch, 2026-09-14): domain-standard tokens that
# structurally match the course-code shape (alpha prefix + digits) but
# are medical/health-IT standards, not course codes -- confirmed real
# false positives on a live healthcare Sonnet run ('ICD-10', 'HL7').
# FHIR/SNOMED/SNOMED CT/LOINC/UMLS don't contain a digit so _COURSE_CODE_RE
# can't currently match them at all, but they're listed anyway per spec
# and as a defensive no-op if the detector's shape ever changes.
_COURSE_CODE_ALLOWLIST.update({
    "icd-10", "hl7", "fhir", "snomed", "snomed ct", "loinc", "umls", "dsm-5",
})

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

# 2026-09-17 (SUITE_step5, Item 3): a bare "N-NNN" frequency-count range
# ("80-190 postings") structurally matches the bare-digit-pair course-
# code shape _COURSE_CODE_RE's second alternative also recognizes (real
# MIT/CMU codes like "10-601", "15-619"). Real false positive on a live
# paid-Sonnet run (SUITE_step4, 2026-09-17): "~80–190 postings" —
# CrewAI/LangGraph/AutoGen's individually-grounded 91/183/82 posting
# counts summarized as a rounded range — got flagged as
# unattributed_course_code. Narrow, context-gated exemption below: only
# a code with NO alphabetic characters at all (real course codes always
# have a subject prefix or trailing letter; this branch's shape never
# does) AND immediately followed by "posting(s)" is treated as a
# frequency range, not a course code — a fabricated course-code-shaped
# string is never immediately followed by "posting(s)" in this project's
# real output, so this can't mask a genuine fabrication.
_POSTINGS_CONTEXT_RE = re.compile(r"^\s*(?:job\s+)?postings?\b", re.IGNORECASE)

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


def _strip_institution_code_prefix(code_norm: str) -> str | None:
    """Item C (GUARD_POLISH_batch, 2026-09-14): a real course code
    prefixed with its institution abbreviation ("CMU 17-762") is matched
    by _COURSE_CODE_RE as one token, but a specialist's own trace usually
    states the bare code alone ("17-762") without the institution glued
    on -- confirmed a real false positive on a live healthcare Sonnet run
    ('CMU 17-762', 'CMU 16-725', both genuinely present in the trace as
    bare codes). Strips a single leading alpha token (2-6 letters,
    optionally possessive, e.g. "queen's") followed by whitespace,
    returning the remainder -- or None if the code has no such
    leading-token-then-space shape (a glued form like "cs330" is
    untouched; stripping there would strip the course subject itself,
    not an institution prefix). The caller still requires the STRIPPED
    remainder to independently appear in the trace, so this can only add
    exemptions for codes that are genuinely grounded once the prefix is
    removed -- never mask a code that's fabricated outright.
    """
    m = re.match(r"^[a-z]{2,6}(?:'s)?\s+(.+)$", code_norm)
    return m.group(1) if m else None


def _normalize_institution_text(s: str) -> str:
    """Item B (GUARD_POLISH_batch, 2026-09-14): case/punctuation/
    whitespace-insensitive normalization for institution-name matching --
    collapses dash variants and other punctuation to spaces and collapses
    whitespace runs, so a candidate like "University of Toronto Rotman"
    matches a trace phrased "University of Toronto — Rotman School of
    Management" (dash-separated, not concatenated) -- confirmed a real
    false positive on a live finance Sonnet run. An institution genuinely
    absent from every trace (e.g. a fabricated "University of
    Fabricationland") still has no normalized substring to match, so it
    stays flagged.
    """
    s = s.lower()
    s = re.sub(r"[" + _DASH_CHARS + r",.;:()\[\]]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


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
    consulted_inst_norm = _normalize_institution_text(consulted_text)
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
        # Item C: an institution-prefixed code ("cmu 17-762") whose bare
        # remainder ("17-762") is independently grounded in the trace.
        stripped = _strip_institution_code_prefix(code_norm)
        if stripped and stripped in consulted_lc:
            continue
        # SUITE_step5 Item 3: a bare digit-pair immediately followed by
        # "posting(s)" is a frequency range, not a course code — see
        # _POSTINGS_CONTEXT_RE's module-level comment for the real false
        # positive this fixes.
        if not any(c.isalpha() for c in code) and _POSTINGS_CONTEXT_RE.match(
            answer[m.end(): m.end() + 20]
        ):
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
        # Item B: normalized (punctuation/whitespace-insensitive) match —
        # "university of toronto rotman" against a trace phrased
        # "university of toronto — rotman school of management".
        if _normalize_institution_text(name_norm) in consulted_inst_norm:
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


# --- Delegation-claim honesty guard (Item E, GUARD_POLISH_batch, 2026-09-14) -
# The attribution guard above catches a non-delegated role being credited
# as the SOURCE OF SPECIFIC CONTENT. This is a narrower, distinct claim:
# the final answer asserting the DELEGATION PROCESS ITSELF happened for a
# role it didn't — "the University AI Programs Researcher was consulted"
# — even without attaching any specific content to it. Confirmed a real
# false claim on a live healthcare dev-lane run (RUN2C): delegated_to
# excluded University AI Programs Researcher, but the answer's own caveat
# said it "was consulted... but no verified peer-program data was
# returned." Modelled the same way the attribution guard was inverted
# (2026-09-10): a POSITIVE detector of the bad pattern (an affirmative,
# past-tense consultation claim naming a non-delegated role), not an
# exemption-allowlist of "polite ways to say no" that would whack-a-mole
# on new honest-disclosure phrasings. Structurally safe against the
# required negative cases without needing to enumerate them: "was NOT
# consulted" / "wasn't needed" share the same verb as the affirmative
# form but differ by a negation word directly after the auxiliary (the
# lookahead below rejects that); "could not be reached" / "unavailable"
# use no monitored verb at all; a conditional future routing sentence
# ("if you provide..., I'll route it through <role>") uses present/future
# tense ("route"), not the past-tense "routed" this guard looks for.
_DELEGATION_CLAIM_VERBS_PASSIVE = r"consulted|used|engaged|utilized|leveraged"
_DELEGATION_CLAIM_VERBS_ACTIVE = r"provided|returned|confirmed"


def _build_delegation_claim_pattern(role: str) -> re.Pattern:
    r = re.escape(role)
    return re.compile(
        # "<role> was/is/has been [not] consulted/used/engaged/..." —
        # only matches when NOT negated directly after the auxiliary.
        r"\b" + r + r"\s+(?:was|were|is|are|has been|have been)\s+"
        r"(?!(?:not|n't|never)\b)(?:actually\s+)?"
        r"(?:" + _DELEGATION_CLAIM_VERBS_PASSIVE + r")\b"
        # "we consulted/used/engaged <role>"
        r"|\bwe\s+(?:actually\s+)?(?:" + _DELEGATION_CLAIM_VERBS_PASSIVE + r")\s+"
        r"(?:the\s+)?" + r + r"\b"
        # "routed (it/this/that) to/through <role>" — PAST TENSE only, so
        # a future/conditional "I'll route it through <role>" doesn't
        # match this shape at all.
        r"|\brouted\s+(?:it|this|that\s+)?\s*(?:to|through)\s+(?:the\s+)?" + r + r"\b"
        # "drew on <role>"
        r"|\bdrew on\s+(?:the\s+)?" + r + r"\b"
        # "<role> provided/returned/confirmed" — active voice, role as
        # grammatical subject; a negated form ("did not provide") uses a
        # different verb form and doesn't match this shape.
        r"|\b" + r + r"(?:'s)?\s+(?:" + _DELEGATION_CLAIM_VERBS_ACTIVE + r")\b",
        re.IGNORECASE,
    )


def _detect_delegation_claim_flags(answer: str, delegated_to: list[str]) -> list[str]:
    """For any specialist absent from `delegated_to`, flag an affirmative
    past-tense claim that it WAS consulted/used/engaged this run — a
    false claim about the delegation PROCESS, distinct from the
    attribution guard's content-sourcing check above. See the module
    comment immediately above for the full design rationale and the
    negative-case safety argument (why honest disclosure and conditional
    future-routing sentences structurally don't match).
    """
    flags = []
    for role in _SPECIALIST_ROLES:
        if role in delegated_to:
            continue
        m = _build_delegation_claim_pattern(role).search(answer)
        if not m:
            continue
        idx = m.start()
        snippet = answer[max(0, idx - 30): idx + len(m.group(0)) + 30].replace("\n", " ").strip()
        flags.append(
            f"delegation_claim: '{role}' is affirmatively claimed as "
            f"consulted/used in the final answer but is NOT in this run's "
            f"delegated_to ({delegated_to or '(none)'}) — a false claim "
            f"about the delegation process itself. Context: "
            f"\"...{snippet}...\""
        )
    return flags


# --- Delegation enforcement (2026-09-10, Part B) ----------------------------
# The four guards above are all post-hoc content checks — they catch a
# fabrication once it's already in the final answer. This is the
# structural backstop: detect from the QUERY ITSELF which specialists a
# defensible answer requires, independent of what the Advisor actually
# produced, and flag (or, in STRICT_DELEGATION mode, hard-fail) when a
# required specialist was never delegated to. Deterministic keyword
# matching, not LLM-dependent — this is meant to hold even when the
# backstory-level routing rules (see ORCHESTRATOR_BACKSTORY's MANDATORY
# ROUTING RULES section) get ignored by the model, which is exactly what
# happened on A1/A4.
# 2026-09-24 (CLOSELOOP B1, attempt C): narrowed from a version that
# also fired on bare "curriculum"/"course"/"teach"/"offers" anywhere in
# the query. That over-broad version made EVERY curriculum-shaped
# query — including a from-scratch "design a curriculum grounded in
# demand" ask with no existing program to compare against — require
# University AI Programs Researcher, exactly backwards for Appendix
# G.2 (a from-scratch curriculum needs Cluster Interpreter + demand
# frequency, NOT peer-program benchmarking; that's a different task,
# G.3's Queen's-MMAI-style comparison). Confirmed via
# chatbot/eval/orchestrator_queries.yaml + agents/test_fabrication_
# guards.py's existing B2 test block: every case that must still
# require this specialist does so via one of the signals kept below
# (a bare "program(s)" mention, explicit peer language, "compare",
# a possessive "my/our program/curriculum" — i.e. an EXISTING program
# reference — a degree token, or a named-institution "fetch the
# course(s)" ask) — none relied on the bare curriculum/course/teach/
# offer alternatives being removed. The natural G.2 query ("design a
# graduate AI/ML curriculum... For each course...") deliberately never
# says "program", "my", "our", "peer", or "compare" — it survives this
# narrowing exactly because it has no existing-program reference to
# trigger on, which is the whole point of the distinction.
_PEER_PROGRAM_INTENT_RE = re.compile(
    r"(?i:peer[ -]?(?:program|institution)s?"
    r"|which (?:program|university|universities)"
    r"|\bprograms?\b|\bcompares?\b"
    # Possessive existing-program reference — "my AI/ML Master's
    # curriculum", "our program" — the signal that distinguishes
    # "improve/benchmark an EXISTING program" (needs peer context)
    # from "design A curriculum" (does not). Bounded to 40 chars and
    # excluded from crossing a sentence boundary so it can't reach
    # into unrelated later text.
    r"|\bmy\b[^.?!]{0,40}?\b(?:program|curriculum)\b"
    r"|\bour\b[^.?!]{0,40}?\b(?:program|curriculum)\b"
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

# 2026-09-24 (CLOSELOOP workstream b): from-scratch curriculum-design
# intent — "design/build/create/develop/propose a curriculum" (object is
# CURRICULUM, deliberately not "program": a bare "program" already fires
# _PEER_PROGRAM_INTENT_RE above via its own \bprograms?\b alternative, so
# keeping this regex scoped to "curriculum" keeps the two intents from
# overlapping in a confusing way — "design a new PROGRAM" already reads
# as more existing-institution-flavored language and correctly requires
# University Programs on its own). Bounded to 40 chars, no sentence-
# boundary crossing, same technique as _PEER_PROGRAM_INTENT_RE's
# possessive-reference alternatives above.
#
# Verified against every existing eval-battery case containing "curriculum"
# (chatbot/eval/orchestrator_queries.yaml): the five update-mixed cases
# (data-eng/soft-skills/mlops/cloud-infra-curriculum, broad-improve-
# curriculum) use "updating my"/"improve my"/"adding a module to my" —
# none match a design/build/create/develop/propose verb, so this doesn't
# fire on them (they're existing-program updates, University Programs
# already correctly required via the possessive "my ... curriculum"
# alternative in _PEER_PROGRAM_INTENT_RE). sector-wrap-finance-curriculum
# ("Design a finance-focused AI/ML Master's curriculum...") DOES match
# this regex, but also contains a bare "program" ("every such program
# needs"), so _PEER_PROGRAM_INTENT_RE fires too and the `not
# _PEER_PROGRAM_INTENT_RE.search(query)` guard below correctly prevents
# double-requiring Analyst+Cluster-Interpreter on top of it — that case's
# own must_delegate_to only requires the Analyst regardless. The natural
# G.2 query ("Design a graduate AI/ML curriculum... Use the demand skill
# clusters as the backbone...") matches this regex AND has no peer
# reference at all, which is exactly the target case this exists for.
_CURRICULUM_DESIGN_INTENT_RE = re.compile(
    r"\b(?:design|build|create|develop|propose|recommend)\b"
    r"[^.?!]{0,40}?\bcurriculum\b",
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
    peer-program queries via intent language ("program(s)", "compare",
    explicit "peer program/institution", a possessive existing-program
    reference like "my curriculum"/"our program") OR a degree-token
    mention (MMAI, MSAII, MEng, MSc, MPH, MS) — both of which co-occur
    with genuine peer-program asks without needing a separate
    institution-name check.

    2026-09-24 (CLOSELOOP B1, attempt C): the bare "curriculum"/
    "course(s)"/"teach(es)"/"offer(s)" alternatives were removed from
    _PEER_PROGRAM_INTENT_RE — they made EVERY curriculum-shaped query
    require University AI Programs Researcher, including a from-scratch
    "design a curriculum grounded in demand" ask with no existing
    program to benchmark against (Appendix G.2's actual shape). A
    from-scratch curriculum needs Cluster Interpreter + demand
    frequency, not peer-program content; benchmarking an EXISTING
    program is the separate G.3-style task, still correctly required via
    the signals kept above. See _PEER_PROGRAM_INTENT_RE's own comment
    for the full before/after verification against every case that
    relied on the removed alternatives.

    2026-09-24 (CLOSELOOP workstream b): a THIRD intent added —
    from-scratch curriculum-DESIGN intent (design/build/create/develop/
    propose A CURRICULUM, no existing-program reference) now requires
    BOTH Cluster Interpreter (Mode B — the curriculum scaffold) AND
    Skills Taxonomy Analyst (lift/z evidence), and explicitly does NOT
    add University AI Programs Researcher — this is the §4.6 method
    (clustering for structure, differential analysis for evidentiary
    weight) realized by the live system, per the new FROM-SCRATCH
    CURRICULUM DESIGN COOPERATION PATTERN in ORCHESTRATOR_BACKSTORY. The
    peer-intent check is a NEGATIVE gate here (`not
    _PEER_PROGRAM_INTENT_RE.search(query)`), not a separate independent
    trigger: a query matching both regexes (e.g. sector-wrap-finance-
    curriculum's "every such program needs") is an existing-program-
    adjacent ask, not a from-scratch one, and is left to the peer-intent
    branch above only. See _CURRICULUM_DESIGN_INTENT_RE's own comment
    for the full verification against every existing eval-battery case.

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
    if _CURRICULUM_DESIGN_INTENT_RE.search(query) and not _PEER_PROGRAM_INTENT_RE.search(query):
        required.add("Cluster Interpreter")
        required.add("Skills Taxonomy Analyst")
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


# 2026-09-10 (POLISH_attribution-flip_and_cost-tracking.md Item B):
# publicly-documented Anthropic per-token pricing for the claude-sonnet-4
# family (USD per million tokens) — the only model/provider combination
# this project's run_query() is currently used with on the paid lane.
# Approximate: does NOT account for prompt-cache read/write discount
# tiers (Anthropic prices cache reads well below, and cache writes
# somewhat above, the base input rate) — cached_prompt_tokens and
# cache_creation_tokens are reported as raw counts in the run record but
# not separately priced here, since getting that tiering exactly right
# is not "trivial" in the sense this task asked for. Treat the dollar
# figure as a rough estimate; the Anthropic console has the exact bill.
_ANTHROPIC_PRICE_PER_MILLION_TOKENS_USD = {
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
}


def _estimate_cost_usd(provider: str, model: str, prompt_tokens: int, completion_tokens: int) -> float | None:
    """Rough USD estimate for a known provider/model, or None if this
    combination has no price entry (callers report tokens-only in that
    case rather than a fabricated dollar figure)."""
    if provider != "anthropic":
        return None
    rates = _ANTHROPIC_PRICE_PER_MILLION_TOKENS_USD.get(model)
    if not rates:
        return None
    return (prompt_tokens * rates["input"] + completion_tokens * rates["output"]) / 1_000_000


def _format_cost_section(usage_metrics: object | None) -> list[str]:
    """Render a '## Cost / Usage' section from crew.usage_metrics.
    Defensive by design: usage_metrics is populated by CrewAI only after
    a real crew.kickoff() call, so it's legitimately absent for a
    request that failed before that point, or None if a future CrewAI
    version changes its shape — either way this writes an honest
    "usage unavailable" line instead of raising.
    """
    lines = ["## Cost / Usage", ""]
    if usage_metrics is None:
        lines += ["usage unavailable (no crew.usage_metrics captured this run).", ""]
        return lines
    try:
        prompt_tokens = int(usage_metrics.prompt_tokens)
        completion_tokens = int(usage_metrics.completion_tokens)
        total_tokens = int(usage_metrics.total_tokens)
        cached_prompt_tokens = int(getattr(usage_metrics, "cached_prompt_tokens", 0) or 0)
        cache_creation_tokens = int(getattr(usage_metrics, "cache_creation_tokens", 0) or 0)
        successful_requests = int(getattr(usage_metrics, "successful_requests", 0) or 0)
    except (AttributeError, TypeError, ValueError):
        lines += [
            "usage unavailable (crew.usage_metrics had an unexpected shape "
            "this run — see agents/orchestrator.py's _format_cost_section()).",
            "",
        ]
        return lines
    lines += [
        f"- **Prompt tokens:** {prompt_tokens:,}",
        f"- **Completion tokens:** {completion_tokens:,}",
        f"- **Total tokens:** {total_tokens:,}",
        f"- **Cached prompt tokens:** {cached_prompt_tokens:,} (not separately "
        f"priced below — see the pricing note above _estimate_cost_usd)",
        f"- **Cache-creation tokens:** {cache_creation_tokens:,} (not "
        f"separately priced below)",
        f"- **Successful LLM requests:** {successful_requests}",
    ]
    provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
    model = os.getenv("LLM_MODEL", "")
    cost = _estimate_cost_usd(provider, model, prompt_tokens, completion_tokens)
    if cost is not None:
        lines.append(
            f"- **Approx. cost:** ${cost:.4f} USD (rough estimate at "
            f"{model} list rates, prompt+completion tokens only — verify "
            f"against the Anthropic console for the exact bill)"
        )
    else:
        lines.append(
            f"- **Approx. cost:** not estimated (no price entry for "
            f"provider={provider!r} model={model!r} — token counts above "
            f"are still real)"
        )
    lines.append("")
    return lines


def _write_run_record(
    query: str,
    step_log: list[dict],
    wall_time_sec: float,
    answer: str | None,
    error: Exception | None,
    usage_metrics: object | None = None,
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
            + _detect_delegation_claim_flags(answer, delegated_to)
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
    lines += _format_cost_section(usage_metrics)
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
            "One or more of this run's five content guards flagged the "
            "final answer: attribution (a specialist NAME cited but not "
            "in `delegated_to`, `_detect_fabrication_flags()`), numeric "
            "(a lift/z/frequency NUMBER absent from any consulted "
            "specialist's output, `_detect_numeric_fabrication_flags()`), "
            "content-attribution (a course CODE, URL, or "
            "INSTITUTION absent from any consulted specialist's output, "
            "`_detect_content_attribution_flags()`), and/or "
            "delegation-claim honesty (an affirmative 'was consulted' "
            "claim naming a specialist not in `delegated_to`, "
            "`_detect_delegation_claim_flags()`) — all in "
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

    # 2026-09-25 (§5.1 F2022 PUSHTHROUGH, Part A1): when an alt-wave data
    # override is active (tools/cluster_tool.py's CLUSTER_RESULTS_FILE_OVERRIDE
    # env var), prepend the data-wave override notice to the query — the
    # SAME injection point as the "ATTACHED UPLOADED CURRICULUM DOCUMENT"
    # marker block (see ORCHESTRATOR_BACKSTORY's handling rule for that
    # feature), just for a different purpose. None (the default, no
    # override active) leaves `query` byte-for-byte unchanged. Centralised
    # here in run_query() itself — the single shared entry point every
    # caller (test scripts, eval harness, the Chainlit app) goes through —
    # so the override is honoured automatically without each caller having
    # to remember to add it.
    from tools.cluster_tool import data_wave_override_notice
    _wave_notice = data_wave_override_notice()
    if _wave_notice:
        query = f"{_wave_notice}\n\n{query}"

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
            "to the Skills Taxonomy Analyst for any lift/z). EXCEPTION — "
            "FROM-SCRATCH DESIGN: if the query instead asks you to "
            "design/build a NEW curriculum from scratch, grounded in "
            "market demand or demand clusters, naming NO existing "
            "program and requesting NO comparison, use the FROM-SCRATCH "
            "pattern instead: delegate to Cluster Interpreter (Mode B, "
            "the curriculum scaffold — no existing curriculum passed as "
            "context) and to the Skills Taxonomy Analyst for lift/z on "
            "the scaffold's key skills; build ~8-10 courses "
            "cluster-by-cluster. Do NOT delegate to the University AI "
            "Programs Researcher and do NOT produce any peer-program, "
            "course-code, URL, or program-comparison content for this "
            "case — peer benchmarking against an existing program is a "
            "separate, later ask, not part of designing something new. "
            "Close with a trade-off or caveat."
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
        # Defensive getattr: crew.usage_metrics is only guaranteed to be
        # populated by a completed kickoff() — a failure path CAN still
        # have partial usage recorded depending on how far the run got,
        # but this must never be the reason a failure record fails to
        # write, so absence/an unexpected shape is handled the same way
        # _format_cost_section() itself handles it (None -> "usage
        # unavailable"), not raised here.
        usage_metrics = getattr(crew, "usage_metrics", None)
        path = _write_run_record(
            query, step_log, wall_time, answer=None, error=e, usage_metrics=usage_metrics
        )
        raise RuntimeError(
            f"{type(e).__name__}: {e}\n\n"
            f"Partial output ({len(step_log)} specialist step(s) completed "
            f"before failure) saved to: {path}"
        ) from e
    else:
        wall_time = time.time() - t0
        usage_metrics = getattr(crew, "usage_metrics", None)
        path = _write_run_record(
            query, step_log, wall_time, answer=answer, error=None, usage_metrics=usage_metrics
        )
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
