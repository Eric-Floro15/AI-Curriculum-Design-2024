"""stage0_v62_dry_runs.py — Stage 0 of the v62 pilot (free, dev lane).

Runs query Q-scratch twice through run_sa_worker.py in fresh subprocesses:
  1. SA_PROCEDURE=structured  label: v62pilot-dry-sa-structured
  2. SA_PROCEDURE=plain        label: v62pilot-dry-sa-plain

Dev lane: LLM_PROVIDER and LLM_MODEL are taken from .env (expected:
ollama-cloud / gpt-oss:120b).  No Anthropic calls.  Exit 2 if provider
would be openai.

Usage:
    KMP_DUPLICATE_LIB_OK=TRUE python chatbot/agents/stage0_v62_dry_runs.py
"""  # v62 pilot:

import os
import subprocess
import sys
import time

_HERE        = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)

# Q-scratch — identical to the Stage 1 query in the prompt
_QUERY = (
    "Design a graduate AI/ML curriculum of about 8-10 courses grounded in "
    "the most recent wave of labour-market demand. Use the demand skill "
    "clusters as the backbone, and for each course give a title, the "
    "cluster(s) and key skills it covers, and a brief rationale grounded "
    "in how distinctively those skills are demanded."
)

_RUNS = [
    {"sa_procedure": "structured", "label": "v62pilot-dry-sa-structured"},
    {"sa_procedure": "plain",      "label": "v62pilot-dry-sa-plain"},
]


def _run_one(sa_procedure: str, label: str) -> int:
    """Spawn a fresh subprocess for one SA run. Returns the exit code."""
    env = os.environ.copy()
    env["SA_PROCEDURE"] = sa_procedure

    cmd = [
        sys.executable,
        os.path.join(_HERE, "run_sa_worker.py"),
        "--label", label,
        "--query", _QUERY,
    ]
    print(f"\n{'='*70}")
    print(f"[stage0] SA_PROCEDURE={sa_procedure!r}  label={label!r}")
    print(f"{'='*70}\n", flush=True)

    t0 = time.time()
    result = subprocess.run(cmd, env=env)
    elapsed = time.time() - t0
    print(f"\n[stage0] Exit code: {result.returncode}  wall time: {elapsed:.1f}s", flush=True)
    return result.returncode


def main() -> None:
    outcomes = []
    for run in _RUNS:
        rc = _run_one(run["sa_procedure"], run["label"])
        outcomes.append((run["label"], rc))

    print(f"\n{'='*70}")
    print("STAGE 0 SUMMARY")
    print(f"{'='*70}")
    all_ok = True
    for label, rc in outcomes:
        status = "OK" if rc == 0 else f"FAIL (exit {rc})"
        print(f"  {label}: {status}")
        if rc != 0:
            all_ok = False
    print()
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
