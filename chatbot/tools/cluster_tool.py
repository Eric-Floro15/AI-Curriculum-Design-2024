"""
cluster_tool.py — Tools for the Cluster Interpreter agent.

Repointed 2026-09-03 from the pre-clean W2026 partition to the CLEAN W2026
CSPA ensemble (see chatbot_integration_prep/build_index_V4_repoint.md Step 2).
Reads chatbot/data/clust_ensembled_results_W2026_clean.csv and derives
frequency data from the V4 taxonomy xlsx (V2 JSONL is retired, see build_index.py).

The co-occurrence CSVs in final_implementation/ are not used here because
the row index was not preserved during export, making skill-to-skill lookup
unreliable. The cluster membership file is the clean source of truth.

⚠️ CLUSTER_THEMES and FOCUSED_CLUSTERS below are STALE — they're the old
labels for the pre-clean partition (kept verbatim from before this repoint,
per build_index_V4_repoint.md's guidance that this step is deferred to a
paid Cluster Interpreter relabel run, not blocking). The clean partition's
cluster IDs hold DIFFERENT skills — per CLAUDE.md, clean-W2026 cluster 2 is
now the 282-skill agentic core, which does not correspond to old cluster 2's
"Software Architecture & Human-Centered Design" label below. Do not trust
these theme names or the focused-cluster set until relabeled; skill_count
per cluster_id will also differ from what's written here since it was
computed on the old file. Run the eyeball snippet in the repoint doc (Step
1e/2c) for provisional labels, or wait for the production relabel run.

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
_PROJECT_ROOT = os.path.dirname(_CHATBOT_DIR)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

# ── File paths ────────────────────────────────────────────────────────────────

# Clean Winter 2026 CSPA ensemble clustering (post description-cleaning
# re-cluster, see CLAUDE.md decisions #46). Supersedes both the old
# clust_ensembled_results.csv (766 skills, V1 clustering) and the pre-clean
# cluster_assignments_w2026.csv this file used before the V4 repoint.
CLUSTER_RESULTS_FILE = os.path.join(_CHATBOT_DIR, "data", "clust_ensembled_results_W2026_clean.csv")

# V4 taxonomy xlsx — source of truth for skill frequencies (V2 JSONL retired
# with the V4 repoint, see build_index.py module docstring).
V4_TAXONOMY_XLSX = os.path.join(_CHATBOT_DIR, "data", "Grouped_Skills_Categorized_V4.xlsx")

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
    """Build skill-name → frequency lookup from the V4 taxonomy xlsx.

    Keyed by raw Skills.lower() (not canonical_key) to match the cluster
    CSV's raw skill names, same lookup convention _enrich_with_freq() already
    uses. Per build_index_V4_repoint.md Step 2b.
    """
    try:
        lookup: dict[str, int] = {}
        df = pd.read_excel(V4_TAXONOMY_XLSX)
        for _, r in df.iterrows():
            name = str(r.get("Skills", "")).strip().lower()
            if name and name not in lookup:
                lookup[name] = int(r.get("Frequency", 0) or 0)
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
