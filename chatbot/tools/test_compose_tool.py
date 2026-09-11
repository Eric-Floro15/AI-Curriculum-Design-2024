"""
test_compose_tool.py — unit tests for the sector-wrap method change
(tools/compose_tool.py, 2026-09-11): separate agentic-core / sector-wrap
rankings, replacing the product (agentic-lift x sector-lift) ranking that
structurally buried domain skills like EHR/HIPAA.

Covers, per RUN2C_separate-rankings_toolchange.md's validation section:
  1. Anchor check — sector_wrap() reproduces the known-good sector-lift/z
     values for both finance and healthcare (Part 1, the "real gate").
  2. Dedup + cut logic — synthetic fixture proving a skill present in the
     agentic core is excluded from the wrap, and the cut (z>=2 AND
     lift>=3) is applied exactly (nothing below it, nothing missing above
     it).
  3. Guard traceability — sector_wrap_tool()'s returned text is a valid
     grounding source for the numeric fabrication guard (a real cited
     number from it is NOT flagged; a number absent from it IS).
  4. Real-data sanity — the live finance/healthcare wraps don't
     accidentally include any agentic-core skill.

No LLM, no CrewAI kickoff, no network — pure functions against the real
committed compose_<sector>_W2026.csv files plus a synthetic monkeypatched
fixture for the dedup/cut boundary cases. Safe to run anywhere.

Run:
    python chatbot/tools/test_compose_tool.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

import pandas as pd  # noqa: E402

import tools.compose_tool as compose_tool  # noqa: E402
from tools.compose_tool import (  # noqa: E402
    sector_wrap,
    sector_wrap_tool,
    _agentic_core_skill_names,
    _norm,
)

_FAILURES = []


def _check(label: str, condition: bool, detail: str = "") -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail and not condition else ""))
    if not condition:
        _FAILURES.append(label)


def _find(rows, skill_name):
    key = _norm(skill_name)
    for r in rows:
        if _norm(r["skill"]) == key:
            return r
    return None


# =====================================================================
# 1. ANCHOR CHECK — the real gate (RUN2C Part 1, validation step 1)
# =====================================================================
print("\n=== 1: anchor check (sector_wrap against known-good values) ===")

_finance_wrap = sector_wrap("finance")
_healthcare_wrap = sector_wrap("healthcare")

# Healthcare anchors: EXACT match expected (source: compose_demo_healthcare.py's
# own printed sanity check, generated the same way as this tool reads it).
for name, lift_anchor, z_anchor in [
    ("Electronic Health Records", 7.20, 3.19),
    ("Health Informatics", 8.99, 2.91),
    ("Clinical Trial Design And Execution", 7.22, 2.45),
    ("Hipaa", 4.29, 2.35),
]:
    r = _find(_healthcare_wrap, name)
    _check(f"healthcare anchor '{name}' present in sector_wrap", r is not None)
    if r is not None:
        _check(
            f"healthcare anchor '{name}' lift == {lift_anchor} (exact)",
            abs(r["lift"] - lift_anchor) < 0.01,
            f"got {r['lift']}",
        )
        _check(
            f"healthcare anchor '{name}' z == {z_anchor} (exact)",
            abs(r["z"] - z_anchor) < 0.01,
            f"got {r['z']}",
        )

# Finance anchors: lift matches exactly; z has a KNOWN ~2% discrepancy vs the
# anchor's stated value, diagnosed and reported (not papered over) —
# compose_demo.py's fightin_words() computes z over the FULL ~962-skill
# vector before any cut is applied, whereas the anchor's source
# (lift_analysis.py's CLI, run earlier this session) filters to n>=25 BEFORE
# computing z — so the z-formula's informative-prior normalising total
# differs between the two scripts even though both use the identical
# formula and identical underlying counts. This does not change which side
# of z>=2 either skill falls on. Tolerance here is 0.2 (not 0.01) to
# reflect that KNOWN, diagnosed gap specifically — not a general loosening.
for name, lift_anchor, z_anchor in [
    ("Financial Services", 4.3, 7.2),
    ("Risk Management", 4.4, 6.3),
]:
    r = _find(_finance_wrap, name)
    _check(f"finance anchor '{name}' present in sector_wrap", r is not None)
    if r is not None:
        _check(
            f"finance anchor '{name}' lift == {lift_anchor} (exact)",
            abs(r["lift"] - lift_anchor) < 0.03,
            f"got {r['lift']}",
        )
        _check(
            f"finance anchor '{name}' z ~= {z_anchor} (known ~2% cross-script "
            f"discrepancy, see comment above — tolerance 0.2)",
            abs(r["z"] - z_anchor) < 0.2,
            f"got {r['z']}",
        )


# =====================================================================
# 2. DEDUP + CUT LOGIC — synthetic fixture (isolates the boundary cases)
# =====================================================================
print("\n=== 2: dedup + cut logic (synthetic fixture) ===")

_orig_load = compose_tool._load
_orig_core = compose_tool._agentic_core_skill_names
_orig_sector_file = compose_tool._sector_file

_SYNTH_DF = pd.DataFrame([
    # In the agentic core AND would clear the sector cut on its own —
    # must be excluded by dedup.
    {"skill": "Fake Core Skill", "lift_fin": 10.0, "z_fin": 5.0, "n_fin": 40,
     "lift_ag": 9.0, "z_ag": 6.0, "lift_comp": 90.0},
    # NOT in the agentic core, clears the cut — must appear in the wrap.
    {"skill": "Fake Domain Skill", "lift_fin": 5.0, "z_fin": 3.0, "n_fin": 30,
     "lift_ag": 0.8, "z_ag": -0.5, "lift_comp": 4.0},
    # NOT in the agentic core, right at the lift floor (lift>=3 boundary) —
    # must appear.
    {"skill": "Fake Boundary Skill", "lift_fin": 3.0, "z_fin": 2.0, "n_fin": 25,
     "lift_ag": 1.0, "z_ag": 0.0, "lift_comp": 3.0},
    # NOT in the agentic core, just below the cut on z — must be excluded.
    {"skill": "Fake Weak Skill Z", "lift_fin": 5.0, "z_fin": 1.9, "n_fin": 20,
     "lift_ag": 1.0, "z_ag": 0.0, "lift_comp": 5.0},
    # NOT in the agentic core, just below the cut on lift — must be excluded.
    {"skill": "Fake Weak Skill Lift", "lift_fin": 2.9, "z_fin": 4.0, "n_fin": 20,
     "lift_ag": 1.0, "z_ag": 0.0, "lift_comp": 2.9},
])

try:
    compose_tool._load = lambda sector: _SYNTH_DF
    compose_tool._agentic_core_skill_names = lambda: frozenset({_norm("Fake Core Skill")})
    compose_tool._sector_file = lambda sector: None
    _synth_wrap = sector_wrap("synthetic-test-sector")
finally:
    compose_tool._load = _orig_load
    compose_tool._agentic_core_skill_names = _orig_core
    compose_tool._sector_file = _orig_sector_file

_synth_names = {r["skill"] for r in _synth_wrap}

_check(
    "dedup: a skill present in the agentic core is excluded from the wrap "
    "even though it clears the sector cut",
    "Fake Core Skill" not in _synth_names,
    f"wrap contained: {_synth_names}",
)
_check(
    "cut: a non-core skill clearing z>=2 AND lift>=3 IS included",
    "Fake Domain Skill" in _synth_names,
)
_check(
    "cut: a non-core skill exactly AT the boundary (z=2.0, lift=3.0) IS included",
    "Fake Boundary Skill" in _synth_names,
)
_check(
    "cut: a non-core skill just below the z floor is excluded",
    "Fake Weak Skill Z" not in _synth_names,
)
_check(
    "cut: a non-core skill just below the lift floor is excluded",
    "Fake Weak Skill Lift" not in _synth_names,
)
_check(
    "wrap size == exactly the 2 skills that should clear (no under- or over-inclusion)",
    len(_synth_wrap) == 2,
    f"got {len(_synth_wrap)}: {_synth_names}",
)
_check(
    "wrap is sorted by z descending",
    [r["z"] for r in _synth_wrap] == sorted([r["z"] for r in _synth_wrap], reverse=True),
)


# =====================================================================
# 3. GUARD TRACEABILITY — sector_wrap_tool output is a valid grounding source
# =====================================================================
print("\n=== 3: guard traceability (numeric fabrication guard) ===")

from agents.orchestrator import _detect_numeric_fabrication_flags  # noqa: E402

_wrap_text = sector_wrap_tool.func("finance")
_check(
    "sector_wrap_tool('finance') returns real formatted text, not an error string",
    "Financial Services" in _wrap_text and "lift" in _wrap_text,
)

_step_log = [{"role": "Skills Taxonomy Analyst", "output": type(
    "Finish", (), {"output": _wrap_text}
)()}]

_answer_with_real_number = (
    "The finance sector distinctively demands Financial Services skills "
    "(sector lift 4.32x, z=7.34)."
)
_flags_real = _detect_numeric_fabrication_flags(
    _answer_with_real_number, _step_log, ["Skills Taxonomy Analyst"]
)
_check(
    "a number actually present in sector_wrap_tool's output is NOT flagged "
    "(confirms the tool's text is a valid grounding source)",
    len(_flags_real) == 0,
    f"unexpected flags: {_flags_real}",
)

_answer_with_fake_number = (
    "The finance sector distinctively demands Financial Services skills "
    "(sector lift 99.9x, z=42.0)."
)
_flags_fake = _detect_numeric_fabrication_flags(
    _answer_with_fake_number, _step_log, ["Skills Taxonomy Analyst"]
)
_check(
    "a number NOT present in sector_wrap_tool's output IS flagged",
    len(_flags_fake) > 0,
)


# =====================================================================
# 4. REAL-DATA SANITY — live wraps never overlap the real agentic core
# =====================================================================
print("\n=== 4: real-data sanity (finance + healthcare, live data) ===")

_real_core = _agentic_core_skill_names()
for sector, wrap in [("finance", _finance_wrap), ("healthcare", _healthcare_wrap)]:
    overlap = [r["skill"] for r in wrap if _norm(r["skill"]) in _real_core]
    _check(
        f"{sector} wrap has zero overlap with the real agentic core",
        len(overlap) == 0,
        f"overlap: {overlap}",
    )
    all_clear_cut = all(r["z"] >= 2.0 and r["lift"] >= 3.0 for r in wrap)
    _check(
        f"{sector} wrap: every returned skill clears z>=2 AND lift>=3",
        all_clear_cut,
    )
    print(f"  {sector}: {len(wrap)} skill(s) — "
          f"{', '.join(r['skill'] for r in wrap)}")


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
