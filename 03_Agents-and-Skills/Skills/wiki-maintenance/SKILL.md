---
name: wiki-maintenance
title: Route wiki work and keep the wiki's shared formats
description: "Umbrella for every hub's _wiki/: route to wiki-ingest, wiki-query, or wiki-lint for the actual operation, and hold the shared architecture (immutable intake → agent-maintained wiki → cited artifacts), the index.md and log.md formats, the promotion gate, and the cross-hub rules. Use when setting up or restructuring a hub wiki, when you need the index or log format, when deciding whether something belongs in the wiki at all, or when unsure which wiki skill to load."
status: stable
when_to_load:
  - Setting up or restructuring a hub's _wiki/
  - Needing the index.md, index.jsonl, or log.md format
  - Deciding whether a source, answer, or note belongs in the wiki at all (the promotion gate)
  - Unsure which of wiki-ingest, wiki-query, or wiki-lint to load
applies-to: 01_Project-Hubs/<hub>/_wiki/ directories
narrative: 00_README/_frameworks/design-thinking-loop.md
inputs:
  - kind: raw-source
    where: "01_Project-Hubs/*/00_context_intake/**/*"
  - kind: wiki-page
    where: "01_Project-Hubs/*/_wiki/**/*.md"
outputs:
  - kind: wiki-update
    schema: "Pages under _wiki/{sources,entities,concepts,syntheses,decisions}/ only when the promotion gate passes, plus an index.md row and an append-only log.md entry"
done_when:
  - Every ingest wrote the smallest sufficient update, refreshed index.md, and appended to log.md
  - Every query read index.md before page bodies and cited wiki pages
  - Every lint run produced a severity-ranked triage table
  - Nothing was written into 00_context_intake/, and no page duplicates its raw source
lints:
  - id: wiki-page-missing-tldr
    severity: warning
    where: "01_Project-Hubs/[!_]*/_wiki/{entities,concepts,syntheses}/**/*.md"
    pattern: "^#\\s"
    must_also_match: "\\*\\*TL;DR"
    message: "Wiki knowledge page has no TL;DR (extreme-clarity)."
  - id: wiki-index-stale-marker
    severity: info
    where: "01_Project-Hubs/[!_]*/_wiki/index.md"
    pattern: "(?i)last updated"
    message: "Confirm index.md 'Last updated' reflects the latest ingest (rebuild with 06_Engine/retrieval/build-wiki-index.py)."
budget:
  context_tokens_max: 3000
---

# Wiki Maintenance

**TL;DR:** Each hub keeps one agent-maintained wiki between its immutable intake and its artifacts; load `wiki-ingest`, `wiki-query`, or `wiki-lint` to do the work, and this skill for the shared formats and rules.

## When to use

| Operation | Load | Goal |
|---|---|---|
| Ingest | `wiki-ingest` | raw source → tagged source page + selective updates + index/log |
| Query | `wiki-query` | question → cited answer (index first; `context-pull` for scoring) |
| Lint | `wiki-lint` | wiki → severity-ranked debt triage |
| Formats, architecture, promotion gate | this skill | the shared reference below |

## Steps

1. **Know the layers** of a hub:

   ```
   01_Project-Hubs/<hub>/
   ├── 00_context_intake/   RAW — immutable; agents read, never write
   ├── _wiki/               SEMANTIC MAP — agent-maintained; cites intake and working files
   │   ├── index.md         catalog + current-phase block (entry point)
   │   ├── index.jsonl      machine index for context-pull
   │   ├── log.md           append-only operation log
   │   ├── _templates/      page skeletons
   │   ├── entities/  concepts/  sources/  syntheses/  decisions/
   └── 01_understand/ … 04_learn/   ARTIFACTS — cite the wiki
   ```

2. **Apply the promotion gate** before writing any page: write only when it reduces retrieval ambiguity, anchors a durable entity or concept, records a decision, or synthesizes repeated evidence. Otherwise report and stop.
3. **Keep the index current** — hand-edit `index.md` rows or rebuild the machine index with `python3 06_Engine/retrieval/build-wiki-index.py <hub>`.
4. **Append to the log** after every ingest, filed query, lint, or session snapshot.
5. **Keep hubs separate**: each hub has its own wiki; insights that recur across hubs graduate to `00_README/_frameworks/` or a skill, never by copying pages between hubs.

## Output format

`index.md` skeleton: [`assets/index.template.md`](assets/index.template.md). Log entries:

```markdown
## [2026-02-14 10:05] ingest | 2026-02-03-coordinator-interviews
- Pages created: sources/2026-02-03-coordinator-interviews.md
- Pages updated: entities/lead-coordinator.md, index.md
- Open questions: Does Site C see the same request volume?

## [2026-02-14 11:20] query | "Which booking channel brings the most urgent requests?" → filed as syntheses/urgent-request-channels.md

## [2026-02-20 09:00] lint
- Discipline: 3 (1 untagged claim, 1 Yellow without trigger, 1 missing TL;DR) · Structural: 2 orphans
```

## Watch-outs

- Ingesting without confirming the framing first causes rewrites.
- Writing into `00_context_intake/` breaks provenance — it is immutable.
- Duplicating a source inside a wiki page instead of summarizing and citing it.
- Optimizing for page count; more pages are not a healthier wiki.
- Skipping the log makes the wiki's evolution invisible.

## See also

- `wiki-ingest` · `wiki-query` · `wiki-lint` · `context-pull` · `evidence-tagging` · `extreme-clarity`
- Retrieval engine: [`06_Engine/retrieval/README.md`](../../../06_Engine/retrieval/README.md)
- Hub template wiki: `01_Project-Hubs/_template-project/_wiki/`
