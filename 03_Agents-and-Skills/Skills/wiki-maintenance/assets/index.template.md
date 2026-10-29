# <Hub> Wiki — Index

**Last updated:** YYYY-MM-DD by `/wiki-ingest`
**Pages:** <n> entities · <n> concepts · <n> sources · <n> syntheses · <n> decisions

<!--
  The index is the agent's ENTRY POINT: a query reads index.md first, then drills into the few named
  pages. Rebuild the machine index (index.jsonl) after any ingest:
    python3 06_Engine/retrieval/build-wiki-index.py <hub>
  Replace each backticked wiki-link placeholder below with a real link when the page exists.
-->

## Current loop phase

**Phase:** Frame | Understand | Design | Build | Learn
**Entered:** YYYY-MM-DD
**Evidence supporting the next gate:**
- `[[syntheses/<topic>]]`
- `[[sources/<source-slug>]]`
- `[[entities/<persona-slug>]]`

## Entities
| Page | One-line | Last updated | Sources |
|---|---|---|---|
| `[[entities/<slug>]]` | <one-line> | YYYY-MM-DD | <n> |

## Concepts
| Page | One-line | Last updated | Sources |
|---|---|---|---|
| `[[concepts/<slug>]]` | <one-line> | YYYY-MM-DD | <n> |

## Syntheses (the evolving thesis)
| Page | TL;DR | Sources cited | Last updated |
|---|---|---|---|
| `[[syntheses/<slug>]]` | <thesis> | <n> | YYYY-MM-DD |

## Sources (raw → summarized)
| Page | Origin | Ingested |
|---|---|---|
| `[[sources/<YYYY-MM-DD>-<slug>]]` | <deck / transcript / vendor doc> | YYYY-MM-DD |

## Decisions
| Record | Light | Owner | Updated |
|---|---|---|---|
| `[[decisions/<slug>]]` | 🟢 / 🟡 / 🔴 | <name> | YYYY-MM-DD |
