---
name: drift-check
title: Detect when a build drifts from its intent
description: "Compare a build against its original brief, PRD, and design system across four drift signals — circling feedback, unexplained friction, distance from the pitch, and no conviction — cite evidence for each, map present signals to their response, and close with a Traffic Light (stay, watch, or go wider). Use when a build has run for several sessions and feels far from the original pitch, when the same feedback keeps circling in reviews, or when the team cannot say why this direction beats the alternatives."
status: beta
when_to_load:
  - A build has run for several sessions and feels far from the original pitch
  - The same feedback keeps circling in reviews
  - The team cannot articulate why this direction over the alternatives
  - Before a Build → Learn gate or a scope change in 03_build/
applies-to: builds and prototypes in 03_build/, their briefs and PRDs in 02_design/
narrative: 00_README/_frameworks/ai-powered-workflows.md
inputs:
  - kind: brief-or-prd
    where: "01_Project-Hubs/*/02_design/**/*.md"
  - kind: build-notes
    where: "01_Project-Hubs/*/03_build/**/*.md"
outputs:
  - kind: drift-finding
    schema: "Four signals marked present or absent with tagged evidence → mapped responses → one Traffic Light (🟢 stay / 🟡 watch with trigger + expiry / 🔴 go wider)"
done_when:
  - Each of the four signals is marked present or absent with specific, evidence-tagged support
  - Each present signal maps to its response
  - The check names what changed versus the original brief or PRD, and why
  - The check closes with a Traffic Light; a Yellow carries trigger and expiry
lints:
  - id: drift-check-missing-baseline
    severity: warning
    where: "01_Project-Hubs/[!_]*/03_build/**/*drift*.md"
    pattern: "^#\\s+Drift check"
    must_also_match: "^informed-by:\\s*\\S"
    message: "A drift check must name the brief or PRD it compares against in front-matter (informed-by:)."
budget:
  context_tokens_max: 2000
loads: [evidence-tagging]
---

# Drift Check

**TL;DR:** Drift looks like progress in a slightly different direction; put the build next to its original brief, test four signals with evidence, and decide to stay, watch, or go wider.

## When to use

- Reviews keep circling the same question.
- Something feels off and nobody can say why.
- The build no longer resembles the pitch, or the team cannot choose between directions.

## Steps

1. **Pull both reference points**: the brief, PRD, and POV in `<hub>/02_design/`; current build notes in `<hub>/03_build/`; the design system in `05_Library/DESIGN-SYSTEM-AI-INSTRUCTIONS.md`.
2. **Mark each signal present or absent** with specific evidence tagged `observed`, `reported`, or `assumed` (`evidence-tagging`).

   | Signal | What it means | Response |
   |---|---|---|
   | Feedback keeps circling the same question | The direction is not addressing the real problem | Stop refining; generate real alternatives and compare them side by side |
   | Something feels off; nobody can say why | Hidden friction | Walk the full flow end to end; get an outside view; ground it in research |
   | The build feels far from the original pitch | Accumulated scope shifts | Put the build next to the brief and PRD; name what changed and why |
   | Can't pick one direction over another | Too few real options seen | `/go-wider`, then `/trade-off`; put the top two in front of users |

3. **Name what changed** versus the original brief, with dates and reasons.
4. **Close with an evidence-backed Traffic Light assessment**: 🟢 stay the course · 🟡 watch (needs `trigger` + `expiry`) · 🔴 go wider now. Use the answer or existing build/task notes; a routine assessment needs no new decision file. Follow [W5](../../../02_Workflows/workflows/W5-decide.md) only for a new durable choice, explicit capture request, or lifecycle change; load `traffic-light-decisions` only when authoring or changing that record.

## Output format

Use [`assets/drift-finding.template.md`](assets/drift-finding.template.md), or this compact form:

```
=== drift check — <hub>/<build> ===
Circling feedback: present — "same filter question in 3 reviews" [observed | review-notes-2026-02-12]
Feels off:         absent
Far from pitch:    present — brief promised 1 screen, build has 4 [observed | 02_design/brief.md]
No conviction:     absent
Changed vs brief:  added bulk-export flow (2026-02-05, sales request)
Verdict: 🟡 watch — trigger: 3 users complete the core task in the 1-screen flow; expiry: 2026-03-01
```

## Watch-outs

- "Feels off" is a prompt to investigate, not a finding — demand the signal and its evidence.
- Polishing through the sticking point hides the real problem; stop refining when feedback circles.
- A 🟡 without trigger and expiry is invalid.
- A routine drift check is an evaluation, not a decision record: it needs no new decision file and stays out of `decisions/`.

## See also

- `go-wider` and `trade-off` prompts: [`/go-wider`](../../../02_Workflows/prompts/go-wider.prompt.md) · [`/trade-off`](../../../02_Workflows/prompts/trade-off.prompt.md) · [`/drift-check`](../../../02_Workflows/prompts/drift-check.prompt.md)
- `evidence-tagging` · `traffic-light-decisions` · `design-system-as-infrastructure` · `problem-framing`
