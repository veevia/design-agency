#!/usr/bin/env python3
"""
06_Engine/retrieval/wiki-neighbors.py

Graph-aware retrieval: given a query (or a seed page), find the best entry pages
in a program's `_wiki/` and expand ONE hop along authored wikilinks and Markdown
note links, including explicit links to other maintained wikis.
The frozen semantic export is an opt-in, provenance-labeled historical overlay.
This is how an agent "finds the right content through the graph":
a lexical hit gives the seed; the graph gives its neighborhood.

Returns lightweight identifiers (path + title + why), never page bodies — the
agent reads the few it wants next.

Usage:
    python 06_Engine/retrieval/wiki-neighbors.py example-project "urgent job routing"
    python 06_Engine/retrieval/wiki-neighbors.py example-project --page concepts/triage-rules.md
    python 06_Engine/retrieval/wiki-neighbors.py example-project "warranty" --hops 2 --top 12
    python 06_Engine/retrieval/wiki-neighbors.py example-project "warranty" --historical-overlay
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wiki_support import (
    LEGACY_GRAPH, NoteResolver, discover_programs, knowledge_pages, nearest_wiki_root,
    normalized_target, note_references,
)

REPO = Path(__file__).resolve().parents[2]
WORD_RX = re.compile(r"[a-z0-9]+")


def find_hub(arg: str) -> Path | None:
    for base in (REPO / "01_Project-Hubs", REPO / "03_Agents-and-Skills", REPO):
        for p in sorted(base.iterdir()) if base.is_dir() else []:
            if arg.lower() in p.name.lower() and (p / "_wiki" / "index.jsonl").exists():
                return p
    return None


def load_index(hub: Path) -> dict[str, dict]:
    idx = {}
    eligible = {path.relative_to(hub / "_wiki").as_posix()
                for path in knowledge_pages(hub / "_wiki", REPO)}
    for line in (hub / "_wiki" / "index.jsonl").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            r = json.loads(line)
            if r["path"] in idx:
                raise ValueError(f"{hub / '_wiki/index.jsonl'}: duplicate path {r['path']}")
            if r["path"] in eligible:
                idx[r["path"]] = r
    return idx


def norm(target: str, idx: dict) -> str | None:
    """Resolve a seed or historical key without first-match stem guessing."""
    target = normalized_target(target)
    if target is None:
        return None
    exact = [path for path in idx if path.lower().removesuffix(".md") == target]
    if len(exact) == 1:
        return exact[0]
    if exact or "/" in target:
        return None
    matches = [path for path in idx if Path(path).stem.lower() == target]
    return matches[0] if len(matches) == 1 else None


class WikiGraph(dict):
    def __init__(self, rows: dict[str, dict]):
        super().__init__((path, set()) for path in rows)
        self.rows = rows
        self.provenance: dict[tuple[str, str], set[str]] = {}
        self.historical_snapshot: str | None = None

    def add_edge(self, source: str, target: str, provenance: str) -> None:
        if source == target:
            return
        self[source].add(target)
        self[target].add(source)
        self.provenance.setdefault(tuple(sorted((source, target))), set()).add(provenance)


def build_graph(hub: Path, idx: dict, *, historical_overlay: bool = False,
                cross_hub: bool = True) -> WikiGraph:
    """Undirected authored-note adjacency; local keys remain wiki-relative."""
    wiki = hub / "_wiki"
    eligible = {path.relative_to(wiki).as_posix() for path in knowledge_pages(wiki, REPO)}
    rows = {path: row for path, row in idx.items() if path in eligible}
    paths = {path: wiki / path for path in rows}
    if cross_hub:
        for other in discover_programs(REPO):
            if other.resolve() == hub.resolve() or not (other / "_wiki/index.jsonl").is_file():
                continue
            for path, row in load_index(other).items():
                absolute = other / "_wiki" / path
                key = absolute.relative_to(REPO).as_posix()
                paths[key], rows[key] = absolute, row
    graph = WikiGraph(rows)
    resolver = NoteResolver(REPO, list(paths.values()))
    keys = {path.resolve(): key for key, path in paths.items()}
    for key, path in paths.items():
        for kind, raw in note_references(path.read_text(encoding="utf-8")):
            target, matches = resolver.resolve(path, raw, kind)
            if len(matches) != 1:
                continue
            destination = matches[0]
            if nearest_wiki_root(path) != nearest_wiki_root(destination) and "/" not in (target or ""):
                continue
            graph.add_edge(key, keys[destination.resolve()], f"authored:{kind}")
    if historical_overlay:
        sg = REPO / LEGACY_GRAPH
        data = json.loads(sg.read_text(encoding="utf-8"))
        graph.historical_snapshot = str(data.get("generated_at") or "undated")
        local = {path: row for path, row in rows.items() if path in eligible}
        for edge in data.get("edges", data.get("links", [])):
            source = norm(str(edge.get("source", "")), local)
            target = norm(str(edge.get("target", "")), local)
            if source and target:
                graph.add_edge(source, target, f"historical:{graph.historical_snapshot}")
    return graph


def score(query: str, r: dict) -> float:
    q = set(WORD_RX.findall(query.lower()))
    if not q:
        return 0.0
    hay = " ".join([r.get("title", ""), r.get("tldr", ""), r["path"],
                    " ".join(r.get("tags", []) or [])]).lower()
    toks = set(WORD_RX.findall(hay))
    overlap = len(q & toks)
    title_hits = sum(1 for w in q if w in r.get("title", "").lower())
    return overlap + 1.5 * title_hits


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hub")
    parser.add_argument("query", nargs="*")
    parser.add_argument("--page")
    parser.add_argument("--top", type=int, default=8)
    parser.add_argument("--hops", type=int, default=1)
    parser.add_argument("--local-only", action="store_true", help="do not expand into other maintained wikis")
    parser.add_argument("--historical-overlay", action="store_true",
                        help="opt in to labeled edges from the frozen semantic export")
    args = parser.parse_intermixed_args()
    if args.top < 1 or args.hops < 0:
        parser.error("--top must be positive and --hops must be nonnegative")
    hub = find_hub(args.hub)
    if not hub:
        print(f"no hub matching '{args.hub}'", file=sys.stderr)
        return 1
    idx = load_index(hub)
    adj = build_graph(hub, idx, historical_overlay=args.historical_overlay,
                      cross_hub=not args.local_only)
    query = " ".join(args.query)

    if args.page:
        seed = norm(args.page, idx)
        seeds = [seed] if seed else []
    else:
        ranked = sorted(idx.values(), key=lambda r: score(query, r), reverse=True)
        seeds = [r["path"] for r in ranked if score(query, r) > 0][:3]

    if not seeds:
        print(f"No seed page found for '{query or args.page}'. Try broader terms or read _wiki/index.md.")
        return 0

    # BFS expand
    seen = {s: 0 for s in seeds if s}
    historical_routes: dict[str, set[str]] = {seed: set() for seed in seeds}
    frontier = list(seen)
    for _ in range(args.hops):
        nxt = []
        for n in frontier:
            for m in sorted(adj.get(n, ())):
                provenance = adj.provenance[tuple(sorted((n, m)))]
                history = set() if any(p.startswith("authored:") for p in provenance) else provenance
                route = historical_routes[n] | history
                if m not in seen:
                    seen[m] = seen[n] + 1
                    historical_routes[m] = route
                    nxt.append(m)
                elif seen[m] == seen[n] + 1 and len(route) < len(historical_routes[m]):
                    historical_routes[m] = route
        frontier = nxt

    def label(p):
        r = adj.rows.get(p, {})
        return f"{p} — {r.get('title', '')}"

    print(f"# Graph neighborhood for: {query or args.page}\n")
    if adj.historical_snapshot:
        print(f"Historical overlay enabled: {adj.historical_snapshot} (not current evidence).\n")
    print("## Seeds (lexical hits)")
    for s in seeds:
        if s:
            print(f"- {label(s)}")
    neighbors = sorted((p for p in seen if p not in seeds),
                       key=lambda p: (seen[p], -len(adj.get(p, ())), p))
    print(f"\n## Neighborhood (+{args.hops} hop, {len(neighbors)} pages)")
    for p in neighbors[:args.top]:
        provenance = "historical overlay" if historical_routes[p] else "authored link"
        print(f"- [{seen[p]}h · {provenance}] {label(p)}")
    print("\n_Read the seeds first; verify the authored link or labeled historical route before relying on a neighbor._")
    return 0


def main() -> int:
    try:
        return _main()
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
