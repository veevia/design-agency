---
name: lightning-demos
title: Mine inspiring solutions for transferable ideas
description: 3-minute demos of inspiring existing solutions — competitors, analogues, adjacent industries — to fuel ideation before sketching begins. Use immediately before Crazy 8s and Solution Sketch. Use when the team feels stuck in a single solution paradigm, or as a structured warm-up replacing open brainstorming (which tends to anchor on the first idea spoken).
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Immediately before Crazy 8s and Solution Sketch
  - When the team feels stuck in a single solution paradigm
  - As a structured warm-up replacing open brainstorming (which tends to anchor on the first idea spoken)
applies-to: ideation warm-up, avoiding reinvention, pattern library building, sketch inspiration
done_when:
  - 3–5 inspiring demos are shown, each in ~3 minutes
  - The transferable “big idea” from each is captured as a sketch/note
  - Captured big ideas feed Crazy 8s / Solution Sketch
metadata:
  duration: 3 min per demo × number of participants + 5 min setup
  team-size: Full sprint team
  sprint-phase: 3 Sketch
---

# Lightning Demos

**TL;DR:** Each team member demos the single most interesting thing they found during research — a competitor feature, an analogous product, a pattern from a different industry. Three minutes per demo. The goal is to load the team's brain with good raw material before individual sketching begins. Ideas from demos often appear directly in solution sketches.

## When to use

- Immediately before Crazy 8s and Solution Sketch
- When the team feels stuck in a single solution paradigm
- As a structured warm-up replacing open brainstorming (which tends to anchor on the first idea spoken)

## Materials

- Devices (one per presenter)
- Shared screen or projector
- Sticky notes for "big idea" capture
- Timer visible to all (3 min hard stop)

## Steps

1. **Assign research (night before or 30 min before the session):** Each person picks one product, competitor, or analogous case. Brief: find the *single most interesting interaction* related to your sprint challenge.
2. **Set up demos (5 min):** Everyone has their demo ready to share on screen.
3. **Demo round (3 min each):**
   - Show the actual product (live or screenshots) — not slides about the product
   - Name the "Big Idea" in one sentence at the start
   - Walk through the specific interaction that's inspiring
   - Explain how it relates to the sprint challenge
4. **Big Idea capture (parallel):** While watching, every team member writes the core concept on a sticky note — in their own words, not copying the product name.
5. **Post all sticky notes on the board** under "Inspiring Patterns"
6. **Quick cluster (5 min):** Group similar ideas. These clusters become source material for sketching.

## What makes a good lightning demo

| Criterion | Good example | Weak example |
|---|---|---|
| Shows an actual interaction | Live screen walkthrough of how a ride-hailing app shows the driver arriving | "The ride-hailing app has good UX" |
| Names the big idea | "The key pattern: nearest available driver × live ETA = one confident promise" | "The app has a map" |
| Connects to sprint challenge | "We could apply this matching to urgent outage requests" | "This is a well-known consumer app" |
| Takes exactly 3 min | Timer enforced, presenter stops mid-sentence if needed | 8-minute overview of the company history |

## Demo source ideas

For triage and assignment products, useful demo areas:

| Domain | Product examples | Big idea to look for |
|---|---|---|
| Ride-hailing | ride-hailing apps, taxi-booking apps | Nearest-driver matching, live tracking |
| Food delivery | food-delivery apps, grocery-delivery apps | Honest ETAs, order-status updates |
| Incident management | on-call paging tools, alerting tools | Escalation logic, post-assignment tracking |
| Smart scheduling | calendar apps, appointment-booking tools | Slot suggestions across many calendars |
| Emergency triage | hospital triage boards, emergency-call consoles | Urgency scoring, clear priority colours |
| Workflow tools | team wikis, issue trackers, project boards | Task assignment, status visibility |

## Output format

```markdown
## Lightning Demos — [Sprint Name] · [Date]

| Presenter | Product / Domain | Big Idea | Sticky note |
|---|---|---|---|
| Facilitator | Incident-management tool | Auto-route incidents by team/severity with escalation fallback | "Assign requests by site + required skill with escalation" |
| [Name] | Ride-hailing app | Live tracking: nearest driver + honest ETA | "Suggest the nearest qualified specialist; show the ETA" |
| [Name] | Food-delivery app | ETA shown up front and updated as the order moves | "Show predicted vs. actual arrival on every request" |
```

## Agent facilitation guide

When preparing lightning demos for a workshop:
1. Assign one demo area per participant based on the sprint's HMW clusters
2. Brief each person with a seed question: "Find the most interesting way [domain] handles [relevant challenge]"
3. After demos, cluster the big ideas and cross-reference with HMW clusters
4. Flag which big ideas map directly to a sprint question — these are the strongest sketch seeds

When running solo (no team):
- Research 5–8 analogous solutions yourself
- Write one "big idea" per product
- Group by pattern type (matching / scoring / filtering / checking / tracking)
- Use the clusters as explicit inspiration anchors when generating Crazy 8s

## Watch-outs

- **"This is what Competitor X does generally":** Not useful. What is the *one specific interaction* worth stealing?
- **Demo goes over time:** Hard-enforce the 3-min limit. Long demos signal the presenter is pitching, not sharing.
- **Team skips the sticky note capture:** The stickies are the output, not the demos themselves. If no one writes down the big ideas, the demos evaporate.
- **Only demoing direct competitors:** The best inspiration usually comes from outside your category.

## Connects to

- [Competitive Landscape](../competitive-landscape/SKILL.md) — same research method, used earlier for understanding
- [Crazy 8s](../crazy-8s/SKILL.md) — big idea stickies directly seed the Crazy 8s warm-up
- [Solution Sketch](../solution-sketch/SKILL.md) — the "inspiring reference" annotation in the sketch often cites a demo
