---
name: stakeholder-map
title: Map who influences the problem by power and interest
description: Map every person or system with a stake in the problem — their interests, influence, and relationship to the primary user. Use when early in Phase 1, after Lightning Talks establish the landscape, when the sprint problem involves multiple teams, approval chains, or external systems, or before defining Sprint Questions.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Early in Phase 1, after Lightning Talks establish the landscape
  - When the sprint problem involves multiple teams, approval chains, or external systems
  - Before defining Sprint Questions — constraints from stakeholders must be visible
  - When the team suspects there are people affected by the solution who haven't been in the room
applies-to: stakeholder alignment, system complexity, hidden constraint identification, XFN planning, sprint scope setting
done_when:
  - Stakeholders are plotted on a power × interest grid
  - Each stakeholder’s position/stance is noted, named not laundered
  - Outer-ring constraints are logged as assumptions
metadata:
  duration: 20–30 min
  team-size: Full sprint team
  sprint-phase: 1 Understand
  redirect-host: alignment-playbook
---

# Stakeholder Map

**TL;DR:** A Stakeholder Map identifies every person, team, or system that has a stake in the sprint's problem space — directly or indirectly. It surfaces the humans and systems that exist *around* the primary user, shapes the constraints the solution must respect, and prevents the sprint from designing something that ignores the people who will need to approve, implement, or live with it.

## When to use

- Early in Phase 1, after Lightning Talks establish the landscape
- When the sprint problem involves multiple teams, approval chains, or external systems
- Before defining Sprint Questions — constraints from stakeholders must be visible
- When the team suspects there are people affected by the solution who haven't been in the room

## The stakeholder map structure

Three rings around the primary user:

```
         ┌─────────────────────────────────────────┐
         │  OUTER: Indirect / System stakeholders  │
         │  ┌─────────────────────────────────────┐│
         │  │  MIDDLE: Direct but non-primary      ││
         │  │  ┌─────────────────────────────────┐ ││
         │  │  │         INNER: Primary user     │ ││
         │  │  │         [Lead Coordinator]      │ ││
         │  │  └─────────────────────────────────┘ ││
         │  └─────────────────────────────────────┘│
         └─────────────────────────────────────────┘
```

| Ring | Who belongs here | Sprint implication |
|---|---|---|
| **Inner** | Primary user — the one we're designing for | Sprint target; prototype participant |
| **Middle** | Users directly affected but not the primary: colleagues, managers, recipients of the primary user's output | Design constraints; secondary considerations |
| **Outer** | Systems, regulators, IT, legal, finance — indirect but influential | Technical and compliance constraints; stakeholders who must approve |

## Stakeholder card format

For each stakeholder, capture:
- **Name / role**
- **Their stake**: what do they care about in this problem space?
- **Influence**: High / Medium / Low (can they block, shape, or ignore the solution?)
- **Relationship to primary user**: who gives them work? who reviews their work?
- **Constraints they impose**: technical, legal, political, process constraints

## Worked example (generic)

```markdown
## Stakeholder Map — Request Triage Sprint · 2026-02-24

### Inner ring — Primary user
- **Lead Coordinator** — Runs the morning assignment round. Stake: workflow efficiency + professional credibility. The design target.

### Middle ring — Direct stakeholders
- **Site Supervisor (Site C)** — Receives assigned requests from the Lead Coordinator. Stake: requests arrive with the right context and parts list so their specialists can act without phoning back for clarification.
- **Operations Manager** (Decider) — Reviews the Lead Coordinator's escalation log weekly. Stake: no missed urgent requests; a clean request history.
- **Customer Care Manager** — Answers customers who chase their booking. Stake: accurate, timely service windows; no surprises.

### Outer ring — Indirect / system stakeholders
- **Legal / Data Protection** — Requires a record of every change to a customer's request. Constraint: every priority decision must be logged with the coordinator's identity and timestamp.
- **IT / Platform Engineering** — Owns the booking inbox and the specialist calendar. Constraint: new features must use the existing API; no new data pipelines without a 3-month approval cycle.
- **AI Model Team** — Owns the ranking model behind the suggested priority. Constraint: model retraining requires 6-week lead time; the urgency score algorithm is not currently configurable per user.
- **Booking channels** (web form, phone line, partner channel) — Source of incoming requests. Constraint: partner-channel terms restrict how its booking details can be displayed; the channel must be shown on every request.

### Constraints surfaced
1. All priority decisions must be logged — anonymous automated actions are not allowed
2. The booking inbox API is the only available integration point — no new pipeline in this sprint
3. The booking channel must be shown when displaying partner-channel details inline
4. Request assignment must flow through the existing specialist calendar

### Open questions for Expert Interviews
- What does Legal require for automatically prioritised requests specifically?
- Can the AI model team expose reasoning fields through the existing API?
```

## Influence × Interest matrix

Plot each stakeholder on a 2×2:

```
HIGH INTEREST
      │
 Manage  │  Collaborate
 closely │  (key players)
─────────┼─────────────── HIGH INFLUENCE
  Keep   │  Keep
informed │  satisfied
      │
LOW INTEREST
```

| Quadrant | Who | Sprint action |
|---|---|---|
| High Interest + High Influence | Decider, primary users | Collaborate; involve in sprint |
| High Interest + Low Influence | End users affected by solution | Inform; may be test participants |
| Low Interest + High Influence | Legal, IT, Finance | Keep satisfied; check constraints early |
| Low Interest + Low Influence | Peripheral users | Monitor; don't over-design for them |

## Agent facilitation guide

When building a stakeholder map from sprint context:
1. Identify the primary user (inner ring)
2. Ask: who receives the output of the primary user's work? Who reviews it? Who works alongside them? → middle ring
3. Ask: what systems does this workflow touch? What teams own those systems? What external parties impose rules? → outer ring
4. For each outer-ring stakeholder: what constraint do they impose on the solution?
5. Produce the influence × interest matrix
6. Flag: any stakeholder whose constraint could invalidate a design direction should feed into Assumption Mapping

## Watch-outs

- **Designing for the outer ring:** Compliance, IT, and legal are constraints, not design targets. A solution that optimises for compliance audit trails at the cost of the Lead Coordinator's workflow is designing for the wrong ring.
- **Missing the indirect users:** The person who receives the coordinator's assigned request (the Site Supervisor) is often invisible in early sprint conversations. Including them prevents designing an assignment flow that works for the coordinator but creates chaos for the Site Supervisor.
- **Influence ≠ importance:** A low-influence user who is directly impacted daily matters more than a high-influence stakeholder who touches the product once a quarter.
- **Static map:** Stakeholder relationships shift. Review the map before the Supervote — a new constraint from IT discovered during the sprint should update the map and potentially the Assumptions Board.

## Connects to

- [Lightning Talks](../lightning-talks/SKILL.md) — middle and outer ring stakeholders are often Lightning Talk speakers
- [Expert Interviews](../expert-interviews/SKILL.md) — constraint-holders in the outer ring are interview targets
- [Assumption Mapping](../assumption-mapping/SKILL.md) — outer ring constraints become assumptions: "we assume IT will allow inline service-contract and parts details via the existing API"
- [Constraint Mapping](../constraint-mapping/SKILL.md) — stakeholder-imposed constraints are formalised here
- [Target](../sprint-target/SKILL.md) — inner ring = sprint target user
