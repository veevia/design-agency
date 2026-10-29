# Goal harness — why agents quit early, and field-tested pitfalls

On-demand detail for the `goal-harness` skill.

## Why the harness exists

Long-running agents tend to rush and stop early as their context fills — a "clock-out" behaviour
where the model declares success to end the episode. A better prompt does not fix this; an external
reviewer does. The reviewer holds the executor to an explicit bar round after round, so "done" is
decided by the rubric and the verification, not by the model's sense of having done enough.

## The executor ↔ reviewer loop

```
goal (5 elements + rubric)
      │
      ▼
 executor ──produces──▶ artifact
      ▲                    │
      │        reviewer ◀──┘  scores every rubric row + runs verification
      │                    │
      └── ITERATE (named gap) ◀──┤
          PASS → stop and deliver ◀──┤
          BLOCKED → stop and report 🔴 ◀──┘
```

## Field-tested pitfalls

- **The reviewer must check the whole rubric, or say what it skipped.** A reviewer that silently
  scores only the rows it can implement is itself a self-report. Every MUST/SHOULD/NEVER row is
  scored or printed as `NOT-SCORED (why)`.
- **Parallel work that shares a rate-limited upstream is negative work.** Units that are independent
  on disk are not independent if they call the same throttled API. Default to one at a time; fan out
  only across truly independent resources.
- **Silent stalls hide without a heartbeat.** Long batches print a line before each unit, run
  unbuffered (`python -u`), and set a per-unit timeout so one stuck call cannot hang the run.
- **Tri-state the stop signal.** PASS / ITERATE is not enough unattended: ITERATE reads as "keep
  going" when the true state is "blocked, needs a human". Add BLOCKED.
- **Reversible means reversible.** If the constraints say writes are undoable, record every write
  (a run log or ledger) and have the reviewer check that the record exists.
- **Keep the reviewer fast.** It runs every round: scope globs to known paths; never walk
  `node_modules` or virtual environments.
- **Calibrate first.** For the first 3–4 rounds of a new rubric, a human compares the verdict with
  the artifact. Agreement earns trust; disagreement means the rubric is the bug.

## Where the artifacts live in this OS

| Artifact | Path |
|---|---|
| Initiative goal | `00_Agentic-OS/initiatives/<slug>/<slug>.goal.md` |
| Initiative rubric | `00_Agentic-OS/initiatives/<slug>/<slug>.rubric.md` |
| Ranked queue | `00_Agentic-OS/OPTIMIZATION-BACKLOG.md` |
| Run evidence | `00_Agentic-OS/_runs/<YYYY-MM-DD>-<slug>.md` |

## Sources

- Public talk on running `/goal` agents for many hours (2026): https://youtu.be/PpeCur6fEXc
- Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

## See also

- Skill: [`../SKILL.md`](../SKILL.md) · Template: [`../assets/goal.template.md`](../assets/goal.template.md)
