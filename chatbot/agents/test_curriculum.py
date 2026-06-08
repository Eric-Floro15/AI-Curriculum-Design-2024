"""
test_curriculum.py — REMOVED.

The Curriculum Architect agent has been merged into the University AI
Programs Researcher. There is no separate agent to test.

To smoke-test curriculum fetching, run:
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_university_programs.py

To smoke-test gap analysis (structured fetch → Cluster Interpreter), run:
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py \
        --only curriculum-fetch-mmai,curriculum-cluster-gap-analysis

This file is a tombstone — do not import from it.
"""

raise ImportError(
    "test_curriculum.py has been removed. "
    "Run test_university_programs.py to test curriculum fetching."
)
