---
description: "Run one goal-plus-rubric optimization loop to a verified result: pick an initiative or backlog item, capture the baseline, then analyze → plan → draft → evaluate (score every rubric row) → test (OS review and targeted checks) → record evidence, repeating until the rubric passes or a stop condition fires."
agent: agent
---

# /optimize-loop

Drives the `goal-runner` loop against an initiative in `00_Agentic-OS/initiatives/`. Procedure contract: [SOP `optimization-loop`](../../02_Workflows/SOPs/optimization-loop/SOP.md).

## Inputs

- **initiative** (optional, default `optimization`): a folder under `00_Agentic-OS/initiatives/` containing `<slug>.goal.md` and `<slug>.rubric.md`
- **item** (optional): one row of [`00_Agentic-OS/OPTIMIZATION-BACKLOG.md`](../../00_Agentic-OS/OPTIMIZATION-BACKLOG.md); omit to take the highest-ranked open row
- **budget** (optional): maximum rounds or time for this run (default: the goal's own budget, else 5 rounds)

## Procedure

1. **Load skills**: `goal-harness`, `rubric-authoring`, `evidence-tagging`, `extreme-clarity`; `traffic-light-decisions` only if a blocker or durable choice must be recorded.
2. **Analyze** — read the goal file and its rubric (see [`00_Agentic-OS/initiatives/README.md`](../../00_Agentic-OS/initiatives/README.md)), the chosen backlog row, and the latest records in `00_Agentic-OS/_runs/`. Refuse to start if the goal lacks a concrete outcome or a verification; ask for the missing element.
3. **Plan** — write this cycle's acceptance in one sentence and capture the baseline: the exact commands (for example `python3 00_Agentic-OS/agentic-os-review.py --fast`, a lint, an eval, a plug-in report) and their results, before changing anything.
4. **Draft** — make the smallest complete change inside the goal's `constraints`, including coupled fixes. Plug-in sources are out of bounds here; use [`/plugin-optimize`](../../02_Workflows/prompts/plugin-optimize.prompt.md).
5. **Evaluate** — score **every** rubric row as PASS, FAIL, or `NOT-SCORED (reason)`. For rendered artifacts, score a screenshot, not the source.
6. **Test** — re-run the baseline commands plus targeted tests, then `python3 00_Agentic-OS/agentic-os-review.py` (all MUST rows must pass). Separate pre-existing failures from new ones; no new regression may remain.
7. **Record** — write `00_Agentic-OS/_runs/<YYYY-MM-DD>-<slug>.md` in the shape from [`00_Agentic-OS/_runs/README.md`](../../00_Agentic-OS/_runs/README.md) and update the backlog row.
8. **Repeat or stop** — verdict `ITERATE` (name the gap; back to step 2), `PASS` (deliver), or `BLOCKED` (stop as a 🔴 with what was tried, where it is stuck, the resume step, and who unblocks). Stop also when the budget is spent; report the best artifact and the remaining gap.

## Output format

```
=== /optimize-loop <initiative> · item <id> · round <n> ===
Acceptance: <one sentence>
Baseline: <command → result>
Change: <summary> · paths: <exact paths>
Rubric: <k> PASS · <k> FAIL · <k> NOT-SCORED
Checks: <command → result> · OS review: <PASS | FAIL (rows)>
Verdict: PASS | ITERATE (<gap>) | BLOCKED (<blocker>, owner <name>)
Run record: 00_Agentic-OS/_runs/<YYYY-MM-DD>-<slug>.md
```

## Never

- Treat self-report as verification, or let rows go silently unscored.
- Weaken a check, lower a threshold, or add placeholders to pass a gate.
- Commit, push, publish, or change schedules without the user's request — commits go through `repo-steward`.
- Retry an unchanged failing strategy, or loop past the budget.
