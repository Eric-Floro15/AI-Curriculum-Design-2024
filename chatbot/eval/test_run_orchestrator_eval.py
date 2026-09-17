"""
test_run_orchestrator_eval.py — unit tests for the eval harness's own
grading logic (eval/run_orchestrator_eval.py), starting with Item 1 of
SUITE_step5 (2026-09-17): the negation-aware forbidden_substrings check.

No LLM, no CrewAI kickoff, no network — pure functions against synthetic
answer-text fixtures plus the real snippet from the false-FAIL this fixes
(curriculum-fetch-mmai, chatbot/run_records/run_20260917T060442Z_success_full.md).
Safe to run anywhere.

Run:
    python chatbot/eval/test_run_orchestrator_eval.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from eval.run_orchestrator_eval import (  # noqa: E402
    _substring_match,
    _forbidden_match_is_disclaimer_only,
    grade_case,
)

_FAILURES = []


def _check(label: str, condition: bool, detail: str = "") -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail and not condition else ""))
    if not condition:
        _FAILURES.append(label)


# =====================================================================
# Item 1 — disclaimer-only forbidden-phrase matches
# =====================================================================
print("\n=== Item 1: negation-aware forbidden_substrings ===")

# The real false-FAIL text (curriculum-fetch-mmai, run_20260917T060442Z).
_MMAI_DISCLAIMER_ANSWER = (
    "The Queen's University Smith School of Business Master of Management "
    "in Artificial Intelligence (MMAI) is a fixed-sequence, 12-month "
    "cohort program. No gap analysis has been performed at this stage — "
    "this document serves as a clean structured baseline for future "
    "curriculum comparison.\n\n"
    "| Cluster Interpreter | ❌ Not consulted | No gap analysis was "
    "requested at this stage. |\n\n"
    "When this inventory is used for gap analysis in a future step, "
    "those depth limitations should be kept in mind."
)

_check(
    "real false-FAIL text: every 'gap analysis' occurrence is disclaimer-only",
    _forbidden_match_is_disclaimer_only("gap analysis", _MMAI_DISCLAIMER_ANSWER),
)

_case_mmai = {
    "expected_substrings": [],
    "forbidden_substrings": ["gap analysis"],
    "must_delegate_to": [],
    "budget": {},
}
_result_mmai = {
    "answer": _MMAI_DISCLAIMER_ANSWER,
    "delegated_to": set(),
    "wall_time_sec": 10.0,
    "error": None,
}
_grade_mmai = grade_case(_case_mmai, _result_mmai, check_time=False)
_check(
    "grade_case: disclaimer-only match does NOT hard-fail",
    _grade_mmai["verdict"] != "FAIL",
    f"verdict={_grade_mmai['verdict']}, hard={_grade_mmai['hard']}",
)

# Still-catches: a genuine violation (the model actually performing the
# forbidden action, no negation cue nearby) must still FAIL.
_GENUINE_VIOLATION_ANSWER = (
    "Here is the gap analysis you requested, even though it wasn't asked "
    "for: Cluster 3 is critically underrepresented, missing ETL, Airflow, "
    "and dbt coverage entirely."
)
_check(
    "genuine violation: 'gap analysis' occurrence is NOT disclaimer-only",
    not _forbidden_match_is_disclaimer_only("gap analysis", _GENUINE_VIOLATION_ANSWER),
)
_case_violation = dict(_case_mmai)
_result_violation = {
    "answer": _GENUINE_VIOLATION_ANSWER,
    "delegated_to": set(),
    "wall_time_sec": 10.0,
    "error": None,
}
_grade_violation = grade_case(_case_violation, _result_violation, check_time=False)
_check(
    "grade_case: genuine violation still hard-FAILs",
    _grade_violation["verdict"] == "FAIL",
    f"verdict={_grade_violation['verdict']}",
)

# Mixed case: one disclaimer occurrence AND one genuine violation in the
# same answer — must still FAIL (not all occurrences are negated).
_MIXED_ANSWER = (
    "No gap analysis has been performed for this baseline fetch. "
    "Separately, here is a bonus gap analysis of Cluster 7: it is "
    "critically underrepresented."
)
_check(
    "mixed disclaimer + genuine violation: NOT treated as disclaimer-only",
    not _forbidden_match_is_disclaimer_only("gap analysis", _MIXED_ANSWER),
)

# A forbidden phrase that genuinely never occurs at all — _substring_match
# gates the call in grade_case, so this direct call should report
# found_any=False (no occurrences at all is a degenerate True from the
# function's own contract, but grade_case never reaches it because
# _substring_match already short-circuits to False first).
_check(
    "_substring_match still gates absent phrases (unaffected by this fix)",
    not _substring_match("gap analysis", "This answer never mentions the topic."),
)

# Unrelated forbidden substrings (no negation semantics expected/needed)
# are unaffected — e.g. a fabricated domain name is never "negated" away.
_check(
    "unrelated forbidden substring (courseleaf.com) still flags normally",
    not _forbidden_match_is_disclaimer_only(
        "courseleaf.com", "See the catalog at courseleaf.com for details."
    ),
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
