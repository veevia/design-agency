---
name: rubric-authoring
title: Turn taste into a rubric a reviewer can score
description: "Convert 'I know good when I see it' into a scoreable rubric in six steps — run a baseline, mine your frowns, group them into weighted dimensions, rewrite each as concrete NEVER/ALWAYS cases, add at least three diverse anchors, then bundle and calibrate against human judgment — so a reviewer agent can hold long-running subjective work to your bar. Use when a task is subjective (writing, design, UX, video, copy) and has no unit test, when building the rubric a goal-harness or reviewer will score against, or when AI output is technically fine but repeatedly misses your taste."
status: beta
narrative: 00_README/_frameworks/long-horizon-execution.md
when_to_load:
  - A task is subjective (writing, design, UX, video, copy) and has no unit test
  - Building the rubric that a goal-harness loop or reviewer agent will score against
  - AI output is "technically fine" but repeatedly misses your taste
  - You keep re-explaining the same corrections
  - Writing or reviewing an initiative's <slug>.rubric.md
applies-to: subjective work, reviewer rubrics, /optimize-loop initiatives, goal completion criteria
inputs:
  - kind: rubric
    where: "{00_Agentic-OS,01_Project-Hubs/[!_]*}/**/*.rubric.md"
outputs:
  - kind: rubric
    schema: "Markdown: weighted dimensions, each with concrete NEVER/ALWAYS cases a reviewer can catch at a glance, MUST/SHOULD levels, ≥3 diverse anchors on taste dimensions, and a calibration log"
done_when:
  - "A baseline of 5–10 real outputs was reviewed before the rubric was written"
  - "Every dimension carries concrete cases ('never splice clauses with em-dashes'), not abstractions ('avoid AI flavour')"
  - "Dimensions are weighted toward the model's known weak spots and each row says MUST or SHOULD"
  - "At least one taste dimension offers three or more diverse anchors"
  - "The rubric was calibrated — reviewer verdicts compared with a human's for at least three rounds and revised on mismatch"
lints:
  - id: rubric-abstraction-without-case
    severity: warning
    where: "{00_Agentic-OS,01_Project-Hubs/[!_]*}/**/*.rubric.md"
    pattern: "(?i)^[-*].*\\b(avoid|ensure|keep it|make it)\\b.*\\b(good|clean|tasteful|professional|modern|original|nice)\\b"
    message: "Rubric line is abstract — replace it with a concrete NEVER/ALWAYS case the reviewer can catch at a glance."
  - id: rubric-single-anchor-overfit
    severity: info
    where: "{00_Agentic-OS,01_Project-Hubs/[!_]*}/**/*.rubric.md"
    pattern: "(?i)museum-grade|museum-quality|world-class"
    message: "Single-anchor phrasing overfits (everything becomes a museum) — offer three or more diverse directions."
budget:
  context_tokens_max: 2500
loads: [goal-harness]
---

# Rubric Authoring

**TL;DR:** A long-running loop is only as good as its rubric, so build it from real outputs you frowned at, write every line as a concrete NEVER/ALWAYS case, and calibrate it against your own eyes before trusting it.

## When to use

- The work is subjective and nothing like a unit test exists.
- A `goal-harness` loop or `/optimize-loop` run needs a reviewer bar.
- You find yourself giving the same correction for the third time.

## Steps

1. **Baseline first.** Run the task 5–10 times without guidance. You are measuring the model's default, not grading yet.
2. **Mine your frowns.** Review every output and write down each frown with its exact reason ("no hook in the opening", "uses a gradient on a white card").
3. **Group frowns into dimensions** (for writing: logic, voice, hook; for UI: design quality, originality, craft, usability) and weight them toward the model's known weak spots.
4. **Rewrite each dimension as concrete cases** — "**Never** use the 'not A, but B' construction", "**Always** generate empty, loading, and error states". Mark each row MUST or SHOULD.
5. **Add diverse anchors** — at least three directions (for example *editorial · brutalist · industrial*) so the model picks per situation instead of converging on one look.
6. **Bundle and calibrate.** Hand the rubric to the reviewer; for the first 3–4 rounds compare its verdict with your own. A mismatch means the rubric hasn't captured your standard — revise it. Log each calibration round.

Score what the user sees: for rendered artifacts (prototypes, decks, storyboards), the reviewer scores a screenshot from a real browser (`04_MCP/playwright/`), not the source.

## Output format

Copy [`assets/rubric.template.md`](assets/rubric.template.md) to `<slug>.rubric.md` beside its goal. Each row is reviewer-checkable:

```markdown
| ID | Level | Case | How the reviewer checks |
|---|---|---|---|
| V1 | MUST | Never open with "In today's fast-changing world" | First sentence |
| S2 | MUST | Non-goals list names ≥3 out-of-scope items | Count bullets under "Non-goals" |
| O3 | SHOULD | Pick one of: editorial · brutalist · industrial | Screenshot matches one anchor |
```

## Watch-outs

- **Writing the rubric before the baseline** codifies imagined problems.
- **Abstractions** ("be original") are uncheckable; the `rubric-abstraction-without-case` lint flags them.
- **A single anchor** ("museum-grade") makes everything look the same.
- **Skipping calibration** produces a confidently wrong reviewer.
- **Never-ending rubrics** — keep MUST rows few and decisive; move nice-to-haves to SHOULD.

## See also

- `goal-harness` (the loop that consumes the rubric) · `extreme-clarity` · `evidence-tagging`
- Agent: [`goal-runner.agent.md`](../../../03_Agents-and-Skills/Agents/goal-runner.agent.md) · Prompts: [`/optimize-loop`](../../../02_Workflows/prompts/optimize-loop.prompt.md), [`/skill-refine`](../../../02_Workflows/prompts/skill-refine.prompt.md)
- Sprint methods with related craft: [`design-criteria`](../design-criteria/SKILL.md), [`success-metrics`](../success-metrics/SKILL.md)
- Framework: [`00_README/_frameworks/long-horizon-execution.md`](../../../00_README/_frameworks/long-horizon-execution.md)
