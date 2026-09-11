"""
compose_tool.py — Composed sector×skill ("agentic-in-<sector>") tool, plus
the separate agentic-core / sector-wrap rankings (2026-09-11 method change).

Serves the compose-don't-intersect method (paper §4.6 sector case studies). The
direct sector∩agentic slice (e.g. finance∩agentic ≈ 256 pooled postings) is too
small to certify, so the sector-specific agentic curriculum was originally
estimated as the PRODUCT of two marginal lifts:  lift_composed = lift_agentic
× lift_sector. See compose_demo.py, which computes the per-sector tables this
tool reads.

WHY THE PRODUCT RANKING WAS REPLACED (2026-09-11): the product structurally
buries a sector's DOMAIN skills. A domain skill like EHR has a strong
sector-lift (7.2x) but an agentic-lift at or below 1 (agentic postings repel
non-agentic domain skills — same pattern as Excel 0.41x/PowerBI 0.32x in the
agentic segment), so the product multiplies it DOWN and it never surfaces in
a top-K-by-product ranking. This is not a sample-size effect (lift is a
normalised rate-ratio; n only affects z, which the product doesn't use) — it
is structural. The healthcare Sonnet run (fab7a60) never surfaced EHR / HIPAA
/ Health Informatics for exactly this reason.

THE FIX: two separate rankings instead of one combined score.
  1. AGENTIC CORE — the horizontal, sector-invariant skills, ranked by
     agentic-lift. This already existed via skill_lift_tool
     (tools/lift_tool.py, focal_skill="Agentic Ai") and is unchanged.
  2. SECTOR WRAP — the sector-distinctive skills, ranked by SECTOR-LIFT ALONE
     (lift_fin / z_fin — NOT the product), subject to: (a) the existing
     reporting cut z>=2 AND lift>=3 (not a fixed top-N — the length of the
     list is itself signal: finance's wrap is thin, healthcare's is rich);
     (b) dedup — exclude any skill already in the agentic core, so the wrap
     is purely the incremental domain layer. See sector_wrap() /
     sector_wrap_tool below.

A sector curriculum = "shared agentic core (skill_lift_tool) + this sector's
domain wrap (sector_wrap_tool)". The old composed_curriculum()/
composed_sector_tool (product ranking) is left in place as a secondary lens
— cheap to keep, and some callers/tests may still reference it — but it is
NOT used by sector_wrap() and should not be treated as the sector-distinctive
ranking going forward.

DATA STEP (one-time per sector, needs the presence matrix — do this before using
this tool). compose_demo.py currently hardcodes the sector 'Finance & Insurance':
    python FOR_CASSIE_AUGUST_2026_V4-TAXONOMY/05_COMPOSE_METHOD/compose_demo.py
    cp compose_finance_W2026.csv chatbot/data/compose_finance_W2026.csv
For another sector, copy compose_demo.py (or compose_demo_healthcare.py, its
already-generalised sibling), change the sector filter, rerun, and save as
chatbot/data/compose_<sector>_W2026.csv.

compose_<sector>_W2026.csv columns (from compose_demo.py) — THIS is where the
per-skill sector-lift and its z live; it is a COMPLETE table (every skill in
the taxonomy, not just a top-K subset) despite the "_fin" naming being a
finance-first leftover (it is sector-agnostic in practice — same columns for
compose_healthcare_W2026.csv):
  skill, n_ag, lift_ag, z_ag, n_fin, lift_fin, z_fin, n_joint, lift_jo, z_jo,
  lift_delta, z_delta, lift_comp

Exposes:
  Python API  — composed_curriculum(sector, top_k, min_lift), available_sectors(),
                sector_wrap(sector, z_min, lift_min)
  CrewAI tool — composed_sector_tool (legacy product ranking, kept as a
                secondary lens), sector_wrap_tool (the sector-distinctive
                domain-skill ranking — use this for "what should a
                <sector>-focused program teach" questions)

Pattern mirrors cluster_tool.py / lift_tool.py.
"""

import os
import sys
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
# Needed so `from tools.lift_tool import ...` resolves both when this module
# is imported normally (chatbot dir already on sys.path via the importing
# agent module) and when run standalone (`python tools/compose_tool.py`).
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

_AGENTIC_FOCAL_SKILL = "Agentic Ai"
_AGENTIC_CORE_SOURCE_FILE = "skill_lift_table.csv"


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


@lru_cache(maxsize=1)
def _agentic_core_skill_names() -> frozenset:
    """Normalised names of the agentic core (skill_lift_table.csv, focal =
    'Agentic Ai'). That table is generated by the deterministic pipeline
    with the z>=2 & lift>=3 cut already applied at persist time (verified:
    all 73 rows for this focal skill satisfy both), so no extra filtering
    is needed here — this is the dedup key for sector_wrap().
    """
    from tools.lift_tool import focal_associations
    rows = focal_associations(_AGENTIC_FOCAL_SKILL, z_min=0.0)
    return frozenset(_norm(r["skill"]) for r in rows)


@_traceable(name="sector_wrap", run_type="tool")
def sector_wrap(sector: str, z_min: float = 2.0, lift_min: float = 3.0) -> list[dict]:
    """Sector-distinctive skills, ranked by SECTOR-LIFT ALONE (lift_fin/z_fin
    from compose_<sector>_W2026.csv) — not the agentic x sector product.

    Cut: every skill with z_fin >= z_min AND lift_fin >= lift_min (the
    existing reporting cut; not a fixed top-N, so the list's length is
    itself signal). Dedup: excludes any skill already in the agentic core
    (skill_lift_table.csv, focal='Agentic Ai') so this is purely the
    incremental domain layer, never double-counting a skill strong on both
    axes.
    """
    df = _load(sector)
    if df is None:
        return []
    core = _agentic_core_skill_names()
    d = df[(df["z_fin"] >= z_min) & (df["lift_fin"] >= lift_min)].copy()
    d = d[~d["skill"].map(_norm).isin(core)]
    d = d.sort_values("z_fin", ascending=False)
    src = _sector_file(sector)
    src_name = os.path.basename(src) if src else f"compose_{_norm(sector)}_W2026.csv"
    return [
        {"skill": r.skill, "lift": round(float(r.lift_fin), 2),
         "z": round(float(r.z_fin), 2), "n": int(r.n_fin),
         "source_file": src_name}
        for r in d.itertuples()
    ]


# ── CrewAI tool wrapper ───────────────────────────────────────────────────────
try:
    from crewai.tools import tool

    @tool("Sector Skill Wrap (domain-distinctive, sector-lift ranked)")
    def sector_wrap_tool(sector: str) -> str:
        """
        Return the skills a SECTOR distinctively demands on their own merits
        — ranked by SECTOR-LIFT ALONE, not combined with agentic-lift. Use
        this alongside Skill Lift (focal_skill="Agentic Ai") for any
        sector-focused curriculum question: Skill Lift gives the shared
        agentic CORE every such program needs; this tool gives the sector's
        domain WRAP on top of that core. Do not use the composed/product
        tool for this — the product buries domain skills whose agentic-lift
        is low (e.g. EHR, HIPAA) even when their sector-lift is strong.

        Argument:
          sector   e.g. "finance", "healthcare" — matches a precomputed
                   compose_<sector>_W2026.csv in chatbot/data/.

        Returns every skill clearing z>=2 AND lift>=3 on the sector axis,
        excluding anything already in the agentic core (so nothing is
        double-counted). The list may be short (a "thin" wrap) or long (a
        "rich" wrap) — that length is itself a finding, not truncated to a
        round number.
        """
        rows = sector_wrap(sector)
        if not rows:
            av = ", ".join(available_sectors()) or "(none generated yet)"
            return (
                f"No sector-wrap data for sector '{sector}' (either no "
                f"compose_{{sector}}_W2026.csv exists, or no skill cleared "
                f"z>=2 AND lift>=3 on the sector axis after excluding the "
                f"agentic core). Available sectors: {av}."
            )
        lines = [
            f"Sector wrap for '{sector}' — {len(rows)} domain-distinctive "
            f"skill(s) clearing z>=2 AND lift>=3 on the sector axis alone "
            f"(agentic-core skills excluded; source: {rows[0]['source_file']}):",
            "",
        ]
        for r in rows:
            lines.append(
                f"  - {r['skill']}  (sector lift {r['lift']}x, z={r['z']}, "
                f"n={r['n']})"
            )
        return "\n".join(lines)

    SECTOR_WRAP_TOOLS = [sector_wrap_tool]

except ImportError:
    SECTOR_WRAP_TOOLS = []


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
        print(f"\n=== agentic-in-{s} (top 12, legacy product ranking) ===")
        for r in composed_curriculum(s, top_k=12):
            print(f"  {r['skill']:34s} comp={r['lift_composed']:<7} "
                  f"(ag {r['lift_ag']}×/z{r['z_ag']}, sec {r['lift_sector']}×/z{r['z_sector']})")
        wrap = sector_wrap(s)
        print(f"\n=== sector wrap for {s} ({len(wrap)} skill(s), z>=2 & lift>=3, "
              f"agentic-core excluded) ===")
        for r in wrap:
            print(f"  {r['skill']:34s} lift={r['lift']:<7} z={r['z']}")
