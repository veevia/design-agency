---
description: "Run the lints[*] rules declared in a SKILL.md against the workspace. Reports `severity | skill | rule | file:line | message` per finding."
agent: agent
---

# /skill-lint

Validate workspace artifacts against the lint rules declared in a skill's `SKILL.md` front-matter.

## Inputs

- **skill** (required): skill slug (e.g. `evidence-tagging`) or path to a `SKILL.md`.
- **target** (optional): glob to override the rule's `where:` (e.g. lint only one program: `01_Project-Hubs/<hub>/_wiki/**/*.md`).
- **severity** (optional, default `info`): minimum severity to report — `error`, `warning`, or `info`.
- **--all** (optional): lint every skill that declares a contract.

## Procedure

1. **Resolve the skill.** Locate `03_Agents-and-Skills/Skills/<skill>/SKILL.md`.
2. **Run the lint script:**
   ```bash
   python3 06_Engine/harness/lint-skill.py <skill> [--target <glob>] [--severity error|warning|info]
   ```
3. **Read findings line-by-line.** Each finding is `<severity> | <skill> | <rule-id> | <file>:<line> | <message>`.
4. **Surface to user:**
   - Group by severity (errors first).
   - Show the top 20 findings; offer to display all.
   - For each error: link the file:line, propose the minimal fix.
5. **Offer follow-up:** "Want me to apply the suggested fixes for <rule-id> across all <n> findings?"

## Output format

```
=== /skill-lint <skill> ===
Errors (<n>):
  - <file>:<line>  <rule-id>  — <message>
Warnings (<n>): ...
Info (<n>): ...

Exit code: <0|1>
```

## When this goes wrong

- **Skill has no `lints:` declared** — expected for narrative-first skills. Script reports `no lints declared — skipping`. Not an error.
- **PyYAML missing** — install the harness dependencies: `python3 -m pip install -r 06_Engine/requirements.txt`.
- **Regex too broad** — if a rule fires hundreds of times across a real wiki, surface the noise to user; don't silently lower severity.

## See also

- [`06_Engine/harness/skill-schema.md`](../../06_Engine/harness/skill-schema.md) — the schema lints declare against
- [`06_Engine/harness/lint-skill.py`](../../06_Engine/harness/lint-skill.py) — the runner
- [`wiki-lint.prompt.md`](../../02_Workflows/prompts/wiki-lint.prompt.md) — the wiki-wide lint that invokes this
