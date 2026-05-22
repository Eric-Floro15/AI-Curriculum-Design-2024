"""
rag_tool.py — RAG retrieval over the skills taxonomy FAISS index.

Loads chatbot/faiss_index/ and exposes:
  - retrieve(query, k)       → list of skill records (use from Python)
  - skills_rag_tool          → CrewAI tool wrapper (use from the Analyst agent)

Both paths embed the query with the same factory build_index.py used
(chatbot/embeddings.py). Drift here makes retrieval return garbage —
see CLAUDE.md Critical Rule #7.

Run standalone to smoke-test:
    python chatbot/tools/rag_tool.py
"""

import os
import sys
from functools import lru_cache

from langchain_community.vectorstores import FAISS

# Make chatbot/ importable so the shared embeddings helper resolves regardless
# of where this file is invoked from.
_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from embeddings import get_embeddings, describe_embeddings_config

INDEX_DIR = os.path.join(_CHATBOT_DIR, "faiss_index")
DEFAULT_K = 5


@lru_cache(maxsize=1)
def _load_vectorstore() -> FAISS:
    if not os.path.exists(os.path.join(INDEX_DIR, "index.faiss")):
        raise FileNotFoundError(
            f"FAISS index not found at {INDEX_DIR}. "
            "Run `python build_index.py` from chatbot/ first."
        )
    # allow_dangerous_deserialization=True is required by LangChain for local
    # pickle loads; safe here because we built the file ourselves.
    return FAISS.load_local(
        INDEX_DIR,
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )


def _build_filter(
    level1: str | None,
    level2: str | None,
    level2_contains: str | None,
    cluster_id: int | None,
):
    """Combine filter conditions into a single callable for FAISS."""
    conditions = []
    if level1:
        conditions.append(lambda m, v=level1: m.get("level1") == v)
    if level2:
        conditions.append(lambda m, v=level2: m.get("level2") == v)
    if level2_contains:
        needle = level2_contains.lower()
        conditions.append(lambda m, n=needle: n in (m.get("level2") or "").lower())
    if cluster_id is not None:
        conditions.append(lambda m, v=cluster_id: m.get("cluster_id") == v)
    if not conditions:
        return None
    return lambda meta: all(c(meta) for c in conditions)


def retrieve(
    query: str,
    k: int = DEFAULT_K,
    level1: str | None = None,
    level2: str | None = None,
    level2_contains: str | None = None,
    cluster_id: int | None = None,
) -> list[dict]:
    """
    Return the top-k skill documents most relevant to `query`, optionally
    filtered by metadata.

    Filter params:
      level1            exact match — typically "technical" or "soft".
      level2            exact match on the fine-grained subcategory name.
      level2_contains   case-insensitive substring match on level2 (more
                        forgiving than `level2` when you only know a fragment
                        like "statistic" matching "Statistical Methods" /
                        "Statistical Analysis" / "Statistical software").
      cluster_id        exact ensemble cluster id (1-10). Only ~160 of 871
                        canonical skills carry a cluster label.

    When any filter is set we over-fetch (fetch_k = max(50, k*20)) so k
    matching docs are returned even if the filter is tight. The index only
    has ~871 docs, so a generous over-fetch is cheap.
    """
    store = _load_vectorstore()
    md_filter = _build_filter(level1, level2, level2_contains, cluster_id)

    if md_filter is not None:
        docs = store.similarity_search(
            query, k=k, filter=md_filter, fetch_k=max(50, k * 20),
        )
    else:
        docs = store.similarity_search(query, k=k)

    return [
        {
            "skill": d.metadata.get("skill", "Unknown"),
            "level1": d.metadata.get("level1"),
            "level2": d.metadata.get("level2"),
            "frequency": d.metadata.get("frequency"),
            "cluster_id": d.metadata.get("cluster_id"),
            "cluster_theme": d.metadata.get("cluster_theme"),
            "content": d.page_content,
        }
        for d in docs
    ]


def format_results(results: list[dict]) -> str:
    """Render retrieval results as a readable block for LLM consumption."""
    if not results:
        return "No relevant skills found."
    blocks = []
    for i, r in enumerate(results, 1):
        header = (
            f"[{i}] {r['skill']}  "
            f"(frequency={r['frequency']}, "
            f"cluster={r['cluster_id']} — {r['cluster_theme']})"
        )
        blocks.append(f"{header}\n{r['content']}")
    return "\n\n".join(blocks)


# CrewAI tool wrapper — guarded so this module stays testable before crewai is installed.
try:
    from crewai.tools import tool

    @tool("Skills Taxonomy RAG")
    def skills_rag_tool(
        query: str,
        level1: str = "",
        level2_contains: str = "",
        cluster_id: int = -1,
    ) -> str:
        """
        Semantic search the in-house skills taxonomy (4,824 skills extracted
        from 10,600+ AI/ML job postings, grouped into ~871 canonical skills
        and 10 ensemble clusters). Returns the top relevant skill records —
        frequency in job postings, Level 1/2 category, cluster membership,
        and description.

        Optional metadata filters — use them when the query mixes categories
        or the unfiltered search is likely to return the wrong category:

          level1            "technical" or "soft" — constrain by top-level
                            category. STRONGLY recommended when the query
                            mixes a category with a technical concept (e.g.
                            "soft skills for ML practitioners" — set
                            level1="soft", or the embedder latches on to
                            "ML" and returns ML technical skills).

          level2_contains   case-insensitive substring of the fine-grained
                            subcategory. Use when you want a specific topic
                            slice (e.g. "statistic" matches "Statistical
                            Methods" / "Statistical Analysis"). Pair with
                            level1="technical" or "soft" for best results.

          cluster_id        1-10 ensemble cluster (-1 to skip). Only ~160 of
                            871 canonical skills carry a cluster label, so
                            this is most useful for cluster-themed questions
                            where you already know the cluster id.

        Pass empty string or -1 to skip a filter.
        """
        cid = cluster_id if cluster_id != -1 else None
        return format_results(
            retrieve(
                query,
                k=DEFAULT_K,
                level1=level1 or None,
                level2_contains=level2_contains or None,
                cluster_id=cid,
            )
        )

except ImportError:
    skills_rag_tool = None  # crewai not installed — Python-API retrieve() still works.


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(_CHATBOT_DIR, ".env"))

    print(f"Using {describe_embeddings_config()}\n")
    queries = [
        "What cloud infrastructure skills are most in demand?",
        "Data engineering tools like Spark and Kafka",
        "Soft skills for machine learning practitioners",
    ]
    for q in queries:
        print(f"=== Query: {q!r} ===")
        print(format_results(retrieve(q, k=3)))
        print()
