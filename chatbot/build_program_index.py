"""
build_program_index.py — Build a FAISS index over hand-curated university
program/curriculum files.

Reads:  chatbot/data/program_and_curriculum/*.txt (except TEMPLATE.txt)
Writes: chatbot/faiss_program_index/{index.faiss, index.pkl}

Run after adding or editing a program file:
    python chatbot/build_program_index.py

Uses the shared chatbot/embeddings.py factory (same model as the skills
and news indices) — per CLAUDE.md Critical Rule #7, build-time and
query-time embeddings MUST match.

Each program file becomes one document (chunked only if long); metadata
carries the program name, source URL(s), and last-verified date so the
RAG tool can cite them directly without re-parsing the file at query time.

This corpus is expected to be small (a handful to a few dozen programs)
and is grown by hand — see data/program_and_curriculum/README.md. It is
normal for this script to find zero files early on; it exits cleanly
(not an error) in that case so the University AI Programs Researcher
simply falls back to web search until files are added.
"""

import glob
import os
import re
import sys

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRAM_DIR = os.path.join(BASE_DIR, "data", "program_and_curriculum")
INDEX_DIR = os.path.join(BASE_DIR, "faiss_program_index")
TEMPLATE_NAME = "TEMPLATE.txt"

# Program files are short hand-curated docs (typically a few hundred to a
# couple thousand chars). 1000/100 matches the news index's tuning and
# keeps a course list from being split mid-bullet in the common case.
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

_FIELD_PATTERNS = {
    "program": re.compile(r"^\*\*Program:\*\*\s*(.+)$", re.MULTILINE),
    "source_urls": re.compile(r"^\*\*Source URL\(s\):\*\*\s*(.+)$", re.MULTILINE),
    "last_verified": re.compile(r"^\*\*Last Verified:\*\*\s*(.+)$", re.MULTILINE),
}


def find_program_files(program_dir: str = PROGRAM_DIR) -> list[str]:
    pattern = os.path.join(program_dir, "*.txt")
    files = sorted(glob.glob(pattern))
    return [f for f in files if os.path.basename(f) != TEMPLATE_NAME]


def parse_program_file(path: str) -> tuple[str, dict]:
    """Returns (body_text, metadata).

    body_text excludes the optional "HOW TO FILL THIS OUT" instructions
    block in case a contributor forgot to delete it before saving — that
    block always starts with a line that is exactly "---" in TEMPLATE.txt.
    """
    with open(path, encoding="utf-8") as f:
        raw = f.read()

    body = raw.split("\n---", 1)[0].strip()

    meta = {"file": os.path.basename(path)}
    for key, pattern in _FIELD_PATTERNS.items():
        m = pattern.search(raw)
        value = m.group(1).strip() if m else ""
        # Guard against an unfilled placeholder like "[Full program name...]"
        # slipping into the index as if it were real metadata.
        if value.startswith("[") and value.endswith("]"):
            value = "(not filled in)"
        meta[key] = value

    return body, meta


def build_documents(files: list[str]) -> tuple[list[str], list[dict]]:
    texts: list[str] = []
    metadatas: list[dict] = []
    for path in files:
        body, meta = parse_program_file(path)
        if not body:
            print(f"  Skipping {meta['file']} — empty after parsing.")
            continue
        texts.append(body)
        metadatas.append(meta)
    return texts, metadatas


def chunk(texts: list[str], metadatas: list[dict]) -> tuple[list[str], list[dict]]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunked_texts: list[str] = []
    chunked_meta: list[dict] = []
    for text, meta in zip(texts, metadatas):
        pieces = splitter.split_text(text)
        for p in pieces:
            chunked_texts.append(p)
            chunked_meta.append(meta)
    return chunked_texts, chunked_meta


def main():
    print("=== Building FAISS index for university programs/curricula ===\n")
    files = find_program_files()

    if not files:
        print(f"No program files found in: {PROGRAM_DIR}/")
        print("(Only TEMPLATE.txt exists, or the directory is empty.)")
        print("This is expected until real program files are added — the")
        print("University AI Programs Researcher will simply fall back to")
        print("web search until then. Nothing to build; exiting cleanly.")
        return

    print(f"Found {len(files)} program file(s):")
    for f in files:
        print(f"  - {os.path.basename(f)}")

    print("\nParsing program files...")
    texts, metadatas = build_documents(files)
    if not texts:
        print("\nAll program files were empty after parsing — nothing to index.")
        return
    print(f"  {len(texts)} program file(s) → {len(texts)} pre-chunk documents.")

    print("\nChunking...")
    texts, metadatas = chunk(texts, metadatas)
    print(f"  Produced {len(texts)} chunks (chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}).")

    # Import the shared embeddings factory — same source of truth as the
    # skills and news indices (Critical Rule #7).
    from embeddings import get_embeddings, describe_embeddings_config

    print(f"\nUsing {describe_embeddings_config()}")
    try:
        embeddings = get_embeddings()
    except (ImportError, RuntimeError, ValueError) as e:
        sys.exit(f"ERROR: {e}")
    print(f"Embedding {len(texts)} text chunks...")

    vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)

    os.makedirs(INDEX_DIR, exist_ok=True)
    vectorstore.save_local(INDEX_DIR)
    print(f"\nFAISS program index saved to: {INDEX_DIR}/")
    print("Next: chatbot/tools/program_rag_tool.py reads this index at query time.")


if __name__ == "__main__":
    main()
