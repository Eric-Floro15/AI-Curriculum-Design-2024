"""
cluster_tool.py — Tools for the Cluster Interpreter agent.

Reads chatbot/data/clust_ensembled_results.csv (766 skills, 10 CSPA
ensemble clusters) and chatbot/data/Grouped_Skills_Categorized_Updated.xlsx
(frequency data) to produce cluster-level gap analysis inputs.

The co-occurrence CSVs in final_implementation/ are not used here because
the row index was not preserved during export, making skill-to-skill lookup
unreliable. The cluster membership file is the clean source of truth.

Cluster themes (derived from inspection of skill contents):
  1  — Collaboration & leadership core (12 skills)
  2  — Cloud databases & storage (20 skills)
  3  — Large mixed: diverse soft + technical (263 skills)
  4  — Data infrastructure & streaming (17 skills)
  5  — Mixed: responsible AI, dev tools, analytics (60 skills)
  6  — Business & management core (4 skills)
  7  — ML algorithms & statistical modelling (50 skills)
  8  — Data engineering: pipelines, big data (22 skills)
  9  — Core analytical tools: Excel, BI, Data Analysis (23 skills)
 10  — Large mixed: ethics, soft skills, communication (295 skills)

Exposes:
  Python API   — all_clusters(), cluster_detail(id), skill_frequency(name)
  CrewAI tools — all_clusters_tool, cluster_detail_tool
"""

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
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

# ── File paths ────────────────────────────────────────────────────────────────

CLUSTER_RESULTS_FILE = os.path.join(_CHATBOT_DIR, "data", "clust_ensembled_results.csv")
SKILLS_FILE = os.path.join(_CHATBOT_DIR, "data", "Grouped_Skills_Categorized_Updated.xlsx")

CLUSTER_THEMES = {
    1:  "Collaboration & Leadership Core",
    2:  "Cloud Databases & Storage",
    3:  "Large Mixed — Diverse Soft + Technical",
    4:  "Data Infrastructure & Streaming",
    5:  "Mixed — Responsible AI, Dev Tools, Analytics",
    6:  "Business & Management Core",
    7:  "ML Algorithms & Statistical Modelling",
    8:  "Data Engineering — Pipelines & Big Data",
    9:  "Core Analytical Tools (Excel, BI, Data Analysis)",
    10: "Large Mixed — Ethics, Soft Skills, Communication",
}

# Clusters worth highlighting in gap analysis (focused, high-signal)
FOCUSED_CLUSTERS = {2, 4, 7, 8, 9}


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
    """Build skill-name → frequency lookup from the taxonomy XLSX."""
    try:
        df = pd.read_excel(SKILLS_FILE)
        # Column names from the XLSX
        skill_col = "Skills"
        freq_col = "Frequency"
        if skill_col not in df.columns or freq_col not in df.columns:
            return {}
        lookup = {}
        for _, row in df.iterrows():
            name = str(row[skill_col]).strip().lower()
            freq = int(row[freq_col]) if pd.notna(row[freq_col]) else 0
            if name not in lookup:
                lookup[name] = freq
            else:
                lookup[name] += freq
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

        Focused clusters (most discriminative for gap analysis): 2, 4, 7, 8, 9.
        Clusters 3 and 10 are large catch-all groups — less useful for targeted
        recommendations.
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

    print("\n=== Cluster 7 detail (ML Algorithms) ===")
    d = cluster_detail(7)
    for s in d["skills"][:10]:
        print(f"  {s['skill']:40s} freq={s['frequency']}")

    print("\n=== Cluster 8 detail (Data Engineering) ===")
    d = cluster_detail(8)
    for s in d["skills"][:10]:
        print(f"  {s['skill']:40s} freq={s['frequency']}")
