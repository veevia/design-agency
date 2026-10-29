---
type: decision
schema_version: decision-record/v2
record_type: adr
id: aos-0006
slug: l5-verification-and-learning
layer: L5
status: accepted
light: green
canonical: true
owner: OS steward
decided_by: OS steward
consultation: solo
created: 2026-10-29
updated: 2026-10-29
tags: [type/decision, record/adr, status/accepted, light/green, scope/workspace, scope/harness]
---
# aos-0006 — L5 Verification & learning

> **TL;DR:** Verify current results, expose failures, keep useful findings and review improvements before promotion.

## Context

Historical passes and valid metadata cannot prove today's outcome. A harness that optimizes capabilities
(native or plug-in) needs baselines and regression proof, or it rewards gaming its own metrics.

## Alternatives

| Option | Benefit | Cost / risk |
|---|---|---|
| A — Trust historical passes and promote automatically | Apparent speed | Stale proof and unreviewed behaviour |
| B — Current proof, measured loops and reviewed promotion | Traceable confidence | Verification effort and visible gaps |

## Decision

We will choose B.

1. Test current results against L3's acceptance: sources for answers, usability and accessibility for designs,
   behaviour and regressions for executable changes. Start small; widen with risk.
2. The [OS review](../agentic-os-review.py) is the integrity gate: contracts, skill spec and contracts, lints,
   evals, SOPs, capability map, catalog and discovery drift, plug-in profiles, links, hygiene and unit tests.
   Passing it proves repository integrity, not runtime health or plug-in quality.
3. Improvement runs as a measured loop ([initiatives](../initiatives/README.md)): baseline → scoped change →
   evaluation against a rubric → regression checks → evidence record. Plug-in improvements use the plug-in's
   report as baseline and are proposed upstream.
4. Record inputs, method, results, failures and untested conditions in the task's evidence; keep durable
   findings in L1's knowledge homes. Promotion through L2 requires reviewed evidence, side effects and rollback.
5. Never lower a threshold, fabricate a result or create placeholders to pass a gate.

## Consequences

- Easier: confidence is traceable and regressions surface early.
- Harder: verification takes effort and gaps stay visible. Task completion and capability promotion are separate gates.

## Consultation

- Solo decision by the template maintainer; wording drafted with an agent and reviewed by the owner.
- Material dissent: none recorded.

## Reversal condition

Reopen for a missed reproducible acceptance failure or a promotion regression. Keep the failing evidence,
withhold or roll back promotion and add a targeted regression check.
