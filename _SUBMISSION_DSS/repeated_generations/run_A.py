#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_A.py — Condition A: assistant (orchestrated) run, §4.7 query.

Usage:
    python _SUBMISSION_DSS/repeated_generations/run_A.py --label v63rg-A-1
    python _SUBMISSION_DSS/repeated_generations/run_A.py --label v63rg-A-dry   # dev lane (no override)

--dry / no --dry: unlike run_B.py and run_C.py, Condition A runs the full assistant
crew with whatever LLM_PROVIDER / LLM_MODEL chatbot/.env already specifies.  The
--dry flag is accepted for interface consistency but has no effect — the assistant
always uses its configured provider.

For Stage 1A/1B, .env must be switched to anthropic / claude-sonnet-4-6 BEFORE calling
this script; this script does NOT override the env (unlike run_B/run_C, which force
anthropic when not --dry).

Writes:
    chatbot/run_records/run_<ts>_<label>_success.md   (and _full.md)
    _SUBMISSION_DSS/repeated_generations/A_<label>.txt <- Final Answer extracted from record
"""

import argparse, os, re, sys, time
from pathlib import Path

HERE    = Path(__file__).resolve().parent
REPO    = HERE.parents[1]
CHATBOT = REPO / "chatbot"

sys.path.insert(0, str(CHATBOT))
os.chdir(CHATBOT)

from dotenv import load_dotenv
load_dotenv(CHATBOT / ".env")

QUERY = (
    "I'm updating my AI/ML Master's curriculum and want to know whether agentic AI warrants its own "
    "dedicated course rather than a module inside the existing machine-learning course. Using the market data: "
    "which skills are most distinctively in demand for agentic AI (report lift and statistical significance, not "
    "just raw frequency); which existing analyst/BI-oriented skills is agentic AI actually not associated with; "
    "how do peer programs currently cover agentic AI; and what recent industry developments should shape the "
    "course? Give concrete, grounded recommendations."
)


def _extract_final_answer(record_text: str) -> str | None:
    """Extract Final Answer section (stops at ## Pair Verification, ## Per-Agent Tool-Call Trace, or EOF)."""
    idx = record_text.find("## Final Answer")
    if idx < 0:
        idx = record_text.find("## Partial Answer")
    if idx < 0:
        return None
    after = record_text[idx + len("## Final Answer"):]
    end = len(after)
    for marker in ("\n## Pair Verification", "\n## Per-Agent Tool-Call Trace"):
        m = after.find(marker)
        if m >= 0:
            end = min(end, m)
    return after[:end].strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--label", required=True, help="Run label, e.g. v63rg-A-1")
    ap.add_argument("--dry", action="store_true",
                    help="Accepted for interface consistency; no effect on provider")
    args = ap.parse_args()

    from agents.orchestrator import run_query, _RUN_RECORDS_DIR  # noqa: E402

    rr_dir = Path(_RUN_RECORDS_DIR)
    before = set(rr_dir.iterdir()) if rr_dir.exists() else set()

    print(f"Label   : {args.label}")
    print(f"Provider: {os.environ.get('LLM_PROVIDER', '(not set)')}")
    print(f"Model   : {os.environ.get('LLM_MODEL', '(not set)')}")
    t0 = time.time()
    answer = run_query(QUERY)
    dt = time.time() - t0

    # Find and relabel new run records
    after_set  = set(rr_dir.iterdir()) if rr_dir.exists() else set()
    new_files  = sorted(after_set - before)
    renamed    = []
    for p in new_files:
        new_name = p.name.replace("_success", f"_{args.label}_success").replace(
                                  "_failure", f"_{args.label}_failure")
        dst = p.parent / new_name
        p.rename(dst)
        renamed.append(dst)

    # Find the main (non-full) record
    main_record = next((p for p in renamed if "_full" not in p.name), None)

    # Extract final answer from the record
    out_txt = HERE / f"A_{args.label}.txt"
    if main_record and main_record.exists():
        record_text = main_record.read_text(encoding="utf-8")
        final_ans   = _extract_final_answer(record_text) or answer or ""
    else:
        final_ans = answer or ""
    out_txt.write_text(final_ans, encoding="utf-8")

    print(f"\n[DONE] wall time: {dt:.1f}s")
    print("Run records:")
    for p in renamed:
        print(f"  {p}")
    print(f"Output text: {out_txt} ({len(final_ans)} chars)")


if __name__ == "__main__":
    main()
