#!/usr/bin/env python3
"""Golden-test the deck linter (the /eval-run self-test pattern).

Each known-bad fixture MUST be caught by its target rule; the golden reference
deck MUST pass with 0 errors. This keeps the linter honest — if someone weakens a
rule, the matching fixture stops failing and this test goes red. Exit non-zero on
any mismatch. Stdlib only.
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = ROOT.parent
LINT = SKILL / "scripts" / "lint_deck.py"
GOLDEN = SKILL / "templates" / "reference-deck.html"

# (fixture, expected_rule)  — expected_rule None means "golden: must pass (0 errors)"
CASES = [
    (ROOT / "decks" / "bad-fake-data.html", "fake-data"),
    (ROOT / "decks" / "bad-slop-color.html", "slop-color"),
    (ROOT / "decks" / "bad-external.html", "not-self-contained"),
    (GOLDEN, None),
]


def run_lint(deck: Path) -> dict:
    out = subprocess.run([sys.executable, str(LINT), str(deck), "--json"],
                         capture_output=True, text=True)
    return json.loads(out.stdout)


def main() -> int:
    ok = True
    for deck, expect in CASES:
        if not deck.is_file():
            print(f"FAIL  | missing fixture {deck}")
            ok = False
            continue
        r = run_lint(deck)
        rules = {f["rule"] for f in r["findings"]}
        if expect is None:
            good = r["errors"] == 0
            print(f"{'PASS' if good else 'FAIL'}  | golden  | {deck.name:24} | errors={r['errors']}")
        else:
            good = expect in rules
            print(f"{'PASS' if good else 'FAIL'}  | catch[{expect:18}] | {deck.name:24} | rules={sorted(rules)}")
        ok = ok and good
    print("\nrun_evals:", "ALL CORRECT (linter is honest)" if ok else "MISMATCH — a rule regressed")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
