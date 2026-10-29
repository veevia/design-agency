---
title: Long-horizon execution — the discipline of agents that don't quit
type: framework
status: draft
owner: OS steward
last-updated: 2026-10-29
source: A public talk on `/goal` loops (2026) + Anthropic's context-engineering research, reconciled with this OS's engine conventions
tags: [type/framework, purpose/build, status/draft, loop/all]
---

# Long-horizon execution — the discipline of agents that don't quit

> **TL;DR:** Long agent runs fail from *context anxiety* and succeed through *evaluation* — structure the goal, turn taste into a scoreable rubric, and let a reviewer hold the executor to it until the result is verified, not merely claimed.

A house framework for running long, multi-step agent work to a real finish. It is the narrative companion to the
[`goal-harness`](../../03_Agents-and-Skills/Skills/goal-harness/SKILL.md) and
[`rubric-authoring`](../../03_Agents-and-Skills/Skills/rubric-authoring/SKILL.md) skills, the
[Goal Runner](../../03_Agents-and-Skills/Agents/goal-runner.agent.md) agent, and the engine's
[evals](../../06_Engine/evals/README.md).

## The thesis

Long-running autonomy fails for one reason, and succeeds for one reason.

- **It fails because of *context anxiety*.** An LLM watches its own context window fill and,
  sensing it's nearly full, rushes to wrap up and quits — even mid-task, even claiming false completion.
  This is structural laziness ("clock-out mentality"), not a prompt defect.
- **It succeeds because of *evaluations*.** Not prompt engineering, not context engineering — the lever is
  whether *you* can define "good" precisely enough that an **external reviewer agent** can hold an
  **executor agent** to it, round after round, until the goal is truly met.

Everything else is mechanism around those two facts.

## The mental model: manager, not collaborator

You stop being the AI's *collaborator* (you ask, it answers, you re-steer every 10 minutes — your
attention stays captive) and become its *manager* (you define the bar and the stop condition; it runs to
completion; the task leaves *your* head). Real automation isn't moving a task from your hands to the AI's —
it's moving it off your **mind**. An unfinished task you're still tracking consumes attention whether or
not you're working on it. Attention is the scarce resource this discipline buys back.

## The two halves

1. **Structure the goal** (`goal-harness`) — a fuzzy task becomes 5 explicit elements: **outcome, verification,
   constraints, iteration policy, error handling.** "Done" gets a boundary, a proof, a fence, a per-round
   behavior, and a pause condition.
2. **Score the taste** (`rubric-authoring`) — for subjective work with no unit test, a short procedure turns "I know it when I
   see it" into concrete, scoreable reference cases an evaluator can enforce: a **rubric**.

The loop (the Goal Runner agent) runs them: implementer produces → reviewer scores against the rubric and runs the verification →
gap? iterate. Met? stop. Blocked? pause and report a 🔴 with a named blocker (never a fake "done").

## Why iteration beats single-shot

Quality climbs **non-monotonically** across rounds — round 10 can beat round 15 — but as the
reviewer↔executor dialogue continues, complexity and ambition rise until a **leap** appears that no single
prompt could have produced (Anthropic describes a run that reimagined a 2D museum page as a walkable 3D
room around iteration 10). The loop is a creativity engine, not just a quality ratchet — *if* the rubric
keeps pushing.

## The deeper payoff

Writing the rubric is ostensibly for the AI, but it forces **you** to externalize the fuzzy taste that
only ever lived in your head. Once it's text, the AI guards it and executes it at scale — and you've
captured a reusable asset (a skill) instead of re-explaining the same corrections forever. This is the
flywheel: every long task you harness leaves behind a rubric that makes the next one cheaper.

## Connections to the other frameworks

- **[Traffic Light decisions](traffic-light-decisions.md)** — a stuck report is a 🔴 with a named blocker
  and unblock owner; a calibrated "ship it" is a 🟢. Same discipline, applied to the loop's stop condition.
- **[Evidence tagging](house-principles.md#4-evidence--opinion-but-evidence-is-rare)** — "verification, not self-report" is the same rule as "observed > reported"; a
  rubric pass is `observed`, an agent's "I think it's done" is `assumed`.
- **[Extreme clarity](extreme-clarity.md)** — concrete reference cases over abstractions is
  clarity-as-craft for taste.
- **[House principles](house-principles.md)** — §1 (have a POV) is the rubric author's stance; §4 (evidence > opinion) is
  verification; §6 (defaults are decisions) is why "make it better" silently ships the model's default
  definition of done.
- **The engine** — a rubric *is* a set of `done_when` assertions made checkable; `06_Engine/evals/` and
  the skill linter are the reviewer for skills themselves. Git history and run folders under
  `00_Agentic-OS/_runs/` make every iteration reviewable and reversible.

## See also

- [Agentic-OS operating guide](../../00_Agentic-OS/README.md) — the task procedure these loops plug into
- [Initiatives](../../00_Agentic-OS/initiatives/README.md) — where long-running OS goals (`*.goal.md`) live
- [Capability catalog](../../03_Agents-and-Skills/INDEX.md) — related skills and agents
- [Anthropic — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
