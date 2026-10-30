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
    # v60: pre-unified-corpus W2026 labels (2026-09-24 relabel, now replaced)
    # "Machine Learning & Generative AI" is NOT stale — it moved to cluster 2 (same string)
    "Cloud, DevOps & AI Systems Deployment",     # was cluster 2, now gone
    "Data Engineering & Data Platforms",         # was cluster 3, now cluster 3 (renamed)
    "Business Intelligence & Data Communication",# was cluster 4
    "Office Productivity, Business Analysis & Admin Tools",  # was cluster 5
    "Cross-cutting analytical & collaboration terms (heterogeneous)",  # was cluster 6
    "Data Science & Statistical Foundations",    # was cluster 7
    "Training & community terms (heterogeneous)",# was cluster 8
    "Niche & Emerging ML/AI Tooling (heterogeneous)",  # was cluster 9
    "Strategic Planning, Program Management & Business Development",   # was cluster 10
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
                       "ai engineering", "ai-enabled", "genai", "nlp", "llm",
                       "core ai")  # v60: cluster 5 "Core AI, Cloud & Data-Platform Engineering"
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
    "FOCUSED_CLUSTERS == {1, 2, 3, 5, 6} (coherent technical clusters, "  # v60b2: computed
    "excludes tiny/incoherent catch-alls 8/9 and broad soft-skill "
    "clusters 4/7/10; 6 now included by the rule: >=20 skills, >=90% technical, "
    "median W2026 freq >=0.1%)",
    FOCUSED_CLUSTERS == {1, 2, 3, 5, 6},
    f"got {sorted(FOCUSED_CLUSTERS)}",
)

_check(
    "old stale FOCUSED_CLUSTERS set {1, 4, 7, 9, 10} is NOT the current value",
    FOCUSED_CLUSTERS != {1, 4, 7, 9, 10},
)


# =====================================================================
# (e) Live cluster sizes match the paper's canonical V4 set exactly
# =====================================================================

# v60: unified-corpus W2026 partition sizes 47/131/89/21/370/66/98/9/3/128
_CANONICAL_SIZES_SORTED = sorted([370, 131, 128, 98, 89, 66, 47, 21, 9, 3], reverse=True)

_clusters = all_clusters()
_check(
    "all_clusters() returns exactly 10 clusters",
    len(_clusters) == 10,
    f"got {len(_clusters)}",
)

_live_sizes_sorted = sorted((c["skill_count"] for c in _clusters), reverse=True)
_check(
    "live cluster sizes match the unified-corpus W2026 set "
    "(370/131/128/98/89/66/47/21/9/3, sum 962)",  # v60
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
    "cluster_detail(1) skill_count == 47 (v60 unified-corpus)",  # v60
    _detail_1["skill_count"] == 47,
    f"got {_detail_1['skill_count']}",
)

_detail_8 = cluster_detail(8)  # v60: cluster 8 is now the near-zero niche cluster (9 skills)
_check(
    "cluster_detail(8) skill_count == 9 (near-zero niche cluster, v60)",  # v60
    _detail_8["skill_count"] == 9,
    f"got {_detail_8['skill_count']}",
)
_check(
    "cluster_detail(8) is NOT in FOCUSED_CLUSTERS",
    not _detail_8["focused"],
)


# =====================================================================
# Data files present at the paths cluster_tool.py expects (untouched)
# =====================================================================

_check(
    "CLUSTER_RESULTS_FILE exists",
    os.path.isfile(cluster_tool.CLUSTER_RESULTS_FILE),
    f"path={cluster_tool.CLUSTER_RESULTS_FILE}",
)
_check(
    "SKILL_FREQ_CSV exists",
    os.path.isfile(cluster_tool.SKILL_FREQ_CSV),
    f"path={cluster_tool.SKILL_FREQ_CSV}",
)
_check(  # v60
    "MEMBERSHIP_CONFIDENCE_FILE exists (new in v60)",
    cluster_tool.MEMBERSHIP_CONFIDENCE_FILE is not None
    and os.path.isfile(cluster_tool.MEMBERSHIP_CONFIDENCE_FILE),
    f"path={cluster_tool.MEMBERSHIP_CONFIDENCE_FILE}",
)


# =====================================================================
# CLUSTER_THEMES sync test — build_index.py vs cluster_tool.py  (v60b2)
# Uses ast parsing to avoid env-var / import-order side effects.
# =====================================================================

def _extract_cluster_themes_via_ast(filepath: str) -> dict:
    """Return CLUSTER_THEMES dict from a source file via ast, no imports."""
    import ast as _ast
    with open(filepath, encoding="utf-8") as _fh:
        _source = _fh.read()
    _tree = _ast.parse(_source, filename=filepath)
    for _node in _ast.walk(_tree):
        if (
            isinstance(_node, _ast.Assign)
            and any(
                isinstance(t, _ast.Name) and t.id == "CLUSTER_THEMES"
                for t in _node.targets
            )
        ):
            return _ast.literal_eval(_node.value)
    raise ValueError(f"CLUSTER_THEMES not found in {filepath}")

_BUILD_INDEX_PATH = os.path.join(_CHATBOT_DIR, "build_index.py")
_CLUSTER_TOOL_PATH = os.path.join(_HERE, "cluster_tool.py")

try:
    _themes_build  = _extract_cluster_themes_via_ast(_BUILD_INDEX_PATH)
    _themes_cltool = _extract_cluster_themes_via_ast(_CLUSTER_TOOL_PATH)
    _check(
        "CLUSTER_THEMES in build_index.py == CLUSTER_THEMES in cluster_tool.py (v60b2 sync)",
        _themes_build == _themes_cltool,
        f"build_index keys={sorted(_themes_build)} cltool keys={sorted(_themes_cltool)}",
    )
except Exception as _exc:
    _check(
        "CLUSTER_THEMES sync ast-parse succeeded",
        False,
        f"parse error: {_exc}",
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
