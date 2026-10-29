# 01_Project-Hubs

**TL;DR:** One self-contained folder per project, each created from `_template-project/` and filed against the Understand → Design → Build → Learn loop; the blank template ships with no hubs but the skeleton.

## What belongs here

- `<project-slug>/` — one hub per project, customer engagement or internal initiative.
- `_template-project/` — the skeleton every hub is copied from. Improve it here so future hubs inherit the change.
- Nothing else: in `mode: template` (see `agency.yaml`) this folder holds only this README and the skeleton.

## Create a hub

```sh
python3 06_Engine/scripts/agency.py hub new <project-slug>
```

This copies `_template-project/` to `01_Project-Hubs/<project-slug>/` and switches `agency.yaml` from
`mode: template` to `mode: workspace`, because the repository now holds project work. Manual fallback:

```sh
cp -R 01_Project-Hubs/_template-project 01_Project-Hubs/<project-slug>
# then set `mode: workspace` in agency.yaml
```

Then follow the [hub skeleton's setup checklist](_template-project/README.md#setup-checklist): owner, goal
and current phase in the hub README; the initiative intake; the problem frame; Understand.

## Where things go inside a hub

| Put… | In… |
|---|---|
| Raw input — transcripts, decks, exports | `00_context_intake/` (immutable; the wiki cites it) |
| Distilled knowledge — entities, concepts, syntheses | `_wiki/` |
| Phase artifacts | `01_understand/` · `02_design/` · `03_build/` · `04_learn/` |
| Durable decisions | The `decisions/` folder of the phase they govern ([W5](../02_Workflows/workflows/W5-decide.md)) |
| Engine projects — a PDG prototype, a VPG film | A hub phase folder, e.g. `01_Project-Hubs/<hub>/03_build/<name>/`; the engine keeps its state there |
| Weekly status | `weekly-status/` — opt-in; create it only for a real reporting cadence |

## Naming and data

- Hub slugs are short lowercase kebab-case (`example-project`, `pilot-project`) and double as the
  `#project/*` tag and the decision ID namespace (`example-project-0001`).
- Treat a customer hub's whole subtree as customer content; label confidential files `_TENANT.md`, which Git
  ignores by default ([CONVENTIONS §4](../00_README/CONVENTIONS.md#4-customer-data-labels)).
- Retire a finished hub in place (`status: archived` in its README) or remove it; Git history keeps it.

## Related

- [How we work](../00_README/HOW-WE-WORK.md) — the loop, the task procedure and the three rules
- [Template catalog](../00_README/_templates/README.md) — artifacts to copy into phase folders
- [Workflows](../02_Workflows/README.md) — W1–W5 and the prompts that draft each artifact
