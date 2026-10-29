# `[Project Name]` Wiki

**TL;DR:** The hub's LLM-maintained knowledge base: it distills `00_context_intake/` raw sources into reusable entities, concepts, sources, syntheses and knowledge decisions that every phase artifact cites.

## How this wiki works

This is an LLM-maintained wiki. Agents maintain it with the
[`wiki-maintenance`](../../../03_Agents-and-Skills/Skills/wiki-maintenance/SKILL.md) skill
(`03_Agents-and-Skills/Skills/wiki-maintenance/SKILL.md`).

```
_wiki/
├── README.md         ← this file
├── index.md          ← generated catalog of every page (read this first)
├── index.jsonl       ← generated, agent-readable index (one line per page)
├── _digest.md        ← generated top-of-mind summary for agents
├── log.md            ← append-only operation log (ingest / query / lint)
├── _templates/       ← page skeletons; copy when creating a page
├── entities/         ← people, teams, vendors, systems, personas
├── concepts/         ← capabilities, architectures, taxonomies, methods
├── sources/          ← one summary per ingested raw source
├── syntheses/        ← evolving topic theses — where the POV lives
└── decisions/        ← typed decision records about knowledge (taxonomy, sources of truth)
```

Page folders appear on first ingest. Never hand-edit the generated files; edit pages and regenerate
(`06_Engine/retrieval/build-wiki-index.py`, `06_Engine/retrieval/build-wiki-digest.py`; the commit hook
refreshes the index for staged wiki changes).

## The operations

| Command | What it does |
|---|---|
| `/wiki-ingest <source-path>` | Reads a source from `../00_context_intake/`, writes a source summary, updates affected entity and concept pages, the index and the log |
| `/wiki-query "<question>"` | Reads `index.md` first, drills into relevant pages, answers with citations, offers to file the answer as a synthesis |
| `/wiki-lint` | Runs discipline and structure checks; returns a triage table |
| `/context-pull <hub-slug> "<query>"` | Pulls the smallest relevant set of pages (via `06_Engine/retrieval/wiki-neighbors.py`) into a task |

Prompts live in [`02_Workflows/prompts/`](../../../02_Workflows/prompts/).

## The rules

1. **Wiki pages cite `../00_context_intake/` files; they never modify them.** Raw is immutable.
2. **Artifacts in `../01_understand/`, `../02_design/` … cite wiki pages.** They don't restate them.
3. **Every claim carries an evidence tag** (`observed`, `reported`, `assumed`).
4. **Every page has a one-sentence TL;DR**, conclusion first.
5. **Decisions are typed records.** `decisions/` here holds knowledge choices (a taxonomy, a source of truth,
   a definition) using the same `decision-record/v2` model and `<hub-slug>-NNNN` IDs as the phase
   `decisions/` folders — see [`_templates/decision.template.md`](_templates/decision.template.md). Yellow
   without a trigger and expiry is rejected.

## See also

- [`index.md`](index.md) — the catalog (read this first)
- [`log.md`](log.md) — what happened and when
- [`_digest.md`](_digest.md) — what an agent should know at session start
