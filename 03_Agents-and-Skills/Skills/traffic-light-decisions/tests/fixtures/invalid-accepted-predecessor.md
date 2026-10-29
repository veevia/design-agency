---
type: decision
schema_version: decision-record/v2
record_type: adr
id: test-0010
status: accepted
light: green
owner: OS steward
consultation: solo
created: 2026-09-04
updated: 2026-09-04
---
# TEST-0010 — Ambiguous accepted predecessor

## Context

Another accepted record claims to replace this still-accepted boundary.

## Alternatives

| Option | Benefit | Cost |
|---|---|---|
| A | Stay accepted | Creates two active answers |
| B | Become superseded | Requires an explicit transition |

## Decision

This fixture intentionally remains accepted.

## Consequences

The validator must reject the ambiguous active pair.

## Consultation

This was a solo fixture.

## Reversal condition

Use a valid mirrored lifecycle transition.
