---
doc_type: analysis_summary
topic: skill_demand_trends
taxonomy_version: V2
status: current
scope: 7 semesters (F2022, W2023, F2023, W2024, F2024, F2025, W2026)
source: RE-ANALYSIS-2026/notebooks/cross_year_feature_analysis.ipynb
last_updated: 2026-07-27
---

# Cross-Semester Skill Demand Trends (F2022 → W2026)

This covers seven semesters of job-posting data (Fall 2022 through Winter
2026; Winter 2025 was excluded — see the source-mix caveat document, it
turned out to be duplicate F2024 data from a scraping issue, not
independent data).

## AI/GenAI skills are rising fast, in both demand share and salary

"Ai" (as a tagged skill) appears in 18.2% of postings in F2022 and 46.1%
by W2026 — the single largest riser in the dataset, both in absolute share
and in slope (+8.4 percentage points/year). Close behind: Large Language
Models (0.7% → 11.5%), LLMs (0.05% → 12.3%), Generative AI (0.3% →
10.8%), Open Source Frameworks (12.6% → 28.2%). These aren't fringe
movements — LLM/GenAI-specific mentions went from essentially absent in
F2022 to appearing in roughly 1 in 8 postings by W2026.

Salaries for these skills rose too, not just demand share. Median salary
for "Ai"-tagged postings: $139,000 (F2022) → $156,138 (W2026), +12.3%.
Large Language Models: $149,625 → $176,000, +17.6%. Generative AI:
$166,500 (W2023, first semester it appears) → $175,000, +5.1%.

## Classic ML/stats/data-science stack: losing demand share, not losing pay

This is the more counterintuitive finding, worth stating carefully because
it's easy to misread. Skills like Statistics, Data Science, R, Machine
Learning, Data Analysis, Mathematics, Algorithms, Data Visualization, SQL,
and SQL Databases all show declining *share* of postings over the same
period — e.g. Machine Learning: 32.8% → 22.7% of postings (-3.1
pp/year), Statistics: 27.0% → 13.5% (-4.2 pp/year), SQL: 43.1% → 34.8%.

But median salary for every one of these same skills *rose* over the same
window — Machine Learning: $134,500 → $168,000 (+24.9%), Statistics:
$117,000 → $140,000 (+19.7%), R: $115,000 → $139,745 (+21.5%), SQL:
$114,400 → $132,300 (+15.6%).

**Read this as: these skills are becoming more baseline/assumed rather
than obsolete.** They're mentioned explicitly in a shrinking fraction of
postings (possibly because they're increasingly assumed rather than
called out, or increasingly folded into "AI/ML" as an umbrella term)
while still commanding rising pay for the people who have them. This is
not evidence that a curriculum should drop core stats/ML/SQL coverage —
if anything the salary data argues the opposite.

## Curriculum implication

The clearest actionable signal: LLM/GenAI topics went from a niche
elective-worthy mention to a mainstream, high-growth, high-salary skill
set within about three years of data. A program that hasn't already
integrated LLM/GenAI content into its core (not just as an elective) is
likely behind current market demand. At the same time, the core
statistics/ML/data-engineering foundation shouldn't be deprioritized —
declining posting-share doesn't mean declining relevance, and the salary
trend for that stack still points up.
