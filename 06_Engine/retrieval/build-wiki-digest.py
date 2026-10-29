#!/usr/bin/env python3
"""
06_Engine/retrieval/build-wiki-digest.py

Distil a program's `_wiki/index.jsonl` into a compact, agent-facing DIGEST — the
"top-of-mind" knowledge an agent should carry at session start, with a pointer to
retrieve depth on demand. This is the READ/LEARN side of the knowledge loop
(navigation, not page creation) — it never writes `_wiki` knowledge pages.

Outputs:
  - `<hub>/_wiki/_digest.md`  — full digest (for Obsidian / on-disk agents)
  - stdout: a compact MEMORY BLOCK to paste into `/memories/repo/<slug>.md`

Usage:
    python 06_Engine/retrieval/build-wiki-digest.py example-project
    python 06_Engine/retrieval/build-wiki-digest.py example-project --memory   # print only the memory block
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

REPO = Path(__file__).resolve().parents[2]


def find_hub(arg: str) -> Path | None:
    for base in (REPO / "01_Project-Hubs", REPO / "03_Agents-and-Skills", REPO):
        for p in sorted(base.iterdir()) if base.is_dir() else []:
            if arg.lower() in p.name.lower() and (p / "_wiki" / "index.jsonl").exists():
                return p
    return None


def load(hub: Path) -> list[dict]:
    rows = []
    for line in (hub / "_wiki" / "index.jsonl").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def by(rows, typ):
    return sorted((r for r in rows if r.get("type") == typ),
                  key=lambda r: r.get("updated", ""), reverse=True)


def line(row: dict, linked: bool = True) -> str:
    title = row.get("title", row["path"])
    if linked:
        title = title.replace("[", "\\[").replace("]", "\\]")
        title = f"[{title}]({quote(row['path'], safe='/')})"
    state = " · ".join(str(row[field]) for field in ("id", "record_type", "status", "light")
                       if row.get(field))
    summary = " — ".join(part for part in (state, (row.get("tldr") or "").strip()) if part)
    return f"- **{title}** — {summary}" if summary else f"- **{title}**"


def build(hub: Path) -> tuple[str, str]:
    rows = load(hub)
    slug = hub.name
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    concepts, syntheses, decisions = by(rows, "concept"), by(rows, "synthesis"), by(rows, "decision")
    entities = by(rows, "entity")
    # group entities by subtype
    esub: dict[str, list] = {}
    for e in entities:
        esub.setdefault(e.get("subtype") or "entity", []).append(e)

    ptr = (f"_Go deeper:_ `python3 06_Engine/retrieval/wiki-neighbors.py {slug} \"<query>\"` "
           f"or `/context-pull {slug} \"<query>\"` → read the page → follow its `links`.")

    # --- full digest ---
    out = [f"# {slug} — wiki digest", "",
           f"_Auto-generated {now} · {len(rows)} pages · agent top-of-mind. {ptr}_", ""]
    if not rows:
        out += ["No knowledge pages indexed yet. Start with the [hub overview](../README.md); this digest is not a source page.", ""]
    if concepts:
        out += [f"## Concepts — the model ({len(concepts)})", ""] + [line(c) for c in concepts] + [""]
    if syntheses:
        out += [f"## Syntheses — current theses ({len(syntheses)})", ""] + [line(s) for s in syntheses] + [""]
    if decisions:
        out += [f"## Decisions ({len(decisions)})", ""] + [line(d) for d in decisions] + [""]
    if entities:
        out += [f"## Key entities ({len(entities)})", ""]
        for sub in sorted(esub, key=lambda k: -len(esub[k])):
            names = ", ".join(e.get("title", e["path"]) for e in esub[sub][:20])
            out += [f"- **{sub}** ({len(esub[sub])}): {names}"]
        out += [""]

    # --- compact memory block (concepts + syntheses + entity headline + pointer) ---
    mem = [f"## Wiki knowledge digest (auto · {now} · {len(rows)} pages)", ""]
    if concepts:
        mem += ["**Concepts (the model):**"] + [line(c, linked=False)[:180] for c in concepts] + [""]
    if syntheses:
        mem += ["**Theses:**"] + [line(s, linked=False)[:180] for s in syntheses] + [""]
    if decisions:
        mem += ["**Decisions:**"] + [line(d, linked=False)[:180] for d in decisions] + [""]
    if entities:
        headline = "; ".join(f"{sub} {len(esub[sub])}" for sub in sorted(esub, key=lambda k: -len(esub[k])))
        mem += [f"**Entities:** {headline}.", ""]
    mem += [ptr]
    return "\n".join(out).rstrip() + "\n", "\n".join(mem) + "\n"


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mem_only = "--memory" in sys.argv
    if not args:
        print("usage: build-wiki-digest.py <hub> [--memory]", file=sys.stderr)
        return 1
    hub = find_hub(args[0])
    if not hub:
        print(f"no hub with _wiki/index.jsonl matching '{args[0]}'", file=sys.stderr)
        return 1
    full, mem = build(hub)
    if not mem_only:
        (hub / "_wiki" / "_digest.md").write_text(full, encoding="utf-8")
        print(f"✓ wrote {hub.name}/_wiki/_digest.md ({full.count(chr(10))} lines)", file=sys.stderr)
    print(mem)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
