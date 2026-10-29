# Setup — any editor, any agent

**TL;DR:** Python 3.11+ and PyYAML run the whole harness; plug-ins and web apps add their own dependencies only when you add them.

## 1. Prerequisites

| Tool | Version | Why | Check |
|---|---|---|---|
| Git | 2.30+ | Repository, plug-in submodules, hooks | `git --version` |
| Python | 3.11+ | `06_Engine/` engine, harness and review | `python3 --version` |
| Node.js | 20+ (22+ for PDG browser checks) | Optional: web starters, PDG prototypes | `node --version` |
| ffmpeg | any recent | Optional: VPG smoke runs | `ffmpeg -version` |

## 2. Harness dependencies and the first review

```sh
python3 -m venv .venv
. .venv/bin/activate                         # Windows: .venv\Scripts\activate
python -m pip install -r 06_Engine/requirements.txt
python 00_Agentic-OS/agentic-os-review.py    # expect: VERDICT: PASS
```

The review recomputes every gate: contracts, decisions, skills, SOPs, catalog and discovery drift, plug-in
profiles, links, hygiene, evals and unit tests. `--fast` skips the evals and unit tests.

## 3. Install the git hooks (recommended)

```sh
bash 06_Engine/scripts/install-hooks.sh
```

`pre-commit` scans staged changes for credentials and runs the fast review, including the privacy gate;
`pre-push` runs the full review. List customer names, people and codenames you must never commit in
`.agency/denylist.txt` (ignored by git) so the gate catches them — see [RELEASING](00_README/RELEASING.md).
CI (`.github/workflows/agency-ci.yml`) runs the full review on every push and pull request.

## 4. Connect your agent

| Agent | How it picks up the OS |
|---|---|
| GitHub Copilot (VS Code, CLI, coding agent) | Reads `AGENTS.md` and `.github/copilot-instructions.md`; skills, agents and prompt files from `.github/skills`, `.github/agents`, `.github/prompts`. The workspace `.vscode/settings.json` turns off `.claude/*` discovery in VS Code so nothing is listed twice. |
| Claude Code | Reads `CLAUDE.md` (which imports `AGENTS.md`); skills, agents and slash commands from `.claude/skills`, `.claude/agents`, `.claude/commands`. |
| Other agents (Codex, Cursor, …) | Point them at `AGENTS.md` and the [capability catalog](03_Agents-and-Skills/INDEX.md). |

Discovery folders hold generated symlinks. After adding or renaming a skill, agent or prompt, regenerate the
links and the capability catalog:

```sh
python3 06_Engine/scripts/agency.py sync
```

On Windows, symlinks need Developer Mode and `git config core.symlinks true`.

## 5. Start a project

```sh
python3 06_Engine/scripts/agency.py hub new <slug>
```

This copies `01_Project-Hubs/_template-project/` and switches `agency.yaml` to `mode: workspace`. Then set the
owner, goal and phase in the hub README and start [W1](02_Workflows/workflows/W1-understand.md).

## 6. Add plug-ins (optional)

```sh
python3 06_Engine/scripts/agency.py plugin list
python3 06_Engine/scripts/agency.py plugin add fde-design-toolkit             # or --edition full
python3 06_Engine/scripts/agency.py plugin add prototype-design --with-companions   # PDG + the skills it binds
python3 06_Engine/scripts/agency.py plugin add video-production --with-companions   # VPG + the skills it binds
```

`--with-companions` first adds the plug-ins that supply the skills an engine's graph binds, including the FDE
toolkit's full edition (it needs repository access).

Engines need their own Python packages; see [PLUGINS](00_README/PLUGINS.md#interpreters-for-engines).
When you clone a repository that already has plug-ins, run `plugin add <name>` (or
`git submodule update --init`) to check them out.

## 7. Web apps (optional)

```sh
cp -R 05_Library/_starters/next-tailwind 01_Project-Hubs/<slug>/03_build/web
cd 01_Project-Hubs/<slug>/03_build/web && npm install && npm run dev
```

See the [starter guide](05_Library/_starters/README.md).

## You're ready

Read [AGENTS.md](AGENTS.md) and the [operating guide](00_Agentic-OS/README.md), then work through
[.github/SETUP-CHECKLIST.md](.github/SETUP-CHECKLIST.md) to confirm everything.
