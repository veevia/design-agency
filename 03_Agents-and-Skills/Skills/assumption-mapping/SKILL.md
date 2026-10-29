---
name: assumption-mapping
title: Surface and rank the team's riskiest beliefs
description: Externalise every belief the team is treating as fact and plot it on an importance × certainty 2×2, so the high-importance / low-certainty assumptions become the things you test first. Use to convert a stuck 🟡 Yellow decision into a testable hypothesis, to pre-mortem a direction before committing, or whenever the team keeps arguing about things that "might be true." Use when the team keeps arguing about things that "might be true", or when a Traffic Light decision is 🟡 Yellow because of an unresolved assumption (this gives the trigger + expiry).
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - The team keeps arguing about things that "might be true" — surface and rank them
  - A Traffic Light decision is 🟡 Yellow because of an unresolved assumption (this gives the trigger + expiry)
  - Before committing to a prototype/direction, to validate the riskiest bets first
  - A stakeholder says "but we don't really know if users want this"
applies-to: risk identification, Yellow decision resolution, sprint question generation, prototype prioritisation
done_when:
  - Every assumption is plotted on importance × certainty
  - The top-left (high-importance, low-certainty) assumptions are named as testable hypotheses
  - Each critical assumption has a test method and a success signal
metadata:
  duration: 30–45 min
  team-size: solo, or full team + Decider
  sprint-phase: 1 Understand
---

# Assumption Mapping

**TL;DR:** Write down every belief you're treating as fact — about users, market, tech, business — and plot each on a 2×2 of importance vs. certainty. The top-left quadrant (high importance, low certainty) is what the sprint must test first; everything else gets documented or built on.

## When to use

- When the team keeps arguing about things that "might be true."
- When a Traffic Light decision is 🟡 because of an unresolved assumption.
- Before committing to a prototype direction, to validate the riskiest bets.
- When a stakeholder says "but we don't really know if users want this."

## The 2×2 matrix

```
HIGH IMPORTANCE
        |
  RISKY |  VALIDATE FIRST     |   BUILD ON THESE
(high   |  (sprint tests       |   (strong foundation;
import, |  these first)        |   confirm in validate)
low cert)|                     |
        |---------------------+-----------------------
  LOW   | LOW PRIORITY         |   LIKELY FINE
RISK    | (document, revisit)  |   (monitor)
        |
LOW IMPORTANCE
X-axis: CERTAINTY (Low → High)   ·   Y-axis: IMPORTANCE (Low → High)
```

## Steps

1. **Brainstorm (10 min, silent):** each person writes every assumption — users, competitors, tech, business model, regulations. One per note. Start with "We believe…"
2. **Read out:** share each; place on the board without debate.
3. **Plot on the 2×2 (15 min):** for each — *importance* (if wrong, does the solution fail?) and *certainty* (how confident are we, data-backed vs gut?).
4. **Identify the critical zone (5 min):** top-left = "Validate First" → these become sprint questions and prototype tests.
5. **Name each as a testable hypothesis:** "We believe X. We'll test by [method]. We'll know we're right when [measurable signal]."
6. **Carry forward:** critical assumptions feed the Assumptions Board in a full sprint.

## Assumption starters

User behaviour ("users will…") · user desire ("users want…") · technical feasibility ("the system can…") · business viability ("the business can sustain…") · market ("the competitive landscape will…") · regulatory ("compliance will allow…").

## Output format

```markdown
## Assumption Map — [Project] · [Date]

### Critical (High importance, Low certainty) — test these
| Assumption | Why risky | Test | Success signal |
|---|---|---|---|
| The coordinator wants ranked requests, not a raw inbox | ranking UI is useless if wrong | ranked vs unranked prototype | prioritises by score in ≥3/5 interviews |

### Foundation (High importance, High certainty) — build on these
- Urgent requests are missed due to volume + manual process [observed | 2026-02-17-coordinator-deepdive]

### Low-priority — document, revisit if scope expands
- Users prefer web over mobile for this workflow
```

## Agent guide

When reviewing a direction or PRD for hidden assumptions:
1. Read the goals / user stories / non-goals.
2. For every statement of user behaviour or desire, ask "what evidence?" (load `evidence-tagging`).
3. Extract implicit beliefs into an assumption log; plot each on importance/certainty.
4. Escalate any critical assumption with no corresponding test-plan item.

To resolve a 🟡 Yellow decision: the **trigger** = resolution of the top critical assumption; the **test** = what the prototype/interview validates; the **expiry** = when the test completes.

## Watch-outs

- **"We know this is true"** — how? Gut feeling or hearsay = low certainty.
- **Risk framing only** — positive assumptions ("users will love X") matter equally.
- **Too many in the critical zone** — prioritise the top 3–5; the rest get documented.
- **Skipping the "test" column** — an untestable assumption isn't a sprint candidate.

## Connects to

- `traffic-light-decisions` — a 🟡 Yellow is a named assumption with a trigger + expiry; this method produces them.
- `problem-framing` — the riskiest assumption often is the problem frame's central bet.
- `evidence-tagging` — each assumption's certainty maps to observed / reported / assumed.
- `design-sprint-tookit` (Decide phase) — `assumptions-board` revisits these after sketching in a full sprint.
