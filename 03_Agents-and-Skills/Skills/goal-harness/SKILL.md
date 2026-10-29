---
name: goal-harness
title: Structure a long-running task as a five-element goal
description: "Turn a fuzzy task into a goal with five elements — a concrete outcome, a verification that proves it, constraints that fence the scope, an iteration policy, and error handling — plus a rubric, then run it as an executor-reviewer loop that stops only when the rubric passes or a stop condition fires. Use when a task will run longer than 30 minutes or across many iterations unattended, when using a /goal, Ralph-loop, or executor/reviewer pattern, when an agent keeps finishing early with output you don't want, or when writing an initiative's .goal.md."
status: beta
narrative: 00_README/_frameworks/long-horizon-execution.md
when_to_load:
  - A task will run longer than 30 minutes or across many iterations without supervision
  - Using a /goal, Ralph-loop, or executor/reviewer agent pattern
  - An agent keeps "finishing early" with output you don't want
  - Writing or reviewing a <slug>.goal.md for an optimization initiative
applies-to: long-running autonomous tasks, optimization initiatives, /optimize-loop runs, scheduled jobs that must reach a real completion bar
inputs:
  - kind: goal
    where: "{00_Agentic-OS,01_Project-Hubs/[!_]*}/**/*.goal.md"
outputs:
  - kind: goal-block
    schema: "A .goal.md whose front-matter declares outcome, verification, constraints, iteration_policy, error_handling, and rubric (path to a .rubric.md)"
done_when:
  - "The goal declares all five elements: outcome, verification, constraints, iteration_policy, error_handling"
  - "The outcome is a concrete target state (a number, threshold, or observable), not an adjective"
  - "Verification names a check that proves done — a tool, a test, or a rubric pass — never self-report"
  - "Constraints name what must not change; error handling says when to pause and report"
  - "A reviewer scores every round against the rubric before the loop may stop"
lints:
  - id: goal-outcome-is-adjective
    severity: error
    where: "{00_Agentic-OS,01_Project-Hubs/[!_]*}/**/*.goal.md"
    pattern: "^outcome:\\s*[\"']?(make it )?(better|nicer|cleaner|good|great|improved)\\b"
    message: "Outcome must be a concrete target state with a number, threshold, or observable — not an adjective like 'better'."
  - id: goal-missing-verification
    severity: error
    where: "{00_Agentic-OS,01_Project-Hubs/[!_]*}/**/*.goal.md"
    pattern: "^outcome:\\s*\\S"
    must_also_match: "^verification:\\s*\\S"
    message: "Every goal with an outcome must declare verification — how we prove it is done (tool, test, or rubric), not self-report."
  - id: goal-missing-error-handling
    severity: warning
    where: "{00_Agentic-OS,01_Project-Hubs/[!_]*}/**/*.goal.md"
    pattern: "^outcome:\\s*\\S"
    must_also_match: "^error_handling:\\s*\\S"
    message: "Long-running goals should declare error_handling — when to pause and report instead of looping."
budget:
  context_tokens_max: 2500
loads: [rubric-authoring, traffic-light-decisions]
---

# Goal Harness

**TL;DR:** A long-running agent stops when an external reviewer says the rubric passes or a declared stop condition fires — never when it feels done — so every goal states five elements and a rubric before the loop starts.

## When to use

- The task is long, iterative, or unattended (an optimization initiative, a backfill, a design polish loop).
- "Make it better" is all you have — the harness forces a real definition of done first.
- An earlier run quit early or declared victory after two small edits.

## Steps

1. **Write the five elements** (template: [`assets/goal.template.md`](assets/goal.template.md)):

   ```yaml
   outcome:          # concrete target STATE — a number, threshold, or observable; never "better"
   verification:     # how we PROVE it — a tool run, a test, a rubric pass; never self-report
   constraints:      # what must NOT change — the scope fence
   iteration_policy: # what to log between attempts — {what changed, measured result, next-best idea}
   error_handling:   # when to PAUSE and REPORT (tool won't run, ideas exhausted, needs a human)
   rubric:           # path to the .rubric.md the reviewer scores against (rubric-authoring)
   ```

2. **Refuse a boundary-less goal.** If the outcome is an adjective or verification is missing, ask for the missing piece before looping.
3. **Run the loop**: the executor produces output; the reviewer scores every rubric row and runs the verification each round. Not met → name the specific gap and iterate. Met → stop.
4. **Use a tri-state verdict**: `PASS` (every MUST row green) · `ITERATE` (work remains the agent can do) · `BLOCKED` (only externally gated rows remain red). BLOCKED stops the loop.
5. **Pause and report** per `error_handling`: a stuck run is a 🔴 with a named blocker and unblock owner — never a silent give-up or a fake "done".
6. **Calibrate** on a new rubric: for the first 3–4 rounds a human compares the reviewer's verdict with the artifact; a mismatch means the rubric needs revising (`rubric-authoring`).
7. **Lint** goal files: `python3 06_Engine/harness/lint-skill.py goal-harness`.

## Output format

Initiative goals live at `00_Agentic-OS/initiatives/<slug>/<slug>.goal.md` with a sibling `<slug>.rubric.md`; project goals live beside the work in a hub. A worked contrast:

- ❌ "Make this project better." → two tiny edits and a victory lap.
- ✅ "Checkout responds in ≤ 0.2 s, measured by the speed-test tool over 5 runs; change only the checkout block and its tests; log change / measurement / next idea each try; if the tool won't run or ideas run out, stop and report what was tried, where it's stuck, and what you need."

## Watch-outs

- **Self-report is not verification.** "I improved it" must become a tool, test, or rubric pass.
- **No rubric on subjective work** lets the model grade its own homework.
- **The reviewer must score the whole rubric** — or print `NOT-SCORED (reason)` for each skipped row.
- **Iteration is not monotonic.** Round 10 can beat round 15; keep the best artifact, not the latest.
- **Looping forever.** Without `error_handling`, a blocked goal burns budget.

## See also

- Reference: [`references/REFERENCE.md`](references/REFERENCE.md) — why agents quit early, field-tested pitfalls, sources
- `rubric-authoring` (the rubric this loop scores against) · `traffic-light-decisions` (a stuck report is a 🔴)
- Agent: [`goal-runner.agent.md`](../../../03_Agents-and-Skills/Agents/goal-runner.agent.md) · Prompt: [`/optimize-loop`](../../../02_Workflows/prompts/optimize-loop.prompt.md)
- Framework: [`00_README/_frameworks/long-horizon-execution.md`](../../../00_README/_frameworks/long-horizon-execution.md)
