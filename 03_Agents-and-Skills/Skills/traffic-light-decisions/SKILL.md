---
name: traffic-light-decisions
title: Typed decision records with lifecycle and Traffic Light posture
description: "Validate, amend, supersede, or retire typed decision records. Use when working on files under decisions/ or handling an explicit durable-decision request; first reuse existing rationale through W5. Not required for routine task progress, bug fixes, settings, or release evidence already recorded elsewhere."
status: stable
applies-to: decisions, ADRs, PDRs, operational notes, release attestations, phase gates
narrative: 00_README/_frameworks/traffic-light-decisions.md
when_to_load:
  - Authoring, changing, retiring, or reviewing a record under any decisions/ folder
  - Deciding whether a material event needs an ADR, PDR, ops note, or release record
  - Reviewing a Yellow decision, lifecycle transition, canonical ID, or supersession chain
inputs:
  - kind: decision
    where: "**/decisions/*.md"
outputs:
  - kind: decision-record
    schema: "decision-record/v2 front matter plus the type-specific body contract"
done_when:
  - "The record uses exactly one of: adr, pdr, ops-note, release"
  - "Its canonical `id` is unique and its `status` is proposed, accepted, superseded, or retired"
  - "ADRs and PDRs declare `light`; Yellow has trigger+expiry and Red has blocker+unblock_owner"
  - "Consultation is honestly marked solo, invited, or reviewed; solo work does not fabricate dissent"
  - "A superseded record resolves through mirrored links to an accepted successor; a retired record has no successor"
  - "Only an accepted ADR may declare `canonical: true`"
  - "check_decision.py recomputes a passing result from disk"
lints:
  - id: yellow-missing-trigger
    severity: error
    where: "{00_Agentic-OS,01_Project-Hubs}/**/decisions/*.md"
    pattern: "^light:\\s*yellow\\b"
    must_also_match: "^trigger:\\s*\\S"
    message: "Yellow decisions must declare the condition that closes them."
  - id: yellow-missing-expiry
    severity: error
    where: "{00_Agentic-OS,01_Project-Hubs}/**/decisions/*.md"
    pattern: "^light:\\s*yellow\\b"
    must_also_match: "^expiry:\\s*\\d{4}-\\d{2}-\\d{2}"
    message: "Yellow decisions must declare a real ISO expiry date."
  - id: red-missing-unblock-owner
    severity: error
    where: "{00_Agentic-OS,01_Project-Hubs}/**/decisions/*.md"
    pattern: "^light:\\s*red\\b"
    must_also_match: "^unblock_owner:\\s*\\S"
    message: "Red decisions must name one unblock owner."
  - id: owner-the-team
    severity: error
    where: "{00_Agentic-OS,01_Project-Hubs}/**/decisions/*.md"
    pattern: "^owner:\\s*(?:the\\s+team|team|everyone|all|us|we|tbd|n/?a)\\s*$"
    message: "Decision ownership must name one accountable person, not a group or placeholder."
budget:
  context_tokens_max: 2400
---

# Validate decision records

[W5 — Decide](../../../02_Workflows/workflows/W5-decide.md) owns the procedure: reuse existing
rationale first, then choose the smallest truthful record only if needed. Routine task execution
does not require loading this skill or creating a file.

## Author or change a record

1. Read the [field reference](references/REFERENCE.md) for identity, lifecycle, consultation, and
   type-specific requirements. Use the [template router](assets/decision-record.template.md) only
   for a genuinely new record; amend an existing record for clarification or closure evidence.
2. Preserve one accountable owner and real evidence. Solo work does not require fabricated dissent.
   Distinguish lifecycle `status` from operating `light`; a passing schema does not make Yellow Green.
3. For replacement, preserve the predecessor's body and atomically mirror `supersedes` /
   `superseded_by`. The chain must end at an accepted record. Retirement without replacement has no
   successor. Do not rewrite historical IDs, filenames, or rationale to make the inventory look newer.
4. Validate the record, then regenerate only its affected index. Return the path, proof, and open
   conditions. New records use v2; historical v1 is not an escape hatch from authoring requirements.

```sh
python3 03_Agents-and-Skills/Skills/traffic-light-decisions/scripts/check_decision.py <record>
```

## Inspect the current contracts

```sh
python3 03_Agents-and-Skills/Skills/traffic-light-decisions/scripts/check_decision.py \
  00_Agentic-OS/decisions --canonical --json
```

This returns selected contract metadata and validation results, not historical bodies. The workspace
has six canonical ADRs, one per L0–L5, each declaring its `layer`. Read the relevant layer, not all six
by default. Keep mechanics and dated proof in their existing reference or run evidence.
`canonical: true` is an explicitly reviewed scope choice, not “accepted” or “important.”
Run `python3 00_Agentic-OS/agentic-os-review.py --contracts-only` to enforce exactly one per layer.
Use whole-corpus validation (`--repo-root .`) only for governance or migration work; the command and
compatibility rules are in the field reference.

## Learnings

Simplify task entrypoints and duplicated prose, not history or obligations. For example, shortening
an ADR still preserves its alternatives, reversal condition, and unchanged Yellow trigger/expiry.
A routine log rotation already captured in its runbook needs no second file; a new trust boundary
does need an ADR. Topic filenames improve navigation while stable IDs preserve supersession links.

When splitting an umbrella ADR, choose one primary successor and link the sibling owners explicitly;
do not invent multiple `superseded_by` targets. Transfer every open condition without changing its
deadline. A new responsibility map is not evidence that its runtime rollout has completed.
