# 02_design/

**TL;DR:** Phase 2 — the solution space: commit to a point of view, align on a brief, and specify what to build, with non-goals and guardrails as explicit as goals.

**Workflow:** [W2 — Design](../../../02_Workflows/workflows/W2-design.md) (`02_Workflows/workflows/W2-design.md`)

## Artifacts

| Artifact | Template | Drafting prompt |
|---|---|---|
| Design POV | [`2-1-Design_POV`](../../../00_README/_templates/2-1-Design_POV.template.md) | `/design-pov` |
| Design brief | [`2-2-Design_brief`](../../../00_README/_templates/2-2-Design_brief.template.md) | `/design-brief` |
| Product PRD | [`2-3-Design_PRD`](../../../00_README/_templates/2-3-Design_PRD.template.md) | `/prd-draft` |
| Design handoff | [`2-4-Design_handoff`](../../../00_README/_templates/2-4-Design_handoff.template.md) | — |

## Exit gate — Design → Build

- [ ] The POV's HMWs are carried verbatim into the brief and PRD (no drift)
- [ ] The brief names three outcomes with measurable success metrics
- [ ] The PRD lists non-goals as explicitly as goals, and success metrics include guardrails
- [ ] The PRD names a rollback trigger and mechanism
- [ ] The brief is signed by the design lead, PM and engineering lead; the PRD by every approval row it lists

Record the result in the hub README's [phase-gate table](../README.md#phase-gates). PRD sign-off is binary
([Traffic Light](../../../00_README/_frameworks/traffic-light-decisions.md#5-integration-with-the-4-phase-loop)): **🟢** signed, scope locked, rollback trigger named, or **🔴** not signed — a
named blocker and unblock owner. Open questions *inside* the PRD may stay 🟡, each with a trigger and expiry
(e.g., "until legal reviews data handling by <date>").

## Feature sub-hubs (multi-workstream programs)

With two or more parallel design initiatives — each with its own design partner, scope choices and
decisions — give each workstream its own sub-hub:

```
02_design/
├── 01_[feature-name]-design/    # workstream 1
│   ├── README.md                # status + artifact links for this workstream
│   ├── design-pov.md
│   ├── [feature-name]-PRD.md
│   ├── decisions/               # workstream decisions (typed records)
│   └── _intake/                 # raw inputs for this workstream
├── 02_[feature-name]-design/    # workstream 2
└── decisions/                   # program-level decisions (cross-cutting scope choices)
```

Start from the [sub-hub pattern](_feature-sub-hub/README.md). A single `02_design/` holding every artifact
becomes unnavigable past about two workstreams. A JTBD synthesis
(`00_README/_templates/1-3b-Understand_jtbd-synthesis.template.md`) maps workstreams to sub-hubs.

## Decisions

Design direction, scope trade-offs, non-goals and rollback triggers that later work must follow go in
[`decisions/`](decisions/README.md) as typed records — usually PDRs.
