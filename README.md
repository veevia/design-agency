# Design Agency OS

**TL;DR:** A repository template that makes GitHub Copilot, Claude Code and Codex follow one rule set and hand back design work with evidence.

Start here when your design or forward-deployed engineering (FDE) team works with AI agents. The template brings the rules, 87 skills, workflows from research to learning, and the checks that keep all of it consistent. Your team adds the projects.

![The Design Agency OS as an animated diagram. A request moves through five task steps, each worked by an agent: Scope, Retrieve, Execute, Verify and Hand off, ending in a verified result. Above each step sits what it uses: AGENTS.md (always on), the capability catalog (87 skills), plug-ins (PDG and VPG, with a person's approval gate), the OS review (21 rows, an evidence gate) and the publish check (READY, an evidence gate), which escalates to the user. Verify returns corrections to Execute. Below, a project hub takes sources through Understand, Design, Build and Learn, and a next-loop rail returns from Learn to Understand. A bar of six contracts, L0 Authority to L5 Verification, supports every step. The animation brings each step into focus in turn, then returns to the full view.](00_README/_assets/design-agency-os.gif)

<sub>Still image: [00_README/_assets/design-agency-os.png](00_README/_assets/design-agency-os.png)</sub>

## Why you need it

AI agents now draft a research synthesis, a PRD or a clickable prototype in minutes. That speed moves the risk into review. A fluent document is easy to mistake for a checked one, and a reader cannot tell which claims came from users and which the model supplied.

A shared repository makes this harder. Copilot reads `.github/copilot-instructions.md` and Claude Code reads `CLAUDE.md`, so a team that runs both keeps two rule sets that nothing holds in step. Skills get copied into one runtime's folder and edited there. A command that exits with code 0 gets reported as a finished outcome, and material from one client's project can end up in the template the next team starts from.

Design Agency OS puts the contract in the repository itself. Every agent reads the same rules and every capability comes from one source, so when either drifts, a single review fails the build.

## How it works

[AGENTS.md](AGENTS.md) holds the rules for every runtime. `CLAUDE.md` and `.github/copilot-instructions.md` only point to it, and Codex reads it directly. [AUTHORITIES.md](AUTHORITIES.md) names the file that owns each concept, and six contracts, [L0](00_Agentic-OS/decisions/l0-authority-and-safety.md) to [L5](00_Agentic-OS/decisions/l5-verification-and-learning.md), cover authority, knowledge, capabilities, control, delivery and verification. An agent opens a contract only when its question comes up.

A task moves from scope to handoff in the same order every time, and each step scales with the size of the request ([operating guide](00_Agentic-OS/README.md)).

| Step | The agent | Draws on |
|---|---|---|
| 01 Scope | States the outcome, the files it will touch, its permissions and the acceptance test | The rules in `AGENTS.md` |
| 02 Retrieve | Loads only the capability and context the task needs | The [capability catalog](03_Agents-and-Skills/INDEX.md) and the hub's `_wiki/index.md` |
| 03 Execute | Advances the current step with the chosen capability | Skills, agents, prompts, workflows and plug-in engines |
| 04 Verify | Checks the result against acceptance and widens the checks with the risk | The OS review, evals and unit tests |
| 05 Hand off | Returns the result, its paths and evidence, and any blockers or next action | `publish-check` before a release; a person authorizes publishing |

Projects run on a longer loop. Each one lives in a hub and moves from Understand to Learn ([workflows](02_Workflows/README.md)).

| Phase | Workflow | Produces |
|---|---|---|
| Understand | [W1](02_Workflows/workflows/W1-understand.md) | Problem frame, research, persona, JTBD and journey map |
| Design | [W2](02_Workflows/workflows/W2-design.md) | POV, brief and PRD |
| Build | [W3](02_Workflows/workflows/W3-build.md) | A prototype or thin slice with its test plan; PDG and VPG projects live here |
| Learn | [W4](02_Workflows/workflows/W4-learn.md) | Evidence brief, retro, updated artifacts and the next loop |

[W5](02_Workflows/workflows/W5-decide.md) records a decision only when it is new and durable; routine work reuses its task evidence.

Each capability has one source. Skills live in `03_Agents-and-Skills/`, prompts in `02_Workflows/prompts/`, and `agency.py sync` links them into `.github/` for Copilot and `.claude/` for Claude Code, then rebuilds the catalog. Plug-ins mount as pinned git submodules with one command, and engine plug-ins such as the Video Production Graph (VPG) keep their own human approval gates.

`agentic-os-review.py` proves the repository: it runs 21 checks, including privacy and 136 unit tests, and returns one verdict. CI runs it on every push and pull request, git hooks run it before commits and pushes, and `publish-check` adds the full history and remote refs before anything is released.

## What changes when you adopt it

| Without a shared contract | With Design Agency OS |
|---|---|
| Each runtime follows its own instruction file | Copilot, Claude Code and Codex read the same `AGENTS.md`, and the review fails if an adapter diverges |
| Skills are copied into `.github/` or `.claude/` and edited there | Each skill has one source; `agency.py sync` regenerates the links, and the review fails on drift |
| A synthesis mixes interview findings with the model's guesses | Every claim carries `observed`, `reported` or `assumed`, with its source |
| A command that exited with code 0 counts as done | Each task hands back the result with its acceptance evidence and any blockers |
| Decisions stay in chat threads | A decision that outlives the task gets one typed record and one Traffic Light (🟢🟡🔴); Yellow names a trigger and an expiry |
| Agents push or publish because they can | Publishing, pushing and other irreversible steps wait for a person |
| Client names slip into a shared template | The privacy gate scans files, history and remote refs, and `publish-check` must report READY before a release |

The template itself ships no projects, people or client material. Your team adds hubs, plug-ins and its own design system, and the rules and checks stay the same.

## Quickstart

### 1. Check the harness

```sh
python3 -m pip install -r 06_Engine/requirements.txt   # PyYAML; Python 3.11+
python3 00_Agentic-OS/agentic-os-review.py             # VERDICT: PASS (21 rows) on a fresh clone
python3 06_Engine/scripts/agency.py status             # mode, capabilities, plug-ins, discovery
```

Editor notes, git hooks and connecting your agent: [SETUP.md](SETUP.md).

### 2. Start a project

```sh
# A project hub: intake, wiki and four phase folders
python3 06_Engine/scripts/agency.py hub new example-project

# Optional: a skill pack and the demo-film engine
python3 06_Engine/scripts/agency.py plugin add fde-design-toolkit
python3 06_Engine/scripts/agency.py plugin add video-production --with-companions
```

`hub new` and `plugin add` switch `agency.yaml` from `mode: template` to `mode: workspace`.

### 3. Ask your agent

Your agent reads `AGENTS.md`, finds the capability in the [catalog](03_Agents-and-Skills/INDEX.md) and loads only that one.

| You have | Run | Ask |
|---|---|---|
| Raw interview notes | `/wiki-ingest` | "Ingest the three interview notes in `example-project/00_context_intake/` into the hub wiki, and tag every claim observed, reported or assumed." |
| Research but no direction | `/design-pov` | "Draft the POV for the primary persona from the wiki's JTBD and journey pages, with non-goals and the evidence behind each claim." |
| A choice that outlives the task | `/decision-log` | "Record the decision to pilot the new flow at one site as a Yellow Traffic Light, with its trigger and expiry." |
| An approved brief for a demo film | `/video-production` | "Start the demo film in `example-project/03_build/demo-film/`, work the task packets and stop at each human gate." |

## Plug-ins

| Plug-in | Kind | What it adds | Add it |
|---|---|---|---|
| FDE Design Toolkit | Skills | Forward-deployed design skills: 12 in the public edition; the full edition adds 68 skills, 5 reviewer agents, commands and gates | `plugin add fde-design-toolkit [--edition full]` |
| PDG, Prototype Production Graph | Engine | Brief to verified prototype: 19 nodes, 8 phases, browser checks and named human gates, driven by `/prototype-design` | `plugin add prototype-design --with-companions` |
| VPG, Video Production Graph | Engine | Governed demo films: 25 nodes, measured media, 6 reviews and 5 named human gates, driven by `/video-production` | `plugin add video-production --with-companions` |
| UI/UX Pro Max | Skills | Third-party UI and UX design data: styles, palettes, font pairings and charts | `plugin add ui-ux-pro-max` |
| Anthropic skills, Impeccable, Video Shotcraft | Skills | Companion skill packs that the engines bind | Added by `--with-companions` |

Run each command as `python3 06_Engine/scripts/agency.py plugin add …`. Plug-ins keep their own licenses and are improved upstream with `/plugin-optimize`, never edited in place ([plug-in guide](00_README/PLUGINS.md)).

## Validation and project map

```sh
python3 00_Agentic-OS/agentic-os-review.py                                     # integrity verdict
python3 06_Engine/scripts/agency.py publish-check --ref main --remote origin   # release gate
```

The review covers the six contracts and decision records, agent entry points, skill specs, contracts and lints, SOP contracts, the capability map, catalog and discovery sync, plug-in profiles, links, repository hygiene, privacy, wiki indexes, golden evals and unit tests. `publish-check` adds the full history, commit identities and every remote ref, then reports READY or NOT READY.

```text
AGENTS.md, AUTHORITIES.md   Rules every agent follows; who owns each concept
00_Agentic-OS/              Operating guide, the six contracts, the review, backlog and run evidence
00_README/                  Architecture, plug-in guide, conventions, 7 frameworks, 16 templates
01_Project-Hubs/            One hub per project; the blank template ships only _template-project/
02_Workflows/               Workflows W1 to W5, / commands and 7 SOPs; engine plug-ins mount here
03_Agents-and-Skills/       87 native skills, 6 agents, the catalog; skill plug-ins mount here
04_MCP/                     Optional tool integrations (Playwright, MarkItDown)
05_Library/                 Web-app starter and design-system guidance
06_Engine/                  agency CLI, plug-in profiles, gates, retrieval, evals, tests and hooks
.github/, .claude/          Generated discovery links and CI
agency.yaml                 OS configuration: mode, discovery targets and plug-in overrides
```

| If you want to | Read |
|---|---|
| Know the rules every agent follows | [AGENTS.md](AGENTS.md) |
| Run a task the OS way | [Operating guide](00_Agentic-OS/README.md) |
| Understand the architecture | [Architecture](00_README/ARCHITECTURE.md) and the [authority registry](AUTHORITIES.md) |
| Add or improve a plug-in | [Plug-in guide](00_README/PLUGINS.md) and the [backlog](00_Agentic-OS/OPTIMIZATION-BACKLOG.md) |
| Join a project as a teammate | [How we work](00_README/HOW-WE-WORK.md) and the [glossary](00_README/GLOSSARY.md) |
| Follow naming, tag, commit and privacy rules | [Conventions](00_README/CONVENTIONS.md) and [Releasing](00_README/RELEASING.md) |

## Status, privacy and license

Version history: [CHANGELOG.md](CHANGELOG.md). Every example in the template is generic: it names no person, organization or real use case. Customer material stays in a fork's project hubs under the [customer-label rules](00_README/CONVENTIONS.md#4-customer-data-labels), and a release passes the [privacy and publish gate](00_README/RELEASING.md) first.

[MIT](LICENSE). Plug-ins keep their own licenses.
