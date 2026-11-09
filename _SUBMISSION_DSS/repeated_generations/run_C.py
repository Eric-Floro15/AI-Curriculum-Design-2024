#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_C.py — Condition C: bare claude-sonnet-4-6 + W2026 Agentic AI lift table, §4.7 query.

Copied from _SUBMISSION_DSS/grounding_rescore/run_d_base_with_table.py with three changes:
  1. The table is the FINAL W2026 "Agentic Ai" rows from chatbot/data/skill_lift_table.csv
     (62 rows — the production table the assistant's Skills Taxonomy Analyst uses).
  2. Takes --label; outputs C_<label>.txt + C_<label>_meta.json.
  3. --dry flag uses the dev lane (current .env provider/model, no override); without
     --dry the provider and model are forced to anthropic / claude-sonnet-4-6.

Everything else (prompt wording, single call, identical query) is identical to the original.

Usage:
    python _SUBMISSION_DSS/repeated_generations/run_C.py --label v63rg-C-1
    python _SUBMISSION_DSS/repeated_generations/run_C.py --label v63rg-C-dry --dry
"""

import argparse, os, sys, csv, time, json
from pathlib import Path

HERE    = Path(__file__).resolve().parent          # _SUBMISSION_DSS/repeated_generations
REPO    = HERE.parents[1]                           # repo root
CHATBOT = REPO / "chatbot"

sys.path.insert(0, str(CHATBOT))
os.chdir(CHATBOT)

from dotenv import load_dotenv
load_dotenv(CHATBOT / ".env")

# ── load the FINAL W2026 Agentic Ai rows ─────────────────────────────────────
LIFT_TABLE = CHATBOT / "data" / "skill_lift_table.csv"

QUERY = (
    "I'm updating my AI/ML Master's curriculum and want to know whether agentic AI warrants its own "
    "dedicated course rather than a module inside the existing machine-learning course. Using the market data: "
    "which skills are most distinctively in demand for agentic AI (report lift and statistical significance, not "
    "just raw frequency); which existing analyst/BI-oriented skills is agentic AI actually not associated with; "
    "how do peer programs currently cover agentic AI; and what recent industry developments should shape the "
    "course? Give concrete, grounded recommendations."
)


def build_table() -> tuple[str, int]:
    rows = []
    with open(LIFT_TABLE, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["skill"] == "Agentic Ai":
                rows.append((r["associated_skill"], float(r["lift"]), float(r["z"])))
    rows.sort(key=lambda x: -x[2])
    table = "\n".join(f"- {s}: lift {l:.2f}x, z {z:.1f}" for s, l, z in rows)
    return table, len(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--label", required=True, help="Run label, e.g. v63rg-C-1")
    ap.add_argument("--dry", action="store_true",
                    help="Dev lane: use current .env provider/model, no override")
    args = ap.parse_args()

    if not args.dry:
        os.environ["LLM_PROVIDER"] = "anthropic"
        os.environ["LLM_MODEL"]    = "claude-sonnet-4-6"

    from llm import get_llm, describe_llm_config   # noqa: E402
    print("CONFIG:", describe_llm_config())

    table, n_rows = build_table()
    print(f"Agentic Ai rows provided: {n_rows} | table chars: {len(table)}")
    if n_rows == 0:
        raise SystemExit("No 'Agentic Ai' rows in skill_lift_table.csv — check path.")

    prompt = (
        "Here is market data from an analysis of job postings on the skills most distinctively co-demanded with "
        "agentic AI (lift = how over-represented the skill is in agentic-AI postings relative to the overall market; "
        f"z = statistical significance via weighted log-odds):\n\n{table}\n\n{QUERY}"
    )
    print(f"Prompt chars: {len(prompt)}")

    llm = get_llm()
    t0  = time.time()
    out = llm.call([{"role": "user", "content": prompt}])
    dt  = time.time() - t0

    out_txt  = HERE / f"C_{args.label}.txt"
    out_json = HERE / f"C_{args.label}_meta.json"
    out_txt.write_text(out, encoding="utf-8")

    in_tok  = len(prompt) // 4
    out_tok = len(out)    // 4
    cost    = in_tok / 1e6 * 3.0 + out_tok / 1e6 * 15.0
    meta    = {
        "label":                args.label,
        "condition":            "C_bare_with_table",
        "dry":                  args.dry,
        "model":                os.environ.get("LLM_MODEL", ""),
        "provider":             os.environ.get("LLM_PROVIDER", ""),
        "wall_s":               round(dt, 1),
        "approx_input_tokens":  in_tok,
        "approx_output_tokens": out_tok,
        "approx_cost_usd":      round(cost, 3),
        "n_agentic_rows_given": n_rows,
    }
    out_json.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"\n✓ DONE in {dt:.0f}s (~${cost:.3f}). Wrote:\n  {out_txt}\n  {out_json}")


if __name__ == "__main__":
    main()
