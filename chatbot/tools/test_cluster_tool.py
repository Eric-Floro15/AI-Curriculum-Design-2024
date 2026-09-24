"""
test_cluster_tool.py — offline unit tests for the 2026-09-24 cluster
relabel (CLOSELOOP workstream a).

The Cluster Interpreter's underlying DATA was already correct (clean
W2026 / V4 partition), but CLUSTER_THEMES / FOCUSED_CLUSTERS in
cluster_tool.py, and the hardcoded CLUSTER REFERENCE block in
cluster_interpreter.py's backstory, were two generations stale (labels
from the old pre-clean partition, applied to the new partition's
different cluster IDs). This produced wrong labels in real runs — e.g.
run_20260917T225459Z (behind Appendix G.3) labeled the 174-skill ML/GenAI
cluster "Security & Applied AI Engineering" and the 159-skill
data-engineering cluster "Leadership, Program Management & Strategy".

This file checks the fix, offline, no LLM/API calls:
  (a) CLUSTER_THEMES has all 10 live cluster ids.
  (b) No label is one of the known-stale strings from the old partition.
  (c) A light membership sanity check — the cluster whose top skills
      include LangChain/RAG/agentic-adjacent tooling is labeled with an
      ML/GenAI/AI-engineering theme, not a DevOps/soft-skills theme.
  (d) FOCUSED_CLUSTERS matches the new, deliberately-chosen set and
      excludes the tiny/incoherent catch-alls.
  (e) Live cluster sizes match the paper's canonical V4 set exactly
      (proves clust_ensembled_results_W2026_clean.csv is the clean
      partition, not a stale file).
  (f) all_clusters()/cluster_detail() actually surface the new labels
      (not hardcoded strings drifting from the dict).

Run:
    python chatbot/tools/test_cluster_tool.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

import tools.cluster_tool as cluster_tool  # noqa: E402
from tools.cluster_tool import (  # noqa: E402
    CLUSTER_THEMES,
    FOCUSED_CLUSTERS,
    all_clusters,
    cluster_detail,
)

_FAILURES = []


def _check(label: str, condition: bool, detail: str = "") -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail and not condition else ""))
    if not condition:
        _FAILURES.append(label)


# =====================================================================
# (a) CLUSTER_THEMES has all 10 live cluster ids
# =====================================================================

_check(
    "CLUSTER_THEMES has exactly cluster ids 1-10",
    set(CLUSTER_THEMES.keys()) == set(range(1, 11)),
    f"got {sorted(CLUSTER_THEMES.keys())}",
)

_check(
    "every CLUSTER_THEMES value is a non-empty string",
    all(isinstance(v, str) and v.strip() for v in CLUSTER_THEMES.values()),
)


# =====================================================================
# (b) No label is one of the known-stale strings (old pre-clean partition)
# =====================================================================

_STALE_LABELS = {
    # cluster_tool.py's old (pre-2026-09-24) CLUSTER_THEMES
    "Security & Applied AI Engineering",
    "Software Architecture & Human-Centered Design",
    "Leadership, Program Management & Strategy",
    "AI/ML Core — Generative AI, NLP & LLMs",
    "Cloud, Infrastructure & Systems Engineering",
    "Software Dev Tools — Mobile & Scientific",
    "Data Analytics, Science & Engineering",
    "Communication, Problem-Solving & Office Tools",
    "DevOps, Agile & Automation",
    "Business Intelligence & Analytical Thinking",
    # cluster_interpreter.py's even-older (V1, 766-skill) CLUSTER REFERENCE
    "Collaboration & Leadership Core",
    "Cloud Databases & Storage",
    "Large Mixed — Diverse Soft + Technical",
    "Data Infrastructure & Streaming",
    "Mixed — Responsible AI, Dev Tools",
    "Business & Management Core",
    "ML Algorithms & Statistical Modelling",
    "Data Engineering — Pipelines & Big Data",
    "Core Analytical Tools",
    "Large Mixed — Ethics, Soft Skills",
}

for cid, label in CLUSTER_THEMES.items():
    _check(
        f"Cluster {cid} label is not a known-stale string",
        label not in _STALE_LABELS,
        f"label={label!r}",
    )


# =====================================================================
# (c) Membership sanity check — agentic/ML-adjacent skills land in an
#     ML/GenAI/AI-engineering-themed cluster, not a DevOps/soft-skills one
# =====================================================================

_AGENTIC_ADJACENT_SKILLS = [
    "LangChain", "CrewAI", "LangGraph", "Agentic Frameworks", "AutoGen",
    "LlamaIndex", "Generative AI",
]
_ML_THEME_KEYWORDS = ("machine learning", "deep learning", "generative ai",
                       "ai engineering", "ai-enabled", "genai", "nlp", "llm")
_WRONG_THEME_KEYWORDS = ("devops", "office", "business intelligence",
                          "strategic planning", "communication")


def _cluster_id_for_skill(skill_csv_name: str) -> int | None:
    df = cluster_tool._load_clusters()
    row = df[df["Skill"].str.lower() == skill_csv_name.lower()]
    return int(row.iloc[0]["Cluster"]) if len(row) else None


_agentic_cluster_ids = set()
for skill in _AGENTIC_ADJACENT_SKILLS:
    cid = _cluster_id_for_skill(skill)
    if cid is not None:
        _agentic_cluster_ids.add(cid)

_check(
    "at least one agentic-adjacent skill (LangChain/CrewAI/etc.) found in the live CSV",
    len(_agentic_cluster_ids) > 0,
)

for cid in _agentic_cluster_ids:
    label_lower = CLUSTER_THEMES.get(cid, "").lower()
    has_ml_theme = any(kw in label_lower for kw in _ML_THEME_KEYWORDS)
    has_wrong_theme = any(kw in label_lower for kw in _WRONG_THEME_KEYWORDS) and not has_ml_theme
    _check(
        f"Cluster {cid} (contains agentic-adjacent skills) is labeled with an "
        f"ML/GenAI/AI-engineering theme, not a DevOps/soft-skills theme",
        has_ml_theme and not has_wrong_theme,
        f"label={CLUSTER_THEMES.get(cid)!r}",
    )


# =====================================================================
# (d) FOCUSED_CLUSTERS is the new, deliberately-chosen set
# =====================================================================

_check(
    "FOCUSED_CLUSTERS == {1, 2, 3, 7} (coherent technical clusters, "
    "excludes tiny/incoherent catch-alls 6/8/9 and broad soft-skill "
    "clusters 4/5/10)",
    FOCUSED_CLUSTERS == {1, 2, 3, 7},
    f"got {sorted(FOCUSED_CLUSTERS)}",
)

_check(
    "old stale FOCUSED_CLUSTERS set {1, 4, 7, 9, 10} is NOT the current value",
    FOCUSED_CLUSTERS != {1, 4, 7, 9, 10},
)


# =====================================================================
# (e) Live cluster sizes match the paper's canonical V4 set exactly
# =====================================================================

_CANONICAL_SIZES_SORTED = sorted([282, 174, 159, 137, 71, 69, 54, 12, 2, 2], reverse=True)

_clusters = all_clusters()
_check(
    "all_clusters() returns exactly 10 clusters",
    len(_clusters) == 10,
    f"got {len(_clusters)}",
)

_live_sizes_sorted = sorted((c["skill_count"] for c in _clusters), reverse=True)
_check(
    "live cluster sizes match the paper's canonical V4 set "
    "(282/174/159/137/71/69/54/12/2/2, sum 962)",
    _live_sizes_sorted == _CANONICAL_SIZES_SORTED,
    f"got {_live_sizes_sorted}",
)

_check(
    "live cluster sizes sum to 962 (the clean W2026 skill count)",
    sum(c["skill_count"] for c in _clusters) == 962,
    f"got {sum(c['skill_count'] for c in _clusters)}",
)


# =====================================================================
# (f) all_clusters()/cluster_detail() actually surface the new labels
# =====================================================================

for c in _clusters:
    expected = CLUSTER_THEMES[c["cluster_id"]]
    _check(
        f"all_clusters() cluster {c['cluster_id']} theme matches CLUSTER_THEMES dict",
        c["theme"] == expected,
        f"got {c['theme']!r}, expected {expected!r}",
    )
    expected_focused = c["cluster_id"] in FOCUSED_CLUSTERS
    _check(
        f"all_clusters() cluster {c['cluster_id']} 'focused' flag matches FOCUSED_CLUSTERS",
        c["focused"] == expected_focused,
    )

_detail_1 = cluster_detail(1)
_check(
    "cluster_detail(1) theme matches CLUSTER_THEMES[1]",
    _detail_1["theme"] == CLUSTER_THEMES[1],
)
_check(
    "cluster_detail(1) skill_count == 174",
    _detail_1["skill_count"] == 174,
    f"got {_detail_1['skill_count']}",
)

_detail_6 = cluster_detail(6)
_check(
    "cluster_detail(6) skill_count == 2 (tiny residual cluster)",
    _detail_6["skill_count"] == 2,
    f"got {_detail_6['skill_count']}",
)
_check(
    "cluster_detail(6) is NOT in FOCUSED_CLUSTERS",
    not _detail_6["focused"],
)


# =====================================================================
# Data files present at the paths cluster_tool.py expects (untouched)
# =====================================================================

_check(
    "CLUSTER_RESULTS_FILE exists (data file untouched by this relabel)",
    os.path.isfile(cluster_tool.CLUSTER_RESULTS_FILE),
    f"path={cluster_tool.CLUSTER_RESULTS_FILE}",
)
_check(
    "V4_TAXONOMY_XLSX exists (data file untouched by this relabel)",
    os.path.isfile(cluster_tool.V4_TAXONOMY_XLSX),
    f"path={cluster_tool.V4_TAXONOMY_XLSX}",
)


# =====================================================================
# Summary
# =====================================================================
print(f"\n{'='*60}")
if _FAILURES:
    print(f"{len(_FAILURES)} FAILURE(S):")
    for f in _FAILURES:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("ALL CHECKS PASSED")
