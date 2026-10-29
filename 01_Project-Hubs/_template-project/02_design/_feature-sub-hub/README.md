# Feature sub-hub — `[NN]-[feature-name]-design/`

**TL;DR:** One workstream's design artifacts, decisions and raw inputs in one folder — use it when a program runs two or more parallel design initiatives.

*Copy this folder to `02_design/[NN]-[feature-name]-design/` and replace the placeholders.*

## Status

> **Workstream:** `[feature name]`
> **Owner:** `[single name]`
> **Light:** 🟢 / 🟡 / 🔴 — `[one-sentence reason; a 🟡 names its trigger and expiry]`
> **Current state:** `[one sentence]`

## Artifacts

| Artifact | File | Status |
|---|---|---|
| Design POV | `design-pov.md` | draft / review / published |
| Design brief | `design-brief.md` | draft / review / published |
| PRD | `[feature-name]-PRD.md` | draft / review / published |
| Architecture options | `architecture-options.md` | optional |

## Decisions

Typed decision records for this workstream live in `decisions/`, named in descriptive kebab-case with IDs
`<hub-slug>-<feature>-NNNN`. Follow the [phase decision guide](../decisions/README.md) and reuse existing
rationale first.

| ID | File | Type | Light | Owner | Summary |
|---|---|---|---|---|---|

## Intake

Raw inputs for this workstream — customer-authored user stories, discovery instruments, storyboards, images —
live in `_intake/`. Don't edit them; cite them from the artifacts above.

## Links

- Parent design phase: [`../README.md`](../README.md)
- Understand artifacts: [`../../01_understand/`](../../01_understand/README.md)
- Build artifacts, when created: [`../../03_build/`](../../03_build/README.md)
