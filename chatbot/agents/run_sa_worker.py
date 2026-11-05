"""run_sa_worker.py — single-query SA worker, always launched as a fresh subprocess.

SA_PROCEDURE is read at module import (via single_agent.py), so it must already
be set in the process environment before this script starts.  The caller
(stage0_v62_dry_runs.py / stage1 scripts) sets it via subprocess env.

Usage:
    python run_sa_worker.py --label LABEL --query TEXT
    python run_sa_worker.py --label LABEL --query-file PATH

Exit codes:
    0  — preflight passed and run_query_single() succeeded
    2  — preflight failed or provider is openai (abort, no query run)
    1  — preflight passed but run_query_single() raised an exception
"""  # v62 pilot:

import argparse
import os
import sys

_HERE        = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)

# ── load .env before any project imports ─────────────────────────────────────
from dotenv import load_dotenv
load_dotenv(os.path.join(_CHATBOT_DIR, ".env"), override=False)

# abort on openai provider — paid call we never want to make by accident
_PROVIDER = os.environ.get("LLM_PROVIDER", "")
if _PROVIDER == "openai":
    print("[ABORT] LLM_PROVIDER=openai — this would be a paid OpenAI call. "
          "Check .env or env override.", flush=True)
    sys.exit(2)

print(f"[run_sa_worker] LLM_PROVIDER={_PROVIDER}  "
      f"LLM_MODEL={os.environ.get('LLM_MODEL', '(unset)')}  "
      f"SA_PROCEDURE={os.environ.get('SA_PROCEDURE', 'plain')}", flush=True)


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Single-query SA worker for v62 pilot runs."
    )
    parser.add_argument("--label", default="", help="Run-record label (embedded in filename).")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--query", help="Query text (inline).")
    group.add_argument("--query-file", help="Path to a file whose contents are the query.")
    args = parser.parse_args()

    if args.query_file:
        with open(args.query_file, encoding="utf-8") as f:
            query = f.read().strip()
    else:
        query = args.query

    # Import after .env is loaded and SA_PROCEDURE is confirmed in env.
    # SA_PROCEDURE is read at single_agent import time, so this order matters.
    from agents.single_agent import _run_sa_preflight, run_query_single  # noqa: E402

    # Preflight runs again inside run_query_single; this call lets us exit 2
    # (clean abort) rather than raising a RuntimeError.
    if not _run_sa_preflight():
        print("[ABORT] SA preflight failed.", flush=True)
        sys.exit(2)

    try:
        answer = run_query_single(query, label=args.label)
        print(f"\n[run_sa_worker] Done — label={args.label!r}", flush=True)
        print(answer)
    except Exception as exc:
        print(f"[run_sa_worker] EXCEPTION: {exc}", flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
