---
title: "W5 — Decide only when needed"
type: workflow
workflow-id: W5
status: canonical
owner: OS steward
last-updated: 2026-10-29
loop-phase: all
inputs:
  - A new durable choice, explicit capture request, or record lifecycle change
outputs:
  - Existing evidence reused, or one validated typed decision record (ADR, PDR, ops note, or release)
source: aos-0004 (L3 task control) + traffic-light-decisions
tags: [type/workflow, purpose/decide, status/canonical]
---

# W5 — Decide

> **TL;DR:** Reuse existing rationale first; record a new choice only when it changes what future work must follow — as the smallest truthful typed record, with its Traffic Light kept separate from its lifecycle, validated from disk.

## 1. Decide whether to write anything

Search the relevant hub's `decisions/` folders (and `00_Agentic-OS/decisions/` for OS-wide choices). If
the task follows an existing choice, cite it in the task evidence and stop. Bug fixes, refactors,
routine settings, progress, and test results belong in existing task, runbook, or release evidence;
do not create a duplicate decision file. Phase closure alone needs no new decision file — W1–W4 keep
gate evidence in their phase artifacts.

Use this workflow for a new durable choice, an explicit capture request, or a lifecycle change.

## 2. Choose the smallest truthful record

| What changed? | `record_type` | Required body evidence |
|---|---|---|
| Durable system, trust, or cross-component boundary; expensive reversal | `adr` | Context · ≥2 alternatives · decision · consequences · consultation · reversal |
| Product, design, scope, or experience choice | `pdr` | Decision · ≥2 options · evidence · affected outcomes · review trigger |
| Operational rationale worth keeping beyond its runbook or task | `ops-note` | Action · reason · evidence/result · rollback |
| A release attestation not already captured with the release | `release` | Subject/version · gates · result · immutable evidence |

Use the [template router](../../03_Agents-and-Skills/Skills/traffic-light-decisions/assets/decision-record.template.md)
only after this choice. No invented alternatives or dissent; solo consultation is valid.

## 3. Keep lifecycle and Traffic Light separate

| Axis | Field | Values | Meaning |
|---|---|---|---|
| Lifecycle | `status` | `proposed` → `accepted` → `superseded` or `retired` | Where the record is in its life |
| Operating posture | `light` | 🟢 `green` · 🟡 `yellow` · 🔴 `red` | Whether work can proceed on it now |

- ADRs and PDRs declare `light`; ops notes and releases may.
- 🟡 Yellow needs `trigger` (what closes it) and `expiry` (a real ISO date).
- 🔴 Red needs `blocker` and one `unblock_owner`.
- An accepted record can be Yellow; a passing schema never turns Yellow into Green.

## 4. Capture or amend once

- Keep the record beside the work it governs: `01_Project-Hubs/<hub>/<phase>/decisions/` (or a feature
  sub-hub's `decisions/`), or `00_Agentic-OS/decisions/` for OS-wide choices. Use a descriptive
  kebab-case filename and a stable namespace ID from [AUTHORITIES](../../AUTHORITIES.md). Do not
  renumber history for display.
- Follow the [field reference](../../03_Agents-and-Skills/Skills/traffic-light-decisions/references/REFERENCE.md):
  `schema_version: decision-record/v2`, `record_type`, `id`, `status`, one `owner`, honest
  `consultation` (`solo`, `invited`, `reviewed`), and real `created`/`updated` dates.
- Clarify wording, update evidence, or close a condition in the existing record. A materially reversed
  decision needs a successor with mirrored `supersedes` / `superseded_by` links; preserve the
  predecessor's body. `retired` means ended without a successor. Do not make a new record merely to
  restate the same contract.
- `canonical: true` is an explicit architecture-scope choice, never a default. The workspace keeps
  [six canonical ADRs, one per L0–L5](../../00_Agentic-OS/README.md). Change the owning layer or its
  reviewed successor; do not add a canonical record for each task, phase, or release. Project
  decisions are not required to mirror these six layers.

## 5. Validate and hand off

```sh
python3 03_Agents-and-Skills/Skills/traffic-light-decisions/scripts/check_decision.py <record>
```

Regenerate only the affected index. Return the choice or reused record, its path, the validation
result, and any open condition (trigger and expiry, or blocker and unblock owner). Stop if evidence or
approval would have to be invented. A structural pass does not grant approval, close a Yellow
condition, or prove that a feature has shipped.

## See also

- Skills: [`decision-capture`](../../03_Agents-and-Skills/Skills/decision-capture/SKILL.md) (when to write) · [`traffic-light-decisions`](../../03_Agents-and-Skills/Skills/traffic-light-decisions/SKILL.md) (how to write and validate)
- Prompt: [`/decision-log`](../prompts/decision-log.prompt.md) · Framework: [`traffic-light-decisions.md`](../../00_README/_frameworks/traffic-light-decisions.md)
