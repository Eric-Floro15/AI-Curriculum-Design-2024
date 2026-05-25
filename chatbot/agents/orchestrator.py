"""
orchestrator.py — The Orchestrator agent + multi-agent crew assembly.

Role: receives the professor's natural-language query, decides which
sub-agents (Analyst, University Programs) to consult, and synthesises
their outputs into a single coherent recommendation.

This is the multi-agent test gate — first real read on whether the
chosen LLM can coordinate sub-agents reliably across multiple hops.

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
from agents.university_programs import make_university_programs_agent  # noqa: E402
from llm import get_llm  # noqa: E402


ORCHESTRATOR_BACKSTORY = """\
You are a senior curriculum advisor coordinating two specialist
researchers to help a university professor design or update an AI/ML
Master's program. You do NOT answer the professor directly from your
own knowledge — you delegate to your specialists and synthesise their
outputs.

YOUR TWO SPECIALISTS:

1. **Skills Taxonomy Analyst** — knows what skills are in demand in
   the AI/ML job market. Backed by 10,600+ job postings, ~871 canonical
   skills, 10 ensemble clusters. Use when the question touches market
   demand, skill frequencies, in-demand topics, or cluster themes.

2. **University AI Programs Researcher** — knows what peer institutions
   teach in their AI/ML Master's programs. Backed by public web search.
   Use when the question touches benchmarking, comparing curricula,
   peer-program coverage, or recent program additions.

CRITICAL DELEGATION RULES:
- MOST professor queries benefit from BOTH perspectives — what the
  market wants AND what peers teach. Default to consulting both unless
  the query is clearly only about one.
- When you delegate, frame the sub-question PRECISELY. Good: "What are
  the top 10 most in-demand data engineering skills by frequency?"
  Bad: "Tell me about data engineering."
- Delegate at most ONCE to each specialist per query. Do NOT loop, do
  NOT re-ask the same question hoping for a better answer.
- If a specialist's output is incomplete, use what they gave you and
  note the gap in your final answer — do not re-delegate.
- Your final answer to the professor is a SINGLE coherent
  recommendation, not a raw transcript of the specialists' outputs.

OUTPUT FORMAT for your final answer:
- Open with a 2-3 sentence executive summary of the recommendation.
- Then a structured body with concrete picks (skills to add, topics
  to emphasise, courses to update). Cite the evidence — frequency
  numbers from the Analyst, peer-program course names and URLs from
  the University Programs researcher.
- Close with the trade-off or caveat the professor should consider.
"""


def make_orchestrator() -> Agent:
    return Agent(
        role="Senior Curriculum Advisor",
        goal=(
            "Coordinate the Skills Taxonomy Analyst and the University AI "
            "Programs Researcher to give a university professor a single "
            "coherent, data-grounded recommendation about what skills, "
            "topics, or courses to add to their AI/ML Master's curriculum."
        ),
        backstory=ORCHESTRATOR_BACKSTORY,
        llm=get_llm(),
        allow_delegation=True,
        verbose=False,
    )


def build_crew() -> tuple[Crew, Agent]:
    """
    Build a fresh Crew with all three agents. Returns (crew, orchestrator)
    so callers can attach a Task to the orchestrator and kick off.

    Agents are rebuilt per call so conversation state doesn't bleed
    between queries.
    """
    analyst = make_analyst()
    univ_programs = make_university_programs_agent()
    orchestrator = make_orchestrator()
    crew = Crew(
        agents=[orchestrator, analyst, univ_programs],
        tasks=[],  # caller adds the task
        verbose=False,
    )
    return crew, orchestrator


def run_query(query: str) -> str:
    """Run a single professor query end-to-end through the full crew."""
    analyst = make_analyst()
    univ_programs = make_university_programs_agent()
    orchestrator = make_orchestrator()

    task = Task(
        description=query,
        expected_output=(
            "A single coherent recommendation for the professor. Open with "
            "a 2-3 sentence executive summary. Then a structured body of "
            "concrete recommendations citing specific skills with "
            "frequencies (from the Analyst) and peer-program courses with "
            "URLs (from the University Programs researcher). Close with a "
            "trade-off or caveat."
        ),
        agent=orchestrator,
    )
    crew = Crew(
        agents=[orchestrator, analyst, univ_programs],
        tasks=[task],
        verbose=False,
    )
    return str(crew.kickoff())
