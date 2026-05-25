"""
test_orchestrator.py — Standalone smoke test for the full multi-agent crew.

THIS IS THE MULTI-AGENT TEST GATE. First real read on whether the chosen
LLM (default: Sonnet 4.6) can coordinate sub-agents reliably across
multiple hops.

Cost: noticeably higher than the per-agent smoke tests — fans out across
3 agents, each may make multiple tool calls. Budget ~10-30¢ per query on
Sonnet 4.6, more on Opus, less on Haiku. Keep the query set small.

Run:
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_orchestrator.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from dotenv import load_dotenv  # noqa: E402
load_dotenv(os.path.join(_CHATBOT_DIR, ".env"))

from agents.orchestrator import run_query  # noqa: E402
from llm import describe_llm_config  # noqa: E402


# A query that NEEDS both specialists — Analyst for market demand on
# data engineering skills, University Programs for what Queen's MMAI
# actually covers. If the Orchestrator only consults one, the answer
# will be incomplete and we'll see the failure mode clearly.
DEFAULT_QUERIES = [
    "I'm updating my AI/ML Master's curriculum. What are the most "
    "in-demand data engineering skills I should make sure my program "
    "covers, and how does Queen's University's MMAI program compare "
    "on this dimension? Give me concrete recommendations for what to "
    "add or strengthen.",
]


def main() -> None:
    print(describe_llm_config())
    print()
    for q in DEFAULT_QUERIES:
        print(f"=== Query ===\n{q}\n")
        print("=== Response ===")
        print(run_query(q))
        print()


if __name__ == "__main__":
    main()
