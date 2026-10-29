# 03_Agents-and-Skills

**TL;DR:** Skills are reusable disciplines and methods, agents are operating contracts that combine skills into a role, and every capability moves through one lifecycle — propose → draft → harness gates → stable — while plug-ins arrive whole through `agency.py plugin add`.

The generated catalog of every installed capability (native and plug-in) is [`INDEX.md`](INDEX.md); search it before writing anything new.

## Layout

| Surface | Native source | Discovery links (generated) |
|---|---|---|
| Skills | `Skills/<slug>/SKILL.md` (+ `references/`, `scripts/`, `assets/`, `templates/`) | `.github/skills/<slug>/` · `.claude/skills/<slug>/` |
| Agents | `Agents/<slug>.agent.md` | `.github/agents/<slug>.agent.md` · `.claude/agents/<slug>.md` |
| Prompts | `02_Workflows/prompts/<name>.prompt.md` | `.github/prompts/<name>.prompt.md` · `.claude/commands/<name>.md` |

Discovery links are relative symlinks written by `python3 06_Engine/scripts/agency.py sync`; edit only the native source. Sources sit at the same depth as their links, so relative links resolve through either path — link through the repository root (`../../…` from agents and prompts, `../../../…` from a `SKILL.md`).

## The agent fleet

| Agent | Role | Loads | Hands off to |
|---|---|---|---|
| [`design-synthesist`](Agents/design-synthesist.agent.md) | Evidence → JTBD, personas, journey, POV — cited and tagged | `context-pull`, `evidence-tagging`, `canonical-artifacts`, `house-principles` | `prototype-runner-qa`, `demo-deck-producer` |
| [`design-sprint-toolkit`](Agents/design-sprint-toolkit.agent.md) | Diagnose, right-size, and facilitate sprints; produce and coach artifacts | `design-sprint-tookit`, `design-thinking-loop`, `alignment-playbook` | `design-synthesist`, `skill-agent-smith` |
| [`prototype-runner-qa`](Agents/prototype-runner-qa.agent.md) | Drive the PDG plug-in to a verified prototype; safe dev servers; browser QA | `design-system-as-infrastructure`, `goal-harness` | `demo-deck-producer`, `repo-steward` |
| [`demo-deck-producer`](Agents/demo-deck-producer.agent.md) | Grounded scripts and verified decks; drive the VPG plug-in for demo films | `extreme-clarity`, `whiteboard-storyboard`, `rubric-authoring` | `repo-steward` |
| [`goal-runner`](Agents/goal-runner.agent.md) | Run a goal + rubric loop to PASS or a reported block | `goal-harness`, `rubric-authoring`, `evidence-tagging` | `skill-agent-smith`, `repo-steward` |
| [`skill-agent-smith`](Agents/skill-agent-smith.agent.md) | Author and refine capabilities against the harness gates | `rubric-authoring`, `goal-harness` | `repo-steward` |
| [`repo-steward`](Agents/repo-steward.agent.md) | Pathspec-scoped, verified commits; pushes only on request | `extreme-clarity` | the user (push, publish) |

Every agent declares inputs, outputs, side effects with required permissions, done-when, skills, and handoffs. Publishing, pushing, and sending anything outside the repository always need the user's explicit authorization; engine human gates (PDG, VPG) are never self-approved.

## Native skills

| Group | Skills |
|---|---|
| Evidence and clarity | `evidence-tagging` · `extreme-clarity` · `alignment-playbook` · `house-principles` · `persona-critic` |
| Design loop and artifacts | `problem-framing` · `design-thinking-loop` · `canonical-artifacts` · `drift-check` · `design-sprint-tookit` · `whiteboard-storyboard` |
| Design sprint methods | 62 method skills across six phases (e.g. `how-might-we` · `assumption-mapping` · `decision-matrix` · `five-act-interview`), indexed by the `design-sprint-tookit` hub |
| Decisions | `decision-capture` (whether to write) · `traffic-light-decisions` (how to write and validate) |
| Knowledge | `wiki-maintenance` · `wiki-ingest` · `wiki-query` · `wiki-lint` · `context-pull` · `context-intake` |
| Design system | `design-system-as-infrastructure` · `figma-icon-sync` |
| Presentation and video | `demo-master` (transcript → self-contained animated HTML deck) · `remotion` (React → rendered MP4) |
| Long-horizon work | `goal-harness` · `rubric-authoring` |

Each `SKILL.md` carries `name`, a verb-first `title`, a `description` with a "Use when …" trigger, `status`, `when_to_load`, and either an executable contract (inputs, outputs, `done_when`, lints) or `contract-exempt` for knowledge skills.

## Plug-ins

| Plug-in | Adds | Mount |
|---|---|---|
| `fde-design-toolkit` | Forward-deployed design skills (and, in the full edition, reviewer agents) | `03_Agents-and-Skills/Skills/fde-design-toolkit/` |
| `ui-ux-pro-max` | UI/UX styles, palettes, and stack guidance | `03_Agents-and-Skills/Skills/ui-ux-pro-max-skill/` |
| `anthropic-skills` | Five Apache-2.0 skills the engines bind (frontend design, web artifacts, web-app testing, brand guidelines, skill creation) | `03_Agents-and-Skills/Skills/anthropic-skills/` |
| `impeccable` | Frontend design fluency: polish, audit and critique commands | `03_Agents-and-Skills/Skills/impeccable/` |
| `video-shotcraft` | Cinematic shot recipes for Remotion product videos | `03_Agents-and-Skills/Skills/video-shotcraft/` |
| `prototype-design` | The PDG engine + host adapters (`/prototype-design`, `prototype-runner-qa`, SOP) | `02_Workflows/prototype-design/` |
| `video-production` | The VPG engine + host adapters (`/video-production`, SOP) | `02_Workflows/video-production/` |

PDG and VPG bind skills by name in their own graphs. `plugin status <engine>` lists the companion plug-ins that
supply the bound skills the native library does not ([engine skill bindings](../00_README/PLUGINS.md#engine-skill-bindings)).

```sh
python3 06_Engine/scripts/agency.py plugin list
python3 06_Engine/scripts/agency.py plugin add <name> [--edition E] [--source URL_OR_PATH]
python3 06_Engine/scripts/agency.py plugin status|check|smoke|report <name>
```

Plug-in skills appear in discovery automatically once mounted; host adapters stay hidden until their plug-in is present. A mount is read-only from the host: improve a plug-in in its own repository with `/plugin-optimize` and re-pin.

## Capability lifecycle

```
propose ──▶ draft ──▶ harness gates ──▶ stable
   ▲            │            │             │
   │            └── fails ───┘             └── signals (evals, lints, reviewer frowns) ──▶ /skill-refine
   └── /capability-spot · /workflow-audit · /sprint-graduate-method
plug-ins: agency.py plugin add <name> ──▶ plugin check + smoke ──▶ discovery (no host edits)
```

1. **Propose** — a backlog row in `00_Agentic-OS/OPTIMIZATION-BACKLOG.md` and, when concrete, a stub in `Skills/_proposed/<slug>/`, `Agents/_proposed/<slug>.agent.md`, or `02_Workflows/SOPs/_proposed/<id>/`. Proposals are outside discovery and the gates.
2. **Draft** — with the owner's approval, move the stub to its native location with `status: draft` (`skill-agent-smith` authors from `06_Engine/harness/SKILL.template.md`).
3. **Harness gates** — all must pass before commit:
   ```sh
   python3 06_Engine/harness/spec-compliance.py
   python3 06_Engine/harness/lint-skill.py --contract <slug>      # ≥10/12 or contract-exempt
   python3 06_Engine/harness/lint-skill.py --all --severity error
   python3 06_Engine/evals/run-evals.py                           # when the skill has evals
   python3 06_Engine/harness/lint-sop.py
   python3 06_Engine/harness/check-links.py                       # includes depth parity
   python3 00_Agentic-OS/agentic-os-review.py --fast              # every MUST row
   ```
4. **Stable** — after real use with evidence (for example three engagements without structural change, or a passing eval), set `status: stable`. Keep refining with `/skill-refine`; retire with `status: deprecated` and a pointer to the replacement.

## Using a capability in your runtime

- **Copilot (VS Code, CLI)** reads `.github/skills/`, `.github/agents/`, and `.github/prompts/`; type `/` for prompts or pick an agent.
- **Claude Code** reads `.claude/skills/`, `.claude/agents/`, and `.claude/commands/`.
- **Any other agent or a human** — open the `SKILL.md` or `.agent.md` and follow it; every file doubles as a checklist.

## See also

- Workflows and prompts: [`02_Workflows/README.md`](../02_Workflows/README.md) · Operating rules: [`AGENTS.md`](../AGENTS.md)
- Harness schemas: [`06_Engine/harness/skill-schema.md`](../06_Engine/harness/skill-schema.md) · [`06_Engine/harness/agent-schema.md`](../06_Engine/harness/agent-schema.md)
- Plug-in profiles: [`00_README/PLUGINS.md`](../00_README/PLUGINS.md)
