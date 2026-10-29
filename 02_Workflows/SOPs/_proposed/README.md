# `_proposed/` — SOP drafts awaiting graduation

**TL;DR:** `/capability-spot` and `/workflow-audit` write SOP stubs here; they stay here, outside the gates, until their owner approves graduation.

## Lifecycle

1. A prompt writes a stub at `_proposed/<sop-id>/SOP.md` from [`../_template/SOP.md`](../_template/SOP.md).
2. The owner reviews it, refines the front-matter, and fills the body.
3. On approval, move it next to the graduated SOPs: `git mv 02_Workflows/SOPs/_proposed/<sop-id> 02_Workflows/SOPs/<sop-id>`.
4. Run `python3 06_Engine/harness/lint-sop.py <sop-id>` to verify its references resolve.

`lint-sop.py` skips `_proposed/` and `_template/`, so half-formed drafts never fail the gate.

## See also

- [`../README.md`](../README.md) — the SOP concept and the graduated set
- [`/capability-spot`](../../prompts/capability-spot.prompt.md) · [`/workflow-audit`](../../prompts/workflow-audit.prompt.md)
