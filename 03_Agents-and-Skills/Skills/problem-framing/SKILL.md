---
name: problem-framing
title: Frame the problem before designing anything
description: "Produce a Problem Frame — the pre-research artifact that grounds an engagement in the people-problem (no solution nouns), the decisions the product must enable, the gap between what stakeholders want and what is feasible, a known/unknown data map, a named stakeholder alignment map, and a readiness Traffic Light. Use when starting a new engagement or workstream where stakeholders are naming solutions ('we want an agent / a dashboard') before the problem is grounded, before authoring any research report, persona, or JTBD on a fresh problem space, or when a build keeps circling the same question and the problem was never framed."
status: beta
when_to_load:
  - Starting a new engagement or workstream where stakeholders name solutions before a problem is grounded
  - Before authoring any Understand-phase artifact (research report, persona, JTBD) on a fresh problem space
  - A build keeps circling the same question and the problem may never have been framed (pairs with drift-check)
  - Preparing an alignment readout with sponsors before discovery with subject-matter experts
applies-to: the front gate of W1 — Understand; filed in <hub>/01_understand/
narrative: 00_README/_frameworks/design-thinking-loop.md
inputs:
  - kind: context-intake
    where: "01_Project-Hubs/*/00_context_intake/**/*"
  - kind: wiki-source
    where: "01_Project-Hubs/*/_wiki/sources/**/*.md"
outputs:
  - kind: problem-frame
    schema: "01_Project-Hubs/<hub>/01_understand/<YYYY-MM-DD>-<slug>-problem-frame.md with TL;DR, Problem statement (no solution nouns), Decisions to enable, Feasibility gap, Known/unknown data map, Stakeholder alignment map, readiness light"
done_when:
  - The problem statement is in the user's language and proposes no solution noun (agent, dashboard, ontology, platform, app, model)
  - A 'Decisions to enable' section lists the decisions the product must let a user make, with who, cadence, and data today
  - A 'Feasibility gap' section names what stakeholders want versus what is achievable now, and the overlap
  - Every non-trivial claim carries an evidence tag
  - The frame closes with a readiness Traffic Light; a Yellow has trigger and expiry
lints:
  - id: problem-statement-names-a-solution
    severity: info
    where: "01_Project-Hubs/[!_]*/01_understand/**/*-problem-frame.md"
    pattern: "(?i)^##+\\s*problem statement"
    message: "Problem Frame detected — confirm the Problem statement names a people-problem, not a solution; run scripts/check_frame.py for the negation-aware check."
  - id: frame-missing-decisions-to-enable
    severity: error
    where: "01_Project-Hubs/[!_]*/01_understand/**/*-problem-frame.md"
    pattern: "^#\\s"
    must_also_match: "(?i)decisions to enable"
    message: "A Problem Frame must declare the decisions the product must enable — design backward from the decision, not forward from the feature."
  - id: frame-missing-feasibility-gap
    severity: error
    where: "01_Project-Hubs/[!_]*/01_understand/**/*-problem-frame.md"
    pattern: "^#\\s"
    must_also_match: "(?i)feasibility gap"
    message: "A Problem Frame must name the want-versus-achievable gap."
  - id: frame-missing-readiness-light
    severity: error
    where: "01_Project-Hubs/[!_]*/01_understand/**/*-problem-frame.md"
    pattern: "^#\\s"
    must_also_match: "(?i)\\blight:\\s*(green|yellow|red)\\b"
    message: "A Problem Frame must close with a readiness Traffic Light (light: green | yellow | red)."
budget:
  context_tokens_max: 2500
loads: [evidence-tagging, traffic-light-decisions, house-principles, alignment-playbook]
---

# Problem Framing

**TL;DR:** Before any persona or JTBD, write a Problem Frame that names the people-problem in the user's words, the decisions the product must enable, and the gap between what is wanted and what is feasible — then decide whether research can start.

## When to use

- Stakeholders say "week one an agent, week two a dashboard" before anyone has grounded the problem.
- A fresh problem space is about to get research, personas, or JTBDs.
- A build keeps circling the same question (`drift-check` found it).

## Steps

1. **Read the intake end to end**: `<hub>/00_context_intake/` and any `_wiki/sources/`. Tag what you extract (`evidence-tagging`).
2. **Write the problem statement in the user's words** with no solution nouns. You may mention a solution only to disclaim it ("this is a connection problem, not a missing-tool problem").
3. **Inventory the decisions to enable**: for each, who makes it, how often, with what data today. A decision with no current data source is a known-unknown.
4. **Name the feasibility gap**: what stakeholders want, what is achievable with today's data and platform, and the overlap you will design for.
5. **Map known/unknown data** (known-known, known-unknown, unknown-unknown) and **stakeholder alignment** by name (`alignment-playbook`).
6. **Close with readiness**: 🟢 grounded → start research · 🟡 grounded with conditions (trigger + expiry) · 🔴 not ready (blocker + unblock owner).
7. **Validate**: `python3 03_Agents-and-Skills/Skills/problem-framing/scripts/check_frame.py <frame>` and `python3 06_Engine/harness/lint-skill.py problem-framing`.

## Output format

Copy [`assets/problem-frame.template.md`](assets/problem-frame.template.md) to `<hub>/01_understand/<YYYY-MM-DD>-<slug>-problem-frame.md`. Sections: TL;DR · Problem statement · Decisions to enable · Feasibility gap · Known/unknown data map · Stakeholder alignment map · Readiness to research (with `light:` in front-matter).

It chains forward: personas and JTBDs earn their keep against the decisions to enable; the POV takes a position on the feasibility gap; the PRD scopes to the decisions.

## Watch-outs

- **Solution in the problem statement** ("users need a dashboard") — name the decision they can't make today instead.
- **Skipping to personas** — strategy and problem-grounding come first.
- **Empty feasibility gap** — if everything is achievable, you haven't found the constraints.
- **Features instead of decisions** — a list of features inverts the design direction.
- **🟡 without trigger and expiry** — a green in hiding or a red in denial.

## See also

- Reference: [`references/REFERENCE.md`](references/REFERENCE.md) — section-by-section guide and a fictional worked example
- Validator: [`scripts/check_frame.py`](scripts/check_frame.py) (negation-aware solution-noun rule)
- `design-thinking-loop` (this is the Frame → Understand gate) · `drift-check` · `alignment-playbook` · `evidence-tagging`
- Workflow: [W1 — Understand](../../../02_Workflows/workflows/W1-understand.md), Step 0
