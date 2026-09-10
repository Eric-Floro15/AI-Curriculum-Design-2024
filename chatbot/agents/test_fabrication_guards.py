"""
test_fabrication_guards.py — unit tests for all four anti-fabrication
guards in agents/orchestrator.py: attribution (_detect_fabrication_flags),
numeric (_detect_numeric_fabrication_flags), content-attribution
(_detect_content_attribution_flags — course codes / URLs / institutions),
and delegation-enforcement (_detect_required_specialists,
_strict_delegation_enabled, RequiredSpecialistMissingError).

No LLM, no CrewAI kickoff, no network — pure functions and regexes only,
exercised against synthetic step_log fixtures plus a few reconstructed
excerpts from real Set A dry-run records (dev lane gpt-oss:120b) that
exposed real bugs during development (a Unicode non-breaking hyphen
this project's model output actually uses, a nested-code-fence parsing
trap, and a character-class range bug). Safe to run anywhere, including
this sandbox.

Run:
    python chatbot/agents/test_fabrication_guards.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from agents.orchestrator import (  # noqa: E402
    _detect_fabrication_flags,
    _detect_numeric_fabrication_flags,
    _detect_content_attribution_flags,
    _detect_required_specialists,
    _strict_delegation_enabled,
    _COURSE_CODE_RE,
    _COURSE_CODE_ALLOWLIST,
    _URL_RE,
    _normalize_url,
    _is_report_year_citation,
    _write_run_record,
    RequiredSpecialistMissingError,
)

_FAILURES = []


def _check(label: str, condition: bool, detail: str = "") -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail and not condition else ""))
    if not condition:
        _FAILURES.append(label)


class _Finish:
    def __init__(self, output):
        self.output = output


def _steps(*role_text_pairs):
    return [{"role": r, "output": _Finish(t)} for r, t in role_text_pairs]


# =====================================================================
# A1 — course-code extraction regex
# =====================================================================
print("\n=== A1: course-code extraction ===")

_check(
    "matches an ASCII-hyphen alpha code",
    "CS330" in _COURSE_CODE_RE.findall("Take CS330 next semester."),
)
_check(
    "matches a spaced alpha code",
    "CS 224N" in _COURSE_CODE_RE.findall("Enroll in CS 224N for NLP."),
)
_check(
    "matches the U+2011 non-breaking hyphen this project's real output "
    "uses (confirmed in a live Set A record, 'MMAI‑902')",
    "MMAI‑902" in _COURSE_CODE_RE.findall("See MMAI‑902 AI Ethics."),
)
_check(
    "matches a bare numeric dept.number code (MIT/CMU style)",
    "6.7960" in _COURSE_CODE_RE.findall("Covers 6.7960 Deep Learning."),
)
_check(
    "matches a bare numeric dept-number code with ASCII hyphen",
    "11-651" in _COURSE_CODE_RE.findall("See course 11-651 for markets."),
)
_check(
    "does NOT match a bare small number with no code shape",
    "2" not in _COURSE_CODE_RE.findall("(2) mirror the proven structure"),
)
_check(
    "does NOT match a z-score expression",
    len(_COURSE_CODE_RE.findall("z=9.56")) == 0,
)
gpt4_matches = [m for m in _COURSE_CODE_RE.findall("Use GPT-4 for this.")]
_check(
    "GPT-4 is extracted by the raw regex (allowlist filters it downstream, "
    "not the regex itself)",
    "GPT-4" in gpt4_matches,
)
_check(
    "allowlist contains gpt-4/ec2/h100/co2 etc., checked case-insensitively",
    {"gpt-4", "ec2", "h100", "co2", "llama", "claude"} <= _COURSE_CODE_ALLOWLIST,
)


# =====================================================================
# A2 — URL extraction + normalization
# =====================================================================
print("\n=== A2: URL extraction + normalization ===")

_check(
    "extracts a bare https URL",
    _URL_RE.findall("See https://smith.queensu.ca/mmai for details.")
    == ["https://smith.queensu.ca/mmai"],
)
_check(
    "normalize strips trailing slash",
    _normalize_url("https://example.com/path/") == "https://example.com/path",
)
_check(
    "normalize strips trailing sentence punctuation",
    _normalize_url("https://example.com/path.") == "https://example.com/path",
)
_check(
    "normalize lowercases the host but not the path",
    _normalize_url("https://Example.COM/CaseSensitivePath")
    == "https://example.com/CaseSensitivePath",
)
_check(
    "normalize is idempotent for already-clean URLs",
    _normalize_url("https://example.com/path") == "https://example.com/path",
)


# =====================================================================
# A3 — institution detection
# =====================================================================
print("\n=== A3: institution detection ===")


def _institution_names(flags):
    # flags are full sentences; pull out the quoted institution name.
    # Lowercased for comparison since flag text preserves the answer's
    # original casing but this test compares against normalized keys.
    import re as _re
    out = []
    for f in flags:
        m = _re.search(r"unattributed_institution: '([^']+)'", f)
        if m:
            out.append(m.group(1).lower())
    return out


# Real Set A pattern: University Programs delegated, but genuinely never
# mentioned Cambridge — the Advisor added it. Cambridge should be flagged;
# Stanford (recognized) should not.
steps_a2_like = _steps((
    "University AI Programs Researcher",
    "MIT offers 6.7960 Deep Learning at https://eecs.mit.edu/6-4/.",
))
answer_a2_like = (
    "Stanford and MIT both cover deep learning. The University of "
    "Cambridge also has an MPhil in Machine Learning at "
    "https://www.mlmi.eng.cam.ac.uk/."
)
flags = _detect_content_attribution_flags(
    answer_a2_like, "compare AI programs", steps_a2_like,
    ["University AI Programs Researcher"],
)
names = _institution_names(flags)
_check(
    "flags a fabricated institution (Cambridge) not in consulted_text",
    "university of cambridge" in names,
    detail=str(names),
)
_check(
    "does NOT flag a recognized institution (Stanford) even though it's "
    "not literally in consulted_text this time",
    "stanford" not in names and "stanford university" not in names,
    detail=str(names),
)

# Real Set A5 pattern: an off-scope refusal that echoes the query's own
# institution mention must NOT be flagged.
steps_none = _steps(("Senior Curriculum Advisor", "N/A"))[:0]  # no specialists at all
answer_refusal = (
    "I'm sorry, I don't have the resources to recommend restaurants near "
    "the University of Toronto."
)
flags_refusal = _detect_content_attribution_flags(
    answer_refusal,
    "Can you tell me about the best restaurants near the University of Toronto?",
    steps_none, [],
)
_check(
    "does NOT flag an institution merely echoed back from the query itself "
    "(real Set A5 false positive, now fixed)",
    len(flags_refusal) == 0,
    detail=str(flags_refusal),
)

# Johns Hopkins: only exempt from the query-echo path if the query named it.
flags_jhu_named = _detect_content_attribution_flags(
    "Johns Hopkins offers a strong MPH program.",
    "Tell me about Johns Hopkins' MPH program.",
    [], [],
)
_check(
    "Johns Hopkins mention is NOT flagged when the query itself named it",
    len(_institution_names(flags_jhu_named)) == 0,
    detail=str(flags_jhu_named),
)
flags_jhu_unprompted = _detect_content_attribution_flags(
    "Johns Hopkins also offers a strong MPH program, unrelated to your question.",
    "What skills should a data engineer learn?",
    [], [],
)
_check(
    "Johns Hopkins mention IS flagged when the query never named it and no "
    "specialist returned it",
    "johns hopkins" in _institution_names(flags_jhu_unprompted),
    detail=str(flags_jhu_unprompted),
)

# A genuinely-delegated real peer program (Rotman, not pre-exempted by
# name) must not be flagged when a specialist actually returned it.
steps_rotman = _steps((
    "University AI Programs Researcher",
    "University of Toronto's Rotman MMA covers predictive analytics.",
))
flags_rotman_real = _detect_content_attribution_flags(
    "The University of Toronto's Rotman MMA program covers this well.",
    "which peer programs cover predictive analytics?",
    steps_rotman, ["University AI Programs Researcher"],
)
_check(
    "a genuinely-delegated real institution mention (Toronto/Rotman) is "
    "NOT flagged, via the verbatim consulted_text check alone (no "
    "hardcoded pre-exemption needed)",
    len(_institution_names(flags_rotman_real)) == 0,
    detail=str(flags_rotman_real),
)
# The SAME institution name, but fabricated (not actually returned this
# run) — must still be flagged despite Toronto being a real project
# institution in other contexts.
flags_toronto_fabricated = _detect_content_attribution_flags(
    "University of Toronto offers a MEng in Artificial Intelligence covering this.",
    "which peer programs cover predictive analytics?",
    [], [],
)
_check(
    "a FABRICATED Toronto program (not returned by any specialist this "
    "run) IS still flagged — confirms no blanket institution-name "
    "pre-exemption creates a blind spot (real Set A4 finding)",
    "university of toronto" in _institution_names(flags_toronto_fabricated),
    detail=str(flags_toronto_fabricated),
)

# Real Stage-2 (2026-09-10) false positive: prose honestly disclosing
# that a specialist wasn't consulted mentions its role name, "University
# AI Programs Researcher" — the generic "X University" matcher mistook
# "The University" (from "The University AI Programs Researcher could
# not be reached") for a fabricated institution, since it isn't
# followed by " of <Capitalized>" (the only case excluded until this
# fix).
flags_role_name_disclosure = _detect_content_attribution_flags(
    "Note: the University AI Programs Researcher could not be reached "
    "this run, so peer-program data is unavailable.",
    "Tell me about Johns Hopkins' MPH program and how it compares to AI/ML programs.",
    [], [],
)
_check(
    "an honest disclosure mentioning the 'University AI Programs "
    "Researcher' role name does NOT get mis-flagged as a fabricated "
    "'University' institution (real Stage-2 false positive, now fixed)",
    len(_institution_names(flags_role_name_disclosure)) == 0,
    detail=str(flags_role_name_disclosure),
)


# =====================================================================
# Required-specialist intent detection (Part B2)
# =====================================================================
print("\n=== B2: required-specialist intent detection ===")

_check(
    "peer-program query requires University AI Programs Researcher",
    "University AI Programs Researcher" in _detect_required_specialists(
        "which peer programs teach data engineering?"
    ),
)
_check(
    "named-institution query requires University AI Programs Researcher "
    "even without the word 'program' — via the MMAI degree-token match, "
    "not a bare institution-name trigger (removed in the Stage 2 "
    "refinement below)",
    "University AI Programs Researcher" in _detect_required_specialists(
        "What does Queen's MMAI cover?"
    ),
)
# Stage 2 refinement (2026-09-10): a bare institution/city name is no
# longer sufficient on its own — real Set A5 query, names "University of
# Toronto" but has zero program/comparison intent (a pure off-scope
# restaurant question), must NOT require University AI Programs
# Researcher. A3's JHU query genuinely compares to AI/ML programs and
# must still require it — the difference is intent language, not the
# presence of a university name.
_check(
    "A5's exact query (names an institution, zero program/comparison "
    "intent) requires NOTHING — the real false positive this stage fixed",
    _detect_required_specialists(
        "Can you tell me about the best restaurants near the University of Toronto?"
    )
    == set(),
)
_check(
    "A3's exact query (MPH degree token + 'compares to AI/ML programs') "
    "still correctly requires University AI Programs Researcher",
    "University AI Programs Researcher" in _detect_required_specialists(
        "Tell me about Johns Hopkins' MPH program in biostatistics and "
        "how it compares to AI/ML programs."
    ),
)
_check(
    "a bare institution name with NO intent language requires nothing "
    "(the removed trigger, tested directly)",
    _detect_required_specialists("Have you heard of Stanford University?") == set(),
)
_check(
    "cluster/gap query requires Cluster Interpreter",
    "Cluster Interpreter" in _detect_required_specialists(
        "Which skill clusters are missing from our curriculum?"
    ),
)
_check(
    "a query with BOTH intents requires both specialists (real A4 pattern)",
    _detect_required_specialists(
        "Which of the 6 peer programs cover these clusters, and which "
        "clusters are missing?"
    )
    >= {"University AI Programs Researcher", "Cluster Interpreter"},
)
_check(
    "an off-scope query with neither intent requires nothing",
    _detect_required_specialists("What's the best pizza place downtown?") == set(),
)
_check(
    "a pure market-demand query (no program/cluster language) requires nothing",
    _detect_required_specialists(
        "What are the top 5 in-demand technical skills for AI/ML roles?"
    )
    == set(),
)


# =====================================================================
# STRICT_DELEGATION config + exception type
# =====================================================================
print("\n=== STRICT_DELEGATION config ===")

_prev = os.environ.pop("STRICT_DELEGATION", None)
try:
    _check("STRICT_DELEGATION defaults to OFF when unset", not _strict_delegation_enabled())
    os.environ["STRICT_DELEGATION"] = "true"
    _check("STRICT_DELEGATION='true' is ON", _strict_delegation_enabled())
    os.environ["STRICT_DELEGATION"] = "1"
    _check("STRICT_DELEGATION='1' is ON", _strict_delegation_enabled())
    os.environ["STRICT_DELEGATION"] = "false"
    _check("STRICT_DELEGATION='false' is OFF", not _strict_delegation_enabled())
    os.environ["STRICT_DELEGATION"] = "garbage"
    _check("STRICT_DELEGATION=<garbage> is OFF (fails safe)", not _strict_delegation_enabled())
finally:
    if _prev is None:
        os.environ.pop("STRICT_DELEGATION", None)
    else:
        os.environ["STRICT_DELEGATION"] = _prev

_check(
    "RequiredSpecialistMissingError is a RuntimeError subclass",
    issubclass(RequiredSpecialistMissingError, RuntimeError),
)


# =====================================================================
# Regression: the two pre-existing guards (attribution, numeric) still
# behave correctly against real Set A/B4 patterns.
# =====================================================================
print("\n=== Attribution guard: honest-disclosure exemption (SONNET_delegation-check.md Step 1) ===")

# Real stage-2 wording (run_20260910T153646Z_stage2-A3-jhu-mph_success.md):
# an honest disclosure that a specialist wasn't reached, not a citation.
_jhu_disclosure_answer = (
    "**Contextual Gaps**\n\n"
    "- **Peer-program curriculum data**: The University AI Programs "
    "Researcher could not retrieve structured course lists for Johns "
    "Hopkins MPH Biostatistics or for the four benchmark AI/ML master's "
    "programs within the current tool budget. Consequently, no direct "
    "course-by-course comparison is available in this answer."
)
_check(
    "honest disclosure ('could not retrieve... within the current tool "
    "budget', real stage-2 wording) is NOT flagged as a fabricated "
    "citation",
    len(_detect_fabrication_flags(
        _jhu_disclosure_answer, ["AI Industry News Researcher", "Senior Curriculum Advisor"]
    )) == 0,
    detail=str(_detect_fabrication_flags(
        _jhu_disclosure_answer, ["AI Industry News Researcher", "Senior Curriculum Advisor"]
    )),
)

_check(
    "the same specialist name IS still flagged when presented as an "
    "actual source of content (not disclosure wording)",
    any(
        "University AI Programs Researcher" in f
        for f in _detect_fabrication_flags(
            "Per the University AI Programs Researcher, Queen's MMAI "
            "offers MMAI-902 AI Ethics.",
            ["AI Industry News Researcher", "Senior Curriculum Advisor"],
        )
    ),
)

_check(
    "a role mentioned ONCE as disclosure and ONCE as a real citation "
    "still flags — exemption requires EVERY mention to be disclosure-"
    "shaped, not just one",
    any(
        "University AI Programs Researcher" in f
        for f in _detect_fabrication_flags(
            "The University AI Programs Researcher could not be reached "
            "this run. Still, per the University AI Programs Researcher, "
            "Queen's MMAI offers MMAI-902 AI Ethics.",
            ["AI Industry News Researcher", "Senior Curriculum Advisor"],
        )
    ),
)

for _phrase in [
    "was not consulted", "were not consulted", "unavailable within the "
    "tool budget", "could not be reached", "did not consult",
]:
    _answer = f"The Cluster Interpreter {_phrase} this run."
    _flags = _detect_fabrication_flags(_answer, ["Senior Curriculum Advisor"])
    _check(
        f"disclosure phrase {_phrase!r} exempts the mention",
        len(_flags) == 0,
        detail=str(_flags),
    )


print("\n=== Regression: pre-existing attribution + numeric guards ===")

steps_b4 = _steps(("Cluster Interpreter", "Automation & Scripting: freq = 501."))
answer_b4_fabricated = (
    "Per the AI Industry News Researcher, 'MLOps Takes Center Stage', "
    "MIT Tech Review, May 2026, demand for Automation & Scripting "
    "(freq = 501) is high."
)
attr_flags = _detect_fabrication_flags(answer_b4_fabricated, ["Cluster Interpreter", "Senior Curriculum Advisor"])
_check(
    "attribution guard still flags an uninvoked specialist name",
    any("AI Industry News Researcher" in f for f in attr_flags),
    detail=str(attr_flags),
)

steps_finance = _steps(("Skills Taxonomy Analyst", "AutoGen lift 12.60x, z=4.65."))
num_flags_real = _detect_numeric_fabrication_flags(
    "AutoGen (lift 12.6x, z=4.65) is the top pick.",
    steps_finance, ["Skills Taxonomy Analyst"],
)
_check(
    "numeric guard does NOT flag a real, byte-matching lift/z value",
    len(num_flags_real) == 0,
    detail=str(num_flags_real),
)
num_flags_fake = _detect_numeric_fabrication_flags(
    "LangGraph (lift 99.9x, z=42.0) is the top pick.",
    steps_finance, ["Skills Taxonomy Analyst"],
)
_check(
    "numeric guard still flags an invented lift/z pair",
    len(num_flags_fake) == 2,
    detail=str(num_flags_fake),
)


# =====================================================================
# GUARD_TUNEUP_sonnet.md — Item 1: no more truncated saved traces
# =====================================================================
print("\n=== Item 1: companion full-text audit file ===")

_long_text = "Y" * 25_000 + " END_MARKER"
_long_steps = [{"role": "Skills Taxonomy Analyst", "output": _Finish(_long_text)}]
_test_path = _write_run_record(
    "item1 test query", _long_steps, 1.0, answer="short answer", error=None
)
_test_full_path = _test_path[:-len(".md")] + "_full.md"
try:
    _check(
        "a companion _full.md file is always written alongside the main record",
        os.path.exists(_test_full_path),
    )
    with open(_test_path, encoding="utf-8") as _f:
        _main_content = _f.read()
    with open(_test_full_path, encoding="utf-8") as _f:
        _full_content = _f.read()
    _check(
        "the main record truncates a long trace and says so",
        "END_MARKER" not in _main_content and "TRUNCATED" in _main_content,
    )
    _check(
        "the companion file has the COMPLETE, untruncated trace",
        _long_text in _full_content,
    )
finally:
    for _p in (_test_path, _test_full_path):
        if os.path.exists(_p):
            os.remove(_p)


# =====================================================================
# GUARD_TUNEUP_sonnet.md — Item 2: broader disclosure + capability-listing
# =====================================================================
print("\n=== Item 2: broadened attribution exemption ===")

# Real Sonnet A2 wording (run_20260910T172658Z_sonnet-A2-ai-trends_success.md):
# proactive routing rationale, not the "could not be reached" style
# Step-1's original regex was built from.
_a2_style = (
    "this query is specifically about industry trends and report findings "
    "— it does not mention peer programs, gap analysis, or clusters, so "
    "per my routing rules, the University AI Programs Researcher and "
    "Cluster Interpreter are not required this turn, and the Skills "
    "Taxonomy Analyst was not needed (the question is a pure fact-lookup, "
    "not a lift/significance curriculum-recommendation question)."
)
_a2_flags = _detect_fabrication_flags(
    _a2_style, ["AI Industry News Researcher", "Senior Curriculum Advisor"]
)
_check(
    "Sonnet A2's real 'not required this turn' / 'was not needed' wording "
    "is exempted (0 flags) — a routing-rationale phrasing Step 1's "
    "original regex didn't cover",
    len(_a2_flags) == 0,
    detail=str(_a2_flags),
)

# Real Sonnet A5 wording (run_20260910T174133Z_sonnet-A5-restaurants_success.md):
# a capability-listing refusal, structurally distinct from a disclosure
# sentence (the intro sits on its own line above each bulleted role).
_a5_style = (
    "My four specialists are:\n\n"
    "- **Skills Taxonomy Analyst** – AI/ML job market skill demand\n"
    "- **University AI Programs Researcher** – peer institution curricula\n"
    "- **AI Industry News Researcher** – recent AI/ML developments\n"
    "- **Cluster Interpreter** – curriculum gap analysis\n"
)
_a5_flags = _detect_fabrication_flags(_a5_style, ["Senior Curriculum Advisor"])
_check(
    "Sonnet A5's real capability-listing refusal is exempted (0 flags) — "
    "each role sits in its own newline-bounded 'sentence', separate from "
    "the intro phrase, so this needed a wider lookback than Item 2a's "
    "sentence-scoped disclosure check alone",
    len(_a5_flags) == 0,
    detail=str(_a5_flags),
)

# Paired still-catches #1: the original fabrication that motivated the
# attribution guard in the first place (a section header naming an
# uninvoked specialist, with real-looking fabricated findings).
_gap_analysis_fabrication = (
    "## Gap Analysis (Cluster Interpreter)\n\n"
    "The Cluster Interpreter identified three missing clusters: DevOps, "
    "Cloud, and MLOps."
)
_gap_flags = _detect_fabrication_flags(
    _gap_analysis_fabrication, ["Senior Curriculum Advisor"]
)
_check(
    "still catches: a fabricated 'Gap Analysis (Cluster Interpreter)' "
    "section with no disclosure/listing language survives Item 2's "
    "broadening unflagged-free — it's still flagged",
    any("Cluster Interpreter" in f for f in _gap_flags),
    detail=str(_gap_flags),
)

# Paired still-catches #2: a direct "According to <specialist>" content
# citation to a non-delegated specialist.
_according_to_fabrication = (
    "According to the University AI Programs Researcher, CMU offers a "
    "new AI ethics elective this year."
)
_according_flags = _detect_fabrication_flags(
    _according_to_fabrication, ["Senior Curriculum Advisor"]
)
_check(
    "still catches: 'According to <specialist>, <specific content>' is "
    "still flagged — Item 2's exemptions don't cover real citations",
    any("University AI Programs Researcher" in f for f in _according_flags),
    detail=str(_according_flags),
)


# =====================================================================
# GUARD_TUNEUP_sonnet.md — Item 3: course-code false positives
# =====================================================================
print("\n=== Item 3: report-year citations + real curated program codes ===")

for _code, _expect_report_year in [
    ("WEF 2025", True), ("HAI 2026", True), ("McKinsey 2025", False),
    # McKinsey is 8 letters, doesn't fit the 2-5 letter alpha-prefix
    # shape at all — included to confirm it's simply never extracted as
    # a candidate in the first place, not that the exclusion "misses" it.
    ("MIT 6-4", False), ("MMAI-902", False), ("CS330", False), ("6.7960", False),
]:
    _check(
        f"_is_report_year_citation({_code!r}) == {_expect_report_year}",
        _is_report_year_citation(_code) == _expect_report_year,
    )

_check(
    "'McKinsey 2025' is never extracted as a course-code CANDIDATE at "
    "all (8-letter prefix doesn't fit the 2-5 letter alpha branch), so "
    "it needs no exclusion to begin with",
    "McKinsey 2025" not in _COURSE_CODE_RE.findall("McKinsey 2025 report"),
)

_report_year_flags = _detect_content_attribution_flags(
    "Sources: WEF 2025 and Stanford HAI 2026 both highlight this trend.",
    "AI trends query", [], [],
)
_check(
    "real Sonnet report-citation wording ('WEF 2025', 'Stanford HAI "
    "2026') produces zero course-code flags end-to-end",
    not any(f.startswith("unattributed_course_code") for f in _report_year_flags),
    detail=str(_report_year_flags),
)

_mit_flags = _detect_content_attribution_flags(
    "Peer programs surveyed include MIT 6-4 and Queen's MMAI.",
    "compare peer programs", [], [],
)
_check(
    "the real MIT '6-4' program identifier, glued to the institution "
    "name, is NOT flagged as a fabricated course code (allowlisted, "
    "same class as the earlier 'MIT 6.7960' finding)",
    not any(f.startswith("unattributed_course_code") for f in _mit_flags),
    detail=str(_mit_flags),
)

# Paired still-catches #1: the original fabricated MMAI-902 (a course
# WITHIN the real MMAI program, but itself invented) must still flag —
# confirms the "mit 6-4" allowlist entry doesn't accidentally shadow
# fabricated MMAI course numbers.
_mmai_fabrication_flags = _detect_content_attribution_flags(
    "Queen's MMAI offers MMAI-902 AI Ethics, Law & Policy.",
    "compare peer programs", [], [],
)
_check(
    "still catches: fabricated 'MMAI-902' (a real program, invented "
    "course within it) is still flagged",
    any("MMAI" in f and f.startswith("unattributed_course_code") for f in _mmai_fabrication_flags),
    detail=str(_mmai_fabrication_flags),
)

# Paired still-catches #2: A4-style wholly invented peer-program codes
# (real Set A4 pattern — wrong institutions, invented course numbers).
_a4_fabrication_flags = _detect_content_attribution_flags(
    "University of Washington offers AI-405 and Imperial College offers CS9999.",
    "compare peer programs", [], [],
)
_check(
    "still catches: A4-style wholly invented course codes at fabricated "
    "peer institutions are still flagged",
    sum(1 for f in _a4_fabrication_flags if f.startswith("unattributed_course_code")) == 2,
    detail=str(_a4_fabrication_flags),
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
