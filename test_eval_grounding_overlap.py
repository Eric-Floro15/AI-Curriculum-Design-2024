#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_eval_grounding_overlap.py — offline self-test for eval_grounding_overlap.py.

No LLM, no network -- pure functions against the real committed skill_lift_table.csv
and reference_courses.json, plus synthetic curriculum fixtures for the boundary cases.
Same "no LLM judge, deterministic, auditable" spirit as the harness itself.

Catches the real bug found while building this harness (2026-09-25): ALIASES mixed
normalised and unnormalised forms, so a genuinely-attested skill (Retrieval-Augmented
Generation (RAG), z=9.01 for focal skill 'Agentic Ai') reported as ungrounded because
neither the alias key nor its canonical value ever equalled its own _norm()'d form via
plain string containment. Fixed by routing every alias lookup through a fully-
normalised _NORM_ALIASES table built once at import time.

Run:
    python3 test_eval_grounding_overlap.py
"""

import sys
from pathlib import Path

from eval_grounding_overlap import (
    _canonical,
    _norm,
    build_vocabulary,
    extract_skills,
    load_attested_skills,
    load_reference_courses,
    match_tier,
    score_curriculum,
)

_FAILURES = []
_ROOT = Path(__file__).parent
_LIFT = _ROOT / "chatbot" / "data" / "skill_lift_table.csv"
_REFS = _ROOT / "reference_courses.json"


def _check(label: str, condition: bool, detail: str = "") -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail and not condition else ""))
    if not condition:
        _FAILURES.append(label)


# =====================================================================
# Real-data sanity: the lift table + reference courses load as expected
# =====================================================================
print("=== Real-data loading ===")

_attested = load_attested_skills(_LIFT, "Agentic Ai", 2.0)
_check(
    "73 skills attested at z>=2 for focal skill 'Agentic Ai' (matches memory/"
    "action-items.md's documented count)",
    len(_attested) == 73,
    f"got {len(_attested)}",
)

_courses = load_reference_courses(_REFS)
_check(
    "reference_courses.json has exactly the 4 expected course ids",
    set(_courses.keys()) == {"A_berkeley_cs294", "B_deeplearning_ai", "C_harvard_hdsr", "D_queens_mmai"},
    f"got {sorted(_courses.keys())}",
)
_check(
    "Queen's MMAI (D) skill list is non-trivial (real course, not still provisional/empty)",
    len(_courses["D_queens_mmai"]["skills"]) >= 15,
    f"got {len(_courses['D_queens_mmai']['skills'])} skills",
)

_vocab = build_vocabulary(_LIFT, "Agentic Ai", _courses)


# =====================================================================
# The real bug this file exists to catch: RAG must be recognised as
# BOTH extractable from text AND grounded (it is genuinely attested,
# z=9.01) despite the lift table's own column spelling it
# "Retrieval-Augmented Generation (Rag)" (hyphen + parens) while a
# curriculum might write it as bare "RAG".
# =====================================================================
print("\n=== Alias normalisation (the real bug found building this harness) ===")

_check(
    "RAG's canonical form is grounded (present in the real z>=2 attested set)",
    _canonical("Retrieval-Augmented Generation (RAG)") in _attested,
    f"attested keys sample: {list(_attested.keys())[:5]}",
)
_rag_extracted = extract_skills("This course covers RAG extensively.", _vocab)
_check(
    "bare 'RAG' in free text extracts to the same canonical form as the lift "
    "table's own spelling",
    _canonical("Retrieval-Augmented Generation (RAG)") in _rag_extracted,
    f"got {_rag_extracted}",
)
_rag_score = score_curriculum(_rag_extracted, _attested, _courses)
_check(
    "a curriculum containing only 'RAG' scores 100% grounding, not 0%",
    _rag_score["grounding_pct"] == 1.0,
    f"got {_rag_score['grounding_pct']}",
)


# =====================================================================
# Match tiers
# =====================================================================
print("\n=== Match tiers ===")

_check(
    "identical canonical skills match 'exact'",
    match_tier(_canonical("Multi-Agent Systems"), {_canonical("multi-agent systems")}) == "exact",
)
_check(
    "a close-but-not-identical phrasing matches 'fuzzy', not 'exact' or None",
    match_tier(_canonical("Agentic AI Frameworks"), {_canonical("Agentic Frameworks")}) == "fuzzy",
)
_check(
    "an unrelated skill matches neither tier (None)",
    match_tier(_canonical("Microsoft Excel"), {_canonical("Retrieval-Augmented Generation (RAG)")}) is None,
)


# =====================================================================
# Synthetic boundary cases: a curriculum built entirely from real
# attested/course skills vs. one built entirely from irrelevant terms.
# =====================================================================
print("\n=== Synthetic boundary cases ===")

_good_text = (
    "This course covers Retrieval-Augmented Generation (RAG), LangChain, LangGraph, "
    "CrewAI, AutoGen, Multi-Agent Systems, Prompt Engineering, Vector Databases, and "
    "Orchestration Tools. Students learn to build agentic frameworks using large "
    "language models."
)
_junk_text = (
    "This course covers Microsoft Excel, PowerPoint, basic accounting, and conflict "
    "resolution skills for office administration."
)

_good_skills = extract_skills(_good_text, _vocab)
_good_score = score_curriculum(_good_skills, _attested, _courses)
_check(
    "a curriculum written entirely in genuinely-attested agentic skills grounds "
    "at 100%",
    _good_score["grounding_pct"] == 1.0,
    f"got {_good_score['grounding_pct']}, ungrounded={_good_score['ungrounded_skills']}",
)
_check(
    "that curriculum overlaps Harvard's executive course (C) at exactly 0% -- "
    "the expected contrast-pole behaviour per decision #49's framing guardrail",
    _good_score["overlap"]["C_harvard_hdsr"]["total_overlap_pct"] == 0.0,
    f"got {_good_score['overlap']['C_harvard_hdsr']}",
)
_check(
    "that curriculum overlaps the tool-focused DeepLearning.AI course (B) more "
    "than the theory-focused Berkeley course (A), matching external_reference_"
    "curricula.md's own 'tightest tool match' characterisation of B",
    _good_score["overlap"]["B_deeplearning_ai"]["strict_overlap_pct"]
    >= _good_score["overlap"]["A_berkeley_cs294"]["strict_overlap_pct"],
    f"A={_good_score['overlap']['A_berkeley_cs294']['strict_overlap_pct']}, "
    f"B={_good_score['overlap']['B_deeplearning_ai']['strict_overlap_pct']}",
)

_junk_skills = extract_skills(_junk_text, _vocab)
_junk_score = score_curriculum(_junk_skills, _attested, _courses)
_check(
    "a curriculum with zero agentic-relevant content grounds at 0%, not crashing "
    "on an empty-overlap edge case",
    _junk_score["grounding_pct"] == 0.0,
    f"got {_junk_score['grounding_pct']}",
)
_check(
    "that same junk curriculum overlaps every reference course at 0%",
    all(ov["total_overlap_pct"] == 0.0 for ov in _junk_score["overlap"].values()),
    f"got {_junk_score['overlap']}",
)


# =====================================================================
# Empty-curriculum edge case (n=0) must not raise ZeroDivisionError
# =====================================================================
print("\n=== Edge case: empty extraction ===")

_empty_score = score_curriculum(set(), _attested, _courses)
_check(
    "an empty skill set reports grounding_pct=None (undefined), not a crash "
    "or a misleading 0%/100%",
    _empty_score["grounding_pct"] is None,
    f"got {_empty_score['grounding_pct']}",
)


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
