---
type: source
slug: <YYYY-MM-DD>-<source-slug>
origin: <deck | transcript | vendor-doc | export | url>
raw-path: <relative path into 00_context_intake/ — the immutable raw file this summarizes>
ingested: <YYYY-MM-DD>
ingested-by: /wiki-ingest
evidence-default: reported          # a source page is self-citing; its slug IS the source
touches-entities: [<entity-slug>]
touches-concepts: [<concept-slug>]
tags: [type/source, status/ingested]
---
# <Source title>

**TL;DR:** <one sentence — what this source is and the single most important thing in it>.

## Origin

<what it is, who produced it, when. Link the raw file via raw-path; summarize and extract, never
paste the full content.>

## Key extracted facts

- <fact> [reported | <this-slug>]
- <fact a second source corroborates> [observed | <this-slug>, <other-slug>]
- <a hypothesis this source raises> [assumed]
  - cheapest test: <experiment>

## Touches

- Entities: `[[entities/<slug>]]`
- Concepts: `[[concepts/<slug>]]`

## Open questions surfaced

- <contradiction, gap, or follow-up this ingest revealed>

<!--
  After writing: add the row to _wiki/index.md, append the ingest entry to _wiki/log.md, and touch
  only durable entity/concept pages the promotion gate justifies.
  VALIDATE: python3 03_Agents-and-Skills/Skills/evidence-tagging/scripts/check_tags.py <this-file>
-->
