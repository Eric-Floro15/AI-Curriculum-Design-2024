# For Cassie — re-analysis outputs for the chatbot

Two independent bundles, built from the completed 7-semester re-analysis
(F2022, W2023, F2023, W2024, F2024, F2025, W2026 — W2025 dropped, it
turned out to be duplicate F2024 data). Neither bundle touches or
replaces anything you've already built — both are additive.

## `01_FAISS_ADDITIONS/`

Content to add to your existing skills FAISS index via `add_texts()`:
the current V2 taxonomy (1,058 canonical skills, tagged and joined to
their W2026 cluster ID) plus four prose summaries of the re-analysis
findings (skill demand trends, salary/education trends, clustering
stability, and an open caveat about F2025/W2026 data quality). Includes
a ready-to-run script and a note on how we're suggesting you handle V1
vs. V2 taxonomy content without hurting retrieval precision. Start with
that folder's own README.

## `02_STRUCTURED_DATA/`

Structured CSVs (cluster assignments, per-semester skill frequency,
salary/education tables, the ARI stability matrix, source-mix data) for
direct pandas/CSV lookup rather than semantic search — plus notes on two
pre-existing bugs in `cluster_tool.py` (a frequency-lookup mismatch and
it pointing at the old V1 taxonomy file) that this data can help fix.
Start with that folder's own README.

## Why split this way

FAISS/semantic search and structured/tabular lookup serve different
query types — "what does the data say about X" vs. "give me the exact
number for Y" — and mixing raw tables into a vector index tends to hurt
retrieval precision. So: prose and skill descriptions go to FAISS,
numbers go to CSVs, both point back at the same underlying analysis.

## One thing to flag before you touch anything

`01_FAISS_ADDITIONS/prompt_update_v1_handling.md` explains why we did
*not* re-embed V1 taxonomy content alongside the new V2 content, even
though the original ask was to keep V1 present but marked outdated —
short version: re-adding it risks the same near-duplicate-content
retrieval-crowding problem you already found and fixed in the news
corpus. We're recommending a one-line prompt change on your Analyst
agent instead. Worth reading before deciding how you want to handle it.
