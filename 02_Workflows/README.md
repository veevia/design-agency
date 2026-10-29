# 02_Workflows

**TL;DR:** Five narrative workflows run the design loop, SOPs contract the recurring operations, prompts are the `/` commands both call, and two plug-in engines (PDG, VPG) mount here when a project needs governed prototype or film production.

## Four layers

| Layer | Where | What it is |
|---|---|---|
| **Workflows (W1–W5)** | [`workflows/`](workflows/) | Narrative procedures: one per loop phase plus one cross-cutting decision flow |
| **SOPs** | [`SOPs/`](SOPs/README.md) | Machine-checkable contracts (front-matter + steps) for recurring operations |
| **Prompts** | [`prompts/`](prompts/) | `/`-invoked commands; workflows and SOPs compose them |
| **Plug-in engines** | `prototype-design/`, `video-production/` (mounts) | Added with `python3 06_Engine/scripts/agency.py plugin add <name>`; driven only through their host-adapter prompts |

Workflows explain the canonical sequence; SOPs contract recurring procedures; prompts invoke bounded actions. Plug-in mounts are read-only from the host: improve them upstream with `/plugin-optimize`.

## Filing contract

Artifacts land in the numbered phase folders of a project hub (create one with `python3 06_Engine/scripts/agency.py hub new <slug>`; the layout comes from `01_Project-Hubs/_template-project/`):

| Phase | Scope root | Decisions (only when W5 requires a record) |
|---|---|---|
| Understand | `<hub>/01_understand/` | `<hub>/01_understand/decisions/` |
| Design | `<hub>/02_design/` or a feature sub-hub beneath it | `<design-scope>/decisions/` |
| Build | `<hub>/03_build/` (PDG and VPG projects live here too) | `<hub>/03_build/decisions/` |
| Learn | `<hub>/04_learn/` | `<hub>/04_learn/decisions/` |

`weekly-status/` is optional; link to it only when the hub already keeps that cadence.

## Workflows

| # | File | Phase | Produces |
|---|---|---|---|
| W1 | [`workflows/W1-understand.md`](workflows/W1-understand.md) | Frame + Understand | Problem frame → research → persona → JTBD → journey |
| W2 | [`workflows/W2-design.md`](workflows/W2-design.md) | Design | POV → brief → PRD |
| W3 | [`workflows/W3-build.md`](workflows/W3-build.md) | Build | Prototype or thin slice + test plan |
| W4 | [`workflows/W4-learn.md`](workflows/W4-learn.md) | Learn | Evidence brief + retro + updated artifacts + forward path |
| W5 | [`workflows/W5-decide.md`](workflows/W5-decide.md) | Cross-cutting | Reused evidence, or one typed record (ADR, PDR, ops note, release) |

Phase closure alone needs no new decision file; gate evidence stays in the phase artifacts.

## Prompts

**Canonical artifacts**

| Prompt | Produces |
|---|---|
| [`/research-synthesize`](prompts/research-synthesize.prompt.md) | UX research report |
| [`/persona-draft`](prompts/persona-draft.prompt.md) | Personas (1–3) |
| [`/jtbd-draft`](prompts/jtbd-draft.prompt.md) | JTBD |
| [`/journey-map`](prompts/journey-map.prompt.md) | User journey map |
| [`/design-pov`](prompts/design-pov.prompt.md) | Design POV |
| [`/design-brief`](prompts/design-brief.prompt.md) | Design brief |
| [`/prd-draft`](prompts/prd-draft.prompt.md) | Product PRD |
| [`/decision-log`](prompts/decision-log.prompt.md) | Reused evidence or one typed decision record (W5) |

**Design judgement**

| Prompt | Purpose |
|---|---|
| [`/trade-off`](prompts/trade-off.prompt.md) | Name what each direction gives up |
| [`/go-wider`](prompts/go-wider.prompt.md) | Generate real alternatives before deciding |
| [`/drift-check`](prompts/drift-check.prompt.md) | Detect a build drifting from its intent |

**Knowledge and context**

| Prompt | Purpose |
|---|---|
| [`/wiki-ingest`](prompts/wiki-ingest.prompt.md) | Ingest a raw source into a hub wiki |
| [`/wiki-query`](prompts/wiki-query.prompt.md) | Citation-grounded answers from a hub wiki |
| [`/wiki-lint`](prompts/wiki-lint.prompt.md) | Severity-ranked wiki health triage |
| [`/context-pull`](prompts/context-pull.prompt.md) | Score the wiki index before loading pages |
| [`/session-snapshot`](prompts/session-snapshot.prompt.md) | End-of-session handoff |

**Capability and OS improvement**

| Prompt | Purpose |
|---|---|
| [`/skill-lint`](prompts/skill-lint.prompt.md) | Run a skill's declared lints |
| [`/eval-run`](prompts/eval-run.prompt.md) | Run golden-task evals |
| [`/skill-refine`](prompts/skill-refine.prompt.md) | Propose one evidence-backed skill refinement |
| [`/capability-spot`](prompts/capability-spot.prompt.md) | Mine snapshots and run records for recurring patterns |
| [`/workflow-audit`](prompts/workflow-audit.prompt.md) | Elicit repeated manual work and route it |
| [`/optimize-loop`](prompts/optimize-loop.prompt.md) | Run a goal + rubric loop to a verified result |
| [`/plugin-optimize`](prompts/plugin-optimize.prompt.md) | Improve a plug-in from a measured baseline, upstream |

**Plug-in host adapters** (exposed in discovery only while the plug-in is mounted)

| Prompt | Plug-in | Purpose |
|---|---|---|
| [`/prototype-design`](prompts/prototype-design.prompt.md) | `prototype-design` (PDG) | Brief → validated prototype in `<hub>/03_build/<name>/` |
| [`/video-production`](prompts/video-production.prompt.md) | `video-production` (VPG) | Product demo film with measured quality and named approvals |

FDE Design Toolkit and UI/UX Pro Max skills arrive through discovery when mounted; they need no adapter prompt.

**Design Sprint Toolkit** (agent `design-sprint-toolkit`): [`/sprint-help`](prompts/sprint-help.prompt.md), [`/sprint-morning-standup`](prompts/sprint-morning-standup.prompt.md), [`/sprint-project-diagnose`](prompts/sprint-project-diagnose.prompt.md), [`/sprint-plan`](prompts/sprint-plan.prompt.md), [`/sprint-facilitate-phase`](prompts/sprint-facilitate-phase.prompt.md), [`/sprint-generate-artifact`](prompts/sprint-generate-artifact.prompt.md), [`/sprint-coach-me`](prompts/sprint-coach-me.prompt.md), [`/sprint-graduate-method`](prompts/sprint-graduate-method.prompt.md).

## How a workflow runs

1. Open the workflow (for example `W1-understand.md`); it lists steps, inputs, and exit gates.
2. Each step names the prompt, skill, or template it uses.
3. Artifacts land in the hub's phase folder; gate evidence stays in those artifacts.
4. A new durable choice goes through W5 (`/decision-log`); nothing else needs a decision file.

## Authoring rules

- Prompts live flat in `prompts/` with front-matter `description:` and `agent: agent`. Link other files through the repository root (`../../02_Workflows/…`) so links resolve from `.github/prompts/` and `.claude/commands/` too.
- New SOPs start from [`SOPs/_template/SOP.md`](SOPs/_template/SOP.md) and pass `python3 06_Engine/harness/lint-sop.py`.
- Never link into a plug-in mount; refer to it with a backticked path.

## Related

- [`../00_README/_templates/`](../00_README/_templates/) — canonical artifact templates
- [`../00_README/_frameworks/design-thinking-loop.md`](../00_README/_frameworks/design-thinking-loop.md) — the loop itself
- [`../03_Agents-and-Skills/README.md`](../03_Agents-and-Skills/README.md) — agents, skills, and the capability lifecycle
- [`../00_Agentic-OS/initiatives/README.md`](../00_Agentic-OS/initiatives/README.md) — optimization initiatives
