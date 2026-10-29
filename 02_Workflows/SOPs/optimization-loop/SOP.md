---
id: optimization-loop
title: Optimization loop — goal plus rubric to a verified result
status: beta
trigger: "A ranked item in 00_Agentic-OS/OPTIMIZATION-BACKLOG.md, an initiative cycle, or a plug-in improvement is ready to work"

owner_agent: goal-runner
sub_agents:
  - skill-agent-smith
  - repo-steward
loads_skills:
  - goal-harness
  - rubric-authoring
  - evidence-tagging
  - extreme-clarity
  - traffic-light-decisions
invokes_prompts:
  - optimize-loop
  - plugin-optimize

produces_artifacts:
  - "00_Agentic-OS/_runs/<YYYY-MM-DD>-<slug>.md"
  - "00_Agentic-OS/OPTIMIZATION-BACKLOG.md (updated row)"

inputs:
  - kind: goal and rubric
    where: "00_Agentic-OS/initiatives/<initiative>/*.goal.md and *.rubric.md"
  - kind: backlog item
    where: "00_Agentic-OS/OPTIMIZATION-BACKLOG.md"
outputs:
  - kind: run record
    location: "00_Agentic-OS/_runs/"

done_when:
  - "The acceptance and baseline were recorded before any change"
  - "Every rubric row was scored PASS, FAIL, or NOT-SCORED with a reason"
  - "`python3 00_Agentic-OS/agentic-os-review.py` exits 0 (every MUST row passes) and no new regression remains"
  - "A dated run record holds the baseline, change, exact paths, checks, verdict, and rollback; the backlog row is updated"
  - "The verdict is PASS, or BLOCKED with a named blocker, resume step, and unblock owner"

context_budget_tokens_max: 8000
narrative_link: ../../../00_Agentic-OS/initiatives/README.md
---

# SOP — Optimization loop

## TL;DR
Work one backlog item or initiative cycle as analyze → plan → draft → evaluate → test → record, repeating until the rubric passes or a stop condition fires — proven by the OS review, never by self-report.

## When to run
- A backlog item is ranked and ready.
- A standing initiative (OS optimization or plug-in optimization) is due for a cycle.
- A capability or plug-in needs a measured improvement rather than an ad-hoc edit.

## Inputs
- The initiative's goal and rubric
- One backlog item (or the highest-ranked open one)

## Procedure

1. **Analyze** the goal, rubric, backlog row, and prior run records (`goal-runner`, `/optimize-loop`).
2. **Plan**: state the acceptance; capture the baseline commands and results.
3. **Draft** the smallest complete change inside the goal's constraints. For plug-ins, change the plug-in's own repository via `/plugin-optimize` — never the mount.
4. **Evaluate** every rubric row.
5. **Test**: re-run the baseline commands, targeted tests, and `python3 00_Agentic-OS/agentic-os-review.py`.
6. **Record** the run in `00_Agentic-OS/_runs/<YYYY-MM-DD>-<slug>.md`; update the backlog row.
7. **Repeat or stop**: ITERATE (name the gap), PASS (deliver), BLOCKED (report as 🔴 with the resume step).

## Outputs
- A run record per cycle and an updated backlog row

## Done when
See front-matter.

## Failure modes
- **No measurable outcome in the goal:** stop and ask for one before changing anything.
- **Same failing strategy twice:** change the hypothesis or stop as BLOCKED.
- **A new regression:** fix it or revert before recording PASS.
- **A human gate (publishing, promotion, approvals):** stop; the authorized human decides.

## See also
- [`/optimize-loop`](../../prompts/optimize-loop.prompt.md) · [`/plugin-optimize`](../../prompts/plugin-optimize.prompt.md) · agent [`goal-runner`](../../../03_Agents-and-Skills/Agents/goal-runner.agent.md)
- [Initiatives](../../../00_Agentic-OS/initiatives/README.md) · [Backlog](../../../00_Agentic-OS/OPTIMIZATION-BACKLOG.md) · [Run records](../../../00_Agentic-OS/_runs/README.md)
