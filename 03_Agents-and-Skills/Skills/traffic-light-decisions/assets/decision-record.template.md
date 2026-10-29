# Decision record template router

First follow [W5](../../../../02_Workflows/workflows/W5-decide.md): reuse existing rationale or task
evidence when sufficient. Copy a template only for a new durable choice or an explicit capture request.
Then choose the smallest record that matches:

| If the durable fact is… | Copy |
|---|---|
| a system boundary, trust boundary, cross-component architecture, or expensive reversal | [`adr.template.md`](adr.template.md) |
| a product, design, scope, or experience choice | [`pdr.template.md`](pdr.template.md) |
| a reversible setting, incident response, maintenance action, or cleanup | [`ops-note.template.md`](ops-note.template.md) |
| a promotion, launch, or release attestation | [`release.template.md`](release.template.md) |

Do not default to ADR or create a duplicate file for routine work. Architectural scope tells you to
choose `record_type: adr`. `canonical: true` is rarer still: use it only when an accepted ADR belongs
to the current architecture contract set. The workspace deliberately keeps six ADRs, one per L0–L5;
this is not a quota for projects or tasks. Amend the owning layer or review its successor; do not
automatically promote another canonical record. Validate the completed copy with:

```sh
python3 03_Agents-and-Skills/Skills/traffic-light-decisions/scripts/check_decision.py <file>
```
