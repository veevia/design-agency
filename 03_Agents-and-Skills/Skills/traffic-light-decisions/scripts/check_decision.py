#!/usr/bin/env python3
"""Validate lifecycle-aware decision records with legacy compatibility.

The validator has two deliberately different jobs:

* ``decision-record/v2`` records are strict, typed contracts.
* migrated ``decision-record/v1`` and unmigrated records keep their historical
  prose; the validator checks identity, lifecycle and Traffic Light metadata
  without pretending an old document used today's section template.

``superseded`` means a successor replaced the record and must form a resolvable
chain to an accepted decision. ``retired`` means the record ended without a
successor. Canonical ADRs are an explicit active subset, not every accepted ADR
and not every numbered file in a decisions directory.

Run one record while authoring, or audit every authoritative decision namespace:

    python3 check_decision.py path/to/record.md
    python3 check_decision.py 00_Agentic-OS/decisions --canonical --json
    python3 check_decision.py --repo-root . --allow-expired \
      --manifest 01_Project-Hubs/00_Decisions/migration/2026-09-04-manifest.csv

Expired active Yellows fail normal authoring checks. ``--allow-expired`` turns
them into closure warnings for a corpus migration; retired/superseded records
never fail merely because their historical expiry is past.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


VALID_RECORD_TYPES = {"adr", "pdr", "ops-note", "release"}
VALID_STATUSES = {"proposed", "accepted", "superseded", "retired"}
VALID_LIGHTS = {"green", "yellow", "red"}
VALID_CONSULTATION = {"solo", "invited", "reviewed"}
VALID_LAYERS = {f"L{number}" for number in range(6)}
GROUP_OWNER = re.compile(r"^(the\s+team|team|everyone|all|us|we|tbd|n/?a)$", re.I)
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CANONICAL_ID = re.compile(r"^[A-Za-z][A-Za-z0-9-]*-\d{4}$")
CANONICAL_BODY_WORD_LIMIT = 600
SKIP_PARTS = {".git", "_archive", "_template-project", "evals", "fixtures", "node_modules", "tests"}


@dataclass(frozen=True)
class Issue:
    level: str
    message: str


@dataclass
class Record:
    path: Path
    fm: dict[str, str]
    body: str
    body_bytes: bytes

    @property
    def identifier(self) -> str:
        return self.fm.get("id", "").strip()

    @property
    def schema(self) -> str:
        return self.fm.get("schema_version", "legacy").strip()

    @property
    def strict(self) -> bool:
        return self.schema == "decision-record/v2"


def split_record(raw: bytes) -> tuple[dict[str, str], bytes]:
    """Parse flat YAML front matter and preserve the exact body bytes."""
    if not raw.startswith(b"---\n"):
        return {}, raw
    match = re.search(br"^---[ \t]*\r?$", raw[4:], re.M)
    if not match:
        return {}, raw
    start = 4 + match.start()
    end = 4 + match.end()
    if end < len(raw) and raw[end:end + 2] == b"\r\n":
        end += 2
    elif end < len(raw) and raw[end:end + 1] == b"\n":
        end += 1
    header = raw[4:start].decode("utf-8")
    out: dict[str, str] = {}
    for line in header.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line[:1].isspace():
            continue
        found = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not found:
            continue
        key, value = found.group(1).lower(), found.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        out[key] = value
    return out, raw[end:]


def load_record(path: Path) -> Record:
    raw = path.read_bytes()
    fm, body = split_record(raw)
    return Record(path=path, fm=fm, body=body.decode("utf-8"), body_bytes=body)


def parse_list(value: str) -> list[str]:
    value = value.strip()
    if not value:
        return []
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [item.strip().strip("\"'") for item in value.split(",") if item.strip().strip("\"'")]


def body_field(body: str, key: str) -> str:
    """Read old body-only Traffic Light YAML without treating prose as metadata."""
    found = re.search(rf"(?mi)^\s*{re.escape(key)}:\s*(.+?)\s*$", body)
    return found.group(1).strip() if found else ""


def legacy_light(record: Record) -> str:
    fm = record.fm
    light = fm.get("light", "").lower()
    if light:
        return light
    if fm.get("status", "").lower() in VALID_LIGHTS:
        return fm["status"].lower()
    return body_field(record.body, "traffic_light").lower()


def traffic_value(record: Record, name: str) -> str:
    value = record.fm.get(name, "")
    if value:
        return value
    return body_field(record.body, f"traffic_light_{name}")


def headings(body: str) -> list[str]:
    return [re.sub(r"[*_`]", "", match.group(1)).strip().lower()
            for match in re.finditer(r"(?m)^#{1,6}\s+(.+?)\s*$", body)]


def has_heading(record: Record, *terms: str) -> bool:
    return any(any(term in heading for term in terms) for heading in headings(record.body))


def options_count(body: str) -> int:
    section = re.search(
        r"(?ims)^#{1,6}\s+(?:options(?: considered)?|alternatives|what was on the table)\b(.*?)(?=^#{1,6}\s+|\Z)",
        body,
    )
    if not section:
        return 0
    text = section.group(1)
    table_rows = []
    for line in text.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or all(re.fullmatch(r":?-{3,}:?", cell or "-") for cell in cells):
            continue
        if cells[0].lower() in {"option", "alternative"}:
            continue
        table_rows.append(cells)
    if table_rows:
        return len(table_rows)
    return len(re.findall(r"(?m)^\s*(?:\d+[.)]|[-*]\s+\*{0,2}(?:option\s+)?[A-Z][.)—:-])\s+", text))


def expected_prefix(path: Path) -> str | None:
    """Namespace convention: `aos-NNNN` for OS contracts, `<hub-slug>-NNNN` inside a project hub."""
    value = path.as_posix()
    if "/00_Agentic-OS/decisions/" in f"/{value}" or value.startswith("00_Agentic-OS/decisions/"):
        return "aos-"
    hub = re.search(r"(?:^|/)01_Project-Hubs/([a-z0-9]+(?:-[a-z0-9]+)*)/", value)
    if hub and "/decisions/" in value:
        return f"{hub.group(1)}-"
    return None


def valid_date(value: str) -> bool:
    if not ISO_DATE.fullmatch(value):
        return False
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def check_record(record: Record, *, allow_expired: bool = False) -> list[Issue]:
    fm = record.fm
    issues: list[Issue] = []
    strict_or_migrated = record.schema in {"decision-record/v1", "decision-record/v2"}

    if strict_or_migrated:
        for field in ("id", "record_type", "status", "owner", "created", "updated", "consultation"):
            if not fm.get(field, ""):
                issues.append(Issue("error", f"missing `{field}:`"))

        identifier = record.identifier
        if identifier and not CANONICAL_ID.fullmatch(identifier):
            issues.append(Issue("error", f"`id: {identifier}` is not a canonical <namespace>-NNNN id"))
        prefix = expected_prefix(record.path)
        if identifier and prefix and not identifier.startswith(prefix):
            issues.append(Issue("error", f"`id: {identifier}` does not use path namespace `{prefix}`"))

        kind = fm.get("record_type", "")
        if kind and kind not in VALID_RECORD_TYPES:
            issues.append(Issue("error", f"`record_type: {kind}` must be one of {sorted(VALID_RECORD_TYPES)}"))
        status = fm.get("status", "")
        if status and status not in VALID_STATUSES:
            issues.append(Issue("error", f"`status: {status}` must be one of {sorted(VALID_STATUSES)}"))
        consultation = fm.get("consultation", "")
        if consultation and consultation not in VALID_CONSULTATION:
            issues.append(Issue("error", f"`consultation: {consultation}` must be one of {sorted(VALID_CONSULTATION)}"))
        for field in ("created", "updated"):
            if fm.get(field) and not valid_date(fm[field]):
                issues.append(Issue("error", f"`{field}: {fm[field]}` is not a real ISO date"))
    else:
        issues.append(Issue("warning", "legacy schema: migrate metadata to decision-record/v1"))

    owner = fm.get("owner", "") or body_field(record.body, "traffic_light_owner")
    if strict_or_migrated and owner and GROUP_OWNER.fullmatch(owner.strip()):
        issues.append(Issue("error", f"`owner: {owner}` is a group/placeholder; name one person"))

    kind = fm.get("record_type", "")
    light = legacy_light(record)
    if strict_or_migrated and kind in {"adr", "pdr"} and not light:
        issues.append(Issue("error", f"`record_type: {kind}` requires `light:`"))
    if light and light not in VALID_LIGHTS:
        issues.append(Issue("error", f"`light: {light}` must be green|yellow|red"))

    lifecycle = fm.get("status", "").lower()
    inactive = lifecycle in {"retired", "superseded"}
    canonical = fm.get("canonical", "").lower()
    if canonical and canonical not in {"true", "false"}:
        issues.append(Issue("error", "`canonical:` must be true or false"))
    if canonical == "true" and (kind != "adr" or lifecycle != "accepted"):
        issues.append(Issue("error", "`canonical: true` requires an accepted ADR"))
    if "layer" in fm:
        if fm["layer"] not in VALID_LAYERS:
            issues.append(Issue("error", "`layer:` must be one of L0, L1, L2, L3, L4, L5"))
        if kind != "adr":
            issues.append(Issue("error", "`layer:` applies only to ADRs"))
    if canonical == "true" and record.strict and len(record.body.split()) > CANONICAL_BODY_WORD_LIMIT:
        issues.append(Issue(
            "error", f"canonical ADR body exceeds {CANONICAL_BODY_WORD_LIMIT} words; link implementation and evidence"
        ))
    if light == "yellow":
        trigger = traffic_value(record, "trigger")
        expiry = traffic_value(record, "expiry")
        if not trigger:
            issues.append(Issue("error", "Yellow requires `trigger:`"))
        if not expiry:
            issues.append(Issue("error", "Yellow requires `expiry:`"))
        elif not valid_date(expiry):
            issues.append(Issue("error", f"`expiry: {expiry}` is not a real ISO date"))
        elif dt.date.fromisoformat(expiry) < dt.date.today() and not inactive:
            level = "warning" if allow_expired else "error"
            issues.append(Issue(level, f"active Yellow expired on {expiry}; close, re-evaluate, or explicitly extend it"))
    if light == "red":
        blocker = traffic_value(record, "blocker")
        unblock_owner = traffic_value(record, "unblock_owner")
        if not blocker:
            issues.append(Issue("error", "Red requires `blocker:`"))
        if not unblock_owner:
            issues.append(Issue("error", "Red requires `unblock_owner:`"))
        elif GROUP_OWNER.fullmatch(unblock_owner.strip()):
            issues.append(Issue("error", f"`unblock_owner: {unblock_owner}` is a group/placeholder"))

    if record.strict:
        required: dict[str, tuple[tuple[str, ...], ...]] = {
            "adr": (("context",), ("decision", "the decision"), ("options", "alternatives", "what was on the table"),
                    ("consequences",), ("disagreement", "consultation", "stakeholder feedback"),
                    ("rollback", "reversal", "what changes if this flips")),
            "pdr": (("decision", "the call"), ("options", "what was on the table"),
                    ("evidence", "the why", "rationale"), ("outcomes", "consequences", "affected outcomes"),
                    ("review trigger", "rollback", "what changes if this flips")),
            "ops-note": (("action", "the action"), ("reason", "rationale", "why"),
                         ("evidence", "result", "verification"), ("rollback", "runbook", "reversibility")),
            "release": (("subject", "version"), ("gates", "gate results"), ("result", "release result"),
                        ("evidence", "immutable evidence")),
        }
        for alternatives in required.get(kind, ()):
            if not has_heading(record, *alternatives):
                issues.append(Issue("error", f"{kind} body missing section: {' / '.join(alternatives)}"))
        if kind in {"adr", "pdr"} and options_count(record.body) < 2:
            issues.append(Issue("error", f"{kind} requires at least two documented alternatives"))
        consultation = fm.get("consultation", "")
        if consultation in {"invited", "reviewed"}:
            has_consultation = has_heading(record, "disagreement", "consultation", "stakeholder feedback")
            if not has_consultation:
                issues.append(Issue("error", f"`consultation: {consultation}` requires consultation evidence in the body"))
            none_only = re.search(r"(?is)(?:disagreement|consultation)[^\n]*\n+\s*[-*]?\s*(?:none|n/?a)\b", record.body)
            if consultation == "reviewed" and none_only:
                issues.append(Issue("error", "`consultation: reviewed` cannot be supported only by `none`"))

    if strict_or_migrated and lifecycle == "superseded":
        successors = parse_list(fm.get("superseded_by", ""))
        if not successors:
            issues.append(Issue("error", "`status: superseded` requires `superseded_by:`"))
        elif len(successors) != 1:
            issues.append(Issue("error", "`status: superseded` requires exactly one successor"))
    if strict_or_migrated and lifecycle != "superseded" and fm.get("superseded_by", ""):
        issues.append(Issue(
            "error",
            f"`status: {lifecycle}` cannot use `superseded_by:`; use `superseded` for replacement or `retired` without a successor",
        ))
    return issues


def is_decision_path(path: Path, explicit_file: bool = False) -> bool:
    if explicit_file:
        return path.suffix.lower() == ".md"
    if path.name.lower() in {"index.md", "readme.md"} or path.suffix.lower() != ".md":
        return False
    parts = set(path.parts)
    return "decisions" in parts and not (parts & SKIP_PARTS)


def discover(targets: list[Path]) -> list[Path]:
    found: set[Path] = set()
    for target in targets:
        if target.is_file() and is_decision_path(target, explicit_file=True):
            found.add(target.resolve())
        elif target.is_dir():
            for path in target.rglob("*.md"):
                if is_decision_path(path):
                    found.add(path.resolve())
    return sorted(found)


def validate_relations(records: list[Record]) -> dict[Path, list[Issue]]:
    extra: dict[Path, list[Issue]] = defaultdict(list)
    by_id: dict[str, list[Record]] = defaultdict(list)
    aliases: dict[str, list[Record]] = defaultdict(list)
    for record in records:
        if record.identifier:
            by_id[record.identifier.casefold()].append(record)
        for alias in parse_list(record.fm.get("aliases", "")):
            aliases[alias.casefold()].append(record)
    for identifier, matches in by_id.items():
        if len(matches) > 1:
            paths = ", ".join(str(item.path) for item in matches)
            for record in matches:
                extra[record.path].append(Issue("error", f"duplicate canonical id `{identifier}`: {paths}"))
    for alias, matches in aliases.items():
        if len(matches) > 1 or alias in by_id:
            paths = ", ".join(str(item.path) for item in matches)
            for record in matches:
                extra[record.path].append(Issue("error", f"alias `{alias}` is not unique: {paths}"))

    unique = {key: value[0] for key, value in by_id.items() if len(value) == 1}
    for record in records:
        source = record.identifier.casefold()
        for field in ("supersedes", "superseded_by"):
            for target_id in parse_list(record.fm.get(field, "")):
                target = unique.get(target_id.casefold())
                if not target:
                    extra[record.path].append(Issue("error", f"`{field}` target `{target_id}` does not resolve"))
                    continue
                reverse = "superseded_by" if field == "supersedes" else "supersedes"
                reverse_ids = {item.casefold() for item in parse_list(target.fm.get(reverse, ""))}
                source_status = record.fm.get("status", "")
                target_status = target.fm.get("status", "")
                if field == "supersedes":
                    if source_status == "proposed":
                        if target_status != "accepted":
                            extra[record.path].append(Issue(
                                "error",
                                f"proposed successor `{record.identifier}` must leave `{target_id}` accepted until promotion",
                            ))
                        require_reverse = False
                    else:
                        if target_status != "superseded":
                            extra[record.path].append(Issue(
                                "error",
                                f"active/historical successor `{record.identifier}` requires `{target_id}` to use `status: superseded`",
                            ))
                        require_reverse = True
                else:
                    require_reverse = True
                    if source_status != "superseded":
                        extra[record.path].append(Issue(
                            "error",
                            f"only `status: superseded` may use `superseded_by:` (found `{source_status}`)",
                        ))
                    if target_status not in {"accepted", "superseded"}:
                        extra[record.path].append(Issue(
                            "error",
                            f"successor `{target_id}` must be accepted or itself superseded, not `{target_status}`",
                        ))
                if require_reverse and source and source not in reverse_ids:
                    extra[record.path].append(Issue(
                        "error", f"`{field}: {target_id}` is not mirrored by `{reverse}: {record.identifier}`"
                    ))

    # Every superseded record must reach an accepted terminal through a finite,
    # resolvable successor chain. This catches ambiguous accepted predecessors,
    # dead-end chains and cycles that pairwise mirror checks cannot detect.
    for record in unique.values():
        if record.fm.get("status") != "superseded":
            continue
        start = record.identifier.casefold()
        stack: list[tuple[str, tuple[str, ...]]] = [(start, ())]
        reached_accepted = False
        chain_error = False
        while stack:
            current_id, trail = stack.pop()
            if current_id in trail:
                extra[record.path].append(Issue(
                    "error", f"supersession cycle detected: {' -> '.join((*trail, current_id))}"
                ))
                chain_error = True
                continue
            current = unique.get(current_id)
            if not current:
                chain_error = True
                continue
            status = current.fm.get("status", "")
            if status == "accepted":
                reached_accepted = True
                continue
            if status != "superseded":
                extra[record.path].append(Issue(
                    "error", f"supersession chain from `{record.identifier}` ends at `{current.identifier}` with status `{status}`"
                ))
                chain_error = True
                continue
            successors = [item.casefold() for item in parse_list(current.fm.get("superseded_by", ""))]
            if not successors:
                chain_error = True
                continue
            for successor in successors:
                stack.append((successor, (*trail, current_id)))
        if not reached_accepted and not chain_error:
            extra[record.path].append(Issue(
                "error", f"supersession chain from `{record.identifier}` has no accepted terminal"
            ))
    return extra


def verify_manifest(path: Path, records: list[Record], repo_root: Path) -> list[Issue]:
    issues: list[Issue] = []
    by_relative: dict[str, Record] = {}
    by_identifier: dict[str, list[Record]] = defaultdict(list)
    for record in records:
        try:
            relative = record.path.resolve().relative_to(repo_root.resolve()).as_posix()
        except ValueError:
            continue
        by_relative[relative] = record
        if record.identifier:
            by_identifier[record.identifier.casefold()].append(record)
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    seen: set[str] = set()
    for row in rows:
        relative = row.get("path", "")
        if not relative:
            issues.append(Issue("error", "manifest row missing path"))
            continue
        if relative in seen:
            issues.append(Issue("error", f"manifest repeats `{relative}`"))
        seen.add(relative)
        record = by_relative.get(relative)
        if not record:
            # The dated migration path remains immutable even when a classified
            # record is later relocated. Resolve a moved record by its frozen
            # canonical identity, then continue to enforce the original body
            # hash. Ambiguous or missing identities still fail closed.
            identifier = row.get("canonical_id", "").casefold()
            candidates = by_identifier.get(identifier, [])
            if len(candidates) == 1:
                record = candidates[0]
            elif len(candidates) > 1:
                issues.append(Issue(
                    "error", f"manifest path `{relative}` resolves ambiguously by id `{identifier}`"
                ))
                continue
            else:
                issues.append(Issue("error", f"manifest path not discovered: `{relative}`"))
                continue
        expected = row.get("body_sha256", "")
        actual = hashlib.sha256(record.body_bytes).hexdigest()
        if expected != actual:
            issues.append(Issue("error", f"historical body changed: `{relative}`"))
        # The migration manifest freezes identity and body content, not mutable
        # lifecycle/type judgments. Later retirement or reclassification must
        # not require rewriting a dated migration artifact.
        for column, actual_value in (("canonical_id", record.identifier),):
            if row.get(column, "") != actual_value:
                issues.append(Issue("error", f"manifest {column} mismatch for `{relative}`"))
    if len(rows) != 72:
        issues.append(Issue("error", f"migration manifest must classify 72 legacy records, found {len(rows)}"))
    return issues


def git_root(start: Path) -> Path:
    result = subprocess.run(["git", "-C", str(start), "rev-parse", "--show-toplevel"],
                            text=True, capture_output=True, check=False)
    return Path(result.stdout.strip()) if result.returncode == 0 else start.resolve()


def record_summary(record: Record, root: Path) -> dict[str, object]:
    try:
        relative = record.path.relative_to(root).as_posix()
    except ValueError:
        relative = str(record.path)
    title = next((line[2:].strip() for line in record.body.splitlines() if line.startswith("# ")),
                 record.path.stem)
    summary: dict[str, object] = {
        "id": record.identifier,
        "title": title,
        "path": relative,
        "record_type": record.fm.get("record_type", ""),
        "status": record.fm.get("status", ""),
        "light": legacy_light(record),
        "canonical": record.fm.get("canonical", "").lower() == "true",
        "body_words": len(record.body.split()),
    }
    if "layer" in record.fm:
        summary["layer"] = record.fm["layer"]
    for field in ("trigger", "expiry", "blocker", "unblock_owner"):
        if value := traffic_value(record, field):
            summary[field] = value
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="*", type=Path)
    parser.add_argument("--repo-root", type=Path, help="audit every authoritative decisions/ namespace")
    parser.add_argument("--manifest", type=Path, help="verify the 72-record migration manifest and body hashes")
    parser.add_argument("--allow-expired", action="store_true", help="report active expired Yellows as closure warnings")
    parser.add_argument("--canonical", action="store_true", help="validate only marked canonical contracts; still resolve corpus links")
    parser.add_argument("--expected-layers", nargs="+", choices=sorted(VALID_LAYERS),
                        help="require exactly one canonical ADR for each listed layer and no others")
    parser.add_argument("--json", action="store_true", help="emit contract metadata and issues without record bodies")
    count_guard = parser.add_mutually_exclusive_group()
    count_guard.add_argument("--expected-count", type=int, help="fail unless discovery finds exactly this many records")
    count_guard.add_argument("--minimum-count", type=int, help="fail if discovery finds fewer than this baseline")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    if args.canonical and args.manifest:
        parser.error("--manifest requires the full corpus, not --canonical selection")
    if args.expected_layers and not args.canonical:
        parser.error("--expected-layers requires --canonical selection")
    if args.expected_layers and len(set(args.expected_layers)) != len(args.expected_layers):
        parser.error("--expected-layers must list each layer once")

    if args.repo_root:
        root = args.repo_root.resolve()
        targets = [root / "00_Agentic-OS", root / "01_Project-Hubs"]
    elif args.targets:
        targets = args.targets
        root = git_root(Path.cwd())
    else:
        parser.error("provide a file/folder target or --repo-root")

    missing = [str(path) for path in targets if not path.exists()]
    if missing:
        print(f"missing target(s): {', '.join(missing)}", file=sys.stderr)
        return 2
    paths = discover(targets)
    if not paths:
        print("no decision records discovered", file=sys.stderr)
        return 2

    all_records: list[Record] = []
    global_issues: list[Issue] = []
    failures: dict[Path, list[Issue]] = defaultdict(list)
    for path in paths:
        try:
            record = load_record(path)
        except (OSError, UnicodeDecodeError) as error:
            global_issues.append(Issue("error", f"cannot read {path}: {error}"))
            continue
        all_records.append(record)
    records = [record for record in all_records
               if not args.canonical or record.fm.get("canonical", "").lower() not in {"", "false"}]
    if args.canonical and not records:
        global_issues.append(Issue("error", "no canonical contracts discovered in the selected scope"))
    for record in records:
        failures[record.path].extend(check_record(record, allow_expired=args.allow_expired))
    relation_records = list(all_records)
    if not args.repo_root:
        # A one-file authoring check still resolves links and canonical identity
        # against the authoritative corpus, without printing unrelated records.
        authoritative_paths = discover([root / "00_Agentic-OS", root / "01_Project-Hubs"])
        loaded = {record.path.resolve() for record in relation_records}
        for path in authoritative_paths:
            if path.resolve() not in loaded:
                try:
                    relation_records.append(load_record(path))
                except (OSError, UnicodeDecodeError) as error:
                    global_issues.append(Issue("error", f"cannot read relation target {path}: {error}"))
    relations = validate_relations(relation_records)
    displayed = {record.path.resolve() for record in records}
    for path, issues in relations.items():
        if path.resolve() in displayed:
            failures[path].extend(issues)

    if args.expected_count is not None and len(records) != args.expected_count:
        global_issues.append(Issue("error", f"expected {args.expected_count} records, discovered {len(records)}"))
    if args.minimum_count is not None and len(records) < args.minimum_count:
        global_issues.append(Issue("error", f"expected at least {args.minimum_count} records, discovered {len(records)}"))
    if args.expected_layers:
        layer_counts = Counter(record.fm.get("layer", "<missing>") for record in records)
        if layer_counts != Counter(args.expected_layers):
            global_issues.append(Issue(
                "error", f"expected one canonical ADR per layer {', '.join(args.expected_layers)}; "
                f"found {dict(sorted(layer_counts.items()))}"
            ))
    if args.manifest:
        global_issues.extend(verify_manifest(args.manifest.resolve(), records, root))

    if args.json:
        issues = [{"path": str(path), "level": issue.level, "message": issue.message}
                  for path, path_issues in failures.items() for issue in path_issues]
        issues.extend({"level": issue.level, "message": issue.message} for issue in global_issues)
        error_count = sum(issue["level"] == "error" for issue in issues)
        print(json.dumps({
            "records": [record_summary(record, root) for record in records],
            "count": len(records),
            "errors": error_count,
            "warnings": sum(issue["level"] == "warning" for issue in issues),
            "issues": issues,
        }, ensure_ascii=False, indent=2))
        return 1 if error_count else 0

    error_count = warning_count = 0
    for record in records:
        issues = failures.get(record.path, [])
        errors = [item for item in issues if item.level == "error"]
        warnings = [item for item in issues if item.level == "warning"]
        error_count += len(errors)
        warning_count += len(warnings)
        if errors or warnings:
            marker = "✗" if errors else "!"
            print(f"{marker} {record.path}")
            for issue in issues:
                print(f"    - {issue.level}: {issue.message}")
        elif not args.quiet:
            print(f"✓ {record.path}")
    for issue in global_issues:
        print(f"{('✗' if issue.level == 'error' else '!')} {issue.level}: {issue.message}")
        error_count += issue.level == "error"
        warning_count += issue.level == "warning"

    kinds = Counter(record.fm.get("record_type", "legacy") or "legacy" for record in records)
    canonical_adrs = sum(
        record.fm.get("canonical", "").lower() == "true"
        and record.fm.get("record_type") == "adr"
        and record.fm.get("status") == "accepted"
        for record in records
    )
    active_expired = sum(
        any("active Yellow expired" in issue.message for issue in failures.get(record.path, []))
        for record in records
    )
    print(
        f"\n{len(records)} record(s) discovered · {error_count} error(s) · {warning_count} warning(s) · "
        f"types: {', '.join(f'{key}={value}' for key, value in sorted(kinds.items()))} · "
        f"canonical ADRs={canonical_adrs}"
    )
    if active_expired:
        print(f"closure report: {active_expired} active Yellow record(s) are past expiry; none changed automatically")
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
