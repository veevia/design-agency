---
id: session-snapshot
title: Session snapshot — compact a working session into a durable handoff
status: beta
trigger: "A working session is wrapping up, context pressure is rising, or a milestone is reached"

owner_agent: none — human-driven
loads_skills:
  - wiki-maintenance
  - extreme-clarity
invokes_prompts:
  - session-snapshot

produces_artifacts:
  - "01_Project-Hubs/<hub>/_wiki/sessions/<YYYY-MM-DD>-<slug>.md"

inputs:
  - kind: hub-slug
  - kind: optional-slug
outputs:
  - kind: session-snapshot
    location: "01_Project-Hubs/<hub>/_wiki/sessions/"

done_when:
  - "The snapshot exists with a TL;DR of 25 words or fewer"
  - "Each decision carries a Traffic Light; only new durable choices were routed to W5"
  - "The next action is single and specific (never 'continue work')"
  - "The hub's _wiki/log.md has a session-snapshot entry"

context_budget_tokens_max: 4000
---

# SOP — Session snapshot

## TL;DR
Distill a session's decisions, files touched, open questions, and one next action into a short file the next session reads first.

## When to run
- The session is wrapping up, or context pressure is rising
- A milestone is reached and you want a clean restart point
- Before a context-resetting event (a long break, a model switch, a new conversation)

## Inputs
- The hub the session worked in (if it spanned hubs, the one that owns the next action)
- Optional: an explicit slug

## Procedure

1. **Invoke** `/session-snapshot <hub> [<slug>]`.
2. **Confirm the framing** the prompt proposes before it writes.
3. **Review** the snapshot; the next session starts by reading it.

## Outputs
- One file under `<hub>/_wiki/sessions/`
- An entry in `<hub>/_wiki/log.md`

## Done when
See front-matter.

## Failure modes
- **Very short session** (about ten turns, no files touched): skip it; a one-paragraph note is enough.
- **Several hubs touched:** write the snapshot in the hub that owns the next action and link the others.

## See also
- [`/session-snapshot`](../../prompts/session-snapshot.prompt.md) · [`capability-spot`](../capability-spot/SOP.md) reads these snapshots
