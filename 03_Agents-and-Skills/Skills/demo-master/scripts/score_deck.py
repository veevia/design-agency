#!/usr/bin/env python3
"""score_deck — run the deterministic demo-master gates on a built deck and emit a
combined verdict: static lint (lint_deck.py) + headless runtime (check_runtime.py).

The taste rows (narrative fit, metaphor coherence, "feels physical") are NOT scored
here on purpose — they're the agent-evaluated prose rubric (references/rubric.md).
This tool covers exactly the deterministic ~70%.

Usage:
    python3 score_deck.py <url-or-file> [--no-runtime]
"""
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def main() -> int:
    ap = argparse.ArgumentParser(description="Combined lint + runtime gate for a built deck.")
    ap.add_argument("deck", help="served URL or path to a self-contained deck")
    ap.add_argument("--no-runtime", action="store_true", help="static lint only (skip headless Chrome)")
    args = ap.parse_args()

    print("== static lint ==")
    rc_lint, out_lint = run([sys.executable, str(HERE / "lint_deck.py"), args.deck])
    print(out_lint)

    rc_run = 0
    if args.no_runtime:
        print("\n== runtime == skipped (--no-runtime)")
        run_state = "skip"
    else:
        print("\n== runtime ==")
        rc_run, out_run = run([sys.executable, str(HERE / "check_runtime.py"), args.deck])
        print(out_run)
        run_state = "ok" if rc_run == 0 else "FAIL"

    verdict = "PASS" if (rc_lint == 0 and rc_run == 0) else "FAIL"
    print(f"\nscore_deck: lint={'ok' if rc_lint == 0 else 'FAIL'}  runtime={run_state}  ->  {verdict}")
    print("(taste rows — narrative / metaphor / engagement — are the agent's prose rubric, not scored here)")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
