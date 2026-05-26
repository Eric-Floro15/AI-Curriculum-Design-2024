"""
news_tool.py — RAG retrieval over the news article FAISS index.

Loads chatbot/faiss_news_index/ and exposes:
  - retrieve(query, k)   → list of news article records (Python API)
  - news_rag_tool        → CrewAI tool wrapper (used by the News agent)

Mirrors tools/rag_tool.py but over the news index. Simpler than the
skills RAG — no metadata filtering, no BM25 hybrid; news retrieval is
pure semantic. Add complexity only if eval shows it's needed.

Both build_news_index.py and this module import from the shared
chatbot/embeddings.py helper, per CLAUDE.md Critical Rule #7.

Run standalone to smoke-test:
    KMP_DUPLICATE_LIB_OK=TRUE python chatbot/tools/news_tool.py
"""

import os
import sys
from functools import lru_cache

from langchain_community.vectorstores import FAISS

# Make chatbot/ importable so embeddings.py resolves regardless of cwd.
_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from embeddings import get_embeddings, describe_embeddings_config

INDEX_DIR = os.path.join(_CHATBOT_DIR, "faiss_news_index")
DEFAULT_K = 5


@lru_cache(maxsize=1)
def _load_vectorstore() -> FAISS:
    if not os.path.exists(os.path.join(INDEX_DIR, "index.faiss")):
        raise FileNotFoundError(
            f"News FAISS index not found at {INDEX_DIR}. "
            "Run `python chatbot/fetch_news.py && python chatbot/build_news_index.py` first."
        )
    return FAISS.load_local(
        INDEX_DIR,
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )


def retrieve(query: str, k: int = DEFAULT_K) -> list[dict]:
    """Return the top-k news article chunks most relevant to `query`."""
    store = _load_vectorstore()
    docs = store.similarity_search(query, k=k)
    return [
        {
            "title": d.metadata.get("title", ""),
            "link": d.metadata.get("link", ""),
            "source": d.metadata.get("source", ""),
            "published": d.metadata.get("published", ""),
            "content": d.page_content,
        }
        for d in docs
    ]


def format_results(results: list[dict]) -> str:
    """Render retrieval results as a citation-ready block for LLM consumption."""
    if not results:
        return "No relevant news articles found."
    blocks = []
    for i, r in enumerate(results, 1):
        header = f"[{i}] {r['title']}"
        meta = f"    Source: {r['source']}"
        if r['published']:
            meta += f" — {r['published']}"
        if r['link']:
            meta += f"\n    Link: {r['link']}"
        blocks.append(f"{header}\n{meta}\n    {r['content']}")
    return "\n\n".join(blocks)


# CrewAI tool wrapper — guarded so this module stays testable before crewai is installed.
try:
    from crewai.tools import tool

    @tool("AI News RAG")
    def news_rag_tool(query: str) -> str:
        """
        Search the recent AI/ML news corpus (~100 articles scraped from
        MIT Technology Review AI, TechCrunch AI, VentureBeat AI, HuggingFace
        Blog, and The Decoder). Returns the most relevant articles with
        title, source, publish date, link, and snippet.

        Use this when the professor asks about recent developments, trending
        topics, model releases, or "what's new in AI?" — anything where the
        answer should reflect what happened in the last few weeks of the
        industry, not the timeless skills taxonomy.

        Argument:
          query  REQUIRED non-empty natural-language search string. Be
                 specific — "agentic AI in enterprise software" beats just
                 "AI". The retriever works over titles + RSS summaries.

        Example:
          - news_rag_tool(query="recent advances in AI agents and tool use")
          - news_rag_tool(query="generative AI for code and software engineering")
        """
        return format_results(retrieve(query, k=DEFAULT_K))

except ImportError:
    news_rag_tool = None  # crewai not installed — Python-API retrieve() still works.


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(_CHATBOT_DIR, ".env"))

    print(f"Using {describe_embeddings_config()}\n")
    queries = [
        "AI agents and tool use",
        "large language model releases",
        "AI regulation and policy",
    ]
    for q in queries:
        print(f"=== Query: {q!r} ===")
        print(format_results(retrieve(q, k=3)))
        print()
