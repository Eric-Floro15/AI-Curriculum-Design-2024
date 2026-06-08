"""
test_news.py — Standalone smoke test for the News agent.

Runs one professor query end-to-end through Crew.kickoff() against the
configured LLM. Same pattern as test_analyst.py / test_university_programs.py.

Run:
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_news.py
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

from agents.news import make_news_agent  # noqa: E402
from llm import describe_llm_config  # noqa: E402


# A single representative query for the smoke test. The query is
# deliberately broad — we want to see whether the agent picks a
# focused search angle rather than just echoing "AI".
DEFAULT_QUERIES = [
    "What recent developments in AI agents and autonomous systems should "
    "I incorporate into my AI/ML Master's curriculum? Cite specific "
    "articles."
]


def run_one(agent, query: str) -> str:
    task = Task(
        description=query,
        expected_output=(
            "A concise summary of the top 3-5 recent developments most "
            "relevant to curriculum design, each citing the source "
            "article title and link from the news corpus."
        ),
        agent=agent,
    )
    crew = Crew(agents=[agent], tasks=[task], verbose=False)
    return str(crew.kickoff())


def main() -> None:
    print(describe_llm_config())
    print()
    agent = make_news_agent()
    for q in DEFAULT_QUERIES:
        print(f"=== Query ===\n{q}\n")
        print("=== Response ===")
        print(run_one(agent, q))
        print()


if __name__ == "__main__":
    main()
