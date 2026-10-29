# 04_learn/

**TL;DR:** Phase 4 — bring the evidence in, separate what we shipped from what we learned, update the beliefs it breaks, and choose one forward path.

**Workflow:** [W4 — Learn](../../../02_Workflows/workflows/W4-learn.md) (`02_Workflows/workflows/W4-learn.md`)

## What to capture here

- **Evidence brief** —
  [`4-1-Learn_evidence-brief.template.md`](../../../00_README/_templates/4-1-Learn_evidence-brief.template.md):
  what shipped vs. what we learned, metrics actuals, and the forward-path recommendation
- **Retro** — [`4-2-Learn_retro.template.md`](../../../00_README/_templates/4-2-Learn_retro.template.md): what
  worked, what didn't, at most five owned action items
- **Updated artifacts** — when evidence changes the research, personas, JTBD or journey, update them *in
  place* under `../01_understand/` and note the change and date here
- **Forward path** — iterate, ship wider, pivot or stop; the evidence brief normally carries the rationale

## Exit gate — Learn → Next

- [ ] Every claim is tagged `observed` / `reported` / `assumed`
- [ ] What-we-shipped and what-we-learned are separate sections
- [ ] Updated Understand artifacts say what changed and when
- [ ] One forward path is chosen, with an owner and the evidence behind it

Record the result in the hub README's [phase-gate table](../README.md#phase-gates). The forward path is always
explicit ([Traffic Light](../../../00_README/_frameworks/traffic-light-decisions.md#5-integration-with-the-4-phase-loop)): **🟢** chosen with the evidence cited, or **🔴** evidence inconclusive
or conflicting — a named owner gathers more signal (e.g., "two more weeks of adoption data, owner <name>") or
escalates. Don't park the forward path in 🟡.

## Decisions

A forward path that outlives the evidence brief, a wider release, or a retirement goes in
[`decisions/`](decisions/README.md) as a typed record. Phase closure alone needs no new decision file.

## Loop back

New questions about the problem send you back to [`../01_understand/`](../01_understand/README.md); new
solution directions send you back to [`../02_design/`](../02_design/README.md). Don't skip phases on the way
back.
