#!/usr/bin/env python3
"""
06_Engine/harness/lint-sop.py

Verify SOP cross-references resolve on disk. For every SOP under
`02_Workflows/SOPs/` (excluding `_template/` and `_proposed/`):

  - Every `loads_skills[*]` exists at `03_Agents-and-Skills/Skills/<slug>/SKILL.md`
  - Every `invokes_prompts[*]` exists at `02_Workflows/prompts/<slug>.prompt.md`
  - Every `produces_artifacts[*]` (when given as a path) exists or is templated
  - `owner_agent`, if specified and not "none", points to a real agent dir

Usage:
    python 06_Engine/harness/lint-sop.py            # all SOPs
    python 06_Engine/harness/lint-sop.py session-snapshot

Exit codes:
    0  no errors
    1  one or more SOPs have unresolved references
    2  invalid arguments
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install -r 06_Engine/requirements.txt", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parents[2]
SOPS_ROOT = REPO_ROOT / "02_Workflows" / "SOPs"
SKILLS_ROOT = REPO_ROOT / "03_Agents-and-Skills" / "Skills"
AGENTS_ROOT = REPO_ROOT / "03_Agents-and-Skills" / "Agents"
PROMPTS_ROOT = REPO_ROOT / "02_Workflows" / "prompts"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_paths import find_skill_dir  # noqa: E402

SKIP_DIRS = {"_template", "_proposed"}


def _split_frontmatter(text: str) -> str | None:
    """Return the raw YAML front-matter block, or None if absent.

    Matches only the FIRST closing `---` fence on its own line. The naive
    text.split("---", 2) breaks whenever the BODY contains a `---` (horizontal
    rules, markdown table separators), wrongly truncating valid YAML. Mirror of
    06_Engine/harness/lint-skill.py:_split_frontmatter.
    """
    if not text.startswith("---"):
        return None
    m = re.search(r"\n---\s*\n", text[3:])
    if not m:
        return None
    return text[3 : m.start() + 3]


def parse_front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    fm = _split_frontmatter(text)
    if fm is None:
        return {}
    try:
        data = yaml.safe_load(fm)
    except yaml.YAMLError as e:
        return {"_yaml_error": str(e)}
    return data if isinstance(data, dict) else {}


def check_sop(sop_path: Path) -> list[str]:
    findings: list[str] = []
    rel = sop_path.relative_to(REPO_ROOT)
    fm = parse_front_matter(sop_path)
    if "_yaml_error" in fm:
        findings.append(f"error | sop-yaml | {rel} | YAML parse error: {fm['_yaml_error'][:80]}")
        return findings

    sop_id = fm.get("id") or sop_path.parent.name

    # Skills
    for sk in fm.get("loads_skills") or []:
        sk = str(sk).strip()
        if find_skill_dir(SKILLS_ROOT, sk) is None:
            findings.append(f"error | missing-skill | {rel} | loads_skills: '{sk}' has no SKILL.md")

    # Prompts
    for p in fm.get("invokes_prompts") or []:
        p = str(p).strip()
        if not (PROMPTS_ROOT / f"{p}.prompt.md").exists():
            findings.append(f"error | missing-prompt | {rel} | invokes_prompts: '{p}' has no .prompt.md")

    # Owner agent (optional)
    owner = fm.get("owner_agent")
    if owner and isinstance(owner, str) and not owner.strip().lower().startswith("none"):
        agent_slug = owner.strip()
        if not (AGENTS_ROOT / f"{agent_slug}.agent.md").is_file():
            findings.append(f"warning | missing-agent | {rel} | owner_agent: '{agent_slug}' has no Agents/{agent_slug}.agent.md")

    # Sub-agents (optional)
    for a in fm.get("sub_agents") or []:
        a = str(a).strip()
        if not (AGENTS_ROOT / f"{a}.agent.md").is_file():
            findings.append(f"warning | missing-sub-agent | {rel} | sub_agents: '{a}' has no Agents/{a}.agent.md")

    # Produces artifacts: if a value contains a relative path with a real-looking glob, check the parent dir exists
    for art in fm.get("produces_artifacts") or []:
        art = str(art).strip()
        # Strip <placeholder> patterns to get the directory portion
        clean = re.sub(r"<[^>]+>", "*", art)
        if "/" in clean:
            parent = Path(clean).parent
            target = REPO_ROOT / parent
            # Skip if parent looks like a glob pattern with no concrete prefix
            concrete = str(parent).split("*", 1)[0].rstrip("/")
            if concrete and not (REPO_ROOT / concrete).exists():
                findings.append(f"warning | missing-output-dir | {rel} | produces_artifacts parent does not exist: {concrete}")

    # Required keys
    for key in ("id", "title", "status", "trigger", "produces_artifacts", "done_when"):
        if key not in fm:
            findings.append(f"warning | missing-key | {rel} | front-matter missing '{key}'")

    return findings


def main() -> int:
    args = sys.argv[1:]
    if args:
        targets = [SOPS_ROOT / a / "SOP.md" for a in args]
    else:
        targets = [
            p / "SOP.md"
            for p in sorted(SOPS_ROOT.iterdir())
            if p.is_dir() and p.name not in SKIP_DIRS
        ]
    all_findings: list[str] = []
    for sop in targets:
        if not sop.exists():
            print(f"# NOT FOUND: {sop.relative_to(REPO_ROOT)}", file=sys.stderr)
            continue
        all_findings.extend(check_sop(sop))
    for f in all_findings:
        print(f)
    error_count = sum(1 for f in all_findings if f.startswith("error"))
    warning_count = sum(1 for f in all_findings if f.startswith("warning"))
    print(f"# lint-sop: {len(all_findings)} finding(s) (errors={error_count}, warnings={warning_count})", file=sys.stderr)
    return 1 if error_count else 0


if __name__ == "__main__":
    sys.exit(main())
