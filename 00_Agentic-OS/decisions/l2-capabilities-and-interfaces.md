---
type: decision
schema_version: decision-record/v2
record_type: adr
id: aos-0003
slug: l2-capabilities-and-interfaces
layer: L2
status: accepted
light: green
canonical: true
owner: OS steward
decided_by: OS steward
consultation: solo
created: 2026-10-29
updated: 2026-10-29
tags: [type/decision, record/adr, status/accepted, light/green, scope/workspace, scope/plugins]
---
# aos-0003 — L2 Capabilities & interfaces

> **TL;DR:** Reuse capabilities with explicit interfaces and one authoring source; plug-ins connect through declared profiles.

## Context

Skills, agents, prompts and external engines must work in several runtimes. Copies per runtime drift,
and an engine plugged in without a declared interface can act beyond what the host expects.

## Alternatives

| Option | Benefit | Cost / risk |
|---|---|---|
| A — Copy capabilities into each runtime and vendor plug-ins | Works offline per tool | Divergent copies, unreviewable upgrades |
| B — Single sources, generated discovery, profiled plug-ins | Predictable reuse and upgrades | Profiles, schemas and generators need upkeep |

## Decision

We will choose B.

1. Select through the [catalog](../../03_Agents-and-Skills/INDEX.md); prefer an existing capability. Load only
   the selected contract and the references it requires.
2. Every skill, agent, prompt, SOP and tool declares inputs, outputs, side effects and required permission,
   and completion criteria. Native skills also meet the portable spec (`name` equals folder, description with
   a "Use when" trigger). Clarify undeclared side effects before use.
3. Edit only the authoring source named in [AUTHORITIES](../../AUTHORITIES.md). Discovery links in `.github/`
   and `.claude/`, the catalog and mounted plug-ins are derived; regenerate them with the engine.
4. A plug-in is described by a profile in `06_Engine/plugins/`: mount, editions, contributions, host
   adapters, requirements, and checks whose side effects are declared (`none`, `temp`, `mount`). An
   undeclared write into the mount fails the check. Host adapters stay hidden until their plug-in is mounted.
5. Keep native skills flat and agents and prompts at the same folder depth as their discovery links, so
   relative links resolve through both paths.

## Consequences

- Easier: one change reaches every runtime; plug-ins are added, checked, upgraded and removed with one command.
- Harder: each new capability or plug-in needs a contract or profile and passing gates. This is not runtime certification.

## Consultation

- Solo decision by the template maintainer; wording drafted with an agent and reviewed by the owner.
- Material dissent: none recorded.

## Reversal condition

Reopen for incompatible consumers, divergent copies or a plug-in that cannot be described by a profile.
Stop promotion, restore the last verified version and repair the owning source before regenerating.
