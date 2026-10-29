# CLAUDE.md

Claude Code loads this file; the operating rules live in AGENTS.md (imported below) and bind every runtime.

@AGENTS.md

## Claude Code specifics

- Skills, agents and slash commands come from generated links in `.claude/skills/`, `.claude/agents/` and
  `.claude/commands/`. Edit the sources (`03_Agents-and-Skills/`, `02_Workflows/prompts/`), then run
  `python3 06_Engine/scripts/agency.py sync`.
- Machine-local settings belong in `.claude/settings.local.json`, which Git ignores.
