"""
test_curriculum.py — Standalone smoke test for the Curriculum Architect agent.

Tests the agent in isolation (no Orchestrator, no other sub-agents) with a
single query referencing Queen's MMAI — the canonical program used throughout
the project's evaluation baseline.

What a passing run produces:
  - A curriculum summary fetched from smith.queensu.ca or similar
  - A skill coverage map (✅ / ⚠️ / ❌) for major taxonomy areas
  - A gap analysis with at least one skill frequency cited
  - Numbered recommendations with market justifications

Cost:  ~5–15¢ on Sonnet 4.6  (~2–4 LLM calls + 4–6 tool dispatches)
       $0 on qwen2.5:14b      (~10–25 min on CPU)

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
    "Analyse the Queen's University MMAI (Master of Management in Artificial "
    "Intelligence) program curriculum. Fetch the current course list from the "
    "web, then compare it against the in-demand AI/ML skills in the job-market "
    "taxonomy. Identify the top gaps — skills most in-demand that the program "
    "doesn't cover — and give concrete recommendations for what to add or "
    "strengthen. Cite skill frequencies and the program URL."
)

EXPECTED_OUTPUT = (
    "A structured report with: (1) current curriculum summary with source URL, "
    "(2) skill coverage map showing which market skills are covered vs missing, "
    "(3) gap analysis listing high-demand uncovered skills with frequencies, "
    "(4) numbered recommendations with market justifications, (5) caveats about "
    "what couldn't be verified."
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
