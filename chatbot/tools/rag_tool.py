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

from langchain_community.retrievers import BM25Retriever
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


@lru_cache(maxsize=1)
def _load_bm25() -> BM25Retriever:
    """
    Build a BM25 retriever from the same canonical-skill documents that the
    FAISS index uses. BM25 catches exact-token matches (e.g. "Python", "SQL",
    "Spark") that pure vector search misses when the embedder prefers
    conceptual neighbours over literal ones.
    Rebuilt fresh from the source XLSX — fast at 871 docs.
    """
    # Lazy import — build_index.py belongs to chatbot/, not tools/.
    from build_index import (  # noqa: E402
        CLUSTER_FILE,
        SKILLS_FILE,
        build_cluster_map,
        build_documents,
        load_skills,
    )

    df = load_skills(SKILLS_FILE)
    cluster_map = build_cluster_map(df, CLUSTER_FILE)
    raw_docs = build_documents(df, cluster_map)
    return BM25Retriever.from_texts(
        texts=[d["page_content"] for d in raw_docs],
        metadatas=[d["metadata"] for d in raw_docs],
    )


def _rrf_merge(ranked_lists, weights, k: int, c: int = 60):
    """Weighted reciprocal-rank-fusion merge of multiple ranked Document lists.

    Each doc's score is sum over rankings of weight / (c + rank). c=60 is the
    standard constant from the original RRF paper. Weights let one retriever
    dominate — pure-semantic queries usually want FAISS to win unless BM25
    finds a strong lexical match. Returns top-k unique docs; dedup key is
    page_content.
    """
    scores: dict[str, float] = {}
    by_key: dict[str, object] = {}
    for ranking, weight in zip(ranked_lists, weights):
        for rank, doc in enumerate(ranking):
            key = doc.page_content
            scores[key] = scores.get(key, 0.0) + weight / (c + rank)
            by_key[key] = doc
    top_keys = sorted(scores, key=scores.get, reverse=True)[:k]
    return [by_key[k] for k in top_keys]


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

    Hybrid retrieval: results from FAISS (semantic) and BM25 (lexical) are
    combined via Reciprocal Rank Fusion. BM25 catches exact-token matches
    like "Python" / "Spark" / "SQL" that the embedder otherwise misses when
    it prefers conceptual neighbours. The index only has ~871 docs so over-
    fetching from both retrievers is cheap.
    """
    store = _load_vectorstore()
    bm25 = _load_bm25()
    md_filter = _build_filter(level1, level2, level2_contains, cluster_id)

    fetch_n = max(50, k * 20) if md_filter is not None else max(20, k * 4)

    # FAISS path
    if md_filter is not None:
        faiss_docs = store.similarity_search(
            query, k=fetch_n, filter=md_filter, fetch_k=fetch_n * 2,
        )
    else:
        faiss_docs = store.similarity_search(query, k=fetch_n)

    # BM25 path — no native filter, so trim manually after retrieval
    bm25.k = fetch_n
    bm25_docs = bm25.invoke(query)
    if md_filter is not None:
        bm25_docs = [d for d in bm25_docs if md_filter(d.metadata)]

    # FAISS-weighted RRF: BM25 contributes a fraction so it only flips
    # rankings when FAISS is genuinely uncertain (i.e. close scores between
    # neighbours). Tuned via the eval — 0.10 rescues lexical-match queries
    # like "Python" without disturbing the queries FAISS handles well.
    docs = _rrf_merge([faiss_docs, bm25_docs], weights=[1.0, 0.10], k=k)

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

        Argument constraints (MUST be respected — invalid values raise errors):

          query             REQUIRED non-empty string. The natural-language
                            question to search for.

          level1            MUST be one of EXACTLY: "technical", "soft", or ""
                            (empty string to skip). No other values are valid.
                            Do NOT pass "collaboration", "ML", "data", topic
                            names, or anything else — only the three values
                            above. STRONGLY recommended to set this when the
                            query mixes a category with a technical concept
                            (e.g. "soft skills for ML practitioners" — set
                            level1="soft", or the embedder latches on to "ML"
                            and returns ML technical skills).

          level2_contains   case-insensitive substring of the fine-grained
                            subcategory; "" to skip. Use when you want a
                            specific topic slice (e.g. "statistic" matches
                            "Statistical Methods" / "Statistical Analysis").
                            Pair with level1 for best results.

          cluster_id        integer 1-10, or -1 to skip. MUST be an integer,
                            never a string. Do not pass "" — pass -1. Only
                            ~160 of 871 canonical skills carry a cluster
                            label, so this is most useful for cluster-themed
                            questions where you already know the cluster id.

        Examples:
          - "What is BERT?" → skills_rag_tool(query="BERT", level1="",
              level2_contains="", cluster_id=-1)
          - "Soft skills for ML engineers" → skills_rag_tool(query="soft
              skills for ML engineers", level1="soft", level2_contains="",
              cluster_id=-1)
          - "Statistical foundations" → skills_rag_tool(query="statistical
              foundations", level1="technical", level2_contains="statistic",
              cluster_id=-1)
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
