# Copilot instructions

Follow [AGENTS.md](../AGENTS.md): it holds the operating rules for every agent in this repository. Read it before acting.

## Copilot specifics

- Skills (`.github/skills/`), custom agents (`.github/agents/`) and prompt files (`.github/prompts/`) are generated
  links. Edit the sources in `03_Agents-and-Skills/` and `02_Workflows/prompts/`, then run
  `python3 06_Engine/scripts/agency.py sync`.
- Copilot coding agent: the environment comes from `.github/workflows/copilot-setup-steps.yml`. Before finishing,
  run `python3 00_Agentic-OS/agentic-os-review.py` and report its verdict.
