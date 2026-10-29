---
name: decision-matrix
title: Score options against weighted criteria
description: Make a comparative choice transparent and defensible by scoring each option against weighted criteria — especially when options are close in quality. Use when you're stuck between 2–3 concepts, when preference (not evidence) is driving selection, or when a decider needs to justify a choice to senior stakeholders with explicit reasoning.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Stuck between 2–3 genuinely competitive options and you need a structured comparison
  - Personal preference is driving selection rather than the criteria that matter
  - A decider must communicate a choice to senior stakeholders with a defensible rationale
  - Trade-off analysis where some criteria matter far more than others (weighting)
applies-to: concept comparison, structured decision making, trade-off analysis, stakeholder communication
done_when:
  - Each option is scored against every weighted criterion
  - Weighted totals are computed and the winner + its weak criterion noted
  - Combinable elements from losing options are identified
metadata:
  duration: 20–30 min
  team-size: solo, or full team; decider approves weights + final selection
  sprint-phase: 4 Decide
---

# Decision Matrix

**TL;DR:** Score each option against the criteria that matter, weight the criteria by importance, and total. Makes the *reasoning* explicit — which option best satisfies what matters most — and is most valuable when two options are close and you need to surface what's actually different and why. Analytical input to a human decision, not a replacement for it.

## When to use

- When 2–3 options are genuinely competitive and need a structured comparison.
- When the decider must communicate a choice to senior stakeholders with a rationale.
- When personal preference is driving selection rather than the criteria.

## The matrix structure

Rows = criteria · Columns = options · Cells = score (1 = doesn't meet, 2 = partially, 3 = fully) · Weight = importance per criterion (1–3) · Weighted score = weight × cell.

```
                         Option A    Option B    Option C
Criterion 1 (weight 3)      3            2            1
Criterion 2 (weight 3)      2            3            2
Criterion 3 (weight 2)      3            2            3
Criterion 4 (weight 1)      1            2            3
─────────────────────────────────────────────────────
Weighted total              24           22           18
```

## Steps

1. **Post the criteria + weights (2 min):** list the criteria; the decider confirms weights (1–3).
2. **Score each option per criterion (10–15 min):** score silently and simultaneously, then read the average/mode — avoids scoring-as-advocacy.
3. **Apply weights and total (5 min):** multiply, sum per option.
4. **Find the winner — and the gaps (5 min):** highest total wins, but note which criterion each option won; losing options often have strong elements worth incorporating.
5. **Hand to the decider (3 min):** the matrix informs the decision; the decider may override for strategic value the criteria didn't capture (and states why, in one sentence, logged as an ADR note).

## Agent guide

When generating a Decision Matrix:
1. List the criteria with weights.
2. Score each option against each criterion using evidence, not intuition; flag any score that is `assumed` rather than `observed` (load `evidence-tagging`).
3. Calculate weighted totals; note the winner and the criterion it lost on.
4. Identify combinable elements — which part of a losing option should be folded into the winner.

## Watch-outs

- **Equal weights for everything** — then it's just a sum of scores; the weighting is the most important step.
- **Scoring as advocacy** — favourites get inflated; score silently and average.
- **Matrix replacing the decision** — it's analytical input; the human still chooses.
- **Forgetting constraints** — an option that violates a known constraint should score 1 on a constraint-compliance criterion, which (weighted) drops it out of contention.

## Connects to

- `rubric-authoring` — the weighted criteria ARE a rubric; author them there for repeatable scoring.
- `traffic-light-decisions` — the matrix surfaces the trade-off; the decision still closes with one light.
- `evidence-tagging` — each score carries its provenance (observed vs assumed).
- `design-sprint-tookit` (Decide phase) — `speed-critique`, `straw-poll`, and `supervote` surround the matrix in a full sprint.
