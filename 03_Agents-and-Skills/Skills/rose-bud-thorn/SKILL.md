---
name: rose-bud-thorn
title: Triage what's working, emerging, and painful
description: Evaluate an existing solution or experience through three lenses — what works (Rose), what could improve (Thorn), and new opportunities (Bud). Use when the sprint topic involves improving or replacing an existing product or workflow, during or after Lightning Talks, when the team has just seen a demo of the current product, or as a complement to Competitive Landscape.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - When the sprint topic involves improving or replacing an existing product or workflow
  - During or after Lightning Talks, when the team has just seen a demo of the current product
  - As a complement to Competitive Landscape — use Rose Bud Thorn to evaluate analogous products in addition to your own
  - When the team is at risk of designing something entirely new that throws away what currently works
  - Before writing HMW notes — Rose Bud Thorn generates better HMW inputs than raw frustration lists
applies-to: existing solution critique, appreciative analysis, opportunity identification, HMW generation, competitive review
done_when:
  - Items are sorted into rose (working), bud (emerging), thorn (painful)
  - Thorns and buds are mined for HMWs
  - The highest-signal items are prioritised for action
metadata:
  duration: 20–30 min
  team-size: Full sprint team
  sprint-phase: 1 Understand
---

# Rose, Bud, Thorn

**TL;DR:** Rose Bud Thorn is a structured appreciative-inquiry technique for evaluating an existing product, process, or experience. Unlike unstructured critique, it forces balanced analysis: what's already working (Rose), what's a risk or pain (Thorn), and what's an emerging opportunity worth exploring (Bud). It produces a richer input for HMW note generation than pure criticism — and avoids the team anchoring exclusively on pain points while ignoring what should be preserved.

## When to use

- When the sprint topic involves improving or replacing an existing product or workflow
- During or after Lightning Talks, when the team has just seen a demo of the current product
- As a complement to Competitive Landscape — use Rose Bud Thorn to evaluate analogous products in addition to your own
- When the team is at risk of designing something entirely new that throws away what currently works
- Before writing HMW notes — Rose Bud Thorn generates better HMW inputs than raw frustration lists

## The three lenses

| Lens | Symbol | What it captures | Sprint use |
|---|---|---|---|
| **Rose** | 🌹 | Positive: what works, what users value, what should be preserved | Design constraint: don't break this |
| **Thorn** | 🌵 | Negative: what doesn't work, what frustrates, what creates friction | HMW source: "how might we fix this?" |
| **Bud** | 🌱 | Potential: emerging opportunity, something not yet fully realised, an idea worth exploring | Sprint fuel: "how might we build on this?" |

## Steps

1. **Define the subject (2 min):** What are we evaluating? The current booking inbox? A competitor product shown in Lightning Demos? The current assignment process? Be specific.

2. **Silent observation (3–5 min):** If evaluating a product, demo it briefly so all team members have a shared reference. Everyone observes silently.

3. **Individual sticky writing (8–10 min, silent):** Each person writes Rose stickies (green), Thorn stickies (red/pink), and Bud stickies (yellow). One observation per sticky.

4. **Post and read (5 min):** Post all stickies on the relevant section of the wall. Facilitator reads aloud by category.

5. **Discussion (5 min):** Focus on: which Thorns generate the strongest HMW notes? Which Buds overlap with Sprint Questions? Which Roses are constraints — things the solution must not break?

6. **Generate HMW notes (5 min):** From Thorns and Buds, write HMW notes. Add them to the Affinity Map pile.

## Output format

```markdown
## Rose Bud Thorn — [Product / Experience being evaluated] · [Sprint Name] · [Date]

### 🌹 Roses — What works / what to preserve
- Booking inbox layout is familiar to anyone who uses email — low learning curve [observed]
- Alerts for requests flagged "outage" are reliable — trusted by coordinators [reported]
- The printed morning request sheet is an established habit — coordinators check it first thing every morning [observed]
- Assignment confirmation text gives coordinators a paper trail they trust [reported]

### 🌵 Thorns — What doesn't work / what creates friction
- No urgency indicator — coordinators open 3–4 other systems per request [observed]
- Assignment form is 7 steps — slower than phoning the site directly [observed]
- No way to see if a colleague has already picked up a request — duplicate handling common [reported]
- "Routine" queue is ignored on busy mornings — coverage gap [reported]
- AI ranking exists in backend but is invisible to users [observed — product review]

### 🌱 Buds — Opportunities / emerging potential
- If the AI ranking were surfaced with an urgency score, it could replace most manual cross-referencing [assumed — needs validation]
- One-tap assignment based on request type is technically feasible with current API [reported — engineering talk]
- Coordinators and site supervisors could share notes on tricky requests — social trust network opportunity [reported — coordinator interview]
- Past request outcome data could train a "was this really urgent?" predictor [assumed — data team conversation]

### HMW notes generated
- HMW make the AI ranking visible and trustworthy enough to act on? (from Thorn 5)
- HMW reduce assignment to one interaction instead of seven steps? (from Thorn 2)
- HMW let coordinators see if a request has already been picked up by a colleague? (from Thorn 3)
- HMW build on the morning request-sheet habit to surface the most urgent requests first? (from Rose 3 × Bud 1)
```

## Rose Bud Thorn for competitive analysis

Apply the same lens to competitor or analogous products shown in Lightning Demos:

```markdown
## Rose Bud Thorn — ride-hailing app driver-tracking view

### 🌹 Roses
- Live driver position and ETA visible inline — no need to phone anyone
- Colour-coded status indicators are immediately interpretable

### 🌵 Thorns
- Built for one trip at a time — doesn't scale to a queue of 38 requests
- No workflow integration — the booking ends at the trip; nothing hands off to downstream tools

### 🌱 Buds
- "Driver is arriving" push creates a sense of certainty — could adapt for confirmed urgent requests ("Specialist on the way, ETA 09:40")
```

## Agent facilitation guide

When generating a Rose Bud Thorn analysis:
1. Identify the subject (existing product, competitor, current workflow)
2. Extract Roses from: observed positive behaviours, reported satisfaction, features users praise, existing habits that indicate value
3. Extract Thorns from: observed workarounds, reported frustrations, pain points in research, features users skip
4. Extract Buds from: engineering possibilities mentioned in talks, analogous products, unmet jobs-to-be-done, Thorn × Rose combinations ("what if we kept X but fixed Y?")
5. For each Thorn and Bud: write a HMW note

## Watch-outs

- **All Thorns, no Roses:** Teams under time pressure default to listing problems. If the Roses column is empty, the team is in pure critique mode — which produces solutions that throw away what currently works.
- **Generic Roses:** "It's easy to use" — too vague. Specific: "Coordinators open the booking inbox first every morning — it has become a trusted daily habit." Generic Roses don't constrain design usefully.
- **Buds that are already solutions:** "Add an urgency score" is a solution. The Bud version: "If ranking data were visible, it might reduce cross-referencing." Buds point toward opportunity; solutions point toward execution.
- **Evaluating too many subjects at once:** One Rose Bud Thorn per subject. Don't mix the current product and a competitor in the same canvas.

## Connects to

- [Lightning Talks](../lightning-talks/SKILL.md) — demos trigger Rose Bud Thorn analysis
- [Competitive Landscape](../competitive-landscape/SKILL.md) — analogous products are evaluated with Rose Bud Thorn
- [How Might We](../how-might-we/SKILL.md) — Thorns and Buds are the richest HMW source
- [Affinity Map](../affinity-map/SKILL.md) — HMW notes from this exercise add to the affinity map
