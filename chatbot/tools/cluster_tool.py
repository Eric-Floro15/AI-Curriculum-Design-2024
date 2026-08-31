"""
cluster_tool.py — Tools for the Cluster Interpreter agent.

Reads chatbot/data/cluster_assignments_w2026.csv (1,058 skills, 10 CSPA
ensemble clusters, Winter 2026 run) and derives frequency data from the
V2 taxonomy JSONL at FOR_CASSIE/01_FAISS_ADDITIONS/documents/v2_taxonomy_skills.jsonl.

The co-occurrence CSVs in final_implementation/ are not used here because
the row index was not preserved during export, making skill-to-skill lookup
unreliable. The cluster membership file is the clean source of truth.

Frequency lookup change (2026-07-27):
  Previously read from Grouped_Skills_Categorized_Updated.xlsx (V1 taxonomy,
  no canonical_key column) using raw .lower() string matching, which caused
  most skills to return frequency=0 due to compound-name mismatches. Now reads
  from the V2 taxonomy JSONL where frequencies are precomputed and joined on
  canonical_key. Case-insensitive matching gives 100% coverage (1,058/1,058).

Cluster themes (Winter 2026 CSPA ensemble — provisional labels derived from
top-frequency skills per cluster; formal theme assignment is flagged as future
work in the paper):
  1  — Security & Applied AI Engineering (22 skills)
  2  — Software Architecture & Human-Centered Design (5 skills)
  3  — Leadership, Program Management & Strategy (137 skills)
  4  — AI/ML Core — Generative AI, NLP & LLMs (148 skills)
  5  — Cloud, Infrastructure & Systems Engineering (332 skills)
  6  — Software Dev Tools — Mobile & Scientific (6 skills)
  7  — Data Analytics, Science & Engineering (212 skills)
  8  — Communication, Problem-Solving & Office Tools (127 skills)
  9  — DevOps, Agile & Automation (33 skills)
 10  — Business Intelligence & Analytical Thinking (36 skills)

Exposes:
  Python API   — all_clusters(), cluster_detail(id), skill_frequency(name)
  CrewAI tools — all_clusters_tool, cluster_detail_tool
"""

import json
import os
import sys
from functools import lru_cache

import pandas as pd

# @traceable lets LangSmith record each cluster tool call as a named span,
# showing the cluster_id argument and the returned data.  Without this,
# all pandas CSV/XLSX reads are invisible in LangSmith.
try:
    from langsmith import traceable as _traceable
except ImportError:
    def _traceable(**_kw):
        """No-op when langsmith is not installed."""
        def _decorator(fn):
            return fn
        return _decorator

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
_PROJECT_ROOT = os.path.dirname(_CHATBOT_DIR)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

# ── File paths ────────────────────────────────────────────────────────────────

# Winter 2026 CSPA ensemble clustering (1,058 skills, 10 clusters).
# Supersedes the old clust_ensembled_results.csv (766 skills, V1 clustering).
CLUSTER_RESULTS_FILE = os.path.join(_CHATBOT_DIR, "data", "cluster_assignments_w2026.csv")

# V2 taxonomy JSONL — source of truth for skill frequencies.
# Frequencies are precomputed and joined on canonical_key, so no raw-string
# matching issues. Reading from here avoids the frequency=0 bug that affected
# the old Grouped_Skills_Categorized_Updated.xlsx (V1) path.
V2_TAXONOMY_JSONL = os.path.join(
    _PROJECT_ROOT, "FOR_CASSIE", "01_FAISS_ADDITIONS", "documents", "v2_taxonomy_skills.jsonl"
)

# Provisional cluster themes for the Winter 2026 CSPA ensemble.
# Derived from top-frequency skills per cluster; formal labels are flagged as
# future work in the paper — update this dict once official labels are assigned.
CLUSTER_THEMES = {
    1:  "Security & Applied AI Engineering",
    2:  "Software Architecture & Human-Centered Design",
    3:  "Leadership, Program Management & Strategy",
    4:  "AI/ML Core — Generative AI, NLP & LLMs",
    5:  "Cloud, Infrastructure & Systems Engineering",
    6:  "Software Dev Tools — Mobile & Scientific",
    7:  "Data Analytics, Science & Engineering",
    8:  "Communication, Problem-Solving & Office Tools",
    9:  "DevOps, Agile & Automation",
    10: "Business Intelligence & Analytical Thinking",
}

# Clusters worth highlighting in gap analysis (focused, high-signal technical areas).
# Excludes the large, broad-spectrum clusters (3, 5, 8) which contain diverse
# soft/general skills and are less discriminative for targeted recommendations.
FOCUSED_CLUSTERS = {1, 4, 7, 9, 10}


# ── Data loaders ─────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def _load_clusters() -> pd.DataFrame:
    """Load cluster assignments: Cluster (int), Skill (str)."""
    df = pd.read_csv(CLUSTER_RESULTS_FILE)
    df["Cluster"] = df["Cluster"].astype(int)
    df["Skill"] = df["Skill"].str.strip()
    return df


@lru_cache(maxsize=1)
def _load_frequencies() -> dict[str, int]:
    """Build skill-name → frequency lookup from the V2 taxonomy JSONL.

    Frequencies are already precomputed and joined on canonical_key in the
    JSONL, so this is a simple read — no raw-string matching, no frequency=0
    mismatch from compound skill names. Keyed by skill.lower() for
    case-insensitive lookup (confirmed 100% coverage against W2026 cluster CSV).
    """
    try:
        lookup: dict[str, int] = {}
        with open(V2_TAXONOMY_JSONL, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                doc = json.loads(line)
                meta = doc.get("metadata", {})
                skill = str(meta.get("skill", "")).strip().lower()
                freq = int(meta.get("frequency", 0))
                if skill and skill not in lookup:
                    lookup[skill] = freq
        return lookup
    except Exception:
        return {}


def _enrich_with_freq(skills: list[str]) -> list[dict]:
    """Add frequency data to a list of skill names."""
    freq_map = _load_frequencies()
    result = []
    for skill in skills:
        freq = freq_map.get(skill.lower(), 0)
        result.append({"skill": skill, "frequency": freq})
    return sorted(result, key=lambda x: x["frequency"], reverse=True)


# ── Python API ────────────────────────────────────────────────────────────────

@_traceable(name="all_clusters", run_type="tool")
def all_clusters() -> list[dict]:
    """
    Return a summary of all 10 clusters: id, theme, skill count, top skills.

    @traceable: recorded by LangSmith so every overview call shows the full
    cluster list in the trace, making it easy to verify the agent saw the
    right data before doing gap analysis.
    """
    df = _load_clusters()
    result = []
    for cid in sorted(df["Cluster"].unique()):
        skills = df[df["Cluster"] == cid]["Skill"].tolist()
        enriched = _enrich_with_freq(skills)
        top = [s["skill"] for s in enriched[:8]]
        result.append({
            "cluster_id": int(cid),
            "theme": CLUSTER_THEMES.get(cid, "Unknown"),
            "skill_count": len(skills),
            "focused": cid in FOCUSED_CLUSTERS,
            "top_skills_by_frequency": top,
        })
    return result


@_traceable(name="cluster_detail", run_type="tool")
def cluster_detail(cluster_id: int) -> dict:
    """
    Return all skills in a cluster, enriched with frequency data.

    @traceable: recorded by LangSmith so every detail drill-down shows
    exactly which cluster_id was queried and the ranked skill list returned.
    """
    df = _load_clusters()
    skills = df[df["Cluster"] == cluster_id]["Skill"].tolist()
    if not skills:
        return {"error": f"No skills found for cluster_id={cluster_id}"}
    enriched = _enrich_with_freq(skills)
    return {
        "cluster_id": cluster_id,
        "theme": CLUSTER_THEMES.get(cluster_id, "Unknown"),
        "focused": cluster_id in FOCUSED_CLUSTERS,
        "skill_count": len(skills),
        "skills": enriched,
    }


# ── CrewAI tool wrappers ──────────────────────────────────────────────────────

try:
    from crewai.tools import tool

    @tool("All Clusters Overview")
    def all_clusters_tool() -> str:
        """
        Return a complete overview of all 10 CSPA ensemble skill clusters:
        cluster ID, theme, skill count, and the top skills by market frequency.

        Use this FIRST to understand the full landscape of skill clusters before
        doing gap analysis. Each cluster represents a group of skills that
        co-occur in AI/ML job postings.

        Focused clusters (most discriminative for gap analysis): 1, 4, 7, 9, 10.
        Clusters 3, 5, and 8 are large, broad-spectrum groups — less useful for
        targeted gap-analysis recommendations.
        """
        clusters = all_clusters()
        lines = ["CSPA Ensemble Skill Clusters (10 total)\n"]
        for c in clusters:
            flag = "⭐" if c["focused"] else "  "
            top = ", ".join(c["top_skills_by_frequency"])
            lines.append(
                f"{flag} Cluster {c['cluster_id']} — {c['theme']}"
                f" ({c['skill_count']} skills)\n"
                f"   Top skills: {top}\n"
            )
        lines.append(
            "⭐ = focused cluster (high signal for gap analysis)\n"
            "Use cluster_detail_tool(cluster_id) to see all skills in a cluster."
        )
        return "\n".join(lines)

    @tool("Cluster Detail")
    def cluster_detail_tool(cluster_id: int) -> str:
        """
        Return ALL skills in a specific CSPA ensemble cluster, sorted by
        market frequency (most in-demand first).

        Use after all_clusters_tool() to drill into clusters that appear
        underrepresented in the curriculum being analysed.

        Argument:
          cluster_id   integer 1–10. Use the cluster IDs from all_clusters_tool().

        Returns each skill with its frequency from the job-postings taxonomy,
        so you can prioritise which missing skills matter most.
        """
        detail = cluster_detail(cluster_id)
        if "error" in detail:
            return detail["error"]

        lines = [
            f"Cluster {detail['cluster_id']} — {detail['theme']}",
            f"Total skills: {detail['skill_count']}",
            "",
        ]
        for s in detail["skills"]:
            freq_str = f"freq={s['frequency']}" if s["frequency"] > 0 else "freq=n/a"
            lines.append(f"  - {s['skill']} ({freq_str})")
        return "\n".join(lines)

    CLUSTER_TOOLS = [all_clusters_tool, cluster_detail_tool]

except ImportError:
    CLUSTER_TOOLS = []


if __name__ == "__main__":
    print("=== Cluster overview ===")
    for c in all_clusters():
        flag = "⭐" if c["focused"] else "  "
        print(f"{flag} Cluster {c['cluster_id']:2d} | {c['theme']:45s} | {c['skill_count']:3d} skills | top: {c['top_skills_by_frequency'][:3]}")

    print("\n=== Cluster 4 detail (AI/ML Core) ===")
    d = cluster_detail(4)
    for s in d["skills"][:10]:
        print(f"  {s['skill']:40s} freq={s['frequency']}")

    print("\n=== Cluster 7 detail (Data Analytics, Science & Engineering) ===")
    d = cluster_detail(7)
    for s in d["skills"][:10]:
        print(f"  {s['skill']:40s} freq={s['frequency']}")
