#!/usr/bin/env python3
"""
06_Engine/retrieval/build-wiki-index.py

Scan tracked project wikis and `00_Agentic-OS/_wiki/` and emit:
  - <wiki>/index.jsonl  (agent-readable; one line per page)
  - <wiki>/index.md     (human-readable; grouped by type)

Usage:
    python 06_Engine/retrieval/build-wiki-index.py             # all programs
    python 06_Engine/retrieval/build-wiki-index.py example-project   # one project hub
    python 06_Engine/retrieval/build-wiki-index.py --wiki-dir 00_Agentic-OS/_wiki
    python 06_Engine/retrieval/build-wiki-index.py --check     # validate without writing

Exit codes:
    0 indexed at least one program
    1 nothing indexed (no _wiki dirs found, or fatal error)
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wiki_support import (
    SKIP_DIRS, SKIP_FILES, discover_programs as discover_tracked_programs,
    knowledge_pages, tracked_markdown, without_fenced_code,
)

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parents[2]
HUBS_ROOT = REPO_ROOT / "01_Project-Hubs"
TYPED_FOLDERS = {"entities", "concepts", "sources", "syntheses", "decisions", "sessions"}

class WikiIndexError(ValueError):
    """Invalid source metadata must not produce a successful projection."""


def discover_programs() -> list[Path]:
    return discover_tracked_programs(REPO_ROOT)


def _git_md_under(root: Path) -> list[Path]:
    """Markdown pages under `root` from the git index (`git ls-files`) — NOT a raw filesystem glob.
    Untracked sibling work in a shared/dirty worktree therefore cannot leak into a generated index
    (generated indexes are built from tracked sources only). `.exists()` filters
    index entries deleted-but-not-yet-staged in a dirty tree so read_text() can't crash. Falls back
    to rglob only when git is unavailable (outside a checkout), so the tool still runs standalone."""
    return tracked_markdown(root, REPO_ROOT)


def _split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (raw YAML front-matter block, body).

    Splits only at the FIRST closing `---` fence on its own line. The naive
    text.split("---", 2) breaks whenever the BODY contains a `---` (horizontal
    rules, markdown table separators), wrongly truncating both the YAML and the
    body. Adapted from 06_Engine/harness/lint-skill.py:_split_frontmatter to
    also return the body (everything after the closing fence).
    """
    opening = re.match(r"^---[ \t]*\r?(?:\n|$)", text)
    if not opening:
        return None, text
    remainder = text[opening.end():]
    closing = re.search(r"^---[ \t]*\r?$", remainder, re.MULTILINE)
    if not closing:
        raise WikiIndexError("unterminated YAML frontmatter")
    fm = remainder[:closing.start()]
    body = remainder[closing.end():].lstrip("\r\n")
    return fm, body


def parse_front_matter(text: str, path: Path | None = None) -> tuple[dict, str]:
    source = str(path) if path is not None else "<text>"
    try:
        fm, body = _split_frontmatter(text)
        if fm is None:
            return {}, text
        data = yaml.safe_load(fm)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        location = f":{mark.line + 2}" if mark is not None else ""
        problem = getattr(exc, "problem", str(exc))
        raise WikiIndexError(f"{source}{location}: invalid YAML frontmatter: {problem}") from exc
    except WikiIndexError as exc:
        raise WikiIndexError(f"{source}: {exc}") from exc
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise WikiIndexError(f"{source}: YAML frontmatter must be a mapping")
    return data, body


def extract_title(body: str) -> str:
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return ""


TLDR_RX = re.compile(r"\*\*TL;DR:\*\*\s*(.+?)(?:\n|$)", re.IGNORECASE)
EVIDENCE_RX = re.compile(r"\[(observed|reported|assumed)\b")
WIKILINK_RX = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
MD_LINK_RX = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def clean_inline(text: str, limit: int = 200) -> str:
    def wikilink_label(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        label = match.group(2)
        return (label or target.split("/")[-1]).strip()

    text = WIKILINK_RX.sub(wikilink_label, text)
    text = MD_LINK_RX.sub(lambda match: match.group(1).strip(), text)
    text = re.sub(r"[`*_]+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    clipped = text[:limit].rsplit(" ", 1)[0].rstrip(".,;:")
    return clipped or text[:limit]


def extract_tldr(body: str, *, decision: bool = False) -> str:
    prose = without_fenced_code(body)
    m = TLDR_RX.search(prose)
    if m:
        return clean_inline(m.group(1))
    if not decision:
        return ""
    section = re.search(r"(?im)^#{1,6}\s+(?:The call|Action)\s*:?\s*$", prose)
    if section:
        paragraph: list[str] = []
        for line in prose[section.end():].splitlines():
            if not line.strip():
                if paragraph:
                    break
                continue
            if re.match(r"^\s*#{1,6}\s", line):
                break
            paragraph.append(line.strip())
        if paragraph:
            return clean_inline(" ".join(paragraph))
    action = re.search(r"(?im)^\s*(?:>\s*)?\*\*Action:?\*\*:?\s*(.+)$", prose)
    return clean_inline(action.group(1)) if action else ""


def count_evidence(body: str) -> dict[str, int]:
    counts = {"observed": 0, "reported": 0, "assumed": 0}
    for m in EVIDENCE_RX.finditer(body):
        counts[m.group(1)] += 1
    return counts


def strip_wikilink(value: object) -> str:
    """Reduce a front-matter relation value to its bare slug.

    Relation keys (`sources`, `touches-entities`, `touches-concepts`) store
    folder-qualified wikilinks so Obsidian's graph renders them as edges,
    e.g. `"[[concepts/triage-rules]]"`. The index keeps
    the bare slug — `triage-rules`. Plain strings pass through unchanged.
    """
    s = str(value).strip()
    m = WIKILINK_RX.fullmatch(s)
    if not m:
        return s
    return (m.group(2) or m.group(1)).strip().split("/")[-1]


def infer_type(rel_path: Path, fm: dict) -> str:
    t = fm.get("type")
    if isinstance(t, str):
        return t
    # First path component after _wiki/ (folder name)
    parts = rel_path.parts
    if parts and parts[0] in TYPED_FOLDERS:
        # Trim trailing "s" for singular type (entities -> entity)
        return {"entities": "entity", "syntheses": "synthesis"}.get(parts[0], parts[0][:-1])
    return "page"


def validate_decision_ids(entries: list[dict], context: object = "wiki") -> None:
    seen: dict[str, str] = {}
    for entry in entries:
        identifier = entry.get("id")
        if entry.get("type") != "decision" or not isinstance(identifier, str) or not identifier.strip():
            continue
        identifier = identifier.strip()
        if identifier in seen:
            raise WikiIndexError(
                f"{context}: duplicate decision id {identifier!r}: "
                f"{seen[identifier]} and {entry['path']}"
            )
        seen[identifier] = entry["path"]


def index_wiki(wiki_dir: Path) -> tuple[list[dict], list[str]]:
    """Walk a _wiki/ directory and return (entries, warnings)."""
    entries: list[dict] = []
    warnings: list[str] = []
    for path in knowledge_pages(wiki_dir, REPO_ROOT):
        rel = path.relative_to(wiki_dir)
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            warnings.append(f"{rel}: read-error: {e}")
            continue
        fm, body = parse_front_matter(text, path)
        title = (
            (fm.get("title") if isinstance(fm.get("title"), str) else None)
            or extract_title(body)
            or rel.stem
        )
        ptype = infer_type(rel, fm)
        tldr = extract_tldr(body, decision=ptype == "decision")
        tags = fm.get("tags") or []
        if not isinstance(tags, list):
            tags = []
        sources = fm.get("sources") or []
        if not isinstance(sources, list):
            sources = []
        updated = fm.get("updated") or fm.get("ingested")
        if isinstance(updated, datetime):
            updated = updated.date().isoformat()
        elif updated is None:
            updated = datetime.fromtimestamp(
                path.stat().st_mtime, tz=timezone.utc
            ).date().isoformat()
        else:
            updated = str(updated)
        subtype = fm.get("subtype")
        subtype = str(subtype) if isinstance(subtype, str) else ""
        entries.append(
            {
                "path": str(rel).replace("\\", "/"),
                "type": ptype,
                "subtype": subtype,
                "title": title,
                "tldr": tldr,
                "tags": [str(t) for t in tags],
                "sources": [strip_wikilink(s) for s in sources],
                "updated": updated,
                "evidence_mix": count_evidence(body),
            }
        )
        if ptype == "decision":
            for field in ("id", "record_type", "status", "light", "layer"):
                if isinstance(fm.get(field), str):
                    entries[-1][field] = fm[field]
            if isinstance(fm.get("canonical"), bool):
                entries[-1]["canonical"] = fm["canonical"]
    validate_decision_ids(entries, wiki_dir)
    return entries, warnings


def index_hub_root(hub_dir: Path, max_depth: int = 1) -> tuple[list[dict], list[str]]:
    """Index a hub's TOP-LEVEL markdown (for hubs whose knowledge isn't under _wiki/, e.g. 00_Design_Toolkit).
    Depth-limited; excludes _wiki/ (indexed separately) + heavy/experimental dirs so a churning subtree
    (skills/v0.73, node_modules) doesn't bloat or stale the index. Emits index.jsonl only — never index.md
    (the navigation index.md is owned by build-folder-index.py)."""
    heavy = {"node_modules", "dist", "__pycache__", ".next", "web_dist", ".venv-gates", "_wiki"}
    entries: list[dict] = []
    warnings: list[str] = []
    for path in _git_md_under(hub_dir):
        rel = path.relative_to(hub_dir)
        if (len(rel.parts) - 1) > max_depth:
            continue
        if any(part in heavy or part.startswith(".") for part in rel.parts):
            continue
        if rel.name.lower() in {"index.md", "log.md", "readme.md"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            warnings.append(f"{rel}: read-error: {e}")
            continue
        fm, body = parse_front_matter(text, path)
        title = (fm.get("title") if isinstance(fm.get("title"), str) else None) or extract_title(body) or rel.stem
        tags = fm.get("tags") if isinstance(fm.get("tags"), list) else []
        entries.append({
            "path": str(rel).replace("\\", "/"),
            "type": fm.get("type") if isinstance(fm.get("type"), str) else "doc",
            "subtype": "",
            "title": title,
            "tldr": extract_tldr(body),
            "tags": [str(t) for t in tags],
            "sources": [],
            "updated": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).date().isoformat(),
            "evidence_mix": count_evidence(body),
        })
    return entries, warnings


def write_jsonl(path: Path, entries: list[dict]) -> None:
    validate_decision_ids(entries, path)
    path.write_text(
        "".join(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n" for e in entries),
        encoding="utf-8",
    )


def write_index_md(path: Path, program: str, entries: list[dict]) -> None:
    validate_decision_ids(entries, path)
    by_type: dict[str, list[dict]] = {}
    for e in entries:
        by_type.setdefault(e["type"], []).append(e)
    lines: list[str] = []
    lines.append(f"# {program} \u2014 wiki index")
    lines.append("")
    lines.append(
        "Auto-derived from `index.jsonl` by `06_Engine/retrieval/build-wiki-index.py`. "
        "Edit the source pages, not this file."
    )
    lines.append("")
    lines.append(
        f"**Pages:** {len(entries)}  |  **Last built:** "
        f"{datetime.now(tz=timezone.utc).date().isoformat()}"
    )
    lines.append("")
    overview = path.parent.parent / "README.md"
    if overview.exists():
        phase = re.search(r"\*\*Current phase:\*\*[ \t]*([^\n]+)",
                          overview.read_text(encoding="utf-8"))
        lines.extend([
            "## Current loop phase", "",
            f"**Phase:** {phase.group(1).strip() if phase else 'Not declared in the hub overview.'}",
            "Source: [hub overview](../README.md); phase is not inferred from page counts.", "",
        ])
    if not entries:
        lines.extend(["No knowledge pages indexed yet; generated digests and templates do not count as knowledge.", ""])
    # Order of entity subtype sub-groups when rendering the entity section.
    ENTITY_SUBTYPE_ORDER = ["archetype", "persona", "platform", "decision-point"]

    def render_rows(rows: list[dict]) -> None:
        lines.append("| Page | TL;DR | Updated |")
        lines.append("|---|---|---|")
        for e in sorted(rows, key=lambda e: e["path"]):
            link = f"[`{e['path']}`]({e['path']})"
            tldr = (e["tldr"] or "").replace("|", "\\|")
            if e["type"] == "decision":
                state = " · ".join(str(e[field]) for field in ("id", "record_type", "status", "light")
                                   if e.get(field))
                if e.get("canonical"):
                    state = f"{state} · canonical" if state else "canonical"
                tldr = f"{state}. {tldr}".strip() if state else tldr
            lines.append(f"| {link} \u2014 {e['title']} | {tldr} | {e['updated']} |")
        lines.append("")

    for ptype in sorted(by_type):
        rows = sorted(by_type[ptype], key=lambda e: e["path"])
        lines.append(f"## {ptype} ({len(rows)})")
        lines.append("")
        # Sub-group the entity section by subtype (persona / platform / decision-point).
        if ptype == "entity" and any(e.get("subtype") for e in rows):
            by_kind: dict[str, list[dict]] = {}
            for e in rows:
                by_kind.setdefault(e.get("subtype") or "unclassified", []).append(e)
            ordered_kinds = [k for k in ENTITY_SUBTYPE_ORDER if k in by_kind]
            ordered_kinds += sorted(k for k in by_kind if k not in ENTITY_SUBTYPE_ORDER)
            for kind in ordered_kinds:
                krows = by_kind[kind]
                label = kind.replace("-", " ").title()
                lines.append(f"### {label} ({len(krows)})")
                lines.append("")
                render_rows(krows)
        else:
            render_rows(rows)
    path.write_text("\n".join(lines), encoding="utf-8")


def _main() -> int:
    args = [arg for arg in sys.argv[1:] if arg != "--check"]
    check_only = "--check" in sys.argv[1:]

    # --wiki-dir: index one explicit wiki outside 01_Project-Hubs (for a self-contained product
    # package such as 00_Agentic-OS). The path may be repo-relative or absolute.
    if "--wiki-dir" in args:
        i = args.index("--wiki-dir")
        if i + 1 >= len(args):
            print("ERROR: --wiki-dir requires a path", file=sys.stderr)
            return 1
        wiki = Path(args[i + 1])
        if not wiki.is_absolute():
            wiki = REPO_ROOT / wiki
        wiki = wiki.resolve()
        if not wiki.is_dir():
            print(f"ERROR: wiki directory not found: {wiki}", file=sys.stderr)
            return 1
        entries, warnings = index_wiki(wiki)
        for warning in warnings:
            print(f"# {wiki.parent.name}: {warning}", file=sys.stderr)
        if check_only:
            print(f"✓ {wiki.parent.name}: {len(entries)} pages validated (no writes)")
        else:
            write_jsonl(wiki / "index.jsonl", entries)
            write_index_md(wiki / "index.md", wiki.parent.name, entries)
            print(f"✓ {wiki.parent.name}: {len(entries)} pages → {wiki / 'index.jsonl'}")
        return 0

    # --hub-root: index a hub's top-level knowledge into <hub>/index.jsonl (for non-_wiki hubs).
    if "--hub-root" in args:
        args = [a for a in args if a != "--hub-root"]
        max_depth = 1
        if "--max-depth" in args:
            i = args.index("--max-depth")
            max_depth = int(args[i + 1])
            del args[i:i + 2]
        indexed = 0
        for name in args:
            hub = HUBS_ROOT / name
            if not hub.is_dir():
                print(f"# {name}: not a hub — skipping", file=sys.stderr)
                continue
            entries, warnings = index_hub_root(hub, max_depth)
            for w in warnings:
                print(f"# {name}: {w}", file=sys.stderr)
            validate_decision_ids(entries, hub)
            if check_only:
                print(f"✓ {name} (hub-root): {len(entries)} pages validated (no writes)")
            else:
                write_jsonl(hub / "index.jsonl", entries)
                print(f"✓ {name} (hub-root, depth≤{max_depth}): {len(entries)} pages → {hub / 'index.jsonl'}")
            indexed += 1
        return 0 if indexed else 1

    programs: list[Path]
    if args:
        programs = [REPO_ROOT / a if a == "00_Agentic-OS" else HUBS_ROOT / a for a in args]
    else:
        programs = discover_programs()

    projections: list[tuple[Path, list[dict]]] = []
    for program_dir in programs:
        wiki = program_dir / "_wiki"
        if not wiki.is_dir():
            print(f"# {program_dir.name}: no _wiki/ \u2014 skipping", file=sys.stderr)
            continue
        entries, warnings = index_wiki(wiki)
        for w in warnings:
            print(f"# {program_dir.name}: {w}", file=sys.stderr)
        projections.append((wiki, entries))
    validate_decision_ids([
        {**entry, "path": str(wiki / entry["path"])}
        for wiki, entries in projections for entry in entries
    ], "selected wikis")
    for wiki, entries in projections:
        if check_only:
            print(f"✓ {wiki.parent.name}: {len(entries)} pages validated (no writes)")
        else:
            write_jsonl(wiki / "index.jsonl", entries)
            write_index_md(wiki / "index.md", wiki.parent.name, entries)
            print(f"✓ {wiki.parent.name}: {len(entries)} pages → {wiki / 'index.jsonl'}")
    return 0 if projections else 1


def main() -> int:
    try:
        return _main()
    except WikiIndexError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
