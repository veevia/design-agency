---
title: "[Project Name]"
type: project
status: active
tenant: internal                 # customer | internal | personal
loop-phase: understand
project: <hub-slug>
owner: <single name>
created: YYYY-MM-DD
tags: [type/project, project/<hub-slug>, tenant/internal, status/active, loop/understand]
---

# `[Project Name]`

> **Owner:** `<single name>`
> **Goal:** `<one sentence — who we help do what, and the signal that proves it>`
> **Current phase:** Understand

**TL;DR:** `<one sentence — the problem, for whom, and where the project stands today>`.

*This is the hub skeleton. `python3 06_Engine/scripts/agency.py hub new <hub-slug>` copies it to
`01_Project-Hubs/<hub-slug>/`; then replace the placeholders above. Keep the `**Current phase:**` label —
the wiki index reads it.*

## Setup checklist

Delete this section once it's done.

1. Fill in the front matter, owner, goal, current phase and TL;DR above. For a customer project set
   `tenant: customer` and treat the whole hub as customer content; label confidential files `_TENANT.md`
   ([CONVENTIONS §4](../../00_README/CONVENTIONS.md#4-customer-data-labels)).
2. Run the **initiative intake**: copy
   [`0-1-Intake_initiative.template.md`](../../00_README/_templates/0-1-Intake_initiative.template.md) to
   `intake.md` here. Fill sections A–E, then send §F as the kickoff.
3. Drop raw inputs into [`00_context_intake/`](00_context_intake/README.md) and ingest them into the
   [wiki](_wiki/README.md) with `/wiki-ingest`.
4. Frame the problem, then work through [`01_understand/`](01_understand/README.md). Each phase README says
   what comes next.
5. Create `weekly-status/` only if the project has a real stakeholder reporting cadence.

## Structure

```
<hub-slug>/
├── README.md              # identity, current phase, phase-gate dashboard (this file)
├── intake.md              # initiative intake (from 0-1-Intake_initiative.template.md)
├── 00_context_intake/     # raw, immutable source material — the wiki cites it, nobody edits it
├── _wiki/                 # LLM-maintained knowledge: entities, concepts, sources, syntheses
├── 01_understand/         # problem frame, research, survey, JTBD, journey maps        (W1)
│   └── decisions/         # durable choices made in Understand (typed records, via W5)
├── 02_design/             # POV, brief, PRD, handoff; feature sub-hubs                   (W2)
│   └── decisions/
├── 03_build/              # prototypes, engine projects, test plans                      (W3)
│   └── decisions/
├── 04_learn/              # evidence briefs, retros, forward path                        (W4)
│   └── decisions/
├── stakeholders/          # one-page profile per XFN function
└── _drafts/               # local-only captures (git-ignored)
```

- **Multi-workstream programs:** with two or more parallel design initiatives, use feature sub-hubs under
  `02_design/` ([pattern](02_design/_feature-sub-hub/README.md)).
- **Engine projects** — a prototype-design (PDG) run or a video-production (VPG) film — live in a phase
  folder, usually `03_build/<name>/`; the engine keeps its state there.
- **Artifacts** are copied from the [template catalog](../../00_README/_templates/README.md) only when you
  start them. Don't pre-fill empty stubs.
- **Decisions** live in the `decisions/` folder of the phase they govern, as typed records with IDs
  `<hub-slug>-NNNN`. Reuse existing rationale first; [W5](../../02_Workflows/workflows/W5-decide.md) decides
  whether a record is needed at all.

## Phase gates

Each gate is met or not met. Record the light, the owner and a link to the evidence — usually the phase's exit
artifact. Closing a phase needs gate evidence, not a new decision file.

| Gate | Question | Light | Owner | Evidence |
|---|---|---|---|---|
| Understand → Design | Problem space understood well enough to design against? | — | — | — |
| Design → Build | PRD reviewed, scope and non-goals locked, rollback trigger named? | — | — | — |
| Build → Learn | Shippable to real users or a representative test audience, with a test plan? | — | — | — |
| Learn → Next | Forward path chosen with evidence: iterate, ship wider, pivot or stop? | — | — | — |

A 🟡 names its trigger and expiry in the Evidence cell; a 🔴 names its blocker and unblock owner.

## Front matter for this hub's files

```yaml
---
title: <artifact name>
type: <template-for value, e.g. jtbd>
tags: [type/<type>, project/<hub-slug>, tenant/<customer|internal>, status/draft, loop/<phase>]
status: draft
tenant: <customer|internal|personal>
loop-phase: <understand|design|build|learn>
project: <hub-slug>
owner: <single name>
created: YYYY-MM-DD
informed-by: [<upstream artifact or source>]    # at least one relationship field
---
```

## Links

- The loop: [`design-thinking-loop.md`](../../00_README/_frameworks/design-thinking-loop.md) ·
  the one-pager: [How we work](../../00_README/HOW-WE-WORK.md)
- Templates: [catalog](../../00_README/_templates/README.md) · Workflows:
  [`02_Workflows/`](../../02_Workflows/README.md) · Prompts: [`02_Workflows/prompts/`](../../02_Workflows/prompts/)
