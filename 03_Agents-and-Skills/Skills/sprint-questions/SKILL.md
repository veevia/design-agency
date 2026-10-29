---
name: sprint-questions
title: List the questions this sprint must answer
description: Convert the Long-Term Goal into 3–5 specific questions the sprint must answer. The riskiest uncertainties become the sprint's research agenda. Use after setting the Long-Term Goal. Use when a sprint is too broad and needs a focused research agenda, or when setting up the Phase 6 Validate interview structure.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Immediately after setting the Long-Term Goal
  - When a sprint is too broad and needs a focused research agenda
  - When setting up the Phase 6 Validate interview structure
  - When writing the test plan hypothesis section
applies-to: sprint scoping, test plan framing, assumption resolution, PRD open questions
done_when:
  - Questions are phrased as “Can we…?” sprint risks
  - Each maps to a critical assumption or goal
  - The questions are answerable by the planned prototype/test
metadata:
  duration: 20–30 min
  team-size: Full sprint team
  sprint-phase: 2 Define
---

# Sprint Questions

**TL;DR:** Sprint Questions reframe the Long-Term Goal as falsifiable questions. They flip the optimism of the goal into productive pessimism: "What would have to be true for this goal to succeed? What might cause it to fail?" The answers the sprint produces are your evidence base for the forward decision.

## When to use

- Immediately after setting the Long-Term Goal
- When a sprint is too broad and needs a focused research agenda
- When setting up the Phase 6 Validate interview structure
- When writing the test plan hypothesis section

## The formula

> "Can we [verb + outcome]?"
> "Will users [behaviour]?"
> "Is [assumption] true in [context]?"

Sprint Questions are different from HMWs:
- HMW = design opportunity ("how might we…")
- Sprint Question = testable uncertainty ("will users… / can we… / is it true that…")

## Steps

1. **Start from the Long-Term Goal:** Read it aloud.
2. **Ask "How might this fail?" (10 min, silent):** Each person writes the questions they'd need answered to have confidence the goal is achievable. One question per sticky note.
3. **Read aloud (5 min):** No critique. Note where different people are uncertain about different things.
4. **Cluster and prioritise (10 min):** Which questions, if left unanswered, would make the sprint useless? Those go to the top.
5. **Pick 3–5 (5 min):** More than 5 and the sprint can't test them all meaningfully. Fewer than 3 and the sprint is under-constrained.
6. **Assign each question to a prototype/interview task** in Phase 5–6.

## Question types

| Type | Example | Tests |
|---|---|---|
| User behaviour | "Will coordinators check the urgent queue first without being reminded?" | Adoption assumption |
| Comprehension | "Can coordinators tell the difference between a confirmed and an unconfirmed booking without a tutorial?" | UX clarity assumption |
| Value | "Do site supervisors find a pre-sorted request list more useful than the raw booking inbox?" | Core value assumption |
| Feasibility | "Can we match the right parts to a Site C request with enough precision to be actionable?" | Technical assumption |
| Trust | "Will coordinators trust the suggested priority enough to act on it?" | Trust/adoption assumption |

## Output format

```markdown
## Sprint Questions — [Sprint Name]

**Long-Term Goal:** [one sentence]

| # | Sprint Question | Type | Tested how |
|---|---|---|---|
| 1 | Will coordinators prioritise requests using urgency scores without coaching? | Behaviour | T1 in usability test |
| 2 | Can the Lead Coordinator distinguish confirmed from unconfirmed bookings at a glance? | Comprehension | T2 in usability test |
| 3 | Do coordinators want one unified queue vs. separate per-channel views? | Value | Post-task interview Q |
| 4 | Will site supervisors accept requests assigned from the suggested priority? | Trust | Open question in debrief |
| 5 | Can the request system's filtered-view model replace the need for a separate page per site? | Feasibility + Value | Implicit in all tasks |
```

## Agent facilitation guide

When generating Sprint Questions from existing PRD or POV:
1. Read the "Assumptions" and "Open Questions" sections
2. Rewrite each as a binary testable question ("Can we X?" / "Will users Y?")
3. Flag which questions have no corresponding test plan item (these are gaps)
4. Rank by impact: which questions, if answered "no," would change the design direction most?
5. For each question, suggest the minimum-viable test (interview task, A/B screen, observation point)

## Watch-outs

- **Questions that can't be tested in the sprint:** "Will this generate revenue?" — too long a feedback loop. Rewrite to the proximate assumption: "Will users say they'd pay for this?"
- **Yes/no questions only:** Make them falsifiable but not binary traps. "Do users prefer X" → "Which version do users gravitate toward, and why?"
- **Not connecting questions to interview tasks:** Sprint Questions without a corresponding test moment are just wishes. Every question needs a test.

## Connects to

- [Long-Term Goal](../long-term-goal/SKILL.md) — Sprint Questions are derived from goal + failure modes
- [Assumption Mapping](../assumption-mapping/SKILL.md) — critical assumptions become Sprint Questions
- [Five-Act Interview](../five-act-interview/SKILL.md) — interview tasks are designed to answer Sprint Questions
- [`00_README/_templates/3-1-Build_test-plan.template.md`](../../../00_README/_templates/3-1-Build_test-plan.template.md) — §Hypothesis maps to Sprint Questions
