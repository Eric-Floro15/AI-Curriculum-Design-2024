#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S2 join: fill the empty `industry` column in every posting_attributes.csv.

    python apply_industry_to_attributes.py --dry-run    # preview coverage, write nothing
    python apply_industry_to_attributes.py              # populate industry in place (.bak kept)

build_posting_attributes.py deliberately leaves `industry = NaN` (its line 253,
"filled by the S2 classifier"). This script is that fill step. It is pure-local,
makes no network calls, and is idempotent — re-running just re-applies the map.

It keys on `company_norm`, the SAME normalised key the sector table was built from,
so the join is exact (no re-normalising). Source of the labels, in order of
preference:
  1) company_sectors_final.csv  (sourced EDGAR/Wikidata + LLM fallback; column
     `sector_final`) — use this once you have run classify_companies_llm.py;
  2) company_sectors_compared.csv (sourced only; column `sector_best`) — the
     fallback if you have not run the LLM step yet.
Override with --source <path> --column <name>.
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent
RUNS = ROOT / "RE-ANALYSIS-2026" / "pipeline_runs"
FINAL = ROOT / "company_sectors_final.csv"
COMPARED = ROOT / "company_sectors_compared.csv"


def load_map(source, column):
    if source:
        path, col = Path(source), column
    elif FINAL.exists():
        path, col = FINAL, "sector_final"
    elif COMPARED.exists():
        path, col = COMPARED, "sector_best"
    else:
        sys.exit("No company_sectors_final.csv or company_sectors_compared.csv found.")
    df = pd.read_csv(path)
    if col not in df.columns:
        sys.exit(f"Column {col!r} not in {path.name}. Columns: {list(df.columns)}")
    m = {}
    for _, r in df.iterrows():
        v = r.get(col)
        if isinstance(v, str) and v.strip() and v.strip().lower() != "nan":
            m[str(r["company_norm"])] = v.strip()
    print(f"sector map: {len(m):,} companies from {path.name}::{col}")
    return m


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", default=None, help="explicit company->sector csv")
    ap.add_argument("--column", default="sector_final", help="sector column in --source")
    ap.add_argument("--dry-run", action="store_true", help="report coverage; write nothing")
    ap.add_argument("--no-backup", action="store_true", help="skip the one-time .bak")
    args = ap.parse_args()

    smap = load_map(args.source, args.column)
    files = sorted(p for p in RUNS.glob("*/posting_attributes.csv")
                   if "FEATURE_TEST" not in str(p))
    if not files:
        sys.exit(f"No posting_attributes.csv under {RUNS}.")

    grand_tot = grand_cov = 0
    for p in files:
        df = pd.read_csv(p)
        if "company_norm" not in df.columns:
            print(f"  {p.parent.name}: no company_norm column — skipped")
            continue
        industry = df["company_norm"].map(smap)
        n, cov = len(df), int(industry.notna().sum())
        grand_tot += n
        grand_cov += cov
        wave = p.parent.name
        print(f"  {wave:7s} n={n:6,}  industry set = {cov:6,} ({100*cov/n:4.1f}%)")
        if not args.dry_run:
            if not args.no_backup:
                bak = p.with_suffix(".csv.bak")
                if not bak.exists():
                    df.to_csv(bak, index=False)      # one-time snapshot of the pre-join file
            df["industry"] = industry
            df.to_csv(p, index=False)

    verb = "would set" if args.dry_run else "set"
    print(f"\n{verb} industry on {grand_cov:,}/{grand_tot:,} postings "
          f"({100*grand_cov/grand_tot:.1f}% of the corpus).")
    if args.dry_run:
        print("dry-run: nothing written. Re-run without --dry-run to apply.")
    else:
        print("done. Backups saved as posting_attributes.csv.bak in each wave folder.")


if __name__ == "__main__":
    main()
