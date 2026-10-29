#!/usr/bin/env python3
"""check-links.py — every relative Markdown link and wiki-link must resolve, also through discovery links.

Two passes over repository Markdown (tracked + untracked, not ignored; plug-in mounts excluded):
  1. Resolution: relative links resolve from the file's real location; [[wiki-links]] resolve
     against the Markdown vault. Links into a plug-in mount that is not checked out are skipped.
  2. Depth parity: native skills, agents and prompts are also read through their discovery links
     (.github/*, .claude/*). Their relative links must resolve to the same file from there.

    python3 06_Engine/harness/check-links.py            # report, exit 1 on any broken link
    python3 06_Engine/harness/check-links.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ENGINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_DIR))

from agency import discovery  # noqa: E402
from agency.catalog import build_catalog  # noqa: E402

LINK = re.compile(r"(?<!\\)\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)")
WIKI = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")
SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
SKIP_PARTS = {".git", "node_modules", ".venv", "__pycache__"}


def markdown_files(root: Path, excluded: list[Path]) -> list[Path]:
    listing = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "*.md"],
        cwd=root, capture_output=True, text=True,
    )
    if listing.returncode != 0:
        paths = [p for p in root.rglob("*.md")]
    else:
        paths = [root / name for name in listing.stdout.split("\0") if name]
    out = []
    for path in paths:
        if not path.is_file() or path.is_symlink() or SKIP_PARTS & set(path.relative_to(root).parts):
            continue
        if any(path.resolve().is_relative_to(mount) for mount in excluded):
            continue
        out.append(path)
    return sorted(set(out))


def link_targets(text: str):
    fenced = False
    for number, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        line = INLINE_CODE.sub("", line)
        for match in LINK.finditer(line):
            yield number, "md", match.group(1)
        for match in WIKI.finditer(line):
            yield number, "wiki", match.group(1).strip()


class Vault:
    def __init__(self, root: Path, files: list[Path]):
        self.keys = {str(path.relative_to(root).with_suffix("")).lower() for path in files}

    def has(self, name: str) -> bool:
        key = name.lower().removesuffix(".md").strip("/")
        return any(entry == key or entry.endswith("/" + key) for entry in self.keys)


def resolve(base_dir: Path, raw: str, root: Path) -> Path | None:
    if SCHEME.match(raw) or raw.startswith("#"):
        return None
    target = unquote(raw.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return None
    return (root / target.lstrip("/")) if target.startswith("/") else (base_dir / target)


def check(root: Path) -> tuple[list[dict], int]:
    root = root.resolve()
    catalog = build_catalog(root)
    mounts = [state.path.resolve() for state in catalog.states.values()]
    absent_mounts = [state.path.resolve() for state in catalog.states.values() if not state.present]
    files = markdown_files(root, mounts)
    vault = Vault(root, files)
    broken: list[dict] = []
    checked = 0

    def absent(path: Path) -> bool:
        normal = Path(os.path.normpath(path))
        return any(normal == mount or normal.is_relative_to(mount) for mount in absent_mounts)

    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line, kind, raw in link_targets(text):
            if kind == "wiki":
                checked += 1
                candidates = [root / raw, root / f"{raw}.md", path.parent / raw, path.parent / f"{raw}.md"]
                if not any(c.exists() for c in candidates) and not vault.has(raw):
                    broken.append({"file": str(path.relative_to(root)), "line": line, "target": raw, "reason": "wiki-link"})
                continue
            target = resolve(path.parent, raw, root)
            if target is None:
                continue
            checked += 1
            if absent(target):
                continue
            if not target.exists():
                broken.append({"file": str(path.relative_to(root)), "line": line, "target": raw, "reason": "missing"})

    # Depth parity through discovery links (native sources only), judged against the planned layout
    # so the check does not depend on whether `agency.py sync` has run yet.
    plan = discovery.plan(root, catalog=catalog)
    planned = sorted(
        ((str(Path(os.path.normpath(link.path))), (link.path.parent / link.target).resolve()) for link in plan.desired.values()),
        key=lambda pair: len(pair[0]), reverse=True,
    )

    def through_links(path: Path) -> Path:
        text = os.path.normpath(path)
        for link_path, source in planned:
            if text == link_path or text.startswith(link_path + os.sep):
                return source / os.path.relpath(text, link_path) if text != link_path else source
        return Path(text)

    for link in plan.desired.values():
        if link.origin != "native":
            continue
        source = (link.path.parent / link.target).resolve()
        members = sorted(source.rglob("*.md")) if source.is_dir() else [source]
        for member in members:
            if SKIP_PARTS & set(member.parts):
                continue
            virtual = (link.path / member.relative_to(source)) if source.is_dir() else link.path
            text = member.read_text(encoding="utf-8", errors="ignore")
            for line, kind, raw in link_targets(text):
                if kind != "md":
                    continue
                real = resolve(member.parent, raw, root)
                if real is None or not real.exists() or absent(real):
                    continue
                seen = through_links(resolve(virtual.parent, raw, root))
                checked += 1
                if not seen.exists() or seen.resolve() != real.resolve():
                    broken.append({
                        "file": str(member.relative_to(root)), "line": line, "target": raw,
                        "reason": f"breaks when read through {link.path.relative_to(root)} (depth parity)",
                    })
    return broken, checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ENGINE_DIR.parent)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    broken, checked = check(args.root)
    if args.json:
        print(json.dumps({"checked": checked, "broken": broken}, indent=2))
    else:
        for item in broken:
            print(f"{item['file']}:{item['line']} -> {item['target']} ({item['reason']})")
        print(f"links: {checked} checked, {len(broken)} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
