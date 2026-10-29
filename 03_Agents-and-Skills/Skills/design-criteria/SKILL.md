---
name: design-criteria
title: Define the testable standards a concept must meet
description: Translate Sprint Questions into explicit criteria a winning concept must satisfy — the scorecard used in Speed Critique and Supervote. Use after Sprint Questions and POV Statement are confirmed, before sketching begins, as the explicit frame for Speed Critique ("does this concept meet criterion 3?"), or before Supervote. Use when the team is evaluating multiple concepts and risks defaulting to personal preference.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - After Sprint Questions and POV Statement are confirmed, before sketching begins
  - As the explicit frame for Speed Critique ("does this concept meet criterion 3?")
  - Before Supervote — criteria give the Decider a structured basis for their choice
  - Any time the team is evaluating multiple concepts and risks defaulting to personal preference
applies-to: solution evaluation, concept scoring, design direction, Speed Critique framing, Supervote input
done_when:
  - Criteria are specific and testable, not vague qualities
  - Each criterion is weighted by importance
  - Criteria are ready to drive a decision matrix or critique
metadata:
  duration: 20–30 min
  team-size: Full sprint team; Decider approves
  sprint-phase: 2 Define
  redirect-host: rubric-authoring
---

# Design Criteria

**TL;DR:** Design Criteria are the explicit standards a solution must meet to answer the Sprint Questions and serve the primary user. They translate the sprint's Sprint Questions and POV Statement into concrete, testable "a winning concept will..." statements. Without Design Criteria, Speed Critique and the Supervote are based on taste; with them, the team is evaluating against a shared standard.

## When to use

- After Sprint Questions and POV Statement are confirmed, before sketching begins
- As the explicit frame for Speed Critique ("does this concept meet criterion 3?")
- Before Supervote — criteria give the Decider a structured basis for their choice
- Any time the team is evaluating multiple concepts and risks defaulting to personal preference

## Design Criteria format

Each criterion is a "must" statement paired with a test:

> **A winning concept must:** [specific outcome it delivers]  
> **We'll know it does this when:** [observable signal or test condition]

Example:
> **Must:** Allow the coordinator to check a request's details without leaving the application  
> **Test:** In usability testing, zero participants open another system while reviewing requests

## Types of criteria

| Type | Question it answers | Example |
|---|---|---|
| **User outcome** | Does this help the user accomplish the job? | "Must reduce triage time below 10 min for a 40-request morning" |
| **Behaviour change** | Does it produce the target behaviour change? | "Must result in ≥4/5 users acting on the suggested priority without additional checking" |
| **Constraint compliance** | Does it respect known constraints? | "Must work within the existing booking inbox API — no new data pipeline" |
| **Experience quality** | Does it feel right? | "Must not feel like surveillance or micromanagement to the coordinator" |
| **Business outcome** | Does it serve the organisation's goal? | "Must be rollout-ready to all three sites without custom configuration" |

A sprint typically needs 3–5 criteria. More than 5 starts to over-constrain the design space.

## Steps

1. **Read the Sprint Questions (2 min):** Post the Sprint Questions visibly. Each criterion should trace back to at least one Sprint Question.

2. **Individual drafting (8 min, silent):** Each person writes draft criteria on stickies — "a winning concept must..." — one per sticky.

3. **Post and cluster (5 min):** Post all stickies. Cluster duplicates. Read remaining ones aloud.

4. **Test for specificity (5 min):** For each candidate criterion: can you write a test for it? If not, it's too vague. Rewrite or discard.

5. **Decider selects and ranks (5 min):** Decider selects the 3–5 criteria that matter most. Ranks them (criterion 1 = most important). This ranking guides the Supervote.

6. **Post prominently (1 min):** The Design Criteria stay on the wall for all of Phase 3 and Phase 4.

## Worked example (generic)

```markdown
## Design Criteria — Request Triage Sprint · 2026-02-24

| # | Criterion | Test | Sprint Question |
|---|---|---|---|
| 1 | Must allow the coordinator to check a request's details without opening another system | In usability test: zero participants open another system during the request review task | SQ1: Can we reduce triage time? |
| 2 | Must present the suggested priority in a way coordinators trust enough to act on without manual checks | ≥3/5 participants prioritise a request based on the AI suggestion alone | SQ2: Can we build trust in the suggested priority? |
| 3 | Must reduce request assignment to ≤2 user interactions | Assignment task completed in ≤2 taps/clicks by ≥4/5 participants | SQ3: Can we simplify assignment? |
| 4 | Must work within the existing booking inbox API and specialist calendar — no new integration | Engineering sign-off: implementation possible within current API contracts | Constraint |
| 5 | Must not increase cognitive load for coordinators on peak-volume mornings | No participant reports feeling "more overwhelmed" in debrief | SQ1 + experience quality |

**Priority ranking (Decider):** 1 > 2 > 3 > 4 > 5
```

## Design Criteria vs. Sprint Questions

| | Sprint Questions | Design Criteria |
|---|---|---|
| **Form** | Question: "Can we...?" | Standard: "A winning concept must..." |
| **Answered by** | Validate phase results | Speed Critique + Supervote assessment |
| **Used for** | Framing the problem | Evaluating solutions |
| **Written** | Phase 2 Define | Phase 2 Define (after Sprint Questions) |

## Agent facilitation guide

When generating Design Criteria:
1. Read the Sprint Questions and POV Statement
2. For each Sprint Question: write one criterion that a solution must satisfy to answer it
3. Add any constraint-compliance criteria (from Constraint Mapping)
4. Write a test for each criterion — if you can't write a test, rewrite the criterion
5. Rank by importance (Decider's order of priority)
6. Flag any criterion that cannot be tested in a single prototype session — note as "validate post-sprint"

## Watch-outs

- **Criteria that are solutions:** "Must have an urgency score widget" is a feature, not a criterion. Reframe: "Must present the suggested priority in a way users can interpret without explanation."
- **Untestable criteria:** "Must feel intuitive" can't be tested. "Must be completed by ≥4/5 participants without guidance" can be.
- **Too many criteria:** 8+ criteria will paralyse Speed Critique. Limit to 5 maximum; 3 is better.
- **Not referencing criteria in Speed Critique:** Design Criteria only add value if the Facilitator explicitly invokes them: "Does this sketch satisfy criterion 2?"

## Connects to

- [POV Statement](../pov-statement/SKILL.md) — user outcome criteria derive from the POV need
- [Sprint Questions](../sprint-questions/SKILL.md) — each Sprint Question maps to at least one criterion
- [Constraint Mapping](../constraint-mapping/SKILL.md) — constraint-compliance criteria come from here
- [Speed Critique](../speed-critique/SKILL.md) — criteria are the evaluation frame during critique
- [Supervote](../supervote/SKILL.md) — Decider references criteria when explaining their vote
