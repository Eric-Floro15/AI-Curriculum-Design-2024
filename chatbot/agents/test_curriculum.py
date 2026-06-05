"""
test_curriculum.py — Standalone smoke test for the Curriculum Architect agent.

The Curriculum Architect is a web-search-only agent. It fetches and structures
the publicly available curriculum of a specific program — nothing more. It does
NOT perform gap analysis or compare against the skills taxonomy (that is the
Cluster Interpreter's job).

What a passing run produces:
  - Program name and source URL(s)
  - Required courses list with brief descriptions from web snippets
  - Elective courses if listed publicly
  - Broad topic areas covered (comma-separated)
  - Notes about what couldn't be verified

The output is intentionally concise and factual — it is designed to be passed
to the Cluster Interpreter by the Orchestrator as context for gap analysis.

Cost:  ~3–8¢ on Sonnet 4.6  (1–2 web searches + synthesis)
       $0 on qwen2.5:14b     (~5–12 min on CPU)

Run:
    cd chatbot
    KMP_DUPLICATE_LIB_OK=TRUE python3 agents/test_curriculum.py

    # With a specific model:
    KMP_DUPLICATE_LIB_OK=TRUE LLM_PROVIDER=ollama LLM_MODEL=qwen2.5:14b \\
        python3 agents/test_curriculum.py
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
from agents.curriculum import make_curriculum_agent  # noqa: E402
from llm import describe_llm_config  # noqa: E402


QUERY = (
    "Fetch and structure the publicly available curriculum for Queen's University "
    "MMAI (Master of Management in Artificial Intelligence) program. Search for the "
    "current course list — both required and elective courses — and return a clean "
    "structured summary with course names, brief descriptions where available, "
    "source URLs, and the broad topic areas the program covers. "
    "Do not perform gap analysis or compare against any skills taxonomy."
)

EXPECTED_OUTPUT = (
    "A structured curriculum report containing: "
    "(1) program name and institution, "
    "(2) source URL(s) found, "
    "(3) list of required courses with brief descriptions from search snippets, "
    "(4) list of elective courses if publicly available, "
    "(5) broad topic areas covered as a comma-separated list, "
    "(6) notes about what could not be verified (e.g. syllabi behind login wall). "
    "No gap analysis, no skill comparisons, no recommendations — just the curriculum facts."
)


def main() -> None:
    print(describe_llm_config())
    print()
    print("=== Query ===")
    print(QUERY)
    print()

    agent = make_curriculum_agent()
    task = Task(
        description=QUERY,
        expected_output=EXPECTED_OUTPUT,
        agent=agent,
    )
    crew = Crew(agents=[agent], tasks=[task], verbose=True)

    print("=== Response ===")
    result = crew.kickoff()
    print(result)


if __name__ == "__main__":
    main()
