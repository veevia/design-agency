---
name: competitive-landscape
title: Audit analogous and competitor solutions fast
description: Survey existing solutions — competitors, analogous industries, adjacent products — to find what's already working that can be adapted, combined, or inverted. Use before sketching to ensure no one reinvents obvious wheels. Use when the team is stuck in a single solution paradigm, or to identify the "gold standard" to match or beat.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Before sketching to ensure no one reinvents obvious wheels
  - When the team is stuck in a single solution paradigm
  - To identify the "gold standard" to match or beat
  - When users reference competitors ("we want something like X but for Y")
applies-to: ideation preparation, avoiding reinvention, identifying patterns worth stealing
done_when:
  - The relevant analogous/competitor solutions are listed with what each does well/badly
  - Each entry notes a takeaway or gap worth designing into
  - Findings feed at least one HMW or sprint question
metadata:
  duration: 60–90 min research + 30 min demos (3 min each)
  team-size: Split team for research; full team for demos
  sprint-phase: 1 Understand
---

# Competitive Landscape

**TL;DR:** A structured scan of existing solutions to the problem — not to copy, but to identify proven patterns, missed opportunities, and meaningful differentiators. Each team member researches one competitor or analogous domain, then gives a 3-minute demo to the group.

## When to use

- Before sketching to ensure no one reinvents obvious wheels
- When the team is stuck in a single solution paradigm
- To identify the "gold standard" to match or beat
- When users reference competitors ("we want something like X but for Y")

## Materials

- Device per researcher
- Shared board or slide deck for demo capture
- Timer (3 min per demo)

## Steps

1. **Assign research areas (10 min):** Each team member takes one competitor, adjacent product, or analogous industry. Rotate — don't all research the same thing.
2. **Research phase (45–60 min):** Each person explores their area looking for:
   - What user problem it solves
   - What's notably good (a "big idea" worth demoing)
   - What's missing or flawed
3. **Lightning Demos (3 min each):** Each person demos the *single most interesting thing* they found:
   - Show the actual interface/product if possible
   - Name the "big idea" in one sentence
   - Explain how it relates to your sprint challenge
4. **Capture big ideas:** While each person demos, team members write down inspiring ideas — one idea per sticky note.
5. **Cluster and vote:** Group the big ideas. Vote on the ones most relevant to your HMW questions.

## Research framing questions

For each competitor/analogue:
- What's the core interaction design pattern?
- What does this product make easy that's currently hard?
- What would users say is the best thing about this?
- What's the thing that would make a user switch away?

## Analogous domains

Great insight often comes from outside your industry. For request-triage and service-coordination products, look at:

| Domain | Why it's analogous |
|---|---|
| Ride-hailing apps (live tracking) | Same "request → match → assign → track" loop |
| Emergency-department triage | Urgency scoring + fast prioritisation under pressure |
| Food-delivery ETA screens | Predicted vs. actual arrival, updated in real time |
| Incident management (on-call paging) | On-call routing + escalation flows |
| Calendar apps (smart scheduling) | Matching a request to the best available person and slot |
| Parcel logistics (route planning) | Loading the right items onto the right vehicle for the day's route |

## Output format

```markdown
## Competitive Landscape — [Sprint Name]

| Product / Domain | Big Idea | Relevant because | Sticky note captured |
|---|---|---|---|
| Ride-hailing app | Nearest-driver matching + live tracking across thousands of trips | The Lead Coordinator matches 38 overnight requests to ~60 specialists — same matching challenge | "HMW suggest the nearest qualified specialist per request?" |
| On-call paging tool | Incident routing by team/owner with escalation logic | Post-assignment visibility problem | "HMW auto-assign urgent requests to the right site?" |
| Email client (smart filters) | 'Mute' patterns that aren't relevant | Reduce noise without losing urgent requests | "HMW let coordinators define what's routine?" |
```

## Agent facilitation guide

When preparing a competitive landscape for a client:
1. Identify 5–8 relevant competitors/analogues (mix: direct competitors + analogous industries)
2. For each: write a 3-sentence summary of the big idea and how it relates to the sprint challenge
3. Extract 2–3 sticky-note-worthy ideas per product
4. Flag which ideas map directly to top HMW clusters
5. Note intellectual property or pattern library considerations (what to adapt vs. avoid)

## Watch-outs

- **Benchmark paralysis:** Research is capped at 60 min. Deeper analysis happens later if needed.
- **Too many competitors:** 5–8 is the limit. More creates noise, not insight.
- **"We need to be better than X":** This is strategy, not sprint input. The sprint question is: what specific interaction pattern can we learn from X?
- **Ignoring analogous domains:** Direct competitors have the same blind spots you do. The best ideas usually come from adjacent industries.

## Connects to

- [Expert Interviews](../expert-interviews/SKILL.md) — experts often know which competitors are worth studying
- [Lightning Demos](../lightning-demos/SKILL.md) — can be repeated in Sketch phase with new discoveries
- [How Might We](../how-might-we/SKILL.md) — each big idea should become an HMW candidate
