"""
csv_tool.py — Pandas-backed structured query tools over the skills taxonomy.

Complements rag_tool.py: where RAG is good at semantic similarity, this tool
handles deterministic filters and aggregations — "top N by frequency",
"all skills in Level 1 = soft", "everything in cluster 8", etc.

Reuses load_skills + build_cluster_map from build_index.py so cluster matching
stays identical between the FAISS index and the structured queries.

Exposes both a Python API (top_skills_by_frequency, ...) and CrewAI tool
wrappers (CSV_TOOLS). The CrewAI import is guarded so the module is testable
without crewai installed.
"""

import os
import sys
from functools import lru_cache

import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from build_index import (  # noqa: E402
    CLUSTER_FILE,
    CLUSTER_THEMES,
    SKILLS_FILE,
    build_cluster_map,
    load_skills,
)


@lru_cache(maxsize=1)
def _enriched_df() -> pd.DataFrame:
    """Load taxonomy + attach cluster_id once and cache."""
    df = load_skills(SKILLS_FILE)
    cluster_map = build_cluster_map(df, CLUSTER_FILE)
    df = df.copy()
    df["cluster_id"] = df["Alternate Spellings"].apply(
        lambda s: cluster_map.get(str(s).strip().lower(), -1)
    )
    return df


@lru_cache(maxsize=1)
def _canonical() -> pd.DataFrame:
    """One row per canonical skill group (the unit of analysis)."""
    df = _enriched_df()
    grouped = (
        df.groupby("Alternate Spellings")
        .agg(
            level1=("Level 1 Category", "first"),
            level2=("Level 2 Category", "first"),
            description=("Description", "first"),
            frequency=("Frequency", "sum"),
            cluster_id=("cluster_id", "first"),
        )
        .reset_index()
        .rename(columns={"Alternate Spellings": "skill"})
    )
    grouped["cluster_theme"] = grouped["cluster_id"].apply(
        lambda cid: CLUSTER_THEMES.get(cid, "Unknown") if cid != -1 else "Unlabelled"
    )
    return grouped


# ── Python API ────────────────────────────────────────────────────────────────

def top_skills_by_frequency(
    n: int = 10,
    level1: str | None = None,
    level2: str | None = None,
    cluster_id: int | None = None,
) -> list[dict]:
    """Top N canonical skills by total frequency, optional category/cluster filters."""
    df = _canonical()
    if level1:
        df = df[df["level1"].str.contains(level1, case=False, na=False)]
    if level2:
        df = df[df["level2"].str.contains(level2, case=False, na=False)]
    if cluster_id is not None:
        df = df[df["cluster_id"] == cluster_id]
    return df.sort_values("frequency", ascending=False).head(n).to_dict(orient="records")


def skills_in_category(level1: str, level2: str | None = None) -> list[dict]:
    """All canonical skills in a Level 1 (and optional Level 2) category."""
    df = _canonical()
    df = df[df["level1"].str.contains(level1, case=False, na=False)]
    if level2:
        df = df[df["level2"].str.contains(level2, case=False, na=False)]
    return df.sort_values("frequency", ascending=False).to_dict(orient="records")


def skills_in_cluster(cluster_id: int) -> list[dict]:
    """All canonical skills with the given ensemble cluster_id."""
    df = _canonical()
    return (
        df[df["cluster_id"] == cluster_id]
        .sort_values("frequency", ascending=False)
        .to_dict(orient="records")
    )


def category_summary() -> list[dict]:
    """Counts + total frequency per Level 1 > Level 2 category."""
    df = _canonical()
    grouped = (
        df.groupby(["level1", "level2"])
        .agg(n_skills=("skill", "count"), total_frequency=("frequency", "sum"))
        .reset_index()
        .sort_values("total_frequency", ascending=False)
    )
    return grouped.to_dict(orient="records")


# ── CrewAI tool wrappers ──────────────────────────────────────────────────────

try:
    from crewai.tools import tool

    def _fmt_skill_row(r: dict) -> str:
        return (
            f"- {r['skill']} (freq={r['frequency']}, "
            f"{r['level1']}>{r['level2']}, cluster={r['cluster_id']})"
        )

    @tool("Top Skills By Frequency")
    def top_skills_tool(
        n: int = 10,
        level1: str = "",
        level2: str = "",
        cluster_id: int = -1,
    ) -> str:
        """
        Return the top N most-frequent skills in the taxonomy. Filters are
        optional: level1 is typically "technical" or "soft"; level2 is a
        subcategory like "Cloud Computing" or "Leadership"; cluster_id is
        the ensemble cluster (1-10, or -1 to skip the filter).

        Best for: "what are the most in-demand skills?", "top soft skills",
        "top skills in cluster 8".
        """
        cid = cluster_id if cluster_id != -1 else None
        rows = top_skills_by_frequency(
            n=n, level1=level1 or None, level2=level2 or None, cluster_id=cid,
        )
        if not rows:
            return "No skills matched the filters."
        return "\n".join(_fmt_skill_row(r) for r in rows)

    @tool("Skills In Category")
    def skills_in_category_tool(level1: str, level2: str = "") -> str:
        """
        List all skills in a given category. level1 is required (typically
        "technical" or "soft"); level2 is an optional subcategory filter
        like "Machine Learning" or "Leadership". Returns up to 50 skills,
        sorted by frequency.

        Best for: "list all soft skills", "skills in the Cloud Computing
        subcategory".
        """
        rows = skills_in_category(level1, level2 or None)
        if not rows:
            return f"No skills found for level1={level1!r}, level2={level2!r}."
        return "\n".join(_fmt_skill_row(r) for r in rows[:50])

    @tool("Skills In Cluster")
    def skills_in_cluster_tool(cluster_id: int) -> str:
        """
        List all skills with a given ensemble cluster_id (1-10). Themes
        (per the CSPA ensemble): 4=Cloud/DB infra, 5=Soft skills/business,
        7=Core ML+stats+programming, 8=Data engineering (Spark/Kafka/Docker),
        9=Analytical/BI tools, 10=Large mixed group; others=General/Mixed.

        Note: only ~160 of 871 canonical skills carry a cluster label due to
        vocabulary drift between the cluster CSV and the indexed XLSX.
        """
        rows = skills_in_cluster(cluster_id)
        if not rows:
            return f"No skills found for cluster_id={cluster_id}."
        return "\n".join(_fmt_skill_row(r) for r in rows)

    @tool("Category Summary")
    def category_summary_tool() -> str:
        """
        High-level summary of the skills taxonomy: skill count and total
        frequency per Level 1 > Level 2 category. Useful for orienting on
        what categories of skills exist before drilling in.
        """
        rows = category_summary()
        return "\n".join(
            f"- {r['level1']} > {r['level2']}: {r['n_skills']} skills, "
            f"total frequency {r['total_frequency']}"
            for r in rows[:40]
        )

    CSV_TOOLS = [
        top_skills_tool,
        skills_in_category_tool,
        skills_in_cluster_tool,
        category_summary_tool,
    ]

except ImportError:
    CSV_TOOLS = []


if __name__ == "__main__":
    print("=== Top 10 skills overall ===")
    for r in top_skills_by_frequency(n=10):
        print(f"  {r['skill']:35s} freq={r['frequency']:5d} cluster={r['cluster_id']}")
    print("\n=== Top 10 soft skills ===")
    for r in top_skills_by_frequency(n=10, level1="soft"):
        print(f"  {r['skill']:35s} freq={r['frequency']:5d}")
    print("\n=== Skills in cluster 8 (data engineering) ===")
    rows = skills_in_cluster(8)
    if rows:
        for r in rows[:15]:
            print(f"  {r['skill']:35s} freq={r['frequency']:5d}")
    else:
        print("  (no skills with cluster_id=8)")
