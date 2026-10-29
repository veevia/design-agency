---
type: rubric
slug: <slug>
goal: ./<slug>.goal.md
owner: <one named person>
baseline_reviewed: <N real outputs read before writing this rubric>
weighted_toward: <the model's known weak spots, e.g. "non-goals left thin; happy path only">
calibration_rounds: 0          # increment after each human-vs-reviewer comparison
---
# <Task type> — review rubric

**TL;DR:** <one sentence — what "good" means for this task, in the reviewer's terms>.

<!--
  RULE: every row is a CONCRETE case a reviewer can catch at a glance — a named NEVER or ALWAYS —
  never an abstraction ("be original", "make it clean"). Build it from a baseline of real outputs.
  ANTI-OVERFIT: give ≥3 diverse anchors on taste dimensions, never a single one.
  RENDERED ARTIFACTS: score the screenshot, not the source.
-->

## Dimension 1 — <name, e.g. "scope fence"> (weight: high)

| ID | Level | Case | How the reviewer checks |
|---|---|---|---|
| D1.1 | MUST | **Never** <named offender> | <observable check> |
| D1.2 | MUST | **Always** <named requirement> | <observable check> |

## Dimension 2 — <name, e.g. "voice"> (weight: medium)

| ID | Level | Case | How the reviewer checks |
|---|---|---|---|
| D2.1 | SHOULD | **Never** <named offender> | <observable check> |

## Dimension 3 — <name, e.g. "originality"> (weight: high — the model is weak here)

| ID | Level | Case | How the reviewer checks |
|---|---|---|---|
| D3.1 | SHOULD | Pick one anchor per situation: <anchor A> · <anchor B> · <anchor C> | <observable check> |

## Verdict rule

- PASS: every MUST row is green.
- ITERATE: a MUST row is red and the executor can fix it.
- BLOCKED: only rows gated on a human or an external system remain red.
- Every row is scored or printed as `NOT-SCORED (reason)`.

## Calibration log

| Round | Reviewer verdict | Human verdict | Rubric change |
|---|---|---|---|
| 1 | | | |

<!--
  VALIDATE: python3 06_Engine/harness/lint-skill.py rubric-authoring --severity warning
-->
