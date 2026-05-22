"""
run_rag_eval.py — Baseline retrieval eval for the skills RAG tool.

Runs each query in queries.yaml through tools.rag_tool.retrieve() and computes
precision@k / recall@k against the curated `expected` substrings (normalized:
lowercase, non-alphanumerics stripped).

Writes a dated snapshot Markdown file next to this script so future runs are
easy to diff against today's baseline.

Run:
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_rag_eval.py
"""

import os
import re
import sys
from datetime import date

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from tools.rag_tool import retrieve  # noqa: E402

QUERIES_FILE = os.path.join(_HERE, "queries.yaml")
K = 5

_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")


def _normalize(s: str) -> str:
    return _NORMALIZE_RE.sub("", s.lower())


def is_match(retrieved_skill: str, expected_term: str) -> bool:
    """True if the expected substring appears inside the retrieved skill name."""
    return _normalize(expected_term) in _normalize(retrieved_skill)


def score_query(query: str, expected: list[str], k: int = K) -> dict:
    results = retrieve(query, k=k)
    retrieved = [r["skill"] for r in results]

    relevant = [s for s in retrieved if any(is_match(s, e) for e in expected)]
    matched_expected = sorted(
        {e for e in expected if any(is_match(s, e) for s in retrieved)}
    )

    return {
        "retrieved": retrieved,
        "relevant": relevant,
        "matched_expected": matched_expected,
        "precision_at_k": len(relevant) / k,
        "recall_at_k": (len(matched_expected) / len(expected)) if expected else 0.0,
    }


def main() -> None:
    with open(QUERIES_FILE) as f:
        cases = yaml.safe_load(f)

    body: list[str] = []
    p_sum = r_sum = 0.0

    for case in cases:
        result = score_query(case["query"], case["expected"], k=K)
        p_sum += result["precision_at_k"]
        r_sum += result["recall_at_k"]

        body += [
            f"## [{case['id']}] {case['query']!r}",
            "",
            f"- expected: `{case['expected']}`",
            f"- precision@{K} = **{result['precision_at_k']:.2f}** ({len(result['relevant'])}/{K})",
            f"- recall@{K} = **{result['recall_at_k']:.2f}** "
            f"({len(result['matched_expected'])}/{len(case['expected'])})",
            f"- matched expected: {result['matched_expected'] or '—'}",
            "- retrieved:",
        ]
        for s in result["retrieved"]:
            mark = "x" if s in result["relevant"] else " "
            body.append(f"    - [{mark}] {s}")
        body.append("")

    n = len(cases)
    avg_p = p_sum / n
    avg_r = r_sum / n

    header = [
        f"# RAG retrieval baseline — {date.today().isoformat()}",
        "",
        f"- queries: {n}",
        f"- k: {K}",
        f"- **mean precision@{K} = {avg_p:.2f}**",
        f"- **mean recall@{K} = {avg_r:.2f}**",
        "",
        "Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_rag_eval.py`",
        "",
        "---",
        "",
    ]

    snapshot_path = os.path.join(_HERE, f"baseline_{date.today().isoformat()}.md")
    with open(snapshot_path, "w") as f:
        f.write("\n".join(header + body))

    print(f"Snapshot written to: {snapshot_path}")
    print(f"Mean precision@{K} = {avg_p:.2f}")
    print(f"Mean recall@{K} = {avg_r:.2f}")


if __name__ == "__main__":
    main()
