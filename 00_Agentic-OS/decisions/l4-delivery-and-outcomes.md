---
type: decision
schema_version: decision-record/v2
record_type: adr
id: aos-0005
slug: l4-delivery-and-outcomes
layer: L4
status: accepted
light: green
canonical: true
owner: OS steward
decided_by: OS steward
consultation: solo
created: 2026-10-29
updated: 2026-10-29
tags: [type/decision, record/adr, status/accepted, light/green, scope/workspace]
---
# aos-0005 — L4 Delivery & outcomes

> **TL;DR:** Satisfy acceptance criteria; files and successful commands alone do not establish completion.

## Context

Answers, research, designs, prototypes, films and code need different deliverables. Counting files
or passing commands rewards activity instead of usable results.

## Alternatives

| Option | Benefit | Cost / risk |
|---|---|---|
| A — File and command checklist | Easy to count | Unusable or unrequested output passes |
| B — Acceptance-backed outcomes | Completion means the agreed use works | Criteria and proof must be explicit |

## Decision

We will choose B.

1. Deliver the scoped outcome from [L3](l3-task-control.md): a grounded answer, usable design, testable
   prototype, reviewed film or working change. Resolve material acceptance ambiguity before widening scope.
2. Keep requested durable artifacts in the project's phase folder (engine projects inside the hub, for example
   `01_Project-Hubs/<hub>/03_build/<name>/`). Sufficient answers need no file; link shared authorities instead
   of copying them.
3. Hand off the result, relevant paths and sources, [L5](l5-verification-and-learning.md) acceptance evidence,
   and blockers or the next action. Mark partial delivery; never claim completion with unmet criteria.
4. Files, commits, passing commands or scores are not acceptance evidence on their own.

## Consequences

- Easier: small answers avoid scaffolding; substantial deliverables keep clear gates.
- Harder: each task needs stated acceptance and matching proof. Activity is not delivery.

## Consultation

- Solo decision by the template maintainer; wording drafted with an agent and reviewed by the owner.
- Material dissent: none recorded.

## Reversal condition

Reopen when a completed result fails its agreed use. Mark it incomplete, keep the evidence and return the
smallest corrective task to L3.
