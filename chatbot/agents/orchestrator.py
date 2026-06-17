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

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from crewai import Agent, Crew, Task  # noqa: E402

from agents.analyst import make_analyst  # noqa: E402
from agents.cluster_interpreter import make_cluster_interpreter  # noqa: E402
from agents.news import make_news_agent  # noqa: E402
from agents.university_programs import make_university_programs_agent  # noqa: E402
from llm import get_llm  # noqa: E402


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


def run_query(query: str) -> str:
    """Run a single professor query end-to-end through the full crew."""
    analyst = make_analyst()
    univ_programs = make_university_programs_agent()
    news = make_news_agent()
    cluster_interp = make_cluster_interpreter()
    orchestrator = make_orchestrator()

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
    return str(crew.kickoff())
