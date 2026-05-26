"""
test_orchestrator_verbose.py — Verbose diagnostic variant of the multi-agent
test gate.

Use this (instead of `test_orchestrator.py`) when you need to SEE the
delegation pattern — which sub-agents were called, what tools each used,
how the Orchestrator synthesised. The canonical `test_orchestrator.py`
runs with `verbose=False` and prints only the final answer; this script
sets `verbose=True` on every agent and the Crew, so the log captures:

  - Each `delegate_work_to_coworker` / `ask_question_to_coworker` call
  - Each sub-agent's tool invocations (with args)
  - Each sub-agent's Final Answer
  - The Orchestrator's final synthesis

This was the workhorse during the 2026-05-26 multi-agent validation
push (see CLAUDE.md setup log) where we needed to distinguish "model
delegated and got bad data" from "model didn't delegate at all" — pass
criteria invisible without verbose tracing.

Same query, same Task, same Crew assembly as `test_orchestrator.py` —
the only differences are `verbose=True` everywhere and a wall-time
printout at the end.

Cost: same as test_orchestrator.py — ~25-50¢ per query on Sonnet 4.6,
free on local Ollama (but ~35 min on qwen2.5:14b on 16 GB Mac CPU; see
the Run 5 entry in the 2026-05-26 setup log).

Run:
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_orchestrator_verbose.py
"""

import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from dotenv import load_dotenv  # noqa: E402
load_dotenv(os.path.join(_CHATBOT_DIR, ".env"))

from crewai import Crew, Task  # noqa: E402

from agents.analyst import make_analyst  # noqa: E402
from agents.news import make_news_agent  # noqa: E402
from agents.orchestrator import make_orchestrator  # noqa: E402
from agents.university_programs import make_university_programs_agent  # noqa: E402
from llm import describe_llm_config  # noqa: E402


# Same query as test_orchestrator.py — the data-engineering / Queen's MMAI
# question, deliberately ambiguous about whether News is needed. With the
# bug-fixed orchestrator backstory (2026-05-26), the Orchestrator should
# consult ALL THREE specialists for any curriculum-update query.
DEFAULT_QUERIES = [
    "I'm updating my AI/ML Master's curriculum. What are the most "
    "in-demand data engineering skills I should make sure my program "
    "covers, and how does Queen's University's MMAI program compare "
    "on this dimension? Give me concrete recommendations for what to "
    "add or strengthen.",
]


def run_one(query: str) -> str:
    """Build a fresh 4-agent crew with verbose=True and run one query."""
    analyst = make_analyst()
    univ = make_university_programs_agent()
    news = make_news_agent()
    orch = make_orchestrator()
    for a in (orch, analyst, univ, news):
        a.verbose = True

    task = Task(
        description=query,
        expected_output=(
            "A single coherent recommendation for the professor. Open with "
            "a 2-3 sentence executive summary. Then a structured body of "
            "concrete recommendations citing specific skills with "
            "frequencies (from the Analyst), peer-program courses with "
            "URLs (from the University Programs researcher), and recent "
            "articles with titles + sources (from the News researcher) "
            "where each is relevant. Close with a trade-off or caveat."
        ),
        agent=orch,
    )
    crew = Crew(
        agents=[orch, analyst, univ, news],
        tasks=[task],
        verbose=True,
    )
    return str(crew.kickoff())


def main() -> None:
    print(describe_llm_config())
    print()
    for q in DEFAULT_QUERIES:
        print(f"=== Query ===\n{q}\n")
        print("=== Response ===")
        t0 = time.time()
        print(run_one(q))
        print(f"\n=== WALL TIME: {time.time() - t0:.1f}s ===\n")


if __name__ == "__main__":
    main()
