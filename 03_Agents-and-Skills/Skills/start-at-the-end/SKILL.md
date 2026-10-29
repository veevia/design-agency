---
name: start-at-the-end
title: Pre-mortem a feature with a failure press release
description: Envision the future state two years out — then list what could go wrong. Sets the optimistic north star and the failure scenarios that become Sprint Questions. Use at the start of Phase 1, before research activities, as an opening frame for the sprint, or as the transition from Phase 1 to Phase 2. Use when the team lacks a shared picture of what success looks like.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - At the start of Phase 1, before research activities, as an opening frame for the sprint
  - Alternatively, as the transition from Phase 1 to Phase 2 — after research, before defining the Long-Term Goal
  - Any time the team lacks a shared picture of what success looks like
  - When stakeholders have different visions of the same goal
applies-to: goal setting, failure mode identification, sprint question generation, long-term thinking, risk framing
done_when:
  - A concrete failure scenario (“why this flopped”) is written
  - Failure modes that can’t be resolved this sprint become assumptions
  - The pre-mortem surfaces at least one design guardrail
metadata:
  duration: 30–45 min
  team-size: Full sprint team; Decider leads
  sprint-phase: 1 Understand
---

# Start at the End

**TL;DR:** Before the team can define what to build, they need to agree on where they're going. Start at the End asks the team to imagine the sprint has been a success — not just the sprint, but the whole program: two years from now, what has changed? Then it flips the question: what could cause that future to not happen? The answers to the second question become the sprint's Sprint Questions — the risks the sprint must resolve.

## When to use

- At the start of Phase 1, before research activities, as an opening frame for the sprint
- Alternatively, as the transition from Phase 1 to Phase 2 — after research, before defining the Long-Term Goal
- Any time the team lacks a shared picture of what success looks like
- When stakeholders have different visions of the same goal

## The two questions

**Question 1 — Optimistic vision:**
> "It's two years from now. The sprint was a success. The product is working, users love it, and we hit our goals. What does that look like? Be specific."

**Question 2 — Pre-mortem:**
> "Now imagine the sprint *failed*. Not just a minor setback — it failed badly. The product was built and nobody used it, or it made things worse, or the business didn't benefit. What went wrong?"

Each answer to Question 2 is a potential Sprint Question in the form: "Can we [overcome this failure mode]?"

## Structure

### Part 1 — Optimistic vision (15 min)

Each person writes their vision of success in 2 years on a sticky note — 1 sentence per sticky, as many stickies as they want. The Facilitator reads them out. The team clusters similar visions. The Decider names the dominant cluster — this becomes the candidate Long-Term Goal.

### Part 2 — Pre-mortem / Failure listing (15–20 min)

Each person silently writes: "What could cause this sprint to fail?" — one failure per sticky. Simultaneously post and read aloud. Common categories:

| Category | Example failure mode |
|---|---|
| **User behaviour** | "Coordinators don't trust the suggested priority and won't act on it" |
| **Technical** | "The booking inbox API can't support inline service-contract and inventory details" |
| **Adoption** | "Coordinators use the tool once and revert to their spreadsheets" |
| **Business** | "Leadership deprioritises the rollout before it reaches Site C" |
| **Design** | "The solution is too complex for a 40-minute morning triage workflow" |
| **Data** | "AI error rate is too high to create user trust" |

Cluster the failure stickies. The Decider identifies the top 3–5 clusters — those most likely and most damaging. These become Sprint Questions.

### Part 3 — Convert to Sprint Questions (10 min)

For each top failure cluster, write a Sprint Question:
- Failure: "Coordinators won't trust the suggested priority"
- Sprint Question: "Can we design an AI-assisted triage experience that coordinators trust enough to act on without manual cross-referencing?"

## Example output

```markdown
## Start at the End — Request Triage Sprint · 2026-02-24

### 2-year optimistic vision (Decider's selection)
"Coordinators for all three sites use a single request queue that reduces morning triage time from 40 minutes to under 10. Urgent requests are never missed. Wrong assignments drop to near zero. The AI assists rather than replaces coordinator judgment."

### Failure modes (top clusters after voting)

1. **Priority trust failure** — Coordinators don't trust the suggested priority enough to act without manual checks → the tool adds steps, not removes them
2. **Adoption drop-off** — Initial enthusiasm wanes after 2 weeks; coordinators revert to spreadsheets because the tool doesn't fit their actual morning rhythm
3. **Assignment still broken** — The assignment improvement is blocked by IT constraints; the new UI just wraps an old broken process
4. **Coverage gap** — The tool works for the busy sites (Site B, Site C) but the quieter Site A doesn't have the request volume to get value from AI ranking
5. **Scope too big** — We try to solve too many problems; the prototype is confusing and tests nothing clearly

### Sprint Questions derived
1. Can we build an AI-assisted triage experience that coordinators trust without needing to check manually?
2. Will coordinators complete their morning triage faster with the new tool after a 2-week adoption period?
3. Can we implement one-tap assignment within the current specialist calendar API constraints?
4. Does the value proposition hold for the quieter Site A, or only for the busy sites?
5. Can we keep the prototype scope narrow enough to test assumption 1 clearly?
```

## Agent facilitation guide

When facilitating a Start at the End session:
1. Ask the team for 2-year success descriptors — extract the most specific and measurable
2. Run the pre-mortem: "What could cause this to fail?" — generate 10–15 failure stickies
3. Cluster failures by category (user behaviour, technical, adoption, business, design, data)
4. Rank clusters by: likelihood × damage if it occurs
5. Convert top 3–5 into Sprint Questions using the "Can we..." format
6. Flag any failure mode that is already a known risk (from prior research or stakeholder input) — these get extra weight

## Watch-outs

- **Generic visions:** "Users will be happy" is not a usable vision. Push for specificity: "The Lead Coordinator completes morning triage in under 10 minutes and doesn't open a single other system."
- **The team softening the pre-mortem:** Groups are reluctant to voice failures. Reinforce: "This is hypothetical. We're not saying it *will* fail — we're looking for the risks worth designing against."
- **Too many Sprint Questions:** If the pre-mortem produces 15 failure clusters, you need to pick the 3–5 that are both most likely and most damaging. More than 5 Sprint Questions and the sprint loses focus.
- **Confusing failure modes with tasks:** "We didn't finish the prototype" is a logistics failure, not a sprint question. Focus on product and user failures, not process failures.

## Connects to

- [Long-Term Goal](../long-term-goal/SKILL.md) — the optimistic vision becomes the Long-Term Goal
- [Sprint Questions](../sprint-questions/SKILL.md) — failure modes become Sprint Questions
- [Assumption Mapping](../assumption-mapping/SKILL.md) — failure modes that can't be resolved in one sprint become assumptions
- [`00_README/_frameworks/traffic-light-decisions.md`](../../../00_README/_frameworks/traffic-light-decisions.md) — each Sprint Question = a potential Yellow trigger condition
