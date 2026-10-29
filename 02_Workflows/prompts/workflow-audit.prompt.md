---
description: "Proactively elicit the manual workflows you repeat (three or more times) and route each to a skill, SOP, automation, or leave-manual, drafting proposals under _proposed/ — the forward-looking complement to /capability-spot."
agent: agent
---

# /workflow-audit

Where `/capability-spot` mines the past for repeated patterns, `/workflow-audit` asks forward: "what do you do by hand, over and over, that is not codified yet?" Then it routes each answer to the right home.

## Inputs

- **period** (optional, default "this week"): the window to reason over
- **hub** (optional): scope to one hub; omit for the whole workspace

## Procedure

1. **Load skills**: `extreme-clarity` (name each workflow concretely) and `goal-harness` (shape an automation's definition of done).
2. **Elicit repeated outputs.** Ask: "What did you produce three or more times this period by hand that has no skill, SOP, prompt, or automation?" Prompt with categories: drafting, synthesis, setup and scaffolding, review, data pulls, stakeholder updates, plug-in runs.
3. **Filter to three or more occurrences** — two is not a pattern.
4. **Route each to exactly one**: `skill` (a specific output made a specific way) · `SOP` (multi-step orchestration) · `automation` (a script or scheduled job) · `leave-manual` (too rare or variable) — with a one-line reason.
5. **De-duplicate** against [the OS backlog](../../00_Agentic-OS/OPTIMIZATION-BACKLOG.md), the catalog [`03_Agents-and-Skills/INDEX.md`](../../03_Agents-and-Skills/INDEX.md), and existing `_proposed/` stubs — link, never re-file.
6. **Draft stubs** for to-codify items: `02_Workflows/SOPs/_proposed/<id>/SOP.md` or `03_Agents-and-Skills/Skills/_proposed/<slug>/SKILL.md`. Never auto-graduate.

## Guardrails

- Minimum frequency: 3. One proposal per candidate.
- Stubs stay in `_proposed/` until the owner moves them.
- Defer to `/capability-spot` for anything already mined from evidence.

## Output format

```
=== /workflow-audit (period=<window>, hub=<scope>) ===
Repeated workflows named: <n>
Routed: <k> skill · <k> SOP · <k> automation · <k> leave-manual
Proposals drafted: <n> (in _proposed/) · deferred to capability-spot: <n>
```

## See also

- SOP: [`workflow-audit`](../../02_Workflows/SOPs/workflow-audit/SOP.md) · [`/capability-spot`](../../02_Workflows/prompts/capability-spot.prompt.md)
