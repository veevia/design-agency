# Context pull — index record shape, scoring signals, staleness

On-demand detail for the `context-pull` skill. `SKILL.md` carries the discipline; this file carries
the record shape, the scoring recap, and the staleness rules. The canonical weights live in the
prompt: [`02_Workflows/prompts/context-pull.prompt.md`](../../../../02_Workflows/prompts/context-pull.prompt.md).

## Why just-in-time retrieval

A wiki page costs roughly 2k–10k tokens to load; its index line costs about 30. Score the index,
pick the few pages that matter, then load bodies on demand. This is the lightweight-identifier
pattern from Anthropic's context-engineering guidance applied to a hub's `_wiki/`.

## The `index.jsonl` record

`python3 06_Engine/retrieval/build-wiki-index.py <hub>` writes one JSON object per wiki page:

```json
{"path": "_wiki/entities/vendor-a.md", "type": "entity",
 "title": "Vendor A", "tldr": "Alerting vendor; strong on regulation feeds, weak on news.",
 "tags": ["type/entity"], "sources": ["2026-01-10-vendor-demo"], "updated": "2026-01-12"}
```

## Scoring signals (recap)

| Signal | Weight | Rule |
|---|---:|---|
| TL;DR contains a query content word | 3 | substring match on `tldr` |
| Title contains a query content word | 2 | substring match on `title` |
| A tag contains a query content word | 2 | any `tags[*]` |
| A cited source slug contains a query word | 1 | any `sources[*]` |
| Evidence-rich page | 1 | evidence mix total ≥ 5 |
| Recently updated | 1 | `updated` within 90 days |

Ignore stopwords (`the, a, an, and, or, of, to, in, on, for, with, what, which, how, why, when, who`).

## Staleness rules

| Signal | Action |
|---|---|
| `index.jsonl` missing | Report it; offer to build the index |
| Older than the last `_wiki/log.md` entry | Treat as stale; rebuild before scoring |
| Older than 7 days | Warn; offer to rebuild |

## See also

- Skill: [`../SKILL.md`](../SKILL.md)
- Retrieval engine: [`06_Engine/retrieval/README.md`](../../../../06_Engine/retrieval/README.md)
- [Anthropic — effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
