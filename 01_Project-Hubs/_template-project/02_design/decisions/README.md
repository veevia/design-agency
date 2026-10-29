# decisions/ — Design phase

**TL;DR:** Typed decision records (`decision-record/v2`) for durable choices made during Design — written through W5 only when later work must follow the choice; routine progress and phase closure need no file here.

## Before you write anything

Search this hub's `decisions/` folders and `_wiki/decisions/` first. If an existing record or artifact already
holds the rationale, cite it and stop. [W5 — Decide](../../../../02_Workflows/workflows/W5-decide.md) (`02_Workflows/workflows/W5-decide.md`) owns
the procedure.

## Pick the smallest truthful record

Start from the [template router](../../../../03_Agents-and-Skills/Skills/traffic-light-decisions/assets/decision-record.template.md), then copy one template:

| The durable fact is… | Copy |
|---|---|
| A product, design, scope or experience choice | [`pdr.template.md`](../../../../03_Agents-and-Skills/Skills/traffic-light-decisions/assets/pdr.template.md) |
| An architecture or trust boundary, or a choice that's expensive to reverse | [`adr.template.md`](../../../../03_Agents-and-Skills/Skills/traffic-light-decisions/assets/adr.template.md) |
| A reversible setting, maintenance action, incident response or cleanup | [`ops-note.template.md`](../../../../03_Agents-and-Skills/Skills/traffic-light-decisions/assets/ops-note.template.md) |
| A promotion, launch or release attestation | [`release.template.md`](../../../../03_Agents-and-Skills/Skills/traffic-light-decisions/assets/release.template.md) |

## Conventions

- **Filename:** descriptive kebab-case (`primary-persona.md`), never a bare number.
- **ID:** `id: <hub-slug>-NNNN`, unique across the whole hub — every phase and `_wiki/decisions/`. Never reuse
  or renumber an ID.
- **Front matter:** `schema_version: decision-record/v2`, `record_type`, `status` (`proposed` | `accepted` |
  `superseded` | `retired`), one named `owner`, `consultation` (`solo` | `invited` | `reviewed`), `created`,
  `updated`. ADRs and PDRs add one `light`: 🟡 needs `trigger` + `expiry`, 🔴 needs `blocker` + `unblock_owner`.
  Details: [field reference](../../../../03_Agents-and-Skills/Skills/traffic-light-decisions/references/REFERENCE.md).
- **Honesty:** record the consultation that actually happened. Solo work is `consultation: solo` — never
  invented reviewers or dissent.
- **Change:** amend in place to clarify or close a condition; a reversed choice gets a successor, linked both
  ways with `supersedes` / `superseded_by`.

Validate before filing:

```sh
python3 03_Agents-and-Skills/Skills/traffic-light-decisions/scripts/check_decision.py 01_Project-Hubs/<hub-slug>/02_design/decisions/<file>.md
```

## Typical decisions in this phase

- Design direction and the POV the team commits to (PDR)
- Scope trade-offs, feature priority and explicit non-goals (PDR)
- The rollback trigger the PRD will carry (PDR)
- A new system, data or integration boundary the PRD implies (ADR)

The Design → Build gate is recorded in the hub README's [phase-gate table](../../README.md#phase-gates), not here. Feature sub-hubs keep their own `decisions/` and may use `<hub-slug>-<feature>-NNNN` IDs.
