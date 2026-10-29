---
type: decision
schema_version: decision-record/v2
record_type: adr
id: test-0006
status: accepted
light: green
owner: OS steward
consultation: solo
created: 2026-09-04
updated: 2026-09-04
supersedes: [test-0005]
---
# TEST-0006 — Current replacement boundary

## Context

The old condition expired.

## Alternatives

| Option | Benefit | Cost |
|---|---|---|
| A | Preserve old boundary | Carries obsolete constraints |
| B | Replace it | Requires migration |

## Decision

We use option B.

## Consequences

The old record remains as history.

## Consultation

This was a solo decision.

## Reversal condition

Reopen when the new boundary fails.
