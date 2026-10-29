---
name: design-principles
title: Commit to 3–5 guiding design values
description: Agree on 3–5 guiding values the team commits to in every design decision — the sprint's design constitution. Use after POV Statement and Sprint Questions, before Phase 3 Sketch. Use when the team has disagreements about design direction that reflect underlying values.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - After POV Statement and Sprint Questions — principles articulate the design values that follow from the research
  - Before Phase 3 Sketch — principles influence how sketches are generated
  - When the team has disagreements about design direction that reflect underlying values ("we keep arguing about detail vs. simplicity — let's name which we're committing to")
  - As the evaluative frame for Speed Critique alongside Design Criteria
applies-to: design direction, concept evaluation, trade-off resolution, team alignment, Speed Critique framing
done_when:
  - 3–5 principles are stated, each actionable not platitudinal
  - Each principle implies a concrete design trade-off
  - Principles are agreed and visible for every design decision
metadata:
  duration: 20–30 min
  team-size: Full sprint team; Decider approves
  sprint-phase: 2 Define
---

# Design Principles

**TL;DR:** Design Principles are the 3–5 values the team commits to honouring in every design decision during the sprint. They don't describe what to build — they describe *how* to build it. A principle like "show the evidence, not just the conclusion" means that every concept which hides its reasoning should be questioned. Principles give the team a shared language for evaluating trade-offs: when two things are in tension, which principle wins?

## When to use

- After POV Statement and Sprint Questions — principles articulate the design values that follow from the research
- Before Phase 3 Sketch — principles influence how sketches are generated
- When the team has disagreements about design direction that reflect underlying values ("we keep arguing about detail vs. simplicity — let's name which we're committing to")
- As the evaluative frame for Speed Critique alongside Design Criteria

## Principles vs. Criteria

| | Design Principles | Design Criteria |
|---|---|---|
| **Form** | Value statement: "always [verb] [thing]" | Testable standard: "a winning concept must..." |
| **Applies to** | How the solution behaves | What the solution does |
| **Evaluated by** | Team judgment during critique | Usability test results |
| **Examples** | "Trust through transparency" | "Must show the reasons for a priority inline" |
| **Use together** | Yes — principles inform which criteria to set |

## The principle formula

> **[Verb] [thing]** — [one sentence that explains the trade-off this principle resolves]

Examples:
- "Show the work, not just the verdict" — when showing AI output, always show the reasons behind it; never present a conclusion without its reasoning, because coordinators need to own their decisions
- "One interaction, not a workflow" — every action the coordinator takes should complete in ≤2 taps; multi-step flows exist only when compliance requires them
- "Serve the expert, not the novice" — the Lead Coordinator has 5 years of domain expertise; don't explain things they already know; reserve UI space for information, not instruction

## Steps

1. **Mine the research for values (5 min):** Read back the POV Statement and key research findings. What values does this research imply? What do users care about that the team might trade away?

2. **Individual drafting (8 min, silent):** Each person writes candidate principles on stickies — one per sticky, in the verb format.

3. **Post and cluster (5 min):** Post all stickies. Cluster duplicates. Name each cluster.

4. **Test for tension (5 min):** Good principles resolve a real trade-off. For each candidate: "What would we design differently if we committed to this?" If the answer is "nothing," the principle is too weak.

5. **Decider selects (3–5 min):** Select 3–5 final principles. Name them. Post prominently — they stay on the wall through Phase 4.

## Worked example (generic)

```markdown
## Design Principles — Request Triage Sprint · 2026-02-24

### 1. Show the evidence, not just the verdict
When presenting a suggested priority or urgency score, always show why — the records, the basis, the reasoning. A coordinator who can see the evidence can disagree intelligently. A coordinator who can only see the conclusion has no choice but to trust or reject blindly.

*Trade-off this resolves:* Clean UI vs. transparency. We choose transparency.

---

### 2. Stay in the flow
Every check should be completable without leaving the request view. System-switching is the enemy of the coordinator's morning rhythm. If a design requires them to navigate away, redesign it.

*Trade-off this resolves:* Rich detail vs. workflow continuity. We choose continuity.

---

### 3. One tap, not a form
Assigning, prioritising, and flagging actions should complete in ≤2 interactions. Multi-step flows exist only when a legal requirement explicitly demands them — and even then, minimise.

*Trade-off this resolves:* Completeness vs. speed. We choose speed for high-frequency actions.

---

### 4. Respect the expert
The Lead Coordinator has 5 years of triage experience. Design for their expertise, not for a first-time user. Don't explain what a unit fault code means. Don't add confirmation dialogs for actions they take 30 times a morning.

*Trade-off this resolves:* Discoverability vs. efficiency. We choose efficiency for expert users.

---

### 5. Log without friction
Every priority decision must be logged (legal requirement). But logging should be automatic — the coordinator should never have to take a separate action to keep the request history complete.

*Trade-off this resolves:* Compliance vs. workflow. We choose compliance that doesn't interrupt workflow.
```

## Principle quality tests

| Test | Question |
|---|---|
| **Resolves a trade-off** | What would we design differently if we *didn't* follow this principle? |
| **Action-guiding** | Can I use this principle to evaluate a specific design decision? |
| **Team-specific** | Is this principle obvious, or does it reflect a genuine choice this team made? |
| **Not a constraint** | A constraint rules something out entirely. A principle guides how to navigate tension. |

## Agent facilitation guide

When generating Design Principles:
1. Read the POV Statement — what values are implied by the user's need and insight?
2. Read the JTBD canvas — what does the user care about that the team might trade away?
3. Identify 3–5 recurring tensions in the research: speed vs. completeness, simplicity vs. transparency, expert vs. novice, compliance vs. experience
4. Write one principle per tension — verb-first, with the trade-off made explicit
5. Test each: "What would we design differently if we didn't follow this?" If nothing changes, drop it

## Watch-outs

- **Obvious principles:** "Be accessible" and "respect the user" are not sprint-specific principles — they're industry hygiene. A principle earns its place by representing a genuine trade-off the *team* is making for *this* sprint.
- **Principles as constraints:** "Don't use custom components" is a constraint, not a principle. Constraints rule out options; principles guide choices among remaining options.
- **Ignoring them after Phase 2:** Principles posted on the wall and never mentioned again in Speed Critique are decoration. The Facilitator must explicitly reference them: "Does this sketch honour Principle 2?"
- **Too many principles:** 3–5 is optimal. 8 principles means the team hasn't prioritised — and in a trade-off, they'll have no guidance on which principle wins.

## Connects to

- [POV Statement](../pov-statement/SKILL.md) — the user's insight implies the values
- [Design Criteria](../design-criteria/SKILL.md) — principles inform which criteria are set
- [Speed Critique](../speed-critique/SKILL.md) — principles are the evaluative frame during critique
- [Supervote](../supervote/SKILL.md) — Decider's rationale should reference at least one principle
