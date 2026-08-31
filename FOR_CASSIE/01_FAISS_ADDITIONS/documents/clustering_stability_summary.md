---
doc_type: analysis_summary
topic: clustering_stability
taxonomy_version: V2
status: current
scope: 7 semesters (F2022, W2023, F2023, W2024, F2024, F2025, W2026)
source: memory/projects/re-analysis-and-clustering.md
last_updated: 2026-07-27
---

# Clustering Stability Across Semesters (Adjusted Rand Index)

Each semester's job postings were independently re-clustered (CSPA
ensemble, same pipeline as the current W2026 clustering) and compared
pairwise using Adjusted Rand Index (ARI) — a measure of how similarly two
independent clustering runs group the same skills, ranging 0 (no
agreement beyond chance) to 1 (identical grouping).

| | F2022 | W2023 | F2023 | W2024 | F2024 | F2025 | W2026 |
|---|---|---|---|---|---|---|---|
| F2022 | 1.00 | .402 | .393 | .383 | .412 | .289 | .233 |
| W2023 | .402 | 1.00 | .393 | .472 | .515 | .329 | .258 |
| F2023 | .393 | .393 | 1.00 | .523 | .451 | .299 | .262 |
| W2024 | .383 | .472 | .523 | 1.00 | .561 | .322 | .297 |
| F2024 | .412 | .515 | .451 | .561 | 1.00 | .319 | .298 |
| F2025 | .289 | .329 | .299 | .322 | .319 | 1.00 | **.416** |
| W2026 | .233 | .258 | .262 | .297 | .298 | **.416** | 1.00 |

## What this shows

The five semesters F2022–F2024 agree with each other reasonably well
(ARI 0.38-0.56) — the skill-cluster structure is fairly stable across
that stretch. F2025 and W2026 each agree with every one of those five at
only 0.24-0.33, but agree with **each other** at 0.416 — clearly the
highest value either of them has with any other semester. They form a
distinct, matched pair, not independent anomalies.

This pairing lines up with two other independent signals from the same
two semesters (see the trend-analysis and source-mix-caveat documents):
skill-demand intensity and Master's-degree share both peak and then
reverse starting at F2025, and F2025/W2026 both show anomalously high
Amazon-related posting concentration. Three independent signals
converging on the same two semesters is fairly strong evidence that
something about the *data* (not the market) shifted at F2025 — see the
source-mix caveat document for the leading hypothesis and what would
confirm or rule it out.

**Practical implication for the chatbot:** if asked to compare cluster
membership or skill groupings across semesters, F2025/W2026 clusters
should not be treated as directly comparable to F2022-F2024 clusters
without flagging this caveat — cluster IDs are also not stable/matched
across independent runs (cluster "3" in one semester's run has no
guaranteed relationship to cluster "3" in another's).
