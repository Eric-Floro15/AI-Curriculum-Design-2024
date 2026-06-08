"""
curriculum.py — REMOVED.

The Curriculum Architect agent has been merged into the University AI
Programs Researcher (university_programs.py).

When the Orchestrator needs a structured course list for gap analysis,
it delegates to "University AI Programs Researcher" and asks for
structured output. The Cluster Interpreter then receives that output
directly from the Orchestrator.

This file is a tombstone — do not import from it.
"""

raise ImportError(
    "curriculum.py has been removed. "
    "Use agents.university_programs.make_university_programs_agent() instead. "
    "See university_programs.py for the structured-output mode."
)
