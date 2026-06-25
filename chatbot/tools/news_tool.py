"""
news_tool.py — RAG retrieval over the news article FAISS index.

Loads chatbot/faiss_news_index/ and exposes:
  - retrieve(query, k)   → list of news article records (Python API)
  - news_rag_tool        → CrewAI tool wrapper (used by the News agent)

Mirrors tools/rag_tool.py but over the news index. Simpler than the
skills RAG — no metadata filtering, no BM25 hybrid; news retrieval is
pure semantic, plus a title-based per-source dedup (added 2026-06-17 → 06-22,
see retrieve()'s docstring) so one long article's many chunks can't crowd
out everything else in the top-k. Add further complexity only if eval
shows it's needed.

The index mixes two corpora as of 2026-06-17: auto-fetched RSS news
articles (doc_type="news_article") and a small hand-curated set of
real industry-report findings (doc_type="industry_report" — Stanford
HAI AI Index 2026, WEF Future of Jobs 2025, McKinsey State of AI 2025,
Coursera Job Skills Report 2026; see build_news_index.py's docstring
for the ingestion design). retrieve() surfaces doc_type per result and
format_results() tags report rows with "[REPORT]" so the agent and the
professor can tell the two apart in a result set.

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
    """Return the top-k news/report chunks most relevant to `query`,
    deduplicated by source title so one long article's chunks can't crowd
    out everything else.

    Dedup rationale (added 2026-06-22): a live agent-level test
    (chatbot/agents/test_news_industry_reports.py) caught a real case
    where a single long RSS article's chunks dominated a raw top-5 —
    VentureBeat embeds full article HTML (~14k chars per CLAUDE.md), which
    build_news_index.py's chunk() splits at CHUNK_SIZE=1000, so one
    article can yield a dozen+ chunks all carrying that article's
    metadata. Plain similarity_search() has no notion that 5 different
    *chunks* can be the same *source* — for one query, all 5 raw results
    were chunks of one VentureBeat article, crowding out an
    actually-relevant industry_report chunk that should have been in the
    result set.

    Dedup key is `title`, deliberately NOT `link` — checked
    chatbot/data/news/industry_reports_2026-06-17.csv before picking this:
    multiple real report FINDINGS from the same report legitimately share
    one `link` (e.g. all 3 WEF Future-of-Jobs rows point at the same
    digest URL; both McKinsey State-of-AI rows point at the same survey
    URL) but have distinct titles per finding. Deduping by `link` would
    have silently collapsed those down to one finding per report. `title`
    is the field that's actually unique per distinct piece of content and
    identical only across chunks of the literal same source row/article
    (chunk() copies one row's metadata, title included, onto every chunk
    of that row).
    """
    store = _load_vectorstore()
    # Over-fetch candidates so dedup can backfill past duplicate-source
    # chunks instead of just truncating the original top-k down further —
    # without this, dedup would just return fewer than k results whenever
    # the raw top-k contains any duplicate source.
    overfetch_k = max(k * 3, k + 10)
    candidates = store.similarity_search(query, k=overfetch_k)

    deduped = []
    seen_keys: set[str] = set()
    for d in candidates:
        # Fall back to link if title is somehow empty, so distinct
        # untitled content doesn't get wrongly collapsed together.
        dedup_key = d.metadata.get("title") or d.metadata.get("link") or ""
        if dedup_key and dedup_key in seen_keys:
            continue
        if dedup_key:
            seen_keys.add(dedup_key)
        deduped.append(d)
        if len(deduped) >= k:
            break

    return [
        {
            "title": d.metadata.get("title", ""),
            "link": d.metadata.get("link", ""),
            "source": d.metadata.get("source", ""),
            "published": d.metadata.get("published", ""),
            # Defaults to "news_article" for pre-2026-06-17 index builds /
            # any chunk whose metadata predates the doc_type field.
            "doc_type": d.metadata.get("doc_type", "news_article"),
            "content": d.page_content,
        }
        for d in deduped
    ]


def format_results(results: list[dict]) -> str:
    """Render retrieval results as a citation-ready block for LLM consumption.

    Industry-report rows are tagged [REPORT] (vs. plain news articles) so the
    agent — and the professor reading its final answer — can tell a
    time-sensitive RSS headline apart from a stable, citable survey/report
    finding when both appear in the same result set.
    """
    if not results:
        return "No relevant news articles found."
    blocks = []
    for i, r in enumerate(results, 1):
        tag = "[REPORT] " if r.get("doc_type") == "industry_report" else ""
        header = f"[{i}] {tag}{r['title']}"
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
        Search the recent AI/ML news corpus: ~100 articles scraped from
        MIT Technology Review AI, TechCrunch AI, VentureBeat AI, HuggingFace
        Blog, and The Decoder, PLUS a small hand-curated set of real
        industry-report findings (Stanford HAI AI Index 2026, WEF Future of
        Jobs Report 2025, McKinsey State of AI 2025, Coursera Job Skills
        Report 2026). Returns the most relevant items with title, source,
        publish date, link, and snippet — report rows are prefixed
        "[REPORT]" in the returned text so they're distinguishable from
        ephemeral news headlines.

        Use this when the professor asks about recent developments, trending
        topics, model releases, or "what's new in AI?" — anything where the
        answer should reflect what happened in the last few weeks/months of
        the industry, not the timeless skills taxonomy. Also use this for
        labor-market / skills-demand questions (e.g. "what does the data say
        about AI's effect on jobs?") — that's exactly what the industry-report
        rows cover, with citable survey statistics rather than news framing.

        Argument:
          query  REQUIRED non-empty natural-language search string. Be
                 specific — "agentic AI in enterprise software" beats just
                 "AI". The retriever works over titles + RSS summaries +
                 report-finding summaries.

        Example:
          - news_rag_tool(query="recent advances in AI agents and tool use")
          - news_rag_tool(query="generative AI for code and software engineering")
          - news_rag_tool(query="AI impact on jobs and workforce skills survey data")
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
