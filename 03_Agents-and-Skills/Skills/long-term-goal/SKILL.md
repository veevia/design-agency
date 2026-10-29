---
name: long-term-goal
title: Write the aspirational 2-year north-star goal
description: Articulate where the team wants to be in 2 years — optimistic but grounded. The north star that prevents sprint scope from shrinking to a local fix. Use when at the start of a sprint's Define phase, after Understand, when the team is debating tactics without an agreed strategic direction, or when a Design Brief or PRD needs a north star before user stories are written.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - At the start of a sprint's Define phase, after Understand
  - When the team is debating tactics without an agreed strategic direction
  - When a Design Brief or PRD needs a north star before user stories are written
applies-to: sprint opening, stakeholder alignment, design brief framing, PRD goals section
done_when:
  - A single optimistic 2-year goal sentence is agreed
  - The goal is customer-outcome framed, not feature framed
  - The goal anchors the sprint questions that follow
metadata:
  duration: 20–30 min
  team-size: Full sprint team + Decider
  sprint-phase: 2 Define
---

# Long-Term Goal

**TL;DR:** The Long-Term Goal is a single, optimistic statement of success 2+ years out. It keeps the sprint from optimising for a local fix while ignoring the larger trajectory. It also makes the "How do we fail?" questions more honest — if the goal is ambitious, the ways to fail it are more specific.

## When to use

- At the start of a sprint's Define phase, after Understand
- When the team is debating tactics without an agreed strategic direction
- When a Design Brief or PRD needs a north star before user stories are written

## The 2-year question

> "If everything goes right, what does [user/product/business] look like in 2 years?"

Frame it as an **"I can" statement** from the user's perspective — or as a **mission-style outcome** from the team's:

| Frame | Example |
|---|---|
| User "I can" | "Site supervisors at Site C can receive and act on urgent requests within 2 hours without ever having to phone head office." |
| Team outcome | "The request system becomes the shared view that connects head office and every site — with no urgent request falling through the cracks." |
| Business outcome | "The organization has zero missed urgent requests in peak season because every urgent request is assigned within 2 hours of reaching the booking inbox." |

## Steps

1. **Silent write (5 min):** Each person writes their Long-Term Goal on a sticky note.
2. **Read aloud (5 min):** No debate — just exposure. Notice where the framing diverges.
3. **Theme map (5 min):** Group similar goals. Name the themes.
4. **Craft together (10 min):** Combine the strongest elements into one statement. The Decider has final word on the language.
5. **Test against "How might we fail" (5 min):** Read the goal aloud and ask: "What would make this fail?" — these become Sprint Questions.

## Quality check

A good Long-Term Goal:
- [ ] Is 2+ years out (not "ship this quarter")
- [ ] Is optimistic but grounded — the team believes it's achievable
- [ ] Is specific enough to fail in a concrete way
- [ ] Doesn't contain jargon or internal acronyms a user wouldn't recognise
- [ ] Fits in one sentence

## Output format

```markdown
## Long-Term Goal — [Sprint Name]

**Statement:** [Single sentence, present tense as if already achieved]

**Framing notes:**
- Divergent positions heard: [name: their version]
- Decider rationale for final wording: [one sentence]
```

## Agent facilitation guide

When drafting a Long-Term Goal from existing documents (PRD, Brief, POV):
1. Extract all goal and mission language from existing artefacts
2. Identify the 2-year horizon statement — often implicit in the "Background" section
3. Rewrite as an active, measurable statement from the user's or business's perspective
4. Surface one alternative framing (to show the Decider the choice they're making)
5. Tag the confidence level: is this goal supported by user research (`observed`/`reported`) or team hypothesis (`assumed`)?

## Watch-outs

- **Too operational:** "Improve the urgency-scoring accuracy by 20%" — that's a metric, not a goal. Goals describe the world; metrics measure progress toward it.
- **Too vague:** "Be the best triage platform" — what does "best" mean? For whom?
- **Multiple goals:** The method produces one goal. If the team insists on two, that's a scope conversation, not a goal conversation.

## Connects to

- [Sprint Questions](../sprint-questions/SKILL.md) — derived from "how might this goal fail"
- [`00_README/_templates/2-1-Design_POV.template.md`](../../../00_README/_templates/2-1-Design_POV.template.md) — §Goals and §Hypothesis directly map here
- [`00_README/_templates/2-2-Design_brief.template.md`](../../../00_README/_templates/2-2-Design_brief.template.md) — §1-Liner Why
