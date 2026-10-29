---
name: how-might-we
title: Reframe a problem into opportunity questions
description: Convert research pain points, complaints, and constraints into open-ended "How Might We…" opportunity questions — the gateway from problem to possibility. Use when reframing a finding into something designable, priming ideation, or when a problem statement is stuck in solution language. Daily-driver thinking tool, also a sprint Understand-phase method.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Reframing a research pain point or complaint into a designable opportunity
  - Priming a team (or yourself) before ideation with possibility framing
  - A problem statement keeps prescribing a solution ("we need a dashboard") and needs opening up
  - Capturing opportunities in real time during expert interviews / user research
applies-to: problem reframing, research synthesis, ideation priming, HMW voting
done_when:
  - Each pain point is reframed as an open “How might we…” question
  - HMWs are neither solution-prescriptive (too narrow) nor generic (too broad)
  - HMWs are clustered and the riskiest-challenge cluster is surfaced
metadata:
  duration: 20–30 min capture + 20 min review
  team-size: solo or full team
  sprint-phase: 1 Understand
---

# How Might We (HMW)

**TL;DR:** Turn an observation, complaint, or constraint into an open-ended "How might we…" question — specific enough to be useful, broad enough not to prescribe the solution. HMWs are the currency between *problem* and *possibility*: voted on, placed on the map, carried forward as the design lens.

## When to use

- **During** expert interviews and user research — capture HMWs in real time.
- **After** research synthesis — translate findings into opportunities.
- **Before** ideation — prime the team with possibility framing.
- **Whenever** a problem statement has hardened into a solution ("we need a search bar") and needs reopening.

## The HMW formula

> **"How might we"** + **[verb]** + **[outcome for user]** + **[context/constraint]?**

The three words do precise work:
- **"How"** — implies it's solvable (not rhetorical).
- **"Might"** — lowers the stakes; exploration, not commitment.
- **"We"** — collective ownership.

## Steps

1. **Capture (parallel, silent):** one idea per note, a different colour per source/expert.
2. **Volume first:** 10–20 HMWs per person; bad ones are fine, they get filtered.
3. **Read-out (2 min):** each person reads their top 5 — exposure, no critique.
4. **Cluster:** group similar HMWs; name each cluster in 1–2 words.
5. **Feed forward:** HMWs move into voting / onto the opportunity map.

## The three-level test (tuning)

| Problem | Too narrow (prescribes) | Right | Too broad (not actionable) |
|---|---|---|---|
| Coordinators can't spot urgent requests | HMW add a search bar? | HMW help coordinators surface urgent requests without hunting? | HMW improve the product? |
| Checking a booking takes too long | HMW automate the checks? | HMW make checking a booking faster and more trustworthy? | HMW save users time? |

**Rule of thumb:** if the HMW names a specific solution, it's too narrow — strip the solution word. If removing the problem context makes it apply to any product, it's too broad.

## Agent guide

When synthesising research into HMWs:
1. Read all findings/pain points.
2. For each, generate 2–3 HMWs at different abstraction levels.
3. Flag HMWs that connect to the long-term goal (sprint-target candidates).
4. Deduplicate; group by theme; output a flat list with evidence tags (load `evidence-tagging`).

When reviewing existing HMWs: flag solution language (too narrow), flag missing user/context (too broad), surface the cluster around the riskiest design challenge.

## Output format

```markdown
## HMW Notes — [Project]

### Cluster: Urgent-Request Discovery
- HMW help the coordinator surface the top 3 requests that need their attention this morning?
- HMW make a booking's confirmation status visible at a glance? [observed | 2026-02-17-coordinator-deepdive]
```

## Watch-outs

- **Starting with solutions** ("HMW build a dashboard that…") — strip back to the user need.
- **Passive voice** ("HMW improve request quality") — who does what for whom? Make it active.
- **Ignoring constraints** — great HMWs honour real constraints; note infeasible ones as assumptions.
- **Skipping the cluster step** — unorganised HMWs can't be voted on.

## Connects to

- `problem-framing` — HMWs operationalise the problem frame's people-problem.
- `evidence-tagging` — each HMW carries its source evidence tag.
- `design-sprint-tookit` (Define phase) — `how-might-we-voting` and `sprint-map` consume the HMWs downstream in a full sprint.
- Loop: `design-thinking-loop` — HMW is an Understand-phase move.
