---
name: prototyping-principles
title: Apply the just-enough-fidelity prototyping rules
description: Set the right fidelity target before building — prototype just enough to get honest reactions, not a finished product. Use when at the start of Prototype day, before role assignment, when the team is debating how much to build or which tool to use, or when the prototype scope is expanding beyond what the sprint questions require.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - At the start of Prototype day, before role assignment
  - When the team is debating how much to build or which tool to use
  - When the prototype scope is expanding beyond what the sprint questions require
  - When a team member wants to code a real backend "just to make it feel right"
applies-to: prototype scoping, fidelity decisions, build prioritisation, sprint day 4 planning, assumption testing
done_when:
  - Fidelity is matched to the question being tested, no higher
  - The prototype is a façade — only the tested path is real
  - Build effort is timeboxed to the sprint, not productionised
metadata:
  duration: 15 min (alignment) + build time varies
  team-size: Full sprint team
  sprint-phase: 5 Prototype
---

# Prototyping Principles

**TL;DR:** Before anyone opens a design tool or writes a line of code, the team agrees on what the prototype needs to be. The guiding question is not "what can we build?" but "what is the minimum needed to get an honest reaction to our critical assumptions?" A prototype that took three days to polish tests nothing the sprint needed to know. A prototype that looks broken tests nothing either. The goal is to find the fidelity level that makes the participant forget they're looking at a fake.

## When to use

- At the start of Prototype day, before role assignment
- When the team is debating how much to build or which tool to use
- When the prototype scope is expanding beyond what the sprint questions require
- When a team member wants to code a real backend "just to make it feel right"

## The core principle: Goldilocks Fidelity

The prototype must be realistic enough to evoke honest reactions — and no more.

| Fidelity level | When to use | Risk |
|---|---|---|
| **Paper / whiteboard** | Testing navigation logic, information architecture, step flow | Too low — participants can't suspend disbelief |
| **Static screens (Figma or a slide deck)** | Testing visual hierarchy, layout decisions, copy clarity | Right for most sprint assumptions |
| **Click-through prototype** | Testing task completion, navigation flow, multi-step interactions | Right when the assumption is about motion or sequence |
| **Coded prototype** | Testing real data loading, API latency perception, live input | Only justified if the assumption requires real behaviour |
| **Wizard of Oz** | Testing AI behaviour, backend responses, edge cases | A person simulates the system; participant doesn't know |

**Default:** Static screens with click-through linking covers 80% of sprint hypotheses. Choose coded or Wizard of Oz only when the assumption explicitly requires it.

## What the prototype is NOT

- A finished product
- A production-ready implementation
- A stress-test for edge cases
- A complete feature set
- A device for impressing stakeholders
- Evidence that the concept will work at scale

The prototype serves one purpose: **test the critical assumptions identified on the Assumptions Board.**

## The "one surface" rule

Build only the screens that appear in the storyboard. If a screen isn't in the storyboard, it doesn't go in the prototype. Every extra screen added during build is a scope decision that should be approved against the sprint questions — not made silently.

Exceptions:
- Error states: only build the error state if testing error recovery is a sprint question
- Empty states: only include if first-use experience is a sprint assumption
- Loading states: only build if latency perception is on the Assumptions Board

## Tool selection guide

| Context | Recommended tool | Avoid |
|---|---|---|
| Web/mobile UI | Figma (click-through prototype mode) | Coding from scratch |
| Enterprise product | Figma + the design-system component kit | A slide deck (fidelity too low) |
| Data-heavy dashboard | Figma with real-ish numbers typed in | Connecting to live data |
| Conversational AI interface | A form tool or Figma + Wizard of Oz | A real LLM backend |
| Physical product | Paper model + photos in Figma | 3D printing (too slow) |
| Native mobile app | Figma mobile prototype or a dedicated mobile prototyping tool | Native code in the platform IDE (too slow) |

## Realistic content rule

Real (or realistic) content matters more than visual polish:

- Use real names, real companies, real amounts — not "User Name" or "Lorem ipsum"
- The content in Panel 1 should set up a specific scenario that a real user could recognise
- Numbers, dates, and status labels must be internally consistent across all screens

Participants spot fake placeholder content immediately and will hedge their reactions. Realistic content lets them respond to the idea, not the artifice.

## Agent facilitation guide

When advising a team on prototype scope:
1. Read the Assumptions Board — list only the critical (high importance, low certainty) assumptions
2. For each: identify the minimum screen(s) needed to surface an honest reaction
3. Propose a prototype scope: "We need [N] screens. We do NOT need [X, Y, Z]."
4. Flag any assumption that cannot be tested with a static prototype — recommend Wizard of Oz or note as out-of-sprint scope
5. Estimate build time at 1 Maker = 1–2 screens per hour at sprint fidelity

Output:
```markdown
## Prototype scope — [Sprint name]

### In scope (maps to Assumptions Board)
| Assumption | Screen(s) required | Tool | Est. time |
|---|---|---|---|
| Users interpret the urgency score correctly | Queue view with score visible | Figma | 1h |
| Inline records reduce system-switching | Request detail with records list | Figma | 1.5h |
| Suggested priority acted on without checking | Detail view + set-priority CTA | Figma | 1h |

### Out of scope (not on Assumptions Board)
- Settings page
- Onboarding flow
- Error states (not a sprint question)
- Mobile responsive layout

### Total estimated build: 3.5h — fits within sprint day 4 (6h available)
```

## Watch-outs

- **"While we're at it...":** Any addition not tied to an Assumptions Board item is scope creep. Name it as such and defer.
- **Pixel perfection:** Sprint prototypes are not portfolio pieces. If the team is spending time on font weights and icon alignment, redirect to the assumptions that still need screens.
- **Coding it to "make it feel real":** Coding introduces bugs, deployment steps, and debugging that eat the build day. Unless the assumption requires real data, Figma prototypes test faster.
- **Fake loading states with `sleep(2)`:** If latency isn't a sprint assumption, don't add it. If it is, Wizard of Oz a 2-second pause.
- **Building for the Decider, not the participant:** The prototype is not a demo. It's a test instrument. Build for what the participant needs to react honestly, not for what looks impressive in a room.

## Connects to

- [Assumptions Board](../assumptions-board/SKILL.md) — scope is derived entirely from critical assumptions
- [Storyboard](../storyboard/SKILL.md) — panels define the screen list
- [Dividing Roles](../dividing-roles/SKILL.md) — who builds what
- [Five-Act Interview](../five-act-interview/SKILL.md) — prototype is the test instrument
