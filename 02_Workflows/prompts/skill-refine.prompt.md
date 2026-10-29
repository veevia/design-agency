---
description: "Self-improvement loop for a capability: read its past-run signals (eval results, lint findings, contract score, repeated reviewer frowns in run records) and propose ONE concrete refinement as a draft under _proposed/; never auto-applies, and stops when no real signal exists."
agent: agent
---

# /skill-refine

A skill should get sharper each time it is used, not drift. This prompt reads the signals the harness already produces and proposes one concrete refinement for the owner to accept.

## Inputs

- **skill** (optional): the slug to refine. Omit to sweep for the weakest signal and pick one.

## Procedure

1. **Load skills**: `rubric-authoring` (turn taste into a catchable rule), `extreme-clarity`.
2. **Gather existing signals only** — never fabricate:
   - evals: `python3 06_Engine/evals/run-evals.py <skill>` (when an eval exists)
   - lints: `python3 06_Engine/harness/lint-skill.py <skill> --severity info` (recurring findings)
   - contract: `python3 06_Engine/harness/lint-skill.py --contract <skill>`
   - repeated reviewer frowns in `00_Agentic-OS/_runs/*.md` for runs that loaded the skill
3. **Require at least one real signal.** If none shows a problem, print `no refinement warranted` and stop.
4. **Diagnose the single biggest weakness** — the most repeated frown, the failing eval, or the recurring lint.
5. **Propose one concrete refinement** — a named NEVER/ALWAYS rule, a tightened lint regex, a clearer `when_to_load`, a sharper "Use when" trigger, or a new eval fixture — as a draft at `03_Agents-and-Skills/Skills/_proposed/<slug>/SKILL.md`, with a one-line rationale citing the signal.
6. **Never apply it to the live skill.** `skill-agent-smith` applies an accepted proposal and re-runs the gates.

## Output format

```
=== /skill-refine (skill=<slug>) ===
Signals: evals <pass/fail/none> · lint <n findings> · contract <score> · frowns <n>
Biggest weakness: <one line, with the signal it came from>
Proposed refinement: <concrete rule or change> → 03_Agents-and-Skills/Skills/_proposed/<slug>/
```

## Guardrails

- At least one real signal — no manufactured problems.
- One refinement per run; never "make it better".
- Plug-in skills (for example the FDE Design Toolkit) are refined upstream with [`/plugin-optimize`](../../02_Workflows/prompts/plugin-optimize.prompt.md), never in the mount.

## See also

- SOP: [`skill-refine`](../../02_Workflows/SOPs/skill-refine/SOP.md) · [`/workflow-audit`](../../02_Workflows/prompts/workflow-audit.prompt.md) creates capabilities; this refines them
