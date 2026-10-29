---
name: straw-poll
title: Take a non-binding team preference vote
description: Each team member votes for their favourite concept — non-binding. Surfaces team preference before the Decider makes the final call. Use after Speed Critique, before Supervote. Use when there are 2–4 viable concepts and the team needs to signal preference, or when the Decider needs data on team alignment before making their call.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - After Speed Critique, before Supervote
  - When there are 2–4 viable concepts and the team needs to signal preference
  - When the Decider needs data on team alignment before making their call
applies-to: team preference signalling, Decider briefing, concept selection
done_when:
  - Each person casts a non-binding vote with a one-line rationale
  - The team’s leaning is visible without being binding
  - The result is handed to the Decider for the supervote
metadata:
  duration: 5–10 min
  team-size: Full sprint team (equal 1 vote each)
  sprint-phase: 4 Decide
---

# Straw Poll

**TL;DR:** Each person places one vote on the concept they think should be prototyped. The vote is non-binding — the Decider makes the actual decision. But the Straw Poll shows the Decider the team's collective preference and surfaces any significant disagreement before the Supervote happens.

## When to use

- After Speed Critique, before Supervote
- When there are 2–4 viable concepts and the team needs to signal preference
- When the Decider needs data on team alignment before making their call

## Materials

- Large dot stickers (1 per person, different colour from heat map dots)
- All sketches still posted on the wall/board

## The rules

- **1 vote per person.** Including the Decider — they cast a straw poll vote too.
- **Vote on whole concepts** (not elements — that was Heat Map).
- **Vote simultaneously:** Everyone reveals at once. No one waits to see where the Decider votes.
- **Non-binding:** The Straw Poll result is information for the Decider, not the final decision.

## Steps

1. **Distribute straw-poll dots (1 min):** Larger dot, different colour from Heat Map dots. 1 per person.
2. **Silent voting (2 min):** Everyone holds their dot, thinks, then on a count of 3 — places it simultaneously.
3. **Read the result (2 min):** Facilitator calls out the distribution. "3 votes on Reasons-First Triage, 2 on One-Tap Assign, 1 on Shared Checking."
4. **Brief discussion of splits (3 min):** If the vote is split, ask people who voted for the minority option: "What did you see in this one that others missed?" — 1 sentence each.
5. **Hand off to Supervote:** The Decider now knows the team's preference and any minority arguments. They make the final call via Supervote.

## Interpreting results

| Vote pattern | Meaning | What to do |
|---|---|---|
| Strong consensus (5/6 on one sketch) | Team is aligned; Decider likely agrees | Supervote is a formality; move fast |
| Split (3/2/1) | Two viable concepts; real choice | Decider needs to hear minority argument; may split the prototype |
| Even split (3/3) | Genuine divergence | Decider must choose; or decide to prototype both (time permitting) |
| Unanimous (6/6) | Rare; either great alignment or groupthink | Check: is everyone actually convinced, or deferring to perceived authority? |

## Agent facilitation guide

When facilitating a Straw Poll decision:
1. List all viable concepts (typically 2–4 after Speed Critique)
2. Score each concept against Sprint Questions (how directly does it answer each question?)
3. Score each concept against Sprint Target (how specifically does it address the target moment?)
4. Produce a recommendation: "If I had one vote: [concept] because it most directly answers Sprint Questions 1 and 2"
5. Flag the strongest minority argument: "The case for [other concept]: [one sentence]"
6. Present both; let the Decider Supervote

Output:
```markdown
## Straw Poll Analysis — [Sprint Name]

| Concept | Sprint Q coverage | Target alignment | My recommendation |
|---|---|---|---|
| Reasons-First Triage | Q1 ✓, Q2 ✓✓, Q5 ✓ | High — Panel 2 is exactly the Check moment | ★ Recommend |
| One-Tap Assign | Q3 ✓ | Medium — addresses Assign, not Check | |
| Shared Checking | Q2 ✓ | High | Strong minority argument |

**My vote:** Reasons-First Triage
**Minority argument worth hearing:** Shared Checking — a multi-coordinator "confirmed by" trail addresses the trust question in a different (social) way. Worth noting even if not winning.
```

## Watch-outs

- **Sequential voting:** If people wait to see where the Decider votes, the Straw Poll is meaningless. Enforce simultaneous reveal.
- **Conflating Straw Poll with the decision:** The Decider may and should override a strong Straw Poll result if they have good reason. "The team voted X but I'm choosing Y because Z" is a valid and good use of Supervote.
- **No discussion of splits:** If the vote is split 3/3, skip the discussion. You'll polarise the room before the Supervote.

## Connects to

- [Speed Critique](../speed-critique/SKILL.md) — precedes this; informs team's vote
- [Supervote](../supervote/SKILL.md) — follows this; the actual binding decision
