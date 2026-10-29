---
title: Traffic Light Decision Making
type: framework
status: canonical
owner: OS steward
last-updated: 2026-10-29
source: House Traffic Light decision-making practice
tags: [type/framework, purpose/decide, status/canonical, loop/all]
---

# Traffic Light Decision Making

> **TL;DR:** Every architecture or product decision closes with exactly one light — 🟢 green
> (proceed), 🟡 yellow (conditional, with trigger + expiry), or 🔴 red (blocked, with an unblock
> owner). Lifecycle status is a separate field; small ops and release records use a light only when
> current posture matters.

A three-state operating-posture model. It does not replace record type or lifecycle status.
[W5](../../02_Workflows/workflows/W5-decide.md) owns the decision procedure; the
[`traffic-light-decisions`](../../03_Agents-and-Skills/Skills/traffic-light-decisions/SKILL.md) skill
validates records. This file explains what the lights mean.

## 1. The three states

| Light | Meaning | When to use |
|---|---|---|
| 🟢 **Green** | **Decided. Proceed.** | Position taken, ownership assigned, no active blockers. Disagreement heard and set aside. |
| 🟡 **Yellow** | **Conditional. Proceed with named dependency or watch-point.** | Decision made but contingent on a named trigger, data arrival, or external approval. Rollback trigger defined. |
| 🔴 **Red** | **Not decided / escalated / blocked.** | Either actively debated, escalated above the room, or a blocker exists. No forward motion until resolved. |

## 2. Why three, not four

Resist the urge to add Orange, Blue, or "Green-with-notes". Three states force a posture. More states invite hiding.

## 3. Rules

- **Every ADR and PDR has exactly one Traffic Light.** Ops notes and releases add one only when
  operating posture matters. If multiple lights apply, split the decisions.
- **Yellow requires a named trigger.** "Yellow until <event / date / data>". No open-ended yellows.
- **Red requires an owner for unblocking.** Red without an owner becomes institutional rot.
- **Green does not mean unanimous.** It means proceed. `consultation: solo` is valid; invited or
  reviewed work records real consultation rather than inventing dissent.

## 4. Transitions

```
   Red ──► Yellow ──► Green
    ▲        ▲          │
    │        │          ▼
    └────────┴──────── Reopen (rollback trigger fired)
```

Every transition is a dated amendment in the record. Never silently flip a light. Do not use colors
as lifecycle: `status` is `proposed|accepted|superseded|retired`.

Lifecycle transitions carry different meanings: `superseded` requires a mirrored, acyclic successor
chain ending at an accepted record; `retired` means the record ended without replacement and has no
successor link. `canonical: true` is narrower still and may identify only an accepted ADR in the
minimal current architecture contract.

## 5. Integration with the 4-phase loop

| Phase | Typical Traffic Light use |
|---|---|
| **Understand** | Phase exit is 🟢 or 🔴 (inherently binary: we know enough to design, or we don't). Individual research findings can be 🟡 when confidence is low. |
| **Design** | POV sign-off 🟢. Open questions in the PRD are 🟡 with trigger + expiry. PRD sign-off is binary — 🟢 or 🔴. |
| **Build** | Fidelity choice 🟢. Feasibility questions are 🟡 until prototyped. Rollback trigger must be 🟢 before shipping to users. |
| **Learn** | Forward path decision (iterate / ship wider / pivot / stop) is always explicit: 🟢 or 🔴, with the evidence cited. |
| **Cross-cutting gates** (privacy, security, accessibility) | Binary by design — 🟢 (clear) or 🔴 (remediate). Not 🟡. |

## 6. The Yellow discipline

Yellow is where decisions go to die when not managed. Rules for keeping Yellow honest:

1. **Named trigger.** "Yellow until customer security review completes on <date>." Not "Yellow until we have more info."
2. **Owner for closure.** One name, not "the team".
3. **Expiry.** If the trigger doesn't fire by <date>, escalate to Red or force to Green/Red.
4. **Status surfaces Yellows.** Whatever reporting rhythm the project uses lists every open Yellow. Don't bury them.

## 7. Usage in typed decision records

ADRs and PDRs use top-level front matter:

```yaml
status: proposed | accepted | superseded | retired
light: green | yellow | red
owner: <single person>
trigger: <required if yellow>
expiry: <YYYY-MM-DD if yellow>
blocker: <required if red>
unblock_owner: <single person if red>
```

The older embedded `traffic_light_*` block remains valid only in unmigrated historical documents and
non-decision artifacts such as a POV sign-off. New decision records follow the strict templates in
[`03_Agents-and-Skills/Skills/traffic-light-decisions/assets/`](../../03_Agents-and-Skills/Skills/traffic-light-decisions/assets/decision-record.template.md)
— start from the router, which picks ADR, PDR, ops note or release.
