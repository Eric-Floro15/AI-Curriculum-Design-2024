# Task 04 — Repoint the chatbot to the clean V4 clusters + rebuild FAISS

`chatbot/build_index.py` still points at the V2 taxonomy and the old 2025 cluster file. The good
news: **V4 is schema-compatible** — `build_index.py` already reads `canonical_key`,
`Level 1 Category`, `Level 2 Category (Canonical)`, `Description`, `Date`, `Frequency`, `Skills`,
and V4 has every one of those columns. So the repoint is **three edits**, no code changes.

See `build_index_repoint.md` for the exact diff. Summary:

1. `SKILLS_FILE` → `SKILLS-LISTS/Grouped_Skills_Categorized_V4.xlsx` (canonical repo copy; already
   cleaned). V4 has ~1,015 canonical groups (V2 had 1,129), so the index will hold ~1,015 skill docs.
2. `CLUSTER_FILE` → `RE-ANALYSIS-2026/pipeline_runs/W2026/clust_ensembled_results.csv` (the clean
   Winter-2026 partition; already in the exact `Cluster,Skill` format `load_cluster_map` expects). A
   convenience copy is in this folder as `clust_ensembled_results_W2026_clean.csv`, but prefer the
   repo path so it stays current.
3. `CLUSTER_THEMES` → replace with the **new W2026 labels from Task 01**. This is why Task 01 comes
   first. A paste-ready stub is in `build_index_repoint.md` with the cluster numbers pre-filled;
   drop in the theme strings once you've labeled them.

Then rebuild the index (`python chatbot/build_index.py`) and smoke-test retrieval.

**Verify after rebuild:** the cluster join is by `canonical_name.lower()`; on the clean data this
matched all 962 clustered skills with zero misses, so `load_cluster_map` should report ~962 skills
with cluster labels and no "cluster not found" spam. If many skills come back cluster -1, the Skill
casing in the cluster file drifted — check that first.
