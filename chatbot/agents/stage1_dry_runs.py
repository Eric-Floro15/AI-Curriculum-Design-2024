"""stage1_dry_runs.py — Part C Stage 1: five dev-lane dry runs.

v2 (2026-11-02): each query runs in its own fresh subprocess via
run_query_worker.py, so module-level singletons (LIFT_TABLE_FILE,
CLUSTER_RESULTS_FILE, …) are always initialized from the correct env.
The F2022 run passes F2022 overrides to the subprocess env.
Each subprocess runs an in-process preflight before calling run_query().

Usage (from repo root):
    python chatbot/agents/stage1_dry_runs.py            # all 5
    python chatbot/agents/stage1_dry_runs.py --only v60dry-A2-F2022

Labels: v60dry-A2-W2026, v60dry-A2-F2022, v60dry-MMAI,
        v60dry-agentic, v60dry-finance
"""

import argparse
import os
import subprocess
import sys
import tempfile
import time

_HERE         = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR  = os.path.dirname(_HERE)
_PROJECT_ROOT = os.path.dirname(_CHATBOT_DIR)   # parent of chatbot/ — relative env-var paths resolve here
_WORKER       = os.path.join(_HERE, "run_query_worker.py")

# Use the venv Python that has all dependencies
_VENV_PYTHON = os.path.join(_CHATBOT_DIR, ".venv", "Scripts", "python.exe")
if not os.path.exists(_VENV_PYTHON):
    _VENV_PYTHON = sys.executable  # fallback

# ── F2022 env overrides ───────────────────────────────────────────────────────
_F2022_ENV = {
    "CLUSTER_RESULTS_FILE_OVERRIDE":
        "chatbot/data/alt_wave_F2022/clust_ensembled_results_F2022.csv",
    "LIFT_TABLE_FILE_OVERRIDE":
        "chatbot/data/alt_wave_F2022/skill_lift_table_F2022.csv",
    "FREQ_WAVE_OVERRIDE": "F2022",
    "DATA_WAVE_LABEL": "Fall 2022 (F2022)",
    "MEMBERSHIP_CONFIDENCE_FILE_OVERRIDE":
        "chatbot/data/alt_wave_F2022/cluster_membership_confidence_F2022.csv",
    "CLUSTER_THEMES_OVERRIDE_JSON": (
        '{"1": "Life Sciences & Clinical Research", '
        '"2": "Emerging Niche AI Tooling & Health Informatics '
        '(near-zero frequency in Fall 2022)", '
        '"3": "Deep Learning, Computer Vision & ML Engineering", '
        '"4": "Python, Machine Learning, Data Science & Statistics", '
        '"5": "Data Storytelling, Analytics & Business Intelligence", '
        '"6": "Strategy, Consulting & Customer-Facing Business", '
        '"7": "Business Analysis, Requirements & Office Tools", '
        '"8": "SQL Databases, BI Tools & Data Management", '
        '"9": "Niche Engineering & Software Terms (heterogeneous)", '
        '"10": "Data Engineering, Cloud & Software Development"}'
    ),
}

# ── queries ───────────────────────────────────────────────────────────────────
Q_A2 = (
    "Design a graduate AI/ML curriculum of about 8-10 courses grounded in "
    "the most recent wave of labour-market demand. Use the demand skill "
    "clusters as the backbone, and for each course give a title, the "
    "cluster(s) and key skills it covers, and a brief rationale grounded in "
    "how distinctively those skills are demanded."
)
Q_MMAI = (
    "Compare the Queen's MMAI programme against current labour-market demand: "
    "which in-demand skills does it cover, which is it missing, and which of "
    "its topics look weakly supported by current demand?"
)
Q_AGENTIC = (
    "I'm updating my AI/ML Master's curriculum and want to know whether "
    "agentic AI warrants its own dedicated course rather than a module inside "
    "the existing machine-learning course. Using the market data: which skills "
    "are most distinctively in demand for agentic AI (report lift and "
    "statistical significance, not just raw frequency); which existing "
    "analyst/BI-oriented skills is agentic AI actually not associated with; "
    "how do peer programs currently cover agentic AI; and what recent industry "
    "developments should shape the course? Give concrete, grounded "
    "recommendations."
)
Q_FIN = (
    "Design a finance-focused AI/ML Master's curriculum grounded in the "
    "market data. Cover both the core agentic-AI skills every such program "
    "needs and the finance-specific skills this sector distinctively demands. "
    "Report lift and statistical significance (z) for the skills you cite, "
    "and give concrete course recommendations."
)
# ── §4.6 re-run queries (v60 Part D, 2026-11-03) ─────────────────────────────
Q_SECTOR = (
    "Using the sector-specific demand analysis, what agentic-AI skills are "
    "distinctively in demand for finance roles versus healthcare roles? For "
    "each sector, show the shared core skills and the sector-specific "
    "additions, and state whether that sector sits at, above, or below the "
    "overall market rate for agentic AI."
)
Q_AGENTIC_CL = (
    "We're considering how to teach agentic AI. Based on current "
    "labour-market demand, what skills most distinguish agentic-AI roles "
    "from AI roles generally, and should agentic AI be its own course or "
    "folded into an existing machine-learning or cloud/DevOps course?"
)

# (label, query, use_f2022)
RUNS = [
    ("v60dry-A2-W2026",   Q_A2,         False),
    ("v60dry-A2-F2022",   Q_A2,         True),
    ("v60dry-MMAI",       Q_MMAI,       False),
    ("v60dry-agentic",    Q_AGENTIC,    False),
    ("v60dry-finance",    Q_FIN,        False),
    # Part D additions:
    ("v60dry-sector",     Q_SECTOR,     False),
    ("v60dry-agentic-cl", Q_AGENTIC_CL, False),
]


# ── subprocess runner ─────────────────────────────────────────────────────────

def _run_one(label: str, query: str, use_f2022: bool,
             preflight_only: bool = False) -> bool:
    """Spawn a fresh Python process for one query. Returns True on success."""
    mode = "PREFLIGHT-ONLY" if preflight_only else ("F2022" if use_f2022 else "W2026")
    print(f"\n{'='*72}")
    print(f"RUN: {label}  [{mode}]")
    print(f"{'='*72}\n")

    # Build env for the subprocess
    env = os.environ.copy()
    env["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    env["PYTHONIOENCODING"] = "utf-8"
    if use_f2022:
        env.update(_F2022_ENV)
    else:
        # Ensure no stale overrides leak in (shouldn't happen, but be explicit)
        for k in _F2022_ENV:
            env.pop(k, None)

    cmd = [_VENV_PYTHON, _WORKER, "--label", label]
    if preflight_only:
        cmd.append("--preflight-only")
    else:
        # Write query to a temp file (avoids Windows command-line length limit)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                         delete=False, encoding="utf-8") as tf:
            tf.write(query)
            query_file = tf.name
        cmd += ["--query-file", query_file]

    try:
        t0     = time.time()
        result = subprocess.run(cmd, env=env, cwd=_PROJECT_ROOT)
        elapsed = time.time() - t0
        success = (result.returncode == 0)
        print(f"\n[{'OK' if success else 'FAIL'}] {label}  exit={result.returncode}  "
              f"wall={elapsed:.0f}s")
        return success
    finally:
        if not preflight_only:
            try:
                os.unlink(query_file)
            except (OSError, UnboundLocalError):
                pass


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", default=None,
                        help="Run only the run with this label.")
    parser.add_argument("--preflight-only", action="store_true",
                        help="Run preflight for each run then exit; no model calls.")
    args = parser.parse_args()

    runs_to_do = [r for r in RUNS if args.only is None or r[0] == args.only]
    if not runs_to_do:
        print(f"[ERROR] --only={args.only!r} did not match any label.")
        sys.exit(1)

    results = []
    for label, query, use_f2022 in runs_to_do:
        success = _run_one(label, query, use_f2022,
                           preflight_only=args.preflight_only)
        results.append((label, success))
        if not success:
            print(f"\n[ABORT] {label} failed preflight. Stopping.")
            break

    title = "PREFLIGHT SUMMARY" if args.preflight_only else "STAGE 1 SUMMARY"
    print(f"\n{'='*72}")
    print(title)
    print(f"{'='*72}")
    for label, ok in results:
        print(f"  {'✓' if ok else '✗'}  {label}")
    print()


if __name__ == "__main__":
    main()
