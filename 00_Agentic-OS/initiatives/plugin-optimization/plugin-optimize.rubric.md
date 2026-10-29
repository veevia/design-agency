# Plug-in optimization — review rubric

**TL;DR:** PASS needs an agreed measure, a before/after report from the same commands, the change merged upstream and a re-pinned host with no regression.

Verdicts: PASS, ITERATE, BLOCKED or NOT-SCORED with a reason.

## Dimension 1 — Measure before change

- **MUST** Record the plug-in, edition, pinned commit and the baseline report before any change.
- **MUST** Name one hypothesis and the metric it should move; the measure is agreed, not chosen afterwards.

## Dimension 2 — Upstream ownership

- **MUST** Change the plug-in only in its own repository, under its contribution rules and license.
- **MUST** Run the plug-in's own tests and gates on the change.
- **MUST** Never commit plug-in source through the host; the host records only the new submodule pin.

## Dimension 3 — Proof of improvement

- **MUST** Re-run the identical baseline commands on the re-pinned host; show the targeted metric moved.
- **MUST** Show no regression in other capabilities of the plug-in or in the host's OS review.
- **SHOULD** Include one real or synthetic task outcome, not only static metrics.

## Dimension 4 — Evidence and reversibility

- **MUST** Record the upstream reference, old and new pins, commands, results and verdict in the run record.
- **MUST** State the rollback: re-pin the previous commit.
- **MUST** Keep publishing and pull-request creation with the authorized human.
