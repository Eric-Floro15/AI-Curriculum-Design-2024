"""
lift_tool.py — Differential (lift) analysis tool for the Skills Taxonomy Analyst.

Reads chatbot/data/skill_lift_table.csv — the FROZEN lift table (7,054
skill→associated-skill edges over 492 focal skills) produced by the deterministic
pipeline (lift_analysis.py). For a focal skill it returns the skills significantly
co-demanded with it in the labour market, ranked by the Fightin'-Words log-odds z
(Monroe et al. 2008). This is the evidence the chatbot grounds an agentic (or any
focal-skill) curriculum in: recommend what the data attests, not what a base model
guesses.

Setup (one-time): copy the frozen table into the chatbot's data dir —
    cp FOR_CASSIE_AUGUST_2026_V4-TAXONOMY/06_LIFT_TABLE_TOOL/skill_lift_table.csv chatbot/data/

skill_lift_table.csv columns:
  skill, associated_skill, n_together, pct_of_skill_postings,
  pct_of_all_postings, lift, z

Exposes:
  Python API  — focal_associations(focal_skill, z_min), list_focal_skills()
  CrewAI tool — skill_lift_tool

Pattern intentionally mirrors cluster_tool.py (traceable + lru_cache loaders +
@tool wrapper returning a formatted string + graceful ImportError fallback).
"""

import os
from functools import lru_cache

import pandas as pd

# @traceable records each call as a named LangSmith span (mirrors cluster_tool.py).
try:
    from langsmith import traceable as _traceable
except ImportError:
    def _traceable(**_kw):
        def _decorator(fn):
            return fn
        return _decorator

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
LIFT_TABLE_FILE = os.path.join(_CHATBOT_DIR, "data", "skill_lift_table.csv")

# |z| >= 2 ≈ significant — the same attestation threshold the paper's extrinsic
# evaluation uses. Kept as a module constant so evals can record what was used.
DEFAULT_Z_MIN = 2.0


@lru_cache(maxsize=1)
def _load() -> pd.DataFrame:
    if not os.path.exists(LIFT_TABLE_FILE):
        raise FileNotFoundError(
            f"Lift table not found at {LIFT_TABLE_FILE}\n"
            "Copy skill_lift_table.csv from "
            "FOR_CASSIE_AUGUST_2026_V4-TAXONOMY/06_LIFT_TABLE_TOOL/ into chatbot/data/."
        )
    df = pd.read_csv(LIFT_TABLE_FILE)
    df["skill"] = df["skill"].astype(str).str.strip()
    df["associated_skill"] = df["associated_skill"].astype(str).str.strip()
    return df


def _norm(s: str) -> str:
    """Collapse a skill name to lowercase alphanumerics for matching."""
    return "".join(ch for ch in str(s).lower() if ch.isalnum())


@_traceable(name="focal_associations", run_type="tool")
def focal_associations(focal_skill: str, z_min: float = DEFAULT_Z_MIN) -> list[dict]:
    """Skills significantly associated with focal_skill (z >= z_min), ranked by z desc."""
    df = _load()
    key = _norm(focal_skill)
    sub = df[df["skill"].map(_norm) == key]
    if sub.empty:
        return []
    sub = sub[sub["z"] >= z_min].sort_values("z", ascending=False)
    return [
        {"skill": r.associated_skill, "lift": round(float(r.lift), 2),
         "z": round(float(r.z), 2), "n_together": int(r.n_together)}
        for r in sub.itertuples()
    ]


@lru_cache(maxsize=1)
def list_focal_skills() -> tuple:
    return tuple(sorted(_load()["skill"].unique().tolist()))


# ── CrewAI tool wrapper ───────────────────────────────────────────────────────
try:
    from crewai.tools import tool

    @tool("Skill Lift / Differential Analysis")
    def skill_lift_tool(focal_skill: str) -> str:
        """
        Return the skills the labour market significantly co-demands with a given
        focal skill, from the frozen differential-analysis (lift) table.

        Use this to GROUND a curriculum in evidence: given a target like
        "Agentic AI", it returns the specific skills that distinctively co-occur
        with it in job postings, each with its lift (how many times more likely
        than the baseline rate) and z (significance; |z|>=2 is significant).
        Recommend from these attested skills rather than from general knowledge.

        Argument:
          focal_skill   the skill to analyse, e.g. "Agentic Ai".
                        Case- and spacing-insensitive.

        Returns the associated skills ranked by z (most distinctive first).
        """
        rows = focal_associations(focal_skill)
        if not rows:
            near = ", ".join(
                s for s in list_focal_skills() if _norm(focal_skill) in _norm(s)
            )[:400]
            return (
                f"No lift rows for focal skill '{focal_skill}' at z>=2. "
                + (f"Did you mean: {near}?" if near
                   else "Check the spelling against the taxonomy's canonical skill names.")
            )
        lines = [
            f"Skills significantly co-demanded with '{focal_skill}' "
            f"(lift table, z>=2 — {len(rows)} skills, ranked by significance):",
            "",
        ]
        for r in rows:
            lines.append(
                f"  - {r['skill']}  (lift {r['lift']}×, z={r['z']}, "
                f"co-occurs in {r['n_together']} postings)"
            )
        return "\n".join(lines)

    LIFT_TOOLS = [skill_lift_tool]

except ImportError:
    LIFT_TOOLS = []


if __name__ == "__main__":
    print("=== Skills significantly associated with 'Agentic Ai' (z>=2) ===")
    rows = focal_associations("Agentic Ai")
    print(f"({len(rows)} skills)\n")
    for r in rows[:20]:
        print(f"  {r['skill']:38s} lift={r['lift']:<7} z={r['z']}")
