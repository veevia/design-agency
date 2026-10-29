---
name: expert-interviews
title: "Run 1:1 expert interviews and capture HMWs live"
description: Gather deep domain knowledge from internal experts in structured 15–20 min sessions. Use to build shared team understanding before problem framing. Use when opening a sprint when team members have uneven domain knowledge, before ideation on a problem that has significant technical or regulatory complexity, or when key stakeholders need to be heard but don't have time for a full workshop.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Opening a sprint when team members have uneven domain knowledge
  - Before ideation on a problem that has significant technical or regulatory complexity
  - When key stakeholders need to be heard but don't have time for a full workshop
applies-to: day-1 sprint opening, stakeholder alignment, domain knowledge gaps, workshop preparation
done_when:
  - Each interview produced HMW notes captured in real time
  - Notes are attributed to the source/expert
  - Output is clustered and handed to How-Might-We synthesis
metadata:
  duration: 15–20 min per expert + 5 min debrief
  team-size: Full sprint team (4–7 people)
  sprint-phase: 1 Understand
---

# Expert Interviews

**TL;DR:** Short, structured talks from internal domain experts — engineers, researchers, sales, support, legal — that give the sprint team shared knowledge they couldn't get from a briefing doc alone. Each expert speaks for 15–20 minutes, takes questions, and the team captures insights as **How Might We** notes in real time.

## When to use

- Opening a sprint when team members have uneven domain knowledge
- Before ideation on a problem that has significant technical or regulatory complexity
- When key stakeholders need to be heard but don't have time for a full workshop

## Materials

- Whiteboard or a shared digital board
- Sticky notes or HMW cards (one colour per expert)
- Timer (visible to all)
- Prepared questions from the sprint team

## Steps

1. **Pre-sprint: Recruit 3–5 experts** (15 min each; spread across disciplines — user-facing, technical, business)
2. **Brief experts in advance:** Send the sprint challenge statement. Ask them to be concrete and bring examples, data, or artefacts.
3. **Open with context (5 min):** Facilitator explains the sprint goal and the team's role as listeners/note-takers.
4. **Expert talk (15 min):** Expert presents their perspective. No debate — only clarifying questions.
5. **Q&A (5 min):** Team asks questions. Facilitator gently enforces time.
6. **HMW capture (parallel):** While listening, every team member silently writes HMW sticky notes — one per note, one idea per note.
7. **Repeat for each expert** with a 5-min buffer between.
8. **Post-interviews:** Feed all HMW notes into the [How Might We](../how-might-we/SKILL.md) method.

## Suggested question starters

- "What's the biggest pain you see users/customers experience?"
- "If you had a magic wand, what would you fix first?"
- "What has been tried before and why did it fail?"
- "What would 'great' look like in 2 years?"
- "What would we regret not knowing before we start building?"

## Agent facilitation guide

When planning expert interviews for a client:
1. Draft the expert list → map each expert to a knowledge gap
2. Write 3 seed questions per expert (specific to their domain)
3. Set the schedule (earliest available slot = first morning of sprint)
4. After interviews, aggregate all HMW notes by theme; feed into HMW voting

When running asynchronously:
- Send a structured async brief (3 questions + 5-min video/doc response format)
- Synthesise responses as HMW notes before the live session

## Output

HMW sticky notes clustered by theme. Feed directly into [How Might We](../how-might-we/SKILL.md) and [User Journey Map](../user-journey-map/SKILL.md).

```
Example output:
HMW make checking a booking feel less like detective work?
HMW get the right request to the right site without manual assignment?
HMW let the coordinator see at a glance which requests only Site C can cover?
```

## Watch-outs

- **Expert goes over time:** Use a visible countdown timer. One person is designated timekeeper.
- **Team debates instead of listens:** Remind the team: "This is upload time, not debate time. Capture disagreement as an HMW note."
- **One expert dominates:** Balance the roster. If one expert has 3x the time, they're now a biased lens.
- **HMW notes stay vague:** Push for specific, actionable HMWs. "HMW improve the experience" is not usable.

## Connects to

- [How Might We](../how-might-we/SKILL.md) — processes the output of this method
- [Assumption Mapping](../assumption-mapping/SKILL.md) — expert talks often surface hidden assumptions
- [Competitive Landscape](../competitive-landscape/SKILL.md) — experts often know existing solutions worth reviewing
