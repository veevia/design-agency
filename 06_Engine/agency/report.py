"""Capability portfolio report: spec, trigger and contract coverage for native or plug-in skills.

Used by ``agency.py plugin report`` (baseline for optimizing a plug-in such as the
FDE toolkit) and by the OS review's native skill spec gate. Read-only.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from .config import ENGINE_DIR, require_yaml

STATUSES = ("draft", "beta", "stable", "deprecated")
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TRIGGER = re.compile(
    r"\b(?:use|invoke|trigger|load)\s+(?:this\s+(?:skill\s+)?|it\s+)?(?:when|whenever|for|to|after|before|on|if)\b",
    re.IGNORECASE,
)
DESCRIPTION_LIMIT = 1024


@dataclass
class SkillRecord:
    name: str
    origin: str
    path: Path
    spec_issues: list[str] = field(default_factory=list)
    has_trigger: bool = False
    mode: str = "none"  # executable | exempt | none
    score: int | None = None

    @property
    def contract_ready(self) -> bool:
        return self.mode == "exempt" or (self.score is not None and self.score >= 10)


def split_front_matter(text: str) -> str | None:
    if not text.startswith("---"):
        return None
    match = re.search(r"\n---\s*\n", text[3:])
    return text[3: match.start() + 3] if match else None


def front_matter(path: Path) -> tuple[dict | None, str | None]:
    yaml = require_yaml()
    block = split_front_matter(path.read_text(encoding="utf-8"))
    if block is None:
        return None, "no YAML front-matter"
    try:
        data = yaml.safe_load(block) or {}
    except yaml.YAMLError as error:
        return None, f"front-matter YAML error: {error.__class__.__name__}"
    if not isinstance(data, dict):
        return None, "front-matter is not a mapping"
    return data, None


def spec_issues(skill_dir: Path, data: dict | None, *, native: bool) -> list[str]:
    """Portability spec: valid `name` == folder, bounded `description` with a trigger phrase."""
    if data is None:
        return ["unparseable front-matter"]
    issues = []
    name = data.get("name")
    if not isinstance(name, str) or not name:
        issues.append("missing `name`")
    elif name != skill_dir.name:
        issues.append(f"`name: {name}` must equal the folder name `{skill_dir.name}`")
    elif not NAME.fullmatch(name) or len(name) > 64:
        issues.append("`name` must be lowercase kebab-case, at most 64 characters")
    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        issues.append("missing `description`")
    else:
        if len(description) > DESCRIPTION_LIMIT:
            issues.append(f"`description` is {len(description)} characters (limit {DESCRIPTION_LIMIT})")
        if not TRIGGER.search(description):
            issues.append("`description` has no trigger phrase (\"Use when …\"); Copilot and Claude route on it")
    if native:
        if not isinstance(data.get("title"), str) or not data.get("title"):
            issues.append("missing `title`")
        if data.get("status") not in STATUSES:
            issues.append(f"`status` must be one of {', '.join(STATUSES)}")
    return issues


def agent_spec_issues(path: Path, data: dict | None) -> list[str]:
    """Portable native agent: `name` equals the file slug (Claude requires lowercase-hyphen), description with a trigger."""
    if data is None:
        return ["unparseable front-matter"]
    slug = path.name.removesuffix(".agent.md")
    issues = []
    if data.get("name") != slug:
        issues.append(f"`name` must be the file slug `{slug}` (Claude Code requires lowercase-hyphen agent names)")
    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        issues.append("missing `description`")
    elif not TRIGGER.search(description):
        issues.append("`description` has no trigger phrase (\"Use when …\")")
    return issues


def prompt_spec_issues(path: Path, data: dict | None) -> list[str]:
    """Prompt files: a description for the command picker and the current `agent:` key, not the retired `mode:`."""
    if data is None:
        return ["unparseable front-matter"]
    issues = []
    if not isinstance(data.get("description"), str) or not data["description"].strip():
        issues.append("missing `description`")
    if "mode" in data:
        issues.append("`mode:` is retired; use `agent:`")
    return issues


def _lint_module():
    harness = ENGINE_DIR / "harness"
    if str(harness) not in sys.path:
        sys.path.insert(0, str(harness))
    spec = importlib.util.spec_from_file_location("agency_lint_skill", harness / "lint-skill.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module  # dataclasses resolve their module through sys.modules
    spec.loader.exec_module(module)
    return module


def skill_record(skill_dir: Path, origin: str, *, lint=None) -> SkillRecord:
    lint = lint or _lint_module()
    data, error = front_matter(skill_dir / "SKILL.md")
    record = SkillRecord(name=skill_dir.name, origin=origin, path=skill_dir)
    record.spec_issues = [error] if error else spec_issues(skill_dir, data, native=origin == "native")
    if data is not None:
        description = data.get("description") if isinstance(data.get("description"), str) else ""
        record.has_trigger = bool(TRIGGER.search(description))
        fields = lint.contract_fields(data)
        record.score, _ = lint.contract_score(skill_dir.name, data)
        if fields.get("contract-exempt"):
            record.mode = "exempt"
        elif any(fields.get(key) for key in ("inputs", "outputs", "lints")):
            record.mode = "executable"
    return record


def portfolio(skill_dirs: list[tuple[Path, str]]) -> list[SkillRecord]:
    lint = _lint_module()
    return [skill_record(directory, origin, lint=lint) for directory, origin in skill_dirs]


def summarize(records: list[SkillRecord]) -> dict:
    total = len(records)

    def share(count: int) -> str:
        return f"{count}/{total} ({count / total:.0%})" if total else "0/0"

    return {
        "skills": total,
        "spec_compliant": share(sum(not r.spec_issues for r in records)),
        "trigger_in_description": share(sum(r.has_trigger for r in records)),
        "contract_ready": share(sum(r.contract_ready for r in records)),
        "executable": sum(r.mode == "executable" for r in records),
        "exempt": sum(r.mode == "exempt" for r in records),
        "no_contract": sum(r.mode == "none" for r in records),
    }
