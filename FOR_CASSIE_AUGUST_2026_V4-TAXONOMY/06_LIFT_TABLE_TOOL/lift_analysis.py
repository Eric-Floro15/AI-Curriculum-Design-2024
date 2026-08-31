#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Differential skill analysis: which skills are over-represented in a segment.

    # which skills co-occur with agentic AI beyond chance?
    python lift_analysis.py --skill "Agentic Ai"

    # sector / seniority / geography segments (needs posting_attributes.csv)
    python lift_analysis.py --where "industry=Life Sciences"
    python lift_analysis.py --where "industry=Finance & Insurance" --where "job_level>=6"

    python lift_analysis.py --skill "Agentic Ai" --semesters W2026 F2025 --top 30

NO NETWORK, NO LLM. Reads skill_presence_matrix.csv and posting_attributes.csv.

WHY THIS EXISTS, AND WHY IT MATTERS MORE THAN THE CLUSTERING
  The consensus partition moves by ARI 0.5-0.8 when a single design choice changes
  (decisions.md #34: weighted vs unweighted consensus), and that reshuffle already
  altered the case-study finding once. Any claim resting on two skills landing in
  the same cluster is resting on sand.

  Lift does not have that problem. It is computed directly from the posting x
  skill presence matrix, so it is invariant to clustering method, feature set,
  skill ordering and consensus weighting. If lift confirms an association, the
  claim survives every one of those choices.

METHOD  (Segmentation_and_Differential_Analysis_Plan_2026-08-04.md §3.2)
  1. Independent filter: skills with n_segment < --min-count are dropped BEFORE
     testing. Fisher on n=1 is noise however it is corrected, and filtering on the
     marginal count is independent of the association under the null -- the
     standard independent-filtering argument (Bourgon et al. 2010). Without it the
     top of the list is junk: "Maintenance Of Laboratory Equipment", n=1, lift 17.
  2. Lift = P(skill | segment) / P(skill | baseline).
  3. Fightin'-Words log-odds z-score with an informative Dirichlet prior (Monroe,
     Colaresi & Quinn 2008) -- shrinks rare terms continuously rather than by a
     hard cutoff, so the threshold governs what is DISPLAYED, not what is inferred.
  4. Fisher exact, one-sided.
  5. Benjamini-Hochberg FDR **within the segment**. The family is that segment's
     skills, not all segments pooled: each segment is a separate question, and
     pooling would be conservative and conceptually wrong. BH rather than BY
     because skills co-occur, i.e. the statistics are positively dependent, which
     is the condition under which BH holds.

  Report lift (interpretable), z (shrunk effect size) and q (significance)
  together. Where they disagree, believe z over lift -- lift is unshrunk.

BASELINES
  Default is the whole corpus. --baseline lets you name a parent segment, which
  is how you separate "what is common here" from "what this factor contributes":
  agentic AI vs corpus answers a different question from agentic AI vs all AI
  postings, and the paper must say which it used.
"""

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

ROOT = Path(__file__).parent
RUNS = ROOT / "RE-ANALYSIS-2026" / "pipeline_runs"
SEMESTERS = ["F2022", "W2023", "F2023", "W2024", "F2024", "F2025", "W2026"]


def load(sem):
    d = RUNS / sem
    M = pd.read_csv(d / "skill_presence_matrix.csv", index_col=0)
    a = None
    p = d / "posting_attributes.csv"
    if p.exists():
        a = pd.read_csv(p, low_memory=False)
        n = min(len(M), len(a))
        M, a = M.iloc[:n], a.iloc[:n].reset_index(drop=True)
    return M, a


def apply_where(attrs, clauses):
    """`col=value`, `col>=n`, `col!=value`, `col~substring` (case-insensitive)."""
    mask = np.ones(len(attrs), bool)
    for c in clauses:
        m = re.match(r"\s*(\w+)\s*(>=|<=|!=|=|~|>|<)\s*(.+?)\s*$", c)
        if not m:
            raise SystemExit(f"cannot parse --where {c!r}")
        col, op, val = m.groups()
        if col not in attrs.columns:
            raise SystemExit(f"no such column {col!r}; have: {list(attrs.columns)}")
        s = attrs[col]
        if op in (">=", "<=", ">", "<"):
            s = pd.to_numeric(s, errors="coerce")
            v = float(val)
            sub = {">=": s >= v, "<=": s <= v, ">": s > v, "<": s < v}[op]
        elif op == "~":
            sub = s.fillna("").astype(str).str.contains(val, case=False, regex=False)
        elif op == "!=":
            sub = s.astype(str) != val
        else:
            sub = s.astype(str) == val
        mask &= sub.fillna(False).values
    return mask


def fightin_words(seg_counts, base_counts, alpha0=None):
    """Monroe et al. (2008) log-odds ratio with an informative Dirichlet prior.

    The prior is the pooled corpus distribution, so a skill's estimate is pulled
    toward the corpus rate in proportion to how little evidence supports it.
    Returns a z-score: roughly ±1.96 is the conventional cutoff.
    """
    seg = seg_counts.astype(float)
    base = base_counts.astype(float)
    a0 = base if alpha0 is None else alpha0
    n_seg, n_base, n_a0 = seg.sum(), base.sum(), a0.sum()
    with np.errstate(divide="ignore", invalid="ignore"):
        lo_seg = np.log((seg + a0) / (n_seg + n_a0 - seg - a0))
        lo_base = np.log((base + a0) / (n_base + n_a0 - base - a0))
        delta = lo_seg - lo_base
        var = 1.0 / (seg + a0) + 1.0 / (base + a0)
        z = delta / np.sqrt(var)
    return np.nan_to_num(z)


def bh_fdr(p):
    """Benjamini-Hochberg. Returns q-values in the original order."""
    p = np.asarray(p, float)
    n = len(p)
    order = np.argsort(p)
    q = np.empty(n)
    prev = 1.0
    for rank in range(n - 1, -1, -1):
        i = order[rank]
        prev = min(prev, p[i] * n / (rank + 1))
        q[i] = prev
    return np.clip(q, 0, 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skill", help="segment = postings mentioning this skill")
    ap.add_argument("--where", action="append", default=[],
                    help="attribute filter, repeatable (AND). e.g. industry=Life Sciences")
    ap.add_argument("--baseline-where", action="append", default=[],
                    help="restrict the BASELINE too, to isolate one factor's contribution")
    ap.add_argument("--semesters", nargs="*", default=SEMESTERS)
    ap.add_argument("--min-count", type=int, default=25,
                    help="pre-specified independent filter (default 25)")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    if not args.skill and not args.where:
        raise SystemExit("need --skill and/or --where to define a segment")

    seg_tot = None
    base_tot = None
    n_seg = n_base = 0
    skills = None

    for sem in args.semesters:
        if not (RUNS / sem / "skill_presence_matrix.csv").exists():
            continue
        M, attrs = load(sem)
        P = M.values.astype(bool)
        if skills is None:
            skills = list(M.columns)
            seg_tot = np.zeros(len(skills), float)
            base_tot = np.zeros(len(skills), float)
        elif list(M.columns) != skills:
            M = M.reindex(columns=skills, fill_value=0)
            P = M.values.astype(bool)

        base_mask = np.ones(len(P), bool)
        if args.baseline_where:
            if attrs is None:
                raise SystemExit(f"{sem}: --baseline-where needs posting_attributes.csv")
            base_mask = apply_where(attrs, args.baseline_where)

        seg_mask = base_mask.copy()
        if args.where:
            if attrs is None:
                raise SystemExit(f"{sem}: --where needs posting_attributes.csv")
            seg_mask &= apply_where(attrs, args.where)
        if args.skill:
            hits = [s for s in skills if s.lower() == args.skill.lower()]
            if not hits:
                raise SystemExit(f"no canonical skill named {args.skill!r}")
            seg_mask &= P[:, skills.index(hits[0])]

        seg_tot += P[seg_mask].sum(0)
        base_tot += P[base_mask].sum(0)
        n_seg += int(seg_mask.sum())
        n_base += int(base_mask.sum())
        print(f"  {sem}: segment {int(seg_mask.sum()):,} / baseline {int(base_mask.sum()):,}",
              flush=True)

    if n_seg == 0:
        raise SystemExit("segment is empty")

    df = pd.DataFrame({"skill": skills, "n_seg": seg_tot, "n_base": base_tot})
    if args.skill:                      # the defining skill is in 100% of its own segment
        df = df[df.skill.str.lower() != args.skill.lower()]

    keep = df.n_seg >= args.min_count
    print(f"\nsegment {n_seg:,} postings | baseline {n_base:,} | "
          f"{int(keep.sum())} of {len(df)} skills pass n>={args.min_count}")
    df = df[keep].copy()
    if df.empty:
        raise SystemExit("no skills survive the minimum-count filter")

    df["p_seg"] = df.n_seg / n_seg
    df["p_base"] = df.n_base / n_base
    df["lift"] = np.where(df.p_base > 0, df.p_seg / df.p_base, np.nan)
    df["z"] = fightin_words(df.n_seg.values, df.n_base.values)
    df["p"] = [fisher_exact([[int(r.n_seg), n_seg - int(r.n_seg)],
                             [int(r.n_base - r.n_seg),
                              n_base - n_seg - int(r.n_base - r.n_seg)]],
                            alternative="greater")[1] for r in df.itertuples()]
    df["q"] = bh_fdr(df.p.values)
    df = df.sort_values("z", ascending=False)

    seg_name = (f"skill={args.skill}" if args.skill else "") + \
               ("" if not args.where else " ; " + " ; ".join(args.where))
    print(f"\n=== OVER-represented in [{seg_name}] ===")
    print(f"{'skill':38s} {'n':>6s} {'%seg':>6s} {'%base':>6s} {'lift':>6s} {'z':>7s} {'q':>8s}")
    for r in df.head(args.top).itertuples():
        print(f"  {r.skill[:36]:36s} {int(r.n_seg):6d} {100*r.p_seg:5.1f}% "
              f"{100*r.p_base:5.1f}% {r.lift:6.2f} {r.z:7.1f} {r.q:8.2g}")
    print(f"\n=== UNDER-represented ===")
    for r in df.tail(8).iloc[::-1].itertuples():
        print(f"  {r.skill[:36]:36s} {int(r.n_seg):6d} {100*r.p_seg:5.1f}% "
              f"{100*r.p_base:5.1f}% {r.lift:6.2f} {r.z:7.1f}")
    sig = int((df.q < 0.05).sum())
    print(f"\n{sig} of {len(df)} skills significant at FDR q<0.05")

    if args.out:
        df.to_csv(args.out, index=False)
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
