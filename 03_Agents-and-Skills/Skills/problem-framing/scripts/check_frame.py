#!/usr/bin/env python3
"""
check_frame.py — validate a Problem Frame artifact from disk.

Bundled with the `problem-framing` skill. Author-time, single-file counterpart to the
skill's `lints[]`. Pure standard library — no PyYAML.

A Problem Frame is the pre-research gate into Understand. This checker recomputes its
validity from the file (verification, never self-report):

  - solution-noun-in-problem-statement → the Problem statement names a solution         (warning)
        (agent/dashboard/ontology/platform/app/model/copilot/tool/portal) instead of a
        people-problem. "No solution yet — let's talk about the problem."
  - missing-decisions-to-enable        → no 'Decisions to enable' section               (error)
  - missing-feasibility-gap            → no 'Feasibility gap' section                    (error)
  - missing-readiness-light            → no closing `light: green|yellow|red`            (error)
  - yellow-readiness-without-trigger   → a 🟡 readiness with no trigger+expiry            (error)

Usage:
    python check_frame.py <problem-frame.md-or-folder> [...]

Exit codes:
    0  valid   1  invalid   2  bad args / no frame found
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SOLUTION_NOUN = re.compile(
    r"\b(agent|dashboard|ontology|platform|app|application|model|copilot|tool|portal|"
    r"chatbot|plugin|widget|pipeline|API|webapp)\b", re.I)
# A solution noun is NOT a violation when it is negated, quoted, or disclaimed — a good
# frame often says "this is NOT a missing-tool problem" or "(not yet 'an agent')". We test
# each sentence: if it carries a negation/disclaimer cue, its solution nouns are exempt.
NEGATION_CUE = re.compile(
    r"\b(not|no|isn'?t|aren'?t|never|rather than|instead of|not yet|"
    r"missing-\w+|no solution)\b", re.I)
LIGHT = re.compile(r"(?im)^\s*light:\s*(green|yellow|red)\b")
TRIGGER = re.compile(r"(?im)^\s*trigger:\s*\S")
EXPIRY = re.compile(r"(?im)^\s*expiry:\s*\d{4}-\d{2}-\d{2}")


def _split_sentences(s: str) -> list[str]:
    # split on sentence terminators AND on parenthetical/quote boundaries so a
    # disclaimer clause is judged on its own (negation scopes to its clause)
    parts = re.split(r"(?<=[.!?])\s+|(?=\()|(?<=\))|(?=\u2014)|(?=—)", s)
    return [p for p in parts if p and p.strip()]


def _names_real_solution(text: str) -> str | None:
    """Return the first solution noun used AS a proposal (not negated/quoted), else None."""
    for sentence in _split_sentences(text):
        # strip quoted spans — quoted nouns ('an agent') are illustrative, not proposed
        unquoted = re.sub(r"['\"\u2018\u2019\u201c\u201d][^'\"\u2018\u2019\u201c\u201d]*['\"\u2018\u2019\u201c\u201d]", "", sentence)
        m = SOLUTION_NOUN.search(unquoted)
        if m and not NEGATION_CUE.search(sentence):
            return m.group(1)
    return None


def section_body(text: str, header_rx: str) -> str | None:
    """Return the body of a `## <header>` section (until the next `##`), or None."""
    m = re.search(rf"(?im)^#{{1,4}}\s*{header_rx}.*$", text)
    if not m:
        return None
    start = m.end()
    nxt = re.search(r"(?m)^#{1,4}\s", text[start:])
    return text[start: start + nxt.start()] if nxt else text[start:]


def check_file(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return [f"cannot read: {e}"]

    fails: list[str] = []

    # problem statement must not name a solution
    ps = section_body(text, r"problem statement")
    if ps is None:
        fails.append("no '## Problem statement' section")
    else:
        noun = _names_real_solution(ps)
        if noun:
            fails.append(f"Problem statement names a solution ('{noun}') — "
                         "describe the people-problem / the decision they can't make, not the build")

    if not re.search(r"(?i)decisions to enable", text):
        fails.append("missing 'Decisions to enable' — design backward from the decision, not the feature")
    if not re.search(r"(?i)feasibility gap", text):
        fails.append("missing 'Feasibility gap' — name what's wanted vs achievable (the Venn center)")

    lm = LIGHT.search(text)
    if not lm:
        fails.append("no readiness Traffic Light (`light: green|yellow|red`) — "
                     "is the problem grounded enough to enter research?")
    elif lm.group(1).lower() == "yellow":
        if not TRIGGER.search(text):
            fails.append("🟡 readiness without `trigger:` — a green in hiding or a red in denial")
        if not EXPIRY.search(text):
            fails.append("🟡 readiness without ISO `expiry:` — name the date the trigger must fire by")

    return fails


def iter_frames(target: Path):
    if target.is_file():
        yield target
    elif target.is_dir():
        # prefer the canonical *-problem-frame.md naming; fall back to any md with the section
        named = sorted(target.rglob("*problem-frame*.md"))
        if named:
            yield from named
        else:
            yield from sorted(target.rglob("*.md"))


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("-")]
    if not args:
        print("Usage: python check_frame.py <problem-frame.md-or-folder> [...]", file=sys.stderr)
        return 2

    targets: list[Path] = []
    for a in args:
        p = Path(a)
        if p.exists():
            targets.extend(iter_frames(p))
        else:
            print(f"warning: not found: {a}", file=sys.stderr)

    checked = invalid = 0
    for path in targets:
        try:
            head = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        # only treat files that look like a problem frame
        if "problem-frame" not in path.name.lower() and not re.search(r"(?i)problem statement", head):
            continue
        checked += 1
        fails = check_file(path)
        if fails:
            invalid += 1
            print(f"✗ {path}")
            for f in fails:
                print(f"    - {f}")
        else:
            print(f"✓ {path}")

    if checked == 0:
        print("no Problem Frame found (looked for *-problem-frame.md or a '## Problem statement')", file=sys.stderr)
        return 2
    print(f"\n{checked} frame(s) · {checked - invalid} valid · {invalid} invalid")
    return 1 if invalid else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
