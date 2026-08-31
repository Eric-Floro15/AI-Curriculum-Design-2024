# Task 06 — Lift-table tool handoff (frozen)

Two artifacts, both frozen and both **clustering-invariant** — they are computed straight off the
posting × skill presence matrix, so the description-cleaning re-clustering did not change them.

## `skill_lift_table.csv` — the precomputed all-pairs table

7,054 skill→skill associations over 492 focal skills, at the reporting cut (lift ≥ 3 and log-odds
z ≥ 2). Columns: `skill, associated_skill, n_together, pct_of_skill_postings, pct_of_all_postings,
lift, z`. This is the same 7,054-association table §4.6.4 refers to.

**How the Analyst agent should query it:** for "what skills go with X", filter
`skill == X` and sort by **`z` descending** — where lift and z disagree, believe z (lift is
unshrunk and inflates rare pairs). Use it for fast, precomputed skill-co-occurrence lookups.

## `lift_analysis.py` — the live tool for arbitrary segments

The precomputed table covers skill→skill only. For a segment defined by a sector, seniority, or
geography, run the tool live (it needs `skill_presence_matrix.csv` + `posting_attributes.csv`):

```bash
python lift_analysis.py --skill "Agentic Ai"                                  # skill segment
python lift_analysis.py --where "industry=Finance & Insurance"                # sector segment
python lift_analysis.py --where "industry=Finance & Insurance" --where "job_level>=6"
python lift_analysis.py --skill "Agentic Ai" --semesters W2026 F2025 --top 30
```

Method (all in the docstring): independent min-count filter (default 25) → lift =
P(skill|segment)/P(skill|baseline) → Fightin'-Words log-odds z with an informative Dirichlet prior
(Monroe et al. 2008) → Fisher exact one-sided → Benjamini–Hochberg FDR within the segment. **No
network, no LLM.**

## Why this matters for the chatbot

Lift is the backbone the paper leans on precisely because it is invariant to clustering method,
feature set and skill ordering — a claim that survives lift survives every clustering choice, whereas
a claim resting on two skills sharing a cluster does not (§4.6, §7). So the Analyst / Cluster
Interpreter agents should treat lift as the primary evidence for "what goes with what," and cluster
membership as hypothesis-generating. The compose method in Task 05 is the same machinery applied to
two marginals at once.

## Status

Frozen as of the current corpus. Eric ships this pair once the analysis is 100% locked (it now is on
the clustering side); if a later corpus refresh happens, regenerate the table with the same tool.
