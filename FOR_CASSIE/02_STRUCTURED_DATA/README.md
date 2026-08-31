# Structured Data — for CSV/pandas lookup, not FAISS

These are structured/tabular analysis outputs, meant to be queried
directly (pandas, a CSV tool, whatever `cluster_tool.py` ends up being)
rather than embedded into the vector index. Semantic search is good at
"what does this mean," bad at "give me the exact number for X" — that's
the split this bundle reflects.

## `reports/`

- **`cluster_assignments_w2026.csv`** — the current, authoritative
  clustering result (`clust_ensembled_results.csv`, copied as-is): 1,058
  skills, 10 clusters (sizes 22/5/137/148/332/6/212/127/33/36). Columns:
  `Cluster`, `Skill`. Note: cluster themes/labels haven't been assigned
  yet for this W2026 clustering (that's flagged as future work in the
  paper) — don't infer theme names from the old D1 cluster labels in
  CLAUDE.md, they're from a different, earlier clustering run and don't
  carry over.
- **`skill_frequency_by_semester.csv`** — 1,058 skills × 7 semesters
  (F2022, W2023, F2023, W2024, F2024, F2025, W2026), values are % share
  of postings mentioning that skill in that semester. W2025 is excluded
  (confirmed duplicate of F2024 — see `cluster_tool_bugfix_notes.md`'s
  sibling context in the top-level README, or `memory/projects/re-
  analysis-and-clustering.md` for the full diagnostic).
- **`salary_by_degree_vs_bachelors.csv`** — Master's/PhD salary premium
  over Bachelor's, per semester.
- **`salary_by_degree_vs_market_median.csv`** — Bachelor's/Master's/PhD
  salary position relative to that semester's own overall median.
- **`clustering_stability_ari_matrix.csv`** — pairwise Adjusted Rand
  Index across all 7 semesters (7×7 matrix).
- **`source_mix_by_semester.csv`** — posting counts, top-10-company
  share, and Amazon-related posting share per semester — the data behind
  the F2025/W2026 source-composition caveat.

All of these are also summarized in prose in
`01_FAISS_ADDITIONS/documents/` if you want the "what does this mean"
version alongside the raw numbers — the prose versions cite the same
underlying figures.

## `cluster_tool_bugfix_notes.md`

Two related, previously-flagged-but-unfixed issues in `cluster_tool.py`:
a frequency-lookup bug (most skills in some clusters return `frequency=0`
due to a string-matching mismatch) and the fact that it's still reading
the V1 taxonomy file instead of V2. Full detail and a suggested fix in
that file.
