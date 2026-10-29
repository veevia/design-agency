---
name: house-principles
title: Gut-check work against seven design principles
description: "Pressure-test any synthesis, POV, brief, PRD, or decision rationale against seven working principles (this OS's house principles) — have a point of view, solve the right problem first, rigor compounds, evidence over opinion, clarity is a craft, defaults are decisions, surface disagreement. Use when drafting or reviewing a synthesis, POV, brief, PRD, or decision rationale, when reviewing a settings, configuration, or onboarding design (a default is a decision), or when checking that a multi-stakeholder page surfaced real disagreement."
status: stable
when_to_load:
  - Drafting or reviewing any synthesis, POV, brief, PRD, or decision rationale
  - Reviewing a settings, configuration, or onboarding design (the default is a decision)
  - Checking whether a multi-stakeholder page surfaced real disagreement
  - Coaching a draft before it goes to stakeholders
applies-to: syntheses, decision rationale, design POVs, briefs, PRDs, retros
narrative: 00_README/_frameworks/house-principles.md
inputs:
  - kind: synthesis
    where: "01_Project-Hubs/*/_wiki/syntheses/**/*.md"
  - kind: design-artifact
    where: "01_Project-Hubs/*/02_design/**/*.md"
outputs:
  - kind: principle-checked-page
    schema: "Page carries an explicit 'Point of view' statement, names its defaults where applicable, and records disagreement by name"
done_when:
  - Synthesis and POV pages carry an explicit point-of-view statement
  - Settings, configuration, and onboarding artifacts name their default and why
  - Multi-stakeholder topics record disagreement with names, not silence
  - Each principle that fails the gut-check produces one concrete revision, not a general comment
lints:
  - id: laundered-consensus
    severity: warning
    where: "01_Project-Hubs/[!_]*/_wiki/{syntheses,entities}/**/*.md"
    pattern: "(?i)\\b(some stakeholders|the team feels|everyone agrees|we all agree)\\b"
    message: "Laundered consensus — replace 'some stakeholders / the team / everyone' with named positions (principle 7)."
  - id: synthesis-without-pov
    severity: warning
    where: "01_Project-Hubs/[!_]*/_wiki/syntheses/**/*.md"
    pattern: "^#\\s"
    must_also_match: "(?i)point of view|\\bPOV\\b"
    message: "Synthesis has no 'Point of view' — take a position (principle 1)."
budget:
  context_tokens_max: 1500
---

# House principles

**TL;DR:** Seven opinions that sharpen design work — use them as a gut-check that produces one concrete revision per failed principle, not as a compliance checklist.

The principles started as one designer's working rules and are shared here as a reusable craft lens; adapt the wording to your team.

## When to use

- A synthesis, POV, brief, PRD, or rationale is about to be shared.
- A settings or onboarding design is under review.
- A page involves several stakeholders and reads as unanimous.

## Steps

1. Read the draft once for meaning, then run each principle's question:

   | # | Principle | Ask |
   |---|---|---|
   | 1 | **Have a point of view** | What do we believe, and what would change our mind? |
   | 2 | **Solve the right problem first** | What is the user hiring this for, in their words? |
   | 3 | **Rigor compounds** | Which sloppy input is producing sloppy output? |
   | 4 | **Evidence over opinion** | What breaks if this assumption is wrong? (`evidence-tagging`) |
   | 5 | **Clarity is a craft** | Could a cross-functional reader repeat this back? (`extreme-clarity`) |
   | 6 | **Defaults are decisions** | What does "do nothing" produce, and is that right? |
   | 7 | **Surface disagreement** | If everyone agrees, what haven't we said? (`alignment-playbook`) |

2. For each failed principle, write one concrete revision ("add a Point of view: we will not buy a single vendor").
3. Apply the revisions or hand them back as review comments.

## Output format

On synthesis, POV, and decision pages (template: [`assets/synthesis-page.template.md`](assets/synthesis-page.template.md)):

```markdown
## Point of view
<one sentence — principle 1>

## Rationale
- <claim> [observed | <source>] — principle 4

## Disagreement heard
- <Name (role)>: <position> — principle 7
```

## Watch-outs

- A POV that any product could adopt is a vision statement, not a position.
- Solution talk before the problem is framed fails principle 2 — route to `problem-framing`.
- An unstated default is still a decision; name it.
- Agreement nobody was asked to challenge is compliance, not alignment.

## See also

- Framework: [`00_README/_frameworks/house-principles.md`](../../../00_README/_frameworks/house-principles.md)
- `evidence-tagging` · `extreme-clarity` · `alignment-playbook` · `problem-framing`
