#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""score_curricula.py — score any curriculum .txt file for §4.7 Table 6 metrics.

Usage:
    python _SUBMISSION_DSS/repeated_generations/score_curricula.py <file1.txt> [<file2.txt> ...]

Prints per file:
  - extracted-skill count
  - grounding on Winter 2026, Fall 2025, employer-disjoint Fall 2025 (k/n and %)
  - four overlap shares (Berkeley, DeepLearning.AI, Harvard HDSR, Queen's MMAI)

Exactly replicates the Table 6 scoring:
  - vocabulary from ROOT/skill_lift_table.csv (73-row version used in original eval)
  - attestation from V4_2 W2026, V4_2 F2025, V4_2 employer-disjoint tables
  - z_min = 2.0, focal = "Agentic Ai", exact+alias grounding only
  - overlap = strict (exact+alias) share only
NO NETWORK, NO LLM.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # _SUBMISSION_DSS/repeated_generations
ROOT = HERE.parents[1]                           # repo root
sys.path.insert(0, str(ROOT))

from eval_grounding_overlap import (            # noqa: E402
    extract_skills, build_vocabulary,
    load_reference_courses, load_attested_skills,
    score_curriculum,
)

# ── fixed paths ───────────────────────────────────────────────────────────────
VOCAB_TABLE    = ROOT / "skill_lift_table.csv"          # root-level (73 Agentic Ai rows)
REFS           = ROOT / "reference_courses.json"
BUNDLE2        = ROOT / "_SUBMISSION_DSS/v60_recompute/v60_bundle2/results"
TABLE_W2026    = BUNDLE2 / "skill_lift_table_W2026.csv"
TABLE_F2025    = BUNDLE2 / "skill_lift_table_F2025.csv"
TABLE_DISJOINT = BUNDLE2 / "lift_S1_F2025_employer_disjoint_V4_2.csv"
FOCAL          = "Agentic Ai"
Z_MIN          = 2.0

COURSE_LABELS = {
    "A_berkeley_cs294": "Berkeley CS294",
    "B_deeplearning_ai": "DeepLearning.AI",
    "C_harvard_hdsr":   "Harvard HDSR",
    "D_queens_mmai":    "Queen's MMAI",
}

# ── load shared resources once ────────────────────────────────────────────────
courses  = load_reference_courses(REFS)
vocab    = build_vocabulary(VOCAB_TABLE, FOCAL, courses)
att_tabs = {
    "W2026":    set(load_attested_skills(TABLE_W2026,    FOCAL, Z_MIN).keys()),
    "F2025":    set(load_attested_skills(TABLE_F2025,    FOCAL, Z_MIN).keys()),
    "disjoint": set(load_attested_skills(TABLE_DISJOINT, FOCAL, Z_MIN).keys()),
}


def _pct(k, n):
    return f"{k}/{n} ({100*k/n:.1f}%)" if n else "0/0 (n/a)"


def score_file(path: Path) -> dict:
    text   = path.read_text(encoding="utf-8")
    skills = extract_skills(text, vocab)
    result = score_curriculum(skills, load_attested_skills(TABLE_W2026, FOCAL, Z_MIN), courses)
    n      = len(skills)
    gnd    = {k: len(skills & att) for k, att in att_tabs.items()}
    ovl    = {cid: len(result["overlap"][cid]["strict_matched"]) for cid in courses}
    return {"n": n, "grounding": gnd, "overlap": ovl}


def print_scores(label: str, r: dict) -> None:
    n = r["n"]
    print(f"\n{'-'*60}")
    print(f"  {label}")
    print(f"  Skills extracted: {n}")
    for tab_key, tab_label in [("W2026", "Winter 2026 (self)"),
                                 ("F2025", "Fall 2025 (held-out)"),
                                 ("disjoint", "Employer-disjoint F2025")]:
        k = r["grounding"][tab_key]
        print(f"  Grounding {tab_label}: {_pct(k, n)}")
    print("  Overlap (strict):")
    for cid, friendly in COURSE_LABELS.items():
        k = r["overlap"][cid]
        print(f"    {friendly}: {_pct(k, n)}")


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: score_curricula.py <file.txt> [<file2.txt> ...]")
    for arg in sys.argv[1:]:
        p = Path(arg)
        if not p.exists():
            print(f"\nWARNING: {p} not found — skipping")
            continue
        r = score_file(p)
        print_scores(str(p), r)
    print()


if __name__ == "__main__":
    main()
