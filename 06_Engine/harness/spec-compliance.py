#!/usr/bin/env python3
"""spec-compliance.py — portable spec gate for native skills, agents and prompts.

Skills: `name` equals the folder, a `description` of at most 1024 characters that names its trigger
("Use when …") — Copilot and Claude route on description alone — plus `title` and a valid `status`.
Agents: `name` equals the file slug and the description names its trigger. Prompts: a `description`
and the current `agent:` key. Rules live in 06_Engine/agency/report.py (one implementation).

    python3 06_Engine/harness/spec-compliance.py          # exit 1 on any violation
    python3 06_Engine/harness/spec-compliance.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_DIR))

from agency.catalog import native_agents, native_prompts, native_skill_dirs  # noqa: E402
from agency.config import SKILLS_DIR  # noqa: E402
from agency.report import agent_spec_issues, front_matter, prompt_spec_issues, spec_issues  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ENGINE_DIR.parent)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = {}
    for skill_dir in native_skill_dirs(args.root / SKILLS_DIR):
        data, error = front_matter(skill_dir / "SKILL.md")
        results[f"skill {skill_dir.name}"] = [error] if error else spec_issues(skill_dir, data, native=True)
    for path in native_agents(args.root):
        data, error = front_matter(path)
        results[f"agent {path.name}"] = [error] if error else agent_spec_issues(path, data)
    for path in native_prompts(args.root):
        data, error = front_matter(path)
        results[f"prompt {path.name}"] = [error] if error else prompt_spec_issues(path, data)
    violations = {name: issues for name, issues in results.items() if issues}
    if args.json:
        print(json.dumps({"skills": len(results), "violations": violations}, indent=2))
    else:
        for name, issues in violations.items():
            for issue in issues:
                print(f"FAIL {name}: {issue}")
        print(f"spec: {len(results) - len(violations)}/{len(results)} native skills, agents and prompts compliant")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
