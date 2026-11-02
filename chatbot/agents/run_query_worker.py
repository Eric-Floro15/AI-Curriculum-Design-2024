"""run_query_worker.py — single-query worker, always launched as a fresh subprocess.

All alt-wave env vars MUST already be in the process environment before this
script is invoked, so every module-level singleton (LIFT_TABLE_FILE,
CLUSTER_RESULTS_FILE, FREQ_WAVE, …) is initialized from the correct source on
first import.  Never reload modules inside this script.

Usage (called by stage1_dry_runs.py / stage2_paid_runs.py):
    python run_query_worker.py --label LABEL --query-file PATH
    python run_query_worker.py --label LABEL --query TEXT

Exit codes:
    0  — preflight passed and run_query() succeeded
    2  — preflight failed (abort, no query run)
    1  — preflight passed but run_query() raised an exception

Preflight expected values
    W2026: Deep Learning→Tensorflow lift=8.752 z=8.32   FOCUSED={1,2,3,5,6}
           membership confidence "Agentic Ai" = 0.299
    F2022: Deep Learning→Tensorflow lift=6.468 z=14.16  FOCUSED={3,4,8,10}
           Deep Learning F2022 frequency ≈ 8.66 %
           membership confidence "Python" = 0.681
"""

import argparse
import math
import os
import sys
import time

_HERE        = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

# ── load .env before any project imports ─────────────────────────────────────
from dotenv import load_dotenv
load_dotenv(os.path.join(_CHATBOT_DIR, ".env"), override=False)

# abort on wrong provider
_PROVIDER = os.environ.get("LLM_PROVIDER", "")
if _PROVIDER == "openai":
    print("[ABORT] LLM_PROVIDER=openai — paid OpenAI call. Check .env.", flush=True)
    sys.exit(2)

# ── preflight constants ───────────────────────────────────────────────────────

_EXPECTED = {
    "W2026": {
        "focal":          "Deep Learning",
        "partner":        "Tensorflow",
        "lift":           8.752,
        "z":              8.32,
        "focused":        frozenset({1, 2, 3, 5, 6}),
        "dl_freq":        None,   # not checked for W2026
        "freq_wave":      "W2026",
        "mc_skill":       "Agentic Ai",
        "mc_conf":        0.299,
    },
    "F2022": {
        "focal":          "Deep Learning",
        "partner":        "Tensorflow",
        "lift":           6.468,
        "z":              14.16,
        "focused":        frozenset({3, 4, 8, 10}),
        "dl_freq":        8.658,  # ≈ 8.66 % — checked within ±0.05
        "freq_wave":      "F2022",
        "mc_skill":       "Python",
        "mc_conf":        0.681,
    },
}

# ── helpers ───────────────────────────────────────────────────────────────────

def _detect_wave() -> str:
    return "F2022" if os.environ.get("CLUSTER_RESULTS_FILE_OVERRIDE") else "W2026"


def _run_preflight(wave: str) -> bool:
    """Print resolved paths and assert data-integrity invariants.
    Returns True if all checks pass, False (and prints the failure) otherwise.
    """
    exp = _EXPECTED[wave]
    ok = True

    print(f"\n{'─'*64}")
    print(f"PREFLIGHT [{wave}]")
    print(f"{'─'*64}")

    # ── resolved paths ────────────────────────────────────────────────────────
    from tools.lift_tool    import LIFT_TABLE_FILE
    from tools.cluster_tool import CLUSTER_RESULTS_FILE, FREQ_WAVE, MEMBERSHIP_CONFIDENCE_FILE

    _freq_csv_override = os.environ.get("SKILL_FREQ_CSV_OVERRIDE")
    _freq_csv_default  = os.path.join(_CHATBOT_DIR, "data", "skill_frequency_by_semester.csv")
    freq_csv           = _freq_csv_override or _freq_csv_default

    mc_path = MEMBERSHIP_CONFIDENCE_FILE or "(not configured for this wave)"

    print(f"  CLUSTER_RESULTS_FILE : {CLUSTER_RESULTS_FILE}")
    print(f"  LIFT_TABLE_FILE      : {LIFT_TABLE_FILE}")
    print(f"  SKILL_FREQ_CSV       : {freq_csv}  [wave={FREQ_WAVE or '(none)'}]")
    print(f"  MEMBERSHIP_CONF_FILE : {mc_path}")

    # ── check 1: lift table — Deep Learning → Tensorflow ─────────────────────
    from tools.lift_tool import focal_associations
    assocs = focal_associations(exp["focal"], z_min=0.0)
    tf_row = next(
        (a for a in assocs if a.get("skill", "").lower() == exp["partner"].lower()),
        None,
    )
    if tf_row is None:
        print(f"\n  [FAIL] lift check: no '{exp['partner']}' row for focal '{exp['focal']}'")
        ok = False
    else:
        got_lift = float(tf_row.get("lift", 0))
        got_z    = float(tf_row.get("z", 0))
        match_l  = math.isclose(got_lift, exp["lift"], rel_tol=0.002)
        match_z  = math.isclose(got_z,   exp["z"],    rel_tol=0.002)
        icon_l   = "✓" if match_l else "✗"
        icon_z   = "✓" if match_z else "✗"
        print(f"\n  [{icon_l}] lift: got {got_lift}  expected {exp['lift']}")
        print(f"  [{icon_z}] z   : got {got_z}     expected {exp['z']}")
        if not (match_l and match_z):
            ok = False

    # ── check 2: FOCUSED_CLUSTERS ─────────────────────────────────────────────
    from tools.cluster_tool import FOCUSED_CLUSTERS
    match_fc = (FOCUSED_CLUSTERS == exp["focused"])
    print(f"\n  [{'✓' if match_fc else '✗'}] FOCUSED_CLUSTERS: got {sorted(FOCUSED_CLUSTERS)}"
          f"  expected {sorted(exp['focused'])}")
    if not match_fc:
        ok = False

    # ── check 3: Deep Learning frequency (F2022 only) ────────────────────────
    if exp["dl_freq"] is not None:
        import pandas as pd
        freq_df = pd.read_csv(freq_csv)
        rows = freq_df[freq_df["skill"].str.lower() == exp["focal"].lower()]
        if rows.empty or FREQ_WAVE not in freq_df.columns:
            print(f"\n  [✗] freq check: Deep Learning row not found in {freq_csv} wave={FREQ_WAVE}")
            ok = False
        else:
            got_freq = float(rows[FREQ_WAVE].values[0])
            match_f  = math.isclose(got_freq, exp["dl_freq"], rel_tol=0.002)
            print(f"\n  [{'✓' if match_f else '✗'}] Deep Learning freq ({FREQ_WAVE}):"
                  f" got {got_freq:.4f} %  expected ≈{exp['dl_freq']} %")
            if not match_f:
                ok = False

    # ── check 4: membership confidence ───────────────────────────────────────
    if exp.get("mc_skill"):
        import pandas as pd
        if not MEMBERSHIP_CONFIDENCE_FILE:
            print(f"\n  [✗] membership confidence: file not configured for {wave}")
            ok = False
        else:
            mc_df   = pd.read_csv(MEMBERSHIP_CONFIDENCE_FILE)
            mc_rows = mc_df[mc_df["Skill"].str.lower() == exp["mc_skill"].lower()]
            if mc_rows.empty:
                print(f"\n  [✗] membership confidence: '{exp['mc_skill']}' not found")
                ok = False
            else:
                got_mc   = float(mc_rows["membership_confidence"].values[0])
                match_mc = math.isclose(got_mc, exp["mc_conf"], rel_tol=0.002)
                print(f"\n  [{'✓' if match_mc else '✗'}] membership confidence"
                      f" '{exp['mc_skill']}': got {got_mc:.3f}  expected {exp['mc_conf']}")
                if not match_mc:
                    ok = False

    print(f"\n  {'PREFLIGHT PASS ✓' if ok else 'PREFLIGHT FAIL ✗ — aborting'}")
    print(f"{'─'*64}\n")
    return ok


def _list_run_records() -> set[str]:
    from agents.orchestrator import _RUN_RECORDS_DIR
    try:
        return set(os.listdir(_RUN_RECORDS_DIR))
    except FileNotFoundError:
        return set()


def _relabel(before: set[str], after: set[str], label: str) -> list[str]:
    from agents.orchestrator import _RUN_RECORDS_DIR
    new     = sorted(after - before)
    renamed = []
    for fname in new:
        nf = fname.replace("_success", f"_{label}_success").replace(
             "_failure", f"_{label}_failure")
        src = os.path.join(_RUN_RECORDS_DIR, fname)
        dst = os.path.join(_RUN_RECORDS_DIR, nf)
        os.rename(src, dst)
        renamed.append(dst)
    return renamed


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label",          required=True)
    parser.add_argument("--query",          default=None)
    parser.add_argument("--query-file",     default=None)
    parser.add_argument("--skip-preflight", action="store_true")
    parser.add_argument("--preflight-only", action="store_true",
                        help="Run preflight then exit; do NOT call the model.")
    args = parser.parse_args()

    wave = _detect_wave()
    print(f"[worker] label={args.label}  wave={wave}  provider={_PROVIDER}", flush=True)

    # --preflight-only: no query needed, no model call
    if args.preflight_only:
        passed = _run_preflight(wave)
        sys.exit(0 if passed else 2)

    if args.query_file:
        with open(args.query_file, encoding="utf-8") as fh:
            query = fh.read().strip()
    elif args.query:
        query = args.query
    else:
        print("[ABORT] --query or --query-file required", flush=True)
        sys.exit(2)

    if not args.skip_preflight:
        if not _run_preflight(wave):
            sys.exit(2)

    from agents.orchestrator import run_query
    before = _list_run_records()
    t0     = time.time()
    error  = None
    try:
        answer  = run_query(query)
        elapsed = time.time() - t0
        status  = "success"
    except Exception as exc:
        elapsed = time.time() - t0
        status  = "failure"
        answer  = None
        error   = f"{type(exc).__name__}: {exc}"
        print(f"\n[ERROR] {error}", flush=True)

    after   = _list_run_records()
    renamed = _relabel(before, after, args.label)

    print(f"\n[{status.upper()}] wall={elapsed:.0f}s", flush=True)
    for p in renamed:
        print(f"  record: {p}", flush=True)

    sys.exit(0 if status == "success" else 1)


if __name__ == "__main__":
    main()
