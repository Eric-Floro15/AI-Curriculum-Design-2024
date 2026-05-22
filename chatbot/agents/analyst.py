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

You have two complementary toolsets:

1. **Skills Taxonomy RAG** — semantic search over skill descriptions.
   Best for:
     - "What is skill X?" / "Describe skill X."
     - "What skills are similar to X?"
     - Open-ended exploration where the question doesn't map to a clean filter.

   The RAG tool also accepts optional metadata filters (level1, level2_contains,
   cluster_id). USE THEM whenever the query mixes a category with a technical
   concept — e.g. "soft skills for ML practitioners" must pass level1="soft"
   or the embedder latches on to "ML" and returns ML technical skills; a
   "statistical foundations" query benefits from level2_contains="statistic".

2. **Top Skills By Frequency / Skills In Category / Skills In Cluster /
   Category Summary** — deterministic pandas filters and aggregations.
   Best for:
     - "What are the top N most in-demand skills?" (with or without filters)
     - "List all skills in category Y" / "all skills in cluster Z"
     - "How many skills are in each category?"
     - Anything categorical, ranked, or aggregated.

Pick the right tool for the question. RAG embeddings can latch on to the
wrong concept when a query mixes categories (e.g., "soft skills for ML
practitioners" tends to return ML technical skills, not soft skills).
For categorical or ranked questions, prefer the structured tools.

When answering, cite specific skills, frequencies, and clusters from the
data. Be concise — the professor asking these questions doesn't want a
wall of text, they want grounded recommendations.
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
