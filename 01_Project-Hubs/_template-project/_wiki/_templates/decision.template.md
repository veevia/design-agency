---
type: wiki-page
subtype: template
purpose: route a wiki knowledge decision to the typed decision-record/v2 templates (no separate wiki format)
applies-skills:
  - ../../../../03_Agents-and-Skills/Skills/traffic-light-decisions
  - ../../../../03_Agents-and-Skills/Skills/house-principles
  - ../../../../03_Agents-and-Skills/Skills/alignment-playbook
---

# Decision template — use the typed records

**TL;DR:** A wiki decision is an ordinary typed decision record (`decision-record/v2`): reuse existing rationale first, then copy the smallest matching canonical template — there is no wiki-specific decision format.

A wiki decision captures a durable *knowledge* choice that later pages and artifacts must follow: a taxonomy, which
source is authoritative, a definition the team commits to. Routine ingests, edits and lint fixes need no record —
`log.md` covers them. Choices about a phase's artifacts belong in that phase's `decisions/` folder.

## 1. Reuse first

Search `index.md` (decision rows show ID, type, status and light) and the hub's phase `decisions/` folders. If the
rationale already exists, cite it and stop. [W5 — Decide](../../../../02_Workflows/workflows/W5-decide.md)
(`02_Workflows/workflows/W5-decide.md`) owns the procedure.

## 2. Copy the smallest truthful template

| The durable fact is… | Copy |
|---|---|
| A definition, taxonomy, scope or source-of-truth choice | [`pdr.template.md`](../../../../03_Agents-and-Skills/Skills/traffic-light-decisions/assets/pdr.template.md) |
| A system or data boundary, e.g. which tool is the system of record | [`adr.template.md`](../../../../03_Agents-and-Skills/Skills/traffic-light-decisions/assets/adr.template.md) |
| A reversible maintenance action worth keeping beyond `log.md` (a merge, rename or re-index) | [`ops-note.template.md`](../../../../03_Agents-and-Skills/Skills/traffic-light-decisions/assets/ops-note.template.md) |
| A release attestation (rare in a wiki) | [`release.template.md`](../../../../03_Agents-and-Skills/Skills/traffic-light-decisions/assets/release.template.md) |

Unsure? Start from the [template router](../../../../03_Agents-and-Skills/Skills/traffic-light-decisions/assets/decision-record.template.md).

## 3. File it

- Save as `_wiki/decisions/<descriptive-slug>.md` with `id: <hub-slug>-NNNN`. One ID namespace covers the whole
  hub — phase folders and wiki alike — and the index rejects duplicate IDs.
- Keep `status`, `light` and, when they apply, `trigger`, `expiry`, `blocker` and `unblock_owner` in front matter;
  the index and digest read them.
- Cite wiki pages as evidence with wiki links inside the record, e.g. `[[syntheses/<topic>]]` or
  `[[sources/<YYYY-MM-DD-slug>]]`.
- Record consultation honestly (`solo`, `invited`, `reviewed`); never invent dissent.
- Append a row to `log.md`, then validate:

```sh
python3 03_Agents-and-Skills/Skills/traffic-light-decisions/scripts/check_decision.py 01_Project-Hubs/<hub-slug>/_wiki/decisions/<file>.md
```
