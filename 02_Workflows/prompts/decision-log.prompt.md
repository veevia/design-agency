---
description: "Reuse existing rationale or capture one durable decision through W5: search first, choose the smallest truthful record type (ADR, PDR, ops note, release), write it beside the work with Traffic Light posture separate from lifecycle, and validate it with check_decision.py."
agent: agent
---

# /decision-log

Follow [W5 — Decide](../../02_Workflows/workflows/W5-decide.md). Most requests are answered by pointing at existing evidence; write a record only for a new durable choice, an explicit capture request, or a lifecycle change.

## Inputs

- **decision** (required): the choice in one sentence, or the record whose lifecycle changes
- **hub** (optional): the hub and phase it governs; omit for OS-wide choices (`00_Agentic-OS/decisions/`)
- **evidence** (optional): links that support it

## Procedure

1. **Search first.** Read the relevant `decisions/` folders and the task evidence. If an existing record or note already carries the rationale, return its path and stop — routine fixes, settings, progress, and test results stay in their existing evidence.
2. **Load** [`traffic-light-decisions`](../../03_Agents-and-Skills/Skills/traffic-light-decisions/SKILL.md) only now, for the field reference and templates.
3. **Choose the smallest truthful type**:

   | What changed? | `record_type` |
   |---|---|
   | A durable system, trust, or cross-component boundary; an expensive reversal | `adr` |
   | A product, design, scope, or experience choice | `pdr` |
   | An operational action worth keeping beyond its runbook | `ops-note` |
   | A release attestation not already captured with the release | `release` |

4. **Write it beside the work** — `01_Project-Hubs/<hub>/<phase>/decisions/<descriptive-kebab>.md` — from the template router `03_Agents-and-Skills/Skills/traffic-light-decisions/assets/decision-record.template.md`, with `schema_version: decision-record/v2`, a stable id (`<hub-slug>-NNNN` in a hub, `aos-NNNN` for OS-wide records), one owner, honest `consultation` (`solo`, `invited`, `reviewed`), and real dates.
5. **Set posture separately from lifecycle**: `status` is `proposed`, `accepted`, `superseded`, or `retired`; `light` is 🟢 `green`, 🟡 `yellow` (with `trigger` and `expiry`), or 🔴 `red` (with `blocker` and `unblock_owner`).
6. **Amend instead of duplicating**: clarify or close a condition in the existing record; a reversal gets a successor with mirrored `supersedes` / `superseded_by` links and the predecessor's body preserved.
7. **Validate from disk**:
   ```sh
   python3 03_Agents-and-Skills/Skills/traffic-light-decisions/scripts/check_decision.py <record>
   ```

## Output format

```
Decision: reused | new | amended
Path: <relative path>
Record: <record_type> <id> · status <lifecycle> · light 🟢|🟡|🔴
Proof: check_decision.py → <n> error(s)
Open: <trigger + expiry | blocker + unblock owner | none>
```

## Never

- Create a record for routine execution, or a second file that restates an existing contract.
- Invent alternatives, dissent, approvals, or dates; solo consultation is valid.
- Treat a passing schema as approval, a closed Yellow, or proof that something shipped.
