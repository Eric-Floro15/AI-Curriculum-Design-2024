"""
test_cluster_interpreter.py — Standalone smoke test for the Cluster Interpreter.

Passes a hardcoded curriculum summary (Queen's University MMAI, based on the
known course list) directly to the agent — no web search needed. This isolates
the cluster analysis logic from the Curriculum Architect so it can be tested
and validated independently.

What a passing run produces:
  - A coverage assessment for all 10 CSPA clusters (✅ / ⚠️ / ❌)
  - Priority gaps for the focused clusters (2, 4, 7, 8, 9)
  - Specific skill recommendations per missing cluster, sorted by frequency
  - A summary table
  - Caveats about cluster coverage limitations

Cost:  ~5–10¢ on Sonnet 4.6  (~1 overview call + 3–4 detail calls)
       $0 on qwen2.5:14b      (~8–15 min on CPU)

Run:
    cd chatbot
    KMP_DUPLICATE_LIB_OK=TRUE python3 agents/test_cluster_interpreter.py

    # With a specific model:
    KMP_DUPLICATE_LIB_OK=TRUE LLM_PROVIDER=ollama LLM_MODEL=qwen2.5:14b \\
        python3 agents/test_cluster_interpreter.py
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
from agents.cluster_interpreter import make_cluster_interpreter  # noqa: E402
from llm import describe_llm_config  # noqa: E402


# ── Hardcoded curriculum summary (Queen's MMAI) ───────────────────────────────
# This mirrors the structured output the Curriculum Architect would produce.
# Using a fixed input lets us test the Cluster Interpreter in isolation without
# requiring a live web search or a full Orchestrator run.
MMAI_CURRICULUM_SUMMARY = """
Program: Queen's University Master of Management in Artificial Intelligence (MMAI)
Source: https://smith.queensu.ca/grad_studies/mmai/program/

Required Courses:
  - Foundations of Artificial Intelligence: Introduction to AI concepts, agents,
    search, and knowledge representation.
  - Machine Learning: Supervised and unsupervised learning, model evaluation.
  - Data Management and Governance: Data ethics, privacy, regulatory frameworks.
  - Business Strategy and AI: Applying AI to business decisions, ROI analysis.
  - AI Project Management: Managing AI/ML projects, agile methodologies.
  - Responsible AI and Ethics: Bias, fairness, accountability in AI systems.
  - Applied AI Capstone: Real-world consulting project with industry partner.

Elective Courses (selection):
  - Natural Language Processing
  - Computer Vision
  - AI in Finance
  - AI in Healthcare

Broad Topic Areas Covered:
  Machine Learning, Business Strategy, Data Governance, Ethics, Project Management,
  Natural Language Processing, Computer Vision, Capstone/Applied Project

Notes:
  Detailed syllabi not publicly listed. Elective offerings vary by term.
  Strong management and business focus — fewer deep-technical engineering courses
  compared to a traditional CS Master's program.
"""

QUERY = (
    f"Here is the structured curriculum summary for Queen's University MMAI:\n\n"
    f"{MMAI_CURRICULUM_SUMMARY}\n\n"
    "Using the CSPA ensemble clustering results, perform a systematic gap analysis: "
    "which of the 10 skill clusters are covered, underrepresented, or entirely missing "
    "from this curriculum? For each missing or partial focused cluster (2, 4, 7, 8, 9), "
    "list the top skills the program should add, sorted by market demand frequency. "
    "End with a prioritised summary table and caveats."
)

EXPECTED_OUTPUT = (
    "A structured gap analysis report containing: "
    "(1) coverage assessment for all 10 clusters with ✅/⚠️/❌ labels and brief "
    "justification for each verdict, "
    "(2) priority gaps section covering each missing/partial focused cluster with "
    "top skills sorted by frequency and a concrete recommendation, "
    "(3) a summary table of all clusters with coverage status and priority, "
    "(4) caveats about the analysis limitations."
)


def main() -> None:
    print(describe_llm_config())
    print()
    print("=== Input curriculum summary ===")
    print(MMAI_CURRICULUM_SUMMARY)
    print("=== Running Cluster Interpreter ===")

    agent = make_cluster_interpreter()
    task = Task(
        description=QUERY,
        expected_output=EXPECTED_OUTPUT,
        agent=agent,
    )
    crew = Crew(agents=[agent], tasks=[task], verbose=True)

    result = crew.kickoff()
    print("\n=== Cluster Interpreter Output ===")
    print(result)


if __name__ == "__main__":
    main()
