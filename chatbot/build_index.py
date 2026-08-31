"""
build_index.py — Build the FAISS vector index from the skills taxonomy.

Run once before starting the chatbot (and re-run if the taxonomy or FOR_CASSIE
documents change):
    python build_index.py

Reads:  data/Grouped_Skills_Categorized_Updated.xlsx        (4,824 rows × 7 cols, V1 taxonomy)
        data/clust_ensembled_results.csv                    (optional — adds V1 cluster labels)
        ../FOR_CASSIE/01_FAISS_ADDITIONS/documents/*.jsonl  (1,058 V2 taxonomy skill docs)
        ../FOR_CASSIE/01_FAISS_ADDITIONS/documents/*.md     (4 prose summary docs)
Writes: faiss_index/index.faiss
        faiss_index/index.pkl

The FOR_CASSIE documents are appended to the V1 taxonomy content. V2 skill docs
are tagged taxonomy_version=V2, status=current in their metadata so the Analyst
agent can prefer them over untagged V1 entries when both surface for the same skill.
If the FOR_CASSIE directory is missing, the build proceeds with V1 content only
(graceful degradation — not an error).
"""

import json
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
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(BASE_DIR, "data")
INDEX_DIR   = os.path.join(BASE_DIR, "faiss_index")
PROJECT_ROOT = os.path.dirname(BASE_DIR)

SKILLS_FILE  = os.path.join(DATA_DIR, "Grouped_Skills_Categorized_Updated.xlsx")
CLUSTER_FILE = os.path.join(DATA_DIR, "clust_ensembled_results.csv")

# FOR_CASSIE additions — V2 taxonomy JSONL + 4 prose summary markdown files.
# Path is relative to the project root (one level above chatbot/).
FOR_CASSIE_DOCS_DIR = os.path.join(
    PROJECT_ROOT, "FOR_CASSIE", "01_FAISS_ADDITIONS", "documents"
)

EXPECTED_COLUMNS = {
    "Skills", "Alternate Spellings", "Date (2024 or 2025)",
    "Level 1 Category", "Level 2 Category", "Description", "Frequency"
}

# Chunk-size hoisted so the eval script can record which config a baseline ran
# against. Wider than the longest skill doc (p99 ≈ 1.1k chars, max ≈ 1.9k) so
# each canonical-skill document fits in one chunk.
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 0


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
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

    texts, metadatas = [], []
    for doc in raw_docs:
        chunks = splitter.split_text(doc["page_content"])
        for chunk in chunks:
            texts.append(chunk)
            metadatas.append(doc["metadata"])

    return texts, metadatas


def load_for_cassie_documents() -> tuple[list[str], list[dict]]:
    """Load V2 taxonomy skills + prose summaries from FOR_CASSIE/01_FAISS_ADDITIONS/documents/.

    Returns parallel (texts, metadatas) lists ready to append to the index.
    Gracefully skips if the directory or individual files are missing — the
    build still succeeds with V1-only content in that case.

    Documents loaded:
      v2_taxonomy_skills.jsonl — 1,058 V2 skill docs (unchunked; already short).
                                  Each tagged taxonomy_version=V2, status=current.
      *.md files               — 4 prose summaries (trend analysis, salary/education,
                                  clustering stability, source mix caveat).
                                  Chunked at 800 chars / 100 overlap to stay
                                  compatible with the RAG retriever's window.
    """
    if not os.path.isdir(FOR_CASSIE_DOCS_DIR):
        print(f"  FOR_CASSIE docs dir not found ({FOR_CASSIE_DOCS_DIR}) — skipping.")
        return [], []

    texts: list[str] = []
    metadatas: list[dict] = []

    # ── 1. JSONL: one V2 skill doc per line, already short — no chunking needed ──
    jsonl_path = os.path.join(FOR_CASSIE_DOCS_DIR, "v2_taxonomy_skills.jsonl")
    if os.path.exists(jsonl_path):
        skill_count = 0
        with open(jsonl_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                doc = json.loads(line)
                texts.append(doc["text"])
                metadatas.append(doc["metadata"])
                skill_count += 1
        print(f"  FOR_CASSIE JSONL: {skill_count} V2 skill documents loaded.")
    else:
        print(f"  FOR_CASSIE JSONL not found — skipping V2 skill docs.")

    # ── 2. Markdown prose summaries (chunked) ──────────────────────────────────
    md_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    for md_file in sorted(os.listdir(FOR_CASSIE_DOCS_DIR)):
        if not md_file.endswith(".md"):
            continue
        md_path = os.path.join(FOR_CASSIE_DOCS_DIR, md_file)
        raw = open(md_path, encoding="utf-8").read()

        # Parse YAML-ish frontmatter (--- key: value --- block at top of file)
        meta: dict = {"source_file": md_file}
        body = raw
        if raw.startswith("---"):
            end = raw.find("\n---", 3)
            if end != -1:
                for line in raw[3:end].strip().splitlines():
                    if ":" in line:
                        k, _, v = line.partition(":")
                        meta[k.strip()] = v.strip()
                body = raw[end + 4:].strip()

        chunks = md_splitter.split_text(body)
        for chunk in chunks:
            texts.append(chunk)
            metadatas.append({**meta, "doc_type": meta.get("doc_type", "summary")})
        print(f"  FOR_CASSIE MD: {md_file} → {len(chunks)} chunks.")

    return texts, metadatas


EMBED_BATCH_SIZE = 150  # Ollama can OOM/EOF if sent too many texts at once


def build_faiss_index(texts: list[str], metadatas: list[dict], index_dir: str) -> None:
    print(f"Using {describe_embeddings_config()}")
    try:
        embeddings = get_embeddings()
    except (ImportError, RuntimeError, ValueError) as e:
        sys.exit(f"ERROR: {e}")
    print(f"Embedding {len(texts):,} text chunks in batches of {EMBED_BATCH_SIZE} …")

    # Build the vectorstore from the first batch, then add subsequent batches.
    # Sending all texts at once to Ollama causes a 400/EOF error on large inputs.
    vectorstore = FAISS.from_texts(
        texts[:EMBED_BATCH_SIZE],
        embeddings,
        metadatas=metadatas[:EMBED_BATCH_SIZE],
    )
    print(f"  Batch 1/{-(-len(texts) // EMBED_BATCH_SIZE)}: "
          f"{min(EMBED_BATCH_SIZE, len(texts))}/{len(texts)} done.")

    for batch_start in range(EMBED_BATCH_SIZE, len(texts), EMBED_BATCH_SIZE):
        batch_end = min(batch_start + EMBED_BATCH_SIZE, len(texts))
        vectorstore.add_texts(
            texts[batch_start:batch_end],
            metadatas=metadatas[batch_start:batch_end],
        )
        batch_num = batch_start // EMBED_BATCH_SIZE + 1
        total_batches = -(-len(texts) // EMBED_BATCH_SIZE)
        print(f"  Batch {batch_num}/{total_batches}: {batch_end}/{len(texts)} done.")

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
    print(f"  V1 taxonomy: {len(texts):,} chunks (chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}).")

    print("\nLoading FOR_CASSIE V2 taxonomy + prose summaries …")
    fc_texts, fc_metadatas = load_for_cassie_documents()
    if fc_texts:
        texts.extend(fc_texts)
        metadatas.extend(fc_metadatas)
        print(f"  Total after FOR_CASSIE additions: {len(texts):,} chunks.")
    else:
        print("  No FOR_CASSIE documents added (directory missing or empty).")

    print()
    build_faiss_index(texts, metadatas, INDEX_DIR)

    print("\nDone. Run the chatbot with: chainlit run app.py")


if __name__ == "__main__":
    main()
