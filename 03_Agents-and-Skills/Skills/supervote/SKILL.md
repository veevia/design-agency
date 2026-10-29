---
name: supervote
title: Have the Decider cast the binding final vote
description: The Decider makes the binding final decision on which concept to prototype. Three special votes, full authority. The sprint moves forward on their choice. Use after Straw Poll. Use when the team has reached an impasse and needs a decision to unblock progress, or as the formal close of the decision-making phase.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Immediately after Straw Poll
  - Whenever the team has reached an impasse and needs a decision to unblock progress
  - As the formal close of the decision-making phase
applies-to: final concept selection, sprint direction, resolving disagreement, decision authority
done_when:
  - The Decider casts the binding vote after the straw poll
  - The rationale is recorded (one sentence minimum)
  - The winning concept is locked for prototyping
metadata:
  duration: 5 min
  team-size: Decider only (team observes)
  sprint-phase: 4 Decide
---

# Supervote

**TL;DR:** After the team's Straw Poll, the Decider places three large sticker dots — their three "supervotes" — on any elements or concepts they choose. Where those dots land is what gets built. The Decider's votes are binding. No debate, no override. The method encodes a clear authority structure: everyone contributes to the decision with their input, but one person makes the final call and owns it.

## When to use

- Immediately after Straw Poll
- Whenever the team has reached an impasse and needs a decision to unblock progress
- As the formal close of the decision-making phase

## Materials

- 3 large sticker dots (distinct size/colour from all previous voting dots)
- All sketches still posted

## The rules

- **Decider places 3 dots.** They can spread them or stack them on one concept.
- **Dots can go on a concept (whole sketch) or on specific elements.** "I want Concept A, but include the urgency score from Concept C."
- **No debate after the Supervote.** The team asks clarifying questions only ("Does this mean we'll include the one-tap assign feature?"). No lobbying, no second-guessing.
- **The Decider explains their reasoning once.** Brief rationale — enough for the team to understand and carry the decision forward.

## Steps

1. **Decider takes their dots (1 min):** Everyone else steps back. The Decider walks the wall alone.
2. **Silent review (2 min):** Decider reviews all sketches with fresh eyes.
3. **Place dots (1 min):** Decider places all 3 dots. May place on one concept or combine.
4. **Rationale (1 min):** "I chose X because Y. I included [element from Z] because it addresses Sprint Question 2 most directly."
5. **Team clarifying questions (2 min):** No debate — only "so does this mean we will/won't include X?"
6. **Record the decision:** Facilitator writes the decision as a one-sentence statement. This becomes the prototype brief.

## Decision patterns

| Vote placement | Meaning |
|---|---|
| All 3 on one sketch | Clear single winner — build exactly this |
| 2 on Sketch A, 1 on element of Sketch B | "Build A, but incorporate this element from B" |
| Split across concepts | Two strong concepts — may warrant two prototype paths if time allows |
| Dots on non-winning sketch element | "The rest of the team didn't see this, but I want it in" |

## The Decider role

The Decider is typically the most senior business stakeholder — the person who is accountable for the outcome and has the context to understand strategic trade-offs. In the sprint context, the Decider's job is:

1. **Listen to all input** (Expert Interviews, Heat Map, Speed Critique, Straw Poll)
2. **Make the call** — even with incomplete information
3. **Own the decision** — if it turns out wrong in Validate, they update their view

The Decider is not "the person who agrees with the design team." They may override a unanimous Straw Poll with good reason.

## Relationship to Traffic Light

Supervote output maps to a Traffic Light:

| Supervote outcome | Traffic Light | Notes |
|---|---|---|
| Clear single concept, team aligned | 🟢 Green — build it | Prototype brief is clear |
| Single concept but open assumptions | 🟡 Yellow — build it, name the assumption | Validate session must test the assumption |
| No consensus; two competing concepts | 🟡 Yellow — test both if time allows | Name the decision trigger (which result would confirm which direction) |
| Team blocked; Decider overrides | 🟢 Green after Supervote | Decider rationale logged as ADR |

## Agent facilitation guide

When acting as a decision-support agent for a Decider:
1. Summarise the full decision context: Long-Term Goal, Sprint Questions, Straw Poll result, minority arguments
2. Produce a decision brief:
   ```
   Recommended: [Concept name]
   Reason: [how it answers Sprint Questions 1–3 most directly]
   Risk: [the one assumption that would make this wrong]
   Alternative worth watching: [concept] — strongest if [condition]
   ```
3. After the Supervote: record the decision as an ADR with Traffic Light
4. Extract any element inclusions/exclusions as explicit scope notes for the prototype

## Watch-outs

- **Decider defers to the group:** "Whatever the team thinks" is not a Supervote. The team has already expressed their preference. The Decider was brought in to make the call.
- **Team debates after the vote:** Supervote closes the decision. Reopen only if new critical information emerges.
- **No rationale given:** The Decider must state their reasoning once. A silent Supervote leaves the team unable to carry the decision forward coherently.
- **Confusing Decider authority with infallibility:** The Decider's job is to decide, not to be right. The Validate phase will tell them if they were.

## Connects to

- [Straw Poll](../straw-poll/SKILL.md) — input that precedes Supervote
- [Assumptions Board](../assumptions-board/SKILL.md) — post-Supervote, re-check assumptions given the winning concept
- [Storyboard](../storyboard/SKILL.md) — winning concept becomes the storyboard input
- [`00_README/_frameworks/traffic-light-decisions.md`](../../../00_README/_frameworks/traffic-light-decisions.md) — Supervote output maps to a Traffic Light ADR
