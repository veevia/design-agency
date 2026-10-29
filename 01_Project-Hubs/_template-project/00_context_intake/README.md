# 00_context_intake

**TL;DR:** The hub's inbox for raw, immutable source material — meeting notes, transcripts, decks, exports — which the wiki distills and cites but never edits.

## What belongs here

- `YYYY-MM-DD-<slug>.md` — meeting notes, using §A of
  [`0-2-Ops_operating-rhythm.template.md`](../../../00_README/_templates/0-2-Ops_operating-rhythm.template.md).
- Decks, documents, spreadsheets, screenshots, sketches and their Markdown conversions. Sub-folder by kind
  (`decks/`, `data/`, `_assets/`) once volume grows.
- Recordings only per [CONVENTIONS §9](../../../00_README/CONVENTIONS.md#9-large-media): Git LFS, or external
  storage plus a small manifest. Transcripts and summaries stay here either way.
- `_drafts/` — raw pastes awaiting cleanup (git-ignored).

## Workflow

1. Drop the raw file here with a date-prefixed kebab-case name. Don't edit it afterwards — it's evidence.
2. Convert binary formats (PDF, Office, audio) to Markdown with
   [MarkItDown](../../../04_MCP/markitdown/README.md), saving the `.md` beside the original.
3. Run `/wiki-ingest 00_context_intake/<file>.md`: it writes a source summary, updates affected wiki pages,
   `_wiki/index.md` and `_wiki/log.md`.
4. Tag notes you author here with `#type/meeting`, `#project/<hub-slug>`, `#tenant/*` and `#status/*`.
5. Phase artifacts cite the wiki pages built from this material; they don't copy it.

## Customer content

Suffix customer-confidential files with `_TENANT.md` — Git ignores them by default
([CONVENTIONS §4](../../../00_README/CONVENTIONS.md#4-customer-data-labels)). In a customer hub, treat
everything here as confidential, and only process it with tools the customer approved.
