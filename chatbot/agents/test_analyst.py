"""
test_analyst.py — Standalone smoke test for the Analyst agent.

Runs one (or more) professor queries end-to-end through Crew.kickoff()
and prints the agent's response. Hits the configured LLM, so it costs
real API budget — keep the query set small.

Run:
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_analyst.py
"""

import os
import sys

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

from agents.analyst import make_analyst  # noqa: E402
from llm import describe_llm_config  # noqa: E402


# A single representative query for the smoke test. Add more here when
# debugging — but every entry hits the LLM, so keep it deliberate.
DEFAULT_QUERIES = [
    "What soft skills should I emphasise in an AI/ML Master's curriculum? "
    "Give me 3-5 concrete recommendations grounded in the taxonomy.",
]


def run_one(analyst, query: str) -> str:
    task = Task(
        description=query,
        expected_output=(
            "A concise data-grounded answer (3-5 bullet points or a short "
            "paragraph) referencing specific skills, frequencies, or "
            "clusters from the taxonomy where appropriate."
        ),
        agent=analyst,
    )
    crew = Crew(agents=[analyst], tasks=[task], verbose=False)
    return str(crew.kickoff())


def main() -> None:
    print(describe_llm_config())
    print()
    analyst = make_analyst()
    for q in DEFAULT_QUERIES:
        print(f"=== Query ===\n{q}\n")
        print("=== Response ===")
        print(run_one(analyst, q))
        print()


if __name__ == "__main__":
    main()
