"""
add_to_faiss_index.py — append the documents in documents/ to an existing
LangChain FAISS index (skills/taxonomy index) in place.

Does NOT rebuild or replace the index. Uses add_texts()/add_documents(),
which appends new vectors to whatever's already there. Your existing V1
taxonomy content, news, and program entries are untouched.

Assumes the same embedding model your existing skills index was built
with (per the chatbot technical log: Ollama `mxbai-embed-large`, local).
If that's changed since the log was written, update EMBEDDING_MODEL below
— using a different embedding model than the rest of the index will
silently corrupt the similarity space (new vectors and old vectors won't
be comparable), so this is the one thing worth double-checking before you
run this.

Usage:
    python add_to_faiss_index.py --index-path /path/to/your/faiss_index

Requires: langchain, langchain-community, faiss-cpu, ollama running
locally with mxbai-embed-large pulled.
"""

import argparse
import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

EMBEDDING_MODEL = "mxbai-embed-large"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

HERE = Path(__file__).parent
DOCS_DIR = HERE / "documents"


def load_jsonl_docs(path: Path) -> list[Document]:
    """Skill-taxonomy docs are already short and one-fact-per-doc — no
    chunking needed, just load as-is."""
    docs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            docs.append(Document(page_content=row["text"], metadata=row["metadata"]))
    return docs


def load_markdown_doc(path: Path, splitter: RecursiveCharacterTextSplitter) -> list[Document]:
    """Prose summary docs have a YAML-ish frontmatter block (--- ... ---)
    followed by the body. Parse the frontmatter into metadata, chunk the
    body with the same splitter config used elsewhere in this project,
    and attach the frontmatter metadata to every resulting chunk."""
    raw = path.read_text(encoding="utf-8")
    metadata = {}
    body = raw
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            frontmatter = raw[3:end].strip()
            body = raw[end + 4:].strip()
            for line in frontmatter.splitlines():
                if ":" in line:
                    key, _, val = line.partition(":")
                    metadata[key.strip()] = val.strip()

    chunks = splitter.split_text(body)
    return [
        Document(page_content=chunk, metadata={**metadata, "source_file": path.name})
        for chunk in chunks
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--index-path",
        required=True,
        help="Path to your existing skills FAISS index directory (the one "
        "you already have, built by build_index.py). This script loads it, "
        "adds the new documents, and saves it back to the SAME path.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Load and chunk documents, print a summary, but don't touch the index.",
    )
    args = parser.parse_args()

    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )

    all_docs: list[Document] = []

    jsonl_path = DOCS_DIR / "v2_taxonomy_skills.jsonl"
    skill_docs = load_jsonl_docs(jsonl_path)
    print(f"Loaded {len(skill_docs)} V2 taxonomy skill documents (unchunked).")
    all_docs.extend(skill_docs)

    for md_file in sorted(DOCS_DIR.glob("*.md")):
        chunks = load_markdown_doc(md_file, splitter)
        print(f"Loaded {md_file.name}: {len(chunks)} chunks.")
        all_docs.extend(chunks)

    print(f"\nTotal new documents to add: {len(all_docs)}")

    if args.dry_run:
        print("\n--dry-run set, stopping before touching the index.")
        print("Sample document:\n", all_docs[0].page_content[:300])
        print("Sample metadata:\n", all_docs[0].metadata)
        return

    print(f"\nLoading existing index from {args.index_path} ...")
    index = FAISS.load_local(
        args.index_path, embeddings, allow_dangerous_deserialization=True
    )
    print(f"Existing index size before add: {index.index.ntotal} vectors.")

    index.add_documents(all_docs)

    print(f"Index size after add: {index.index.ntotal} vectors.")
    index.save_local(args.index_path)
    print(f"Saved back to {args.index_path}.")


if __name__ == "__main__":
    main()
