---
name: constraint-mapping
title: Separate hard constraints from soft assumptions
description: Explicitly document every constraint — technical, business, legal, time — before sketching begins, so the team designs within reality. Use after the Ecosystem Map and Stakeholder Map surface potential constraints, before Phase 3 Sketch. Use when the team includes engineers who know there are technical limits that others aren't aware of.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - After the Ecosystem Map and Stakeholder Map surface potential constraints
  - Before Phase 3 Sketch — constraints must be known before sketching begins
  - When the team includes engineers who know there are technical limits that others aren't aware of
  - When a previous sprint or project failed because of an unexpected constraint discovered late
applies-to: constraint identification, feasibility framing, scope boundaries, Design Criteria input, prototype scope setting
done_when:
  - Each item is classified as a hard constraint or a soft assumption
  - Hard constraints are sourced (who/what imposes them)
  - Soft assumptions are routed to assumption mapping for testing
metadata:
  duration: 20–30 min
  team-size: Full sprint team; technical and legal stakeholders contribute
  sprint-phase: 2 Define
---

# Constraint Mapping

**TL;DR:** Constraints are the boundaries the solution must stay within. Constraint Mapping makes them explicit before any sketching happens — so the team doesn't spend Phase 3 generating ideas that are technically impossible, legally blocked, or organisationally undeliverable. Naming constraints early is not defeatist; it focuses creative energy on the space where good solutions actually exist.

## When to use

- After the Ecosystem Map and Stakeholder Map surface potential constraints
- Before Phase 3 Sketch — constraints must be known before sketching begins
- When the team includes engineers who know there are technical limits that others aren't aware of
- When a previous sprint or project failed because of an unexpected constraint discovered late

## Four constraint types

| Type | What it covers | Where it comes from |
|---|---|---|
| **Technical** | API limits, integration restrictions, data availability, platform capabilities | Engineering Lightning Talks, Ecosystem Map |
| **Business / Organisational** | Timeline, budget, team capacity, organisational approval processes | Decider, project context |
| **Legal / Compliance** | Compliance requirements, data privacy, attribution rules, audit obligations | Legal/compliance stakeholders, Stakeholder Map |
| **Design** | Brand guidelines, accessibility standards, platform design system rules | Design system, platform requirements |

## Constraint card format

Each constraint is documented with:
- **Type:** Technical / Business / Legal / Design
- **Statement:** What is constrained
- **Reason:** Why this constraint exists
- **Impact on design:** What kinds of solutions this rules out — or rules in
- **Certainty:** Known / Probable / Assumed (if assumed, flag for validation)

## Worked example (generic)

```markdown
## Constraint Map — Request Triage Sprint · 2026-02-24

### Technical constraints
| Constraint | Reason | Design impact | Certainty |
|---|---|---|---|
| All new features must use the existing booking inbox API — no new data pipelines | IT approval for new pipelines takes 3 months | Cannot surface data not currently available through the booking inbox API endpoints | Known |
| The ranking API exists but has no urgency score field in its current schema | API was built for a simple urgent / routine flag | Urgency score display requires an API schema update — not available in sprint timeframe | Known |
| The specialist calendar only accepts assignments through its existing form API | Legacy system; no direct UI override permitted | One-tap assign must write to the existing form API; cannot bypass | Known |

### Business / Organisational constraints
| Constraint | Reason | Design impact | Certainty |
|---|---|---|---|
| Prototype must be testable within 6 hours of build time | Sprint timeline; Day 4 is build day | Figma click-through only; no coded prototype | Known |
| Rollout must work across all three sites without site-specific customisation | IT maintenance overhead; one product for every site | Design must not use site-specific terminology or assignment logic | Known |
| Solution must use the design-system component kit only | Platform integration requirement; brand compliance | No custom component library; all UI from the design-system component kit | Known |

### Legal / Compliance constraints
| Constraint | Reason | Design impact | Certainty |
|---|---|---|---|
| All priority decisions must be logged with coordinator identity and timestamp | Customer complaints and service-contract claims need a record of who decided what | Automatic prioritisation with no coordinator action is not allowed | Known |
| Bookings from a partner channel must show the booking channel in any display | Partner agreement | All inline booking displays must show the channel; no unlabelled partner content | Known |
| Customers' personal data must not be shown without access control | GDPR / data privacy | Filter or redact personal data in request summaries before display | Probable (check with Legal) |

### Design constraints
| Constraint | Reason | Design impact | Certainty |
|---|---|---|---|
| Must meet WCAG AA accessibility standards | Company accessibility policy | Colour contrast ≥4.5:1; keyboard navigable; screen reader compatible | Known |
| Must use desktop-first layout (the coordinator's primary device) | Observed: the Lead Coordinator and all tested coordinators work on desktop | No mobile-first design; desktop layout is primary | Known |

### Constraints ruled OUT (not applicable to this sprint)
- Mobile responsiveness — not a sprint constraint; desktop only
- Specialist mobile app — out of scope; this sprint covers the triage console only
```

## The "design within the box" principle

Constraints define the box. The team's job in Phase 3 is to find the best possible solution *within* the box. If the best solution requires breaking a constraint, that is a separate decision (an ADR with a Traffic Light) — not something to silently design around.

When a proposed sketch violates a constraint:
- Name it explicitly in Speed Critique: "This concept requires a new data pipeline — that's a known constraint."
- The Decider can choose to reconsider the constraint (if it's assumed) or eliminate the concept from consideration.

## Agent facilitation guide

When generating a Constraint Map:
1. Read the Ecosystem Map — annotate all ⚠️ items as constraints
2. Read the Stakeholder Map — outer-ring stakeholders are the primary source of legal/organisational constraints
3. Interview the tech lead: what API, system, and data limits apply?
4. Tag each constraint: Known / Probable / Assumed — flag Assumed constraints for validation before the prototype is built
5. For each constraint: write the "design impact" — what kinds of solutions does this rule out?
6. List constraints that are NOT applicable — this prevents false limitations from creeping into the design conversation

## Watch-outs

- **Constraints as excuses:** "We can't do that because of constraints" is the most common blocker to good sprint outcomes. Constraints should narrow the solution space, not eliminate it. If a constraint rules out all good solutions, question the constraint first.
- **Assumed constraints treated as known:** "I think Legal requires X" is not the same as "Legal confirmed X in writing." Tag assumptions; validate before building.
- **Constraint discovered after prototyping:** This invalidates the prototype. If an engineer raises a technical constraint on Day 4 that nobody knew about on Day 2, something went wrong in Phase 1. Constraints must be surfaced in Understand, not in Prototype.
- **No "ruled out" list:** Constraints that don't apply to this sprint should be named and cleared. A team that thinks they're constrained by something they're not will design around a phantom boundary.

## Connects to

- [Ecosystem Map](../ecosystem-map/SKILL.md) — technical constraints come from ⚠️ annotations
- [Stakeholder Map](../stakeholder-map/SKILL.md) — outer-ring stakeholders are the source of legal constraints
- [Design Criteria](../design-criteria/SKILL.md) — constraint compliance criteria derive from here
- [Solution Sketch](../solution-sketch/SKILL.md) — annotate sketches that approach constraint boundaries
- [Speed Critique](../speed-critique/SKILL.md) — constraints are the "feasibility question" raised during critique
