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
import re
import sys
import difflib
import pandas as pd
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from embeddings import get_embeddings, describe_embeddings_config

load_dotenv()

# ── paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
INDEX_DIR = os.path.join(BASE_DIR, "faiss_index")

SKILLS_FILE = os.path.join(DATA_DIR, "Grouped_Skills_Categorized_Updated.xlsx")
CLUSTER_FILE = os.path.join(DATA_DIR, "clust_ensembled_results.csv")

EXPECTED_COLUMNS = {
    "Skills", "Alternate Spellings", "Date (2024 or 2025)",
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


_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")


def _normalize(name: str) -> str:
    """Collapse a skill name to lowercase alphanumerics for matching."""
    return _NORMALIZE_RE.sub("", name.lower())


def build_cluster_map(df: pd.DataFrame, cluster_csv_path: str) -> dict[str, int]:
    """
    Match cluster-CSV skill names to canonical XLSX groups and return
    {canonical_group_lower: cluster_id}.

    The cluster CSV (766 skills) was generated from a different skills file
    than the XLSX we index (4,824 rows / 871 canonical groups), so the names
    don't align exactly. Matching strategy:
      1. Normalized exact match (strip non-alphanumerics, lowercase) against
         the union of XLSX Skills + Alternate Spellings columns.
      2. Fuzzy fallback via difflib with cutoff=0.9 — high enough to avoid
         wrong matches like "Brand Management" -> "Management".
    CSV skills with no confident match are skipped and counted.
    """
    if not os.path.exists(cluster_csv_path):
        print(f"  Cluster file not found ({cluster_csv_path}) — skipping cluster labels.")
        return {}
    clusters = pd.read_csv(cluster_csv_path)
    if "Cluster" not in clusters.columns or "Skill" not in clusters.columns:
        print("  Cluster file missing expected columns (Cluster, Skill) — skipping.")
        return {}

    # Normalized name → canonical-group-lower, from the XLSX taxonomy
    norm_to_canonical: dict[str, str] = {}
    for _, row in df.iterrows():
        canonical = str(row["Alternate Spellings"]).strip().lower()
        for col in ("Skills", "Alternate Spellings"):
            v = row[col]
            if pd.notna(v):
                key = _normalize(str(v))
                if key:
                    norm_to_canonical[key] = canonical

    all_norm_names = list(norm_to_canonical.keys())

    result: dict[str, int] = {}
    exact = fuzzy = miss = 0
    for _, row in clusters.iterrows():
        if pd.isna(row["Skill"]):
            miss += 1
            continue
        key = _normalize(str(row["Skill"]))
        cid = int(row["Cluster"])
        if not key:
            miss += 1
            continue
        if key in norm_to_canonical:
            result[norm_to_canonical[key]] = cid
            exact += 1
            continue
        close = difflib.get_close_matches(key, all_norm_names, n=1, cutoff=0.9)
        if close:
            result[norm_to_canonical[close[0]]] = cid
            fuzzy += 1
        else:
            miss += 1

    total_groups = df["Alternate Spellings"].nunique()
    print(
        f"  Cluster matching: exact={exact}, fuzzy={fuzzy}, unmatched={miss} "
        f"(CSV total={exact + fuzzy + miss})"
    )
    print(f"  Canonical groups labelled: {len(result):,} / {total_groups:,}")
    return result


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
        dates = sorted(group["Date (2024 or 2025)"].dropna().unique().tolist())
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
    """Split documents that exceed chunk_size; return parallel lists of texts and metadatas.

    chunk_size is set wider than the longest skill doc (p99 ≈ 1.1k chars,
    max ≈ 1.9k) so each canonical-skill document stays in one chunk. Splitting
    these short docs was previously stripping the "Skill: X" header off from
    the description.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)

    texts, metadatas = [], []
    for doc in raw_docs:
        chunks = splitter.split_text(doc["page_content"])
        for chunk in chunks:
            texts.append(chunk)
            metadatas.append(doc["metadata"])

    return texts, metadatas


def build_faiss_index(texts: list[str], metadatas: list[dict], index_dir: str) -> None:
    print(f"Using {describe_embeddings_config()}")
    try:
        embeddings = get_embeddings()
    except (ImportError, RuntimeError, ValueError) as e:
        sys.exit(f"ERROR: {e}")
    print(f"Embedding {len(texts):,} text chunks …")

    vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)

    os.makedirs(index_dir, exist_ok=True)
    vectorstore.save_local(index_dir)
    print(f"FAISS index saved to: {index_dir}/")


def main():
    print("=== Building FAISS index for skills taxonomy ===\n")

    df = load_skills(SKILLS_FILE)
    cluster_map = build_cluster_map(df, CLUSTER_FILE)

    print("\nBuilding documents from skill groups …")
    raw_docs = build_documents(df, cluster_map)
    print(f"  Created {len(raw_docs):,} skill group documents.")

    print("\nChunking documents …")
    texts, metadatas = chunk_documents(raw_docs)
    print(f"  Produced {len(texts):,} chunks (chunk_size=2000, overlap=0).")

    print()
    build_faiss_index(texts, metadatas, INDEX_DIR)

    print("\nDone. Run the chatbot with: chainlit run main.py")


if __name__ == "__main__":
    main()
