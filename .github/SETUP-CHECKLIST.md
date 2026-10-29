# Setup checklist

**TL;DR:** Ten checks confirm a fresh clone or fork is ready; each one names the command that proves it.

- [ ] `python3 --version` reports 3.11 or newer, and `python3 -c "import yaml"` succeeds.
- [ ] `python3 00_Agentic-OS/agentic-os-review.py` ends with `VERDICT: PASS`.
- [ ] `python3 06_Engine/scripts/agency.py status` shows the expected mode (`template` for the blank harness).
- [ ] `python3 06_Engine/scripts/agency.py sync --check` reports `discovery: in sync`.
- [ ] `bash 06_Engine/scripts/install-hooks.sh` installed `pre-commit` and `pre-push`.
- [ ] Your agent reads [AGENTS.md](../AGENTS.md): ask it "what is the task procedure?" and expect scope → retrieve → execute → verify → hand off.
- [ ] A slash command appears in your agent (for example `/context-pull` or `/wiki-query`).
- [ ] You read the [operating guide](../00_Agentic-OS/README.md) and [How we work](../00_README/HOW-WE-WORK.md).
- [ ] For real work: `python3 06_Engine/scripts/agency.py hub new <slug>` created your first hub.
- [ ] For plug-ins: `python3 06_Engine/scripts/agency.py plugin add <name>` then `plugin check <name>` passes.
