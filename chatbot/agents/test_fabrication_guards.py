"""
test_fabrication_guards.py — unit tests for all five anti-fabrication
guards in agents/orchestrator.py: attribution (_detect_fabrication_flags),
numeric (_detect_numeric_fabrication_flags), content-attribution
(_detect_content_attribution_flags — course codes / URLs / institutions),
delegation-claim honesty (_detect_delegation_claim_flags — a false "was
consulted" process claim, distinct from content attribution), and
delegation-enforcement (_detect_required_specialists,
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
    _detect_delegation_claim_flags,
    _detect_required_specialists,
    _strict_delegation_enabled,
    _COURSE_CODE_RE,
    _COURSE_CODE_ALLOWLIST,
    _URL_RE,
    _normalize_url,
    _is_report_year_citation,
    _normalize_institution_text,
    _strip_institution_code_prefix,
    _write_run_record,
    _format_cost_section,
    _estimate_cost_usd,
    _extract_market_numbers,
    _normalize_market_num,
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
# POLISH_attribution-flip_and_cost-tracking.md — Item A: inverted
# attribution guard (positive detector, not exemption blocklist)
# =====================================================================
print("\n=== Item A: inverted attribution guard ===")

# Still-catches, third shape: a bare "— Role" source line (the third
# citation shape named in the spec, not yet covered by any earlier test
# — the header and "According to" shapes already have paired tests
# above from the guard-tuneup work).
_source_line_fabrication = (
    "Automation & Scripting shows the highest lift this quarter.\n"
    "— Cluster Interpreter\n"
    "More findings follow."
)
_source_line_flags = _detect_fabrication_flags(
    _source_line_fabrication, ["Senior Curriculum Advisor"]
)
_check(
    "still catches: a bare '— Role' source line credits content to a "
    "non-delegated specialist",
    any("Cluster Interpreter" in f for f in _source_line_flags),
    detail=str(_source_line_flags),
)

# The exact sentence that slipped through the old exemption-based design
# on Run 1 (d126756) — a hypothetical/conditional FUTURE routing plan,
# not a citation, not disclosure-phrased, not capability-listing-shaped.
_run1_hypothetical_routing = (
    "The professor's query did not explicitly request a cluster-level "
    "gap analysis of an existing curriculum, so the Cluster Interpreter "
    "was not consulted this run in order to stay within delegation "
    "budget. If you would like a systematic cluster-level gap analysis "
    "— showing which of the 10 CSPA ensemble skill clusters your "
    "current ML course covers vs. what an agentic AI course would "
    "address — provide or upload your current course list and I will "
    "route that through the University AI Programs Researcher (for "
    "structured curriculum extraction) and the Cluster Interpreter in "
    "sequence."
)
_run1_flags = _detect_fabrication_flags(
    _run1_hypothetical_routing,
    ["AI Industry News Researcher", "Senior Curriculum Advisor",
     "Skills Taxonomy Analyst", "University AI Programs Researcher"],
)
_check(
    "the exact Run 1 (d126756) hypothetical-future-routing sentence — "
    "the real false positive this item fixes — is NOT flagged under "
    "the inverted design",
    len(_run1_flags) == 0,
    detail=str(_run1_flags),
)

# Full end-to-end validation against Run 1's actual saved record: zero
# flags of any kind (attribution was the only flag it ever had).
_run1_record_path = os.path.join(
    _HERE, "..", "run_records",
    "run_20260910T212751Z_sonnet-run1-agentic-curriculum_success.md",
)
if os.path.exists(_run1_record_path):
    with open(_run1_record_path, encoding="utf-8") as _f:
        _run1_content = _f.read()
    import re as _re_mod
    _run1_delegated = eval(_re_mod.search(  # noqa: S307 - trusted local fixture file
        r"\*\*Delegated to:\*\* (\[.*?\])", _run1_content
    ).group(1))
    _run1_ans_start = _run1_content.index("## Final Answer") + len("## Final Answer")
    _run1_ans_end = _run1_content.index("## Per-Agent Tool-Call Trace")
    _run1_answer = _run1_content[_run1_ans_start:_run1_ans_end].strip()
    _run1_real_flags = _detect_fabrication_flags(_run1_answer, _run1_delegated)
    _check(
        "Run 1's real saved record (d126756) now shows ZERO attribution "
        "flags — it previously had exactly one, on 'Cluster Interpreter'",
        len(_run1_real_flags) == 0,
        detail=str(_run1_real_flags),
    )
else:
    print("  (skipped: Run 1's saved record not found at expected path)")


# =====================================================================
# POLISH_attribution-flip_and_cost-tracking.md — Item B: cost tracking
# =====================================================================
print("\n=== Item B: cost/usage tracking ===")


class _FakeUsage:
    prompt_tokens = 12_000
    completion_tokens = 3_000
    total_tokens = 15_000
    cached_prompt_tokens = 500
    cache_creation_tokens = 200
    successful_requests = 17


_check(
    "None usage_metrics writes 'usage unavailable', not a crash",
    "usage unavailable" in "\n".join(_format_cost_section(None)),
)


class _WeirdUsage:
    pass


_check(
    "an unexpected-shape usage_metrics object also writes 'usage "
    "unavailable' rather than raising",
    "usage unavailable" in "\n".join(_format_cost_section(_WeirdUsage())),
)

_check(
    "_estimate_cost_usd computes the expected dollar figure for "
    "anthropic/claude-sonnet-4-6 (12000 prompt + 3000 completion tokens "
    "at $3/$15 per million)",
    abs(_estimate_cost_usd("anthropic", "claude-sonnet-4-6", 12_000, 3_000) - 0.081) < 1e-9,
)
_check(
    "_estimate_cost_usd returns None for a provider/model with no price "
    "entry (no fabricated dollar figure)",
    _estimate_cost_usd("ollama-cloud", "gpt-oss:120b", 12_000, 3_000) is None,
)

_cost_lines = _format_cost_section(_FakeUsage())
_cost_text = "\n".join(_cost_lines)
_check(
    "a real usage_metrics object renders all token counts",
    "12,000" in _cost_text and "3,000" in _cost_text and "15,000" in _cost_text,
    detail=_cost_text,
)

_prev_provider = os.environ.get("LLM_PROVIDER")
_prev_model = os.environ.get("LLM_MODEL")
try:
    os.environ["LLM_PROVIDER"] = "anthropic"
    os.environ["LLM_MODEL"] = "claude-sonnet-4-6"
    _priced_text = "\n".join(_format_cost_section(_FakeUsage()))
    _check(
        "the Cost/Usage section includes an approx. dollar figure when "
        "the env vars resolve to a known-priced model",
        "Approx. cost:** $0.0810" in _priced_text,
        detail=_priced_text,
    )

    os.environ["LLM_PROVIDER"] = "ollama-cloud"
    os.environ["LLM_MODEL"] = "gpt-oss:120b"
    _unpriced_text = "\n".join(_format_cost_section(_FakeUsage()))
    _check(
        "the Cost/Usage section reports 'not estimated' (never a "
        "fabricated dollar figure) for an unpriced provider/model, "
        "while still showing real token counts",
        "not estimated" in _unpriced_text and "12,000" in _unpriced_text,
        detail=_unpriced_text,
    )
finally:
    if _prev_provider is None:
        os.environ.pop("LLM_PROVIDER", None)
    else:
        os.environ["LLM_PROVIDER"] = _prev_provider
    if _prev_model is None:
        os.environ.pop("LLM_MODEL", None)
    else:
        os.environ["LLM_MODEL"] = _prev_model

# End-to-end: _write_run_record() actually calls _format_cost_section()
# and the section lands in the saved file.
_cost_test_steps = [{"role": "Skills Taxonomy Analyst", "output": _Finish("short output")}]
_cost_test_path = _write_run_record(
    "cost test query", _cost_test_steps, 1.0, answer="short answer",
    error=None, usage_metrics=_FakeUsage(),
)
_cost_test_full_path = _cost_test_path[:-len(".md")] + "_full.md"
try:
    with open(_cost_test_path, encoding="utf-8") as _f:
        _saved_content = _f.read()
    _check(
        "_write_run_record() writes a '## Cost / Usage' section with "
        "real token counts into the actual saved run record",
        "## Cost / Usage" in _saved_content and "12,000" in _saved_content,
    )
finally:
    for _p in (_cost_test_path, _cost_test_full_path):
        if os.path.exists(_p):
            os.remove(_p)


# =====================================================================
# GUARD_POLISH_batch.md, Item A: numeric guard — rounded prose ranges
# =====================================================================
print("\n=== GUARD-POLISH Item A: rounded prose ranges ===")

_itemA_trace = (
    "Generative Ai (lift 5.05x, z=6.46) ... Multi-Agent Systems (lift "
    "13.11x, z=5.08) ... CrewAI (lift 13.14x, z=5.01)"
)
_itemA_steps = _steps(("Skills Taxonomy Analyst", _itemA_trace))

_itemA_flags_range = _detect_numeric_fabrication_flags(
    "The distinctive skills range from roughly 5x to 13x above baseline.",
    _itemA_steps, ["Skills Taxonomy Analyst"],
)
_check(
    "no-longer-FP: a rounded prose range ('5x to 13x') whose endpoints "
    "are plausible roundings of real grounded lift values is not flagged",
    _itemA_flags_range == [],
    f"unexpected flags: {_itemA_flags_range}",
)

_itemA_flags_dash = _detect_numeric_fabrication_flags(
    "Lift values span 5x-13x across the identified skills.",
    _itemA_steps, ["Skills Taxonomy Analyst"],
)
_check(
    "no-longer-FP: same range with a dash separator ('5x-13x') is also "
    "not flagged",
    _itemA_flags_dash == [],
    f"unexpected flags: {_itemA_flags_dash}",
)

_itemA_flags_specific = _detect_numeric_fabrication_flags(
    "One skill shows an exceptional lift of 50x with z=30, unmatched by anything else.",
    _itemA_steps, ["Skills Taxonomy Analyst"],
)
_check(
    "still-catches: a fabricated SPECIFIC value ('50x / z=30' for a "
    "named skill), not part of a range construct, stays flagged",
    len(_itemA_flags_specific) >= 1
    and any("50" in f for f in _itemA_flags_specific),
    f"got: {_itemA_flags_specific}",
)

_itemA_flags_bad_range = _detect_numeric_fabrication_flags(
    "Lift values range from 5x to 99x across the board.",
    _itemA_steps, ["Skills Taxonomy Analyst"],
)
_check(
    "a range with one fabricated endpoint (99x, no grounded value near "
    "it) still flags that endpoint — the range exemption doesn't "
    "blanket-launder an unrelated bad number",
    any("99" in f for f in _itemA_flags_bad_range),
    f"got: {_itemA_flags_bad_range}",
)


# =====================================================================
# GUARD_POLISH_batch.md, Item B: institution guard — phrasing/substring
# =====================================================================
print("\n=== GUARD-POLISH Item B: institution phrasing/substring ===")

_itemB_trace = (
    "Institution 2: University of Toronto — Rotman School of "
    "Management, MMA program. Source: sgs.calendar.utoronto.ca"
)
_itemB_steps = _steps(("University AI Programs Researcher", _itemB_trace))

_check(
    "_normalize_institution_text collapses dash + whitespace variants "
    "to the same normalized form",
    _normalize_institution_text("University of Toronto — Rotman School of Management")
    == _normalize_institution_text("university of toronto rotman school of management"),
)

_itemB_flags_ok = _detect_content_attribution_flags(
    "University of Toronto Rotman offers a strong analytics-focused MMA.",
    "query", _itemB_steps, ["University AI Programs Researcher"],
)
_check(
    "no-longer-FP: 'University of Toronto Rotman' is not flagged when "
    "the trace phrases it 'University of Toronto — Rotman School of "
    "Management' (dash-separated, not concatenated)",
    _itemB_flags_ok == [],
    f"unexpected flags: {_itemB_flags_ok}",
)

_itemB_flags_bad = _detect_content_attribution_flags(
    "University of Fabricationland has an excellent AI program.",
    "query", _itemB_steps, ["University AI Programs Researcher"],
)
_check(
    "still-catches: a fabricated 'University of Fabricationland', "
    "absent from every trace, stays flagged",
    len(_itemB_flags_bad) >= 1
    and any("Fabricationland" in f for f in _itemB_flags_bad),
    f"got: {_itemB_flags_bad}",
)


# =====================================================================
# GUARD_POLISH_batch.md, Item C: course-code guard — institution prefix
# =====================================================================
print("\n=== GUARD-POLISH Item C: institution-prefixed codes ===")

_check(
    "_strip_institution_code_prefix strips a leading institution token",
    _strip_institution_code_prefix("cmu 17-762") == "17-762",
)
_check(
    "_strip_institution_code_prefix returns None for a glued form with "
    "no separate leading token (nothing to strip)",
    _strip_institution_code_prefix("cs330") is None,
)

_itemC_trace = "CMU MSAII: 17-762 Law of Computer Technology (required)."
_itemC_steps = _steps(("University AI Programs Researcher", _itemC_trace))

_itemC_flags_ok = _detect_content_attribution_flags(
    "The CMU 17-762 course covers AI regulation and startup law.",
    "query", _itemC_steps, ["University AI Programs Researcher"],
)
_check(
    "no-longer-FP: 'CMU 17-762' is not flagged when the trace contains "
    "the bare '17-762'",
    _itemC_flags_ok == [],
    f"unexpected flags: {_itemC_flags_ok}",
)

_itemC_flags_bad = _detect_content_attribution_flags(
    "The CMU 99-999 course covers a fabricated topic.",
    "query", _itemC_steps, ["University AI Programs Researcher"],
)
_check(
    "still-catches: a fabricated 'CMU 99-999' whose bare '99-999' "
    "appears in no trace stays flagged",
    len(_itemC_flags_bad) >= 1
    and any("99-999" in f for f in _itemC_flags_bad),
    f"got: {_itemC_flags_bad}",
)


# =====================================================================
# GUARD_POLISH_batch.md, Item D: course-code guard — medical standards
# =====================================================================
print("\n=== GUARD-POLISH Item D: medical-standard acronyms ===")

for _acronym in ("icd-10", "hl7", "fhir", "snomed", "snomed ct", "loinc", "umls", "dsm-5"):
    _check(
        f"'{_acronym}' is in the course-code allowlist",
        _acronym in _COURSE_CODE_ALLOWLIST,
    )

_itemD_steps = _steps(("University AI Programs Researcher", "no course-code content here"))

_itemD_flags_ok = _detect_content_attribution_flags(
    "Clinical ontologies include ICD-10 and HL7 standards for interoperability.",
    "query", _itemD_steps, ["University AI Programs Researcher"],
)
_check(
    "no-longer-FP: 'ICD-10' and 'HL7' are not flagged as course codes",
    _itemD_flags_ok == [],
    f"unexpected flags: {_itemD_flags_ok}",
)

_itemD_flags_bad = _detect_content_attribution_flags(
    "The fabricated course 11-999 covers an invented topic.",
    "query", _itemD_steps, ["University AI Programs Researcher"],
)
_check(
    "still-catches: a fabricated '11-999', not a domain-standard "
    "acronym and absent from every trace, stays flagged",
    len(_itemD_flags_bad) >= 1
    and any("11-999" in f for f in _itemD_flags_bad),
    f"got: {_itemD_flags_bad}",
)


# =====================================================================
# GUARD_POLISH_batch.md, Item E: NEW delegation-claim honesty guard
# =====================================================================
print("\n=== GUARD-POLISH Item E: delegation-claim honesty (new guard) ===")

_role = "University AI Programs Researcher"

_itemE_flags_claim = _detect_delegation_claim_flags(
    "The University AI Programs Researcher was consulted but no "
    "verified peer-program data was returned.",
    delegated_to=[],
)
_check(
    "still-catches: an affirmative 'was consulted' claim naming a "
    "specialist absent from delegated_to is flagged (the real RUN2C "
    "healthcare dev-lane finding)",
    len(_itemE_flags_claim) == 1 and _role in _itemE_flags_claim[0],
    f"got: {_itemE_flags_claim}",
)

_itemE_flags_neg1 = _detect_delegation_claim_flags(
    "The University AI Programs Researcher was not consulted this run.",
    delegated_to=[],
)
_check(
    "no-clean-flag: honest negative disclosure ('was not consulted') "
    "is not flagged",
    _itemE_flags_neg1 == [],
    f"unexpected flags: {_itemE_flags_neg1}",
)

_itemE_flags_neg2 = _detect_delegation_claim_flags(
    "The University AI Programs Researcher wasn't needed for this "
    "particular question.",
    delegated_to=[],
)
_check(
    "no-clean-flag: contracted negation ('wasn't needed') is not "
    "flagged",
    _itemE_flags_neg2 == [],
    f"unexpected flags: {_itemE_flags_neg2}",
)

_itemE_flags_cond = _detect_delegation_claim_flags(
    "If you provide your course list, I'll route it through the "
    "Cluster Interpreter for a full gap analysis.",
    delegated_to=[],
)
_check(
    "no-clean-flag: a conditional/future routing sentence ('I'll "
    "route it through <role>') is not flagged — present/future tense, "
    "not the past-tense claim this guard looks for",
    _itemE_flags_cond == [],
    f"unexpected flags: {_itemE_flags_cond}",
)

_itemE_flags_unavailable = _detect_delegation_claim_flags(
    "The University AI Programs Researcher was unavailable and could "
    "not be reached this run.",
    delegated_to=[],
)
_check(
    "no-clean-flag: 'unavailable' / 'could not be reached' phrasing is "
    "not flagged",
    _itemE_flags_unavailable == [],
    f"unexpected flags: {_itemE_flags_unavailable}",
)

_itemE_flags_delegated = _detect_delegation_claim_flags(
    "The University AI Programs Researcher was consulted and returned "
    "real peer-program data.",
    delegated_to=[_role],
)
_check(
    "a role that IS in delegated_to is never flagged for a "
    "consultation claim, even the same affirmative phrasing",
    _itemE_flags_delegated == [],
    f"unexpected flags: {_itemE_flags_delegated}",
)

# End-to-end: confirm this new guard is actually wired into the
# combined fabrication_flags list _write_run_record() produces (not
# just callable in isolation).
_itemE_e2e_steps = _steps(
    ("Skills Taxonomy Analyst", "Large Language Models (lift 6.17x, z=9.56)")
)
_itemE_e2e_path = _write_run_record(
    "test query for Item E wiring", _itemE_e2e_steps, 1.0,
    answer=(
        "Large Language Models (lift 6.17x, z=9.56). The University AI "
        "Programs Researcher was consulted for peer benchmarking."
    ),
    error=None, usage_metrics=None,
)
_itemE_e2e_full_path = _itemE_e2e_path[:-len(".md")] + "_full.md"
try:
    with open(_itemE_e2e_path, encoding="utf-8") as _f:
        _itemE_e2e_content = _f.read()
    _check(
        "_detect_delegation_claim_flags is wired into the real "
        "fabrication_flags list _write_run_record() saves",
        "delegation_claim:" in _itemE_e2e_content
        and "University AI Programs Researcher" in _itemE_e2e_content,
        "delegation_claim: substring not found in saved record",
    )
finally:
    for _p in (_itemE_e2e_path, _itemE_e2e_full_path):
        if os.path.exists(_p):
            os.remove(_p)


# =====================================================================
# SUITE_step5_regrade-cleanup.md, Item 3: two new FP guard shapes found
# on the real paid-Sonnet SUITE_step4 batch (2026-09-17)
# =====================================================================
print("\n=== SUITE_step5 Item 3: floored lift + residual range-summary ===")

# --- Shape 1: floored/approximate lift ("over N×", "more than N×") ---
_s5_trace_jax = "JAX co-demand: PyTorch (lift 20.14x, z=2.85)."
_s5_steps_jax = _steps(("Skills Taxonomy Analyst", _s5_trace_jax))

_s5_flags_over20 = _detect_numeric_fabrication_flags(
    "When a job mentions JAX, it is over 20x more likely to also require PyTorch.",
    _s5_steps_jax, ["Skills Taxonomy Analyst"],
)
_check(
    "no-longer-FP: 'over 20x' floored from a real grounded 20.14x is not flagged",
    _s5_flags_over20 == [],
    f"unexpected flags: {_s5_flags_over20}",
)

_s5_trace_mlops = "MLOps co-demand: Responsible AI (lift 9.03x, z=4.09)."
_s5_steps_mlops = _steps(("Skills Taxonomy Analyst", _s5_trace_mlops))

_s5_flags_over9 = _detect_numeric_fabrication_flags(
    "Responsible AI clears z=4.09 with lift over 9x — not a footnote.",
    _s5_steps_mlops, ["Skills Taxonomy Analyst"],
)
_check(
    "no-longer-FP: 'more than'-style qualifier ('lift over 9x') floored "
    "from a real grounded 9.03x is not flagged",
    _s5_flags_over9 == [],
    f"unexpected flags: {_s5_flags_over9}",
)

_s5_flags_more_than = _detect_numeric_fabrication_flags(
    "This skill shows more than 20x the baseline co-demand rate.",
    _s5_steps_jax, ["Skills Taxonomy Analyst"],
)
_check(
    "no-longer-FP: 'more than 20x' (new qualifier word) floored from the "
    "same real grounded 20.14x is not flagged",
    _s5_flags_more_than == [],
    f"unexpected flags: {_s5_flags_more_than}",
)

_s5_flags_bad_over90 = _detect_numeric_fabrication_flags(
    "This skill shows a lift of over 90x versus baseline, dwarfing everything else.",
    _s5_steps_jax, ["Skills Taxonomy Analyst"],
)
_check(
    "still-catches: a fabricated floored value ('over 90x' with no "
    "grounded value anywhere near it) still flags — the qualifier word "
    "alone is not a blanket exemption",
    len(_s5_flags_bad_over90) >= 1 and any("90" in f for f in _s5_flags_bad_over90),
    f"got: {_s5_flags_bad_over90}",
)

# --- Shape 2a: residual range-summary, numeric guard (single trailing x) ---
_s5_trace_orch = (
    "LangGraph (lift 12.25x, z=6.83) ... CrewAI (lift 13.14x, z=5.01) ... "
    "AutoGen (lift 12.60x, z=4.65)"
)
_s5_steps_orch = _steps(("Skills Taxonomy Analyst", _s5_trace_orch))

_s5_flags_range_single_x = _detect_numeric_fabrication_flags(
    "Their lift scores are the highest in the dataset (12-13x) — intensely concentrated.",
    _s5_steps_orch, ["Skills Taxonomy Analyst"],
)
_check(
    "no-longer-FP: a range with only ONE trailing '×' symbol ('12-13x', "
    "not '12x-13x') whose endpoints are grounded is not flagged",
    _s5_flags_range_single_x == [],
    f"unexpected flags: {_s5_flags_range_single_x}",
)

_s5_flags_bad_range_single_x = _detect_numeric_fabrication_flags(
    "Their lift scores are the highest in the dataset (50-99x) — unmatched by anything real.",
    _s5_steps_orch, ["Skills Taxonomy Analyst"],
)
_check(
    "still-catches: a fabricated single-trailing-x range ('50-99x' with "
    "nothing grounded near either endpoint) still flags",
    len(_s5_flags_bad_range_single_x) >= 1
    and any("99" in f for f in _s5_flags_bad_range_single_x),
    f"got: {_s5_flags_bad_range_single_x}",
)

# --- Shape 2b: residual range-summary, content-attribution guard ------
# A bare "N-NNN" posting-count range structurally matches the same
# bare-digit-pair course-code shape as real MIT/CMU codes ("10-601").
_s5_flags_postings_range = _detect_content_attribution_flags(
    "Their posting frequencies are moderate (~80-190 postings), but their lift scores lead.",
    "How strong is market demand for these tools?",
    _s5_steps_orch, ["Skills Taxonomy Analyst"],
)
_check(
    "no-longer-FP: a bare digit-pair range immediately followed by "
    "'postings' ('80-190 postings') is not flagged as unattributed_course_code",
    not any("80" in f or "190" in f for f in _s5_flags_postings_range),
    f"unexpected flags: {_s5_flags_postings_range}",
)

_s5_flags_bad_code = _detect_content_attribution_flags(
    "See course 15-999 for the full syllabus and prerequisites.",
    "What courses does this program require?",
    _s5_steps_orch, ["Skills Taxonomy Analyst"],
)
_check(
    "still-catches: a genuinely fabricated bare-digit-pair course code "
    "('15-999', NOT followed by 'postings', not grounded anywhere) "
    "still flags — the postings-context exemption is structurally "
    "narrow, not a blanket bare-digit-pair exemption",
    any("15" in f and "999" in f for f in _s5_flags_bad_code),
    f"got: {_s5_flags_bad_code}",
)

_s5_flags_real_bare_code_unaffected = _detect_content_attribution_flags(
    "This program's core sequence includes MIT's 10-601 (Machine Learning).",
    "What courses does this program require?",
    _steps(("University AI Programs Researcher", "10-601 Machine Learning is a required course.")),
    ["University AI Programs Researcher"],
)
_check(
    "a real, grounded bare-digit-pair course code ('10-601', verbatim in "
    "the trace) is still correctly exempted via the pre-existing "
    "verbatim-trace check, unaffected by the new postings-context check",
    _s5_flags_real_bare_code_unaffected == [],
    f"unexpected flags: {_s5_flags_real_bare_code_unaffected}",
)


# =====================================================================
# CLOSELOOP B1 (2026-09-19): table-row attribution — 4th shape the
# prose-citation attribution guard didn't cover
# =====================================================================
print("\n=== CLOSELOOP B1: table-row attribution fabrication ===")

_realincident_table = (
    "| Specialist | Evidence Provided | How It Informs the Recommendation |\n"
    "|------------|-------------------|-----------------------------------|\n"
    "| **University AI Programs Researcher** | Structured course lists from "
    "five peer programs (Stanford, CMU, MIT, University of Washington, "
    "University of Toronto). For example, UW's \"Artificial Intelligence "
    "Foundations\" course. | Demonstrates benchmark alignment. |\n"
)
_b1_flags_real = _detect_fabrication_flags(_realincident_table, ["Skills Taxonomy Analyst"])
_check(
    "still-catches: the real incident (run_20260917T224109Z) — a table row "
    "crediting a non-delegated 'University AI Programs Researcher' with "
    "specific peer-program content — is flagged",
    len(_b1_flags_real) == 1
    and "University AI Programs Researcher" in _b1_flags_real[0]
    and "table row" in _b1_flags_real[0],
    f"got: {_b1_flags_real}",
)

_honest_table_emoji = (
    "| Cluster Interpreter | ❌ Not consulted | No gap analysis was "
    "requested at this stage. |\n"
)
_b1_flags_honest = _detect_fabrication_flags(_honest_table_emoji, ["Skills Taxonomy Analyst"])
_check(
    "no-longer-a-gap / correctly clean: an honest '❌ Not consulted' table "
    "row (curriculum-fetch-mmai's own real pattern) is NOT flagged",
    _b1_flags_honest == [],
    f"unexpected flags: {_b1_flags_honest}",
)

_honest_table_words = (
    "| AI Industry News Researcher | Not delegated this run — no recent "
    "articles retrieved. | N/A |\n"
)
_b1_flags_honest2 = _detect_fabrication_flags(_honest_table_words, ["Skills Taxonomy Analyst"])
_check(
    "a differently-worded honest disclosure row ('Not delegated this "
    "run...') is also NOT flagged — the negation-cue list isn't limited "
    "to the emoji spelling",
    _b1_flags_honest2 == [],
    f"unexpected flags: {_b1_flags_honest2}",
)

_b1_flags_delegated = _detect_fabrication_flags(
    _realincident_table, ["University AI Programs Researcher"]
)
_check(
    "the identical table row is NOT flagged when the role genuinely IS in "
    "delegated_to this run",
    _b1_flags_delegated == [],
    f"unexpected flags: {_b1_flags_delegated}",
)

_different_role_table = (
    "| **AI Industry News Researcher** | Recent articles on agentic AI "
    "adoption from three major outlets. | Confirms industry momentum. |\n"
)
_b1_flags_other = _detect_fabrication_flags(_different_role_table, ["Skills Taxonomy Analyst"])
_check(
    "still-catches: a fabricated table row for a DIFFERENT non-delegated "
    "role (News Researcher, not University Programs) is also flagged — "
    "not hardcoded to the one incident's specific role",
    len(_b1_flags_other) == 1 and "AI Industry News Researcher" in _b1_flags_other[0],
    f"got: {_b1_flags_other}",
)


# =====================================================================
# CLOSELOOP B1: STRICT_DELEGATION raises for a curriculum query missing
# the required specialists (Step 2 — enforce delegation for this run)
# =====================================================================
print("\n=== CLOSELOOP B1: STRICT_DELEGATION on a curriculum/cluster query ===")

_g2_query = (
    "Recommend an 8-10 course graduate AI/ML curriculum grounded in the "
    "most recent wave of demand. Consult the Cluster Interpreter for "
    "cluster labels and the University AI Programs Researcher for "
    "peer-program context."
)
_g2_required = _detect_required_specialists(_g2_query)
_check(
    "the G.2-style query is detected as requiring BOTH University AI "
    "Programs Researcher and Cluster Interpreter",
    _g2_required == {"University AI Programs Researcher", "Cluster Interpreter"},
    f"got: {_g2_required}",
)

_prev_strict = os.environ.get("STRICT_DELEGATION")
os.environ["STRICT_DELEGATION"] = "true"
try:
    _check(
        "_strict_delegation_enabled() reads the env var correctly",
        _strict_delegation_enabled() is True,
    )
    _g2_path = _write_run_record(
        _g2_query,
        _steps(("Skills Taxonomy Analyst", "some real analyst output")),
        wall_time_sec=1.0, answer="a curriculum answer missing the required specialists",
        error=None, usage_metrics=None,
    )
    _delegated = sorted({"Skills Taxonomy Analyst"})
    _missing = sorted(_detect_required_specialists(_g2_query) - set(_delegated))
    _raised = False
    try:
        if _missing and _strict_delegation_enabled():
            raise RequiredSpecialistMissingError(
                f"STRICT_DELEGATION is on and this query's detected intent "
                f"required {_missing}, which was/were never delegated."
            )
    except RequiredSpecialistMissingError:
        _raised = True
    _check(
        "STRICT_DELEGATION raises RequiredSpecialistMissingError when a "
        "G.2-style query's required specialists (Cluster Interpreter + "
        "University Programs) were never delegated — mirrors run_query()'s "
        "own STRICT_DELEGATION block (agents/orchestrator.py, ~line 1812)",
        _raised,
    )
finally:
    if os.path.exists(_g2_path):
        os.remove(_g2_path)
    full_path = _g2_path[:-len(".md")] + "_full.md"
    if os.path.exists(full_path):
        os.remove(full_path)
    if _prev_strict is None:
        os.environ.pop("STRICT_DELEGATION", None)
    else:
        os.environ["STRICT_DELEGATION"] = _prev_strict


# =====================================================================
# CLOSELOOP B1 attempt C (2026-09-24): narrowed _PEER_PROGRAM_INTENT_RE —
# a from-scratch curriculum design no longer requires University AI
# Programs Researcher; benchmarking an EXISTING program still does.
# =====================================================================
print("\n=== CLOSELOOP B1 attempt C: from-scratch vs. existing-program intent ===")

_natural_g2_query = (
    "Design a graduate AI/ML curriculum of about 8-10 courses, grounded "
    "in the most recent wave of labour-market demand. For each course, "
    "give a title, the demand skills or clusters it covers, and a "
    "brief rationale."
)
_natural_g2_required = _detect_required_specialists(_natural_g2_query)
_check(
    "the NATURAL G.2 query (no hand-holding, the paper-provenance text) "
    "requires Cluster Interpreter but NOT University AI Programs "
    "Researcher — a from-scratch curriculum is a demand-grounding task, "
    "not a program-comparison task. UPDATED 2026-09-24 (CLOSELOOP "
    "workstream b): this query ALSO now requires Skills Taxonomy "
    "Analyst — the from-scratch curriculum-design intent requires BOTH "
    "Cluster Interpreter (structure) and the Analyst (lift/z evidence), "
    "see _CURRICULUM_DESIGN_INTENT_RE. Was `== {'Cluster Interpreter'}` "
    "only, before workstream b added the Analyst requirement.",
    _natural_g2_required == {"Cluster Interpreter", "Skills Taxonomy Analyst"},
    f"got: {_natural_g2_required}",
)

# still-required: every case that names/compares an EXISTING program
# must keep requiring University AI Programs Researcher.
_check(
    "still-required: 'improve MY curriculum' (broad-improve-curriculum's "
    "real query, references an EXISTING program via 'my') still requires "
    "University AI Programs Researcher",
    "University AI Programs Researcher" in _detect_required_specialists(
        "I want to improve my AI/ML Master's curriculum. What should I focus on?"
    ),
)
_check(
    "still-required: 'peer institutions cover MLOps' (mlops-coverage-"
    "benchmark's real query — 'institution', not 'program') still "
    "requires University AI Programs Researcher via the widened "
    "peer[ -]?(?:program|institution) alternative",
    "University AI Programs Researcher" in _detect_required_specialists(
        "I'm considering adding a dedicated MLOps module to my AI/ML "
        "Master's. How strong is the market demand, how do peer "
        "institutions cover MLOps today, and what recent industry "
        "developments should shape the module's content?"
    ),
)
_check(
    "still-required: the real Rotman gap-analysis query (names a "
    "specific existing program, MMA — not the MMAI degree token) still "
    "requires University AI Programs Researcher via the bare "
    "'program' trigger",
    "University AI Programs Researcher" in _detect_required_specialists(
        "Analyse the University of Toronto Rotman Master of Management "
        "Analytics (MMA) program curriculum for skill gaps. First fetch "
        "the current course list, then use the CSPA ensemble clustering "
        "results to identify which skill clusters are missing or "
        "underrepresented."
    ),
)
_check(
    "still-required: MIT peer-program query ('program offer') still "
    "requires University AI Programs Researcher",
    "University AI Programs Researcher" in _detect_required_specialists(
        "What does MIT's AI / data science Master's program offer? "
        "Cite specific URLs for the program page."
    ),
)
_check(
    "still-required: Queen's MMAI data-eng-curriculum-update query "
    "('program compare') still requires University AI Programs Researcher",
    "University AI Programs Researcher" in _detect_required_specialists(
        "I'm updating my AI/ML Master's curriculum. What are the most "
        "in-demand data engineering skills I should make sure my program "
        "covers, and how does Queen's University's MMAI program compare "
        "on this dimension?"
    ),
)

# Re-run the full original B2 block's 9 assertions inline as a single
# regression check — the narrowing must not have touched any of them
# (verified individually above already; this is a compact re-assertion).
_check(
    "B2 regression: all 9 original required-specialist assertions still "
    "hold after the _PEER_PROGRAM_INTENT_RE narrowing",
    (
        "University AI Programs Researcher" in _detect_required_specialists("which peer programs teach data engineering?")
        and "University AI Programs Researcher" in _detect_required_specialists("What does Queen's MMAI cover?")
        and _detect_required_specialists("Can you tell me about the best restaurants near the University of Toronto?") == set()
        and "University AI Programs Researcher" in _detect_required_specialists(
            "Tell me about Johns Hopkins' MPH program in biostatistics and how it compares to AI/ML programs."
        )
        and _detect_required_specialists("Have you heard of Stanford University?") == set()
        and "Cluster Interpreter" in _detect_required_specialists("Which skill clusters are missing from our curriculum?")
        and _detect_required_specialists(
            "Which of the 6 peer programs cover these clusters, and which clusters are missing?"
        ) >= {"University AI Programs Researcher", "Cluster Interpreter"}
        and _detect_required_specialists("What's the best pizza place downtown?") == set()
        and _detect_required_specialists("What are the top 5 in-demand technical skills for AI/ML roles?") == set()
    ),
)

# --- Step 3(a): a from-scratch answer grounded in cluster labels +
# demand frequency, with NO peer-program content, passes guard-clean ---
_clean_g2_answer = (
    "## Recommended 8-Course Curriculum\n\n"
    "| # | Course | Cluster | Demand frequency |\n"
    "|---|--------|---------|-------------------|\n"
    "| 1 | Foundations of LLMs | Cluster 4 (AI/ML Core) | 910 postings, rising |\n"
    "| 2 | Agentic Systems & Orchestration | Cluster 4 (AI/ML Core) | 190 postings, rising |\n\n"
    "### Evidence Base\n\n"
    "| Specialist | Evidence Provided |\n"
    "|------------|--------------------|\n"
    "| Cluster Interpreter | 10-cluster breakdown with per-cluster demand frequency. |\n"
    "| Skills Taxonomy Analyst | Demand frequency and rising/falling trend per skill. |\n"
)
_clean_g2_flags = (
    _detect_fabrication_flags(_clean_g2_answer, ["Cluster Interpreter", "Skills Taxonomy Analyst"])
    + _detect_numeric_fabrication_flags(
        _clean_g2_answer,
        _steps(
            ("Cluster Interpreter", "Cluster 4 (AI/ML Core): 910 postings, rising. 190 postings, rising."),
            ("Skills Taxonomy Analyst", "910 postings, rising. 190 postings, rising."),
        ),
        ["Cluster Interpreter", "Skills Taxonomy Analyst"],
    )
    + _detect_content_attribution_flags(
        _clean_g2_answer, _natural_g2_query,
        _steps(
            ("Cluster Interpreter", "Cluster 4 (AI/ML Core): 910 postings, rising. 190 postings, rising."),
            ("Skills Taxonomy Analyst", "910 postings, rising. 190 postings, rising."),
        ),
        ["Cluster Interpreter", "Skills Taxonomy Analyst"],
    )
)
_check(
    "Step 3(a): a from-scratch curriculum answer grounded in real "
    "Cluster Interpreter + Analyst frequency output, with no peer-"
    "program content, passes all three content guards clean",
    _clean_g2_flags == [],
    f"unexpected flags: {_clean_g2_flags}",
)

# --- Step 3(b): the guards still fire on peer-program content or an
# ungrounded lift value with no matching specialist/tool output ---
_fabricated_g2_answer = (
    "| University AI Programs Researcher | Stanford offers CS229 "
    "covering this material. | \n"
    "Large Language Models (lift 6.17x, z=9.56) anchors the core course.\n"
)
_fab_g2_flags = (
    _detect_fabrication_flags(_fabricated_g2_answer, ["Cluster Interpreter"])
    + _detect_numeric_fabrication_flags(
        _fabricated_g2_answer,
        _steps(("Cluster Interpreter", "Cluster 4 (AI/ML Core): 910 postings.")),
        ["Cluster Interpreter"],
    )
)
_check(
    "Step 3(b): loosening the University-Programs requirement does NOT "
    "blind the guards — a table-row peer-program claim with no matching "
    "delegated specialist still flags",
    any("University AI Programs Researcher" in f and "table row" in f for f in _fab_g2_flags),
    f"got: {_fab_g2_flags}",
)
_check(
    "Step 3(b): an ungrounded lift/z value (no real focal-skill tool "
    "call behind it) still flags even on a from-scratch-curriculum-"
    "shaped answer",
    any("6.17" in f or "9.56" in f for f in _fab_g2_flags),
    f"got: {_fab_g2_flags}",
)

# --- Step 3(c): STRICT_DELEGATION requires the RIGHT specialist for
# each intent — Cluster Interpreter for from-scratch, University
# Programs for an existing-program comparison ---
_prev_strict_c = os.environ.get("STRICT_DELEGATION")
os.environ["STRICT_DELEGATION"] = "true"
try:
    _fromscratch_missing = sorted(
        _detect_required_specialists(_natural_g2_query) - {"Skills Taxonomy Analyst"}
    )
    _check(
        "Step 3(c): STRICT_DELEGATION on the natural G.2 query requires "
        "ONLY Cluster Interpreter (not University Programs) when only "
        "the Analyst was delegated",
        _fromscratch_missing == ["Cluster Interpreter"],
        f"got: {_fromscratch_missing}",
    )

    _existing_program_query = (
        "Compare the Queen's University MMAI programme against current "
        "labour-market demand: which in-demand skills does it cover, "
        "which is it missing?"
    )
    _comparison_missing = sorted(
        _detect_required_specialists(_existing_program_query) - {"Skills Taxonomy Analyst"}
    )
    _check(
        "Step 3(c): STRICT_DELEGATION on an existing-program comparison "
        "query (G.3-style, names Queen's MMAI + 'compare') still "
        "requires University AI Programs Researcher",
        "University AI Programs Researcher" in _comparison_missing,
        f"got: {_comparison_missing}",
    )
finally:
    if _prev_strict_c is None:
        os.environ.pop("STRICT_DELEGATION", None)
    else:
        os.environ["STRICT_DELEGATION"] = _prev_strict_c


# =====================================================================
# CLOSELOOP workstream b (2026-09-24): Cluster Interpreter gets a
# from-scratch curriculum-generation role (Mode B, curriculum scaffold).
# _CURRICULUM_DESIGN_INTENT_RE now requires {Cluster Interpreter, Skills
# Taxonomy Analyst} for a genuine from-scratch design intent, and
# explicitly does NOT add University AI Programs Researcher. Tests here
# use Eric's exact STEP 5 natural-query wording from this workstream's
# prompt (distinct phrasing from attempt C's older natural_g2_query
# above — both now correctly resolve the same way).
# =====================================================================
print("\n=== CLOSELOOP workstream b: from-scratch generation role ===")

_g2b_query = (
    "Design a graduate AI/ML curriculum of about 8-10 courses grounded "
    "in the most recent wave of labour-market demand. Use the demand "
    "skill clusters as the backbone, and for each course give a title, "
    "the cluster(s) and key skills it covers, and a brief rationale "
    "grounded in how distinctively those skills are demanded."
)
_g2b_required = _detect_required_specialists(_g2b_query)
_check(
    "Step 4(c): the workstream-b natural G.2 query requires EXACTLY "
    "{Cluster Interpreter, Skills Taxonomy Analyst} and NOT University "
    "AI Programs Researcher",
    _g2b_required == {"Cluster Interpreter", "Skills Taxonomy Analyst"},
    f"got: {_g2b_required}",
)

# Regression: the existing update-mixed / gap-analysis battery cases
# must NOT pick up a spurious Skills Taxonomy Analyst requirement from
# the new _CURRICULUM_DESIGN_INTENT_RE branch — verified by checking
# that branch is correctly gated off (peer-intent already fires on all
# of these, or no design verb is present near "curriculum" at all).
_check(
    "regression: 'improve my curriculum' (broad-improve-curriculum) "
    "does not gain a spurious from-scratch requirement — 'improve' is "
    "not a design/build/create/develop/propose/recommend verb",
    _detect_required_specialists(
        "I want to improve my AI/ML Master's curriculum. What should I focus on?"
    ) == {"University AI Programs Researcher"},
)
_check(
    "regression: sector-wrap-finance-curriculum's real query ('Design a "
    "... curriculum' + bare 'program') is gated off by the peer-intent "
    "negative guard, not double-counted",
    _detect_required_specialists(
        "Design a finance-focused AI/ML Master's curriculum grounded in "
        "the market data. Cover both the core agentic-AI skills every "
        "such program needs and the finance-specific skills this sector "
        "distinctively demands. Report lift and statistical "
        "significance (z) for the skills you cite, and give concrete "
        "course recommendations."
    ) == {"University AI Programs Researcher"},
)
_check(
    "regression: the Rotman gap-analysis query ('Analyse ... program "
    "curriculum for skill gaps') has no design/build/create/develop/"
    "propose/recommend verb near 'curriculum' — no spurious Analyst "
    "requirement added, University Programs + Cluster Interpreter "
    "(gap-analysis intent) unchanged",
    _detect_required_specialists(
        "Analyse the University of Toronto Rotman Master of Management "
        "Analytics (MMA) program curriculum for skill gaps. First fetch "
        "the current course list, then use the CSPA ensemble clustering "
        "results to identify which skill clusters are missing or "
        "underrepresented."
    ) == {"University AI Programs Researcher", "Cluster Interpreter"},
)

# 2026-09-24 finding, out of scope for this workstream, flagged not
# fixed: curriculum-fetch-mmai's real query contains the literal phrase
# "Do not perform gap analysis" — _CLUSTER_GAP_INTENT_RE has no
# negation-awareness (unlike _TABLE_ATTRIBUTION_NEGATION_CUES elsewhere
# in this file), so "gap analysis" inside a NEGATED sentence still
# spuriously requires Cluster Interpreter. Pre-existing (unrelated to
# _CURRICULUM_DESIGN_INTENT_RE, confirmed unaffected by this
# workstream's diff), reported to Eric rather than silently fixed here —
# see the workstream-b report. Documented as a known/expected result,
# not asserted as correct behavior.
_check(
    "KNOWN PRE-EXISTING ISSUE (not fixed this workstream): "
    "curriculum-fetch-mmai's 'Do not perform gap analysis' spuriously "
    "requires Cluster Interpreter due to no negation-awareness in "
    "_CLUSTER_GAP_INTENT_RE — documenting current (wrong) behavior so a "
    "future fix's diff is visible here, not asserting it's correct",
    "Cluster Interpreter" in _detect_required_specialists(
        "Fetch and structure the publicly available curriculum for "
        "Queen's University MMAI program. Return a clean course list "
        "with source URLs and the broad topic areas covered. Do not "
        "perform gap analysis."
    ),
)

# --- Step 4(a): a Mode-B-shaped Cluster Scaffold answer, grounded in
# real Cluster Interpreter + Analyst output, with NO peer-program
# content anywhere, passes all three content guards clean. ---
_scaffold_answer = (
    "## Cluster Scaffold — Graduate AI/ML Curriculum\n\n"
    "**Cluster 1 — Machine Learning & Generative AI** (174 skills)\n"
    "Top demand skills: Machine Learning (freq=5952), Generative Ai (freq=1975), "
    "Mlops (freq=885). Anchors Course 1: Foundations of ML & GenAI.\n\n"
    "**Cluster 3 — Data Engineering & Data Platforms** (159 skills)\n"
    "Top demand skills: Python (freq=7198), Sql (freq=6725), Cloud Computing (freq=6155). "
    "Anchors Course 2: Data Engineering & Cloud Platforms.\n\n"
    "### Evidence Base\n\n"
    "| Specialist | Evidence Provided |\n"
    "|------------|--------------------|\n"
    "| Cluster Interpreter | Cluster Scaffold — 4 focused clusters, top demand skills by frequency. |\n"
    "| Skills Taxonomy Analyst | Lift/z on the scaffold's key skills. |\n"
    "| University AI Programs Researcher | Not consulted this run — from-scratch design, no existing program to benchmark. |\n"
)
_scaffold_grounding_steps = _steps(
    (
        "Cluster Interpreter",
        "Cluster 1 - Machine Learning & Generative AI (174 skills): "
        "Machine Learning (freq=5952), Generative Ai (freq=1975), Mlops (freq=885). "
        "Cluster 3 - Data Engineering & Data Platforms (159 skills): "
        "Python (freq=7198), Sql (freq=6725), Cloud Computing (freq=6155).",
    ),
    ("Skills Taxonomy Analyst", "Machine Learning demand grounding, no lift/z figures cited this excerpt."),
)
_scaffold_flags = (
    _detect_fabrication_flags(_scaffold_answer, ["Cluster Interpreter", "Skills Taxonomy Analyst"])
    + _detect_numeric_fabrication_flags(
        _scaffold_answer, _scaffold_grounding_steps, ["Cluster Interpreter", "Skills Taxonomy Analyst"]
    )
    + _detect_content_attribution_flags(
        _scaffold_answer, _g2b_query, _scaffold_grounding_steps,
        ["Cluster Interpreter", "Skills Taxonomy Analyst"],
    )
    + _detect_delegation_claim_flags(_scaffold_answer, ["Cluster Interpreter", "Skills Taxonomy Analyst"])
)
_check(
    "Step 4(a): a Mode-B Cluster Scaffold answer (real cluster themes + "
    "frequencies, honest '❌ Not consulted' row for University Programs, "
    "no peer-program content) passes all four content guards clean",
    _scaffold_flags == [],
    f"unexpected flags: {_scaffold_flags}",
)

# --- Step 4(b): guards STILL catch a fabricated lift/z value AND
# fabricated peer-program content on a Mode-B-shaped answer where
# neither Cluster Interpreter nor University Programs Researcher was
# actually delegated to. ---
_fab_scaffold_answer = (
    "**Cluster 1 — Machine Learning & Generative AI**\n"
    "Top skills: Large Language Models (lift 6.17x, z=9.56).\n\n"
    "| University AI Programs Researcher | Stanford's CS229 and MIT's "
    "6.7960 both cover this cluster's core material. |\n"
)
_fab_scaffold_flags = (
    _detect_fabrication_flags(_fab_scaffold_answer, [])
    + _detect_numeric_fabrication_flags(_fab_scaffold_answer, [], [])
)
_check(
    "Step 4(b): a fabricated peer-program table row STILL flags on a "
    "Mode-B-shaped answer even though University Programs was never "
    "required by _detect_required_specialists for this query shape — "
    "the content guards are independent of the required-specialist "
    "backstop and don't get weaker just because a specialist is now "
    "optional rather than required",
    any("University AI Programs Researcher" in f and "table row" in f for f in _fab_scaffold_flags),
    f"got: {_fab_scaffold_flags}",
)
_check(
    "Step 4(b): an ungrounded lift/z value on a Mode-B-shaped answer "
    "still flags (no Cluster Interpreter/Analyst tool output behind it "
    "at all in this fixture)",
    any("6.17" in f or "9.56" in f for f in _fab_scaffold_flags),
    f"got: {_fab_scaffold_flags}",
)


# =====================================================================
# §5.1 F2022 PUSHTHROUGH (2026-09-25), Part A2/A3: real gaps found on a
# live F2022 dev-lane run (run_20260925T164511Z) — gpt-oss:120b formatted
# its own grounding text with U+202F narrow no-break spaces as thousands
# separators (corrupting extraction of real, correctly-cited numbers), and
# a genuine fabrication used "frequency ≈ N" (not "=") which the old guard
# never even extracted, let alone checked.
# =====================================================================
print("\n=== §5.1 F2022 PUSHTHROUGH A2/A3: Unicode-space + approx-separator fixes ===")

# A2 — extraction from grounded text with U+202F thousands separators now
# recovers the REAL value, not a truncated one.
_a2_grounded_text = "TensorFlow (freq = 2 387), Deep Learning (freq = 2 373)"
_a2_extracted = _extract_market_numbers(_a2_grounded_text)
_check(
    "A2: U+202F-formatted 'freq\\u202f=\\u202f2\\u202f387' extracts as "
    "2387.0, not truncated to 2.0",
    any(val == 2387.0 for _raw, val, kind, _s, _e in _a2_extracted),
    f"got: {_a2_extracted}",
)
_check(
    "A2: a SECOND U+202F-formatted number in the same text ('2\\u202f373') "
    "also extracts correctly — not just the first occurrence",
    any(val == 2373.0 for _raw, val, kind, _s, _e in _a2_extracted),
    f"got: {_a2_extracted}",
)
_check(
    "A2: _normalize_market_num handles U+00A0 (no-break space) and "
    "U+2009 (thin space) thousands separators too, not just U+202F",
    _normalize_market_num("15 171") == 15171.0
    and _normalize_market_num("2 769") == 2769.0,
)
_check(
    "A2: ordinary-comma formatting (the common case) is completely "
    "unaffected by the widened character class",
    _normalize_market_num("1,435") == 1435.0 and _normalize_market_num("56k") == 56000.0,
)

# A2 end-to-end: the exact real F2022 run scenario — a correctly-cited,
# genuinely-grounded number in the Advisor's answer no longer flags once
# the grounding-side extraction can actually see the real value.
_a2_answer = "TensorFlow (2,387 postings) anchors this course."
_a2_flags = _detect_numeric_fabrication_flags(
    _a2_answer, _steps(("Skills Taxonomy Analyst", _a2_grounded_text)), ["Skills Taxonomy Analyst"]
)
_check(
    "A2 end-to-end: 'TensorFlow (2,387 postings)' no longer flags once "
    "the grounded text's own U+202F-formatted '2\\u202f387' is correctly "
    "parsed as 2387 (was a real false positive on run_20260925T164511Z)",
    _a2_flags == [],
    f"got: {_a2_flags}",
)

# A3 — "frequency ≈ N" is now extracted and checked (previously invisible
# to the guard entirely).
_a3_extracted = _extract_market_numbers("Distributed Data Processing (frequency ≈ 800)")
_check(
    "A3: 'frequency ≈ 800' (approx symbol, not '=') is now extracted "
    "as a frequency claim",
    any(val == 800.0 for _raw, val, kind, _s, _e in _a3_extracted),
    f"got: {_a3_extracted}",
)
_a3_tilde = _extract_market_numbers("Some Skill (freq ~ 250)")
_check(
    "A3: 'freq ~ 250' (tilde) is also recognised",
    any(val == 250.0 for _raw, val, kind, _s, _e in _a3_tilde),
    f"got: {_a3_tilde}",
)

# A3 end-to-end: THE exact real fabrication from run_20260925T164511Z —
# invented content with NO backing in either specialist's actual output —
# must now be flagged, not silently pass.
_a3_fab_answer = (
    "| **4** | **Data Engineering & Cloud Platforms** | Server Systems "
    "(frequency = 46), Distributed Data Processing (frequency ≈ 800) |"
)
_a3_grounding = _steps(
    ("Cluster Interpreter", "Server Systems (freq=46), technical Problem Solving (freq=34)."),
)
_a3_flags = _detect_numeric_fabrication_flags(_a3_fab_answer, _a3_grounding, ["Cluster Interpreter"])
_check(
    "A3 end-to-end: the exact real fabrication ('Distributed Data "
    "Processing (frequency ≈ 800)', invented, absent from every "
    "specialist's real output) is now FLAGGED — was silently missed "
    "entirely on run_20260925T164511Z",
    any("800" in f for f in _a3_flags),
    f"got: {_a3_flags}",
)
_check(
    "A3 still-catches: the genuinely-grounded 'Server Systems "
    "(frequency = 46)' in the SAME answer does NOT also flag — only the "
    "fabricated skill does",
    not any("'46'" in f for f in _a3_flags),
    f"got: {_a3_flags}",
)
_check(
    "A3 still-catches: an ordinary '=' -formatted fabrication (no approx "
    "symbol involved at all) still flags exactly as before — the widened "
    "separator class didn't loosen the baseline check. (Non-empty "
    "step_log required — _detect_numeric_fabrication_flags short-circuits "
    "to [] on an empty step_log by design, a pre-existing behaviour "
    "unrelated to A2/A3, not something to trip over here.)",
    any(
        "99999" in f
        for f in _detect_numeric_fabrication_flags(
            "Fake Skill (frequency = 99999)",
            _steps(("Skills Taxonomy Analyst", "Real Skill (frequency = 12345)")),
            ["Skills Taxonomy Analyst"],
        )
    ),
)


# =====================================================================
# §5.1 F2022 PUSHTHROUGH, Part A1: per-run data-wave override notice.
# Still-catches: the W2026 gap-analysis path (no override active) is
# completely unaffected — data_wave_override_notice() returns None and
# run_query() prepends nothing, byte-identical to pre-A1 behaviour.
# =====================================================================
print("\n=== §5.1 F2022 PUSHTHROUGH A1: data-wave override notice ===")

import importlib as _importlib
import tools.cluster_tool as _cluster_tool_mod

_check(
    "A1: with no CLUSTER_RESULTS_FILE_OVERRIDE set (the default, W2026 "
    "production state), data_wave_override_notice() returns None",
    _cluster_tool_mod.data_wave_override_notice() is None,
)

_prev_override = os.environ.get("CLUSTER_RESULTS_FILE_OVERRIDE")
_prev_wave_label = os.environ.get("DATA_WAVE_LABEL")
try:
    os.environ["CLUSTER_RESULTS_FILE_OVERRIDE"] = "/tmp/fake_f2022_clusters.csv"
    os.environ["DATA_WAVE_LABEL"] = "Fall 2022 (F2022)"
    _importlib.reload(_cluster_tool_mod)
    _notice = _cluster_tool_mod.data_wave_override_notice()
    _check(
        "A1: with the override active, data_wave_override_notice() "
        "returns a non-empty marker block",
        bool(_notice) and "DATA WAVE OVERRIDE NOTICE" in _notice,
        f"got: {_notice!r}",
    )
    _check(
        "A1: the notice names the active wave label (generic/"
        "parameterized, not hardcoded 'F2022' in the code)",
        "Fall 2022 (F2022)" in (_notice or ""),
    )
    _check(
        "A1: the notice tells the reader to trust the live tool output "
        "over their own backstory",
        "SOLE source of truth" in (_notice or ""),
    )
finally:
    if _prev_override is None:
        os.environ.pop("CLUSTER_RESULTS_FILE_OVERRIDE", None)
    else:
        os.environ["CLUSTER_RESULTS_FILE_OVERRIDE"] = _prev_override
    if _prev_wave_label is None:
        os.environ.pop("DATA_WAVE_LABEL", None)
    else:
        os.environ["DATA_WAVE_LABEL"] = _prev_wave_label
    _importlib.reload(_cluster_tool_mod)
    _check(
        "A1 still-catches (G.3-style path unaffected): after restoring "
        "the environment to its default (no override), "
        "data_wave_override_notice() is None again — the W2026 "
        "gap-analysis path never sees an injected notice",
        _cluster_tool_mod.data_wave_override_notice() is None,
    )


# =====================================================================
# §5.1 F2022 PUSHTHROUGH, Part B: vetted F2022 label override
# (CLUSTER_THEMES_OVERRIDE_JSON) takes priority over the numeric-only
# fallback, and FOCUSED_CLUSTERS_OVERRIDE = {1,2,4,5} per Cowork's review.
# =====================================================================
print("\n=== §5.1 F2022 PUSHTHROUGH Part B: vetted label override ===")

_prev_themes_json = os.environ.get("CLUSTER_THEMES_OVERRIDE_JSON")
_prev_focused = os.environ.get("FOCUSED_CLUSTERS_OVERRIDE")
try:
    os.environ["CLUSTER_RESULTS_FILE_OVERRIDE"] = "/tmp/fake_f2022_clusters.csv"
    os.environ["CLUSTER_THEMES_OVERRIDE_JSON"] = (
        '{"1": "Machine Learning & Deep Learning", '
        '"2": "Data Science, Statistics & Classical ML", '
        '"4": "Data Engineering & Cloud Data Platforms"}'
    )
    os.environ["FOCUSED_CLUSTERS_OVERRIDE"] = "1,2,4,5"
    _importlib.reload(_cluster_tool_mod)
    _check(
        "Part B: cluster 1's theme is the vetted override label, not the "
        "numeric-only placeholder",
        _cluster_tool_mod._theme_for(1) == "Machine Learning & Deep Learning",
        f"got: {_cluster_tool_mod._theme_for(1)!r}",
    )
    _check(
        "Part B: cluster 4's theme is the vetted override label",
        _cluster_tool_mod._theme_for(4) == "Data Engineering & Cloud Data Platforms",
        f"got: {_cluster_tool_mod._theme_for(4)!r}",
    )
    _check(
        "Part B: a cluster id NOT covered by the override JSON (e.g. "
        "cluster 3) falls back to the numeric-only placeholder, not a "
        "crash or a stale W2026 label",
        "numeric only" in _cluster_tool_mod._theme_for(3),
        f"got: {_cluster_tool_mod._theme_for(3)!r}",
    )
    _check(
        "Part B: FOCUSED_CLUSTERS_OVERRIDE = '1,2,4,5' parses to exactly "
        "{1, 2, 4, 5} — cluster 9 (the AI's earlier provisional guess) is "
        "correctly NOT in the vetted set",
        _cluster_tool_mod.FOCUSED_CLUSTERS == {1, 2, 4, 5},
        f"got: {sorted(_cluster_tool_mod.FOCUSED_CLUSTERS)}",
    )
finally:
    for _var in ("CLUSTER_RESULTS_FILE_OVERRIDE", "CLUSTER_THEMES_OVERRIDE_JSON", "FOCUSED_CLUSTERS_OVERRIDE"):
        os.environ.pop(_var, None)
    if _prev_themes_json is not None:
        os.environ["CLUSTER_THEMES_OVERRIDE_JSON"] = _prev_themes_json
    if _prev_focused is not None:
        os.environ["FOCUSED_CLUSTERS_OVERRIDE"] = _prev_focused
    _importlib.reload(_cluster_tool_mod)
    _check(
        "Part B still-catches (W2026 default unaffected): after "
        "restoring the environment, cluster 1's theme is back to the "
        "W2026 production label",
        _cluster_tool_mod._theme_for(1) == "Machine Learning & Generative AI",
        f"got: {_cluster_tool_mod._theme_for(1)!r}",
    )
    _check(
        "Part B still-catches: FOCUSED_CLUSTERS is back to the W2026 "
        "production set {1, 2, 3, 7}",
        _cluster_tool_mod.FOCUSED_CLUSTERS == {1, 2, 3, 7},
        f"got: {sorted(_cluster_tool_mod.FOCUSED_CLUSTERS)}",
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
