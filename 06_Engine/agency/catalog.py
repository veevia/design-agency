"""Native capabilities and the unified catalog consumed by discovery, lint and the review.

Native sources (host-owned, one file per capability, depth parity with discovery):
  skills  03_Agents-and-Skills/Skills/<slug>/SKILL.md
  agents  03_Agents-and-Skills/Agents/<slug>.agent.md
  prompts 02_Workflows/prompts/<name>.prompt.md
Plug-in contributions come from mounted plug-ins (see ``plugins.py``). Native
*host adapters* named in a profile's ``host_adapters`` (for example the PDG
prompt) are exposed only while that plug-in is plugged in.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .config import AGENTS_DIR, PROMPTS_DIR, SKILLS_DIR, SOPS_DIR, AgencyConfig, load_config
from .plugins import (
    DEFAULT_TARGETS,
    Contribution,
    PluginState,
    contributions,
    load_profiles,
    mount_of,
    plugin_states,
)

SKILL_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
NATIVE = "native"

# (runtime target, surface) -> (discovery directory, link-name pattern)
LAYOUT: dict[tuple[str, str], tuple[str, str]] = {
    ("copilot", "skills"): (".github/skills", "{name}"),
    ("copilot", "agents"): (".github/agents", "{name}.agent.md"),
    ("copilot", "prompts"): (".github/prompts", "{name}.prompt.md"),
    ("claude", "skills"): (".claude/skills", "{name}"),
    ("claude", "agents"): (".claude/agents", "{name}.md"),
    ("claude", "claude_agents"): (".claude/agents", "{name}.md"),
    ("claude", "prompts"): (".claude/commands", "{name}.md"),
}
DISCOVERY_DIRS = tuple(sorted({directory for directory, _ in LAYOUT.values()}))


class CatalogError(ValueError):
    """Two capabilities claim the same discovery name, or a source is invalid."""


@dataclass(frozen=True)
class Catalog:
    items: tuple[Contribution, ...]
    issues: tuple[str, ...]           # warnings and notes
    gated: dict[str, dict[str, str]]  # surface -> {native name: plug-in that unlocks it}
    states: dict[str, PluginState]
    errors: tuple[str, ...] = ()      # blocking: broken contributions or adapter declarations


def repo_root_from_skills(skills_root: Path) -> Path:
    return Path(skills_root).resolve().parents[1]


def plugin_mount_paths(root: Path, config: AgencyConfig | None = None) -> set[Path]:
    config = config or load_config(root)
    return {(Path(root) / mount_of(profile, config)).resolve() for profile in load_profiles(root).values()}


def native_skill_dirs(skills_root: Path) -> list[Path]:
    """Flat native skills; plug-in mounts and `_`/`.` folders are excluded."""
    skills_root = Path(skills_root)
    if not skills_root.is_dir():
        return []
    mounts = plugin_mount_paths(repo_root_from_skills(skills_root))
    found = []
    for child in sorted(skills_root.iterdir()):
        if not child.is_dir() or child.name.startswith((".", "_")) or child.resolve() in mounts:
            continue
        if (child / "SKILL.md").is_file():
            found.append(child)
    return found


def iter_skill_dirs(skills_root: Path) -> list[Path]:
    """Skills the host lints and owns: native skills only (plug-ins carry their own checks)."""
    return native_skill_dirs(skills_root)


def native_agents(root: Path) -> list[Path]:
    directory = Path(root) / AGENTS_DIR
    return sorted(directory.glob("*.agent.md")) if directory.is_dir() else []


def native_prompts(root: Path) -> list[Path]:
    directory = Path(root) / PROMPTS_DIR
    return sorted(directory.glob("*.prompt.md")) if directory.is_dir() else []


def build_catalog(root: Path, config: AgencyConfig | None = None) -> Catalog:
    root = Path(root)
    config = config or load_config(root)
    states = plugin_states(root, config)
    errors: list[str] = []
    native_exists = {
        "prompts": lambda name: (root / PROMPTS_DIR / f"{name}.prompt.md").is_file(),
        "agents": lambda name: (root / AGENTS_DIR / f"{name}.agent.md").is_file(),
        "skills": lambda name: (root / SKILLS_DIR / name / "SKILL.md").is_file(),
        "sops": lambda name: (root / SOPS_DIR / name / "SOP.md").is_file(),
    }
    claimed_by: dict[tuple[str, str], str] = {}
    gated: dict[str, dict[str, str]] = {surface: {} for surface in ("skills", "agents", "prompts", "sops")}
    for state in states.values():
        for surface, names in state.profile.host_adapters.items():
            for name in names:
                if not native_exists[surface](name):
                    errors.append(f"{state.profile.name}: host adapter {surface}/{name} does not exist in this repository")
                if (surface, name) in claimed_by:
                    errors.append(f"host adapter {surface}/{name} is claimed by {claimed_by[(surface, name)]} and {state.profile.name}")
                claimed_by[(surface, name)] = state.profile.name
                # Adapters follow the pin, not the checkout, so a clone without submodules sees the same catalog.
                if not state.in_repository:
                    gated[surface][name] = state.profile.name
    items: list[Contribution] = []
    issues: list[str] = []
    for directory in native_skill_dirs(root / SKILLS_DIR):
        if directory.name not in gated["skills"]:
            items.append(Contribution("skills", directory.name, directory, NATIVE, DEFAULT_TARGETS["skills"]))
    for path in native_agents(root):
        name = path.name[: -len(".agent.md")]
        if name not in gated["agents"]:
            items.append(Contribution("agents", name, path, NATIVE, ("copilot", "claude")))
    for path in native_prompts(root):
        name = path.name[: -len(".prompt.md")]
        if name not in gated["prompts"]:
            items.append(Contribution("prompts", name, path, NATIVE, ("copilot", "claude")))
    for state in states.values():
        found, plugin_errors, plugin_issues = contributions(state)
        items.extend(found)
        errors.extend(f"{state.profile.name}: {error}" for error in plugin_errors)
        issues.extend(f"{state.profile.name}: {issue}" for issue in plugin_issues)
        issues.extend(f"{state.profile.name}: {issue}" for issue in state.issues)
    claimed: dict[str, Contribution] = {}
    for item in items:
        for target in item.targets:
            layout = LAYOUT.get((target, item.surface))
            if layout is None:
                continue
            link = f"{layout[0]}/{layout[1].format(name=item.name)}"
            other = claimed.get(link)
            if other is not None and other.source != item.source:
                raise CatalogError(
                    f"{link} is claimed by {other.origin} ({other.source}) and {item.origin} ({item.source}); "
                    "rename one capability or add an `exclude:` to the plug-in profile"
                )
            claimed[link] = item
    return Catalog(tuple(items), tuple(issues), gated, states, tuple(errors))


def binding_coverage(catalog: Catalog) -> dict[str, dict]:
    """For each plugged-in engine that declares skill bindings: which bound skills this host resolves.

    `gaps` are missing skills a host is expected to supply (natively or through the profile's
    `companions`); `tenant` are missing skills the profile declares as tenant integrations, which a
    blank template never ships and a fork supplies itself.
    """
    from .plugins import bound_skills

    available = {item.name for item in catalog.items if item.surface == "skills"}
    coverage: dict[str, dict] = {}
    for name, state in catalog.states.items():
        bound = bound_skills(state)
        if bound is None:
            continue
        spec = state.profile.skill_bindings or {}
        tenant = set(spec.get("tenant_skills") or ())
        missing = [skill for skill in bound if skill not in available]
        companions = []
        for companion in spec.get("companions") or ():
            other = catalog.states.get(companion["plugin"])
            plugged = bool(other and other.enabled and companion["edition"] in (None, other.edition))
            companions.append({**companion, "plugged_in": plugged})
        coverage[name] = {
            "bound": bound,
            "resolved": [skill for skill in bound if skill in available],
            "missing": missing,
            "gaps": [skill for skill in missing if skill not in tenant],
            "tenant": [skill for skill in missing if skill in tenant],
            "companions": companions,
        }
    return coverage


def companion_hint(entry: dict) -> str:
    """`plugin add` commands for the companions an engine still needs ('' when none are missing)."""
    wanted = [c for c in entry.get("companions", []) if not c["plugged_in"]]
    return "; ".join(
        f"agency.py plugin add {c['plugin']}" + (f" --edition {c['edition']}" if c["edition"] else "") for c in wanted
    )


def find_skill_dir(skills_root: Path, slug: str) -> Path | None:
    for directory in native_skill_dirs(skills_root):
        if directory.name == slug:
            return directory
    catalog = build_catalog(repo_root_from_skills(skills_root))
    for item in catalog.items:
        if item.surface == "skills" and item.name == slug:
            return item.source
    return None


def canonical_skill_map(skills_root: Path) -> dict[str, Path]:
    """Every discoverable skill (native + plugged-in plug-ins) by name."""
    catalog = build_catalog(repo_root_from_skills(skills_root))
    skills = {item.name: item.source for item in catalog.items if item.surface == "skills"}
    if not skills:
        raise ValueError(f"no skills found in {skills_root}")
    return dict(sorted(skills.items()))
