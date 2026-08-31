---
doc_type: analysis_summary
topic: education_salary_trends
taxonomy_version: V2
status: current
scope: 7 semesters (F2022, W2023, F2023, W2024, F2024, F2025, W2026)
source: RE-ANALYSIS-2026/notebooks/cross_year_feature_analysis.ipynb (sections 9 and 9b)
last_updated: 2026-07-27
---

# Degree-Level Salary Trends (F2022 → W2026)

Two different framings of the same underlying question — does more
education pay off, and is that premium changing over time — computed two
ways for robustness.

## Framing 1: premium relative to Bachelor's degree, same semester

| Semester | Master's vs Bachelor's | PhD vs Bachelor's | PhD vs Master's |
|---|---|---|---|
| F2022 | +14.4% | +34.3% | +17.4% |
| W2023 | +14.5% | +44.9% | +26.6% |
| F2023 | +19.6% | +50.0% | +25.5% |
| W2024 | +15.5% | +43.2% | +24.0% |
| F2024 | +14.1% | +36.4% | +19.6% |
| F2025 | +13.5% | +47.9% | +30.2% |
| W2026 | +11.6% | +43.2% | +28.3% |

Master's premium over Bachelor's holds fairly steady around 12-20% across
all seven semesters, no clear rising or falling trend — no sign of
Master's-degree salary premium eroding.

## Framing 2: position relative to that semester's own overall market median

`relative_position(year, degree) = (degree_median(year) − overall_median(year)) / overall_median(year) × 100`

| Semester | Bachelor's vs median | Master's vs median | PhD vs median |
|---|---|---|---|
| F2022 | -12.2% | +0.5% | +18.0% |
| W2023 | -12.3% | +0.4% | +27.1% |
| F2023 | -12.6% | +4.5% | +31.1% |
| W2024 | -10.2% | +3.7% | +28.6% |
| F2024 | -10.0% | +2.7% | +22.8% |
| F2025 | -10.1% | +2.1% | +32.9% |
| W2026 | -8.1% | +2.6% | +31.7% |

Bachelor's sits consistently 8-13% below that semester's own market
median (mildly narrowing over time). Master's sits close to the market
median throughout (+0.4% to +4.5%, no clear trend). PhD sits well above
market every semester (+18% to +33%, noisy, no clear trend).

**Both framings agree: no evidence of a Master's-degree salary premium
eroding over this period.** This is directly relevant to the MMAI
program's value proposition — a professor asking "is a Master's still
worth it relative to a Bachelor's in this market" gets a consistent "yes,
holding steady" answer from two independently-computed angles.

## Overall salary and degree-requirement context

Median posting salary rose from $114,400 (F2022) to $135,076 (W2026).
Bachelor's-degree share of postings requiring/mentioning a degree level
rose slightly (43.5% → 49.7%), Master's share dipped slightly in the
final two semesters (32.6% F2024 → 28.8% W2026) — see the source-mix
caveat document for why F2025/W2026 numbers specifically should be read
with a grain of salt.
