---
doc_type: analysis_caveat
topic: source_composition_artifact
taxonomy_version: V2
status: current — unresolved open question
scope: F2025 and W2026 specifically
source: memory/projects/re-analysis-and-clustering.md
last_updated: 2026-07-27
---

# Open Caveat: F2025/W2026 May Be a Source-Composition Artifact, Not a Market Shift

This is an explicitly unresolved question. If the chatbot is asked about
recent (2025-2026) trends, it should surface this caveat rather than
stating F2025/W2026 numbers as confirmed market findings.

## What was found

| Semester | Postings | Top-10-company share | Amazon-related share |
|---|---|---|---|
| F2022 | 41,588 | 5.0% | 0.8% |
| W2023 | 44,681 | 4.2% | 0.1% |
| F2023 | 30,948 | 4.5% | 0.8% |
| W2024 | 24,803 | 4.8% | 0.8% |
| F2024 | 27,733 | 3.6% | 0.7% |
| **F2025** | 29,593 | **5.4%** | **2.7%** |
| **W2026** | 23,822 | **6.7%** | **3.7%** |

F2025 and W2026 are clear outliers on Amazon-related posting
concentration (2.7%/3.7% vs. 0.1-0.8% for every other semester); W2026
additionally has Amazon appearing 4 separate times in its top-10 poster
list under different name variants (likely different subsidiaries/business
units posting separately).

The same two semesters are also where skill-demand intensity (median
skills/posting) and Master's-degree share both reverse after rising
smoothly and monotonically through every prior semester, and where
clustering stability (ARI) diverges from every other semester while
matching *each other* strongly (0.416, see clustering-stability
document). Three independent signals converge on exactly these two
semesters.

## What this means (and doesn't mean, yet)

This is meaningfully stronger evidence for a source/company-composition
artifact (Amazon-heavy postings likely following a distinctive templated
skill-listing style that reads differently to the extraction pipeline)
than for a genuine two-semester reversal in market demand. But it is not
confirmed — the robustness check that would confirm or rule it out
(re-computing skill-demand/education/clustering trends for F2025 and
W2026 with Amazon-tagged postings excluded or down-weighted, and seeing
whether the reversal disappears or shrinks) has not yet been run as of
this writing.

**If asked about F2025 or W2026 trends specifically, the honest answer
is: "the raw numbers show X, but there's an open question about whether
this reflects a real market shift or an artifact of unusually high
Amazon-posting concentration in exactly those two semesters — the
robustness check to resolve this hasn't been run yet."** Do not present
F2025/W2026 findings with the same confidence as F2022-F2024 findings.
