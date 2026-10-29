# OS optimization — review rubric

**TL;DR:** PASS needs evidence of the scoped outcome, a green OS review and no new regression; a higher score or a larger inventory cannot substitute for quality.

Verdicts: PASS, ITERATE, BLOCKED or NOT-SCORED with a reason. A missing MUST never silently passes.

## Dimension 1 — Outcome evidence

- **MUST** Name one coherent problem, its backlog ID and the acceptance before execution.
- **MUST** Capture the baseline and the after-result, with method and limits.
- **MUST** Distinguish runtime evidence, local tests and reported historical results.
- **ALWAYS** Explain a justified no-change outcome instead of inventing work.

## Dimension 2 — Scope and completeness

- **MUST** Complete the affected behaviour across its consumers, including coupled fixes and docs.
- **MUST** Preserve unrelated changes and in-flight engine state.
- **SHOULD** Group related changes into one verifiable cycle.

## Dimension 3 — No metric gaming

- **MUST** Never create placeholders, duplicate guides or unused infrastructure to raise a score.
- **MUST** Never lower a threshold, skip a failing check or edit a generated file instead of its source.
- **MUST** Never infer quality or runtime health from file presence.

## Dimension 4 — Regression proof

- **MUST** Run targeted checks and widen with risk.
- **MUST** End with `python3 00_Agentic-OS/agentic-os-review.py` at VERDICT PASS.
- **MUST** Resolve failures the cycle introduced; list unrelated baseline failures separately.

## Dimension 5 — Reversibility and queue hygiene

- **MUST** Record exact changed paths, checks and a safe rollback in the run record.
- **MUST** Update the [backlog](../../OPTIMIZATION-BACKLOG.md) row; never start a second global checklist.
- **MUST** Keep publishing and consequential-decision permissions with their human owners.
