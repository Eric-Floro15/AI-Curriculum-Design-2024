"""
fetch_news.py — Pull recent articles from AI/ML-focused RSS feeds.

Writes a timestamped CSV to chatbot/data/news/. The CSV is the input to
build_news_index.py (the news FAISS index).

Run:
    python chatbot/fetch_news.py

Design notes:
- v1 uses only the RSS-provided title + summary. Full article extraction
  (trafilatura/newspaper3k) is intentionally skipped — it adds two heavy
  deps, slows the scrape ~5×, and hammers external sites. Most feeds give
  a 1-3 sentence summary which is enough signal for a "what's new in AI?"
  curriculum-design query. If retrieval quality is poor later, add a
  --full-text flag to enable extraction.
- Feed list is curated for AI/ML developments relevant to curriculum
  design (model releases, industry trends, research highlights). Edit
  RSS_FEEDS below to add/remove sources.
- Pattern borrowed from News-Agent-Chatbot-Code-Example/news_ingestion/
  MIE1624_RSS.ipynb (Eric's reference) — but rewritten as a Python module,
  with relative paths, configurable feed list, and no external-site
  scraping.
"""

import csv
import hashlib
import os
import re
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

import feedparser
import requests

# Real browser User-Agent. Publishers with strict bot-detection
# (MIT TR, TechCrunch, etc.) serve empty responses to feedparser's
# default UA.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
HTTP_TIMEOUT = 20

# We fetch with `requests` instead of letting feedparser do the HTTP itself,
# because feedparser uses Python's urlopen which on macOS often hits SSL
# cert-verify failures (system Python ships without proper CA bundle).
# requests uses certifi and works out of the box.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEWS_DIR = os.path.join(BASE_DIR, "data", "news")

# AI/ML-focused feeds. Verified-stable URLs from major industry & research
# outlets. Edit this list to change sources — code below adapts automatically.
RSS_FEEDS = {
    "MIT Technology Review AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed",  # no trailing slash — VB redirects with 308
    "HuggingFace Blog": "https://huggingface.co/blog/feed.xml",
    "The Decoder": "https://the-decoder.com/feed/",
}

ITEMS_PER_SOURCE = 50
SLEEP_BETWEEN_FEEDS = 1.0

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def _clean_text(s: str) -> str:
    """Strip HTML tags and collapse whitespace. RSS summaries often contain
    inline HTML (<p>, <a>) which we don't want in the indexed text."""
    if not s:
        return ""
    return _WS_RE.sub(" ", _TAG_RE.sub(" ", s)).strip()


def _parse_published(entry) -> str:
    """Return ISO-8601 publish time if available, else empty string."""
    for attr in ("published", "updated", "created"):
        val = getattr(entry, attr, "")
        if val:
            return str(val)
    return ""


def _parse_authors(entry) -> str:
    """feedparser puts authors in several places; join all non-empty values."""
    names = []
    for a in getattr(entry, "authors", []) or []:
        n = a.get("name", "") if isinstance(a, dict) else ""
        if n:
            names.append(n)
    if not names:
        single = getattr(entry, "author", "")
        if single:
            names.append(single)
    return ", ".join(names)


def _sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", "ignore")).hexdigest()


def _fetch_feed(url: str) -> "feedparser.FeedParserDict | None":
    """HTTP-fetch the feed with a real UA + certifi-backed SSL, then hand
    the raw bytes to feedparser. Returns None on network errors."""
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/xml, */*"},
            timeout=HTTP_TIMEOUT,
            allow_redirects=True,
        )
    except requests.RequestException as e:
        print(f"  HTTP error: {e}")
        return None
    if resp.status_code != 200:
        print(f"  HTTP {resp.status_code} — skipping.")
        return None
    return feedparser.parse(resp.content)


def fetch_all() -> list[dict]:
    """Fetch every configured feed and return deduplicated article records."""
    records: list[dict] = []
    seen_links: set[str] = set()

    for source_name, feed_url in RSS_FEEDS.items():
        print(f"\nFetching: {source_name}")
        print(f"  {feed_url}")
        feed = _fetch_feed(feed_url)
        if feed is None:
            continue

        if feed.bozo:
            # bozo just means the parser had to recover from minor issues —
            # still usually returns useful entries.
            print(f"  (parser noted minor issues, bozo={feed.bozo})")

        entries = list(getattr(feed, "entries", []))[:ITEMS_PER_SOURCE]
        if not entries:
            print(f"  No entries returned — feed may be broken or rate-limited.")
            continue
        print(f"  Got {len(entries)} entries")

        kept = 0
        for entry in entries:
            link = (getattr(entry, "link", "") or "").strip()
            if not link or link in seen_links:
                continue
            seen_links.add(link)

            title = _clean_text(getattr(entry, "title", "") or "")
            summary = _clean_text(
                getattr(entry, "summary", None) or getattr(entry, "description", "") or ""
            )
            published = _parse_published(entry)
            authors = _parse_authors(entry)
            entry_id = (
                getattr(entry, "id", None) or getattr(entry, "guid", None) or _sha1(link)
            )

            records.append({
                "source": source_name,
                "title": title,
                "link": link,
                "summary": summary,
                "published": published,
                "entry_id": str(entry_id),
                "authors": authors,
                "domain": urlparse(link).netloc,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            })
            kept += 1

        print(f"  Kept {kept} unique entries (after dedup against earlier feeds)")
        time.sleep(SLEEP_BETWEEN_FEEDS)

    return records


def save_csv(records: list[dict], out_dir: str = NEWS_DIR) -> str:
    """Write records to a timestamped CSV. Returns the written path."""
    if not records:
        sys.exit("ERROR: No records fetched — nothing to save.")

    os.makedirs(out_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(out_dir, f"news_articles_{timestamp}.csv")

    fieldnames = list(records[0].keys())
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"\nSaved {len(records)} articles to: {out_path}")
    return out_path


def main():
    print("=== Fetching AI/ML news from RSS feeds ===")
    print(f"Configured feeds: {len(RSS_FEEDS)}")
    print(f"Items per source (max): {ITEMS_PER_SOURCE}")
    records = fetch_all()
    print(f"\nTotal unique articles collected: {len(records)}")
    save_csv(records)
    print("\nNext: build the news FAISS index with `python chatbot/build_news_index.py`")


if __name__ == "__main__":
    main()
