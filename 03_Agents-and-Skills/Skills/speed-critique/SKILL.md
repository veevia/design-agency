---
name: speed-critique
title: Critique concepts fast against the sprint questions
description: Structured 3-minute critique of each sketch — focused on what's interesting, not what's wrong. Efficient, fair, and opinion-surface without debate. Use after Art Museum and Heat Map Voting, before Straw Poll. Use when you need structured discussion of multiple concepts without debate spiral, or when the team has a mix of strong and weak concepts and needs to extract the best elements.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - After Art Museum and Heat Map Voting, before Straw Poll
  - When you need structured discussion of multiple concepts without debate spiral
  - When the team has a mix of strong and weak concepts and needs to extract the best elements
applies-to: design critique, idea refinement, combining concepts, decision prep
done_when:
  - Each concept is reviewed in a timeboxed pass
  - Standout elements and concerns are captured against the sprint questions
  - Output is ready to inform the supervote
metadata:
  duration: 3 min per sketch + 1 min transition
  team-size: Full sprint team; one designated Scribe
  sprint-phase: 4 Decide
---

# Speed Critique

**TL;DR:** A time-boxed, structured walk-through of every solution sketch. The facilitator leads, team members call out standout ideas, a Scribe captures everything on sticky notes, and the sketch creator speaks last (or not at all). Three minutes per sketch. The goal is to surface ideas worth carrying forward — not to debate or defend.

## When to use

- After Art Museum and Heat Map Voting, before Straw Poll
- When you need structured discussion of multiple concepts without debate spiral
- When the team has a mix of strong and weak concepts and needs to extract the best elements

## Roles

| Role | Responsibility |
|---|---|
| **Facilitator** | Keeps time, reads back the team's heat map observations, moves discussion forward |
| **Scribe** | Writes standout ideas on sticky notes and posts them above each sketch |
| **Team members** | Call out interesting/compelling elements — not defects |
| **Sketch creator** | Silent until the end. Speaks only to clarify a specific misunderstanding. |

## Steps

1. **Gather at the first sketch (1 min):** Facilitator reads the sketch title, then gives everyone 30 seconds to re-read it silently.
2. **Observation round (2 min):** Facilitator asks: "What's interesting here? What stood out?" Team members call out specific elements. Scribe captures each as a sticky note posted above the sketch.
3. **Concerns (30 sec):** Facilitator asks: "Any concerns or questions?" Scribe captures these too (different colour sticky).
4. **Creator speaks last (30 sec):** The creator can correct a specific misunderstanding ("The panel 2 detail actually shows X, not Y") but cannot defend or explain motivation.
5. **Move to next sketch.** Repeat.
6. **After all sketches:** Scribe reads back all standout idea stickies. Team looks for themes and combinable elements.

## The language of Speed Critique

Speed Critique uses specific language to keep feedback productive:

| Instead of... | Say... |
|---|---|
| "This is bad because..." | "What I'm not seeing is..." |
| "I don't think users want this" | "An assumption here seems to be that users will [X] — worth testing" |
| "This won't work technically" | "A feasibility question: can we [X] in our stack?" |
| "I prefer the other sketch" | Save preference for Straw Poll — don't do comparative judgment here |

## Scribe sticky format

```
[Standout idea - green]                [Concern - yellow]
"Urgency score is prominent            "Assumes the AI ranking is
 and action-oriented"                   accurate enough to show a score"
```

## Agent facilitation guide

When running Speed Critique on a set of solution sketches:
1. For each sketch: write a structured critique in 3 sections
   - **What's interesting:** 2–3 specific elements that address Sprint Questions
   - **Key assumption:** The biggest unverified belief the concept depends on
   - **Combinable element:** One idea from this sketch that could be incorporated into another
2. After all sketches: compile the "best-of" list — elements worth carrying forward regardless of which sketch wins

Output format:
```markdown
## Speed Critique — [Sprint Name]

### Sketch: "Reasons-First Triage"
**Interesting:**
- Urgency score visible at queue level — answers Q2 without opening a detail view
- Inline CRM, service-contract, and inventory-system records remove the "open another system" friction [observed | pain point from journey map]

**Key assumption:** Coordinators will trust a numeric urgency score enough to act on it

**Combinable element:** The urgency score display could be added to any winning sketch

---

### Sketch: "One-Tap Assign"
**Interesting:**
- Assignment gesture is one action — eliminates the coordinator's current 3-step manual assignment

**Key assumption:** The right specialist is always correctly pre-selected by the system

**Combinable element:** The one-tap assign action could be added to Reasons-First Triage as a secondary CTA
```

## Watch-outs

- **Creator defending while critique is live:** The creator speaks last, for 30 seconds max. Politely interrupt: "We'll hear from you at the end."
- **Discussion becoming debate:** Speed Critique is observation, not argument. If the team starts debating, call it: "Let's capture this as a concern and move on."
- **3 minutes isn't enough for complex sketches:** It is. Longer critiques become self-indulgent. If something needs more discussion, it goes into the Straw Poll debrief — not here.
- **Scribe can't keep up:** Scribe writes keywords, not full sentences. "Urgency score" not "The way the urgency score is displayed prominently in the queue is interesting."

## Connects to

- [Heat Map Voting](../heat-map-voting/SKILL.md) — dot clusters focus the critique agenda
- [Straw Poll](../straw-poll/SKILL.md) — follows Speed Critique
- [Supervote](../supervote/SKILL.md) — Decider makes final call after seeing Speed Critique output
