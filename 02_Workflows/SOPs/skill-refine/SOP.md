---
id: skill-refine
title: Skill refine — turn past-run signals into one better rule
status: beta
trigger: "A capability repeatedly under-performs (a failing eval, a recurring lint finding, or a repeated reviewer frown in run records), or alongside a periodic capability review"

owner_agent: skill-agent-smith
loads_skills:
  - rubric-authoring
  - extreme-clarity
invokes_prompts:
  - skill-refine

produces_artifacts:
  - "03_Agents-and-Skills/Skills/_proposed/<slug>/SKILL.md (refined draft)"
  - "a one-line rationale citing the motivating signal"

inputs:
  - kind: skill-slug
  - kind: past-run signals (evals, lint findings, contract score, reviewer frowns)
outputs:
  - kind: refinement-proposal
    location: "03_Agents-and-Skills/Skills/_proposed/<slug>/"

done_when:
  - "Signals came from existing sources only (evals, lints, contract score, run records) — nothing fabricated"
  - "Exactly one concrete refinement is proposed (a NEVER/ALWAYS rule, a tightened lint, a sharper 'Use when' trigger, or a new eval) — never 'make it better'"
  - "The proposal is a draft under _proposed/; the live skill is unchanged until its owner approves"
  - "With no real signal, the run printed 'no refinement warranted' and stopped"

context_budget_tokens_max: 6000
---

# SOP — Skill refine

## TL;DR
Read a capability's past-run signals and propose one concrete refinement as a draft, so each skill gets sharper with use instead of drifting.

## When to run
- An eval fails, a lint fires repeatedly, or reviewers repeat the same correction
- During a periodic capability review

## Inputs
- The skill slug (or "sweep" to pick the weakest)
- Its existing signals

## Procedure

1. **Gather signals** from existing sources: `python3 06_Engine/evals/run-evals.py <slug>`, `python3 06_Engine/harness/lint-skill.py <slug>`, `python3 06_Engine/harness/lint-skill.py --contract <slug>`, and reviewer frowns in `00_Agentic-OS/_runs/`.
2. **Require one real signal**; otherwise stop with "no refinement warranted".
3. **Diagnose the single biggest weakness.**
4. **Draft one refinement** with `/skill-refine` under `03_Agents-and-Skills/Skills/_proposed/<slug>/`.
5. **Hand to `skill-agent-smith`**: on the owner's approval it applies the change and re-runs the gates.

## Outputs
- A refined draft and its rationale

## Done when
See front-matter.

## Failure modes
- **No real signal:** stop; never manufacture a problem.
- **Vague proposal:** rejected — it must be a rule a reviewer can catch.
- **Plug-in skill:** refine upstream with `/plugin-optimize`; never edit the mount.

## See also
- [`/skill-refine`](../../prompts/skill-refine.prompt.md) · [`workflow-audit`](../workflow-audit/SOP.md) (creates capabilities; this refines them)
