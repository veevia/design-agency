# AUTHORITIES — one source of truth per concept

**TL;DR:** When sources disagree, the authoritative source below wins; catalogs, discovery links, indexes, mounted plug-ins and summaries are derived views.

## Authority registry

| Concept | Authoritative source | Derived views / boundary |
|---|---|---|
| Agent operating rules | [AGENTS.md](AGENTS.md) | [CLAUDE.md](CLAUDE.md) and [copilot-instructions](.github/copilot-instructions.md) only route to it |
| Task procedure | [Operating guide](00_Agentic-OS/README.md) | Prompts, agents and SOPs route there |
| L0 — Authority & safety | [aos-0001](00_Agentic-OS/decisions/l0-authority-and-safety.md) | Source ownership, permission, repository and plug-in boundaries |
| L1 — Knowledge & context | [aos-0002](00_Agentic-OS/decisions/l1-knowledge-and-context.md) | Retrieval, durable memory, resume points |
| L2 — Capabilities & interfaces | [aos-0003](00_Agentic-OS/decisions/l2-capabilities-and-interfaces.md) | Capability contracts, plug-in profiles, generated discovery |
| L3 — Task control | [aos-0004](00_Agentic-OS/decisions/l3-task-control.md) | Scope, workflows, decision capture, engine gates |
| L4 — Delivery & outcomes | [aos-0005](00_Agentic-OS/decisions/l4-delivery-and-outcomes.md) | Acceptance and handoff |
| L5 — Verification & learning | [aos-0006](00_Agentic-OS/decisions/l5-verification-and-learning.md) | Proof, measured improvement loops, promotion |
| Architecture map | The six contracts above | [ARCHITECTURE.md](00_README/ARCHITECTURE.md) explains them; it adds no policy |
| OS configuration (mode, discovery targets, plug-in overrides) | [agency.yaml](agency.yaml) | `agency.py status` |
| Plug-in profiles | [06_Engine/plugins/](06_Engine/plugins/) | Plug-in table in the [catalog](03_Agents-and-Skills/INDEX.md); [PLUGINS.md](00_README/PLUGINS.md) explains the schema |
| Plug-in versions | `.gitmodules` and each mount's pinned submodule commit | `agency.py plugin status <name>` |
| Plug-in capabilities | The plug-in's own repository | Mounted copy and discovery links; never edited in place |
| Native skills | `03_Agents-and-Skills/Skills/<slug>/SKILL.md` | Catalog, `.github/skills/`, `.claude/skills/` |
| Native agents | `03_Agents-and-Skills/Agents/<slug>.agent.md` | `.github/agents/`, `.claude/agents/` |
| Prompts | `02_Workflows/prompts/<name>.prompt.md` | `.github/prompts/`, `.claude/commands/` |
| Discovery wiring | [agency engine](06_Engine/agency/) (`agency.py sync`) | Everything in `.github/{skills,agents,prompts}` and `.claude/{skills,agents,commands}` |
| Capability catalog | [build-skill-index.py](06_Engine/harness/build-skill-index.py) | [INDEX.md](03_Agents-and-Skills/INDEX.md) (generated) |
| SOP contracts | `02_Workflows/SOPs/<slug>/SOP.md`, checked by [lint-sop.py](06_Engine/harness/lint-sop.py) | Catalog SOP table |
| Project workflows W1–W5 | [02_Workflows/workflows/](02_Workflows/workflows/) | Prompts and SOPs |
| Decision procedure | [W5](02_Workflows/workflows/W5-decide.md), the [decision reference](03_Agents-and-Skills/Skills/traffic-light-decisions/references/REFERENCE.md) and [check_decision.py](03_Agents-and-Skills/Skills/traffic-light-decisions/scripts/check_decision.py) | Prompts and indexes route there |
| Discipline | [Frameworks](00_README/_frameworks/) explain why | Skills operationalize; wiki pages apply |
| Artifact templates | [00_README/_templates/](00_README/_templates/) | Hub copies |
| Naming, tags, commit and secret policy | [CONVENTIONS](00_README/CONVENTIONS.md) | Local guides link here |
| Capability coverage | [domain-coverage-map.md](00_README/domain-coverage-map.md), checked by [check-capability-map.py](06_Engine/harness/check-capability-map.py) | Static record checks, not runtime certification |
| Improvement queue | [OPTIMIZATION-BACKLOG.md](00_Agentic-OS/OPTIMIZATION-BACKLOG.md) | Plug-in defects stay in the plug-in's own tracker |
| Integrity verdict | [agentic-os-review.py](00_Agentic-OS/agentic-os-review.py) | CI, hooks and `agency.py check` call it |
| Commit and push checks | [pre-commit.sh](06_Engine/scripts/pre-commit.sh), [pre-push.sh](06_Engine/scripts/pre-push.sh) | Installed by [install-hooks.sh](06_Engine/scripts/install-hooks.sh) |

## Decision identity

The front-matter `id` is a record's identity, not its filename. Record type, lifecycle `status`,
Traffic Light `light` and `canonical` are separate fields (see [W5](02_Workflows/workflows/W5-decide.md)).

| Namespace | Record home | Citation |
|---|---|---|
| Operating system | `00_Agentic-OS/decisions/` | `aos-NNNN` (exactly six canonical, one per L0–L5) |
| Project hub | `01_Project-Hubs/<hub>/**/decisions/` | `<hub>-NNNN` |
| Plug-in | The plug-in's own repository | The plug-in's own scheme |
