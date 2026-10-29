---
type: decision
schema_version: decision-record/v2
record_type: adr
id: aos-0002
slug: l1-knowledge-and-context
layer: L1
status: accepted
light: green
canonical: true
owner: OS steward
decided_by: OS steward
consultation: solo
created: 2026-10-29
updated: 2026-10-29
tags: [type/decision, record/adr, status/accepted, light/green, scope/workspace, scope/context]
---
# aos-0002 — L1 Knowledge & context

> **TL;DR:** Retrieve selectively from repository-backed memory; keep one resume point for substantial work.

## Context

Agents lose progress when chats end and waste context when they load everything. Knowledge must
survive tools, people and sessions without replaying conversations.

## Alternatives

| Option | Benefit | Cost / risk |
|---|---|---|
| A — Replay full history and load whole catalogs | Broad context | Repeated reading, stale state, crowded windows |
| B — Selective retrieval plus one checkpoint per substantial task | Bounded context, durable progress | Indexes and checkpoints need reconciliation |

## Decision

We will choose B.

1. Repository sources and task evidence are durable memory; chat and runtime memory are caches of them.
   Raw intake (`00_context_intake/`) stays immutable; maintained knowledge lives in `_wiki/`; phase outputs
   cite the wiki instead of copying it; claims carry `observed`, `reported` or `assumed`.
2. Retrieve through indexes first: the [capability catalog](../../03_Agents-and-Skills/INDEX.md), a hub's
   `_wiki/index.md` or `/context-pull`. Load history only for a concrete question.
3. Substantial work (multi-step, research-heavy or interruptible) keeps one resume point in its existing task
   home: outcome and scope, current step, next action, completed work with proof, changed and protected
   files, verification, blockers. Refresh it before interruption or handoff.
4. Simple tasks need no journal. On resume, reconcile the checkpoint with current files before continuing.

## Consequences

- Easier: work resumes across sessions and runtimes; context stays small.
- Harder: indexes must be regenerated and checkpoints reconciled. Smaller context alone is not reliable recovery.

## Consultation

- Solo decision by the template maintainer; wording drafted with an agent and reviewed by the owner.
- Material dissent: none recorded.

## Reversal condition

Reopen after a failed recovery of scope, next action or proof. Repair the checkpoint or retrieval route
before widening default context.
