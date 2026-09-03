"""
compose_tool.py — Composed sector×skill ("agentic-in-<sector>") tool.

Serves the compose-don't-intersect method (paper §4.6 sector case studies). The
direct sector∩agentic slice (e.g. finance∩agentic ≈ 256 pooled postings) is too
small to certify, so the sector-specific agentic curriculum is estimated as the
PRODUCT of two marginal lifts:  lift_composed = lift_agentic × lift_sector.
See compose_demo.py, which computes the per-sector tables this tool reads.

DATA STEP (one-time per sector, needs the presence matrix — do this before using
this tool). compose_demo.py currently hardcodes the sector 'Finance & Insurance':
    python FOR_CASSIE_AUGUST_2026_V4-TAXONOMY/05_COMPOSE_METHOD/compose_demo.py
    cp compose_finance_W2026.csv chatbot/data/compose_finance_W2026.csv
For life sciences, copy compose_demo.py, change the sector filter
('Finance & Insurance' -> the life-sciences sector label in company_sectors_final.csv),
rerun, and save as chatbot/data/compose_lifesciences_W2026.csv.

compose_<sector>_W2026.csv columns (from compose_demo.py):
  skill, n_ag, lift_ag, z_ag, n_fin, lift_fin, z_fin, n_joint, lift_jo, z_jo,
  lift_delta, z_delta, lift_comp

Exposes:
  Python API  — composed_curriculum(sector, top_k, min_lift), available_sectors()
  CrewAI tool — composed_sector_tool

Pattern mirrors cluster_tool.py / lift_tool.py.
"""

import os
import glob
from functools import lru_cache

import pandas as pd

try:
    from langsmith import traceable as _traceable
except ImportError:
    def _traceable(**_kw):
        def _decorator(fn):
            return fn
        return _decorator

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
_DATA_DIR = os.path.join(_CHATBOT_DIR, "data")


def _norm(s: str) -> str:
    return "".join(ch for ch in str(s).lower() if ch.isalnum())


def _sector_file(sector: str) -> str | None:
    """Find chatbot/data/compose_<sector>_W2026.csv by fuzzy tag match."""
    key = _norm(sector)
    for p in glob.glob(os.path.join(_DATA_DIR, "compose_*_W2026.csv")):
        tag = _norm(os.path.basename(p).replace("compose_", "").replace("_W2026.csv", ""))
        if tag == key or key in tag or tag in key:
            return p
    return None


@lru_cache(maxsize=8)
def _load(sector: str):
    p = _sector_file(sector)
    if not p or not os.path.exists(p):
        return None
    return pd.read_csv(p)


def available_sectors() -> list[str]:
    out = []
    for p in glob.glob(os.path.join(_DATA_DIR, "compose_*_W2026.csv")):
        out.append(os.path.basename(p).replace("compose_", "").replace("_W2026.csv", ""))
    return sorted(out)


@_traceable(name="composed_curriculum", run_type="tool")
def composed_curriculum(sector: str, top_k: int = 15, min_lift: float = 1.0) -> list[dict]:
    """Composed agentic-in-<sector> skills, ranked by lift_comp = lift_ag × lift_sector.

    Keeps skills that are significant on either marginal (z_ag>=2 or z_fin>=2) and
    positively associated on both (lift>=min_lift), matching compose_demo.py's
    'COMPOSED curriculum' panel.
    """
    df = _load(sector)
    if df is None:
        return []
    d = df[((df["z_ag"] >= 2) | (df["z_fin"] >= 2))
           & (df["lift_ag"] >= min_lift) & (df["lift_fin"] >= min_lift)].copy()
    d = d.sort_values("lift_comp", ascending=False).head(top_k)
    return [
        {"skill": r.skill,
         "lift_ag": round(float(r.lift_ag), 2), "z_ag": round(float(r.z_ag), 2),
         "lift_sector": round(float(r.lift_fin), 2), "z_sector": round(float(r.z_fin), 2),
         "lift_composed": round(float(r.lift_comp), 2)}
        for r in d.itertuples()
    ]


# ── CrewAI tool wrapper ───────────────────────────────────────────────────────
try:
    from crewai.tools import tool

    @tool("Composed Sector Curriculum (agentic × sector)")
    def composed_sector_tool(sector: str) -> str:
        """
        Return the agentic-AI skills a given SECTOR distinctively emphasises, via
        the compose method (product of the agentic marginal lift and the sector
        marginal lift). Use this for a sector-specific agentic curriculum
        (e.g. "agentic AI for finance") — it is more reliable than a direct
        sector∩agentic slice, which is usually too small to trust.

        Argument:
          sector   e.g. "finance", "life sciences" — matches a precomputed
                   compose_<sector>_W2026.csv in chatbot/data/.

        Returns skills ranked by composed lift (lift_agentic × lift_sector).
        """
        rows = composed_curriculum(sector)
        if not rows:
            av = ", ".join(available_sectors()) or "(none generated yet)"
            return (
                f"No composed table for sector '{sector}'. Available: {av}. "
                "Generate one by running compose_demo.py for that sector and copying "
                "compose_<sector>_W2026.csv into chatbot/data/ (see the file header)."
            )
        lines = [
            f"Composed agentic-in-{sector} curriculum "
            f"(top {len(rows)} by lift_agentic × lift_sector):",
            "",
        ]
        for r in rows:
            lines.append(
                f"  - {r['skill']}  (agentic lift {r['lift_ag']}× z={r['z_ag']}; "
                f"{sector} lift {r['lift_sector']}× z={r['z_sector']}; "
                f"composed {r['lift_composed']})"
            )
        return "\n".join(lines)

    COMPOSE_TOOLS = [composed_sector_tool]

except ImportError:
    COMPOSE_TOOLS = []


if __name__ == "__main__":
    secs = available_sectors()
    print(f"Available composed sectors: {secs or '(none — run compose_demo.py first)'}")
    for s in secs:
        print(f"\n=== agentic-in-{s} (top 12) ===")
        for r in composed_curriculum(s, top_k=12):
            print(f"  {r['skill']:34s} comp={r['lift_composed']:<7} "
                  f"(ag {r['lift_ag']}×/z{r['z_ag']}, sec {r['lift_sector']}×/z{r['z_sector']})")
