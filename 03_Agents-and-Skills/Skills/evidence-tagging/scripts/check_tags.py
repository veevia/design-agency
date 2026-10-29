#!/usr/bin/env python3
"""
check_tags.py — validate evidence tagging on a wiki page or artifact, from disk.

Bundled with the `evidence-tagging` skill. The author-time, single-file counterpart
to the workspace-wide `lints[]` that `lint-skill.py` runs. Pure standard library —
no PyYAML — so it runs anywhere with `python3`.

Rules (from 00_README/_frameworks/house-principles.md §4 and the skill's lints[]):
  - untagged claim bullet      → a bullet asserting a fact with no [observed|reported|assumed] tag
  - observed-without-source    → `[observed]` with no `| <source-slug>`
  - assumed-without-test       → `[assumed]` at end of line with no test/follow-up
  - single-source observed     → `[observed | n=1 ...]` or a lone observed on a one-source page (info)

A page that declares `evidence-default:` in front-matter has set its evidence class at
the page level — its untagged bodies and bare [observed] inherit that provenance, so
they are NOT flagged (mirrors the skill's `skip_if_frontmatter: [evidence-default]`).

This is a PRAGMATIC author-time heuristic. The authoritative, exclude-calibrated check
is `lint-skill.py evidence-tagging` across the whole hub. Use this to catch the obvious
misses while you write, then run the real lint before commit.

Usage:
    python check_tags.py <file-or-folder> [...]
    python check_tags.py --quiet <folder>     # only failures + summary

Exit codes:
    0  no errors (warnings/info may still print)   1  one or more errors   2  bad args
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TAG = re.compile(r"\[(observed|reported|assumed)\b")
OBSERVED = re.compile(r"\[observed\b")
OBSERVED_WITH_SOURCE = re.compile(r"\[observed\s*\|[^\]]+\]")
ASSUMED_EOL = re.compile(r"\[assumed\]\s*$")
SINGLE_SOURCE = re.compile(r"\[observed\s*\|\s*n=1\b")

# Lines that match "looks like a bullet" but are NOT claims — keep in sync with the
# skill's `exclude` regex (pragmatic subset: the high-frequency structural rows).
NOT_A_CLAIM = re.compile(
    r"\[\[|\]\(|\?\s*$|\[open\]\s*$"                       # links, questions, open markers
    r"|^-\s*\*\*[^*]+:\*\*"                                  # - **Key:** metadata rows
    r"|^-\s*_[^_]+_\s*$"                                     # - _italic note_
    r"|^-\s*(Created|Updated|Deleted|Raw file|Date range|Type|Source|Sources|Owner|"
    r"Status|Inputs|Outputs|Used by|Consumed by|Feeds|Pairs with|Part of|Member|"
    r"Consumes|Hands off|Produces|Tags|Related):"           # relationship/metadata keys
    r"|^-\s*Open:\s|^-\s*Q\d+\b"                             # question register
)


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict = {}
    for line in text[3:end].splitlines():
        if not line.strip() or line[0] in " \t#":
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            out[m.group(1).lower()] = m.group(2).strip()
    return out


def split_body(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


def check_file(path: Path) -> tuple[list[str], list[str]]:
    """Return (errors, warnings)."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return [f"cannot read: {e}"], []

    fm = parse_frontmatter(text)
    page_default = bool(fm.get("evidence-default"))
    body = split_body(text)
    errors: list[str] = []
    warnings: list[str] = []

    in_fence = False
    for i, raw in enumerate(body.splitlines(), 1):
        line = raw.rstrip("\n")
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        # observed-without-source (skip if page sets evidence-default)
        if OBSERVED.search(line) and not OBSERVED_WITH_SOURCE.search(line) and not page_default:
            errors.append(f"L{i}: `observed` without a source — use `[observed | <slug>]`: {line.strip()[:70]}")

        # assumed-without-test (warning)
        if ASSUMED_EOL.search(line):
            warnings.append(f"L{i}: `[assumed]` with no test/follow-up — name the cheapest test: {line.strip()[:70]}")

        # single-source observed (info-as-warning)
        if SINGLE_SOURCE.search(line):
            warnings.append(f"L{i}: single-source `observed` (n=1) — consider softening to `reported`: {line.strip()[:70]}")

        # untagged claim bullet (skip if page sets evidence-default)
        if not page_default and re.match(r"^\s*-\s+\S", line):
            stripped = line.strip()
            content = re.sub(r"^-\s+", "", stripped)
            if (len(content) >= 20 and not TAG.search(line)
                    and not NOT_A_CLAIM.search(stripped)):
                errors.append(f"L{i}: claim bullet without an evidence tag: {content[:70]}")

    if page_default and not fm.get("sources") and fm.get("evidence-default") != "assumed":
        warnings.append("page sets evidence-default but lists no `sources:` "
                        "(ok only for `type: source` self-citing pages)")
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
        print("Usage: python check_tags.py <file-or-folder> [...]", file=sys.stderr)
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
                print(f"    warn  {w}")
        elif warnings:
            warn_only += 1
            if not quiet:
                print(f"⚠ {path}")
                for w in warnings:
                    print(f"    warn  {w}")
        elif not quiet:
            print(f"✓ {path}")

    if checked == 0:
        print("no markdown files found", file=sys.stderr)
        return 2
    print(f"\n{checked} file(s) · {checked - err_files - warn_only} clean · "
          f"{warn_only} warn-only · {err_files} with errors")
    return 1 if err_files else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
