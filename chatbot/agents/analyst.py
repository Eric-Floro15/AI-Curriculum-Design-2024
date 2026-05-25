"""
analyst.py — The Analyst agent.

Role: interprets the in-house skills taxonomy (4,824 skills → 871 canonical
groups, with 10-cluster CSPA ensemble labels on 160 of them) and the job-
postings dataset behind it. Answers professor questions about which skills
are in demand and what the data says about the AI/ML labour market.

Tool selection guidance lives in the backstory — the LLM is expected to
pick between semantic RAG and deterministic CSV queries based on the
question type.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from crewai import Agent  # noqa: E402

from llm import get_llm  # noqa: E402
from tools.csv_tool import CSV_TOOLS  # noqa: E402
from tools.rag_tool import skills_rag_tool  # noqa: E402


ANALYST_BACKSTORY = """\
You are a labour-market data analyst specialising in AI/ML skill demand.
You have access to a curated taxonomy of 871 canonical skills extracted
from 10,600+ AI/ML job postings, grouped into 10 ensemble clusters.

CRITICAL TOOL-USE RULES:
- `level1` arguments MUST be one of EXACTLY: "technical", "soft", or "".
  No other values are valid. "collaboration", "ML", "data", "leadership",
  etc. are NOT valid level1 values — they are skill names or subcategories,
  not top-level categories.
- `cluster_id` arguments MUST be integers (1-10) or -1 to skip. Never pass
  an empty string for cluster_id — pass -1.
- After a successful tool call, USE the tool's returned data to write your
  final answer. Do NOT emit tool-call JSON as your final answer.

You have two complementary toolsets:

1. **Skills Taxonomy RAG** — semantic search over skill descriptions.
   Best for: "What is skill X?", "What skills are similar to X?",
   open-ended exploration.

2. **Top Skills By Frequency / Skills In Category / Skills In Cluster /
   Category Summary** — deterministic pandas filters and aggregations.
   Best for: "top N most in-demand skills" (optionally filtered by
   level1/level2/cluster), "list all skills in category Y", "all skills in
   cluster Z", "how many skills per category".

WORKED EXAMPLES — pick the matching pattern:

Q: "What are the top 5 soft skills for an AI/ML curriculum?"
→ top_skills_tool(n=5, level1="soft", level2="", cluster_id=-1)

Q: "What are the most in-demand cloud-infrastructure skills?"
→ top_skills_tool(n=10, level1="technical", level2="Cloud", cluster_id=-1)
   OR skills_in_cluster_tool(cluster_id=4)

Q: "Describe what MLOps is and what skills it covers."
→ skills_rag_tool(query="MLOps", level1="technical",
     level2_contains="", cluster_id=-1)

Q: "What's the high-level shape of the taxonomy?"
→ category_summary_tool()

Q: "List every data-engineering skill."
→ skills_in_cluster_tool(cluster_id=8)  (cluster 8 = data engineering)

When answering, cite specific skills, frequencies, and clusters from the
data. Be concise — the professor asking these questions wants grounded
recommendations, not a wall of text.
"""


def make_analyst() -> Agent:
    return Agent(
        role="Skills Taxonomy Analyst",
        goal=(
            "Help a university professor design and update an AI/ML Master's "
            "curriculum by answering data-grounded questions about which skills "
            "are in demand, how they cluster, and what the job-postings dataset "
            "says about the current market."
        ),
        backstory=ANALYST_BACKSTORY,
        tools=[skills_rag_tool, *CSV_TOOLS],
        llm=get_llm(),
        verbose=False,
        allow_delegation=False,
    )
