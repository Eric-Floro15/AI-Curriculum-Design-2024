"""
run_news_tests.py — News Agent targeted tests.

Two test modes covered:

APPROACH 1 (free, retrieval-layer only):
    Synthetic article injection. We append 5 hand-written test articles
    (test_articles.csv) with unique anchor terms that cannot appear by
    chance, build an augmented FAISS index in /tmp, then query the
    anchor phrases and verify the test articles appear in the top-k
    retrieved set. Validates the scrape → index → retrieve pipeline
    end-to-end without needing the LLM.

APPROACH 2 (paid, ~$0.50-1.00 on Sonnet 4.6):
    Off-corpus probes. For each query in news_offcorpus_queries.yaml,
    run the live News Agent (using the production FAISS index) and
    check the answer for:
      - honest "thin retrieval" / "no coverage" signals (PASS)
      - fabricated URLs / organisation names / publication names
        (FAIL — these are the forbidden_substrings)
    Catches the URL-fabrication failure mode in advance instead of by
    post-hoc eyeball.

Run:
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_news_tests.py
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_news_tests.py --approach 1   # free only
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_news_tests.py --approach 2   # paid only
"""

import argparse
import csv
import glob
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

# RSS source CSVs sometimes have long article bodies; raise CSV's default
# field-size limit so reading doesn't truncate.
csv.field_size_limit(sys.maxsize)

from dotenv import load_dotenv  # noqa: E402
load_dotenv(os.path.join(_CHATBOT_DIR, ".env"))

# Must be set BEFORE any `from crewai import ...` — crewai is lazy-imported
# inside approach_2() but these env vars must already be in the environment
# before that happens. Setting them here (module level, after load_dotenv)
# guarantees the order regardless of which approach is run.
os.environ.setdefault("CREWAI_TELEMETRY_OPT_OUT", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")

import yaml  # noqa: E402

from langchain_community.vectorstores import FAISS  # noqa: E402
from langchain_text_splitters import RecursiveCharacterTextSplitter  # noqa: E402

from embeddings import get_embeddings, describe_embeddings_config  # noqa: E402

TEST_ARTICLES_CSV = os.path.join(_HERE, "test_articles.csv")
OFFCORPUS_QUERIES = os.path.join(_HERE, "news_offcorpus_queries.yaml")
PROD_NEWS_DIR = os.path.join(_CHATBOT_DIR, "data", "news")
TEST_INDEX_DIR = "/tmp/news_test_augmented_index"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
TOP_K = 5


def latest_prod_csv() -> str:
    files = sorted(glob.glob(os.path.join(PROD_NEWS_DIR, "news_articles_*.csv")))
    if not files:
        sys.exit("ERROR: No production news CSV found in chatbot/data/news/")
    return files[-1]


def load_articles(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_test_augmented_index() -> FAISS:
    """Combine production articles + test articles, build FAISS index."""
    prod_csv = latest_prod_csv()
    prod_articles = load_articles(prod_csv)
    test_articles = load_articles(TEST_ARTICLES_CSV)
    all_articles = prod_articles + test_articles
    print(f"  Prod articles: {len(prod_articles)}")
    print(f"  Test articles: {len(test_articles)}")
    print(f"  Total: {len(all_articles)}")

    texts: list[str] = []
    metadatas: list[dict] = []
    for a in all_articles:
        title = (a.get("title") or "").strip()
        summary = (a.get("summary") or "").strip()
        if not title and not summary:
            continue
        body = f"Title: {title}\n{summary}" if summary else f"Title: {title}"
        texts.append(body)
        metadatas.append({
            "title": title,
            "link": a.get("link", ""),
            "source": a.get("source", ""),
            "published": a.get("published", ""),
            "domain": a.get("domain", ""),
        })

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunked_texts: list[str] = []
    chunked_meta: list[dict] = []
    for text, meta in zip(texts, metadatas):
        for piece in splitter.split_text(text):
            chunked_texts.append(piece)
            chunked_meta.append(meta)

    print(f"  Chunks: {len(chunked_texts)}")
    print(f"  Embedding...")
    vs = FAISS.from_texts(chunked_texts, get_embeddings(), metadatas=chunked_meta)
    os.makedirs(TEST_INDEX_DIR, exist_ok=True)
    vs.save_local(TEST_INDEX_DIR)
    return vs


def approach_1(vs: FAISS) -> list[dict]:
    """Anchor-phrase retrieval check on each test article."""
    print("\n" + "=" * 72)
    print("APPROACH 1 — Synthetic article injection (retrieval-layer test)")
    print("=" * 72)

    test_articles = load_articles(TEST_ARTICLES_CSV)
    results: list[dict] = []
    for a in test_articles:
        anchor = a.get("anchor_query", "").strip()
        unique = a.get("unique_term", "").strip()
        if not anchor or not unique:
            continue
        print(f"\n  Test article: {a['title'][:64]}")
        print(f"    Anchor query: {anchor!r}")
        print(f"    Unique term:  {unique!r}")
        retrieved = vs.similarity_search(anchor, k=TOP_K)
        rank: int | None = None
        for i, d in enumerate(retrieved, 1):
            if unique.lower() in d.page_content.lower():
                rank = i
                break
        if rank is not None:
            print(f"    PASS — retrieved at rank {rank}/{TOP_K}")
            results.append({"id": a.get("entry_id"), "pass": True, "rank": rank})
        else:
            print(f"    FAIL — unique term not found in top {TOP_K}")
            print(f"    Top-{TOP_K} titles: {[d.metadata.get('title', '')[:40] for d in retrieved]}")
            results.append({"id": a.get("entry_id"), "pass": False, "rank": None})

    passed = sum(1 for r in results if r["pass"])
    print(f"\nApproach 1 total: {passed}/{len(results)} test articles retrieved at top-{TOP_K}")
    return results


def approach_2() -> list[dict]:
    """Off-corpus probes via the live News Agent."""
    print("\n" + "=" * 72)
    print("APPROACH 2 — Off-corpus probe queries (agent-layer test)")
    print("=" * 72)
    print(f"NOTE: uses the production index at chatbot/faiss_news_index/")
    print(f"NOTE: each query is a live LLM call against the configured provider")
    print(f"      ({os.getenv('LLM_PROVIDER', 'anthropic')} / {os.getenv('LLM_MODEL', 'default')})")

    # Lazy import — only needed if --approach 2.
    from crewai import Crew, Task  # noqa: E402
    from agents.news import make_news_agent  # noqa: E402

    with open(OFFCORPUS_QUERIES) as f:
        queries = yaml.safe_load(f)

    results: list[dict] = []
    for q in queries:
        print(f"\n  Query: [{q['id']}] {q['query']}")

        agent = make_news_agent()
        task = Task(
            description=q["query"],
            expected_output=(
                "A summary of relevant articles from the news corpus, "
                "OR an honest 'thin retrieval' note if the corpus does "
                "not cover this topic."
            ),
            agent=agent,
        )
        crew = Crew(agents=[agent], tasks=[task], verbose=False)
        t0 = time.time()
        try:
            answer = str(crew.kickoff())
            elapsed = time.time() - t0
        except Exception as e:
            print(f"    ERROR running crew: {e}")
            results.append({"id": q["id"], "verdict": "ERROR", "elapsed": time.time() - t0})
            continue

        answer_lc = answer.lower()
        thin_signals = q.get("expected_thin_signals", [])
        forbidden = q.get("forbidden_substrings", [])
        honest_match = any(sig.lower() in answer_lc for sig in thin_signals)
        fabrications = [f for f in forbidden if f.lower() in answer_lc]

        if fabrications:
            verdict = "FAIL"
        elif honest_match:
            verdict = "PASS"
        else:
            verdict = "INSPECT"  # neither honest signal nor fabrication — needs human

        print(f"    {verdict} ({elapsed:.0f}s)")
        if honest_match:
            print(f"      [honest thin-retrieval signal detected]")
        if fabrications:
            print(f"      [FAILURE: fabricated content: {fabrications}]")
        # Always show first 400 chars of the answer so inspection is easy
        ans_preview = answer.replace("\n", " ")[:400]
        print(f"      Answer preview: {ans_preview}...")

        results.append({
            "id": q["id"],
            "verdict": verdict,
            "honest_match": honest_match,
            "fabrication": fabrications,
            "elapsed": elapsed,
        })

    summary = {"PASS": 0, "FAIL": 0, "INSPECT": 0, "ERROR": 0}
    for r in results:
        summary[r["verdict"]] = summary.get(r["verdict"], 0) + 1
    print(f"\nApproach 2 totals: {summary}")
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--approach", choices=["1", "2", "both"], default="both")
    args = parser.parse_args()

    print(f"Embeddings: {describe_embeddings_config()}\n")

    r1 = r2 = None
    if args.approach in ("1", "both"):
        print("Building test-augmented index...")
        vs = build_test_augmented_index()
        r1 = approach_1(vs)

    if args.approach in ("2", "both"):
        r2 = approach_2()

    print("\n" + "=" * 72)
    print("FINAL SUMMARY")
    print("=" * 72)
    if r1 is not None:
        passed = sum(1 for r in r1 if r["pass"])
        print(f"  Approach 1 (retrieval):    {passed}/{len(r1)} PASS")
    if r2 is not None:
        passed = sum(1 for r in r2 if r["verdict"] == "PASS")
        failed = sum(1 for r in r2 if r["verdict"] == "FAIL")
        inspect = sum(1 for r in r2 if r["verdict"] == "INSPECT")
        print(f"  Approach 2 (off-corpus):   {passed} PASS, {failed} FAIL, {inspect} INSPECT")


if __name__ == "__main__":
    main()
