"""Load and validate ``agency.yaml``, the operating configuration of a Design Agency OS repository.

The file is human-authored. Tools read it and change only the top-level ``mode``
line (``template`` → ``workspace``) when a hub or plug-in is added through the CLI.
Plug-in *state* is not stored here: a plug-in is plugged in when its mount is
checked out. ``plugins.<name>`` entries are optional overrides.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

try:  # PyYAML is the harness's only third-party dependency.
    import yaml
except ImportError:  # pragma: no cover - exercised only without dependencies
    yaml = None

ENGINE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = ENGINE_DIR.parent

CONFIG_FILE = "agency.yaml"
SCHEMA = "agency/v1"
MODES = ("template", "workspace")
TARGETS = ("copilot", "claude")

HUBS_DIR = PurePosixPath("01_Project-Hubs")
TEMPLATE_HUB = "_template-project"
PROMPTS_DIR = PurePosixPath("02_Workflows/prompts")
SOPS_DIR = PurePosixPath("02_Workflows/SOPs")
SKILLS_DIR = PurePosixPath("03_Agents-and-Skills/Skills")
AGENTS_DIR = PurePosixPath("03_Agents-and-Skills/Agents")
PROFILES_DIR = PurePosixPath("06_Engine/plugins")

_TOP_KEYS = {"schema", "name", "mode", "discovery", "plugins"}
_PLUGIN_KEYS = {"enabled", "edition", "mount", "source", "branch"}
_MODE_LINE = re.compile(r"^mode:\s*(\S+)\s*(#.*)?$", re.MULTILINE)


class ConfigError(ValueError):
    """Raised when agency.yaml or a dependency it needs is invalid."""


def require_yaml():
    if yaml is None:
        raise ConfigError(
            "PyYAML is required. Install the harness dependencies: "
            "python3 -m pip install -r 06_Engine/requirements.txt"
        )
    return yaml


def repo_path(value: object, *, field_name: str) -> PurePosixPath:
    """Validate a repository-relative POSIX path (no absolute paths, no `..`)."""
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{field_name} must be a non-empty relative path")
    path = PurePosixPath(value.strip().rstrip("/"))
    drive = re.match(r"^[A-Za-z]:", value.strip()) is not None
    if path.is_absolute() or drive or "\\" in value or ".." in path.parts or str(path) in {"", "."}:
        raise ConfigError(f"{field_name} must stay inside the repository: {value!r}")
    return path


@dataclass(frozen=True)
class PluginOverride:
    enabled: bool | None = None
    edition: str | None = None
    mount: PurePosixPath | None = None
    source: str | None = None
    branch: str | None = None


@dataclass(frozen=True)
class AgencyConfig:
    root: Path
    name: str
    mode: str
    targets: tuple[str, ...]
    plugins: dict[str, PluginOverride] = field(default_factory=dict)
    exists: bool = True

    @property
    def path(self) -> Path:
        return self.root / CONFIG_FILE


def _plugin_override(name: str, data: object) -> PluginOverride:
    if data is None:
        return PluginOverride()
    if not isinstance(data, dict):
        raise ConfigError(f"plugins.{name} must be a mapping")
    unknown = set(data) - _PLUGIN_KEYS
    if unknown:
        raise ConfigError(f"plugins.{name}: unknown keys {sorted(unknown)}; allowed {sorted(_PLUGIN_KEYS)}")
    enabled = data.get("enabled")
    if enabled is not None and not isinstance(enabled, bool):
        raise ConfigError(f"plugins.{name}.enabled must be true or false")
    for key in ("edition", "source", "branch"):
        if data.get(key) is not None and not isinstance(data[key], str):
            raise ConfigError(f"plugins.{name}.{key} must be a string")
    mount = data.get("mount")
    return PluginOverride(
        enabled=enabled,
        edition=data.get("edition"),
        mount=repo_path(mount, field_name=f"plugins.{name}.mount") if mount is not None else None,
        source=data.get("source"),
        branch=data.get("branch"),
    )


def load_config(root: Path = REPO_ROOT) -> AgencyConfig:
    """Return the validated configuration; a missing file yields template defaults."""
    root = Path(root)
    path = root / CONFIG_FILE
    if not path.is_file():
        return AgencyConfig(root=root, name=root.name, mode="template", targets=TARGETS, exists=False)
    data = require_yaml().safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ConfigError(f"{CONFIG_FILE} must contain a mapping")
    unknown = set(data) - _TOP_KEYS
    if unknown:
        raise ConfigError(f"{CONFIG_FILE}: unknown top-level keys {sorted(unknown)}")
    if data.get("schema", SCHEMA) != SCHEMA:
        raise ConfigError(f"{CONFIG_FILE}: schema must be {SCHEMA!r}")
    mode = data.get("mode", "template")
    if mode not in MODES:
        raise ConfigError(f"{CONFIG_FILE}: mode must be one of {MODES}, not {mode!r}")
    discovery = data.get("discovery") or {}
    if not isinstance(discovery, dict) or set(discovery) - {"targets"}:
        raise ConfigError(f"{CONFIG_FILE}: discovery supports only `targets`")
    targets = discovery.get("targets", list(TARGETS))
    if not isinstance(targets, list) or not targets or any(t not in TARGETS for t in targets):
        raise ConfigError(f"{CONFIG_FILE}: discovery.targets must be a non-empty subset of {TARGETS}")
    if len(set(targets)) != len(targets):
        raise ConfigError(f"{CONFIG_FILE}: discovery.targets lists a target twice")
    plugins = data.get("plugins") or {}
    if not isinstance(plugins, dict):
        raise ConfigError(f"{CONFIG_FILE}: plugins must be a mapping of plug-in name to overrides")
    name = data.get("name", root.name)
    if not isinstance(name, str) or not name.strip():
        raise ConfigError(f"{CONFIG_FILE}: name must be a non-empty string")
    return AgencyConfig(
        root=root,
        name=name,
        mode=mode,
        targets=tuple(targets),
        plugins={str(key): _plugin_override(str(key), value) for key, value in plugins.items()},
    )


def set_mode(root: Path, mode: str) -> bool:
    """Rewrite only the top-level ``mode:`` line. Returns True when the file changed."""
    if mode not in MODES:
        raise ConfigError(f"mode must be one of {MODES}")
    path = Path(root) / CONFIG_FILE
    if not path.is_file():
        raise ConfigError(f"{CONFIG_FILE} not found in {root}")
    text = path.read_text(encoding="utf-8")
    match = _MODE_LINE.search(text)
    if match is None:
        raise ConfigError(f"{CONFIG_FILE} has no top-level `mode:` line to update")
    if match.group(1) == mode:
        return False
    comment = f"  {match.group(2)}" if match.group(2) else ""
    path.write_text(text[: match.start()] + f"mode: {mode}{comment}" + text[match.end():], encoding="utf-8")
    load_config(root)  # re-validate what was written
    return True
