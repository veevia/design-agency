---
name: decision-capture
title: Capture a durable decision as a typed, linked record
description: "Decide whether a choice needs a record at all, reuse existing rationale when it does not, and otherwise capture the smallest truthful typed record (ADR, PDR, ops note, or release) through W5, beside the work it governs. Use when someone asks to log or capture a decision, when a choice changes what future work must follow, or when an existing record's lifecycle changes (accepted, superseded, retired)."
status: stable
when_to_load:
  - Someone asks to log, record, or capture a decision
  - A choice among options changes constraints that future work must follow
  - A material action should survive chat and become searchable project memory
  - An existing decision is being clarified, superseded, or retired
applies-to: material decisions, recommendations, maintenance actions, and release attestations in any hub or in 00_Agentic-OS
inputs:
  - kind: decision-record
    where: "{00_Agentic-OS,01_Project-Hubs}/**/decisions/*.md"
outputs:
  - kind: decision-reference
    schema: "Either the path of existing evidence that already answers the question, or one decision-record/v2 file with record_type, stable id, lifecycle status, owner, consultation, and dates"
done_when:
  - Existing decisions and task evidence were searched before anything was written
  - A new record exists only for a new durable choice, an explicit capture request, or a lifecycle change
  - The record uses the smallest truthful record_type and sits beside the work it governs
  - The record passes check_decision.py from disk; reused evidence needs no duplicate file
  - The answer returns the path, the decision and its Traffic Light, the proof, and any open condition
lints:
  - id: v2-record-missing-type
    severity: warning
    where: "{00_Agentic-OS,01_Project-Hubs}/**/decisions/*.md"
    pattern: "^schema_version:\\s*decision-record/v2\\b"
    must_also_match: "^record_type:\\s*(adr|pdr|ops-note|release)\\b"
    message: "A decision-record/v2 file must declare record_type: adr | pdr | ops-note | release (see W5)."
budget:
  context_tokens_max: 1600
loads: [traffic-light-decisions]
---

# Decision Capture

**TL;DR:** Most "log this decision" requests are answered by pointing at existing evidence; write a new typed record only when a durable choice changes what future work must follow.

## When to use

- Someone says "log this", "capture the decision", or "write an ADR".
- A trade-off was settled and later work must respect it.
- A record changes state: a Yellow closes, a choice is reversed, or a record is retired.

## Steps

1. **Search first.** Read the hub's `decisions/` folders and the task evidence. If an existing record or note already carries the rationale, return its path and stop.
2. **Apply the W5 test.** Write only for a new durable choice, an explicit capture request, or a lifecycle change. Routine fixes, settings, progress, and test results stay in task or release evidence.
3. **Pick the smallest truthful type** — `adr` (system or trust boundary, expensive reversal), `pdr` (product, design, scope, experience), `ops-note` (operational action worth retaining), `release` (attestation not already captured).
4. **Write it beside the work** (`<hub>/<phase>/decisions/` or `00_Agentic-OS/decisions/` for OS-wide choices) from the template router in `traffic-light-decisions`, keeping one owner and honest consultation (`solo`, `invited`, `reviewed`).
5. **Validate from disk**: `python3 03_Agents-and-Skills/Skills/traffic-light-decisions/scripts/check_decision.py <record>`.
6. **Return** the path, decision, Traffic Light, validation result, and open conditions.

## Output format

```
Decision: reused | new | amended
Path: <relative path>
Record: <record_type> <id> · status <lifecycle> · light 🟢|🟡|🔴
Proof: check_decision.py → <n> error(s)
Open: <trigger + expiry, or blocker + unblock owner, or none>
```

## Watch-outs

- "Capture" often means *link an existing fact*; a second file for the same contract is drift.
- Lifecycle (`proposed → accepted → superseded | retired`) is separate from the Traffic Light; a passing schema does not turn Yellow into Green.
- Never invent alternatives or dissent to fill a template; solo consultation is valid.
- Never renumber or rewrite history to make an index look tidy.

## See also

- `traffic-light-decisions` — field reference, templates, and the validator
- Workflow: [W5 — Decide](../../../02_Workflows/workflows/W5-decide.md) · Prompt: [`/decision-log`](../../../02_Workflows/prompts/decision-log.prompt.md)
- `alignment-playbook` — consultation and named disagreement
