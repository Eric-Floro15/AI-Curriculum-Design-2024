"""
test_university_programs.py — Standalone smoke test for the University
Programs agent.

Runs one professor query end-to-end through Crew.kickoff() and prints
the response. Hits the configured LLM AND the live DuckDuckGo endpoint,
so it costs real API budget and depends on network — keep the query set
small.

Run:
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_university_programs.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from dotenv import load_dotenv  # noqa: E402
load_dotenv(os.path.join(_CHATBOT_DIR, ".env"))

from crewai import Crew, Task  # noqa: E402

from agents.university_programs import make_university_programs_agent  # noqa: E402
from llm import describe_llm_config  # noqa: E402


DEFAULT_QUERIES = [
    "What courses does the Queen's University MMAI program offer, "
    "and what topics are emphasised? Cite URLs for the program pages.",
]


def run_one(agent, query: str) -> str:
    task = Task(
        description=query,
        expected_output=(
            "A concise data-grounded answer (3-6 bullet points or a short "
            "paragraph) summarising the program, naming specific courses "
            "or topics where possible, and citing the URL(s) used."
        ),
        agent=agent,
    )
    crew = Crew(agents=[agent], tasks=[task], verbose=False)
    return str(crew.kickoff())


def main() -> None:
    print(describe_llm_config())
    print()
    agent = make_university_programs_agent()
    for q in DEFAULT_QUERIES:
        print(f"=== Query ===\n{q}\n")
        print("=== Response ===")
        print(run_one(agent, q))
        print()


if __name__ == "__main__":
    main()
