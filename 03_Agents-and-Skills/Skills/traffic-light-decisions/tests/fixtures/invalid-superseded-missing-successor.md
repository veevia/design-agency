---
type: decision
schema_version: decision-record/v2
record_type: ops-note
id: test-0009
status: superseded
owner: OS steward
consultation: solo
created: 2026-09-04
updated: 2026-09-04
---
# TEST-0009 — Broken supersession

## Action

Replaced a reversible setting.

## Reason

Exercise the required successor link.

## Evidence / result

The fixture intentionally omits `superseded_by`.

## Rollback / runbook

Delete the fixture.
