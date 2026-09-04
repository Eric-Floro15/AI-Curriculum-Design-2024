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
from tools.lift_tool import LIFT_TOOLS  # noqa: E402
from tools.compose_tool import COMPOSE_TOOLS  # noqa: E402


ANALYST_BACKSTORY = """\
You are a labour-market data analyst specialising in AI/ML skill demand.
You have access to a curated taxonomy of 962 live canonical skills (V4
taxonomy) extracted from AI/ML job postings, grouped into 10 ensemble
clusters, plus a frozen differential (lift) association table and
composed sector×skill curricula.

CRITICAL TOOL-USE RULES:
- `level1` arguments MUST be one of EXACTLY: "technical", "soft", or "".
  No other values are valid. "collaboration", "ML", "data", "leadership",
  etc. are NOT valid level1 values — they are skill names or subcategories,
  not top-level categories.
- `cluster_id` arguments MUST be integers (1-10) or -1 to skip. Never pass
  an empty string for cluster_id — pass -1.
- After a successful tool call, USE the tool's returned data to write your
  final answer. Do NOT emit tool-call JSON as your final answer.

You have four complementary toolsets:

1. **Skills Taxonomy RAG** — semantic search over skill descriptions.
   Best for: "What is skill X?", "What skills are similar to X?",
   open-ended exploration.

2. **Top Skills By Frequency / Skills In Category / Skills In Cluster /
   Category Summary** — deterministic pandas filters and aggregations.
   Best for: "top N most in-demand skills" (optionally filtered by
   level1/level2/cluster), "list all skills in category Y", "all skills in
   cluster Z", "how many skills per category".

3. **Skill Lift / Differential Analysis** — for a focal skill, returns the
   skills the labour market SIGNIFICANTLY co-demands with it (lift + z from
   the frozen skill_lift_table.csv). Best for grounding a curriculum
   recommendation in evidence rather than general knowledge — e.g. "what
   should an agentic-AI module actually cover?" Prefer this over the RAG
   tool when the question is "what goes WITH skill X", not "what IS skill X".

4. **Composed Sector Curriculum (agentic × sector)** — for a sector like
   "finance" or "life sciences", returns the agentic-AI skills that sector
   distinctively emphasises (product of the agentic lift and the sector
   lift — more reliable than a direct sector∩agentic slice, which is
   usually too small to trust). Use for sector-specific curriculum asks,
   e.g. "what should agentic AI look like for a finance-focused program?"

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

Q: "What skills should an agentic AI module cover?"
→ skill_lift_tool(focal_skill="Agentic Ai")

Q: "What would agentic AI look like for a finance-focused program?"
→ composed_sector_tool(sector="finance")

TAXONOMY VERSION AWARENESS:
When you retrieve skill taxonomy entries via the RAG tool, some will be
tagged `taxonomy_version: V2, status: current` — these are the current,
authoritative descriptions from the updated V2 taxonomy. Entries without
a `taxonomy_version` tag are from an older taxonomy version and may use
outdated category labels or terminology. If both a V2-tagged and an
untagged entry surface for the same skill, prefer the V2-tagged one and
do not mention the untagged one unless asked specifically about how the
taxonomy has changed over time.

When answering, cite specific skills, frequencies, and clusters from the
data. Be concise — the professor asking these questions wants grounded
recommendations, not a wall of text.

HARD BUDGET: at most **6 tool calls per task** across all 7 tools
combined. The taxonomy + clusters are small — one well-chosen CSV
query usually answers a structured question, one RAG query usually
answers a semantic one. If you're past 6 calls without an answer,
write your final answer with what you have.
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
        tools=[skills_rag_tool, *CSV_TOOLS, *LIFT_TOOLS, *COMPOSE_TOOLS],
        llm=get_llm(),
        verbose=False,
        allow_delegation=False,
        # Framework-level hard cap. 7 tools available but most questions
        # need only 1-2 well-chosen calls. 10 iterations leaves headroom
        # for retries while preventing runaway loops on Sonnet.
        max_iter=10,
        # 2026-09-04 hardening: CrewAI's default max_retry_limit=2 means
        # ANY exception (regardless of cause) re-invokes execute_task()
        # from scratch up to 2 more times — for a delegating/tool-using
        # agent that's the full tool loop re-run each time, 3x cost in
        # the worst case. CrewAI has zero visibility into WHY a task
        # failed (see crewai/agent/core.py's _check_execution_error — it
        # only special-cases litellm exceptions and ToolExecutionFailedError,
        # neither of which a Gemini quota/rate-limit error is), so it
        # can't itself skip retrying a known-permanent failure like a
        # daily quota cap. Lowered to 1 as a bounded backstop for genuine
        # transient issues outside the LLM-call layer (network blips,
        # parsing errors) — the LLM-call-level retry/fail-fast decision
        # itself now lives in gemini_retry.RetryAwareGeminiCompletion,
        # which IS reason-aware (see llm.py's gemini branch).
        max_retry_limit=1,
    )
