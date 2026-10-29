---
title: "W3 — Build"
type: workflow
workflow-id: W3
status: canonical
owner: OS steward
last-updated: 2026-10-29
loop-phase: build
inputs:
  - Signed Product PRD
  - Approved Design Brief and POV
outputs:
  - Prototype or shippable increment (form varies — Figma, code, paper)
  - Existing task evidence, plus typed records only for new durable build-time choices
  - Weekly statuses throughout build
source: design-thinking-loop.md + 2-3-Design_PRD.template.md + 2-4-Design_handoff.template.md + 3-1-Build_test-plan.template.md + 0-2-Ops_operating-rhythm.template.md
tags: [type/workflow, loop/build, purpose/build, status/canonical]
---

# W3 — Build

> **TL;DR:** Make the smallest thing that tests the riskiest assumption. Ship it to a real user or representative test audience. Keep build evidence with the work; route only new durable choices through W5.

## When to run

- After **W2 — Design** gate has cleared (PRD signed)
- For iteration loops mid-build when a prototype reveals a gap — don't halt the loop, iterate within W3

## Who runs it

| Role | Responsibility |
|---|---|
| Design lead | Protects design intent; reviews build artifacts |
| Engineering lead | Drives implementation |
| PM (if separate) | Tracks progress against PRD; prioritizes trade-offs |
| QA / Research (for user testing prep) | Prepares test protocol |

## Capabilities used

- Skills: `design-system-as-infrastructure`, `design-thinking-loop` (fidelity ladder), `drift-check`, `goal-harness`
- Agent: `prototype-runner-qa`; `repo-steward` for scoped commits
- Plug-in path: when a prototype should run through the governed Prototype Production Graph, use `/prototype-design` — it first checks `python3 06_Engine/scripts/agency.py plugin status prototype-design`, files the project in `<project-hub>/03_build/<name>/`, and stops at every human gate

## What cross-functional partners will see

| Partner | They'll receive | They'll be asked to | Time |
|---|---|---|---|
| PM | Weekly status; each material scope or trade-off typed decision record | Prioritize riskiest assumption; unblock scope questions; confirm rollback trigger | ongoing |
| Engineering lead | PRD (already signed); fidelity choice; slice scope | Own the build; name the rollback trigger; log architectural decisions as ADRs | ongoing |
| Marketing / GTM | Prototype preview before user test | Flag anything that undermines the pitch or positioning | 30 min |
| Legal / Privacy / Security | Test plan before the slice reaches real users; any §Privacy-affecting change | Confirm 🟢 before shipping to real users | 30 min |
| Executive sponsor | Weekly status; only 🔴 items if they escalate | Unblock 🔴s; otherwise stay out of the way | as needed |
| Research participants (for test) | Test invite + consent | 30–45 min session with the prototype | 45 min each |

## Fidelity ladder

Choose fidelity to match the riskiest assumption. Don't over-build.

| Fidelity | When to use | Typical effort |
|---|---|---|
| Paper / storyboard | Testing concept comprehension | Hours |
| Wireframe / clickable Figma | Testing flow and information architecture | 1–3 days |
| High-fi prototype (Figma or code stub) | Testing visual + interaction details | 3–7 days |
| Thin production slice (feature flag, small segment) | Testing real-world behavior | 1–3 sprints |
| Full release | After thin slice has learned enough | Variable |

Start at the lowest fidelity that can answer the question.

## Steps

### Step 1 — Identify the riskiest assumption

1. From the PRD, list the top 3 assumptions that, if wrong, would change the plan.
2. Rank by (likelihood of being wrong) × (cost if wrong).
3. The top-ranked assumption is what this build cycle tests.

**Exit criterion:** One assumption named as the focus for this build slice.

### Step 2 — Choose fidelity

1. Match fidelity to assumption type (per ladder above).
2. If the team wants higher fidelity "to look serious," push back. Fidelity costs — pay only when needed.

**Exit criterion:** Fidelity and rationale recorded in existing prototype/task notes. Use a PDR only
if a new durable product choice needs separate capture through [W5](W5-decide.md); non-obvious does not mean architectural.

### Step 3 — Define the smallest testable slice

1. One user story from the PRD or one path across stages of the journey map.
2. Defer everything outside the slice. This is not "full feature minus polish" — it's "one path end to end."

**Exit criterion:** Slice scope written down, agreed with PM + engineering.

### Step 4 — Build

1. Engineering/design builds the slice per PRD acceptance criteria and [`2-4-Design_handoff.template.md`](../../00_README/_templates/2-4-Design_handoff.template.md) specs.
2. Reuse existing decisions. Route new durable architecture/scope choices through `W5 — Decide`; ordinary implementation and refactoring stay in task evidence.
3. Weekly status (`0-2-Ops_operating-rhythm.template.md`) captures deltas, not totals.
4. Standups (at a cadence that fits the team — no dogma here) surface blockers early.

**Exit criterion:** Slice runs end-to-end in a representative environment.

### Step 5 — Prepare to learn

Build isn't done until it can teach us something. Before declaring the slice "built":

- [ ] Test protocol ready — fill [`3-1-Build_test-plan.template.md`](../../00_README/_templates/3-1-Build_test-plan.template.md) (who tests, what tasks, what instrumentation)
- [ ] Metrics from PRD §6 are instrumented (or a plan exists if that requires a separate workstream)
- [ ] Rollback mechanism is exercised at least once (even if only in staging)
- [ ] Access to test audience is confirmed

**Exit criterion:** Slice is testable, not just functional.

### Step 6 — Close the phase gate

Per `design-thinking-loop.md` BUILD → LEARN gate:

- [ ] Something is shippable to a real user or representative test audience
- [ ] Instrumentation exists for the PRD success metrics (or its gap is explicitly accepted)
- [ ] Rollback is known to work

Record readiness, acceptance evidence, and the next phase in the existing test plan or project phase
block. Phase closure alone needs no new decision file; use W5 only for a new durable choice,
explicit capture request, or lifecycle change.

## Build-time discipline

- **Don't defer blocking questions into the slice.** Resolve a PRD question with evidence or existing
  rationale before continuing; use W5 only when its durable-choice criteria apply.
- **Don't gold-plate.** If the slice tests the core assumption, it's done — even if pixels aren't perfect yet.
- **Don't skip the rollback test.** A rollback you haven't exercised is theoretical.
- **Don't let build drift from PRD.** If the build is drifting, version-bump the PRD — don't silently build something else.

## Stop conditions

- Slice scope expands mid-sprint beyond what was agreed in Step 3 → pause, re-run Step 3 or go back to W2 for a PRD amendment
- Engineering finds a feasibility problem that materially changes the PRD → back to W2, not a Band-Aid in W3
- Instrumentation can't be built in time → explicitly accept the measurement gap in writing; do not proceed as if it's fine

## Artifacts produced

- The prototype or shippable slice itself
- `<project-hub>/03_build/decisions/NNNN-*.md` (for material durable decisions/actions, typed via W5)
- `<project-hub>/03_build/YYYY-MM-DD-<topic>-test-plan.md`
- `<project-hub>/03_build/prototype-notes.md` (optional build-time design rationale)
- `<project-hub>/weekly-status/YYYY-MM-DD-week-<n>-status.md` only when the hub already uses weekly reporting

## Next workflow

→ **W4 — Learn**

---

*Workflow grounded in `design-thinking-loop.md` BUILD phase. The core discipline is fidelity-matching and assumption-testing: build the smallest thing that answers the riskiest question, not the most impressive demo.*
