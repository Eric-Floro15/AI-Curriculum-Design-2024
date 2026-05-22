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


def retrieve(query: str, k: int = DEFAULT_K) -> list[dict]:
    """Return the top-k skill documents most relevant to `query`."""
    docs = _load_vectorstore().similarity_search(query, k=k)
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
    def skills_rag_tool(query: str) -> str:
        """
        Search the in-house skills taxonomy (4,824 skills extracted from 10,600+
        AI/ML job postings, grouped into ~870 canonical skills and 10 ensemble
        clusters). Returns the top relevant skill records — frequency in job
        postings, Level 1/2 category, cluster membership, and description.

        Use this for any question about which skills are in demand, how skills
        cluster together, or what a specific skill means in the AI/ML hiring
        context.
        """
        return format_results(retrieve(query, k=DEFAULT_K))

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
