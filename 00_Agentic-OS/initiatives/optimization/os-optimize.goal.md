---
type: goal
slug: os-optimize-loop
owner: OS steward
created: 2026-10-29
updated: 2026-10-29
agent: goal-runner
status: standing
rubric: ./os-optimize.rubric.md
source: ../../OPTIMIZATION-BACKLOG.md
tags: [type/goal, purpose/measure, status/standing, scope/agent-os]
outcome: >-
  Improve one demonstrated outcome of this operating system per cycle: quality, reliability, retrieval,
  recovery, onboarding or useful execution efficiency. A cycle ends with a verified improvement, a justified
  no-change result or an explicit blocker; it never creates work to raise a score.
verification: >-
  State the acceptance and capture the baseline before changing files, run the smallest checks that establish
  the outcome, widen regression checks with risk, and keep python3 00_Agentic-OS/agentic-os-review.py at
  VERDICT PASS. Separate pre-existing findings from failures introduced by the cycle.
constraints: >-
  Preserve authorization, source provenance and historical evidence. Do not weaken a check, lower a threshold,
  fabricate a result or add placeholders to pass a gate. Do not add a competing backlog or scheduler.
  Plug-in sources change only upstream.
iteration_policy: >-
  Read the backlog and existing evidence; choose one coherent problem and its acceptance; retrieve only relevant
  sources; make the smallest complete change; validate; append proof and the next action to the run record;
  update the backlog row. Do not retry an unchanged failing strategy.
error_handling: >-
  Stop the affected action for unknown authority, unsafe concurrent edits, irreconcilable evidence, a new
  unresolved regression, repeated no-progress or a real service limit, and name a concrete resume path.
  Publishing and consequential commitments stay with their human gates.
output_expectation: >-
  An updated backlog row, one dated run record in 00_Agentic-OS/_runs/ with baseline, change, exact paths,
  checks, rubric verdict and rollback, and a concise outcome statement.
---

# Standing OS optimization loop

**TL;DR:** Improve a demonstrated outcome, prove it against a scoped baseline and keep the review green; a bigger file count or a rising score is never the goal.

## The loop

[Backlog](../../OPTIMIZATION-BACKLOG.md) → scoped acceptance → baseline → complete change → rubric
([os-optimize.rubric.md](os-optimize.rubric.md)) → regression checks → [run record](../../_runs/README.md) → next item.

## Measure the outcome, not the artifact

- Correctness, recoverability, rework avoided, onboarding time, retrieval precision, maintenance burden.
- Say when a measure is a proxy or a synthetic fixture.
- Keep earlier run records unchanged; explain any score that moves because of an authorized cleanup.

## Non-goals

- No automatic promotion, publishing, schedule change or human-gate bypass.
- No placeholders, duplicate guides or unused infrastructure created to satisfy a metric.
- No edits to mounted plug-ins; use the [plug-in optimization loop](../plugin-optimization/plugin-optimize.goal.md).
