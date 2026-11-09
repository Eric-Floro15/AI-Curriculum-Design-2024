#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_B.py — Condition B: bare claude-sonnet-4-6, no data, §4.7 query.

Usage:
    python _SUBMISSION_DSS/repeated_generations/run_B.py --label v63rg-B-1
    python _SUBMISSION_DSS/repeated_generations/run_B.py --label v63rg-B-dry --dry

Writes:
    _SUBMISSION_DSS/repeated_generations/B_<label>.txt    <- curriculum text
    _SUBMISSION_DSS/repeated_generations/B_<label>_meta.json

--dry  uses dev lane (LLM_PROVIDER / LLM_MODEL from chatbot/.env as-is; no override),
       so the plumbing can be tested free.  Without --dry the provider and model are
       forced to anthropic / claude-sonnet-4-6.

Identical query to the original bare run (extrinsic_eval_base_run_record_2026-09-25.md).
No data is given; only the query. This matches the §4.7 "base, no data" condition.
"""

import argparse, os, sys, time, json
from pathlib import Path

HERE   = Path(__file__).resolve().parent          # _SUBMISSION_DSS/repeated_generations
REPO   = HERE.parents[1]                           # repo root
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


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--label", required=True, help="Run label, e.g. v63rg-B-1")
    ap.add_argument("--dry", action="store_true",
                    help="Dev lane: use current .env provider/model, no override")
    args = ap.parse_args()

    if not args.dry:
        os.environ["LLM_PROVIDER"] = "anthropic"
        os.environ["LLM_MODEL"]    = "claude-sonnet-4-6"

    from llm import get_llm, describe_llm_config   # noqa: E402  (import after env override)
    print("CONFIG:", describe_llm_config())
    print(f"Query chars: {len(QUERY)}")

    llm = get_llm()
    t0  = time.time()
    out = llm.call([{"role": "user", "content": QUERY}])
    dt  = time.time() - t0

    out_txt  = HERE / f"B_{args.label}.txt"
    out_json = HERE / f"B_{args.label}_meta.json"
    out_txt.write_text(out, encoding="utf-8")

    in_tok  = len(QUERY) // 4
    out_tok = len(out)   // 4
    cost    = in_tok / 1e6 * 3.0 + out_tok / 1e6 * 15.0
    meta    = {
        "label":                args.label,
        "condition":            "B_bare_no_data",
        "dry":                  args.dry,
        "model":                os.environ.get("LLM_MODEL", ""),
        "provider":             os.environ.get("LLM_PROVIDER", ""),
        "wall_s":               round(dt, 1),
        "approx_input_tokens":  in_tok,
        "approx_output_tokens": out_tok,
        "approx_cost_usd":      round(cost, 3),
    }
    out_json.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"\n✓ DONE in {dt:.0f}s (~${cost:.3f}). Wrote:\n  {out_txt}\n  {out_json}")


if __name__ == "__main__":
    main()
