# Initiatives — measured improvement loops

**TL;DR:** An initiative is a standing goal plus a rubric; one loop cycle picks a backlog item, measures a baseline, makes the smallest complete change, scores it against the rubric and records the evidence.

## How a cycle runs

```
backlog item ─▶ acceptance + baseline ─▶ change ─▶ evaluate (rubric) ─▶ test (regressions) ─▶ evidence ─┐
      ▲                                                                                                │
      └──────────────────────────── ITERATE until PASS, or stop with BLOCKED and a resume path ◀───────┘
```

1. Pick one item from [OPTIMIZATION-BACKLOG](../OPTIMIZATION-BACKLOG.md) (or the plug-in's own tracker).
2. State the acceptance and capture the baseline before changing anything.
3. Make the smallest complete change, including coupled fixes.
4. Score it against the initiative's rubric: PASS, ITERATE, BLOCKED or NOT-SCORED with a reason.
5. Run the [OS review](../agentic-os-review.py) and the targeted tests; no new regression may remain.
6. Record the cycle in [_runs/](../_runs/README.md) and update the backlog row.

Drive a cycle with the `goal-runner` agent or the `/optimize-loop` prompt; author new goals and rubrics with
the `goal-harness` and `rubric-authoring` skills.

## Standing initiatives

| Initiative | Goal | Rubric | Use it to |
|---|---|---|---|
| OS optimization | [goal](optimization/os-optimize.goal.md) | [rubric](optimization/os-optimize.rubric.md) | Improve this OS: gates, retrieval, recovery, docs, native capabilities |
| Plug-in optimization | [goal](plugin-optimization/plugin-optimize.goal.md) | [rubric](plugin-optimization/plugin-optimize.rubric.md) | Improve a plug-in (FDE toolkit skills, PDG or VPG workflows) from a measured baseline, upstream |

Add an initiative only for a recurring improvement theme with its own measurable outcome. One-off fixes
belong in the backlog, not a new goal file.
