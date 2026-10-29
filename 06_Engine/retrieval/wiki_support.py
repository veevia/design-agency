"""Shared tracked-wiki scope and authored note-link resolution."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

LEGACY_GRAPH = Path("06_Engine/retrieval/legacy/semantic-graph.json")

SKIP_DIRS = {"_templates", "_template", "templates", "tests", "fixtures", "evals"}
SKIP_FILES = {"index.md", "log.md", "readme.md", "_digest.md", "_gaps.md"}
SKIP_PARTS = SKIP_DIRS | {
    ".git", ".next", "dist", "node_modules", "__pycache__", "_quarantine",
    "_template-project", "web", "web_dist",
}
PLACEHOLDER_RE = re.compile(r"^<.*>$|^[xyz]$|^\.\.\.?$|^…$")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
INLINE_CODE_RE = re.compile(r"(?<!`)(`+)(?!`)[\s\S]*?(?<!`)\1(?!`)")


def tracked_markdown(root: Path, repo: Path) -> list[Path]:
    try:
        relative = root.resolve().relative_to(repo.resolve())
    except ValueError:
        return sorted(root.rglob("*.md"))
    try:
        prefix = "" if relative == Path(".") else relative.as_posix() + "/"
        prefix = re.sub(r"([\\*?\[])", r"\\\1", prefix)
        result = subprocess.run(
            ["git", "-C", str(repo), "ls-files", "-z", "--", f":(glob){prefix}**/*.md"],
            capture_output=True, text=True,
        )
    except OSError:
        result = None
    if result is None or result.returncode != 0:
        return sorted(root.rglob("*.md"))
    return sorted(repo / name for name in result.stdout.split("\0")
                  if name.endswith(".md") and (repo / name).is_file())


def discover_programs(repo: Path) -> list[Path]:
    hubs = repo / "01_Project-Hubs"
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "ls-files", "-z", "--",
             "01_Project-Hubs/*/_wiki/*", "00_Agentic-OS/_wiki/*"],
            capture_output=True, text=True,
        )
    except OSError:
        result = None
    if result is not None and result.returncode == 0:
        programs: set[Path] = set()
        for filename in result.stdout.split("\0"):
            parts = Path(filename).parts
            if len(parts) > 3 and parts[0] == "01_Project-Hubs" and parts[2] == "_wiki":
                if not parts[1].startswith("."):
                    programs.add(hubs / parts[1])
            elif len(parts) > 2 and parts[:2] == ("00_Agentic-OS", "_wiki"):
                programs.add(repo / "00_Agentic-OS")
        return sorted(programs)
    candidates = list(hubs.iterdir()) if hubs.is_dir() else []
    candidates.append(repo / "00_Agentic-OS")
    return sorted(path for path in candidates
                  if not path.name.startswith(".") and (path / "_wiki").is_dir())


def keep(path: Path) -> bool:
    return not any(part in SKIP_PARTS or part.startswith(".") for part in path.parts)


def knowledge_pages(wiki: Path, repo: Path) -> list[Path]:
    if wiki.parent.name == "_template-project":
        return []
    return [path for path in tracked_markdown(wiki, repo)
            if keep(path.relative_to(wiki)) and path.name.lower() not in SKIP_FILES]


def maintained_wiki_pages(repo: Path) -> list[Path]:
    return [page for hub in discover_programs(repo)
            for page in knowledge_pages(hub / "_wiki", repo)]


def note_targets(repo: Path) -> list[Path]:
    return [path for path in tracked_markdown(repo, repo) if keep(path.relative_to(repo))]


def without_fenced_code(text: str) -> str:
    lines: list[str] = []
    fence = ""
    for line in text.splitlines(keepends=True):
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\n"))
        if fence:
            if (match and match.group(1)[0] == fence[0]
                    and len(match.group(1)) >= len(fence) and not match.group(2).strip()):
                fence = ""
            lines.append("\n")
        elif match:
            fence = match.group(1)
            lines.append("\n")
        else:
            lines.append(line)
    return "".join(lines)


def prose_only(text: str) -> str:
    return INLINE_CODE_RE.sub("", without_fenced_code(text))


def nearest_wiki_root(path: Path) -> Path | None:
    return next((parent for parent in path.parents if parent.name == "_wiki"), None)


def normalized_target(raw: str, kind: str = "wikilink", *, casefold: bool = True) -> str | None:
    target = raw.strip()
    if kind == "wikilink":
        target = target.replace("\\|", "|").split("|", 1)[0]
    if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0].strip())
    target = re.sub(r"\\([()])", r"\1", target).replace("\\", "/")
    if casefold:
        target = target.lower()
    if not target:
        return None
    if kind == "markdown" and not target.lower().endswith(".md"):
        return None
    if target.lower().endswith(".md"):
        target = target[:-3]
    if PLACEHOLDER_RE.match(target) or PLACEHOLDER_RE.match(target.split("/")[-1]):
        return None
    return target


def note_references(text: str):
    """Yield authored wikilinks and inline Markdown note destinations, not examples."""
    prose = prose_only(text)
    for match in WIKILINK_RE.finditer(prose):
        yield "wikilink", match.group(1)
    for match in re.finditer(r"\]\(\s*", prose):
        start = match.end()
        if start < len(prose) and prose[start] == "<":
            end = prose.find(">", start + 1)
            if end >= 0 and re.match(r'\s*(?:["\'][^\n]*["\']\s*)?\)', prose[end + 1:]):
                yield "markdown", prose[start + 1:end]
            continue
        position, depth = start, 1
        while position < len(prose) and depth:
            char = prose[position]
            if char == "\\":
                position += 2
                continue
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            if depth:
                position += 1
        if not depth:
            target = re.sub(r'''\s+(?:"[^"]*"|'[^']*')\s*$''', "", prose[start:position])
            yield "markdown", target.strip()


class NoteResolver:
    """Resolve against known files; qualified misses never fall back to a guessed stem."""

    def __init__(self, repo: Path, paths: list[Path], *, allow_unindexed_targets: bool = False):
        self.repo = repo
        self.allow_unindexed_targets = allow_unindexed_targets
        self.paths = sorted(set(paths))
        self.absolute: dict[str, list[Path]] = {}
        self.stems: dict[str, list[Path]] = {}
        for path in self.paths:
            self.absolute.setdefault(str(path.resolve()).lower(), []).append(path)
            self.stems.setdefault(path.stem.lower(), []).append(path)

    def resolve(self, source: Path, raw: str, kind: str = "wikilink") -> tuple[str | None, list[Path]]:
        target = normalized_target(raw, kind)
        if target is None:
            return None, []
        spelling = normalized_target(raw, kind, casefold=False)
        wiki = nearest_wiki_root(source)
        bases = (source.parent,) if kind == "markdown" else (source.parent, wiki, self.repo)
        for base in bases:
            if base is not None:
                candidate = (base / f"{spelling}.md").resolve()
                found = self.absolute.get(str(candidate).lower())
                if found is not None:
                    return target, found
                if candidate.is_relative_to(self.repo.resolve()) and candidate.is_file():
                    return target, [candidate] if self.allow_unindexed_targets else []
        if kind == "markdown" or target.startswith((".", "/")):
            return target, []
        if "/" in target:
            return target, [path for path in self.paths
                            if path.as_posix().lower().endswith(f"/{target}.md")]
        matches = self.stems.get(target, [])
        local = [path for path in matches if wiki is not None and path.is_relative_to(wiki)]
        return target, local or matches


def obsidian_graph_query() -> str:
    scope = (r'path:/^(01_Project-Hubs\/[^/]+\/_wiki\/|00_Agentic-OS\/_wiki\/|'
             r'00_Agentic-OS\/decisions\/l[0-5]-|00_README\/ARCHITECTURE\.md$)/')
    excluded = "|".join(re.escape(name) for name in sorted(SKIP_PARTS) if not name.startswith("."))
    metadata = "|".join(re.escape(name) for name in sorted(SKIP_FILES))
    return f'{scope} -path:/\\/(?:{excluded})\\// -file:/^(?:{metadata})$/'
