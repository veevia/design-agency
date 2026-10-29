---
id: workflow-audit
title: Workflow audit — codify what you do repeatedly
status: beta
trigger: "Weekly, or the moment the same manual sequence has been run three or more times"

owner_agent: none — human-driven
loads_skills:
  - extreme-clarity
  - goal-harness
invokes_prompts:
  - workflow-audit
  - capability-spot

produces_artifacts:
  - "02_Workflows/SOPs/_proposed/<id>/SOP.md"
  - "03_Agents-and-Skills/Skills/_proposed/<slug>/SKILL.md"
  - "00_Agentic-OS/OPTIMIZATION-BACKLOG.md entries"

inputs:
  - kind: lookback-period
    where: "the week, or since the last audit"
  - kind: the user's recollection of repeated manual work
outputs:
  - kind: graduation-proposals
    location: "02_Workflows/SOPs/_proposed/ and 03_Agents-and-Skills/Skills/_proposed/"

done_when:
  - "Every workflow run manually three or more times in the period that is not yet codified has been named"
  - "Each named workflow has one route: skill, SOP, automation, or leave-manual — with a reason"
  - "Each to-codify workflow has a stub in _proposed/ (never auto-graduated)"
  - "Candidates already found by capability-spot were linked, not re-proposed"

context_budget_tokens_max: 6000
---

# SOP — Workflow audit

## TL;DR
Ask what you repeat by hand, then route each repeated workflow to a skill, SOP, automation, or leave-manual — the forward-looking half of the self-evolution loop.

## When to run
- Weekly, next to `capability-spot`
- When you catch yourself running the same sequence a third time
- At the start of a new hub, to reuse existing capabilities instead of improvising

## Inputs
- The period to review
- Your recollection, plus session snapshots if available

## Procedure

1. **Elicit** with `/workflow-audit`: every output produced by hand three or more times.
2. **Filter** to three or more occurrences.
3. **Route** each to skill · SOP · automation · leave-manual.
4. **De-duplicate** against the backlog, the catalog, and `_proposed/`.
5. **Draft stubs** in `_proposed/`; the owner graduates them.

## Outputs
- Proposal stubs and backlog rows

## Done when
See front-matter.

## Failure modes
- **Nothing repeats three times:** a valid outcome — print "No new codification candidates".
- **Too variable to codify:** route to leave-manual and record why, so the next audit doesn't re-raise it.

## See also
- [`/workflow-audit`](../../prompts/workflow-audit.prompt.md) · [`capability-spot`](../capability-spot/SOP.md)
