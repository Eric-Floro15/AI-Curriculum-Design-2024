"""
cluster_tool.py — Tools for the Cluster Interpreter agent.

Repointed 2026-09-03 from the pre-clean W2026 partition to the CLEAN W2026
CSPA ensemble (see chatbot_integration_prep/build_index_V4_repoint.md Step 2).
Reads chatbot/data/clust_ensembled_results_W2026_clean.csv and derives
frequency data from the V4 taxonomy xlsx (V2 JSONL is retired, see build_index.py).

The co-occurrence CSVs in final_implementation/ are not used here because
the row index was not preserved during export, making skill-to-skill lookup
unreliable. The cluster membership file is the clean source of truth.

2026-09-24 RELABEL (CLOSELOOP workstream a): CLUSTER_THEMES and
FOCUSED_CLUSTERS below were rewritten offline against the clean W2026
partition. Ground truth: clust_ensembled_results_W2026_clean.csv gives 10
clusters sized 174/282/159/71/54/2/69/2/12/137 (sum 962), which matches
the paper's canonical set exactly and confirms this is the clean V4
partition. Labels were derived from
FOR_CASSIE_AUGUST_2026_V4-TAXONOMY/01_APPENDIX_G_W2026_LABELS_CURRICULUM/
cluster_composition_W2026.md (top-15 skills by frequency + mean job
level/education level/salary premium per cluster) — that file, plus a
cross-check against Clustered_Skills_W2026.xlsx in the same folder (a
962-row per-skill file using a differently-aliased skill vocabulary but
identical cluster sizes/numbering), confirm the live cluster_id here maps
1:1 to that file's cluster number for all 10 clusters — sizes match
exactly and small clusters 6/8/9 match on exact skill content (cluster 9's
12 skills match verbatim; 6 and 8's 2-skill pairs match semantically under
each file's own vocabulary). No membership realignment was needed.

2026-09-24 CONFIRMED (post-review): CLUSTER_THEMES below was first
drafted by hand from cluster_composition_W2026.md's stats (no canonical
label-string source existed in the repo at that point) and reported to
Eric for review; Eric + Cowork then approved a final wording that now
matches Appendix G.1 verbatim — code == paper. Clusters 6, 8, and 9 are
deliberately NOT forced into a coherent theme (2/2/12 skills, 9 is
largely near-zero-frequency) — labeled "(heterogeneous)" rather than
themed, per this repo's own README guidance ("don't force a label on
incoherent clusters").

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
_W2026_CLUSTER_RESULTS_FILE = os.path.join(_CHATBOT_DIR, "data", "clust_ensembled_results_W2026_clean.csv")

# V4 taxonomy xlsx — source of truth for skill frequencies (V2 JSONL retired
# with the V4 repoint, see build_index.py module docstring).
_W2026_V4_TAXONOMY_XLSX = os.path.join(_CHATBOT_DIR, "data", "Grouped_Skills_Categorized_V4.xlsx")

# 2026-09-25 (§5.1 F2022 curriculum, PROMPT_for_ClaudeCode_S51_F2022_curriculum.md
# STEP 1): REVERSIBLE env-var override — points the cluster tool at a different
# wave's data for one run only, without touching .env or any destructive edit to
# the W2026 files above. Unset (the default) -> byte-for-byte identical W2026
# production behaviour. Set (process-local only, same pattern this project uses
# for STRICT_DELEGATION) -> reads the override paths instead. When an override
# is active, CLUSTER_THEMES falls back to numeric-only labels (see _theme_for()
# below) rather than reusing W2026's theme text on a different wave's cluster
# contents — an alternate wave's clusters hold different skills at the same
# numeric id, so a W2026 label would misdescribe them (exactly the mistake the
# 2026-09-24 relabel fixed for the old pre-clean partition).
CLUSTER_RESULTS_FILE = os.environ.get("CLUSTER_RESULTS_FILE_OVERRIDE") or _W2026_CLUSTER_RESULTS_FILE
V4_TAXONOMY_XLSX = os.environ.get("FREQ_XLSX_OVERRIDE") or _W2026_V4_TAXONOMY_XLSX
_ALT_WAVE_MODE = bool(os.environ.get("CLUSTER_RESULTS_FILE_OVERRIDE"))

# Cluster themes for the clean Winter 2026 CSPA ensemble partition.
# FINAL labels (2026-09-24) — Eric + Cowork approved; these match the
# paper's Appendix G.1 verbatim, so code == paper. Do not edit without a
# corresponding Appendix G.1 change (and vice versa). Only used when
# _ALT_WAVE_MODE is False (see _theme_for() below) — an override run never
# reads this dict.
CLUSTER_THEMES = {
    1:  "Machine Learning & Generative AI",
    2:  "Cloud, DevOps & AI Systems Deployment",
    3:  "Data Engineering & Data Platforms",
    4:  "Business Intelligence & Data Communication",
    5:  "Office Productivity, Business Analysis & Admin Tools",
    6:  "Cross-cutting analytical & collaboration terms (heterogeneous)",
    7:  "Data Science & Statistical Foundations",
    8:  "Training & community terms (heterogeneous)",
    9:  "Niche & Emerging ML/AI Tooling (heterogeneous)",
    10: "Strategic Planning, Program Management & Business Development",
}


# 2026-09-25 (§5.1 F2022 PUSHTHROUGH, Part B): optional VETTED label
# override for an alt-wave run — a JSON object {"1": "label", ...} of
# reviewed theme labels for the active override's cluster ids, e.g. the
# Cowork-reviewed F2022 labels. Takes priority over the numeric-only
# fallback below when present, so a reviewed alt-wave run gets real
# labels instead of "Cluster N (numeric only...)". Still falls back to
# numeric-only for any cluster id NOT covered by the override JSON, so a
# partial/malformed override degrades safely rather than crashing.
_cluster_themes_override_raw = os.environ.get("CLUSTER_THEMES_OVERRIDE_JSON")
_CLUSTER_THEMES_OVERRIDE: dict[int, str] = {}
if _cluster_themes_override_raw:
    import json as _json
    try:
        _CLUSTER_THEMES_OVERRIDE = {
            int(k): v for k, v in _json.loads(_cluster_themes_override_raw).items()
        }
    except (ValueError, TypeError):
        _CLUSTER_THEMES_OVERRIDE = {}

# 2026-09-25 (§5.1 F2022 PUSHTHROUGH, Part A1): human-readable label for the
# active override's data wave, e.g. "Fall 2022 (F2022)" — used only to build
# data_wave_override_notice() below, and only when _ALT_WAVE_MODE is active.
# Generic/wave-parameterized by design (not F2022-hardcoded), so the same
# mechanism serves any future off-wave run (F2023, W2024, ...).
DATA_WAVE_LABEL = os.environ.get("DATA_WAVE_LABEL", "a non-default data wave")


def _theme_for(cluster_id: int) -> str:
    """Theme label for a cluster id — the W2026 CLUSTER_THEMES dict when
    running on the default W2026 data; the vetted CLUSTER_THEMES_OVERRIDE_JSON
    label when an alt-wave override is active AND that cluster id is covered
    by it; otherwise a numeric-only placeholder (an alt-wave run with no
    reviewed labels yet, or a cluster id the override JSON doesn't cover) —
    reusing the W2026 label on a different wave's cluster N would misdescribe
    it, since a different wave's cluster N holds different skills. See the
    2026-09-25 override comments above."""
    if _ALT_WAVE_MODE:
        if cluster_id in _CLUSTER_THEMES_OVERRIDE:
            return _CLUSTER_THEMES_OVERRIDE[cluster_id]
        return f"Cluster {cluster_id} (numeric only — no theme assigned for this data wave)"
    return CLUSTER_THEMES.get(cluster_id, "Unknown")


def data_wave_override_notice() -> str | None:
    """A per-run notice block for injection into the Orchestrator's task
    text (2026-09-25, §5.1 F2022 PUSHTHROUGH Part A1) — None when no
    override is active (the default; callers must not inject anything in
    that case), or a marker-delimited block when CLUSTER_RESULTS_FILE_OVERRIDE
    is set, instructing every agent that reads it to trust the LIVE tool
    output over their own static backstory text for this run.

    Fixes the real failure found on a live F2022 dev-lane run
    (run_20260925T164511Z): the Cluster Interpreter followed its backstory's
    static W2026 CLUSTER REFERENCE table (hardcoded cluster-number -> label/
    focused-star text) instead of this run's actual tool output, and its own
    narration mislabelled F2022 data as "Winter 2026" throughout — both
    because nothing told it its backstory's default-wave assumptions no
    longer held for this run. This block closes that gap the same way the
    "ATTACHED UPLOADED CURRICULUM DOCUMENT" marker block already does for a
    different purpose (see agents/orchestrator.py's HANDLING AN ATTACHED
    UPLOADED CURRICULUM DOCUMENT rule) — plain-text instructions injected
    into the task description, not a permanent, run-independent backstory
    edit, and generic/wave-parameterized so it serves any future off-wave
    validation run without further code changes.
    """
    if not _ALT_WAVE_MODE:
        return None
    return (
        "===== DATA WAVE OVERRIDE NOTICE =====\n"
        "For THIS run, the live cluster_tool output (from All Clusters "
        "Overview / Cluster Detail) is the SOLE source of truth for cluster "
        "sizes, membership, labels, the focused set, and the labour-market "
        "wave/time period this data was collected in. Disregard any cluster "
        "reference table, theme label, focused-set marker, or wave/date "
        "framing (e.g. a specific year) written in your own static "
        "backstory wherever it disagrees with what the tool actually "
        f"returns this run. The data grounding this run is the "
        f"{DATA_WAVE_LABEL} wave — describe it as such in your own "
        "reasoning and final synthesis; do not assume or state your "
        "backstory's default wave/time period instead.\n"
        "===== END DATA WAVE OVERRIDE NOTICE ====="
    )


# Clusters worth highlighting in gap analysis (focused, high-signal technical
# areas). Selection criterion (2026-09-24 relabel, Eric + Cowork approved):
# coherent, discriminative, TECHNICAL clusters only — 1 (Machine Learning &
# Generative AI), 2 (Cloud, DevOps & AI Systems Deployment), 3 (Data
# Engineering & Data Platforms), 7 (Data Science & Statistical Foundations).
# Excludes the tiny/heterogeneous catch-alls (6, 8, 9) and the broad
# soft-skill / general-business clusters (4, 5, 10 — BI/communication,
# office/admin, strategy/sales/PM) which are less discriminative for
# targeted curriculum-gap recommendations, mirroring the same
# broad-cluster-exclusion logic the old (stale) partition used.
#
# 2026-09-25: overridable via FOCUSED_CLUSTERS_OVERRIDE (comma-separated
# cluster ids), for the same alternate-wave-run reason as CLUSTER_RESULTS_FILE
# above — a different wave's cluster N is not the same skills as W2026's
# cluster N, so which numbers are "coherent/technical" can differ by wave.
_focused_override = os.environ.get("FOCUSED_CLUSTERS_OVERRIDE")
if _focused_override:
    FOCUSED_CLUSTERS = {int(x) for x in _focused_override.split(",") if x.strip()}
else:
    FOCUSED_CLUSTERS = {1, 2, 3, 7}


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
            "theme": _theme_for(int(cid)),
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
        "theme": _theme_for(cluster_id),
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

        On the default W2026 data: focused clusters (most discriminative for
        gap analysis) are 1, 2, 3, 7. Clusters 4, 5, and 10 are large,
        broad-spectrum soft-skill/business groups — less useful for targeted
        gap-analysis recommendations. Clusters 6, 8, and 9 are small/
        incoherent catch-alls — disclose, don't theme. TRUST THE ⭐ MARKERS
        AND THEMES IN THIS TOOL'S ACTUAL RETURNED TEXT over this note — on a
        different data wave the same cluster NUMBER can hold different
        skills, so the returned data (not this static description) is
        authoritative for which clusters are focused and what they mean.
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

    print("\n=== Cluster 1 detail (Machine Learning & Generative AI) ===")
    d = cluster_detail(1)
    for s in d["skills"][:10]:
        print(f"  {s['skill']:40s} freq={s['frequency']}")

    print("\n=== Cluster 3 detail (Data Engineering & Data Platforms) ===")
    d = cluster_detail(3)
    for s in d["skills"][:10]:
        print(f"  {s['skill']:40s} freq={s['frequency']}")
