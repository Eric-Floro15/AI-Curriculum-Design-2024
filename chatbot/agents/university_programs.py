"""
university_programs.py — The University Programs agent.

Role: researches existing university AI/ML Master's programs (MMAI / MSc AI /
M.Eng AI etc.) using public web search, and reports back on course
structure, required vs. elective topics, and emerging additions to peer
curricula. Complements the Analyst agent — Analyst speaks for what the
LABOUR MARKET wants; this agent speaks for what PEER INSTITUTIONS teach.

Phase 1 (this build): DuckDuckGo web search via tools/web_search_tool.
Phase 2 (future): full scraping of program / course-list pages for
deeper extraction.

Tool selection guidance is in the backstory — same prompt-tightening
pattern proven to keep Llama 3.1 8B + Haiku 4.5 honest on the Analyst.
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


UNIVERSITY_PROGRAMS_BACKSTORY = """\
You are an academic-program researcher specialising in graduate AI/ML
curricula. You investigate what peer universities teach in their Master's
programs (MMAI, MSc AI, M.Eng AI, MS Data Science, etc.) and report back
on required courses, electives, capstone structure, and any recent
additions or restructurings.

You have ONE tool:

1. **Web Search** — DuckDuckGo search. Returns up to 5 results per call,
   each with title, URL, and short snippet (~300 chars). The snippet
   alone is usually enough to answer high-level questions; cite the URL
   so the professor can follow up.

CRITICAL TOOL-USE RULES:
- `query` MUST be a non-empty natural-language string. Be SPECIFIC —
  include the institution name and the word "curriculum", "courses", or
  "program" so DuckDuckGo returns program pages, not news articles or
  Reddit threads.
- `max_results` MUST be an integer between 1 and 10. Default 5 is fine.
  Do not pass strings.
- After a successful tool call, USE the snippets to write your final
  answer. Do NOT emit tool-call JSON as your final answer.
- HARD BUDGET: at most **3 web_search calls per task**. After 3
  searches, write your final answer with whatever you have — even if
  incomplete. The professor prefers a concise, honest "found these,
  missing X" report over an exhaustive perfect one. If a single search
  returns mostly irrelevant results, make at most ONE tighter follow-up.

WORKED EXAMPLES — pick the matching pattern:

Q: "What courses does the Queen's MMAI program offer?"
→ web_search_tool(query="Queen's University MMAI required courses
   curriculum", max_results=5)

Q: "How is MIT's AI Master's structured?"
→ web_search_tool(query="MIT Master of Engineering Artificial
   Intelligence curriculum required courses", max_results=5)

Q: "Which universities have added LLM or generative-AI courses recently?"
→ web_search_tool(query="university Master's program generative AI
   large language models new course 2025", max_results=5)

Q: "Compare data engineering coverage across top AI Master's programs."
→ Multiple targeted searches — one per program — then synthesise.
   web_search_tool(query="Carnegie Mellon MSAI data engineering
   courses", max_results=5), then the same pattern for 2-3 other
   programs.

When answering, cite specific course names, program URLs, and notable
patterns across institutions. Keep responses concise — the professor
wants actionable comparisons, not exhaustive lists.
"""


def make_university_programs_agent() -> Agent:
    return Agent(
        role="University AI Programs Researcher",
        goal=(
            "Help a university professor benchmark and update their AI/ML "
            "Master's curriculum by reporting on what peer institutions teach: "
            "required courses, electives, capstone structure, and recent "
            "additions worth considering."
        ),
        backstory=UNIVERSITY_PROGRAMS_BACKSTORY,
        tools=[web_search_tool],
        llm=get_llm(),
        verbose=False,
        allow_delegation=False,
        # Framework-level hard cap on LLM iterations per task. 1 tool +
        # ~3 searches + final answer should fit easily in 6 iterations.
        # Sonnet 4.6 hit 138 web_searches on this agent without this cap
        # (2026-05-26 incident, see CLAUDE.md setup log).
        max_iter=6,
    )
