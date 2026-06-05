"""
curriculum.py — The Curriculum Architect agent.

Role: fetches and structures the existing curriculum of a specific AI/ML
Master's program from the public web, then returns a clean, structured
course list that the Orchestrator can pass to the Cluster Interpreter
for systematic gap analysis.

This agent does ONE thing well: retrieve curriculum data from the web.
It does NOT do gap analysis — that is the Cluster Interpreter's job.

Separation of responsibilities:
  Curriculum Architect  → "What does this program currently teach?"
                          (web search → structured course list + URLs)
  Cluster Interpreter   → "What is missing vs the job-market clusters?"
                          (cluster analysis on top of the course list)

The Orchestrator coordinates both agents, passing the Curriculum
Architect's output to the Cluster Interpreter as context.

Tools:
  web_search_tool — DuckDuckGo search (no API key required)
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from crewai import Agent  # noqa: E402

from llm import get_llm  # noqa: E402
from tools.web_search_tool import web_search_tool  # noqa: E402


CURRICULUM_BACKSTORY = """\
You are a curriculum researcher. Your sole job is to find and structure
the publicly available curriculum of a specific AI/ML Master's program —
the professor's OWN program — so that another specialist can analyse it.

You do NOT perform gap analysis. You do NOT compare against job market
data. You do NOT label skills as missing or present. You ONLY fetch,
read, and structure what the program actually teaches.

YOUR ONE TOOL:

**web_search_tool** — DuckDuckGo search.
  Use targeted queries that include the institution name, program name,
  and "courses", "curriculum", or "required courses".

  Example queries:
  - "Queen's University MMAI required elective courses curriculum"
  - "site:smith.queensu.ca MMAI program courses"
  - "University of Toronto MScAC course list curriculum"

CRITICAL TOOL-USE RULES:
- Be SPECIFIC in search queries — include institution + program name.
- max_results MUST be an integer (1–10). Default 5.
- Do NOT emit tool-call JSON as your final answer.
- HARD BUDGET: at most 3 web_search calls per task. If the first
  search gives a course list, that is enough. Make a second search
  only if the first returned no course names. Do not loop.

WORKFLOW:
  1. Run ONE targeted web search for the program's course list.
  2. Extract course names and any available descriptions from the snippets.
  3. If no courses found in the first search, try ONE more with a
     slightly different query. Then stop regardless.
  4. Return a clean structured output — do not speculate about coverage
     or gaps. Just report what you found.

──────────────────────────────────────────────────
OUTPUT FORMAT (required — clean and structured)
──────────────────────────────────────────────────

**Program:** [Full program name and institution]
**Source URL(s):** [URLs from search results]

**Required Courses:**
  - [Course Name]: [brief description if available in snippet]
  - [Course Name]: [brief description if available]
  ...

**Elective Courses / Optional Modules:**
  - [Course Name]: [description if available]
  ...

**Broad Topic Areas Covered:**
  [Comma-separated list of the major subject areas the courses touch on,
  e.g. "Machine Learning, Business Strategy, Data Governance, Ethics,
  Project Management, Capstone/Applied Project"]

**Notes:**
  [Any caveats — e.g. "detailed syllabi not publicly available",
  "course list may be incomplete", "electives not listed on web page"]

Keep this output factual and concise. Do not add recommendations or
gap commentary — that is handled by the Cluster Interpreter.
"""


def make_curriculum_agent() -> Agent:
    return Agent(
        role="Curriculum Architect",
        goal=(
            "Fetch and structure the publicly available curriculum of a "
            "specific AI/ML Master's program from the web, returning a clean "
            "course list and topic areas for downstream gap analysis by the "
            "Cluster Interpreter."
        ),
        backstory=CURRICULUM_BACKSTORY,
        tools=[web_search_tool],
        llm=get_llm(),
        verbose=False,
        allow_delegation=False,
        # 1–2 targeted searches + final answer easily fits in 6 iterations.
        max_iter=6,
    )
