"""
program_rag_tool.py — RAG retrieval over the hand-curated university
program/curriculum index. BM25 lexical scoring is retained purely as a
diagnostic signal (not used for ranking or gating) — see "Hybrid-retrieval
history" below for why.

Loads chatbot/faiss_program_index/ and exposes:
  - retrieve(query, k)   → list of program records above the relevance
                            threshold (Python API)
  - program_rag_tool     → CrewAI tool wrapper (used by the University AI
                            Programs Researcher)

Design: RAG-first, web-search-fallback. This corpus only covers programs
someone has hand-curated (see data/program_and_curriculum/), so a query
about a not-yet-covered program SHOULD miss. retrieve() applies a distance
threshold so weak/irrelevant matches are dropped rather than returned as
false positives — an empty result is the deliberate signal that tells the
agent to call web_search_tool instead.

Hybrid-retrieval history (2026-06-16): with 6 programs in the corpus, the
negative-control eval case (a query about a real but NOT-locally-covered
program, University of Washington) started returning confident FAISS
false positives — Stanford/CMU chunks at L2 distance 0.46-0.53, sitting
squarely INSIDE the observed genuine-match range (0.27-0.60). A first
attempt fixed this by merging FAISS- and BM25-ranked candidates via
weighted Reciprocal Rank Fusion (mirroring tools/rag_tool.py's validated
skills-RAG pattern) and using that FUSED order to decide which k chunks
to return, on the theory that BM25's IDF weighting would downweight the
templated boilerplate shared across every program write-up and reward
rare institution-specific tokens instead.

REVERTED the same day, after a real eval rerun
(chatbot/eval/program_baseline_2026-06-16_mxbai-embed-large.md, run after
the hybrid change landed) showed two things:
  1. It did NOT fix negative-control-uw — still 0/1. Real bm25_score for
     genuine matches ranges as low as 3.29 (cmu-direct) up to 26.95
     (rotman-direct); the negative control's false positives scored
     4.68-5.48 — squarely INSIDE that range. Same overlapping-ranges
     problem as raw distance, just shifted to a new feature; no single
     bm25_score floor separates them either.
  2. It actively REGRESSED a previously-fine case: mit-by-topic went from
     precision@3=0.33 / recall@3=1.00 (FAISS-only ranking; the MIT chunk
     at distance 0.5458 ranked #2) to precision@3=0.00 / recall@3=0.00
     (fused ranking demoted that same MIT chunk out of the top-3 entirely,
     in favor of two Queen's chunks and a CMU chunk that BM25 happened to
     rank higher for that query's specific wording). FAISS is weighted
     10x over BM25 in the fusion, but that's not enough to prevent
     reordering when several FAISS distances cluster tightly together,
     as they did here (0.4506-0.5697 across 5 candidates).
  Net effect across the 8 directional cases: mean precision@3 dropped
  0.79→0.75 and mean recall@3 dropped 1.00→0.88, entirely attributable to
  the mit-by-topic regression — no-cross-contamination stayed flat at
  5/8. In short: the hybrid reordering cost more than it bought, and a
  real fix for the negative control still doesn't exist.

Current behavior: selection of which k chunks to return is back to pure
FAISS L2 distance ranking (the approach validated before 2026-06-16).
retrieve() still builds a BM25 index via _load_bm25() and reports both
`fused_score` (RRF fusion, informational only) and `bm25_score` (raw
BM25/Okapi magnitude via _bm25_scores(), informational only) alongside
`distance` for every returned chunk — kept purely as instrumentation for
a future attempt, since neither signal is provably useless, just not
provably sufficient ALONE with the data on hand. One untried idea: instead
of a generic magnitude floor, check whether the query's distinctive proper
nouns (e.g. an institution name) literally appear anywhere in the
candidate chunk's text — that targets the actual root cause (the
negative-control program's name never appears in this corpus at all) more
directly than either distance or BM25 magnitude does.

Both build_program_index.py and this module import from the shared
chatbot/embeddings.py helper, per CLAUDE.md Critical Rule #7.

Institution-name gate (added 2026-06-16, later the same day as the
hybrid-retrieval revert above) — VALIDATED by a live eval rerun the same
day (chatbot/eval/program_baseline_2026-06-16_mxbai-embed-large-2dbd6229.md,
67 indexed chunks): negative-control-uw flipped to **1/1 PASS** (from 0/1 —
the primary goal), no-cross-contamination went **7/8** (from 5/8), mean
P@3 **0.88** (from 0.79), R@3 unchanged at **1.00**. The hypothesized side
benefit was confirmed too: both queens-direct and georgia-tech-direct,
which had cross-contamination before this gate, now have none. mit-by-topic
(the case the earlier RRF attempt regressed) is confirmed UNCHANGED at
P@3=0.33/R@3=1.00 — not regressed, exactly per design (by-topic queries
skip the gate). The one remaining contamination case is mit-by-topic
itself, same as before this gate existed, not a new issue.

Rationale: every attempt above (tightening MAX_DISTANCE, the RRF hybrid)
tried to separate genuine matches from negative-control-uw's false
positives using a MAGNITUDE threshold on some score (distance, bm25_score).
Both failed because the actual genuine-match and false-positive ranges
overlap on every magnitude tried so far — no threshold can split them.
This attempt uses a categorically different signal instead: does the
QUERY's named institution (if any) literally match the CANDIDATE chunk's
institution? `_query_institution_groups()` checks the query text against a
hand-maintained, word-boundary-anchored alias regex per corpus institution
(e.g. "MIT" / "Massachusetts Institute of Technology" / "EECS" / "6-4" all
map to the MIT group); `_institution_group_for_program()` does the same for
a candidate's curated `program` metadata field, checking ALL of a group's
aliases (an earlier version anchored on only the longest alias per group,
which broke self-classification for MIT and Georgia Tech — their curated
`program` field uses the short form, not the spelled-out name; fixed before
this ever reached a real eval run, see _institution_group_for_program's
docstring). Word-boundary anchoring matters because a plain substring check
on a short alias like "mit" also matches inside unrelated words ("submit",
"commit", "admit"...) — confirmed empirically while building this, not a
hypothetical concern. `retrieve()` only applies the alias filter when
`_institution_gate_active()` judges the query to be ABOUT a specific
institution at all (either it names one of the 6 corpus institutions, or it
contains a generic institution-type word like
"university"/"institute"/"college"/"school of") — by-topic queries with no
institution name at all (e.g. queens-by-topic, mit-by-topic) skip this
filter entirely and fall through to the existing pure-distance behavior
unchanged, specifically so this fix can't repeat the RRF mistake of
regressing a case it wasn't trying to fix.

KNOWN LIMITATION: the generic institution-type-word check only catches
queries phrased with "university"/"institute"/"college"/"school of" (which
is exactly negative-control-uw's phrasing: "University of Washington...").
It will NOT catch an institution name that uses none of those words and
isn't one of the 6 corpus aliases either (e.g. a bare "Caltech" with no
spelled-out "California Institute of Technology") — that query would skip
the gate and fall back to the same overlapping-distance problem as before.
A general-purpose institution-name extractor (NER) would close that
remaining gap; out of scope for this attempt. Also: any NEW program added
to the corpus needs a matching entry added to `_INSTITUTION_ALIASES`
(mirroring the existing MAX_DISTANCE re-validation reminder below) — until
then, candidates from that program are invisible to this gate and fall back
to pure-distance filtering only (fails open, not closed, so an unmapped
program can't be wrongly suppressed — it just doesn't get the new
protection either).

Run standalone to smoke-test (also prints raw distance + fused/bm25
scores, useful for re-calibrating PROGRAM_RAG_MAX_DISTANCE once more
program files and eval queries exist):
    KMP_DUPLICATE_LIB_OK=TRUE python chatbot/tools/program_rag_tool.py
"""

import os
import re
import sys
from functools import lru_cache

from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS

# Make chatbot/ importable so embeddings.py resolves regardless of cwd.
_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from embeddings import get_embeddings, describe_embeddings_config

INDEX_DIR = os.path.join(_CHATBOT_DIR, "faiss_program_index")
DEFAULT_K = 5

# FAISS (via langchain_community's default flat index) returns L2 distance:
# LOWER is more similar. Calibrated 2026-06-16 against the first 2 real
# program files + program_queries.yaml (see chatbot/eval/program_baseline_*.md):
# worst genuine match seen so far = 0.7548 (queens-direct), best false-positive
# seen so far = 0.7689 (negative-control-stanford, via an MIT chunk). 0.76 sits
# in that ~0.014-wide gap — passes the negative control without dropping any
# observed genuine match. That gap is razor-thin with only 2 programs in the
# corpus, so RE-VALIDATE this value (rerun run_program_rag_eval.py) every time
# a new program file is added — don't assume it still holds. STATUS as of the
# 2026-06-16 6-program eval round: 0.76 still passes every genuine match, but
# no longer rejects every false positive on its own — negative-control-uw's
# false positives sit at distance 0.4674-0.5281, INSIDE the genuine range.
# Tried fixing this with fused_score (RRF) and bm25_score (raw BM25
# magnitude) — neither works as a single-feature gate either: bm25_score for
# genuine matches ranges 3.29-26.95, and negative-control-uw's false
# positives (4.68-5.48) sit squarely inside that range too. See the module
# docstring's "Hybrid-retrieval history" section for the full story and why
# the RRF-fused selection was reverted the same day. Don't tighten
# MAX_DISTANCE (or add a bm25_score floor) based on this one negative-control
# query — the ranges genuinely overlap with the data on hand; a real fix
# needs either more negative-control examples or a different kind of signal
# entirely, not a magnitude threshold on any one score. UPDATE (later
# 2026-06-16): the institution-name gate below is exactly that different
# signal, and a live eval rerun the same day confirmed it worked — see its
# section in the module docstring for the numbers.
# Override without editing code via env var: PROGRAM_RAG_MAX_DISTANCE=<float>
MAX_DISTANCE = float(os.getenv("PROGRAM_RAG_MAX_DISTANCE", "0.76"))

_INDEX_MISSING_MSG = (
    "No local program/curriculum index found yet (no program files have "
    "been added to chatbot/data/program_and_curriculum/, or the index "
    "hasn't been built). Use the Web Search tool instead for this query."
)
_NO_MATCH_MSG = (
    "No sufficiently relevant program/curriculum data found in the local "
    "corpus for this query. Use the Web Search tool instead."
)


# ── Institution-name gate (added 2026-06-16) ──────────────────────────────
# See module docstring's "Institution-name gate" section for full rationale.
# MAINTENANCE: every program currently in the corpus needs an entry here.
# When a 7th program is added to data/program_and_curriculum/, add its
# aliases here too -- otherwise its chunks are invisible to this gate (they
# just fall back to plain-distance filtering, same as before this fix).
_INSTITUTION_ALIASES: dict[str, list[str]] = {
    "queens": [
        "queen's university",
        "queen's",
        "queens university",
        "smith school of business",
        "smith school",
        "mmai",
    ],
    "mit": [
        "massachusetts institute of technology",
        "mit",
        "eecs",
        "6-4",
    ],
    "cmu": [
        "carnegie mellon university",
        "carnegie mellon",
        "cmu",
        "msaii",
        "language technologies institute",
    ],
    "georgia_tech": [
        "georgia institute of technology",
        "georgia tech",
        "college of computing",
    ],
    "uoft_rotman": [
        "university of toronto",
        "uoft",
        "u of t",
        "rotman school of management",
        "rotman",
    ],
    "stanford": [
        "stanford university",
        "stanford",
    ],
}

# Per-group alias regex, word-boundary-anchored. \b matters here: a plain
# substring check on a short alias like "mit" would also match inside
# unrelated words ("submit", "commit", "summit", "admit"...) -- confirmed
# empirically while building this (see chat record 2026-06-16). \b forces a
# real word/phrase boundary on both sides of whichever alternative matches,
# for every alias regardless of length, so "MIT" the institution still
# matches a standalone "MIT" token without also matching "submit".
_INSTITUTION_ALIAS_PATTERNS: dict[str, re.Pattern] = {
    group: re.compile(
        r"\b(?:" + "|".join(re.escape(alias) for alias in aliases) + r")\b",
        re.IGNORECASE,
    )
    for group, aliases in _INSTITUTION_ALIASES.items()
}

# Generic institution-type words. If a query contains one of these but
# doesn't name any of the 6 corpus institutions above, it's most likely
# asking about a DIFFERENT, not-yet-curated institution (e.g.
# negative-control-uw's "University of Washington") -- the gate should still
# activate so that a confident-looking FAISS false positive for some OTHER
# institution's chunk gets filtered out, rather than silently accepted.
_GENERIC_INSTITUTION_HINT_RE = re.compile(
    r"\b(university|institute|college|school of)\b", re.IGNORECASE
)


def _institution_group_for_program(program_field: str) -> str | None:
    """Classify a chunk's curated `program` metadata string into one of the
    groups in _INSTITUTION_ALIASES, by checking ALL of that group's aliases
    (not just the longest) -- an earlier version anchored on the longest
    alias only and that broke self-classification for MIT and Georgia Tech,
    whose curated `program` field uses the short form ("MIT", "Georgia
    Tech") rather than the spelled-out official name; checking every alias
    fixed it without reintroducing the substring-collision risk, since the
    patterns are word-boundary-anchored (see _INSTITUTION_ALIAS_PATTERNS).

    Returns None for any program not yet represented in _INSTITUTION_ALIASES
    (e.g. a newly added 7th program before its aliases are added) -- see the
    MAINTENANCE note above. None means "can't classify", and retrieve()
    below treats that as "don't apply the gate to this candidate" (fails
    open, not closed).
    """
    for group, pattern in _INSTITUTION_ALIAS_PATTERNS.items():
        if pattern.search(program_field):
            return group
    return None


def _query_institution_groups(query_lc: str) -> set[str]:
    """Which of the 6 corpus institutions (if any) does this query literally
    name, via any of their known aliases? `query_lc` may be passed already
    lowercased by the caller, though the patterns are case-insensitive
    regardless."""
    return {
        group
        for group, pattern in _INSTITUTION_ALIAS_PATTERNS.items()
        if pattern.search(query_lc)
    }


def _institution_gate_active(query_lc: str, named_groups: set[str]) -> bool:
    """True if this query appears to be ABOUT a specific institution at all
    (named or not), in which case retrieve() should filter out candidates
    whose institution doesn't match. False for by-topic queries with no
    institution-like signal at all (e.g. "AI master's program with business
    strategy courses") -- those queries fall through to the pre-existing
    pure-distance behavior, unchanged, so this fix can't regress a by-topic
    case the way the 2026-06-16 RRF attempt did.

    KNOWN LIMITATION: see module docstring -- this only catches institution
    references that either match one of the 6 corpus aliases OR contain a
    generic word like "university"/"institute"/"college"/"school of". A
    bare "Caltech" (no spelled-out "California Institute of Technology")
    would slip through ungated.
    """
    return bool(named_groups) or bool(_GENERIC_INSTITUTION_HINT_RE.search(query_lc))


@lru_cache(maxsize=1)
def _load_vectorstore() -> FAISS:
    if not os.path.exists(os.path.join(INDEX_DIR, "index.faiss")):
        raise FileNotFoundError(
            f"Program FAISS index not found at {INDEX_DIR}. "
            "Run `python chatbot/build_program_index.py` after adding at "
            "least one real program file to data/program_and_curriculum/."
        )
    return FAISS.load_local(
        INDEX_DIR,
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )


@lru_cache(maxsize=1)
def _load_bm25() -> BM25Retriever | None:
    """
    Build a BM25 retriever from the same chunked program documents the FAISS
    index uses, mirroring tools/rag_tool.py's hybrid pattern exactly. Rebuilt
    fresh from the source .txt files each process — cheap at this corpus's
    size (a handful of programs, well under a hundred chunks total).

    Returns None (not an empty retriever) when no program files exist yet,
    so retrieve() can skip BM25 entirely rather than fail — same "a miss is
    not an error" posture as the rest of this module.
    """
    # Lazy import — build_program_index.py belongs to chatbot/, not tools/.
    from build_program_index import (  # noqa: E402
        build_documents,
        chunk,
        find_program_files,
    )

    files = find_program_files()
    if not files:
        return None
    texts, metadatas = build_documents(files)
    if not texts:
        return None
    texts, metadatas = chunk(texts, metadatas)
    return BM25Retriever.from_texts(texts=texts, metadatas=metadatas)


def _bm25_scores(bm25: BM25Retriever, query: str) -> dict[str, float]:
    """Raw BM25 (Okapi) relevance scores for every doc in the corpus, keyed
    by page_content — magnitudes, NOT just rank position.

    BM25Retriever's public invoke()/get_relevant_documents() only returns
    ranked Documents, never the underlying score, so this reaches into the
    rank_bm25.BM25Okapi vectorizer it wraps internally (the same library
    backing tools/rag_tool.py's hybrid retrieval) to get real magnitudes.

    This matters because _rrf_merge() below fuses by RANK POSITION only
    (the standard RRF formula), and with FAISS weighted 10x over BM25
    (matching the skills RAG's validated weighting), a doc FAISS ranks #1
    keeps a high fused_score almost regardless of where BM25 ranks it —
    rank-only fusion can re-order candidates, but can't by itself express
    "this candidate has no real lexical grounding in the query at all",
    which is exactly the signal needed to catch a confident FAISS false
    positive like the negative-control-uw case (see module docstring). An
    absolute score floor can express that; a rank cannot.

    No floor is applied on this — the 2026-06-16 post-hybrid eval rerun
    showed genuine matches' bm25_score ranging 3.29-26.95, with the
    negative-control-uw false positives (4.68-5.48) sitting inside that
    range, so a single global floor can't separate them either (see module
    docstring's "Hybrid-retrieval history"). Reported alongside distance
    and fused_score purely as instrumentation for a future, more targeted
    attempt.
    """
    tokens = bm25.preprocess_func(query)
    raw_scores = bm25.vectorizer.get_scores(tokens)
    return {doc.page_content: float(s) for doc, s in zip(bm25.docs, raw_scores)}


def _rrf_merge(ranked_lists, weights, k: int, c: int = 60):
    """Weighted reciprocal-rank-fusion merge of multiple ranked Document lists.

    Identical formula to tools/rag_tool.py's hybrid skills retrieval: each
    doc's score = sum over rankings of weight / (c + rank); c=60 is the
    standard constant from the original RRF paper.

    As of 2026-06-16 this is used ONLY to compute the informational
    `fused_score` retrieve() reports per result — it no longer determines
    which chunks get returned or in what order. It drove selection for one
    day, but a real eval rerun showed that reordering by fused rank
    regressed a previously-fine directional case (mit-by-topic) without
    fixing the negative control it was meant to fix, so selection reverted
    to plain FAISS-distance ranking (see the module docstring's
    "Hybrid-retrieval history" section).

    Dedup key is page_content. Returns up to k (doc, fused_score) tuples,
    sorted by fused_score descending.
    """
    scores: dict[str, float] = {}
    by_key: dict[str, object] = {}
    for ranking, weight in zip(ranked_lists, weights):
        for rank, doc in enumerate(ranking):
            key = doc.page_content
            scores[key] = scores.get(key, 0.0) + weight / (c + rank)
            by_key[key] = doc
    top_keys = sorted(scores, key=scores.get, reverse=True)[:k]
    return [(by_key[key], scores[key]) for key in top_keys]


def retrieve(
    query: str, k: int = DEFAULT_K, max_distance: float = MAX_DISTANCE
) -> list[dict]:
    """Return up to k program/curriculum chunks relevant to `query`.

    Selection is pure FAISS L2 distance ranking (reverted from RRF-fused
    ranking on 2026-06-16 — see the module docstring's "Hybrid-retrieval
    history": fusing in BM25 rank didn't fix the negative-control case it
    was meant to fix, and it regressed a previously-fine directional case
    by reordering a tight cluster of FAISS distances). Only chunks at or
    below `max_distance` are returned; an empty list means "no good local
    match" and the caller should treat that as a signal to fall back to web
    search, not as an error.

    Each returned chunk also carries `fused_score` (RRF fusion of FAISS +
    BM25 rank) and `bm25_score` (raw BM25/Okapi magnitude) — both computed
    for diagnostic visibility only, neither used to decide what gets
    returned or in what order. Treat their presence here as instrumentation
    for a future, better-informed attempt, not as evidence they already
    solve anything.

    On top of the distance threshold, an institution-name gate (added
    2026-06-16, see module docstring) drops any candidate whose institution
    doesn't match the query's named institution -- but ONLY for queries
    that appear to be about a specific institution at all; by-topic queries
    are unaffected. Each result also carries `institution_group` (which of
    the 6 corpus institutions it was classified as, or None) for visibility
    into whether/how the gate applied.

    Raises FileNotFoundError if the FAISS index hasn't been built yet.
    Callers that want a plain-string fallback instead of an exception should
    use the `program_rag_tool` CrewAI wrapper below, which catches this.
    """
    store = _load_vectorstore()
    bm25 = _load_bm25()

    query_lc = query.lower()
    named_groups = _query_institution_groups(query_lc)
    gate_active = _institution_gate_active(query_lc, named_groups)

    # Corpus is small (well under a hundred chunks today) so over-fetching
    # before filtering is cheap.
    fetch_n = max(20, k * 4)

    faiss_hits = store.similarity_search_with_score(query, k=fetch_n)

    if bm25 is not None:
        bm25.k = fetch_n
        bm25_docs = bm25.invoke(query)
        faiss_docs = [doc for doc, _ in faiss_hits]
        # Computed for the informational fused_score only — does NOT drive
        # selection or ordering below (see docstring).
        fused = _rrf_merge([faiss_docs, bm25_docs], weights=[1.0, 0.10], k=fetch_n)
        fused_score_by_key = {doc.page_content: score for doc, score in fused}
        lexical_scores = _bm25_scores(bm25, query)
    else:
        # No BM25 index buildable (e.g. corpus genuinely empty) — no
        # diagnostics to report, but FAISS-only selection still works fine.
        fused_score_by_key = {}
        lexical_scores = {}

    results = []
    for doc, distance in faiss_hits:  # FAISS order drives selection, not fused order
        distance = float(distance)
        if distance > max_distance:
            continue
        program_field = doc.metadata.get("program", "")
        doc_group = _institution_group_for_program(program_field)
        if gate_active and doc_group is not None and doc_group not in named_groups:
            # Query is about a specific institution (named or generically
            # implied) and this candidate is confidently classified as a
            # DIFFERENT one -- treat as a false positive regardless of how
            # low its distance is. This is the fix for negative-control-uw
            # (confirmed PASS, up from 0/1, in the 2026-06-16 live eval
            # rerun) and it also cleaned up queens-direct's and
            # georgia-tech-direct's cross-contamination as a side effect,
            # confirmed in that same rerun (no-cross-contamination went
            # 5/8 -> 7/8; see module docstring for full numbers).
            continue
        results.append({
            "program": program_field,
            "source_urls": doc.metadata.get("source_urls", ""),
            "last_verified": doc.metadata.get("last_verified", ""),
            "file": doc.metadata.get("file", ""),
            "content": doc.page_content,
            "distance": round(distance, 4),
            "fused_score": round(fused_score_by_key.get(doc.page_content, 0.0), 6),
            "bm25_score": round(lexical_scores.get(doc.page_content, 0.0), 4),
            "institution_group": doc_group,
        })
        if len(results) == k:
            break
    return results


def format_results(results: list[dict]) -> str:
    """Render retrieval results as a citation-ready block for LLM consumption."""
    if not results:
        return _NO_MATCH_MSG
    blocks = []
    for i, r in enumerate(results, 1):
        header = f"[{i}] {r['program']}"
        meta = f"    Source: {r['source_urls']}"
        if r["last_verified"]:
            meta += f" (verified {r['last_verified']})"
        blocks.append(f"{header}\n{meta}\n    {r['content']}")
    return "\n\n".join(blocks)


# CrewAI tool wrapper — guarded so this module stays testable before crewai is installed.
try:
    from crewai.tools import tool

    @tool("University Program RAG")
    def program_rag_tool(query: str) -> str:
        """
        Search the LOCAL, hand-curated corpus of university AI/ML program
        and curriculum data FIRST, before using Web Search. Every entry in
        this corpus was manually verified against an official program page
        by a human, so a match here is more trustworthy than a fresh web
        search and should be preferred whenever it's available.

        If this tool returns "No sufficiently relevant program/curriculum
        data found..." or a message about the index not existing, that is
        the expected signal to fall back to the Web Search tool for this
        query — it is NOT an error.

        Argument:
          query  REQUIRED non-empty natural-language search string, e.g.
                 the program/institution name or the topic you need
                 curriculum info about.

        Example:
          - program_rag_tool(query="Queen's University MMAI curriculum")
          - program_rag_tool(query="master's programs covering MLOps and data governance")
        """
        try:
            return format_results(retrieve(query, k=DEFAULT_K))
        except FileNotFoundError:
            return _INDEX_MISSING_MSG

except ImportError:
    program_rag_tool = None  # crewai not installed — Python-API retrieve() still works.


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(_CHATBOT_DIR, ".env"))

    print(f"Using {describe_embeddings_config()}")
    print(
        f"MAX_DISTANCE threshold = {MAX_DISTANCE} "
        "(lower score = more similar; tune via PROGRAM_RAG_MAX_DISTANCE)\n"
    )

    queries = [
        "Queen's University MMAI curriculum",
        "master's program covering MLOps and data governance",
        "completely unrelated query about medieval history",
        "University of Washington Master's in Computer Science Artificial Intelligence track requirements",
    ]
    for q in queries:
        print(f"=== Query: {q!r} ===")
        try:
            results = retrieve(q, k=3)
        except FileNotFoundError as e:
            print(f"(index not built yet: {e})\n")
            continue
        if results:
            for r in results:
                print(
                    f"  distance={r['distance']:.4f}  "
                    f"fused_score={r['fused_score']:.6f}  "
                    f"bm25_score={r['bm25_score']:.4f}  "
                    f"institution_group={r['institution_group']}  {r['program']}"
                )
        else:
            print("  (no results above threshold / filtered by institution gate)")
        print(format_results(results))
        print()
