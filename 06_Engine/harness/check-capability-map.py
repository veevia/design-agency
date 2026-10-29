#!/usr/bin/env python3
"""Validate source coverage records, not runtime certification or capability counts."""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAP = ROOT / "00_README/domain-coverage-map.md"
START, END = "<!-- CAPABILITY-MAP:START -->", "<!-- CAPABILITY-MAP:END -->"
STATES = {"source-checked", "tested", "proposed", "reported", "blocked"}


def local_links(text: str, document: Path) -> list[Path]:
    paths = []
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = unquote(target.strip("<>").split("#", 1)[0])
        if not re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            paths.append(document.parent / target)
    return paths


def check(document: Path) -> dict:
    text = document.read_text(encoding="utf-8")
    errors: list[str] = []
    if text.count(START) != 1 or text.count(END) != 1 or text.index(START) >= text.index(END):
        raise ValueError("expected one ordered CAPABILITY-MAP marker pair")
    body = text.split(START, 1)[1].split(END, 1)[0]
    identifiers: set[str] = set()
    stale: list[str] = []
    records = 0
    for line in body.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells[0] == "ID" or re.fullmatch(r"[-: ]+", cells[0]):
            continue
        records += 1
        if len(cells) != 7:
            errors.append(f"record {records}: expected seven columns")
            continue
        identifier, task, authority, state, owner, verified, runtime = cells
        if not re.fullmatch(r"CAP-\d{2,}", identifier) or identifier in identifiers:
            errors.append(f"{identifier}: invalid or duplicate ID")
        identifiers.add(identifier)
        if not task or state not in STATES:
            errors.append(f"{identifier}: missing task or invalid state")
        if owner.lower() in {"", "tbd", "none", "team", "the team", "unassigned"}:
            errors.append(f"{identifier}: named owner required")
        match = re.search(r"\b\d{4}-\d{2}-\d{2}\b", verified)
        try:
            observed = date.fromisoformat(match.group()) if match else None
        except ValueError:
            observed = None
        if observed is None or observed > date.today():
            errors.append(f"{identifier}: valid past/present verification date required")
        elif (date.today() - observed).days > 90:
            stale.append(f"{identifier}: verification is stale (>90 days); review before claiming current coverage")
        for field, value in (("authority", authority), ("verification", verified)):
            paths = local_links(value, document)
            if not paths or any(not path.is_file() for path in paths):
                errors.append(f"{identifier}: {field} must link to existing source/evidence files")
        if not runtime:
            errors.append(f"{identifier}: runtime evidence or an explicit not-tested limit is required")
        if state == "tested" and "not runtime-tested" not in runtime.lower():
            paths = local_links(runtime, document)
            if not paths or any(not path.is_file() for path in paths):
                errors.append(f"{identifier}: a runtime-tested claim needs its evidence link")
    if not records:
        errors.append("capability map has no records")
    return {
        "scope": "source/record integrity and review freshness; not live runtime certification",
        "records": records, "errors": errors, "stale": stale,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--integrity-only", action="store_true",
                        help="report stale (>90 days) reviews as warnings instead of errors")
    args = parser.parse_args(argv)
    try:
        result = check(args.map)
    except (OSError, ValueError) as error:
        print(f"capability map unavailable: {error}", file=sys.stderr)
        return 2
    failures = result["errors"] + ([] if args.integrity_only else result["stale"])
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Capability map: {result['records']} records; {len(failures)} errors")
        for error in failures:
            print("  " + error)
        if args.integrity_only:
            for warning in result["stale"]:
                print("  warning: " + warning)
        print(result["scope"])
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
