"""
test_single_agent.py — Unit tests for the SA ablation module (single_agent.py).

Tests (no LLM calls — all static / import-time checks):
  1. tool_set_union  — SA agent's tools == exact union of all four specialists.
  2. ma_unchanged    — build_crew() still returns 5 agents; orchestrator max_iter
                       unchanged at 8.
  3. guard1_catches  — guard #1 (_detect_fabrication_flags) flags a specialist
                       name cited as a source in an SA answer (delegated_to=[]).
  4. guard4_catches  — guard #4 (_detect_delegation_claim_flags) flags an
                       affirmative "consulted" claim in an SA answer.
  5. guard2_catches  — guard #2 (_detect_numeric_fabrication_flags) flags a
                       lift/z value absent from _build_sa_step_log tool outputs.
  6. guard3_catches  — guard #3 (_detect_content_attribution_flags) flags a URL
                       absent from _build_sa_step_log tool outputs.

Run:
  KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_single_agent.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from agents.single_agent import _SA_TOOLS, _build_sa_step_log  # noqa: E402
from agents.orchestrator import (  # noqa: E402
    _detect_content_attribution_flags,
    _detect_delegation_claim_flags,
    _detect_fabrication_flags,
    _detect_numeric_fabrication_flags,
    build_crew,
    make_orchestrator,
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


# ── Runner ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        test_tool_set_union,
        test_ma_unchanged,
        test_guard1_catches_specialist_attribution,
        test_guard4_catches_delegation_claim,
        test_guard2_catches_numeric_fabrication,
        test_guard3_catches_content_fabrication,
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
