---
type: decision
schema_version: decision-record/v2
record_type: adr
id: test-0011
status: accepted
light: green
owner: OS steward
consultation: solo
created: 2026-09-04
updated: 2026-09-04
supersedes: [test-0010]
---
# TEST-0011 — Ambiguous accepted successor

## Context

The claimed predecessor still says it is accepted.

## Alternatives

| Option | Benefit | Cost |
|---|---|---|
| A | Allow both | Ambiguous authority |
| B | Require transition | Explicit history |

## Decision

This fixture claims replacement without completing the transition.

## Consequences

The validator must fail.

## Consultation

This was a solo fixture.

## Reversal condition

Mark the predecessor superseded and mirror the links.
