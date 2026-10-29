---
type: wiki-page
subtype: template
purpose: skeleton for source summaries (one per ingested raw doc)
applies-skills:
  - ../../../../03_Agents-and-Skills/Skills/evidence-tagging
  - ../../../../03_Agents-and-Skills/Skills/extreme-clarity
  - ../../../../03_Agents-and-Skills/Skills/wiki-maintenance
---

# Source template — copy and rename

**TL;DR:** Skeleton for a source summary — one page per raw file ingested from `00_context_intake/`, which it cites and never edits.

Copy the block below to `_wiki/sources/YYYY-MM-DD-<slug>.md` (date prefix required) and replace the placeholders. `/wiki-ingest` does this for you.

```markdown
---
type: source
slug: <YYYY-MM-DD-slug>
origin: deck | transcript | vendor-doc | workshop | interview | spreadsheet | image | other
raw-path: ../../00_context_intake/<filename>   # immutable
ingested: YYYY-MM-DD
ingested-by: /wiki-ingest
evidence-default: observed | reported          # most facts from this source default to this label
touches-entities: []                           # filled during ingest
touches-concepts: []
---
# <Source title>

**TL;DR:** <one sentence — what does this source tell us we didn't already know?>.

## Origin
- **Type:** <deck | transcript | …>
- **Author / source:** <name or org>
- **Date of source:** <YYYY-MM-DD>
- **Raw file:** [`../../00_context_intake/<filename>`](../../00_context_intake/<filename>)

## Key facts extracted
- <claim> [observed | <this-source>]
- <claim> [reported | <this-source>]

## Affected wiki pages (touched by this ingest)
- Created: [[entities/...]], [[concepts/...]]
- Updated: [[entities/...]], [[syntheses/...]]

## Open questions surfaced
- <question>

## Quotes / verbatim (optional — for stakeholder positions)
> "<direct quote>" — <person, role>
```
