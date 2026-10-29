---
type: decision
schema_version: decision-record/v2
record_type: adr
id: aos-0001
slug: l0-authority-and-safety
layer: L0
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
# aos-0001 — L0 Authority & safety

> **TL;DR:** One authoritative source per concept; scope, permission and repository boundaries govern every action.

## Context

Several runtimes (Copilot, Claude Code, background workers) act on one repository that also mounts
independent plug-in repositories. Without one ownership model they follow stale copies, act beyond
the request, or change another repository's source.

## Alternatives

| Option | Benefit | Cost / risk |
|---|---|---|
| A — Per-runtime rules and copies | Local freedom per tool | Divergent behaviour and silent conflicts |
| B — One authority registry and explicit permission rules | Predictable resolution across tools | Registry and adapters need upkeep |

## Decision

We will choose B.

1. [AUTHORITIES](../../AUTHORITIES.md) names the owner of every cross-cutting concept. Derived views (catalog,
   discovery links, indexes, summaries, mounted plug-in copies) never override their source, host instructions or
   the user's permission.
2. Establish scope and authorization before acting; recheck when scope or side effects change. Analysis is not
   approval to implement. Publishing, pushing, restarts, external messages and irreversible actions need explicit
   authorization; capability is not permission.
3. Plug-ins are independent repositories mounted as pinned submodules. Their sources change upstream, through
   their own review, never by editing the mount in place.
4. Never commit credentials. Dependencies, environments, caches and builds stay out of Git; customer material
   follows the labels and visibility rules in [CONVENTIONS](../../00_README/CONVENTIONS.md).
5. Keep evidence beside its task; repository placement alone never authorizes egress to another tool or tenant.

## Consequences

- Easier: any runtime resolves a conflict the same way, and plug-ins stay upgradeable.
- Harder: adapters, registry rows and submodule pins must be maintained; a clone cannot restore ignored state.

## Consultation

- Solo decision by the template maintainer; wording drafted with an agent and reviewed by the owner.
- Material dissent: none recorded.

## Reversal condition

Reopen when an authority conflict cannot be resolved from the registry or a required function cannot run
safely. Stop the affected action and keep the working implementation until authorization and recovery exist.
