# Typed decision records — field and validation reference

This reference and [validator](../scripts/check_decision.py) implement
[L3 — Task control](../../../../00_Agentic-OS/decisions/l3-task-control.md). [W5](../../../../02_Workflows/workflows/W5-decide.md)
owns the procedure; this file owns field details. The
[framework](../../../../00_README/_frameworks/traffic-light-decisions.md) defines Traffic Light meaning.

## Common fields

| Field | Required | Values / rule |
|---|---:|---|
| `schema_version` | yes | New: `decision-record/v2`; migrated history: `decision-record/v1` |
| `record_type` | yes | `adr`, `pdr`, `ops-note`, `release` |
| `id` | yes | Unique canonical `<namespace>-NNNN` |
| `status` | yes | `proposed`, `accepted`, `superseded`, `retired` |
| `owner` | yes | One accountable person; never a generic group placeholder |
| `consultation` | yes | `solo`, `invited`, `reviewed` |
| `created`, `updated` | yes | Real ISO dates |
| `aliases` | no | Unique historical/contextual handles used only for collision repair |
| `supersedes` | no | Canonical predecessor IDs |
| `superseded_by` | superseded only | Canonical successor IDs; must resolve bidirectionally to an accepted terminal |
| `canonical` | no | `true` only for an accepted ADR in the deliberately small active contract set |
| `layer` | workspace canonical ADRs | Exactly one of `L0`–`L5`; optional on other ADRs, never a maturity score |

`superseded` means replaced: it names exactly one successor, and its links are mandatory, mirrored,
acyclic, and must reach an
accepted record. `retired` means ended without replacement and therefore forbids `superseded_by`.
A proposed successor may cite an accepted predecessor while under review; accepting it requires one
atomic lifecycle/link transition on both records.

## Traffic Light fields

ADRs and PDRs require a Traffic Light. Ops notes and releases can use one when current operating
posture matters.

| Field | Green | Yellow | Red |
|---|:---:|:---:|:---:|
| `light` | required | required | required |
| `trigger` | — | required | — |
| `expiry` | — | required ISO date | — |
| `blocker` | — | — | required |
| `unblock_owner` | — | — | required person |

An expired active Yellow is an authoring failure. Repository migration can use `--allow-expired` to
emit closure warnings while continuing structural validation. A retired or superseded Yellow retains
its old expiry as historical evidence and does not fail.

## Type contracts

| Type | Required body evidence |
|---|---|
| ADR | Context; ≥2 alternatives; decision; consequences; consultation/disagreement; reversal/rollback |
| PDR | Decision; ≥2 options; evidence/rationale; affected outcomes/consequences; review trigger |
| Ops note | Action; reason; evidence/result; rollback/runbook |
| Release | Subject/version; gates; result; immutable evidence |

The v2 validator recognizes equivalent headings listed in the templates. V1 migration records are not
forced into a new body outline; only their metadata is normalized.

## Consultation semantics

- `solo`: one accountable author made/reported the choice. No dissent section is required.
- `invited`: review was requested. Name the invitees; “invited; none surfaced” is honest.
- `reviewed`: review occurred. Record the reviewer evidence and material dissent.

“None” is not globally invalid. It is invalid only when used as the sole evidence for
`consultation: reviewed`.

## Canonical namespace examples

| Home | Canonical form | Example |
|---|---|---|
| `00_Agentic-OS/decisions/` | `aos-NNNN` | `aos-0004` |
| `01_Project-Hubs/<hub>/**/decisions/` | `<hub-slug>-NNNN` | `example-project-0002` |

Collision repair keeps the first canonical holder and gives the colliding record a new ID plus a
contextual alias (for example `example-project-0007`, alias `example-project-0003-export-flow`). Short legacy numbers can
stay visible in filenames and headings so old path links keep working; new citations use the
canonical front-matter ID.

New filenames may be descriptive kebab-case without a numeric prefix. Renaming a file does not
allocate a new ID. Canonical v2 bodies are limited to 600 whitespace-delimited words by the validator;
keep implementation detail and dated results in linked runbooks/evidence, not a second ADR.

## Validator behavior matrix

| Scenario | Result |
|---|---|
| Valid solo ops note | pass |
| ADR with fewer than two alternatives | fail |
| Yellow missing trigger or expiry | fail |
| Active expired Yellow | fail; warning under `--allow-expired` |
| Retired expired Yellow without successor | pass |
| Superseded expired Yellow with accepted successor | pass |
| Superseded record without successor or with a cycle/dead end | fail |
| Accepted successor that leaves its predecessor accepted | fail |
| `canonical: true` on anything except an accepted ADR | fail |
| Layer metadata on a non-ADR, or a value outside L0–L5 | fail |
| Missing, duplicate, or extra layer with `--expected-layers` | fail |
| Duplicate canonical ID | fail |
| Missing or one-way required supersession target | fail |
| V1 historical prose not shaped like a v2 template | pass |

Run the behavioral suite:

```sh
python3 -m unittest \
  03_Agents-and-Skills/Skills/traffic-light-decisions/tests/test_check_decision.py -v
```

## Files

Inspect a bounded current-contract manifest with `check_decision.py 00_Agentic-OS/decisions --canonical --json`.
Selection excludes unmarked records from the output, but relation checks still resolve the authoritative
corpus. Invalid records marked canonical fail rather than disappearing. The layer field is authored in
the ADR, not a second manifest. The workspace reviewer enforces its complete six-layer set:

```sh
python3 00_Agentic-OS/agentic-os-review.py --contracts-only
# Equivalent guard on a scoped canonical selection:
python3 03_Agents-and-Skills/Skills/traffic-light-decisions/scripts/check_decision.py \
  00_Agentic-OS/decisions --canonical --expected-count 6 \
  --expected-layers L0 L1 L2 L3 L4 L5 --json
```

`--expected-layers` requires `--canonical`; it checks one record per listed layer, with no unassigned
or extra records. Project hubs need not adopt this six-record structure. Whole-corpus governance audit:

```sh
python3 03_Agents-and-Skills/Skills/traffic-light-decisions/scripts/check_decision.py \
  --repo-root . --allow-expired
```

- Validator: [`../scripts/check_decision.py`](../scripts/check_decision.py)
- Template chooser: [`../assets/decision-record.template.md`](../assets/decision-record.template.md)
- ADR template: [`../assets/adr.template.md`](../assets/adr.template.md)
- PDR template: [`../assets/pdr.template.md`](../assets/pdr.template.md)
- Ops-note template: [`../assets/ops-note.template.md`](../assets/ops-note.template.md)
- Release template: [`../assets/release.template.md`](../assets/release.template.md)
