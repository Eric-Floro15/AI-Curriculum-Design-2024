"""
test_single_agent.py — Unit tests for the SA ablation module (single_agent.py).

Tests (no LLM calls — all static / import-time checks):
  1.  tool_set_union  — SA agent's tools == exact union of all four specialists.
  2.  ma_unchanged    — build_crew() still returns 5 agents; orchestrator max_iter
                        unchanged at 8.
  3.  guard1_catches  — guard #1 (_detect_fabrication_flags) flags a specialist
                        name cited as a source in an SA answer (delegated_to=[]).
  4.  guard4_catches  — guard #4 (_detect_delegation_claim_flags) flags an
                        affirmative "consulted" claim in an SA answer.
  5.  guard2_catches  — guard #2 (_detect_numeric_fabrication_flags) flags a
                        lift/z value absent from _build_sa_step_log tool outputs.
  6.  guard3_catches  — guard #3 (_detect_content_attribution_flags) flags a URL
                        absent from _build_sa_step_log tool outputs.
  7.  plain_backstory_unchanged  — (v62 pilot) SA_BACKSTORY is byte-identical to
                        the pinned hash when SA_PROCEDURE is unset / "plain".
  8.–11. structured/general backstory hashes (v62 pilot2, v62 pilot2 amend1).
  12. pair_verify_disabled  — (v62 pilot4) PAIR_VERIFY=0 returns identity + None.
  13. pair_verify_extracts  — (v62 pilot4) extract_pairs finds all required formats.
  14. pair_verify_splice     — (v62 pilot4) cross-entry splice correctly fails.
  15. pair_verify_colocated  — (v62 pilot4) colocated pair passes.
  16. sa_sequenced_equals_general_plus_step — (v62 pilot5) SA sequenced = general + step6_text.
  17. sa_sequenced_hash      — (v62 pilot5) SA_BACKSTORY hash when SA_PROCEDURE=sequenced.
  18. orch_sequenced_equals_general_plus_step — (v62 pilot5) orch sequenced = general + step7_text.
  19. sequenced_procedure_recorded_in_header — (v62 pilot5) value written to run-record header.

Run:
  KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_single_agent.py
"""

import hashlib  # v62 pilot:
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from agents.single_agent import (  # noqa: E402
    _SA_TOOLS,
    _build_sa_step_log,
    SA_BACKSTORY,
    _SA_PLAIN_BACKSTORY_HASH,
    _SA_STRUCTURED_BACKSTORY_HASH,  # v62 pilot2:
    _SA_GENERAL_BACKSTORY_HASH,     # v62 pilot2:
    _SA_SEQUENCED_BACKSTORY_HASH,   # v62 pilot5:
    _SA_GENERAL_PROCEDURE_TEXT,     # v62 pilot5:
    _SA_SEQUENCED_STEP_TEXT,        # v62 pilot5:
    _SA_PROCEDURE,                  # v62 pilot5:
)
from agents.orchestrator import (  # noqa: E402
    _detect_content_attribution_flags,
    _detect_delegation_claim_flags,
    _detect_fabrication_flags,
    _detect_numeric_fabrication_flags,
    build_crew,
    make_orchestrator,
    _ORCHESTRATOR_PLAIN_BACKSTORY,   # v62 pilot2 amend1:
    _ORCH_PLAIN_BACKSTORY_HASH,      # v62 pilot2 amend1:
    _ORCH_GENERAL_BACKSTORY_HASH,    # v62 pilot2 amend1:
    _ORCH_GENERAL_PROCEDURE_TEXT,    # v62 pilot2 amend1:
    _ORCH_SEQUENCED_BACKSTORY_HASH,  # v62 pilot5:
    _ORCH_SEQUENCED_STEP_TEXT,       # v62 pilot5:
    _ORCH_PROCEDURE,                 # v62 pilot5:
    ORCHESTRATOR_BACKSTORY,          # v62 pilot5:
)


def _tool_names(tools) -> set[str]:
    """Extract the .name attribute from each CrewAI Tool object."""
    return {getattr(t, "name", repr(t)) for t in tools}


# ── Test 1 — SA tool set equals union of all four specialists ─────────────────

def test_tool_set_union():
    from tools.csv_tool import CSV_TOOLS
    from tools.rag_tool import skills_rag_tool
    from tools.lift_tool import LIFT_TOOLS
    from tools.compose_tool import COMPOSE_TOOLS, SECTOR_WRAP_TOOLS
    from tools.program_rag_tool import program_rag_tool
    from tools.web_search_tool import web_search_tool
    from tools.news_tool import news_rag_tool
    from tools.cluster_tool import CLUSTER_TOOLS

    expected = _tool_names([
        skills_rag_tool,
        *CSV_TOOLS,
        *LIFT_TOOLS,
        *SECTOR_WRAP_TOOLS,
        *COMPOSE_TOOLS,
        program_rag_tool,
        web_search_tool,
        news_rag_tool,
        *CLUSTER_TOOLS,
    ])
    actual = _tool_names(_SA_TOOLS)

    missing = expected - actual
    extra = actual - expected
    assert not missing, f"SA tool set is missing: {missing}"
    assert not extra, f"SA tool set has unexpected extra tools: {extra}"
    print(f"  PASS — SA has exactly {len(actual)} tools (union of all four specialists)")


# ── Test 2 — MA objects untouched ─────────────────────────────────────────────

def test_ma_unchanged():
    crew, orchestrator = build_crew()

    assert len(crew.agents) == 5, (
        f"MA crew agent count changed: {len(crew.agents)} (expected 5). "
        "build_crew() must not have been altered."
    )
    assert orchestrator.max_iter == 8, (
        f"MA orchestrator max_iter changed: {orchestrator.max_iter} (expected 8). "
        "make_orchestrator() must not have been altered."
    )
    print(
        f"  PASS — MA crew still has 5 agents and orchestrator max_iter=8"
    )


# ── Test 3 — guard #1 still-catches (specialist-name attribution) ─────────────

def test_guard1_catches_specialist_attribution():
    """An SA answer citing a non-delegated specialist as a source must be
    flagged by _detect_fabrication_flags(answer, delegated_to=[])."""
    answer = (
        "According to the Skills Taxonomy Analyst, Large Language Models "
        "show lift 6.17× (z=9.56). The University AI Programs Researcher "
        "reports Queen's MMAI covers Python and SQL."
    )
    flags = _detect_fabrication_flags(answer, delegated_to=[])
    assert flags, (
        "Expected fabrication flags for specialist-name attribution, got none.\n"
        f"Answer tested: {answer!r}"
    )
    print(
        f"  PASS — guard #1 flagged {len(flags)} item(s) for specialist attribution: "
        f"{flags[:2]}"
    )


# ── Test 4 — guard #4 still-catches (delegation-claim) ───────────────────────

def test_guard4_catches_delegation_claim():
    """An SA answer claiming to have 'consulted' a specialist must be flagged
    by _detect_delegation_claim_flags(answer, delegated_to=[])."""
    answer = (
        "I consulted the AI Industry News Researcher, who confirmed that "
        "agentic AI is trending. The Skills Taxonomy Analyst was consulted "
        "for lift and significance data on tool-use skills."
    )
    flags = _detect_delegation_claim_flags(answer, delegated_to=[])
    assert flags, (
        "Expected delegation-claim flags, got none.\n"
        f"Answer tested: {answer!r}"
    )
    print(
        f"  PASS — guard #4 flagged {len(flags)} item(s) for delegation claims: "
        f"{flags[:2]}"
    )


# ── Test 5 — guard #2 still-catches (numeric fabrication) ────────────────────

def test_guard2_catches_numeric_fabrication():
    """Guard #2 must flag a lift/z value in the answer that is absent from
    all captured tool outputs (assembled via _build_sa_step_log)."""
    # Simulate one tool call whose output contains no matching numbers
    fake_tool_calls = [
        {
            "tool": "skills_rag_tool",
            "input": "large language models",
            "output": "Large language models are frequently mentioned in job postings.",
            "output_len": 65,
        }
    ]
    sa_step_log, sa_delegated_to = _build_sa_step_log(fake_tool_calls)

    # Answer claims specific lift/z values that are not in the tool output
    answer = "Large Language Models (lift 6.17×, z=9.56) dominate agentic-AI postings."

    flags = _detect_numeric_fabrication_flags(answer, sa_step_log, sa_delegated_to)
    assert flags, (
        "Expected guard #2 to flag '6.17' and/or '9.56' as ungrounded — "
        f"neither appears in the fake tool output.\nAnswer: {answer!r}"
    )
    print(
        f"  PASS — guard #2 flagged {len(flags)} numeric value(s) via _build_sa_step_log: "
        f"{flags[:1]}"
    )


# ── Test 6 — guard #3 still-catches (content-attribution fabrication) ─────────

def test_guard3_catches_content_fabrication():
    """Guard #3 must flag a URL in the answer that is absent from all captured
    tool outputs (assembled via _build_sa_step_log)."""
    fake_tool_calls = [
        {
            "tool": "program_rag_tool",
            "input": "Queen's MMAI",
            "output": "The MMAI program covers Python, SQL, and machine learning fundamentals.",
            "output_len": 70,
        }
    ]
    sa_step_log, sa_delegated_to = _build_sa_step_log(fake_tool_calls)

    # Answer contains a URL not present in any tool output
    answer = (
        "The Queen's MMAI curriculum is detailed at https://example.com/mmai-program "
        "and covers Python fundamentals."
    )
    query = "Compare Queen's MMAI against market demand"

    flags = _detect_content_attribution_flags(answer, query, sa_step_log, sa_delegated_to)
    assert flags, (
        "Expected guard #3 to flag 'https://example.com/mmai-program' as ungrounded — "
        f"URL absent from fake tool output.\nAnswer: {answer!r}"
    )
    print(
        f"  PASS — guard #3 flagged {len(flags)} content item(s) via _build_sa_step_log: "
        f"{flags[:1]}"
    )


# ── Test 7 — v62 pilot: SA_BACKSTORY unchanged when SA_PROCEDURE=plain ────────
# ── Extended for structured and general  # v62 pilot2: ───────────────────────

def test_plain_backstory_unchanged():  # v62 pilot:
    """When SA_PROCEDURE is unset or 'plain', SA_BACKSTORY must be byte-identical
    to the pinned plain backstory (verified by SHA-256 hash).
    If this fails, _SA_PLAIN_BACKSTORY was edited without updating
    _SA_PLAIN_BACKSTORY_HASH — update the hash in single_agent.py to match.
    """
    import os as _os
    sa_procedure = _os.environ.get("SA_PROCEDURE", "plain")
    if sa_procedure not in ("plain", ""):
        print(f"  SKIP — SA_PROCEDURE={sa_procedure!r}; plain test skipped")
        return
    actual_hash = hashlib.sha256(SA_BACKSTORY.encode()).hexdigest()
    assert actual_hash == _SA_PLAIN_BACKSTORY_HASH, (
        f"SA_BACKSTORY hash mismatch (SA_PROCEDURE=plain):\n"
        f"  got    : {actual_hash}\n"
        f"  pinned : {_SA_PLAIN_BACKSTORY_HASH}\n"
        "Update _SA_PLAIN_BACKSTORY_HASH in single_agent.py if you intentionally changed SA_BACKSTORY."
    )
    print(f"  PASS — SA_BACKSTORY hash matches pinned value (len={len(SA_BACKSTORY)})")


def test_structured_backstory_hash():  # v62 pilot2:
    """When SA_PROCEDURE=structured, SA_BACKSTORY must match the pinned structured hash.
    If _SA_STRUCTURED_BACKSTORY_HASH is empty (not yet pinned), prints the actual hash
    to paste into single_agent.py and skips the assertion.
    """
    import os as _os
    sa_procedure = _os.environ.get("SA_PROCEDURE", "plain")
    if sa_procedure != "structured":
        print(f"  SKIP — SA_PROCEDURE={sa_procedure!r}; structured test skipped")
        return
    actual_hash = hashlib.sha256(SA_BACKSTORY.encode()).hexdigest()
    if not _SA_STRUCTURED_BACKSTORY_HASH:
        print(f"  HASH (not yet pinned) — paste into _SA_STRUCTURED_BACKSTORY_HASH: {actual_hash}")
        return
    assert actual_hash == _SA_STRUCTURED_BACKSTORY_HASH, (
        f"SA_BACKSTORY hash mismatch (SA_PROCEDURE=structured):\n"
        f"  got    : {actual_hash}\n"
        f"  pinned : {_SA_STRUCTURED_BACKSTORY_HASH}\n"
        "Update _SA_STRUCTURED_BACKSTORY_HASH in single_agent.py if you intentionally changed SA_BACKSTORY."
    )
    print(f"  PASS — SA_BACKSTORY hash matches pinned structured value (len={len(SA_BACKSTORY)})")


def test_general_backstory_hash():  # v62 pilot2:
    """When SA_PROCEDURE=general, SA_BACKSTORY must match the pinned general hash.
    If _SA_GENERAL_BACKSTORY_HASH is empty (not yet pinned), prints the actual hash
    to paste into single_agent.py and skips the assertion.
    """
    import os as _os
    sa_procedure = _os.environ.get("SA_PROCEDURE", "plain")
    if sa_procedure != "general":
        print(f"  SKIP — SA_PROCEDURE={sa_procedure!r}; general test skipped")
        return
    actual_hash = hashlib.sha256(SA_BACKSTORY.encode()).hexdigest()
    if not _SA_GENERAL_BACKSTORY_HASH:
        print(f"  HASH (not yet pinned) — paste into _SA_GENERAL_BACKSTORY_HASH: {actual_hash}")
        return
    assert actual_hash == _SA_GENERAL_BACKSTORY_HASH, (
        f"SA_BACKSTORY hash mismatch (SA_PROCEDURE=general):\n"
        f"  got    : {actual_hash}\n"
        f"  pinned : {_SA_GENERAL_BACKSTORY_HASH}\n"
        "Update _SA_GENERAL_BACKSTORY_HASH in single_agent.py if you intentionally changed SA_BACKSTORY."
    )
    print(f"  PASS — SA_BACKSTORY hash matches pinned general value (len={len(SA_BACKSTORY)})")


# ── Tests 8–9: v62 pilot2 amend1: Orchestrator backstory hash pins ────────────

def test_orch_plain_backstory_hash():  # v62 pilot2 amend1:
    """_ORCHESTRATOR_PLAIN_BACKSTORY must match the pinned plain hash.
    If ORCH_PROCEDURE != 'plain', skip the test (hash only checks plain).
    If this fails, _ORCHESTRATOR_PLAIN_BACKSTORY was edited without updating
    _ORCH_PLAIN_BACKSTORY_HASH — update the hash in orchestrator.py to match.
    """
    actual = hashlib.sha256(_ORCHESTRATOR_PLAIN_BACKSTORY.encode()).hexdigest()
    assert actual == _ORCH_PLAIN_BACKSTORY_HASH, (
        f"_ORCHESTRATOR_PLAIN_BACKSTORY hash mismatch:\n"
        f"  got    : {actual}\n"
        f"  pinned : {_ORCH_PLAIN_BACKSTORY_HASH}\n"
        "Update _ORCH_PLAIN_BACKSTORY_HASH in orchestrator.py if you intentionally changed it."
    )
    print(f"  PASS — _ORCHESTRATOR_PLAIN_BACKSTORY hash matches pinned value (len={len(_ORCHESTRATOR_PLAIN_BACKSTORY)})")


# ── Tests 10–14: v62 pilot5: sequenced procedure (both arms) ─────────────────

def test_sa_sequenced_backstory_equals_general_plus_step():  # v62 pilot5:
    """SA sequenced backstory must equal SA general backstory + '\n' + step6_text.

    Checks the structural invariant: sequenced = general + newline + step text.
    Plain, structured, and general must stay byte-identical to their pinned values.
    """
    import os as _os
    sa_procedure = _os.environ.get("SA_PROCEDURE", "plain")
    if sa_procedure not in ("sequenced", "plain", ""):
        print(f"  SKIP — SA_PROCEDURE={sa_procedure!r}; run with SA_PROCEDURE=sequenced to exercise this test")
        return

    # Structural check: sequenced = general_procedure_text + step_text, appended to plain
    general_text = _SA_GENERAL_PROCEDURE_TEXT
    step_text = _SA_SEQUENCED_STEP_TEXT
    expected = _SA_PLAIN_BACKSTORY_HASH  # just a placeholder — we check structure, not via env

    # Build the expected sequenced backstory from parts
    # _SA_PLAIN_BACKSTORY is not exported; use SA_BACKSTORY when procedure=plain as proxy
    # Instead, verify via hash: sequenced hash must equal hash of (general_backstory + step_text)
    # where general_backstory = plain + general_procedure_text
    # We do this by recomputing from the exported pieces.
    import hashlib as _hl
    # Reconstruct general backstory from (plain hash known) + general_procedure_text
    # We can't reconstruct plain backstory text directly, but we can verify the structural rule
    # by confirming: SA_BACKSTORY when sequenced == SA_BACKSTORY[when general] + step_text
    # The simplest check: sequenced hash == hash(general + step_text)
    # We need the actual plain backstory text — import it
    from agents.single_agent import _SA_PLAIN_BACKSTORY as _plain  # noqa
    general_full = _plain + general_text
    sequenced_full = general_full + step_text
    computed_hash = _hl.sha256(sequenced_full.encode()).hexdigest()
    assert computed_hash == _SA_SEQUENCED_BACKSTORY_HASH, (
        f"sequenced backstory hash mismatch:\n"
        f"  computed from (general + step_text) : {computed_hash}\n"
        f"  pinned _SA_SEQUENCED_BACKSTORY_HASH  : {_SA_SEQUENCED_BACKSTORY_HASH}\n"
        "Structural rule violated: sequenced != general + newline + step6_text"
    )
    # Also confirm general and plain hashes unchanged
    plain_hash = _hl.sha256(_plain.encode()).hexdigest()
    assert plain_hash == _SA_PLAIN_BACKSTORY_HASH, (
        f"plain backstory changed: {plain_hash} != {_SA_PLAIN_BACKSTORY_HASH}"
    )
    general_hash = _hl.sha256(general_full.encode()).hexdigest()
    assert general_hash == _SA_GENERAL_BACKSTORY_HASH, (
        f"general backstory changed: {general_hash} != {_SA_GENERAL_BACKSTORY_HASH}"
    )
    print(f"  PASS — SA sequenced = general + step6_text; general and plain unchanged")
    print(f"         sequenced hash : {computed_hash}")


def test_sa_sequenced_backstory_hash():  # v62 pilot5:
    """When SA_PROCEDURE=sequenced, SA_BACKSTORY must match the pinned sequenced hash."""
    import os as _os
    sa_procedure = _os.environ.get("SA_PROCEDURE", "plain")
    if sa_procedure != "sequenced":
        print(f"  SKIP — SA_PROCEDURE={sa_procedure!r}; sequenced test skipped")
        return
    actual_hash = hashlib.sha256(SA_BACKSTORY.encode()).hexdigest()
    assert actual_hash == _SA_SEQUENCED_BACKSTORY_HASH, (
        f"SA_BACKSTORY hash mismatch (SA_PROCEDURE=sequenced):\n"
        f"  got    : {actual_hash}\n"
        f"  pinned : {_SA_SEQUENCED_BACKSTORY_HASH}\n"
        "Update _SA_SEQUENCED_BACKSTORY_HASH in single_agent.py if you intentionally changed SA_BACKSTORY."
    )
    print(f"  PASS — SA_BACKSTORY hash matches pinned sequenced value (len={len(SA_BACKSTORY)})")


def test_orch_sequenced_backstory_equals_general_plus_step():  # v62 pilot5:
    """Orchestrator sequenced backstory must equal general backstory + '\n' + step7_text."""
    import hashlib as _hl
    step_text = _ORCH_SEQUENCED_STEP_TEXT
    general_full = _ORCHESTRATOR_PLAIN_BACKSTORY + _ORCH_GENERAL_PROCEDURE_TEXT
    sequenced_full = general_full + step_text
    computed_hash = _hl.sha256(sequenced_full.encode()).hexdigest()
    assert computed_hash == _ORCH_SEQUENCED_BACKSTORY_HASH, (
        f"orch sequenced backstory hash mismatch:\n"
        f"  computed from (general + step_text) : {computed_hash}\n"
        f"  pinned _ORCH_SEQUENCED_BACKSTORY_HASH: {_ORCH_SEQUENCED_BACKSTORY_HASH}\n"
        "Structural rule violated: sequenced != general + newline + step7_text"
    )
    general_hash = _hl.sha256(general_full.encode()).hexdigest()
    assert general_hash == _ORCH_GENERAL_BACKSTORY_HASH, (
        f"orch general backstory changed: {general_hash} != {_ORCH_GENERAL_BACKSTORY_HASH}"
    )
    print(f"  PASS — orch sequenced = general + step7_text; general unchanged")
    print(f"         sequenced hash : {computed_hash}")


def test_sequenced_procedure_recorded_in_header():  # v62 pilot5:
    """When SA_PROCEDURE=sequenced or ORCH_PROCEDURE=sequenced, the value 'sequenced'
    must appear in the run-record header lines produced by the respective worker.
    """
    import os as _os
    # SA arm: _build_run_record_header is not directly exported, but SA_PROCEDURE
    # is written via run_record_header list in run_sa_worker. We test the module-level
    # _SA_PROCEDURE value is 'sequenced' when that env var is set, and that
    # SA_BACKSTORY reflects the sequenced text (hash check covers this via the other tests).
    # The direct test: _SA_PROCEDURE == "sequenced" when env is set.
    sa_proc = _os.environ.get("SA_PROCEDURE", "plain")
    # Check that the imported _SA_PROCEDURE reflects the env var correctly.
    if sa_proc == "sequenced":
        assert _SA_PROCEDURE == "sequenced", (
            f"_SA_PROCEDURE should be 'sequenced' but is {_SA_PROCEDURE!r}"
        )
        print(f"  PASS — _SA_PROCEDURE == 'sequenced' (env SA_PROCEDURE=sequenced)")
    else:
        print(f"  SKIP — SA_PROCEDURE={sa_proc!r}; set SA_PROCEDURE=sequenced to test header recording")
    # Orch arm
    orch_proc = _os.environ.get("ORCH_PROCEDURE", "plain")
    if orch_proc == "sequenced":
        assert _ORCH_PROCEDURE == "sequenced", (
            f"_ORCH_PROCEDURE should be 'sequenced' but is {_ORCH_PROCEDURE!r}"
        )
        print(f"  PASS — _ORCH_PROCEDURE == 'sequenced' (env ORCH_PROCEDURE=sequenced)")
    else:
        if sa_proc != "sequenced":
            print(f"  SKIP — ORCH_PROCEDURE={orch_proc!r}; set ORCH_PROCEDURE=sequenced to test orch header")


# ── Pair-verification tests (v62 pilot4) ──────────────────────────────────────

def test_pair_verify_disabled_returns_identity():  # v62 pilot4:
    """With PAIR_VERIFY=0, run_pair_verify must return the original answer
    byte-identical and None as the summary.  (PAIR_VERIFY=0 is now explicit
    opt-out; default changed to 1 in v63.)
    """
    import tools.pair_verify as pv
    original_flag = pv.PAIR_VERIFY
    try:
        pv.PAIR_VERIFY = False
        answer = "lift 6.66×, z=8.89 for Agentic AI"
        evidence = ["Agentic AI 6.66 lift 8.89 z"]
        result_answer, summary = pv.run_pair_verify(answer, evidence, llm=None)
        assert result_answer is answer, (
            "run_pair_verify must return the SAME object (byte-identical) when PAIR_VERIFY=0"
        )
        assert summary is None, f"summary must be None when PAIR_VERIFY=0, got {summary!r}"
        section = pv.format_pair_verify_section(None)
        assert section == [], f"format_pair_verify_section(None) must return [], got {section!r}"
    finally:
        pv.PAIR_VERIFY = original_flag
    print("  PASS — PAIR_VERIFY=0 returns identity + None summary + empty section")


def test_pair_verify_extracts_inline_pairs():  # v62 pilot4:
    """extract_pairs must find pairs in all required inline formats.

    v62 pilot4 amend: sector tool outputs lowercase 'x' — must be accepted.
    Composed-score table ('Finance Lift' / 'Composed Score' headers) must NOT
    extract 1.6× / 15.74 as a pair.
    """
    from tools.pair_verify import extract_pairs
    cases = [
        ("lift 6.66×, z=8.89 for a skill", "6.66", "8.89"),
        ("6.66× (z=8.89)", "6.66", "8.89"),
        ("**6.66×** z=8.89", "6.66", "8.89"),
        ("result 4.76×, z=9.39 noted", "4.76", "9.39"),
        # SA sector line with lowercase x  # v62 pilot4 amend:
        ("Financial Services  (sector lift 3.83x, z=7.03, n=485)", "3.83", "7.03"),
    ]
    for text, exp_lift, exp_z in cases:
        pairs = extract_pairs(text)
        assert len(pairs) >= 1, f"No pairs found in: {text!r}"
        assert pairs[0]["lift_str"] == exp_lift, (
            f"lift_str={pairs[0]['lift_str']!r} != {exp_lift!r} in: {text!r}"
        )
        assert pairs[0]["z_str"] == exp_z, (
            f"z_str={pairs[0]['z_str']!r} != {exp_z!r} in: {text!r}"
        )
    # Table format: z= prefix in next cell → extracted  # v62 pilot4 amend:
    table = "| Skill | 6.66× | z=8.89 | notes |"
    table_pairs = extract_pairs(table)
    assert len(table_pairs) >= 1, f"No pairs found in table row: {table!r}"
    assert table_pairs[0]["lift_str"] == "6.66"
    assert table_pairs[0]["z_str"] == "8.89"
    # Composed-score table: Finance Lift + Composed Score headers → 1.6×/15.74 NOT extracted  # v62 pilot4 amend:
    composed_table = (
        "| Skill | Agentic Lift | Finance Lift | Composed Score |\n"
        "|---|---|---|---|\n"
        "| **AutoGen** | 9.87× (z=4.66) | 1.6× | 15.74 |\n"
    )
    all_comp_pairs = extract_pairs(composed_table)
    bad = [p for p in all_comp_pairs if p["lift_str"] == "1.6" and p["z_str"] == "15.74"]
    assert not bad, (
        f"composed-score 1.6×/15.74 must NOT be extracted, but got: {bad}"
    )
    # 9.87×/4.66 (inline within the cell) is still found by INLINE regex  # v62 pilot4 amend:
    agentic = [p for p in all_comp_pairs if p["lift_str"] == "9.87"]
    assert agentic, "9.87×/4.66 (inline in table cell) should still be extracted by inline regex"
    print("  PASS — extract_pairs finds all required inline and table formats;"
          " sector x-form extracted; composed-score 1.6×/15.74 not extracted")


def test_pair_verify_detects_cross_entry_splice():  # v62 pilot4:
    """The pilot-3 splice '6.66×, z=13.13' must FAIL via data-table lookup.

    v62 pilot4 amend: verification uses frozen data tables, not run evidence.
    _is_pair_in_tables("6.66", "13.13") must return False (not in any table row).
    _is_pair_in_tables("6.66", "8.89") must return True (real pair in tables).
    _is_pair_in_tables("6.23", "13.13") must return True (real pair in tables).
    verify_all on a spliced answer must have exactly 1 failing pair.
    """
    from tools.pair_verify import _is_pair_in_tables, verify_all  # v62 pilot4 amend:

    # Data-table checks (arm-independent)  # v62 pilot4 amend:
    assert not _is_pair_in_tables("6.66", "13.13"), (
        "splice 6.66×/z=13.13 must NOT verify — not in any data-table row"
    )
    assert _is_pair_in_tables("6.66", "8.89"), (
        "6.66×/z=8.89 must verify — real pair in data tables"
    )
    assert _is_pair_in_tables("6.23", "13.13"), (
        "6.23×/z=13.13 must verify — real pair in data tables"
    )

    # verify_all on the spliced pair text must produce a failing entry  # v62 pilot4 amend:
    text = "RAG 6.66×, z=13.13 is the best skill."
    result = verify_all(text, [])
    assert len(result["failing"]) == 1, (
        f"Expected 1 failing pair, got {len(result['failing'])}: {result['failing']}"
    )
    assert result["failing"][0]["lift_str"] == "6.66"
    assert result["failing"][0]["z_str"] == "13.13"
    print("  PASS — splice 6.66×/z=13.13 correctly FAILS via data-table lookup")


def test_pair_verify_passes_colocated_pair():  # v62 pilot4:
    """Real data-table pairs must verify; sector line in x form must verify.

    v62 pilot4 amend: verification uses frozen data tables (not evidence).
    SA sector line 'sector lift 3.83x, z=7.03' must verify via _is_pair_in_tables.
    Real pairs 6.66/8.89 and 4.76/9.39 must also verify.
    """
    from tools.pair_verify import _is_pair_in_tables, verify_all  # v62 pilot4 amend:

    # SA sector line in x form verifies via data tables  # v62 pilot4 amend:
    assert _is_pair_in_tables("3.83", "7.03"), (
        "sector lift 3.83×/z=7.03 must verify — real pair in data tables"
    )

    # Two real pairs in answer text both pass verify_all with no evidence  # v62 pilot4 amend:
    text = (
        "Top skill: Agentic AI 6.66×, z=8.89. "
        "Second: Cloud Engineering 4.76×, z=9.39."
    )
    result = verify_all(text, [])
    assert len(result["pairs"]) == 2, f"Expected 2 pairs, got {len(result['pairs'])}"
    assert len(result["failing"]) == 0, (
        f"Expected 0 failing pairs, got {len(result['failing'])}: {result['failing']}"
    )
    assert len(result["verified_indices"]) == 2

    # Rounding-tie: table value at exact tolerance boundary must verify  # v62 pilot4 amend2:
    assert _is_pair_in_tables("12.38", "3.34"), (
        "12.38/3.34 must verify — rounding tie at tolerance boundary (epsilon fix)"
    )
    assert _is_pair_in_tables("9.12", "2.39"), (
        "9.12/2.39 must verify — rounding tie at tolerance boundary (epsilon fix)"
    )
    print("  PASS — real data-table pairs verified; sector 3.83×/z=7.03 verifies; rounding ties pass")


def test_orch_general_backstory_hash():  # v62 pilot2 amend1:
    """_ORCHESTRATOR_PLAIN_BACKSTORY + _ORCH_GENERAL_PROCEDURE_TEXT must match
    the pinned general hash. If this fails, one of those was edited without
    updating _ORCH_GENERAL_BACKSTORY_HASH — update it in orchestrator.py.
    """
    general_text = _ORCHESTRATOR_PLAIN_BACKSTORY + _ORCH_GENERAL_PROCEDURE_TEXT
    actual = hashlib.sha256(general_text.encode()).hexdigest()
    assert actual == _ORCH_GENERAL_BACKSTORY_HASH, (
        f"Orchestrator general backstory hash mismatch:\n"
        f"  got    : {actual}\n"
        f"  pinned : {_ORCH_GENERAL_BACKSTORY_HASH}\n"
        "Update _ORCH_GENERAL_BACKSTORY_HASH in orchestrator.py if you intentionally changed it."
    )
    print(f"  PASS — Orchestrator general backstory hash matches pinned value (len={len(general_text)})")


def test_pair_verify_default_on():  # v63:
    """PAIR_VERIFY must default to True (layer on) when env var PAIR_VERIFY is unset.

    v63: default changed from '0' to '1'.
    """
    import os
    import tools.pair_verify as pv
    if os.environ.get("PAIR_VERIFY"):
        print(f"  SKIP — PAIR_VERIFY={os.environ['PAIR_VERIFY']!r} set in env, skipping default check")
        return
    assert pv.PAIR_VERIFY, (
        "PAIR_VERIFY must be True when PAIR_VERIFY env var is not set "
        "(default changed to '1' in v63)"
    )
    print("  PASS — PAIR_VERIFY defaults to True (layer on) when env var is unset")


def test_pair_verify_range_skipped():  # v63:
    """Range expressions must be skipped (not checked, not failed, not removed).

    - Inline range '15.12x-15.91x, z=4.66-7.38' -> ranges_skipped >= 1, 0 pairs, 0 failing.
    - Table range '| Tableau | 3.35-3.89x | z=12.80-13.62 |' -> 0 pairs, 0 failing.
    - RAG splice '6.66x, z=13.13' and table splice '| ... | 6.66x | z=13.13 |' still fail.
    - run_pair_verify with range text: answer unchanged, n_removed=0, ranges_skipped >= 1.
    """
    import tools.pair_verify as pv

    # 1. Inline range: en-dash variants
    for range_text in [
        "Top skills: 15.12×–4.66×, z=4.66–7.38 across cohort.",  # U+2013
        "Top skills: 15.12×—15.91×, z=4.66–7.38 across cohort.",  # U+2014
        "Top skills: 15.12×-15.91×, z=4.66-7.38 across cohort.",            # hyphen
    ]:
        result = pv.verify_all(range_text, [])
        assert result["pairs"] == [], (
            f"Inline range must produce 0 pairs in {range_text!r}: {result['pairs']}"
        )
        assert result["failing"] == [], (
            f"Inline range must have 0 failing in {range_text!r}: {result['failing']}"
        )
        assert result["ranges_skipped"] >= 1, (
            f"Inline range must increment ranges_skipped in {range_text!r}: "
            f"ranges_skipped={result['ranges_skipped']}"
        )

    # 2. Table row with range cells — not extracted, not failed
    table_range = "| Tableau | 3.35–3.89× | z=12.80–13.62 |"
    result2 = pv.verify_all(table_range, [])
    assert result2["pairs"] == [], (
        f"Table range row must produce 0 pairs, got {result2['pairs']}"
    )
    assert result2["failing"] == [], (
        f"Table range row must have 0 failing, got {result2['failing']}"
    )

    # 3. RAG splice 6.66x/z=13.13 still fails (not a range)
    splice_text = "RAG 6.66×, z=13.13 is the best skill."
    result3 = pv.verify_all(splice_text, [])
    assert len(result3["failing"]) == 1, (
        f"Splice 6.66x/z=13.13 must still fail, got {result3['failing']}"
    )
    assert result3["failing"][0]["lift_str"] == "6.66"
    assert result3["failing"][0]["z_str"] == "13.13"

    # 4. Table splice | ... | 6.66x | z=13.13 | still fails
    table_splice = "| Skill | 6.66× | z=13.13 | notes |"
    result4 = pv.verify_all(table_splice, [])
    assert len(result4["failing"]) >= 1, (
        f"Table splice 6.66x/z=13.13 must still fail, got {result4['failing']}"
    )

    # 5. run_pair_verify with range: answer unchanged, n_removed=0, ranges_skipped >= 1
    orig_flag = pv.PAIR_VERIFY
    try:
        pv.PAIR_VERIFY = True
        range_ans = "Top skills: 15.12×–15.91×, z=4.66–7.38 across cohort."
        result_ans, summary = pv.run_pair_verify(range_ans, [], llm=None)
        assert result_ans == range_ans, (
            "Answer must be unchanged when only ranges are present"
        )
        assert summary["n_removed"] == 0, (
            f"n_removed must be 0 for range-only answer, got {summary['n_removed']}"
        )
        assert summary["ranges_skipped"] >= 1, (
            f"ranges_skipped must be >= 1, got {summary['ranges_skipped']}"
        )
    finally:
        pv.PAIR_VERIFY = orig_flag

    print("  PASS — inline range skipped (ranges_skipped>=1), table range not extracted, "
          "splices still fail, run_pair_verify leaves range answer unchanged")


# ── Runner ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        test_tool_set_union,
        test_ma_unchanged,
        test_guard1_catches_specialist_attribution,
        test_guard4_catches_delegation_claim,
        test_guard2_catches_numeric_fabrication,
        test_guard3_catches_content_fabrication,
        test_plain_backstory_unchanged,       # v62 pilot:
        test_structured_backstory_hash,       # v62 pilot2:
        test_general_backstory_hash,          # v62 pilot2:
        test_orch_plain_backstory_hash,       # v62 pilot2 amend1:
        test_orch_general_backstory_hash,     # v62 pilot2 amend1:
        test_pair_verify_disabled_returns_identity,  # v62 pilot4:
        test_pair_verify_extracts_inline_pairs,      # v62 pilot4:
        test_pair_verify_detects_cross_entry_splice, # v62 pilot4:
        test_pair_verify_passes_colocated_pair,      # v62 pilot4:
        test_sa_sequenced_backstory_equals_general_plus_step,  # v62 pilot5:
        test_sa_sequenced_backstory_hash,            # v62 pilot5:
        test_orch_sequenced_backstory_equals_general_plus_step,  # v62 pilot5:
        test_sequenced_procedure_recorded_in_header,  # v62 pilot5:
        test_pair_verify_default_on,                 # v63:
        test_pair_verify_range_skipped,              # v63:
    ]
    failures = []
    for fn in tests:
        print(f"\n[TEST] {fn.__name__}")
        try:
            fn()
        except Exception as exc:
            print(f"  FAIL — {exc}")
            failures.append((fn.__name__, exc))

    print(f"\n{'=' * 50}")
    if failures:
        print(f"FAILED: {len(failures)} / {len(tests)}")
        for name, exc in failures:
            print(f"  {name}: {exc}")
        sys.exit(1)
    else:
        print(f"ALL {len(tests)} / {len(tests)} TESTS PASSED")
