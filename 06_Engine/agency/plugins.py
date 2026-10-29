"""Plug-in profiles, mount state, capability contributions and lifecycle operations.

A *profile* (``06_Engine/plugins/<name>.plugin.yaml``) tells the host how to mount,
recognise, wire and check one external capability package. A plug-in is
*plugged in* when its mount is checked out and an edition marker is found; there
is no separate enabled flag to drift. ``agency.yaml`` may override the mount,
edition, source or hide a mounted plug-in with ``enabled: false``.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from .config import (
    PROFILES_DIR,
    AgencyConfig,
    ConfigError,
    PluginOverride,
    load_config,
    repo_path,
    require_yaml,
)

PROFILE_SCHEMA = "agency-plugin/v1"
PROFILE_SUFFIX = ".plugin.yaml"
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KINDS = ("skills", "engine", "mixed")
SURFACES = ("skills", "agents", "claude_agents", "prompts")
DEFAULT_TARGETS = {
    "skills": ("copilot", "claude"),
    "agents": ("copilot",),
    "claude_agents": ("claude",),
    "prompts": ("copilot", "claude"),
}
ADAPTER_SURFACES = ("prompts", "agents", "skills", "sops")
SIDE_EFFECTS = ("none", "temp", "mount")
PLACEHOLDERS = ("{python}", "{tmp}", "{mount}", "{root}")

_PROFILE_KEYS = {
    "schema", "name", "title", "summary", "kind", "homepage", "license", "mount",
    "default_edition", "editions", "requires", "host_adapters", "project",
    "provides", "checks", "smoke", "skill_bindings",
}
_BINDING_KEYS = {"file", "collection", "field"}
_BINDING_OPTIONAL_KEYS = {"companions", "tenant_skills"}
_COMPANION_KEYS = {"plugin", "edition"}
_EDITION_KEYS = {"source", "branch", "marker", "provides", "provides_from", "command_prefix", "checks", "smoke", "summary",
                 "shallow"}
_RULE_KEYS = {"glob", "prefix", "exclude", "targets"}
_CHECK_KEYS = {"name", "run", "side_effects", "timeout", "requires", "cwd", "summary", "env", "optional"}
_REQUIRES_KEYS = {"python", "python_modules", "commands", "optional_commands"}
_PROJECT_KEYS = {"marker", "state_dir", "location"}


class PluginError(RuntimeError):
    """A plug-in profile, mount or lifecycle operation failed."""


@dataclass(frozen=True)
class Rule:
    glob: str
    prefix: str = ""
    exclude: tuple[str, ...] = ()
    targets: tuple[str, ...] | None = None


@dataclass(frozen=True)
class Check:
    name: str
    run: tuple[str, ...]
    side_effects: str = "none"
    timeout: int = 900
    requires: tuple[str, ...] = ()
    cwd: str = "mount"
    summary: str = ""
    env: tuple[tuple[str, str], ...] = ()
    optional: bool = False


@dataclass(frozen=True)
class Edition:
    name: str
    source: str
    branch: str | None
    marker: str
    provides: dict[str, tuple[Rule, ...]]
    provides_from: str | None
    command_prefix: str
    checks: tuple[Check, ...]
    smoke: tuple[Check, ...]
    summary: str = ""
    shallow: bool = False   # mount with history depth 1 and record `shallow = true` in .gitmodules


@dataclass(frozen=True)
class Profile:
    name: str
    title: str
    summary: str
    kind: str
    homepage: str
    license: str
    mount: PurePosixPath
    default_edition: str
    editions: dict[str, Edition]
    requires: dict
    host_adapters: dict[str, tuple[str, ...]]
    project: dict
    path: Path
    skill_bindings: dict | None = None


@dataclass(frozen=True)
class PluginState:
    profile: Profile
    mount: PurePosixPath
    path: Path
    registered: bool
    present: bool
    edition: str | None
    override: PluginOverride
    issues: tuple[str, ...] = ()
    pinned: bool = False

    @property
    def recognized(self) -> bool:
        """Checked out and identified by an edition marker (checks can run)."""
        return self.present and self.edition is not None

    @property
    def enabled(self) -> bool:
        """Recognized and not hidden by `enabled: false` (contributes to discovery)."""
        return self.recognized and self.override.enabled is not False

    @property
    def in_repository(self) -> bool:
        """Part of this repository (registered or checked out) and not hidden: its host adapters are unlocked."""
        return (self.registered or self.recognized) and self.override.enabled is not False

    @property
    def status(self) -> str:
        if self.override.enabled is False:
            return "disabled"
        if self.present and self.edition:
            return "enabled"
        if self.present:
            return "unrecognized"
        if self.registered:
            return "not-checked-out"
        return "available"

    @property
    def edition_spec(self) -> Edition | None:
        return self.profile.editions.get(self.edition) if self.edition else None


@dataclass(frozen=True)
class Contribution:
    surface: str
    name: str
    source: Path
    origin: str
    targets: tuple[str, ...]


@dataclass
class CheckResult:
    name: str
    ok: bool
    returncode: int | None
    seconds: float
    detail: str = ""
    skipped: str = ""


# --------------------------------------------------------------------------- profiles


def _str(data: dict, key: str, where: str, *, required: bool = True, default: str = "") -> str:
    value = data.get(key, None)
    if value is None:
        if required:
            raise ConfigError(f"{where}: `{key}` is required")
        return default
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{where}: `{key}` must be a non-empty string")
    return value.strip()


def _str_list(value: object, where: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ConfigError(f"{where} must be a list of non-empty strings")
    return tuple(item.strip() for item in value)


def _unknown(data: dict, allowed: set[str], where: str) -> None:
    extra = set(data) - allowed
    if extra:
        raise ConfigError(f"{where}: unknown keys {sorted(extra)}; allowed {sorted(allowed)}")


def _rule(value: object, surface: str, where: str) -> Rule:
    if isinstance(value, str):
        value = {"glob": value}
    if not isinstance(value, dict):
        raise ConfigError(f"{where}: a rule is a glob string or a mapping")
    _unknown(value, _RULE_KEYS, where)
    glob = _str(value, "glob", where)
    if glob.startswith("/") or ".." in PurePosixPath(glob).parts:
        raise ConfigError(f"{where}: glob must stay inside the mount: {glob!r}")
    if surface == "skills" and not glob.endswith("SKILL.md"):
        raise ConfigError(f"{where}: skill globs must end with SKILL.md")
    targets = None
    if "targets" in value:
        targets = _str_list(value["targets"], f"{where}.targets")
        if not targets or any(t not in DEFAULT_TARGETS[surface] + ("copilot", "claude") for t in targets):
            raise ConfigError(f"{where}.targets must list copilot and/or claude")
    prefix = value.get("prefix", "")
    if not isinstance(prefix, str) or (prefix and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*-?", prefix)):
        raise ConfigError(f"{where}.prefix must be lowercase kebab-case")
    return Rule(glob=glob, prefix=prefix, exclude=_str_list(value.get("exclude"), f"{where}.exclude"), targets=targets)


def _provides(value: object, where: str) -> dict[str, tuple[Rule, ...]]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ConfigError(f"{where} must map surfaces to rules")
    _unknown(value, set(SURFACES), where)
    out: dict[str, tuple[Rule, ...]] = {}
    for surface, rules in value.items():
        if not isinstance(rules, list):
            raise ConfigError(f"{where}.{surface} must be a list of rules")
        out[surface] = tuple(_rule(rule, surface, f"{where}.{surface}[{i}]") for i, rule in enumerate(rules))
    return out


def _checks(value: object, where: str) -> tuple[Check, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ConfigError(f"{where} must be a list of checks")
    checks = []
    for index, item in enumerate(value):
        at = f"{where}[{index}]"
        if not isinstance(item, dict):
            raise ConfigError(f"{at} must be a mapping")
        _unknown(item, _CHECK_KEYS, at)
        run = _str_list(item.get("run"), f"{at}.run")
        if not run:
            raise ConfigError(f"{at}.run must be a non-empty argument list")
        effects = item.get("side_effects", "none")
        if effects not in SIDE_EFFECTS:
            raise ConfigError(f"{at}.side_effects must be one of {SIDE_EFFECTS}")
        timeout = item.get("timeout", 900)
        if not isinstance(timeout, int) or timeout <= 0:
            raise ConfigError(f"{at}.timeout must be a positive integer (seconds)")
        cwd = item.get("cwd", "mount")
        if cwd not in ("mount", "root"):
            raise ConfigError(f"{at}.cwd must be mount or root")
        env = item.get("env") or {}
        if not isinstance(env, dict) or not all(
            isinstance(k, str) and re.fullmatch(r"[A-Z_][A-Z0-9_]*", k) and isinstance(v, str) for k, v in env.items()
        ):
            raise ConfigError(f"{at}.env must map UPPER_CASE names to strings")
        optional = item.get("optional", False)
        if not isinstance(optional, bool):
            raise ConfigError(f"{at}.optional must be true or false")
        checks.append(Check(
            name=_str(item, "name", at), run=run, side_effects=effects, timeout=timeout,
            requires=_str_list(item.get("requires"), f"{at}.requires"), cwd=cwd,
            summary=_str(item, "summary", at, required=False), env=tuple(sorted(env.items())), optional=optional,
        ))
    names = [check.name for check in checks]
    if len(set(names)) != len(names):
        raise ConfigError(f"{where}: check names must be unique")
    return tuple(checks)


def _companions(value: object, where: str) -> tuple[dict[str, str | None], ...]:
    """Plug-ins that supply skills an engine binds: `name` or {plugin, edition}."""
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ConfigError(f"{where} must be a list")
    out = []
    for index, item in enumerate(value):
        at = f"{where}[{index}]"
        item = {"plugin": item} if isinstance(item, str) else item
        if not isinstance(item, dict):
            raise ConfigError(f"{at} must be a plug-in name or a mapping")
        _unknown(item, _COMPANION_KEYS, at)
        plugin = _str(item, "plugin", at)
        edition = item.get("edition")
        if not NAME.fullmatch(plugin) or (edition is not None and (not isinstance(edition, str) or not NAME.fullmatch(edition))):
            raise ConfigError(f"{at}: plug-in and edition names are lowercase kebab-case")
        out.append({"plugin": plugin, "edition": edition})
    return tuple(out)


def parse_profile(data: object, path: Path) -> Profile:
    where = path.name
    if not isinstance(data, dict):
        raise ConfigError(f"{where}: profile must be a mapping")
    _unknown(data, _PROFILE_KEYS, where)
    if data.get("schema") != PROFILE_SCHEMA:
        raise ConfigError(f"{where}: schema must be {PROFILE_SCHEMA!r}")
    name = _str(data, "name", where)
    if not NAME.fullmatch(name):
        raise ConfigError(f"{where}: name must be lowercase kebab-case")
    if path.name != f"{name}{PROFILE_SUFFIX}":
        raise ConfigError(f"{where}: file must be named {name}{PROFILE_SUFFIX}")
    kind = _str(data, "kind", where)
    if kind not in KINDS:
        raise ConfigError(f"{where}: kind must be one of {KINDS}")
    shared_provides = _provides(data.get("provides"), f"{where}.provides")
    shared_checks = _checks(data.get("checks"), f"{where}.checks")
    shared_smoke = _checks(data.get("smoke"), f"{where}.smoke")
    editions_raw = data.get("editions")
    if not isinstance(editions_raw, dict) or not editions_raw:
        raise ConfigError(f"{where}: editions must be a non-empty mapping")
    editions: dict[str, Edition] = {}
    for edition_name, raw in editions_raw.items():
        at = f"{where}.editions.{edition_name}"
        if not isinstance(edition_name, str) or not NAME.fullmatch(edition_name):
            raise ConfigError(f"{at}: edition names are lowercase kebab-case")
        if not isinstance(raw, dict):
            raise ConfigError(f"{at} must be a mapping")
        _unknown(raw, _EDITION_KEYS, at)
        marker = _str(raw, "marker", at)
        repo_path(marker, field_name=f"{at}.marker")
        provides = {surface: tuple(rules) for surface, rules in shared_provides.items()}
        for surface, rules in _provides(raw.get("provides"), f"{at}.provides").items():
            provides[surface] = provides.get(surface, ()) + rules
        provides_from = raw.get("provides_from")
        if provides_from not in (None, "claude-plugin"):
            raise ConfigError(f"{at}.provides_from supports only 'claude-plugin'")
        prefix = raw.get("command_prefix", "")
        if not isinstance(prefix, str):
            raise ConfigError(f"{at}.command_prefix must be a string")
        checks = shared_checks + _checks(raw.get("checks"), f"{at}.checks")
        smoke = shared_smoke + _checks(raw.get("smoke"), f"{at}.smoke")
        for group in (checks, smoke):
            names = [check.name for check in group]
            if len(set(names)) != len(names):
                raise ConfigError(f"{at}: duplicate check names across shared and edition checks")
        branch = raw.get("branch")
        if branch is not None and (not isinstance(branch, str) or not branch.strip()):
            raise ConfigError(f"{at}.branch must be a non-empty string")
        shallow = raw.get("shallow", False)
        if not isinstance(shallow, bool):
            raise ConfigError(f"{at}.shallow must be true or false")
        editions[edition_name] = Edition(
            name=edition_name, source=_str(raw, "source", at), branch=branch, marker=marker,
            provides=provides, provides_from=provides_from, command_prefix=prefix,
            checks=checks, smoke=smoke, summary=_str(raw, "summary", at, required=False), shallow=shallow,
        )
    default_edition = _str(data, "default_edition", where, required=False, default=next(iter(editions)))
    if default_edition not in editions:
        raise ConfigError(f"{where}: default_edition {default_edition!r} is not a declared edition")
    requires = data.get("requires") or {}
    if not isinstance(requires, dict):
        raise ConfigError(f"{where}.requires must be a mapping")
    _unknown(requires, _REQUIRES_KEYS, f"{where}.requires")
    python = requires.get("python")
    if python is not None and (not isinstance(python, str) or not re.fullmatch(r"3\.\d+", python)):
        raise ConfigError(f"{where}.requires.python must look like '3.11'")
    for key in ("python_modules", "commands", "optional_commands"):
        _str_list(requires.get(key), f"{where}.requires.{key}")
    adapters_raw = data.get("host_adapters") or {}
    if not isinstance(adapters_raw, dict):
        raise ConfigError(f"{where}.host_adapters must be a mapping")
    _unknown(adapters_raw, set(ADAPTER_SURFACES), f"{where}.host_adapters")
    host_adapters = {key: _str_list(value, f"{where}.host_adapters.{key}") for key, value in adapters_raw.items()}
    project = data.get("project") or {}
    if not isinstance(project, dict):
        raise ConfigError(f"{where}.project must be a mapping")
    _unknown(project, _PROJECT_KEYS, f"{where}.project")
    bindings = data.get("skill_bindings")
    if bindings is not None:
        if not isinstance(bindings, dict):
            raise ConfigError(f"{where}.skill_bindings must be a mapping")
        _unknown(bindings, _BINDING_KEYS | _BINDING_OPTIONAL_KEYS, f"{where}.skill_bindings")
        for key in _BINDING_KEYS:
            _str(bindings, key, f"{where}.skill_bindings")
        repo_path(bindings["file"], field_name=f"{where}.skill_bindings.file")
        bindings = {
            **{key: bindings[key] for key in _BINDING_KEYS},
            "companions": _companions(bindings.get("companions"), f"{where}.skill_bindings.companions"),
            "tenant_skills": _str_list(bindings.get("tenant_skills"), f"{where}.skill_bindings.tenant_skills"),
        }
        for skill in bindings["tenant_skills"]:
            if not NAME.fullmatch(skill):
                raise ConfigError(f"{where}.skill_bindings.tenant_skills: {skill!r} is not a skill name")
    return Profile(
        name=name,
        title=_str(data, "title", where),
        summary=_str(data, "summary", where),
        kind=kind,
        homepage=_str(data, "homepage", where, required=False),
        license=_str(data, "license", where, required=False),
        mount=repo_path(_str(data, "mount", where), field_name=f"{where}.mount"),
        default_edition=default_edition,
        editions=editions,
        requires=requires,
        host_adapters=host_adapters,
        project=project,
        path=path,
        skill_bindings=bindings,
    )


def profile_dir(root: Path) -> Path:
    return Path(root) / PROFILES_DIR


def load_profiles(root: Path) -> dict[str, Profile]:
    """Load every profile; raise ConfigError naming the first invalid file."""
    yaml = require_yaml()
    profiles: dict[str, Profile] = {}
    directory = profile_dir(root)
    if not directory.is_dir():
        return profiles
    for path in sorted(directory.glob(f"*{PROFILE_SUFFIX}")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as error:
            raise ConfigError(f"{path.name}: invalid YAML: {error}") from error
        profile = parse_profile(data, path)
        profiles[profile.name] = profile
    mounts: dict[PurePosixPath, str] = {}
    for profile in profiles.values():
        if profile.mount in mounts:
            raise ConfigError(f"profiles {mounts[profile.mount]} and {profile.name} share mount {profile.mount}")
        mounts[profile.mount] = profile.name
    for profile in profiles.values():
        listed: set[str] = set()
        for companion in (profile.skill_bindings or {}).get("companions", ()):
            other = profiles.get(companion["plugin"])
            if other is None or other.name == profile.name:
                raise ConfigError(f"{profile.path.name}: companion {companion['plugin']!r} is not another plug-in profile")
            if companion["edition"] and companion["edition"] not in other.editions:
                raise ConfigError(f"{profile.path.name}: companion {other.name} has no edition {companion['edition']!r}")
            if other.name in listed:  # one mount holds one edition
                raise ConfigError(f"{profile.path.name}: companion {other.name} is listed more than once")
            listed.add(other.name)
    return profiles


# --------------------------------------------------------------------------- state


def read_gitmodules(root: Path) -> dict[str, dict[str, str]]:
    """Map submodule path → {name, url, branch} without invoking git."""
    path = Path(root) / ".gitmodules"
    if not path.is_file():
        return {}
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith(("#", ";")):
            continue
        header = re.fullmatch(r'\[submodule\s+"(.+)"\]', line)
        if header:
            current = {"name": header.group(1)}
            entries.append(current)
            continue
        if current is not None and "=" in line:
            key, _, value = line.partition("=")
            current[key.strip()] = value.strip()
    return {entry["path"].rstrip("/"): entry for entry in entries if "path" in entry}


def _has_content(path: Path) -> bool:
    try:
        return path.is_dir() and any(child.name != ".git" for child in path.iterdir())
    except OSError:
        return False


def mount_of(profile: Profile, config: AgencyConfig) -> PurePosixPath:
    override = config.plugins.get(profile.name, PluginOverride())
    return override.mount or profile.mount


def detect_edition(profile: Profile, path: Path, preferred: str | None = None) -> str | None:
    if preferred and preferred in profile.editions and (path / profile.editions[preferred].marker).exists():
        return preferred
    for name, edition in profile.editions.items():
        if (path / edition.marker).exists():
            return name
    return None


def plugin_state(root: Path, profile: Profile, config: AgencyConfig | None = None) -> PluginState:
    root = Path(root)
    config = config or load_config(root)
    override = config.plugins.get(profile.name, PluginOverride())
    mount = mount_of(profile, config)
    path = root / mount
    registered = str(mount) in read_gitmodules(root)
    present = _has_content(path)
    pinned = _has_gitlink(root, mount)
    issues: list[str] = []
    edition = None
    if present and not registered:
        issues.append("checked-out content is not a registered submodule (a copy or manual clone); plug-ins mount as pinned submodules")
    if registered and not pinned and (root / ".git").exists():
        issues.append("registered in .gitmodules without a pinned gitlink in the index")
    if present:
        edition = detect_edition(profile, path, override.edition)
        if edition is None:
            markers = ", ".join(sorted({e.marker for e in profile.editions.values()}))
            issues.append(f"mount has content but no edition marker ({markers})")
        elif override.edition and edition != override.edition:
            issues.append(f"agency.yaml asks for edition {override.edition!r} but the mount is {edition!r}")
    elif registered:
        issues.append(f"registered in .gitmodules but not checked out; run: python3 06_Engine/scripts/agency.py plugin add {profile.name}")
    return PluginState(profile, mount, path, registered, present, edition, override, tuple(issues), pinned)


def plugin_states(root: Path, config: AgencyConfig | None = None) -> dict[str, PluginState]:
    config = config or load_config(root)
    profiles = load_profiles(root)
    unknown = set(config.plugins) - set(profiles)
    if unknown:
        raise ConfigError(f"agency.yaml overrides unknown plug-ins: {sorted(unknown)}")
    effective = sorted((mount_of(profile, config).parts, name) for name, profile in profiles.items())
    for (left, left_name), (right, right_name) in zip(effective, effective[1:]):
        if right[: len(left)] == left:
            raise ConfigError(
                f"plug-ins {left_name} and {right_name} have overlapping mounts ({'/'.join(left)}, {'/'.join(right)})"
            )
    return {name: plugin_state(root, profile, config) for name, profile in profiles.items()}


def _has_gitlink(root: Path, mount: PurePosixPath) -> bool:
    """True when the index pins the mount as a submodule commit (mode 160000)."""
    if not (Path(root) / ".git").exists():
        return False
    result = subprocess.run(["git", "ls-files", "-s", "--", str(mount)], cwd=root, capture_output=True, text=True)
    return any(line.startswith("160000 ") for line in result.stdout.splitlines())


def edition_of_source(profile: Profile, url: str) -> str | None:
    """Identify the edition a registered source URL belongs to (checkout-independent)."""
    for name, edition in profile.editions.items():
        if url and _same_source(url, edition.source):
            return name
    return None


# --------------------------------------------------------------------------- contributions


def _claude_plugin_rules(path: Path, edition: Edition) -> dict[str, tuple[Rule, ...]]:
    manifest = path / ".claude-plugin" / "plugin.json"
    if not manifest.is_file():
        raise PluginError(f"{manifest} not found (edition {edition.name} uses provides_from: claude-plugin)")
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise PluginError(f"{manifest}: invalid JSON: {error}") from error

    def entries(key: str, default: str) -> list[str]:
        value = data.get(key)
        if value is None:
            # An undeclared default folder counts only if it holds what the convention expects: plug-ins in
            # the shared skills format often keep other runtimes' metadata there (e.g. agents/openai.yaml).
            folder = path / default
            expected = "*/SKILL.md" if key == "skills" else "*.md"
            return [default] if folder.is_dir() and any(folder.glob(expected)) else []
        items = [value] if isinstance(value, str) else value
        if not isinstance(items, list) or not all(isinstance(item, str) for item in items):
            raise PluginError(f"{manifest}: `{key}` must be a path or list of paths")
        cleaned = []
        for item in items:
            relative = PurePosixPath(item.strip())
            relative = PurePosixPath(*[part for part in relative.parts if part != "."]) if relative.parts else relative
            if relative.is_absolute() or ".." in relative.parts:
                raise PluginError(f"{manifest}: `{key}` entry leaves the plug-in: {item!r}")
            cleaned.append(str(relative))
        return cleaned

    rules: dict[str, list[Rule]] = {"skills": [], "claude_agents": [], "prompts": []}
    for directory in entries("skills", "skills"):
        # Claude manifests list either a folder of skills or one skill folder ("./" = the plug-in is one skill).
        base = "" if directory in ("", ".") else f"{directory}/"
        glob = f"{base}SKILL.md" if (path / directory / "SKILL.md").is_file() else f"{base}*/SKILL.md"
        rules["skills"].append(Rule(glob=glob))
    for item in entries("agents", "agents"):
        glob = item if item.endswith(".md") else f"{item}/*.md"
        rules["claude_agents"].append(Rule(glob=glob))
    for item in entries("commands", "commands"):
        glob = item if item.endswith(".md") else f"{item}/*.md"
        rules["prompts"].append(Rule(glob=glob, prefix=edition.command_prefix, targets=("claude",)))
    return {surface: tuple(values) for surface, values in rules.items() if values}


def _capability_name(surface: str, match: Path, rule: Rule) -> str:
    if surface == "skills":
        stem = match.parent.name
    elif match.name.endswith(".agent.md"):
        stem = match.name[: -len(".agent.md")]
    elif match.name.endswith(".prompt.md"):
        stem = match.name[: -len(".prompt.md")]
    else:
        stem = match.stem
    return f"{rule.prefix}{stem}" if rule.prefix and not stem.startswith(rule.prefix) else stem


def contributions(state: PluginState) -> tuple[list[Contribution], list[str], list[str]]:
    """Capabilities a plugged-in plug-in contributes, plus errors (layout drift) and warnings."""
    if not state.enabled:
        return [], [], []
    edition = state.edition_spec
    assert edition is not None
    rules: dict[str, tuple[Rule, ...]] = dict(edition.provides)
    if edition.provides_from == "claude-plugin":
        for surface, derived in _claude_plugin_rules(state.path, edition).items():
            rules[surface] = derived + rules.get(surface, ())
    found: list[Contribution] = []
    errors: list[str] = []
    issues: list[str] = []
    seen: dict[tuple[str, str], Path] = {}
    root = state.path.resolve()
    for surface, surface_rules in rules.items():
        for rule in surface_rules:
            matches = sorted(state.path.glob(rule.glob))
            if not matches:
                errors.append(f"{surface} rule {rule.glob!r} matched nothing (the plug-in layout changed?)")
            for match in matches:
                if not match.is_file():
                    continue
                if not match.resolve().is_relative_to(root):
                    issues.append(f"{match} resolves outside the mount; skipped")
                    continue
                name = _capability_name(surface, match, rule)
                if name in rule.exclude or match.parent.name in rule.exclude:
                    continue
                if not NAME.fullmatch(name) or len(name) > 64:
                    issues.append(f"{surface} name {name!r} from {match.relative_to(state.path)} is not lowercase kebab-case; skipped")
                    continue
                source = match.parent if surface == "skills" else match
                key = (surface, name)
                if key in seen:
                    if seen[key] != source:
                        issues.append(f"duplicate {surface} name {name!r}: {seen[key]} and {source}")
                    continue
                seen[key] = source
                found.append(Contribution(surface, name, source, state.profile.name, rule.targets or DEFAULT_TARGETS[surface]))
    return found, errors, issues


def bound_skills(state: PluginState) -> list[str] | None:
    """Skills an engine's own workflow binds (from the profile's `skill_bindings`), or None if not declared."""
    spec = state.profile.skill_bindings
    if not spec or not state.recognized:
        return None
    yaml = require_yaml()
    source = state.path / spec["file"]
    if not source.is_file():
        raise PluginError(f"{state.profile.name}: skill_bindings file {spec['file']} is missing from the mount")
    data = yaml.safe_load(source.read_text(encoding="utf-8")) or {}
    items = data.get(spec["collection"]) if isinstance(data, dict) else None
    if not isinstance(items, list):
        raise PluginError(f"{state.profile.name}: {spec['file']} has no `{spec['collection']}` list")
    names = {name for item in items if isinstance(item, dict)
             for name in (item.get(spec["field"]) or []) if isinstance(name, str)}
    return sorted(names)


# --------------------------------------------------------------------------- checks


def resolve_python(state: PluginState, explicit: str | None = None) -> str:
    if explicit:
        return explicit
    if os.environ.get("AGENCY_PYTHON"):
        return os.environ["AGENCY_PYTHON"]
    for candidate in (state.path / ".venv" / "bin" / "python", state.path / ".venv" / "Scripts" / "python.exe"):
        if candidate.exists():
            return str(candidate)
    return sys.executable


def requirement_issues(state: PluginState, python: str) -> list[str]:
    requires = state.profile.requires
    issues: list[str] = []
    wanted = requires.get("python")
    probe = subprocess.run(
        [python, "-c", "import sys; print('%d.%d' % sys.version_info[:2])"],
        capture_output=True, text=True, timeout=60,
    )
    if probe.returncode != 0:
        return [f"python interpreter {python!r} did not run"]
    actual = probe.stdout.strip()
    if wanted and tuple(map(int, actual.split("."))) < tuple(map(int, wanted.split("."))):
        issues.append(f"needs Python >= {wanted}; {python} is {actual}")
    modules = list(requires.get("python_modules") or [])
    if modules:
        missing = subprocess.run(
            [python, "-c", "import importlib.util, sys; print(' '.join(m for m in sys.argv[1:] if importlib.util.find_spec(m) is None))", *modules],
            capture_output=True, text=True, timeout=60,
        )
        if missing.stdout.strip():
            issues.append(
                f"missing Python modules for {python}: {missing.stdout.strip()} "
                f"(install the plug-in's requirements or pass --python)"
            )
    for command in requires.get("commands") or []:
        if shutil.which(command) is None:
            issues.append(f"required command not found on PATH: {command}")
    return issues


def _fingerprint(target: Path) -> str:
    if target.is_symlink():
        return "link:" + os.readlink(target)
    if target.is_file():
        digest = hashlib.sha1()
        with target.open("rb") as handle:
            for block in iter(lambda: handle.read(1 << 20), b""):
                digest.update(block)
        return digest.hexdigest()
    if target.is_dir():
        entries = [p for p in target.rglob("*") if p.is_file()]
        return f"dir:{len(entries)}:{max((p.stat().st_mtime_ns for p in entries), default=0)}"
    return "missing"


def _snapshot(path: Path, *, ignored: bool, exclude: str | None = None) -> dict[str, str] | None:
    """Fingerprint every path git reports as changed, untracked (and ignored); None if not a git checkout."""
    command = ["git", "-C", str(path), "status", "--porcelain=v1", "-z", "--untracked-files=all"]
    if ignored:
        command.append("--ignored=matching")
    result = subprocess.run(command, capture_output=True)
    if result.returncode != 0:
        return None
    entries = result.stdout.decode("utf-8", "surrogateescape").split("\0")
    snapshot: dict[str, str] = {}
    index = 0
    while index < len(entries):
        entry = entries[index]
        index += 1
        if len(entry) < 4:
            continue
        status, name = entry[:2], entry[3:]
        if status[0] in "RC":
            index += 1  # the next field is the rename/copy source
        if exclude and (name == exclude or name.startswith(exclude.rstrip("/") + "/")):
            continue
        snapshot[name] = f"{status}:{_fingerprint(path / name)}"
    return snapshot


def _difference(before: dict[str, str], after: dict[str, str]) -> list[str]:
    return sorted(name for name in set(before) | set(after) if before.get(name) != after.get(name))


def run_checks(
    root: Path,
    state: PluginState,
    *,
    kind: str = "checks",
    python: str | None = None,
    only: str | None = None,
    allow_mount_writes: bool = False,
    keep_temp: bool = False,
) -> list[CheckResult]:
    """Run a plug-in's declared checks.

    A step declared `none` or `temp` fails when it changes anything inside the mount (ignored files
    included) or in the host repository; a `mount` step may change the mount only. Without a git
    checkout to compare, steps fail closed. Required steps that cannot run are BLOCKED (not passed).
    """
    if not state.recognized:
        raise PluginError(f"{state.profile.name} is not plugged in ({state.status})")
    edition = state.edition_spec
    assert edition is not None
    checks = edition.checks if kind == "checks" else edition.smoke
    if only:
        checks = tuple(check for check in checks if check.name == only)
        if not checks:
            raise PluginError(f"{state.profile.name} has no {kind} named {only!r}")
    interpreter = resolve_python(state, python)
    results: list[CheckResult] = []
    # One scratch folder per invocation: ordered steps (dry run, then verify) share {tmp}.
    temporary = tempfile.mkdtemp(prefix=f"agency-{state.profile.name}-")
    for check in checks:
        missing = [command for command in check.requires if shutil.which(command) is None]
        if missing:
            results.append(CheckResult(check.name, check.optional, None, 0.0, skipped=f"requires {', '.join(missing)}"))
            continue
        if check.side_effects == "mount" and not allow_mount_writes:
            results.append(CheckResult(check.name, check.optional, None, 0.0,
                                       skipped="writes into the mount; pass --allow-mount-writes"))
            continue
        values = {"{python}": interpreter, "{tmp}": temporary, "{mount}": str(state.path), "{root}": str(Path(root))}

        def expand(argument: str) -> str:
            for placeholder, value in values.items():
                argument = argument.replace(placeholder, value)
            return argument

        argv = [expand(argument) for argument in check.run]
        cwd = state.path if check.cwd == "mount" else Path(root)
        mount_before = _snapshot(state.path, ignored=True)
        host_before = _snapshot(Path(root), ignored=False, exclude=str(state.mount))
        if check.side_effects != "mount" and (mount_before is None or host_before is None):
            results.append(CheckResult(check.name, False, None, 0.0,
                                       "cannot verify side effects: the mount or host is not a git checkout"))
            continue
        started = time.monotonic()
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        env.update({key: expand(value) for key, value in check.env})
        try:
            process = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=check.timeout, env=env)
            output = (process.stdout + process.stderr).strip()
            ok = process.returncode == 0
            code: int | None = process.returncode
        except subprocess.TimeoutExpired:
            ok, code, output = False, None, f"timed out after {check.timeout}s"
        except OSError as error:
            ok, code, output = False, None, f"could not start: {error}"
        seconds = time.monotonic() - started
        changed: list[str] = []
        if check.side_effects != "mount":
            changed += [f"{state.mount}/{name}" for name in _difference(mount_before or {}, _snapshot(state.path, ignored=True) or {})]
        changed += _difference(host_before or {}, _snapshot(Path(root), ignored=False, exclude=str(state.mount)) or {})
        if ok and changed:
            ok = False
            output = (output + "\nUNDECLARED SIDE EFFECT: the check changed files it did not declare:\n  "
                      + "\n  ".join(changed[:20])).strip()
        tail = "\n".join(output.splitlines()[-25:])
        results.append(CheckResult(check.name, ok, code, seconds, tail))
    if keep_temp:
        results.append(CheckResult("scratch", True, 0, 0.0, f"kept scratch folder: {temporary}"))
    else:
        shutil.rmtree(temporary, ignore_errors=True)
    return results


# --------------------------------------------------------------------------- lifecycle


def _is_local_source(source: str) -> bool:
    return source.startswith(("/", "./", "../", "file://", "~")) or os.path.isdir(source)


def _git(root: Path, *args: str, local: bool = False) -> subprocess.CompletedProcess:
    command = ["git"]
    if local:
        command += ["-c", "protocol.file.allow=always"]
    command += list(args)
    process = subprocess.run(command, cwd=root, capture_output=True, text=True)
    if process.returncode != 0:
        raise PluginError(f"`{' '.join(command)}` failed:\n{(process.stderr or process.stdout).strip()}")
    return process


def _module_cache(root: Path, mount: PurePosixPath) -> Path | None:
    """Git's cached clone for a submodule (``<git-common-dir>/modules/<name>``), if present."""
    common = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=root, capture_output=True, text=True)
    if common.returncode != 0:
        return None
    name = read_gitmodules(root).get(str(mount), {}).get("name", str(mount))
    cache = (root / common.stdout.strip() / "modules" / name).resolve()
    return cache if cache.exists() else None


def _cache_origin(cache: Path) -> str:
    result = subprocess.run(["git", "--git-dir", str(cache), "config", "--get", "remote.origin.url"],
                            capture_output=True, text=True)
    return result.stdout.strip()


def _same_source(left: str, right: str) -> bool:
    def norm(value: str) -> str:
        value = os.path.expanduser(value.strip()).removeprefix("file://").rstrip("/").removesuffix(".git")
        return os.path.realpath(value) if _is_local_source(value) else value.lower()
    return norm(left) == norm(right)


def add_plugin(
    root: Path,
    name: str,
    *,
    edition: str | None = None,
    source: str | None = None,
    branch: str | None = None,
) -> tuple[PluginState, list[str]]:
    """Mount a plug-in as a pinned git submodule (or initialise a registered one)."""
    root = Path(root)
    config = load_config(root)
    profiles = load_profiles(root)
    if name not in profiles:
        raise PluginError(f"unknown plug-in {name!r}; known: {', '.join(sorted(profiles)) or 'none'}")
    profile = profiles[name]
    override = config.plugins.get(name, PluginOverride())
    wanted = edition or override.edition or profile.default_edition
    if wanted not in profile.editions:
        raise PluginError(f"{name} has no edition {wanted!r}; editions: {', '.join(profile.editions)}")
    spec = profile.editions[wanted]
    url = os.path.expanduser(source or override.source or spec.source)
    track = branch or override.branch or spec.branch
    state = plugin_state(root, profile, config)
    notes: list[str] = []
    local = _is_local_source(url)
    entry = read_gitmodules(root).get(str(state.mount), {})
    if state.present and not state.registered:
        raise PluginError(
            f"{state.mount} has content that is not a registered submodule (a copy or a manual clone). "
            "Move it away, then add the plug-in again."
        )
    if state.registered:
        registered_url = entry.get("url", "")
        if (source or override.source) and not _same_source(registered_url, url):
            raise PluginError(
                f"{state.mount} is registered from {registered_url}. To point the same plug-in at another URL run "
                f"`git submodule set-url -- {state.mount} <url>`; to change edition, `agency.py plugin remove {name}` first."
            )
        if branch and entry.get("branch") != branch:
            tracked = f"tracks branch {entry['branch']!r}" if entry.get("branch") else "tracks no branch"
            raise PluginError(f"{state.mount} {tracked}, not {branch!r}; change it with "
                              f"`git submodule set-branch --branch {branch} -- {state.mount}`")
        if state.present:
            notes.append(f"{state.mount} is already plugged in")
        else:
            _git(root, "submodule", "update", "--init", "--", str(state.mount), local=_is_local_source(registered_url))
            notes.append(f"initialised registered submodule {state.mount}")
    else:
        if not (root / ".git").exists():
            raise PluginError(f"{root} is not a git repository; plug-ins are mounted as git submodules")
        args = ["submodule", "add"]
        cache = _module_cache(root, state.mount)
        if cache is not None:
            origin = _cache_origin(cache)
            if not _same_source(origin, url):
                raise PluginError(
                    f"git keeps a cached clone of a different source for {state.mount} ({origin or 'unknown origin'}) "
                    f"at {cache}. Delete that folder after review, then add again from {url}."
                )
            args.append("--force")  # reuse the cached clone of the same source
        if track:
            args += ["-b", track]
        if spec.shallow:
            args += ["--depth", "1"]
        args += ["--", url, str(state.mount)]
        _git(root, *args, local=local)
        notes.append(f"added submodule {state.mount} from {url}" + (f" (tracking {track})" if track else ""))
        if spec.shallow:
            submodule = read_gitmodules(root).get(str(state.mount), {}).get("name", str(state.mount))
            _git(root, "config", "-f", ".gitmodules", f"submodule.{submodule}.shallow", "true")
            _git(root, "add", ".gitmodules")
            notes.append("shallow mount (history depth 1); .gitmodules records shallow = true so clones stay small")
        if local:
            notes.append(
                "the source is a local path, which is not portable; before sharing, run "
                f"`git submodule set-url -- {state.mount} <https-url>`"
            )
    state = plugin_state(root, profile, load_config(root))
    if state.edition is None:
        raise PluginError(f"{name}: mounted at {state.mount} but no edition marker was found")
    if state.edition != wanted:
        explicit = edition or override.edition
        if explicit:
            raise PluginError(
                f"{name}: edition {explicit!r} was requested but {state.mount} holds the {state.edition!r} edition; "
                f"remove it (`agency.py plugin remove {name}`) and add again from the {explicit} source"
            )
        notes.append(f"default edition is {wanted!r}; the mounted source is the {state.edition!r} edition")
    return state, notes


def _unsaved_work(path: Path, *, git_dir: Path | None = None) -> list[str]:
    """Local changes or commits that no remote holds, in a mounted plug-in or (``git_dir``) its cached clone."""
    base = ["git", "--git-dir", str(git_dir)] if git_dir else ["git", "-C", str(path)]
    problems = []
    if git_dir is None:  # a cached clone without a worktree has no uncommitted changes to lose
        status = subprocess.run(base + ["status", "--porcelain", "--untracked-files=all"], capture_output=True, text=True)
        if status.returncode != 0:
            return ["cannot read the plug-in's git status"]
        if status.stdout.strip():
            problems.append(f"{len(status.stdout.splitlines())} uncommitted change(s)")
    unpushed = subprocess.run(base + ["log", "--oneline", "--branches", "--not", "--remotes"],
                              capture_output=True, text=True)
    contained = subprocess.run(base + ["branch", "-r", "--contains", "HEAD"], capture_output=True, text=True)
    if unpushed.stdout.strip() or not contained.stdout.strip():
        shallow = subprocess.run(base + ["rev-parse", "--is-shallow-repository"],
                                 capture_output=True, text=True).stdout.strip() == "true"
        problems.append(("commits that no remote branch contains" if git_dir is None
                         else "a cached clone with commits that no remote branch contains")
                        + (" (or a shallow clone whose truncated history cannot prove otherwise)" if shallow else ""))
    return problems


def remove_plugin(root: Path, name: str, *, force: bool = False) -> list[str]:
    """Unmount a submodule plug-in without losing local work. Vendored copies are never deleted."""
    root = Path(root)
    profiles = load_profiles(root)
    if name not in profiles:
        raise PluginError(f"unknown plug-in {name!r}")
    state = plugin_state(root, profiles[name])
    if not state.registered:
        if state.present:
            raise PluginError(
                f"{state.mount} is not a registered submodule; remove the vendored copy manually after review"
            )
        return [f"{name} is not mounted"]
    cache = _module_cache(root, state.mount)
    if state.present:
        unsaved = _unsaved_work(state.path)
    elif cache is not None:  # not checked out here, but git may still hold a clone with local-only commits
        unsaved = _unsaved_work(state.path, git_dir=cache)
    else:
        unsaved = []
    if unsaved and not force:
        raise PluginError(
            f"{state.mount} has {' and '.join(unsaved)}. Push or discard them first, or pass --force "
            "(the cached clone is then kept in .git/modules so nothing is lost)."
        )
    _git(root, "submodule", "deinit", "-f", "--", str(state.mount))
    _git(root, "rm", "-f", "--", str(state.mount))
    notes = [f"removed submodule {state.mount}"]
    safe = cache is not None and cache.is_relative_to((root / ".git").resolve()) and (cache / "HEAD").exists()
    if safe and not unsaved:
        shutil.rmtree(cache)
        notes.append("deleted git's cached clone (everything in it is on a remote) so a later add starts clean")
    elif cache is not None:
        notes.append(f"kept git's cached clone at {cache}; delete it after recovering any local work")
    return notes
