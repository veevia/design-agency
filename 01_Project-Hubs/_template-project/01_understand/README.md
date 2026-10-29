# 01_understand/

**TL;DR:** Phase 1 — the problem space: who has the problem, what job they're trying to get done, and where today's journey fails, all backed by tagged evidence.

**Workflow:** [W1 — Understand](../../../02_Workflows/workflows/W1-understand.md) (`02_Workflows/workflows/W1-understand.md`)

## Artifacts

Copy a template here only when you start that artifact.

| Artifact | Template | Drafting prompt |
|---|---|---|
| Problem frame | [`1-0-Understand_problem-frame`](../../../00_README/_templates/1-0-Understand_problem-frame.template.md) | [`problem-framing`](../../../03_Agents-and-Skills/Skills/problem-framing/SKILL.md) skill |
| UX survey (optional, before interviews) | [`1-2-Understand_UX_survey`](../../../00_README/_templates/1-2-Understand_UX_survey.template.md) | — |
| UX research report | [`1-1-Understand_research-report`](../../../00_README/_templates/1-1-Understand_research-report.template.md) | `/research-synthesize` |
| Persona (1–3) | No template — synthesized from the research report | `/persona-draft` |
| JTBD analysis | [`1-3-Understand_jtbd`](../../../00_README/_templates/1-3-Understand_jtbd.template.md) | `/jtbd-draft` |
| JTBD synthesis (several domains) | [`1-3b-Understand_jtbd-synthesis`](../../../00_README/_templates/1-3b-Understand_jtbd-synthesis.template.md) | — |
| User journey map | [`1-4-Understand_journey-map`](../../../00_README/_templates/1-4-Understand_journey-map.template.md) | `/journey-map` |

Cross-functional input comes through the hub's `intake.md` (§C stakeholder map, §D async input form); W1
describes what each partner will see.

## Exit gate — Understand → Design

- [ ] The problem frame states the problem without a solution noun, and its readiness light is 🟢
- [ ] The research report has ≥3 findings, each tagged `observed` / `reported` / `assumed`
- [ ] At least one primary persona, citing research
- [ ] The JTBD statement fits "When … I want to … so I can …" in one sentence
- [ ] The journey map has an emotional arc and at least one moment of truth

Record the result in the hub README's [phase-gate table](../README.md#phase-gates): one light, one owner,
a link to the evidence. This gate is binary ([Traffic Light](../../../00_README/_frameworks/traffic-light-decisions.md#5-integration-with-the-4-phase-loop)): **🟢** the problem space is clear
enough to design against, or **🔴** not yet — a named blocker and unblock owner (e.g., "second interview
round outstanding"). Individual findings may carry 🟡 when confidence is low. Closing the phase needs no new
decision file.

## Decisions

Durable choices made here — research scope, which persona is primary, which pain points we prioritize — go
in [`decisions/`](decisions/README.md) only when later work must follow them.
