---
type: reference
slug: agentic-os-architecture
status: active
created: 2026-10-29
updated: 2026-10-29
owner: OS steward
tags: [type/reference, status/active, purpose/reference, scope/workspace, scope/agent-os]
---

# Design Agency OS — architecture

**TL;DR:** Six responsibilities (L0–L5), each owned by one contract, support one proportionate task procedure; capabilities come from native sources or pinned plug-ins and reach every agent runtime through generated discovery links.

This page maps the [six contracts](../00_Agentic-OS/README.md); it adds no policy. [AUTHORITIES](../AUTHORITIES.md)
registers ownership.

## 1. Six responsibilities, not a directory stack

| Layer / contract | Responsibility | Where it lives |
|---|---|---|
| [L0 Authority & safety](../00_Agentic-OS/decisions/l0-authority-and-safety.md) | Which sources, rules and permissions govern work | `AUTHORITIES.md`, `AGENTS.md`, CONVENTIONS, plug-in boundaries |
| [L1 Knowledge & context](../00_Agentic-OS/decisions/l1-knowledge-and-context.md) | Supply relevant knowledge; preserve progress | Hub intake and `_wiki/`, task checkpoints, `06_Engine/retrieval/` |
| [L2 Capabilities & interfaces](../00_Agentic-OS/decisions/l2-capabilities-and-interfaces.md) | Reusable skills, agents, prompts, tools, plug-ins | `03_Agents-and-Skills/`, `02_Workflows/prompts/`, `04_MCP/`, `06_Engine/plugins/`, `06_Engine/agency/` |
| [L3 Task control](../00_Agentic-OS/decisions/l3-task-control.md) | Decide what happens next | Operating guide, `02_Workflows/` (W1–W5, SOPs), plug-in engines' own gates |
| [L4 Delivery & outcomes](../00_Agentic-OS/decisions/l4-delivery-and-outcomes.md) | Produce the requested result | Answers, hub phase folders, prototypes, films, code |
| [L5 Verification & learning](../00_Agentic-OS/decisions/l5-verification-and-learning.md) | Prove results; improve through measured loops | `00_Agentic-OS/agentic-os-review.py`, `06_Engine/harness/`, evals, tests, initiatives, `_runs/` |

L0 applies throughout. L1 supplies context, L2 reusable execution, L3 controls work, L4 produces results,
L5 checks them and feeds corrections back to L3, findings to L1 and reviewed improvements to L2.

## 2. How capabilities reach a runtime

```
 sources (authoritative)                     engine (06_Engine/agency)          discovery (generated)
 ─────────────────────────                   ─────────────────────────          ─────────────────────
 03_Agents-and-Skills/Skills/<slug>/   ─┐                                    ┌─▶ .github/skills/  .claude/skills/
 03_Agents-and-Skills/Agents/*.agent.md ├─▶  catalog ─▶ collision check ─▶  ├─▶ .github/agents/  .claude/agents/
 02_Workflows/prompts/*.prompt.md      ─┤    + host-adapter gating          └─▶ .github/prompts/ .claude/commands/
 plug-in mounts (pinned submodules)    ─┘    + plug-in profiles                   + 03_Agents-and-Skills/INDEX.md
```

- Every discovery entry is a relative symlink written by `python3 06_Engine/scripts/agency.py sync`; the
  review fails on drift. Unmanaged files are never overwritten.
- Native skills sit at `Skills/<slug>/`, agents and prompts directly in their folders: the same depth as their
  discovery links, so relative links work through both paths (checked by `check-links.py`).
- Host adapters (for example `/prototype-design`) are native files that drive a plug-in; they stay out of
  discovery until that plug-in is mounted.

## 3. Plug-ins

A plug-in is an independent repository mounted at a fixed path as a pinned git submodule and described by a
profile in `06_Engine/plugins/`. The profile declares editions (recognised by a marker file), what the
plug-in contributes, which host adapters it unlocks, its requirements, and its checks with declared side
effects. See [PLUGINS](PLUGINS.md).

| Plug-in | Mount | Contributes |
|---|---|---|
| FDE Design Toolkit | `03_Agents-and-Skills/Skills/fde-design-toolkit/` | Skills; the full edition adds reviewer agents and commands |
| PDG | `02_Workflows/prototype-design/` | Prototype engine driven by `/prototype-design` and its SOP |
| VPG | `02_Workflows/video-production/` | Demo-film engine driven by `/video-production` and its SOP |
| UI/UX Pro Max | `03_Agents-and-Skills/Skills/ui-ux-pro-max-skill/` | Third-party UI/UX skill |

## 4. Task procedure versus project lifecycle

- **Task:** scope → retrieve → execute → verify → hand off ([operating guide](../00_Agentic-OS/README.md)).
- **Project:** Understand → Design → Build → Learn ([workflows](../02_Workflows/README.md)).

A routine fix needs no PRD or ADR. A project phase still needs its acceptance evidence. W5 runs only for a
new durable choice, an explicit capture request or a lifecycle change.

## 5. Modes

`agency.yaml` sets `mode: template` for the blank harness (only `_template-project`, no plug-ins mounted) and
`mode: workspace` for a repository doing real work. `agency.py hub new` and `agency.py plugin add` switch it.

## 6. What the architecture does not claim

Passing the review proves repository integrity: contracts, schemas, links, catalog and discovery are
consistent. It does not prove that a runtime loaded a capability, that a plug-in performs well or that a
deliverable meets its users' needs; those claims need runtime evidence recorded in the
[capability map](domain-coverage-map.md) or a task's own evidence.
