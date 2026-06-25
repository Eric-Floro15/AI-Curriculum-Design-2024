"""
build_news_index.py — Build a FAISS index over the scraped news CSV.

Reads:  chatbot/data/news/news_articles_*.csv   (the most recent file —
        auto-fetched RSS dump, refreshed/replaced wholesale by fetch_news.py)
        chatbot/data/news/industry_reports_*.csv (ALL matching files, merged —
        hand-curated, one-row-per-finding industry reports; see "Industry
        reports corpus" below. Unlike the RSS file, every matching file here
        is loaded, not just the latest, since each is added once and never
        superseded the way a fetch_news.py rerun replaces the RSS CSV.)
Writes: chatbot/faiss_news_index/{index.faiss, index.pkl}

Run after `fetch_news.py`:
    python chatbot/build_news_index.py

Uses the shared chatbot/embeddings.py factory (same model as the skills
index) — per CLAUDE.md Critical Rule #7, build-time and query-time
embeddings MUST match.

Articles are indexed as title + summary in a single chunk each. RSS
summaries are short (typically 1-3 sentences, ~200-500 chars), well
under chunk_size, so chunking is effectively a no-op. If we later add
full-text extraction in fetch_news.py, retune chunk_size/overlap.

Industry reports corpus (added 2026-06-17): a small, hand-curated,
NOT-auto-scraped set of real, citable AI industry reports (Stanford HAI
AI Index 2026, WEF Future of Jobs 2025, McKinsey State of AI 2025,
Coursera Job Skills Report 2026), added per CLAUDE.md's anti-hallucination
posture — each row's content was read directly from the publisher's own
page (or, for the one page that returned no usable text via fetch, from a
search-engine summary directly quoting that same official page) before
being written, the same verification discipline already used for
chatbot/data/program_and_curriculum/. Stored as a SEPARATE CSV
(industry_reports_<date>.csv) rather than appended into the RSS CSV, so a
future `fetch_news.py` rerun (which replaces the RSS CSV wholesale) can
never silently drop this hand-curated content. Rows carry an extra
doc_type="industry_report" column (vs. the RSS rows' implicit
doc_type="news_article" default) so retrieval results can be labeled
distinctly — see tools/news_tool.py.
"""

import csv
import glob
import os
import sys

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEWS_DIR = os.path.join(BASE_DIR, "data", "news")
INDEX_DIR = os.path.join(BASE_DIR, "faiss_news_index")

# Hand-curated industry-report rows live in their own file(s), separate from
# the auto-fetched RSS dump — see module docstring ("Industry reports corpus").
INDUSTRY_REPORTS_PATTERN = "industry_reports_*.csv"

# 1000 char ≈ 250 tokens — safely under mxbai-embed-large's 512-token
# limit. Skills index uses 2000/0 because canonical-skill docs are short
# (p99 ≈ 1.1k chars) and we wanted no splitting; news articles are much
# longer (VentureBeat RSS embeds full HTML, ~14k chars per article) so
# we need real chunking with overlap.
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# Increase the CSV field-size limit — some RSS feeds embed long summaries
# (full first-paragraph quotes etc.) that exceed the default 131,072.
csv.field_size_limit(sys.maxsize)


def latest_news_csv(news_dir: str = NEWS_DIR) -> str:
    pattern = os.path.join(news_dir, "news_articles_*.csv")
    matches = sorted(glob.glob(pattern))
    if not matches:
        sys.exit(
            f"ERROR: No news CSV found at {pattern}\n"
            "Run `python chatbot/fetch_news.py` first."
        )
    return matches[-1]


def load_articles(csv_path: str) -> list[dict]:
    rows: list[dict] = []
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    print(f"Loaded {len(rows)} articles from: {csv_path}")
    return rows


def load_industry_reports(news_dir: str = NEWS_DIR) -> list[dict]:
    """Load and concatenate ALL industry_reports_*.csv files (not just the
    latest — see module docstring). Each file is a small, hand-curated,
    one-row-per-finding extract from a real published report (added per
    CLAUDE.md's anti-hallucination posture). Returns [] with a printed
    notice (not an error/exit) if none exist yet, since this corpus is
    optional and the RSS corpus alone is a valid, complete index.
    """
    pattern = os.path.join(news_dir, INDUSTRY_REPORTS_PATTERN)
    matches = sorted(glob.glob(pattern))
    if not matches:
        print(f"  No industry-report CSVs found at {pattern} (skipping — optional corpus).")
        return []
    rows: list[dict] = []
    for path in matches:
        with open(path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            file_rows = list(reader)
        rows.extend(file_rows)
        print(f"Loaded {len(file_rows)} industry-report rows from: {path}")
    print(f"  Total industry-report rows from {len(matches)} file(s): {len(rows)}")
    return rows


def build_documents(articles: list[dict]) -> tuple[list[str], list[dict]]:
    """One document per article: 'Title' on first line, then summary. Tiny
    metadata (title/link/source/published/domain/doc_type) so the retrieved
    chunks can cite themselves correctly and be labeled news vs. report.
    """
    texts: list[str] = []
    metadatas: list[dict] = []
    skipped = 0
    for a in articles:
        title = (a.get("title") or "").strip()
        summary = (a.get("summary") or "").strip()
        if not title and not summary:
            skipped += 1
            continue
        body = f"Title: {title}\n{summary}" if summary else f"Title: {title}"
        texts.append(body)
        metadatas.append({
            "title": title,
            "link": a.get("link", ""),
            "source": a.get("source", ""),
            "published": a.get("published", ""),
            "domain": a.get("domain", ""),
            # RSS rows have no doc_type column -> default to "news_article".
            # Industry-report rows carry doc_type="industry_report" in the CSV.
            "doc_type": a.get("doc_type", "news_article"),
        })
    if skipped:
        print(f"  Skipped {skipped} articles with no title and no summary.")
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
    print("=== Building FAISS index for news articles ===\n")
    csv_path = latest_news_csv()
    rss_articles = load_articles(csv_path)
    report_rows = load_industry_reports()
    articles = rss_articles + report_rows
    print(
        f"\n  {len(rss_articles)} RSS articles + {len(report_rows)} industry-report "
        f"rows = {len(articles)} total source rows."
    )

    print("\nBuilding documents from articles...")
    texts, metadatas = build_documents(articles)
    print(f"  {len(texts)} articles → {len(texts)} pre-chunk documents.")

    print("\nChunking...")
    texts, metadatas = chunk(texts, metadatas)
    print(f"  Produced {len(texts)} chunks (chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}).")

    # Import the shared embeddings factory — same source of truth as the
    # skills index (Critical Rule #7).
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
    print(f"\nFAISS news index saved to: {INDEX_DIR}/")
    print("Next: build the News agent and wire it into the Orchestrator.")


if __name__ == "__main__":
    main()
