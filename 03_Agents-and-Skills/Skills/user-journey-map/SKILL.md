---
name: user-journey-map
title: Map the current end-to-end user experience
description: Map the current user experience from trigger to goal — including emotions, pain points, and key moments. The empathy anchor for the whole sprint. Use on Day 1 of the sprint to build shared team empathy, before writing personas or JTBDs to ground them in real behaviour. Use when the team disagrees about where the problem actually is.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Day 1 of the sprint to build shared team empathy
  - Before writing personas or JTBDs to ground them in real behaviour
  - When the team disagrees about where the problem actually is
  - When deciding which moment in the journey to target for the sprint
applies-to: problem framing, empathy building, HMW placement, sprint target selection
done_when:
  - The journey covers entry to exit with stages and steps
  - Pain points and emotional highs/lows are marked per stage
  - HMWs attach to specific journey moments
metadata:
  duration: 30–60 min (collaborative) or 60–90 min (detailed)
  team-size: 2–7 people; facilitator + domain expert recommended
  sprint-phase: 1 Understand
  redirect-host: canonical-artifacts
---

# User Journey Map

**TL;DR:** A visual narrative of a specific user's experience through a process — from the moment a need arises to the moment it's resolved (or abandoned). Captures what users do, think, and feel at each stage. The emotional arc reveals where pain concentrates and where opportunity exists.

## When to use

- Day 1 of the sprint to build shared team empathy
- Before writing personas or JTBDs to ground them in real behaviour
- When the team disagrees about where the problem actually is
- When deciding which moment in the journey to target for the sprint

## Materials

- Whiteboard or digital board
- Sticky notes: 3 colours (actions, thoughts/feelings, opportunities)
- A defined persona + scenario to map

## Map structure

```
Actor:   [Persona name + role]
Scenario: [Specific trigger → goal they're trying to achieve]

Stage 1     Stage 2     Stage 3     Stage 4     Stage 5
[name]      [name]      [name]      [name]      [name]

DOING
[action]    [action]    [action]    [action]    [action]

THINKING / FEELING
[thought]   [emotion]   [thought]   [emotion]   [thought]

PAIN POINTS
[pain]                  [pain]                  [pain]

OPPORTUNITIES (HMW)
[HMW]                              [HMW]
```

## Steps

1. **Set the scope (5 min):** Agree on the actor (one persona) and scenario (one specific trigger-to-goal).
2. **Name the stages (10 min):** Collaboratively name 4–7 stages of the journey. Stages should be active (verbs: "Spot", "Check", "Assign", not "Sorting Phase").
3. **Fill in DOING row (15 min):** What specific actions does the user take at each stage? Concrete, observable.
4. **Fill in THINKING/FEELING row (15 min):** What's in their head? What's the emotional tone? Use direct quotes from research where possible.
5. **Mark pain points (10 min):** Where does the journey break down, slow down, or cause frustration? Mark these prominently — they become HMW candidates.
6. **Add opportunities (HMW notes) (10 min):** At the most painful moments, attach HMW notes. These are your primary design targets.
7. **Mark the emotional arc:** Draw a rough emotional curve across stages (high = positive; low = frustrated/stuck).
8. **Identify moment of truth:** Where does the user's confidence in the system peak or bottom out? Mark it.

## Output format

```markdown
## Journey Map — [Persona] · [Scenario]

**Actor:** Lead Coordinator (client organization with three regional sites)
**Scenario:** An urgent outage request arrives overnight for Site C; the coordinator must spot it, check it, and assign it to the right specialist within 2 hours.

| Stage | 1. Spot | 2. Check | 3. Assess | 4. Assign | 5. Track |
|---|---|---|---|---|---|
| **Doing** | Scans the booking inbox + phone-line voicemails manually | Cross-references the CRM, service-contract database, and inventory system + asks a senior specialist by chat | Judges urgency against the other requests in the queue | Phones Site C + adds to a spreadsheet tracker | Follows up manually; no visibility until the specialist calls back |
| **Thinking** | "Something here might be urgent but I'm not sure" | "I need a second opinion but the senior specialist is busy" | "Is this a Site C request, or can Site B cover it sooner?" | "I hope the Site C supervisor got my message" | "I don't know if anyone is on the way" |
| **Feeling** | Anxious · Overwhelmed | Uncertain · Time-pressured | Cautious | Responsible but powerless | Frustrated · Resigned |
| **Pain** | No unified view; relies on manual scanning | No structured way to check a booking | No cross-site comparison | No tracking; relies on personal follow-up | Zero visibility post-handoff |
| **HMW** | HMW surface the urgent requests without hunting? | HMW make checking a booking faster + more trustworthy? | | HMW give the coordinator visibility after they assign? | |

**Emotional arc:** Starts neutral → spikes anxious at Spot → peaks frustration at Assign/Track
**Moment of truth:** Checking (Stage 2) — this is where confidence is won or lost
```

## Agent facilitation guide

When building a journey map from research/interview notes:
1. Identify the primary persona and the scenario most relevant to the sprint challenge
2. Extract all "doing" observations (tagged `observed` or `reported`) and assign to stages
3. Extract emotional signals (direct quotes, body language notes) and assign to stages
4. Generate HMW notes at the 2–3 highest-pain moments
5. Identify the moment of truth — the inflection point where the user decides to trust or abandon
6. Flag the stage that the sprint target should focus on

## Watch-outs

- **Mapping too many personas:** One map per persona per scenario. Two personas = two maps (or a comparative view).
- **Skipping the emotional row:** Pain is felt, not just described. The emotional arc is what generates empathy — without it, the map is a flowchart.
- **Vague stage names:** "Planning" → "Choose which requests to assign first". Active, specific.
- **HMWs disconnected from pain:** Every HMW should attach to a specific painful moment on the map.
- **No moment of truth:** Every map should name one moment. If you can't, the map is too abstract.

## Connects to

- [How Might We](../how-might-we/SKILL.md) — HMW notes attach to map pain points
- [Map](../sprint-map/SKILL.md) — simplified journey used as sprint target surface
- [Target](../sprint-target/SKILL.md) — moment of truth becomes the sprint target moment
- [`00_README/_templates/1-4-Understand_journey-map.template.md`](../../../00_README/_templates/1-4-Understand_journey-map.template.md) — workspace template
