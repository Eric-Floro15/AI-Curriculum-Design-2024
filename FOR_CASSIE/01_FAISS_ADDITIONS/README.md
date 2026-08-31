# FAISS Additions — Skills Index

Adds new content to your **existing** skills FAISS index. Doesn't rebuild
or replace it — your current index, embeddings, and everything already in
it stay exactly as they are.

## What's in `documents/`

- **`v2_taxonomy_skills.jsonl`** — 1,058 skill documents from the current
  V2 taxonomy (`Grouped_Skills_Categorized_V2.xlsx`, `is_generic == 0`).
  One doc per canonical skill: name, category, description, V2-corpus
  frequency, and its cluster ID from the current W2026 clustering
  (`clust_ensembled_results.csv`). Tagged `taxonomy_version: V2, status:
  current`.
- **`trend_analysis_summary.md`** — 7-semester skill demand trends
  (F2022→W2026): AI/GenAI rising sharply, classic ML/stats stack losing
  demand *share* but not pay.
- **`salary_education_summary.md`** — degree-level salary trends, two
  framings (vs. Bachelor's, vs. that semester's own market median). No
  sign of Master's premium eroding.
- **`clustering_stability_summary.md`** — pairwise ARI across 7
  semesters; F2025 and W2026 cluster with each other much more than with
  any other semester.
- **`source_mix_caveat.md`** — the open, unresolved question of whether
  F2025/W2026's divergence is a real market shift or an Amazon-posting-
  concentration artifact. Flagged explicitly as unconfirmed — the
  Analyst agent should surface this caveat, not present F2025/W2026
  findings with the same confidence as earlier semesters.

Each `.md` file has a small frontmatter block (doc_type, topic,
taxonomy_version, status, scope, source, last_updated) — `add_to_faiss_
index.py` parses this into document metadata automatically, matching the
`doc_type` pattern already used in your news/programs corpora.

## What's NOT in here

Structured/tabular data (cluster assignments, per-semester skill
frequency tables, the ARI matrix and source-mix table as raw numbers) is
**not** included here — it's in the sibling `02_STRUCTURED_DATA/` bundle
instead, meant for a CSV/pandas-based lookup tool rather than semantic
search. Mixing raw tables into a vector index tends to hurt retrieval
precision, so we kept them separate on purpose.

## Running it

```bash
cd 01_FAISS_ADDITIONS
python add_to_faiss_index.py --index-path /path/to/your/skills_faiss_index --dry-run
```

Run with `--dry-run` first — it loads and chunks everything and prints a
summary without touching your index. Once that looks right, drop
`--dry-run` to actually load your index, add the new documents, and save
it back in place.

Needs `langchain`, `langchain-community`, `faiss-cpu`, and Ollama running
locally with `mxbai-embed-large` pulled (same embedding model your
existing index uses, per the technical log — worth double-checking this
hasn't changed, since a mismatched embedding model would silently corrupt
the index's similarity space rather than throwing an error).

## Smoke-test after adding

A couple of queries that should return the new content if the add
worked:

- `"large language models demand trend"` → should surface
  `trend_analysis_summary.md` content and/or the `Large Language Models`
  / `Llms` skill docs.
- `"is a master's degree still worth it salary"` → should surface
  `salary_education_summary.md`.
- `"can I trust the 2025 2026 data"` → should surface
  `source_mix_caveat.md`.

## V1 vs V2 taxonomy

See `prompt_update_v1_handling.md` — we're recommending a prompt-layer
fix (tell the Analyst agent to prefer V2-tagged entries) rather than
re-embedding V1 content, to avoid a retrieval-crowding risk. Read that
file before deciding how to handle it.
