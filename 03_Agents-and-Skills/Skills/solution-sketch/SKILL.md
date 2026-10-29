---
name: solution-sketch
title: Detail one concept into a testable sketch
description: A detailed, annotated 3-panel storyboard of one solution concept. The artefact that goes to the Decision phase for critique and voting. Use after Crazy 8s, to develop the top 1–2 ideas in depth. Use when a concept needs to be communicated to the full team without live explanation, or as input to the Art Museum, Speed Critique, and voting methods.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - After Crazy 8s, to develop the top 1–2 ideas in depth
  - When a concept needs to be communicated to the full team without live explanation
  - As input to the Art Museum, Speed Critique, and voting methods
applies-to: concept communication, design decision input, prototype planning, critique preparation
done_when:
  - A single concept is drawn as a 3-panel self-explanatory sketch
  - The sketch is anonymous, titled, and detailed enough to test
  - Critical UI/interaction moments are explicit, not implied
metadata:
  duration: 30–60 min (individual, silent)
  team-size: Individual
  sprint-phase: 3 Sketch
---

# Solution Sketch

**TL;DR:** The Solution Sketch is a detailed, self-explanatory concept proposal — typically 3 panels showing the key steps of the user experience, with annotations explaining the design decisions. Unlike Crazy 8s (divergent, fast), this is convergent and careful. It must communicate clearly to someone who wasn't in the room — because the critique process (Phase 4) is silent.

## When to use

- After Crazy 8s, to develop the top 1–2 ideas in depth
- When a concept needs to be communicated to the full team without live explanation
- As input to the Art Museum, Speed Critique, and voting methods

## Materials

- 3 sheets of A4 paper (one per panel), or a 3-panel template
- Permanent marker or felt-tip pen
- Optional: sticky note for the title/concept name

## Structure

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│              │   │              │   │              │
│   Panel 1    │──►│   Panel 2    │──►│   Panel 3    │
│  (set-up)    │   │  (key moment)│   │  (outcome)   │
│              │   │              │   │              │
│ [annotation] │   │ [annotation] │   │ [annotation] │
└──────────────┘   └──────────────┘   └──────────────┘
        
Title: [Concept name — one strong, memorable phrase]
```

**The 3 panels:**
- **Panel 1 — Set-up:** What context/trigger brings the user to this screen or moment?
- **Panel 2 — Key interaction:** The core design idea. The thing that solves the sprint target moment.
- **Panel 3 — Outcome:** What happens next? What does success look like for the user?

## The rules

1. **No names.** The sketch is anonymous until after voting. Removes authority bias.
2. **Self-explanatory.** Someone who missed the sprint must be able to understand it from the sketch + annotations alone. If you need to explain it verbally, add more annotations.
3. **Ugly is fine.** The quality criterion is clarity, not aesthetics. Rectangles + labels + arrows.
4. **The title is the concept.** Give it a strong, memorable name that captures the core idea — not "Design Option B."
5. **One concept per sketch.** Don't combine two ideas into one sketch. Each sketch must be clearly one coherent concept.

## What to annotate

Every panel should have short explanatory notes pointing to key design elements:
- "AI urgency score (0–100) per request"
- "Tapping opens a record card — not a new page"
- "Green = confirmed by a coordinator; amber = AI-only"
- "This step replaced 3 manual cross-checks"

## Example sketch structure

For sprint target: "The Lead Coordinator checking a request (Stage 2)"

```
Title: "Reasons-First Triage"

Panel 1 — Context
[Request queue with scores]
"The coordinator opens the request system — each request shows:
record count, urgency score, skill tag"
"Clear-cut urgent requests pre-sorted to top"

Panel 2 — Key Interaction (Checking moment)
[Request detail card opens on tap]
"Inline: CRM, service-contract, and inventory records with reliability rating
One-tap 'Mark confirmed' after reviewing records
No separate system required"
"Urgency score updates after the coordinator's mark"

Panel 3 — Outcome
[Request moves to Confirmed state in queue]
"Request now shows 'Confirmed by LC — [date]'
Site C automatically notified
Coordinator's checking time: < 2 min"
```

## Agent facilitation guide

When producing a Solution Sketch from a Crazy 8s top panel:
1. Expand the Crazy 8 concept into 3 distinct scenes
2. Name the concept with a single memorable phrase (noun-first: "Reasons Card", "One-Tap Assign", "Urgency Layer")
3. Write annotations for every non-obvious design element — aim for 3–5 per panel
4. Confirm: Panel 2 directly addresses the sprint target moment
5. Confirm: Panel 3 shows the user's success state (not a loading screen or next-step message)

Output format:
```markdown
## Solution Sketch — [Concept Name]

**Sprint target:** [user + moment]
**Core idea:** [one sentence — what this design does differently]

### Panel 1 — [Stage name]
**Visual:** [describe the UI state/screen]
**Annotations:**
- [design note 1]
- [design note 2]

### Panel 2 — [Key interaction]
**Visual:** [describe the core interaction]
**Annotations:**
- [design note]
- [the key differentiating element]

### Panel 3 — [Outcome]
**Visual:** [describe the success state]
**Annotations:**
- [what changed for the user]
- [how this answers Sprint Question X]
```

## Watch-outs

- **The "everything in one sketch" mistake:** Three panels ≠ three features. Three panels = one coherent experience. Narrow the concept.
- **Panel 2 is not the key moment:** If your target is "checking a booking" but Panel 2 shows "navigation", the sketch is off-target.
- **No annotations:** An unannotated sketch is ambiguous. During the silent critique (Art Museum), team members can only interpret — they can't ask. Annotate.
- **Named sketches:** Anonymity is enforced until after the straw poll. Named sketches bias voting toward authority, not quality.

## Connects to

- [Crazy 8s](../crazy-8s/SKILL.md) — top panel becomes the Solution Sketch concept
- [Art Museum](../art-museum/SKILL.md) — sketches are posted and reviewed here
- [Heat Map Voting](../heat-map-voting/SKILL.md) — dot voting on sketch elements
- [Storyboard](../storyboard/SKILL.md) — winning sketch is expanded to a 10–15 panel storyboard
