---
name: five-whys
title: Trace a recurring problem to its root cause
description: Ask "why" five times to drill past symptoms to the root cause of a problem — before designing a solution that treats the wrong thing. Use when a problem feels like a symptom of something deeper, before writing Sprint Questions, or when the team disagrees about what's causing a problem.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - When a problem feels like a symptom of something deeper
  - Before writing Sprint Questions — to ensure the question targets the root cause, not the surface
  - When the team disagrees about what's causing a problem
  - When a proposed solution would address the symptom but might not prevent recurrence
  - After Expert Interviews reveal a recurring pain that hasn't been solved despite previous attempts
applies-to: root cause analysis, problem reframing, HMW generation, assumption challenging, scope calibration
done_when:
  - The chain of “why” reaches a root cause, not a symptom
  - Each step names a cause, not a blame
  - The root cause converts into an HMW or a fix to test
metadata:
  duration: 15–20 min per problem thread
  team-size: Small group (2–4); full team for review
  sprint-phase: 1 Understand
---

# Five Whys

**TL;DR:** The Five Whys technique stops a team from designing solutions for symptoms. When a user pain is identified — "coordinators spend 40 minutes on manual triage every morning" — the instinct is to address it directly. The Five Whys asks: is this the real problem, or is there a deeper cause that, if addressed, would eliminate the symptom entirely? You ask "why?" five times in sequence, each time taking the previous answer as the new problem to explain. Typically the root cause emerges by the third or fourth why.

## When to use

- When a problem feels like a symptom of something deeper
- Before writing Sprint Questions — to ensure the question targets the root cause, not the surface
- When the team disagrees about what's causing a problem
- When a proposed solution would address the symptom but might not prevent recurrence
- After Expert Interviews reveal a recurring pain that hasn't been solved despite previous attempts

## The method

State the problem clearly, then ask "Why does this happen?" five times:

```
Problem: Coordinators spend 40 minutes manually triaging overnight requests every morning.

Why 1: Why do they spend 40 minutes?
→ Because they can't quickly tell which requests are urgent without cross-checking the CRM, service-contract database, and inventory system.

Why 2: Why can't they tell without cross-checking?
→ Because the booking inbox shows only the customer's description and the booking channel — no urgency indicator or request context.

Why 3: Why doesn't the inbox show urgency or context?
→ Because the inbox was built to collect bookings, not assess them — prioritising was always a manual step.

Why 4: Why was prioritising left manual?
→ Because when the inbox was built, automated ranking wasn't available and the team didn't want to invest in manual tagging.

Why 5: Why hasn't this changed since a ranking model became available?
→ Because integrating the AI ranking requires the model team's involvement, which has a 6-week backlog.

Root cause: AI ranking capability exists but isn't integrated; the bottleneck is team coordination and backlog priority — not technical impossibility.
```

## Root cause vs. symptom — the test

The root cause is usually reached when the answer reveals:
- A structural decision made in the past
- A process or governance gap
- A missing capability, not just a missing feature
- A constraint that, if removed, would solve multiple symptoms

If the fifth "why" answer still feels like a symptom, keep going. If an answer reveals something the team can't influence in this sprint, that's a constraint — document it and stop that branch.

## Rules

- **One chain per problem thread:** Don't fork into multiple "why" paths in the same conversation. If two different explanations emerge, document both chains separately.
- **Ask about *causes*, not *blame*:** "Why did the team not prioritise this?" is blame. "Why was this deprioritised?" is cause analysis.
- **Stop when you hit a constraint:** If the answer is "because of a law/regulation/competitor action" — that's a boundary condition, not a solvable root cause. Stop there.
- **Validate with evidence:** Each "why" answer should be grounded in observed or reported evidence. Flag assumptions: "We think this is why, but it hasn't been confirmed."

## Five Whys output format

```markdown
## Five Whys — [Problem Statement] · [Sprint Name] · [Date]

**Symptom:** [The surface-level problem observed or reported]

| Level | Why? | Answer | Evidence |
|---|---|---|---|
| Why 1 | Why does [symptom] happen? | [Answer 1] | [observed/reported/assumed] |
| Why 2 | Why does [answer 1] happen? | [Answer 2] | [observed/reported/assumed] |
| Why 3 | Why does [answer 2] happen? | [Answer 3] | [observed/reported/assumed] |
| Why 4 | Why does [answer 3] happen? | [Answer 4] | [observed/reported/assumed] |
| Why 5 | Why does [answer 4] happen? | [Answer 5] | [observed/reported/assumed] |

**Root cause:** [Final answer — the underlying structural cause]
**Evidence quality:** [Overall assessment — how much of this chain is observed vs. assumed]
**Constraint hit (if any):** [If the chain hit an external constraint — name it]

**Sprint implication:**
- If we address the root cause, the symptom [would / might / would not] be resolved
- HMW derived: "How might we [address root cause]?"
```

## Multiple chains

Some problems have multiple root causes — different "why" branches lead to different places. Run separate chains and compare:

```markdown
Problem: Assignment errors occur (requests reach the wrong specialist)

Chain A: Coordinator selects the wrong specialist → specialist list is alphabetical, not skills-sorted → system has no matching intelligence → root: no skills-based matching
Chain B: Coordinator guesses when unsure → no skills or certification indicator in the assignment form → system was built for experienced coordinators, not new starters → root: poor onboarding design
Chain C: Coordinator uses a workaround (phoning the site) when uncertain → a phone call is faster than the 7-step form → root: form UX is too slow for a time-pressured workflow
```

Three different root causes → three different Sprint Questions → Sprint Target selects which to focus on.

## Agent facilitation guide

When running a Five Whys analysis from sprint research:
1. State the problem clearly — quote observed behaviour if possible
2. For each "why" step: provide an answer grounded in research evidence; tag with `observed/reported/assumed`
3. Identify if the chain hits a structural decision, a process gap, or an external constraint
4. Stop when the root cause is reached (structural issue) or when an unresolvable constraint is hit
5. Generate one HMW from the root cause
6. Flag assumptions in the chain that the sprint should validate

## Watch-outs

- **Stopping at "users don't want to":** This is almost never the root cause — it's a symptom of something else (bad UX, wrong mental model, insufficient value). Keep asking why.
- **Reaching the root cause in one why:** If the root cause is obvious from the first question, the problem may already be well-understood. Five Whys is most useful when the cause is unclear or disputed.
- **The chain becoming circular:** "Why X? Because Y. Why Y? Because X." Stop and reformulate the problem.
- **Using it to justify a pre-decided solution:** If every chain mysteriously leads to "therefore we need to build Feature Z," the team is reverse-engineering, not analysing.

## Connects to

- [Expert Interviews](../expert-interviews/SKILL.md) — interviews surface the answers to "why" questions
- [Fishbone Diagram](../fishbone-diagram/SKILL.md) — Five Whys explores one branch in depth; Fishbone maps all branches simultaneously
- [How Might We](../how-might-we/SKILL.md) — root causes generate the strongest HMW questions
- [Sprint Questions](../sprint-questions/SKILL.md) — root causes become Sprint Questions
