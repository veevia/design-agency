---
type: goal
slug: <slug>
owner: <one named person>
status: active                 # active | paused | done | stopped
outcome: <concrete target STATE — a number, threshold, or observable; e.g. "all MUST rows of <slug>.rubric.md pass">
verification: <how we PROVE it — e.g. "python3 00_Agentic-OS/agentic-os-review.py exits 0 and the reviewer scores every rubric row">
constraints: <what must NOT change — e.g. "touch only 02_Workflows/prompts/; no edits inside plug-in mounts">
iteration_policy: <what to log between attempts — "append {what changed, measured result, next-best idea} to the run evidence">
error_handling: <when to PAUSE and REPORT — "if a check cannot run, ideas are exhausted, or a human decision is needed, stop and report">
rubric: ./<slug>.rubric.md
budget: <optional cap — e.g. "max 8 rounds or 2 hours">
---
# <Initiative or task name> — goal

**TL;DR:** <one sentence — the outcome and how it is proven>.

## Context anchor

<what each round re-reads before acting: the brief, the baseline measurement, the files in scope>

## Baseline

<the measured starting point — a number, a failing check, or the current rubric score>

## Stop conditions

- PASS: every MUST row in the rubric is green and the verification passes.
- BLOCKED: only externally gated rows remain red, or `error_handling` fires — stop and report as 🔴.
- Budget spent: stop, report the best artifact so far and the gap.

<!--
  VALIDATE: python3 06_Engine/harness/lint-skill.py goal-harness --severity error
-->
