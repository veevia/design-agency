#!/usr/bin/env python3
"""
check_clarity.py — validate the extreme-clarity bar on a page, from disk.

Bundled with the `extreme-clarity` skill. Author-time, single-file counterpart to the
skill's workspace-wide `lints[]`. Pure standard library — no PyYAML.

Rules (from 00_README/_frameworks/extreme-clarity.md and the skill's lints[]):
  - missing-tldr        → a page with an `# H1` but no `**TL;DR:**` slot          (error)
  - tldr-too-long       → the TL;DR sentence runs > 25 words                       (warning)
  - tldr-not-early      → `**TL;DR:**` appears after the first 250 body chars       (warning)
  - adjective-magnitude → many|several|various|significant|soon|fast|slow|small|   (info)
                          large|few|huge|tiny used with NO number on the line
  - throat-clearing     → opens with "This document describes…" / "It's important   (warning)
                          to note…" / "In the future…" with no date

Usage:
    python check_clarity.py <file-or-folder> [...]
    python check_clarity.py --quiet <folder>

Exit codes:
    0  no errors   1  one or more errors   2  bad args
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TLDR = re.compile(r"\*\*TL;DR:?\*\*\s*(.+)")
ADJ = re.compile(r"\b(many|several|various|significant|soon|fast|slow|small|large|few|huge|tiny|numerous|substantial)\b", re.I)
HAS_NUMBER = re.compile(r"\d|\bone\b|\btwo\b|\bthree\b|\bzero\b", re.I)
THROAT = re.compile(r"^\s*(this (document|page|section|skill|file)\s+(describes|covers|explains|outlines)|"
                    r"it'?s important to note|there are (many|several)|in the future\b(?!.*\d{4})|"
                    r"we should consider)", re.I)
SENTENCE_END = re.compile(r"[.!?]")


def split_body(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


def first_sentence(s: str) -> str:
    m = SENTENCE_END.search(s)
    return s[: m.end()] if m else s


def check_file(path: Path) -> tuple[list[str], list[str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return [f"cannot read: {e}"], []

    body = split_body(text)
    errors: list[str] = []
    warnings: list[str] = []

    has_h1 = bool(re.search(r"^#\s", body, re.M))
    tldr_m = TLDR.search(body)

    # missing-tldr (only enforce on pages that have an H1 title — i.e. real pages)
    if has_h1 and not tldr_m:
        errors.append("no `**TL;DR:**` slot — every page needs a one-sentence conclusion-first TL;DR")

    if tldr_m:
        # tldr-not-early: where does the TL;DR sit relative to body start?
        if tldr_m.start() > 250:
            warnings.append(f"`**TL;DR:**` appears {tldr_m.start()} chars into the body — move it to the top")
        # tldr-too-long: first sentence > 25 words
        sentence = first_sentence(tldr_m.group(1).strip())
        words = len(sentence.split())
        if words > 25:
            warnings.append(f"TL;DR first sentence is {words} words (>25) — trim: {sentence[:60]}…")

    in_fence = False
    for i, raw in enumerate(body.splitlines(), 1):
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not line:
            continue
        if THROAT.search(line):
            warnings.append(f"L{i}: throat-clearing opener — start with the conclusion: {line[:60]}")
        am = ADJ.search(line)
        if am and not HAS_NUMBER.search(line):
            errors_or_info = warnings  # treat as advisory (info-grade)
            errors_or_info.append(f"L{i}: adjective magnitude '{am.group(1)}' with no number — quantify it: {line[:55]}")

    return errors, warnings


def iter_md(target: Path):
    if target.is_file():
        yield target
    elif target.is_dir():
        yield from sorted(target.rglob("*.md"))


def main(argv: list[str]) -> int:
    quiet = "--quiet" in argv
    args = [a for a in argv if not a.startswith("-")]
    if not args:
        print("Usage: python check_clarity.py <file-or-folder> [...]", file=sys.stderr)
        return 2

    targets: list[Path] = []
    for a in args:
        p = Path(a)
        if p.exists():
            targets.extend(iter_md(p))
        else:
            print(f"warning: not found: {a}", file=sys.stderr)

    checked = err_files = warn_only = 0
    for path in targets:
        errors, warnings = check_file(path)
        checked += 1
        if errors:
            err_files += 1
            print(f"✗ {path}")
            for e in errors:
                print(f"    ERROR {e}")
            for w in warnings:
                print(f"    note  {w}")
        elif warnings:
            warn_only += 1
            if not quiet:
                print(f"⚠ {path}")
                for w in warnings:
                    print(f"    note  {w}")
        elif not quiet:
            print(f"✓ {path}")

    if checked == 0:
        print("no markdown files found", file=sys.stderr)
        return 2
    print(f"\n{checked} file(s) · {checked - err_files - warn_only} clean · "
          f"{warn_only} note-only · {err_files} missing TL;DR")
    return 1 if err_files else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
