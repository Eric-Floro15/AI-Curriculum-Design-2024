# Notes for `cluster_tool.py` — frequency-lookup bug + taxonomy version

## 1. Known bug: `frequency=0` for most skills in some clusters

While validating the Cluster Interpreter agent's specialist-coverage case
(University Programs eval), a live `cluster_detail(2)` / `cluster_detail(4)`
pull from `cluster_tool.py` showed nearly every skill in Clusters 2 and 4
returning `frequency=0` from `Grouped_Skills_Categorized_Updated.xlsx` —
only "Oracle" (freq=7, Cluster 2) came back non-zero. That's implausible;
real postings clearly mention cloud-storage and streaming-infrastructure
skills.

Suspected cause: a skill-name lookup mismatch between
`clust_ensembled_results.csv`'s skill strings and the frequency XLSX's
skill strings — likely exact-string-match failures on compound names (e.g.
"Columnar databases (HBase Apache Kudu)"). Whatever `_load_frequencies()`
is doing internally, it isn't matching on a normalized/canonical key.

**This was never fixed** — flagged in the technical log as out of scope
for the eval-coverage task it was found during. Any frequency-grounded
assertion already made using this tool should be treated as
possibly-partially-broken until it's fixed and re-validated.

**Suggested fix:** match on `canonical_key` (the same
`.str.split('|').str[0].str.strip()` normalization used everywhere else in
this project — see CLAUDE.md Critical Rule #5) rather than raw skill
strings. The V2 taxonomy file (see below) already has a `canonical_key`
column precomputed, which should make this a straightforward join instead
of a fuzzy-matching problem.

## 2. Taxonomy version: `cluster_tool.py` is reading V1, not V2

`_load_frequencies()` currently points at
`Grouped_Skills_Categorized_Updated.xlsx` — the V1 taxonomy (4,824 rows,
~871 canonical skills, no `is_generic` flag, no `canonical_key` column).

The current authoritative taxonomy is V2:
`Grouped_Skills_Categorized_V2.xlsx` (5,090 rows, 1,129 canonical groups
including generic; 1,058 canonical non-generic skills). V2 fixed category
inconsistencies present in V1 and added an `is_generic` flag (315 rows to
exclude) and a precomputed `canonical_key` column.

**Recommendation:** repoint `cluster_tool.py` at V2, filter
`is_generic == 0`, and join on `canonical_key`. Fixing this at the same
time as the frequency-lookup bug above is probably more efficient than two
separate patches, since both point at the same underlying fix (stop
matching on raw skill strings from two independently-typed files).

The `skill_v2_*` documents in `01_FAISS_ADDITIONS/documents/v2_taxonomy_skills.jsonl`
already carry `frequency` (as of the current V2 taxonomy) and `cluster_id`
(current W2026 clustering) per skill, precomputed and correctly joined on
`canonical_key` — if it's easier, `cluster_tool.py`'s frequency lookups
could read directly from that JSONL instead of re-deriving the join from
the raw xlsx.

## 3. Data included in this bundle relevant to this fix

- `reports/cluster_assignments_w2026.csv` — the current `clust_ensembled_results.csv`
  (1,058 skills, 10 clusters), copied as-is.
- `01_FAISS_ADDITIONS/documents/v2_taxonomy_skills.jsonl` — one doc per
  canonical V2 skill, already joined to its W2026 cluster ID and its V2
  frequency, so you can spot-check the fix against known-good numbers.
