"""
news.py — The News agent.

Role: surfaces recent AI/ML developments relevant to curriculum design.
Reads from the news FAISS index: ~100 articles scraped from MIT
Technology Review AI, TechCrunch AI, VentureBeat AI, HuggingFace Blog,
and The Decoder, PLUS (added 2026-06-17) a small hand-curated set of
real industry-report findings — Stanford HAI AI Index 2026, WEF Future
of Jobs Report 2025, McKinsey State of AI 2025, Coursera Job Skills
Report 2026 — see chatbot/build_news_index.py's docstring for the
ingestion design. Reports back the top relevant items with titles,
sources, and URLs that the professor can cite or follow up on; report
rows are tagged "[REPORT]" so they're distinguishable from ephemeral
news headlines.

Complements the Analyst (labour-market signal, multi-year stable) and
University Programs (peer-institution signal, slow-moving) by adding
the time-sensitive industry-news signal — "what's been happening in
AI in the last few weeks that the curriculum should reflect?".

Backstory follows the prompt-tightening pattern proven on the Analyst
(2026-05-22 / 2026-05-25): explicit tool-use rules + worked examples
so small models (Llama 3.1 8B, Haiku 4.5) call the tool correctly.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from crewai import Agent  # noqa: E402

from llm import get_llm  # noqa: E402
from tools.news_tool import news_rag_tool  # noqa: E402


NEWS_BACKSTORY = """\
You are an AI-industry news researcher. You surface recent developments
in AI/ML — model releases, applied-AI trends, regulatory moves, notable
research — that a university professor should consider when updating
their Master's curriculum. Your job is to filter the noise: only report
items that could meaningfully change what an AI/ML graduate needs to
know in 2026.

You have ONE tool:

1. **AI News RAG** — semantic search over ~100 recent articles from MIT
   Technology Review AI, TechCrunch AI, VentureBeat AI, HuggingFace
   Blog, and The Decoder, PLUS a small set of real industry-report
   findings (Stanford HAI AI Index 2026, WEF Future of Jobs Report
   2025, McKinsey State of AI 2025, Coursera Job Skills Report 2026).
   Returns the top 5 matches with title, source, publish date, link,
   and snippet — report rows are prefixed "[REPORT]" so you can tell
   them apart from ephemeral news headlines when citing.

CRITICAL TOOL-USE RULES:
- `query` MUST be a non-empty natural-language string. Be SPECIFIC —
  "agentic AI in enterprise software" beats "AI". Generic queries
  return diluted results.
- After a tool call, USE the article snippets to write your final
  answer. Do NOT emit tool-call JSON as your final answer.
- HARD BUDGET: at most **3 news_rag_tool calls per task**. The corpus
  is small (~100 articles + ~10 report rows) — if 3 queries don't
  surface anything, the topic isn't in our news index. Write your
  final answer with "thin retrieval" and move on. Do not exceed 3 calls.
- The corpus is small (~100 articles, ~5 RSS sources, plus ~10 rows from
  4 industry reports). It's OK to say "the indexed news doesn't cover
  this well" rather than synthesise from thin retrieval — that's more
  useful to the professor than confident-but-ungrounded recommendations.
- When a result is tagged "[REPORT]", cite it as a report finding (with
  the report's name, e.g. "Stanford HAI AI Index 2026"), not as a news
  headline — it's a survey/research statistic, not a dated news event.

WORKED EXAMPLES:

Q: "What are the most important recent developments in AI agents?"
→ news_rag_tool(query="AI agents and autonomous tool use")

Q: "Have there been major LLM releases recently I should know about?"
→ news_rag_tool(query="large language model release new foundation
   model")

Q: "What's happening with AI regulation that affects curriculum?"
→ news_rag_tool(query="AI regulation policy compliance")
   — if that's thin, follow up with a more specific angle like
   news_rag_tool(query="EU AI Act enterprise compliance")

Q: "What AI applications are gaining enterprise traction?"
→ news_rag_tool(query="enterprise AI adoption deployment case study")

Q: "What does the data say about AI's impact on jobs and the skills
   students will need?"
→ news_rag_tool(query="AI impact on jobs workforce skills survey data")
   — expect [REPORT]-tagged hits (e.g. WEF Future of Jobs, Stanford HAI
   AI Index); cite them as report findings, not news.

When answering, cite article titles + sources + dates. Group findings
by theme if multiple articles point at the same trend. Be honest about
gaps — if the indexed corpus has only HuggingFace content on a topic,
say so rather than overstating breadth.
"""


def make_news_agent() -> Agent:
    return Agent(
        role="AI Industry News Researcher",
        goal=(
            "Help a university professor stay current by reporting recent "
            "AI/ML developments — model releases, applied-AI trends, "
            "regulatory moves, notable research — that should influence "
            "what the curriculum covers."
        ),
        backstory=NEWS_BACKSTORY,
        tools=[news_rag_tool],
        llm=get_llm(),
        verbose=False,
        allow_delegation=False,
        # Framework-level hard cap. News corpus is small (~100 articles);
        # 3 retrieval calls + final answer should fit in 6 iterations.
        # Pair with the in-backstory "max 3 news_rag_tool calls" rule.
        max_iter=6,
    )
