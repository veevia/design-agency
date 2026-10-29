---
name: wiki-ingest
title: Ingest one raw source into a hub wiki
description: "Turn one raw source (a deck, transcript, vendor document, export, or clipped URL) into the smallest sufficient wiki update — a sources/ summary with evidence-tagged facts, selective entity and concept updates that pass the promotion gate, an index row, and an append-only log entry — without ever modifying the raw file. Use when ingesting a file from a hub's 00_context_intake/ into its _wiki/, when promoting meeting notes or research exports into a durable source page, or when running /wiki-ingest."
status: stable
when_to_load:
  - Ingesting a file from a hub's 00_context_intake/ into its _wiki/
  - Promoting meeting notes, research exports, or clipped pages into a durable source page
  - Running the /wiki-ingest prompt
applies-to: 01_Project-Hubs/<hub>/_wiki/ ingest operations
narrative: 00_README/_frameworks/design-thinking-loop.md
inputs:
  - kind: raw-source
    where: "01_Project-Hubs/*/00_context_intake/**/*"
outputs:
  - kind: wiki-ingest-result
    schema: "_wiki/sources/<YYYY-MM-DD>-<slug>.md (TL;DR, origin, raw-path, evidence-tagged facts) + selective entity/concept/synthesis updates + an index.md row + an append-only log.md entry"
done_when:
  - The framing was confirmed with the user before any wiki file was written
  - A sources/ page exists with a TL;DR, its origin, a raw-path, and evidence-tagged key facts
  - Entity and concept pages were created or appended only when durable enough to reuse, each listing the new source
  - index.md and log.md were both updated; 00_context_intake/ is unchanged
lints:
  - id: source-page-missing-tldr
    severity: warning
    where: "01_Project-Hubs/[!_]*/_wiki/sources/**/*.md"
    pattern: "^#\\s"
    must_also_match: "\\*\\*TL;DR"
    message: "Ingested source page has no TL;DR (extreme-clarity)."
  - id: source-page-missing-raw-path
    severity: warning
    where: "01_Project-Hubs/[!_]*/_wiki/sources/**/*.md"
    pattern: "^type:\\s*source\\b"
    must_also_match: "^(raw-path|origin):\\s*\\S"
    message: "Source page should name where it came from (raw-path: or origin:) so claims can be traced to the raw file."
budget:
  context_tokens_max: 3000
loads: [evidence-tagging, extreme-clarity]
---

# Wiki Ingest

**TL;DR:** Read one raw source end to end, confirm the framing, then write the smallest wiki change that makes it findable and citable — a tagged source page, selective entity updates, an index row, and a log entry.

## When to use

- A new file landed in `<hub>/00_context_intake/`.
- Notes from a meeting or workshop should become citable evidence.
- You are running `/wiki-ingest`.

Part of the wiki trio (`wiki-ingest` · `wiki-query` · `wiki-lint`); `wiki-maintenance` holds the shared formats.

## Steps

1. **Read the source end to end.** For binaries without a readable export, ask for one (the `04_MCP/markitdown/` adapter can convert documents); never invent content.
2. **Discuss 1–3 key takeaways** with the user and confirm the framing before writing.
3. **Apply the promotion gate.** Write wiki pages only when the source reduces retrieval ambiguity, anchors a durable entity or concept, records a decision, or synthesizes repeated evidence. Otherwise report and stop.
4. **Create `_wiki/sources/<YYYY-MM-DD>-<slug>.md`** from [`assets/source-page.template.md`](assets/source-page.template.md): TL;DR, origin, `raw-path`, evidence-tagged facts, touched pages, open questions.
5. **Touch durable pages only**: append tagged facts to existing entity or concept pages and add the source to their `sources:`; create a new page only if it will be reused.
6. **Update `index.md`** and **append to `log.md`**: `## [YYYY-MM-DD HH:MM] ingest | <source-slug>` with pages created, pages updated, and open questions.
7. **Surface follow-ups**: contradictions with existing pages, gaps, and the next source worth ingesting.

## Output format

```
✓ Ingest complete: 2026-02-03-coordinator-interviews
  Created: sources/2026-02-03-coordinator-interviews.md
  Updated: entities/lead-coordinator.md, index.md, log.md
  Open questions: Does Site C see the same request volume?
  Suggested next ingest: 00_context_intake/2026-02-05-booking-export.csv
```

## Watch-outs

- **Never write into `00_context_intake/`** — it is immutable raw intake.
- **Don't duplicate the source** — summarize, extract, and cite the raw file.
- **More pages are not healthier** — a related batch usually becomes one source page plus selective updates.
- **Contradictions are surfaced, not overwritten** — log them and let the user choose.
- **Sensitive sources** stay in their hub; don't copy confidential content into cross-hub pages.

## See also

- `wiki-maintenance` (architecture, index and log formats) · `wiki-query` · `wiki-lint` · `evidence-tagging` · `extreme-clarity`
- Prompt: [`/wiki-ingest`](../../../02_Workflows/prompts/wiki-ingest.prompt.md)
