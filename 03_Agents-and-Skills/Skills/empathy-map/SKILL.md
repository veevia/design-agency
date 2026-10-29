---
name: empathy-map
title: Capture what a user says, thinks, does, and feels
description: Map what a specific user says, thinks, does, and feels — surface the emotional and cognitive landscape beneath their surface behaviour. Use after Lightning Talks and Expert Interviews, to synthesise insights about a specific user. Use when the team has a named persona (e.g., the Lead Coordinator) but lacks shared understanding of their emotional experience, or before User Journey Mapping.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - After Lightning Talks and Expert Interviews, to synthesise insights about a specific user
  - When the team has a named persona (e.g., the Lead Coordinator) but lacks shared understanding of their emotional experience
  - Before User Journey Mapping — or immediately after — to add the internal layer
  - When assumptions about user behaviour need to be surfaced and stress-tested
  - When the team includes people who have never spoken directly to the user
applies-to: user empathy, persona deepening, assumption surfacing, HMW generation, pain point mapping
done_when:
  - All four quadrants (says / thinks / does / feels) carry evidence-grounded entries
  - Pains and gains are explicit and distinguished
  - At least one pain converts into an HMW or assumption
metadata:
  duration: 20–30 min
  team-size: Full sprint team; one map per key persona
  sprint-phase: 1 Understand
---

# Empathy Map

**TL;DR:** An Empathy Map is a collaborative tool for building a shared picture of a specific user's inner world. Where a User Journey Map traces what someone does step by step, an Empathy Map captures what they think, feel, say, and do simultaneously — revealing the emotional and cognitive texture that journey maps often flatten. The result is a richer user mental model that directly improves the quality of HMW questions and Sprint Questions.

## When to use

- After Lightning Talks and Expert Interviews, to synthesise insights about a specific user
- When the team has a named persona (e.g., the Lead Coordinator) but lacks shared understanding of their emotional experience
- Before User Journey Mapping — or immediately after — to add the internal layer
- When assumptions about user behaviour need to be surfaced and stress-tested
- When the team includes people who have never spoken directly to the user

## The four quadrants

The Empathy Map uses four quadrants around a central representation of the user:

```
              SAYS                    THINKS
        ┌──────────────────┬──────────────────┐
        │ Quotes and words │ Beliefs and       │
        │ the user says    │ internal thoughts │
        │ aloud            │ (often unspoken)  │
        ├──────────────────┼──────────────────┤
        │ Observable       │ Emotional state;  │
        │ actions and      │ reactions;        │
        │ behaviours       │ feelings          │
        └──────────────────┴──────────────────┘
              DOES                    FEELS
```

**Says:** Direct quotes from research. What words does this user actually use?  
**Thinks:** What are they processing internally that they may not say out loud? What beliefs and assumptions do they hold?  
**Does:** Observable behaviours — what do they literally do in this context?  
**Feels:** Their emotional state — not what they say they feel, but what the team believes they feel based on the evidence.

## Two additional zones (extended version)

Below the quadrant, add:
- **Pains:** What's frustrating them? What obstacles are in their way? What risks do they worry about?
- **Gains:** What does success look like to them? What would a great outcome feel like?

The Pains/Gains layer connects the empathy map directly to JTBD (Jobs to be Done) and HMW note generation.

## Steps

1. **Name the user (1 min):** This map is for a specific person, not a generic user type. Write their name, role, and the specific context: "[Name] (Lead Coordinator), during morning request triage."

2. **Generate raw notes per quadrant (8–10 min, silent):** Each team member writes observations on sticky notes and places them in the relevant quadrant. One observation per sticky. Based on research heard in Lightning Talks and Expert Interviews.

3. **Read the quadrants (5 min):** Team walks the map. Facilitator reads clusters aloud. No debate yet.

4. **Identify contradictions (3 min):** Where does the "says" column contradict the "does" column? Where does "thinks" contradict "feels"? These contradictions are the most valuable insight — they reveal where user behaviour is driven by something other than explicit preference.

5. **Generate HMW notes (5–10 min):** Looking at Pains in particular: write one HMW note for each significant pain. These add to the affinity map pile.

6. **Identify key assumptions (3 min):** Review the "thinks" and "feels" columns. How many of these are observations vs. assumptions? Mark assumptions with a question mark. They go into Assumption Mapping.

## Example — Lead Coordinator, morning triage context

```markdown
## Empathy Map — Lead Coordinator · Morning triage

**SAYS**
- "I spend the first 40 minutes just sorting what came in overnight"
- "I don't trust a priority if I can't see why it was given"
- "The assignment screen is unreliable — I phone the site to be safe"
- "If an outage call waits, it reflects on my team"

**THINKS**
- "There are too many requests and not enough time to check them all"
- "The system will miss context that only an experienced coordinator would catch"
- "My manager will only hear about the misses, not the catches"

**DOES**
- Opens 3–4 other systems (CRM, service-contract database, inventory system) to check each unclear request
- Uses a personal tracking spreadsheet in parallel with the booking inbox
- Phones site supervisors about ambiguous requests rather than using the assignment screen
- Skips the 'Routine' queue on busy mornings

**FEELS**
- Anxious about gaps — "what if I missed an urgent one?"
- Frustrated by tool switching and repetitive clicking
- Exposed when a request is given the wrong priority
- Quiet pride when a routine-looking request they flagged turns out to be urgent

**PAINS**
- 40+ minutes every morning on manual triage with no time savings in sight
- Can't see a request's history in one place — must check each system every time
- Assignment-screen unreliability creates rework
- No visibility into whether another coordinator has already picked up a request

**GAINS**
- Confidence that the urgent requests are assigned before the 8am start
- Ability to assign a request quickly without second-guessing the details
- Professional credibility: being known for catching what others miss
```

## Agent facilitation guide

When generating an Empathy Map from research notes:
1. Identify the specific user and context (name, role, scenario)
2. Extract every quote from research — sort into SAYS
3. Infer internal states from observable behaviour — populate THINKS and FEELS
4. List specific observable actions — populate DOES
5. Derive Pains from friction points and Gains from success criteria
6. Flag THINKS and FEELS entries that are assumptions (not directly observed) — mark as `[assumed]`
7. Generate 2–3 HMW notes directly from the top Pains

Output format: the four-quadrant table + HMW generation from pains.

## Watch-outs

- **Treating "feels" as "says":** Users often describe their feelings inaccurately in interviews. "I feel fine about it" while showing hesitation behaviour is a FEELS contradiction. Trust behaviour over stated feeling.
- **Generic empathy maps:** A map that could apply to any coordinator isn't useful. Specific quotes, specific behaviour, specific fears are what make this actionable.
- **One map for multiple users:** Make one map per distinct user. If the Lead Coordinator and a junior coordinator would have completely different THINKS columns, they're different users.
- **Skipping the contradiction step:** The contradiction between SAYS and DOES is usually the most important finding. An empathy map that has no contradictions usually means the team filled it in too optimistically.
- **Assumptions untaged:** The THINKS and FEELS columns are partially invented. If the team hasn't done direct research, tag entries as `[assumed]` so they feed into Assumption Mapping rather than being treated as fact.

## Connects to

- [Lightning Talks](../lightning-talks/SKILL.md) — primary source material for empathy map entries
- [Expert Interviews](../expert-interviews/SKILL.md) — direct quotes for the SAYS column
- [User Journey Map](../user-journey-map/SKILL.md) — journey map provides the step-by-step context; empathy map provides the emotional layer
- [How Might We](../how-might-we/SKILL.md) — Pains generate HMW notes directly
- [Assumption Mapping](../assumption-mapping/SKILL.md) — tagged `[assumed]` entries become assumptions on the map
