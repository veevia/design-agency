---
name: context-pull
title: Pull just-in-time context from a hub wiki index
description: "Score a hub's _wiki/index.jsonl against a question and return the top few page paths with one-line summaries — never page bodies — so the caller loads only what it needs. Use before answering a question that depends on wiki content, when the working context is filling up and needs a targeted refresh, or as the first step of /wiki-query and /wiki-ingest."
status: stable
when_to_load:
  - Before answering a question that depends on a hub's wiki content
  - When the working context is filling up and a targeted refresh of relevant pages is needed
  - As the first step of /wiki-query, /wiki-ingest, or a sub-agent research task
applies-to: retrieval over 01_Project-Hubs/<hub>/_wiki/ for any agent or prompt
narrative: 06_Engine/retrieval/README.md
contract-exempt: "retrieval discipline — scoring happens in the /context-pull procedure and 06_Engine/retrieval; there are no authored files for a regex lint to check"
inputs:
  - kind: wiki-index
    where: "01_Project-Hubs/*/_wiki/index.jsonl"
outputs:
  - kind: candidate-list
    schema: "Top-N {path, type, title, tldr, tags, updated, score}; no page bodies"
done_when:
  - The index was read once and no page body was loaded before scoring
  - The returned list has at most N entries, each with an explicit score
  - A stale or missing index was reported, not silently used
  - The caller was offered a concrete next step (read selected pages or run /wiki-query)
budget:
  context_tokens_max: 1500
---

# Context Pull

**TL;DR:** Read the wiki's index, score it against the question, and hand back the top few paths with their TL;DRs — load page bodies only after that choice.

## When to use

- A question depends on a hub's wiki and you do not yet know which pages matter.
- Context is getting crowded and you need a precise refresh, not a re-read.
- Skip it when the user names a file (just read it), when the wiki has five or fewer pages, or when the task needs every page (read `index.md`).

## Steps

1. **Check freshness.** If `01_Project-Hubs/<hub>/_wiki/index.jsonl` is missing, or older than the last `_wiki/log.md` entry, report it and offer `python3 06_Engine/retrieval/build-wiki-index.py <hub>`.
2. **Read only the index** — one JSON object per page (`path`, `type`, `title`, `tldr`, `tags`, `sources`, `updated`).
3. **Score each entry** with the weights in [`02_Workflows/prompts/context-pull.prompt.md`](../../../02_Workflows/prompts/context-pull.prompt.md) (TL;DR match 3, title 2, tags 2, sources 1, evidence-rich 1, recency 1).
4. **Return the top N** (default 5) sorted by score, ties broken by `updated`.
5. **Offer the next step**: read pages 1–3, or run `/wiki-query` on a candidate.

## Output format

```
=== /context-pull <hub> "<query>" ===
1. _wiki/syntheses/request-triage.md  [synthesis] (score=7, updated=2026-02-14)
   TL;DR: Keep the inventory system; show stock, service-contract and CRM data inline beside each request.
2. …
Next: read 1–2, or /wiki-query on #1.
```

## Watch-outs

- Loading ten page bodies "to get a feel" defeats the purpose.
- Never invent a TL;DR the index does not contain; say the index is thin instead.
- Do not return the whole index unsorted, or order by path.
- A tag-only match is weak; don't surface it without a title or TL;DR hit.

## See also

- Reference: [`references/REFERENCE.md`](references/REFERENCE.md) — index record shape, scoring signals, staleness rules
- `wiki-query` (consumes these candidates) · `wiki-maintenance` (index and log formats)
- Index builder: [`06_Engine/retrieval/build-wiki-index.py`](../../../06_Engine/retrieval/build-wiki-index.py)
