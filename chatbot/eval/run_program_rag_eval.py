"""
run_program_rag_eval.py — Baseline retrieval eval for tools/program_rag_tool.py
(the university program/curriculum RAG). NOT the skills RAG eval — see
run_rag_eval.py for that one; the two tools have different result schemas
and this script is not a drop-in reuse of that one.

Runs each query in program_queries.yaml through tools.program_rag_tool.retrieve()
and scores it one of two ways:

  - directional cases (expected: [...]):  precision@k / recall@k against the
    curated `expected` substrings, matched against each result's `program`
    metadata field (the program title) — NOT free body/content text.
  - negative-control cases (expect_empty: true): pass/fail on whether
    retrieve() returned zero hits, i.e. whether PROGRAM_RAG_MAX_DISTANCE
    correctly rejected every candidate so the agent would fall back to
    web_search_tool instead of returning a false-positive local match.

Also reports, per directional case, whether ALL retrieved chunks belonged
to the expected program ("no cross-contamination"). With only a couple of
programs in the corpus, raw precision@k is noisy (perfect retrieval still
caps out well below 1.0 once k > number of distinct programs) — the
no-cross-contamination flag is the more meaningful pass/fail signal at
this corpus size, and stays meaningful as the corpus grows.

Writes a dated snapshot Markdown file next to this script (prefixed
`program_baseline_` so it never collides with the skills RAG's
`baseline_*.md` files in this same directory) so future runs — especially
after adding more program files, or after retuning
PROGRAM_RAG_MAX_DISTANCE — are easy to diff against today's numbers.

Run:
    KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_program_rag_eval.py
"""

import os
import re
import sys
from datetime import date, datetime

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

from tools.program_rag_tool import retrieve, _load_vectorstore, INDEX_DIR, MAX_DISTANCE  # noqa: E402
from embeddings import describe_embeddings_config  # noqa: E402
from build_program_index import CHUNK_SIZE, CHUNK_OVERLAP  # noqa: E402

QUERIES_FILE = os.path.join(_HERE, "program_queries.yaml")
K = 3


def _index_provenance() -> dict:
    """Capture which index + embedding config + threshold a baseline run was against."""
    store = _load_vectorstore()
    try:
        n_docs = store.index.ntotal
    except Exception:
        n_docs = "?"
    faiss_file = os.path.join(INDEX_DIR, "index.faiss")
    mtime_iso = (
        datetime.fromtimestamp(os.path.getmtime(faiss_file)).isoformat(timespec="seconds")
        if os.path.exists(faiss_file)
        else "?"
    )
    return {
        "embeddings": describe_embeddings_config(),
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "index_docs": n_docs,
        "index_mtime": mtime_iso,
        "max_distance": MAX_DISTANCE,
    }


_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")


def _normalize(s: str) -> str:
    return _NORMALIZE_RE.sub("", s.lower())


def is_match(retrieved_program: str, expected_term: str) -> bool:
    """True if the expected substring appears inside the retrieved program title."""
    return _normalize(expected_term) in _normalize(retrieved_program)


def score_query(
    query: str,
    expected: list[str],
    k: int = K,
    expect_empty: bool = False,
) -> dict:
    results = retrieve(query, k=k)
    retrieved = [r["program"] for r in results]
    distances = [r["distance"] for r in results]
    fused_scores = [r.get("fused_score") for r in results]
    bm25_scores = [r.get("bm25_score") for r in results]

    if expect_empty:
        return {
            "mode": "negative_control",
            "retrieved": retrieved,
            "distances": distances,
            "fused_scores": fused_scores,
            "bm25_scores": bm25_scores,
            "passed": len(retrieved) == 0,
        }

    relevant = [s for s in retrieved if any(is_match(s, e) for e in expected)]
    matched_expected = sorted(
        {e for e in expected if any(is_match(s, e) for s in retrieved)}
    )
    return {
        "mode": "directional",
        "retrieved": retrieved,
        "distances": distances,
        "fused_scores": fused_scores,
        "bm25_scores": bm25_scores,
        "relevant": relevant,
        "matched_expected": matched_expected,
        "precision_at_k": (len(relevant) / k) if k else 0.0,
        "recall_at_k": (len(matched_expected) / len(expected)) if expected else 0.0,
        "no_cross_contamination": bool(retrieved) and len(relevant) == len(retrieved),
    }


def main() -> None:
    with open(QUERIES_FILE) as f:
        cases = yaml.safe_load(f)

    body: list[str] = []
    p_sum = r_sum = 0.0
    n_directional = 0
    n_clean = 0
    n_negative = 0
    n_negative_passed = 0

    for case in cases:
        expect_empty = case.get("expect_empty", False)
        result = score_query(
            case["query"], case.get("expected", []), k=K, expect_empty=expect_empty
        )

        body.append(f"## [{case['id']}] {case['query']!r}")
        body.append("")

        if result["mode"] == "negative_control":
            n_negative += 1
            n_negative_passed += int(result["passed"])
            status = (
                "PASS (zero hits — correctly signals fall back to web search)"
                if result["passed"]
                else "FAIL (returned hits below threshold — see distance/fused_score/bm25_score below; "
                "neither distance nor bm25_score has separated this case from genuine matches in any "
                "run so far (both ranges overlap with genuine-match ranges — see program_rag_tool.py's "
                "module docstring 'Hybrid-retrieval history' for the worked numbers); a real fix likely "
                "needs a different kind of signal, e.g. literal institution-name presence/absence)"
            )
            body += [
                "- mode: negative control (expect zero hits)",
                f"- result: **{status}**",
                "- retrieved:" if result["retrieved"] else "- retrieved: (none)",
            ]
            for s, d, fs, bs in zip(
                result["retrieved"], result["distances"], result["fused_scores"], result["bm25_scores"]
            ):
                body.append(f"    - distance={d:.4f}  fused_score={fs:.6f}  bm25_score={bs:.4f}  {s}")
            body.append("")
            continue

        n_directional += 1
        p_sum += result["precision_at_k"]
        r_sum += result["recall_at_k"]
        n_clean += int(result["no_cross_contamination"])

        contamination_flag = (
            "no cross-contamination"
            if result["no_cross_contamination"]
            else "CROSS-CONTAMINATION DETECTED — a chunk from a different program ranked inside top-k"
        )
        body += [
            "- mode: directional",
            f"- expected: `{case.get('expected', [])}`",
            f"- precision@{K} = **{result['precision_at_k']:.2f}** ({len(result['relevant'])}/{K})",
            f"- recall@{K} = **{result['recall_at_k']:.2f}** "
            f"({len(result['matched_expected'])}/{len(case.get('expected', []))})",
            f"- {contamination_flag}",
            "- matched expected: " + (", ".join(result["matched_expected"]) or "—"),
            "- retrieved:",
        ]
        for s, d, fs, bs in zip(
            result["retrieved"], result["distances"], result["fused_scores"], result["bm25_scores"]
        ):
            mark = "x" if s in result["relevant"] else " "
            body.append(f"    - [{mark}] distance={d:.4f}  fused_score={fs:.6f}  bm25_score={bs:.4f}  {s}")
        body.append("")

    avg_p = p_sum / n_directional if n_directional else 0.0
    avg_r = r_sum / n_directional if n_directional else 0.0

    prov = _index_provenance()
    header = [
        f"# Program RAG retrieval baseline — {date.today().isoformat()}",
        "",
        "## Run config",
        f"- embeddings: `{prov['embeddings']}`",
        f"- chunk_size: {prov['chunk_size']}, chunk_overlap: {prov['chunk_overlap']}",
        f"- index docs (chunks): {prov['index_docs']}",
        f"- index built: {prov['index_mtime']}",
        f"- PROGRAM_RAG_MAX_DISTANCE: {prov['max_distance']}",
        f"- queries: {len(cases)} ({n_directional} directional, {n_negative} negative control)",
        f"- k: {K}",
        "",
        "## Results",
        f"- **mean precision@{K} = {avg_p:.2f}** (directional cases only — "
        "noisy at small corpus size; see no-cross-contamination below instead)",
        f"- **mean recall@{K} = {avg_r:.2f}**",
        f"- **no cross-contamination: {n_clean}/{n_directional}** directional cases "
        "retrieved ONLY chunks from the expected program",
        f"- **negative control: {n_negative_passed}/{n_negative}** passed "
        "(correctly returned zero hits)",
        "",
        "Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_program_rag_eval.py`",
        "",
        "---",
        "",
    ]

    model_slug = (
        os.getenv("OLLAMA_EMBED_MODEL", "mxbai-embed-large")
        if os.getenv("EMBEDDING_PROVIDER", "ollama").lower() == "ollama"
        else os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
    )
    safe_slug = re.sub(r"[^A-Za-z0-9._-]+", "-", model_slug)
    snapshot_path = os.path.join(
        _HERE, f"program_baseline_{date.today().isoformat()}_{safe_slug}.md"
    )
    with open(snapshot_path, "w") as f:
        f.write("\n".join(header + body))

    print(f"Snapshot written to: {snapshot_path}")
    print(f"Mean precision@{K} = {avg_p:.2f} (directional cases)")
    print(f"Mean recall@{K} = {avg_r:.2f}")
    print(f"No cross-contamination: {n_clean}/{n_directional}")
    print(f"Negative control passed: {n_negative_passed}/{n_negative}")


if __name__ == "__main__":
    main()
