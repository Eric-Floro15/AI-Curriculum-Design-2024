# build_index.py — exact repoint

## 1. SKILLS_FILE
```python
# before
SKILLS_FILE = os.path.join(PROJECT_ROOT, "SKILLS-LISTS", "Grouped_Skills_Categorized_V2.xlsx")
# after
SKILLS_FILE = os.path.join(PROJECT_ROOT, "SKILLS-LISTS", "Grouped_Skills_Categorized_V4.xlsx")
```

## 2. CLUSTER_FILE
```python
# before
CLUSTER_FILE = os.path.join(
    PROJECT_ROOT, "2024-AND-2025-FILES", "Final Files Re-Running 2025", "clust_ensembled_results.csv"
)
# after
CLUSTER_FILE = os.path.join(
    PROJECT_ROOT, "RE-ANALYSIS-2026", "pipeline_runs", "W2026", "clust_ensembled_results.csv"
)
```

## 3. CLUSTER_THEMES — fill from Task 01 labels
The clean W2026 cluster numbers and sizes are below; replace each theme string with the label you
assign in Task 01. Flag the small/incoherent clusters (6, 8, 9) rather than inventing a theme.
```python
CLUSTER_THEMES = {
    1:  "",   # 174 skills — ML / Generative AI / NLP core
    2:  "",   # 282 skills — large AI-infrastructure cluster (the agentic-adjacent one)
    3:  "",   # 159 skills — Python / SQL / cloud / optimization foundations
    4:  "",   # 71  skills — communication & BI / dashboards
    5:  "",   # 54  skills — office / business analysis
    6:  "",   # 2   skills — small; likely disclose as incoherent
    7:  "",   # 69  skills — data analytics / BI / Excel / finance
    8:  "",   # 2   skills — small; likely disclose as incoherent
    9:  "",   # 12  skills — small / niche
    10: "",   # 137 skills — strategy / sales / project management
}
```
(The hints after each cluster are orientation only — use your Task 01 labels as the source of truth.)
