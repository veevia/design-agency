---
name: assumptions-board
title: Track sprint assumptions on a risk board
description: Re-examine the team's assumptions in light of the winning concept. Map each assumption by importance and certainty. Flag what the prototype must test. Use after Supervote, before starting the prototype storyboard. Use when a decision is 🟡 Yellow and the trigger condition needs to be specified, or when the team is building on beliefs that could invalidate the whole concept if wrong.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Immediately after Supervote, before starting the prototype storyboard
  - When a decision is 🟡 Yellow and the trigger condition needs to be specified
  - Any time the team is building on beliefs that could invalidate the whole concept if wrong
applies-to: risk identification, prototype test prioritisation, 🟡 Yellow trigger conditions, sprint question refinement
done_when:
  - Critical assumptions are posted with importance × certainty
  - Each has a test plan and an owner
  - The board is revisited after sketching to update risk
metadata:
  duration: 20–30 min
  team-size: Full sprint team
  sprint-phase: 4 Decide
---

# Assumptions Board

**TL;DR:** After the Supervote, the winning concept is known but the risks aren't gone — they've just shifted from "which concept?" to "will this concept actually work?" The Assumptions Board revisits the team's critical assumptions in light of the specific winning design, plots them on a risk matrix, and identifies which ones the prototype must test.

## When to use

- Immediately after Supervote, before starting the prototype storyboard
- When a decision is 🟡 Yellow and the trigger condition needs to be specified
- Any time the team is building on beliefs that could invalidate the whole concept if wrong

## The 2×2 matrix (revisited from Phase 1)

```
                    HIGH IMPORTANCE
                           │
         ┌─────────────────┼─────────────────┐
         │  PROTOTYPE MUST │  STRONG BET     │
HIGH     │  TEST THIS      │  Confirm in     │
CERTAINTY│  (highest risk) │  validate       │
 LOW     │                 │                 │
         ├─────────────────┼─────────────────┤
         │  DOCUMENT +     │  MONITOR        │
 HIGH    │  REVISIT        │                 │
CERTAINTY│                 │                 │
         └─────────────────┼─────────────────┘
                           │
                    LOW IMPORTANCE

Y-axis: IMPORTANCE (high = if wrong, concept fails)
X-axis: CERTAINTY (high = backed by data; low = gut feeling)
```

## Steps

1. **List assumptions from Phase 1 (3 min):** Retrieve the Assumption Map from Phase 1. Are these assumptions still relevant given the winning concept?
2. **Add new assumptions (5 min):** The winning concept probably introduced new assumptions not present in Phase 1. Write them — one per sticky note.
3. **Plot on 2×2 (10 min):** For each assumption, collaboratively agree on placement.
4. **Top-left quadrant = prototype test requirements (5 min):** For each high-importance, low-certainty assumption:
   - Write the assumption as a testable hypothesis
   - Identify the specific prototype screen or interaction that will test it
   - Define the success signal ("we'll know this is true when...")
5. **Log as 🟡 Yellow conditions:** Each critical assumption becomes a named trigger for a 🟡 Yellow Traffic Light on the build decision.

## Updated assumptions for a winning concept

After Supervote on "Reasons-First Triage":

```markdown
## Assumptions Board — Reasons-First Triage · [Date]

### Critical (High Importance, Low Certainty) — Prototype must test these

| Assumption | Hypothesis | Prototype test | Success signal |
|---|---|---|---|
| Users will interpret the urgency score correctly | "We believe a numeric urgency score (0–100) is self-explanatory to coordinators without a legend" | Show score without tooltip in T2 task | ≥4/5 users correctly interpret High/Medium/Low without prompting |
| Inline records reduce the need to leave the queue | "We believe showing 3 records (CRM, service contract, inventory) inline eliminates 80% of system-switching" | Observe task completion in T1 | Zero participants open another system while checking a booking |
| The suggested priority is accurate enough to be acted on | "We believe the AI ranking's error rate is below the user's existing manual error rate" | Ask directly in debrief | ≥3/5 say they'd act on the AI-only priority without additional checking |

### Strong bets (High Importance, High Certainty)

- Queue layout is familiar to users with email-inbox or work-order-board experience [observed | team expertise]
- The Lead Coordinator accesses the tool on desktop (not mobile) [observed | 2026-02-17-coordinator-deepdive]

### Low priority (Low Importance)

- Dark/light mode preference
- Table vs. card layout preference
```

## Agent facilitation guide

When generating an Assumptions Board from a winning concept:
1. Read the winning Solution Sketch and all its annotations
2. Extract every claim that requires user behaviour or system capability to be true
3. For each: assign importance (does the concept fail if this is wrong?) and certainty (what's the evidence base?)
4. For critical assumptions: write the testable hypothesis + the minimum valid test
5. Connect each critical assumption to a Sprint Question — if the assumption doesn't connect to a Sprint Question, it may not be worth testing in this sprint

## Relationship to Traffic Light

| Assumption state | Traffic Light mapping |
|---|---|
| All critical assumptions have prototype tests | 🟢 — proceed to build |
| 1–2 critical assumptions cannot be tested in prototype | 🟡 — Yellow until test method found |
| Critical assumption would invalidate the whole concept | 🔴 — reconsider Supervote or scope |

## Watch-outs

- **"We assume everything works":** Over-confidence. Every concept rests on 3–5 critical assumptions. If the board is empty, the team isn't thinking hard enough.
- **Assumptions without tests:** An unresolvable assumption should block the build, not be ignored. If it can't be tested in the sprint, name it as a known risk with a future resolution date.
- **Treating the board as bureaucracy:** This is the most important 20 minutes in Phase 4. The test plan (Phase 6) is built on this board.

## Connects to

- [Assumption Mapping](../assumption-mapping/SKILL.md) — Phase 1 version; this is the Phase 4 update
- [Supervote](../supervote/SKILL.md) — winning concept triggers this board review
- [Five-Act Interview](../five-act-interview/SKILL.md) — interview tasks are designed around critical assumptions
- [`00_README/_frameworks/traffic-light-decisions.md`](../../../00_README/_frameworks/traffic-light-decisions.md) — each critical assumption = 🟡 trigger condition
