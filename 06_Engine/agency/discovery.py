"""Generated discovery links: expose catalog capabilities where agent runtimes look for them.

Copilot reads ``.github/{skills,agents,prompts}``; Claude Code reads
``.claude/{skills,agents,commands}``. Every entry the tool writes is a relative
symlink into a capability source. Unmanaged files (regular files, or links that
point elsewhere) are never replaced: they are reported as conflicts.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from .catalog import DISCOVERY_DIRS, LAYOUT, Catalog, build_catalog
from .config import AGENTS_DIR, PROMPTS_DIR, SKILLS_DIR, AgencyConfig, load_config


@dataclass(frozen=True)
class Link:
    path: Path
    target: str
    surface: str
    origin: str
    is_dir: bool


@dataclass
class Plan:
    desired: dict[Path, Link] = field(default_factory=dict)
    create: list[Link] = field(default_factory=list)
    update: list[Link] = field(default_factory=list)
    remove: list[Path] = field(default_factory=list)
    deferred: list[Path] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def drift(self) -> bool:
        return bool(self.create or self.update or self.remove or self.conflicts)

    @property
    def failed(self) -> bool:
        return self.drift or bool(self.errors)


def _normal(path: Path | str) -> str:
    return os.path.normpath(os.path.abspath(path))


def _link_target(link: Path) -> str:
    return _normal(link.parent / os.readlink(link))


def _within(path: str, roots: list[str]) -> bool:
    return any(path == root or path.startswith(root + os.sep) for root in roots)


def plan(root: Path, config: AgencyConfig | None = None, catalog: Catalog | None = None) -> Plan:
    root = Path(root)
    config = config or load_config(root)
    catalog = catalog or build_catalog(root, config)
    result = Plan(issues=list(catalog.issues), errors=list(catalog.errors))
    for item in catalog.items:
        for target in item.targets:
            if target not in config.targets:
                continue
            layout = LAYOUT.get((target, item.surface))
            if layout is None:
                continue
            directory, pattern = layout
            path = root / directory / pattern.format(name=item.name)
            # POSIX separators so links created on Windows still resolve on macOS and Linux.
            relative = os.path.relpath(item.source, path.parent).replace(os.sep, "/")
            result.desired[path] = Link(path, relative, item.surface, item.origin, item.surface == "skills")

    native_roots = [_normal(root / SKILLS_DIR), _normal(root / AGENTS_DIR), _normal(root / PROMPTS_DIR)]
    unmounted = [_normal(state.path) for state in catalog.states.values() if state.registered and not state.present]
    plugin_roots = [_normal(state.path) for state in catalog.states.values()]
    managed = native_roots + plugin_roots

    for path, link in result.desired.items():
        if path.is_symlink():
            if os.readlink(path) == link.target:
                continue
            current = _link_target(path)
            if _within(current, unmounted):
                # The name belongs to a pinned plug-in that is not checked out here; taking it over would
                # hide a collision that a checkout with the plug-in reports.
                result.conflicts.append(
                    f"{path.relative_to(root)} belongs to a plug-in that is not checked out here; "
                    f"{link.origin} also provides {link.surface} {path.name!r}. Rename one, or check the plug-in out "
                    "(agency.py plugin add <name>) to see the collision"
                )
            elif _within(current, managed):
                result.update.append(link)
            else:
                result.conflicts.append(f"{path.relative_to(root)} is an unmanaged symlink to {os.readlink(path)}")
        elif path.exists():
            result.conflicts.append(
                f"{path.relative_to(root)} is an unmanaged file; move its source into "
                f"{AGENTS_DIR if link.surface == 'agents' else SKILLS_DIR if link.surface == 'skills' else PROMPTS_DIR} "
                "so the catalog owns it"
            )
        else:
            result.create.append(link)

    for directory in DISCOVERY_DIRS:
        folder = root / directory
        if folder.is_symlink():
            result.conflicts.append(f"{directory} must be a real directory, not a symlink")
            continue
        if not folder.is_dir():
            continue
        for entry in sorted(folder.iterdir()):
            if entry in result.desired or not entry.is_symlink():
                continue
            target = _link_target(entry)
            if _within(target, unmounted):
                result.deferred.append(entry)
            elif _within(target, managed):
                result.remove.append(entry)
    return result


def apply(root: Path, result: Plan) -> None:
    if result.conflicts:
        raise RuntimeError("discovery conflicts:\n  " + "\n  ".join(result.conflicts))
    root = Path(root)
    for link in result.create + result.update:
        link.path.parent.mkdir(parents=True, exist_ok=True)
        if link.path.is_symlink():
            link.path.unlink()
        try:
            os.symlink(link.target, link.path, target_is_directory=link.is_dir)
        except OSError as error:  # pragma: no cover - platform dependent
            raise RuntimeError(
                f"could not create symlink {link.path.relative_to(root)}: {error}. On Windows enable Developer "
                "Mode and run `git config core.symlinks true`."
            ) from error
    for path in result.remove:
        path.unlink()
    for directory in DISCOVERY_DIRS:
        folder = root / directory
        if folder.is_dir() and not folder.is_symlink() and not any(folder.iterdir()):
            folder.rmdir()
    for parent in sorted({(root / directory).parent for directory in DISCOVERY_DIRS}):
        if parent != root and parent.is_dir() and not parent.is_symlink() and not any(parent.iterdir()):
            parent.rmdir()


def summary(result: Plan) -> str:
    counts: dict[str, int] = {}
    for link in result.desired.values():
        label = f"{link.path.parent.parent.name}/{link.path.parent.name}"
        counts[label] = counts.get(label, 0) + 1
    parts = ", ".join(f"{key} {value}" for key, value in sorted(counts.items())) or "no links"
    return (
        f"discovery: {parts} | create {len(result.create)}, update {len(result.update)}, "
        f"remove {len(result.remove)}, deferred {len(result.deferred)}, conflicts {len(result.conflicts)}"
    )
