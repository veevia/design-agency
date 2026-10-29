---
name: sprint-map-update
title: Update the sprint map with what testing showed
description: Update the sprint's primary artifacts — Sprint Map, Assumptions Board, and Long-Term Goal — with validated knowledge from Validate day, closing the sprint loop with evidence-grounded decisions. Use when at the end of every sprint, after Synthesis is complete and the forward decision is made, before the team disperses at the end of Day 6, or after a mid-sprint pivot that changes the map significantly enough to invalidate the original structure.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - At the end of every sprint, after Synthesis is complete and the forward decision is made
  - Before the team disperses at the end of Day 6
  - After a mid-sprint pivot that changes the map significantly enough to invalidate the original structure
  - As the handoff artifact when sprint learnings are being shared with a build team or stakeholder group that wasn't in the sprint room
applies-to: sprint closure, knowledge integration, assumptions board update, sprint map update, forward ADR, momentum handoff to next sprint or build phase
done_when:
  - The map reflects validated vs invalidated assumptions
  - Changed journey moments are revised on the map
  - The forward decision is captured against the updated map
metadata:
  duration: 30–45 min (follows Synthesis; final act of Validate day)
  team-size: Facilitator + Decider; full team present for review
  sprint-phase: 6 Validate
---

# Sprint Map Update

**TL;DR:** The Sprint Map Update is the final act of the sprint. After Synthesis produces the forward decision (iterate / ship / pivot / stop), the team takes 30 minutes to update the sprint's primary artifacts to reflect what is now known, what is now assumed, and what the next action is. These updates are the mechanism by which the sprint's validated knowledge transfers into the project hub — so the next team member, next sprint, or build team begins with the current state of truth, not the assumptions the team held on Day 1.

## When to use

- At the end of every sprint, after Synthesis is complete and the forward decision is made
- Before the team disperses at the end of Day 6
- After a mid-sprint pivot that changes the map significantly enough to invalidate the original structure
- As the handoff artifact when sprint learnings are being shared with a build team or stakeholder group that wasn't in the sprint room

## What gets updated

### 1. The Sprint Map (Customer Journey Map)

The map drawn on Day 2 reflects the team's Day 1 understanding of the user's journey. Validate day produced observed evidence. Update the map to reflect:

- **What the prototype tested:** Mark the step(s) that the prototype covered
- **What was validated:** Add a ✓ symbol + brief note at each map step that produced confirming data
- **What was challenged:** Add a ✗ symbol + brief note at each map step where data challenged the assumption
- **What remains unknown:** Add a ? symbol at each step not covered by the prototype

The updated map is now the team's evidence-grounded view of the journey — not a hypothesis.

### 2. The Assumptions Board

Every critical assumption on the Assumptions Board gets a final status:

| Status | Symbol | Criteria |
|---|---|---|
| **Validated** | 🟢 | ≥ 4 of 5 participants confirmed; no strong contradicting evidence |
| **Partially validated** | 🟡 | Mixed results; ≥ 3 of 5 confirmed but with caveats; requires follow-up |
| **Challenged** | 🔴 | ≥ 3 of 5 participants challenged or failed to confirm |
| **Untested** | ⚪ | Prototype did not reach this assumption; status unchanged |

The updated Assumptions Board is the primary input to the next sprint's Day 1.

### 3. The Long-Term Goal

The Long-Term Goal defined on Day 2 ("In two years, the coordinator checks and assigns a request in 45 seconds with confidence") may need revision based on what was learned:

- If the sprint **confirms** the goal is correct: add a timestamp and validation note ("Confirmed directionally valid as of [date] — [N] participants responded positively to the core experience")
- If the sprint **reveals the goal needs updating**: revise the goal with a note explaining what the data surfaced ("Revised: 45-second target may be aggressive for complex requests — P2, P3 took 65–82 sec on the Unit U-200 scenario; revisit benchmark")

### 4. The ADR (Decision Record)

The forward decision from Synthesis — iterate / ship / pivot / stop — gets filed as an ADR using the Traffic Light format.

```markdown
## Sprint Forward Decision ADR — [Sprint Name] · [Date]

**Decision:** Iterate — refine urgency score explanation before next validation round

**Light:** 🟡 Yellow
**Rationale:** Core assignment workflow validated (4/5 task completion; mean 74 sec — acceptable). Urgency score interpretation failed (20% unaided completion; all 5 participants asked "what does this mean?"). The assumption about AI explanation legibility is not yet valid.

**Trigger to 🟢 Green:** Next prototype version achieves ≥ 80% unaided completion on Task 2 (urgency score interpretation) across 5 new participants.
**Expiry:** 2 weeks from today — revisit if the next prototype is not ready by then.

**Next action:** Redesign urgency score explanation component (owner: [name]). Retest with 3 new participants before proceeding to Build.
```

## Sprint Map Update output

```markdown
## Sprint Map Update — [Sprint Name] · [Date] · Post-Validate

### Updated Sprint Map notes

Step 3 — Request Review:
  Prototype covered this step. ✓ Validated: queue filtering works (4/5 found the urgent request).
  ✗ Challenged: "unconfirmed" filter label not intuitive — 2 participants tapped wrong filter first.

Step 4 — Booking Check:
  Prototype covered this step. ✗ CHALLENGED: urgency score explanation fails (1/5 unaided).
  ✓ Validated: inline CRM, service-contract, and inventory records replaced system-switching (3/5 explicit confirmation).

Step 5 — Assignment:
  Prototype covered this step. ✓ Validated: assign CTA visible (4/5 completion).
  ✗ Challenged: assignment entry point (list vs. detail) unclear — 2 participants started from wrong location.

Steps 1–2 (Request Intake) and Steps 6–7 (Post-Assignment Tracking): NOT TESTED — prototype did not cover.

### Assumptions Board final status
A1 (urgency score reduces checking time): 🔴 Challenged — time did not improve
A2 (inline records replace system-switching): 🟢 Validated
A3 (assign CTA visible and intuitive): 🟡 Partial — visible but entry point ambiguous
A4 (one-tap assign replaces 7-field form): 🟢 Validated
A5 (urgency score legibility): 🔴 Challenged — requires redesign

### Long-Term Goal status
Revised: 45-second target is achievable for assignment (Task 3 mean 74 sec trending toward target with assignment refinement). Not achievable with current urgency score design. Revise milestone: "first confirm that explanation legibility is solved; then re-measure total time."

### Forward decision: 🟡 Iterate
Owner: [Name]
Next sprint date: [Date]
Focus: Urgency score explanation component redesign + 3-participant retest
```

## Watch-outs

- **Skipping the update "because we know what to do next":** The team knows what to do now — but the build team, the next sprint team, and the stakeholder reviewer don't. The map update is not for the people in the room; it's for everyone who comes after.
- **Updating with opinions instead of evidence:** Every mark on the updated map and Assumptions Board must cite at least one participant observation. "We think the assignment flow is fine" is not a validated assumption. "4 of 5 completed Task 3 without help" is.
- **Filing a 🟡 Yellow ADR without trigger + expiry:** Per the Traffic Light discipline, a Yellow without a specific trigger condition and an expiry date is invalid. Name the measurable condition that would make this Green, and the date by which you'll re-evaluate.
- **Updating the map before Synthesis is complete:** The map update should reflect the team's agreed interpretation of the data — not one person's reaction. Run Synthesis first; update after the forward decision is made.

## Agent facilitation guide

When producing the Sprint Map Update:
1. Receive the Synthesis output: validated assumptions, challenged assumptions, forward decision
2. Map each assumption to the relevant sprint map step — update with ✓ / ✗ / ? symbols and one-sentence evidence notes
3. Update each Assumptions Board item with its final status (🟢/🟡/🔴/⚪) and the evidence that determines it
4. Revise the Long-Term Goal if the sprint produced evidence that the benchmark or direction needs updating
5. Draft the forward decision ADR: state the light, the rationale, the trigger (for Yellow), and the next action with an owner and date
6. Output: the four updated artifacts in the format above

## Connects to

- [Synthesis](../research-synthesis/SKILL.md) — the forward decision from Synthesis drives the map update
- [Map](../sprint-map/SKILL.md) — the original sprint map is the artifact being updated
- [Long-Term Goal](../long-term-goal/SKILL.md) — Long-Term Goal may be revised based on validated evidence
- [Assumptions Board](../assumptions-board/SKILL.md) — the Assumptions Board is closed with final statuses
- [Assumption Mapping](../assumption-mapping/SKILL.md) — the updated Assumptions Board feeds the next sprint's Day 1 assumption mapping
