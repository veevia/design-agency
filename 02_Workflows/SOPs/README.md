# 02_Workflows/SOPs

**TL;DR:** An SOP is a machine-checkable workflow contract — trigger, owner, skills, prompts, artifacts, and done-when in front-matter — for an operation that recurs often enough that drift costs more than the contract.

## Why SOPs (in addition to W1–W5)

The W1–W5 narratives in [`../workflows/`](../workflows/) stay narrative. SOPs add three things:

1. **A contract the engine can lint.** `loads_skills`, `invokes_prompts`, and `produces_artifacts` are checked against the filesystem by `python3 06_Engine/harness/lint-sop.py`.
2. **A self-evolution target.** `/capability-spot` and `/workflow-audit` propose new SOPs into `_proposed/`.
3. **Agent binding.** Each SOP names its `owner_agent` and sub-agents — explicit context boundaries.

## When to write one

- The workflow is new (not one of W1–W5) and runs regularly.
- It produces an artifact worth checking.
- A one-off prompt does not already cover it.

## Structure

```
SOPs/
├── README.md
├── _template/SOP.md      # the canonical schema
├── _proposed/            # drafts awaiting owner approval (not linted)
└── <sop-id>/SOP.md
```

## Graduated SOPs

| ID | Title | Triggered by | Owner |
|---|---|---|---|
| [`capability-spot`](capability-spot/SOP.md) | Propose reusable capabilities from evidence | Recurring patterns in snapshots and run records | human-driven |
| [`optimization-loop`](optimization-loop/SOP.md) | Run a goal + rubric loop to a verified result | A ranked backlog item or initiative cycle | `goal-runner` |
| [`prototype-design`](prototype-design/SOP.md) | Brief → validated prototype through the PDG plug-in | A brief must become a functional, verified prototype | `prototype-runner-qa` |
| [`session-snapshot`](session-snapshot/SOP.md) | Compact a working session into a handoff | Session end or context pressure | human-driven |
| [`skill-refine`](skill-refine/SOP.md) | Refine a capability from its past-run signals | A recurring eval, lint, or reviewer failure | `skill-agent-smith` |
| [`video-production`](video-production/SOP.md) | Demo film through the VPG plug-in | A product demo film must be produced or revised | `demo-deck-producer` |
| [`workflow-audit`](workflow-audit/SOP.md) | Codify repeated manual work | A sequence repeated three or more times | human-driven |

The `prototype-design` and `video-production` SOPs are host adapters: they apply only while their plug-in is mounted (`python3 06_Engine/scripts/agency.py plugin status <name>`).

## Add a new SOP

1. Copy [`_template/SOP.md`](_template/SOP.md) to `<sop-id>/SOP.md` (or draft it in `_proposed/`).
2. Fill the required front-matter: `id`, `title`, `status`, `trigger`, `produces_artifacts`, `done_when`.
3. Declare `loads_skills` (bare skill slugs), `invokes_prompts` (prompt names), `owner_agent`, and `context_budget_tokens_max` as needed.
4. Run `python3 06_Engine/harness/lint-sop.py <sop-id>`.

## See also

- [`../workflows/`](../workflows/) — narrative workflows W1–W5 · [`../prompts/`](../prompts/) — `/` commands
- [`../../06_Engine/harness/skill-schema.md`](../../06_Engine/harness/skill-schema.md) — the analogous contract for skills
