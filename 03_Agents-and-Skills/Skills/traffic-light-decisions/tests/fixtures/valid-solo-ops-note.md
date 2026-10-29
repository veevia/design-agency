---
type: decision
schema_version: decision-record/v2
record_type: ops-note
id: test-0001
status: accepted
owner: OS steward
consultation: solo
created: 2026-09-04
updated: 2026-09-04
---
# TEST-0001 — Rotate a disposable log

## Action

Rotated the disposable test log.

## Reason

The log exceeded its documented retention threshold.

## Evidence / result

- Probe: `test -s rotated.log`
- Result: the active log is empty and the retained copy exists.

## Rollback / runbook

Move the retained copy back into place.
