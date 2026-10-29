---
id: capability-spot
title: Capability spotter — close the self-evolution loop
status: beta
trigger: "End of a week or milestone, after three or more session snapshots or run records accumulate, or on demand"

owner_agent: none — human-driven
loads_skills:
  - wiki-maintenance
  - extreme-clarity
invokes_prompts:
  - capability-spot

produces_artifacts:
  - "02_Workflows/SOPs/_proposed/<id>/SOP.md"
  - "03_Agents-and-Skills/Skills/_proposed/<slug>/SKILL.md"
  - "00_Agentic-OS/OPTIMIZATION-BACKLOG.md entries"

inputs:
  - kind: lookback-days
  - kind: optional-hub-scope
outputs:
  - kind: proposal-stubs
    location: "02_Workflows/SOPs/_proposed/ and 03_Agents-and-Skills/Skills/_proposed/"

done_when:
  - "Every session snapshot and run record in the lookback window was read"
  - "Each pattern observed three or more times has exactly one proposal citing its evidence"
  - "Existing backlog rows and proposals were linked, not duplicated"
  - "Nothing was graduated; proposals wait in _proposed/ for the owner"

context_budget_tokens_max: 8000
---

# SOP — Capability spotter

## TL;DR
Scan recent session snapshots, run records, and the backlog for patterns seen three or more times; draft one proposal per pattern; the owner decides.

## When to run
- End of a week or milestone
- After three or more session snapshots accumulate
- When the workspace seems to repeat a workflow ad hoc

## Inputs
- Lookback window in days (default 7)
- Optional hub scope

## Procedure

1. **Invoke** `/capability-spot [lookback=7] [hub=<slug>]`.
2. **Review** each proposal with its evidence links.
3. **Decide** per proposal: approve (hand to `skill-agent-smith` to draft and gate), reject (close with a reason), or defer (leave in `_proposed/`).

## Outputs
- Stubs in `02_Workflows/SOPs/_proposed/` and `03_Agents-and-Skills/Skills/_proposed/`
- Rows in `00_Agentic-OS/OPTIMIZATION-BACKLOG.md`

## Done when
See front-matter.

## Failure modes
- **Nothing to surface:** a valid outcome — print "No new patterns" and stop.
- **More than five proposals:** raise the frequency threshold to four or five and re-run.

## See also
- [`/capability-spot`](../../prompts/capability-spot.prompt.md) · [`session-snapshot`](../session-snapshot/SOP.md) (produces the snapshots) · [`workflow-audit`](../workflow-audit/SOP.md) (the forward-looking half)
- [OS backlog](../../../00_Agentic-OS/OPTIMIZATION-BACKLOG.md)
