"""
build_index.py — One-time script to build the FAISS vector index from the skills taxonomy.

Run this once before starting the chatbot:
    python build_index.py

Reads:  data/Grouped_Skills_Categorized_Updated.xlsx  (4,824 rows × 7 cols)
        data/clust_ensembled_results.csv               (optional — adds cluster labels)
Writes: faiss_index/index.faiss
        faiss_index/index.pkl
"""

import os
import sys
import pandas as pd
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

load_dotenv()

# Embedding provider — "ollama" (local, default) or "openai".
# The same provider/model must be used at query time by the RAG tool.
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "ollama").lower()
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")

# ── paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
INDEX_DIR = os.path.join(BASE_DIR, "faiss_index")

SKILLS_FILE = os.path.join(DATA_DIR, "Grouped_Skills_Categorized_Updated.xlsx")
CLUSTER_FILE = os.path.join(DATA_DIR, "clust_ensembled_results.csv")

EXPECTED_COLUMNS = {
    "Skills", "Alternate Spellings", "Date",
    "Level 1 Category", "Level 2 Category", "Description", "Frequency"
}


def load_skills(path: str) -> pd.DataFrame:
    print(f"Loading skills taxonomy from: {path}")
    if not os.path.exists(path):
        sys.exit(
            f"ERROR: Skills file not found at {path}\n"
            "Copy or symlink Grouped_Skills_Categorized_Updated.xlsx into chatbot/data/"
        )
    df = pd.read_excel(path)
    missing = EXPECTED_COLUMNS - set(df.columns)
    if missing:
        sys.exit(f"ERROR: Missing columns in skills file: {missing}")
    print(f"  Loaded {len(df):,} rows, {df['Alternate Spellings'].nunique():,} canonical skill groups.")
    return df


def load_cluster_map(path: str) -> dict[str, int]:
    """Returns {skill_name_lower: cluster_id} if the file exists, else {}."""
    if not os.path.exists(path):
        print(f"  Cluster file not found ({path}) — skipping cluster labels.")
        return {}
    clusters = pd.read_csv(path)
    if "Cluster" not in clusters.columns or "Skill" not in clusters.columns:
        print("  Cluster file missing expected columns (Cluster, Skill) — skipping.")
        return {}
    mapping = {row["Skill"].strip().lower(): int(row["Cluster"]) for _, row in clusters.iterrows()}
    print(f"  Loaded cluster labels for {len(mapping):,} skills.")
    return mapping


CLUSTER_THEMES = {
    1: "General / Mixed",
    2: "General / Mixed",
    3: "General / Mixed",
    4: "Cloud & Database Infrastructure",
    5: "Soft Skills & Business",
    6: "General / Mixed",
    7: "Core ML, Statistics & Programming",
    8: "Data Engineering (Spark / Kafka / Docker)",
    9: "Analytical & BI Tools",
    10: "Large Mixed Group",
}


def build_documents(df: pd.DataFrame, cluster_map: dict) -> list[dict]:
    """
    Group rows by Alternate Spellings (canonical skill group) and build one
    rich text document per group.  Returns a list of {page_content, metadata} dicts.
    """
    documents = []

    for canonical_group, group in df.groupby("Alternate Spellings", sort=False):
        # Collect variant names
        variants = group["Skills"].dropna().unique().tolist()
        canonical_name = str(canonical_group).strip()

        # Aggregate fields (take first non-null value for categorical fields)
        level1 = group["Level 1 Category"].dropna().iloc[0] if group["Level 1 Category"].notna().any() else "Unknown"
        level2 = group["Level 2 Category"].dropna().iloc[0] if group["Level 2 Category"].notna().any() else "Unknown"
        description = group["Description"].dropna().iloc[0] if group["Description"].notna().any() else ""
        dates = sorted(group["Date"].dropna().unique().tolist())
        total_freq = int(group["Frequency"].fillna(0).sum())

        # Look up cluster for the canonical name
        cluster_id = cluster_map.get(canonical_name.lower())
        cluster_theme = CLUSTER_THEMES.get(cluster_id, "Unknown") if cluster_id is not None else "Unknown"

        # Build the text representation
        lines = [
            f"Skill: {canonical_name}",
        ]
        if len(variants) > 1:
            other_variants = [v for v in variants if v.strip().lower() != canonical_name.lower()]
            if other_variants:
                lines.append(f"Also known as: {', '.join(other_variants)}")
        lines += [
            f"Category: {level1} > {level2}",
            f"Frequency in job postings: {total_freq}",
        ]
        if dates:
            lines.append(f"Observed in datasets: {', '.join(str(d) for d in dates)}")
        if cluster_id is not None:
            lines.append(f"Skill cluster: {cluster_id} — {cluster_theme}")
        if description:
            lines.append(f"Description: {description}")

        page_content = "\n".join(lines)

        metadata = {
            "skill": canonical_name,
            "level1": str(level1),
            "level2": str(level2),
            "frequency": total_freq,
            "cluster_id": cluster_id if cluster_id is not None else -1,
            "cluster_theme": cluster_theme,
        }

        documents.append({"page_content": page_content, "metadata": metadata})

    return documents


def chunk_documents(raw_docs: list[dict]) -> tuple[list[str], list[dict]]:
    """Split documents that exceed chunk_size; return parallel lists of texts and metadatas."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

    texts, metadatas = [], []
    for doc in raw_docs:
        chunks = splitter.split_text(doc["page_content"])
        for chunk in chunks:
            texts.append(chunk)
            metadatas.append(doc["metadata"])

    return texts, metadatas


def get_embeddings():
    if EMBEDDING_PROVIDER == "ollama":
        try:
            from langchain_ollama import OllamaEmbeddings
        except ImportError:
            sys.exit(
                "ERROR: langchain-ollama not installed.\n"
                "  pip install langchain-ollama"
            )
        print(f"Using Ollama embeddings: model={OLLAMA_EMBED_MODEL}, host={OLLAMA_BASE_URL}")
        print(f"  (Make sure Ollama is running: `ollama serve` and `ollama pull {OLLAMA_EMBED_MODEL}`)")
        return OllamaEmbeddings(model=OLLAMA_EMBED_MODEL, base_url=OLLAMA_BASE_URL)

    if EMBEDDING_PROVIDER == "openai":
        try:
            from langchain_openai import OpenAIEmbeddings
        except ImportError:
            sys.exit("ERROR: langchain-openai not installed.\n  pip install langchain-openai")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            sys.exit("ERROR: OPENAI_API_KEY not set. Add it to chatbot/.env")
        print(f"Using OpenAI embeddings: model={OPENAI_EMBED_MODEL}")
        return OpenAIEmbeddings(model=OPENAI_EMBED_MODEL, openai_api_key=api_key)

    sys.exit(f"ERROR: Unknown EMBEDDING_PROVIDER={EMBEDDING_PROVIDER!r}. Use 'ollama' or 'openai'.")


def build_faiss_index(texts: list[str], metadatas: list[dict], index_dir: str) -> None:
    embeddings = get_embeddings()
    print(f"Embedding {len(texts):,} text chunks …")

    vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)

    os.makedirs(index_dir, exist_ok=True)
    vectorstore.save_local(index_dir)
    print(f"FAISS index saved to: {index_dir}/")


def main():
    print("=== Building FAISS index for skills taxonomy ===\n")

    df = load_skills(SKILLS_FILE)
    cluster_map = load_cluster_map(CLUSTER_FILE)

    print("\nBuilding documents from skill groups …")
    raw_docs = build_documents(df, cluster_map)
    print(f"  Created {len(raw_docs):,} skill group documents.")

    print("\nChunking documents …")
    texts, metadatas = chunk_documents(raw_docs)
    print(f"  Produced {len(texts):,} chunks (chunk_size=800, overlap=100).")

    print()
    build_faiss_index(texts, metadatas, INDEX_DIR)

    print("\nDone. Run the chatbot with: chainlit run main.py")


if __name__ == "__main__":
    main()
