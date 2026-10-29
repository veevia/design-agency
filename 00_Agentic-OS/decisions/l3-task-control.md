---
type: decision
schema_version: decision-record/v2
record_type: adr
id: aos-0004
slug: l3-task-control
layer: L3
status: accepted
light: green
canonical: true
owner: OS steward
decided_by: OS steward
consultation: solo
created: 2026-10-29
updated: 2026-10-29
tags: [type/decision, record/adr, status/accepted, light/green, scope/workspace]
---
# aos-0004 — L3 Task control

> **TL;DR:** Keep one scope, plan when needed and choose proportionate workflows; routine work needs no decision record.

## Context

Uniform ceremony buries small tasks in paperwork, while unscoped work drifts. Engines with their own
state machines (PDG, VPG) must keep control of their transitions and human gates.

## Alternatives

| Option | Benefit | Cost / risk |
|---|---|---|
| A — Full workflow and record for every task | Uniform audit trail | Context bloat and record backlog |
| B — Scoped control with proportionate workflows | Effort matches risk | Judgment needed for scope and durable change |

## Decision

We will choose B.

1. Keep one scope per task: outcome, constraints, non-goals, permissions, acceptance criteria. Multi-step work
   keeps one live plan; simple tasks need none.
2. Follow the [operating guide](../README.md). Understand → Design → Build → Learn is the project lifecycle;
   L0–L5 are responsibilities, not mandatory stages.
3. [W5](../../02_Workflows/workflows/W5-decide.md) handles new durable choices, explicit capture requests and
   lifecycle changes, typed as ADR, PDR, ops note or release. Routine progress, fixes and settings stay in task
   evidence. Traffic Light is separate from lifecycle; Yellow needs a trigger and expiry.
4. Keep exactly six canonical workspace ADRs, one per L0–L5. Amend compatible wording in the owning layer;
   use a reviewed successor for a material reversal.
5. Plug-in engines own their transitions and human gates. Host adapters drive them and report their state;
   no adapter or agent approves on a human's behalf.
6. Prefer quality and useful progress over invented cost ceilings: stop for uncertainty, repeated no-progress,
   real service limits or required human authority, with a precise resume path.

## Consequences

- Easier: small tasks stay small; engines keep authority over their own gates.
- Harder: scope and durable-change judgments remain explicit. Less paperwork never waives acceptance or safety.

## Consultation

- Solo decision by the template maintainer; wording drafted with an agent and reviewed by the owner.
- Material dissent: none recorded.

## Reversal condition

Reopen for repeated scope loss or duplicate tracking. Stop and re-scope the affected work; repair the
existing procedure before adding workflows.
