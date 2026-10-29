---
description: "Read a hub's _wiki/index.jsonl and return the top-N candidate page paths for a query, before any page body is loaded."
agent: agent
---

# /context-pull

Just-in-time retrieval over a hub's wiki. Returns paths + 1-line summaries; the caller decides which pages to `read_file`.

## Inputs

- **hub** (required): folder slug under `01_Project-Hubs/` (e.g. `example-project`)
- **query** (required): natural-language description of what context is needed
- **n** (optional, default 5): number of candidates to return

## Procedure

1. **Load operating skills**:
   - `03_Agents-and-Skills/Skills/context-pull/SKILL.md`
   - `03_Agents-and-Skills/Skills/wiki-maintenance/SKILL.md`

2. **Read ONLY the index**, not page bodies:
   ```
   01_Project-Hubs/<hub>/_wiki/index.jsonl
   ```
   **Auto-refresh if stale.** Before scoring, compare the index's mtime against `_wiki/log.md`'s mtime. If the log was modified more recently OR the index doesn't exist, run:
   ```bash
   python3 06_Engine/retrieval/build-wiki-index.py <hub>
   ```
   This is non-optional. A stale index produces wrong rankings.

3. **Score each entry.** For each JSONL line, compute a score using these signals:

   | Signal | Weight | How |
   |---|---|---|
   | TL;DR contains query terms (lemmatized) | 3 | Substring match on any content word in `tldr` |
   | Title contains query terms | 2 | Substring match on `title` |
   | Tag contains query terms | 2 | Any `tags[*]` matches a query content word |
   | Sources cite query terms | 1 | Any `sources[*]` slug contains a content word |
   | Evidence-rich (sum of `evidence_mix`) | 1 | Bonus if total ≥ 5 |
   | Recency (updated within 90 days) | 1 | Compare `updated` against today |

   Stopwords to ignore: `the, a, an, and, or, of, to, in, on, for, with, what, which, how, why, when, who`.

4. **Sort descending by score; return top-N.** Tie-break by `updated` desc.

5. **Output shape:**
   ```
   === /context-pull <hub> "<query>" ===
   Top <n> candidates from <wiki> (<page count> indexed):

   1. <path>  [type] (score=<s>, updated=<date>)
      TL;DR: <tldr>
      Tags: <comma-separated>

   2. ...
   ```
   No page bodies. The caller decides which to `read_file`.

6. **Offer follow-up:** "Want me to read pages 1–3 into context?" or "Run `/wiki-query` on candidate N for a citation-grounded answer?"

## Targets / guardrails

- **Never load page bodies in this prompt.** That defeats the point.
- **Don't return more than N.** If fewer pages match meaningfully, return fewer and say so.
- **Don't fabricate scores.** If the JSONL is missing or empty, say so plainly.
- **Tag-only matches are weak signal.** Don't surface a page that matched only on a single tag with no TL;DR/title hit.

## When this goes wrong

- **index.jsonl missing or empty**: ask user to run `python3 06_Engine/retrieval/build-wiki-index.py <hub>`, then retry.
- **Query is too vague (1 word, common term)**: return top-3 with a note: "broad query; consider narrowing."
- **Hub has no `_wiki/`**: surface the project structure, suggest creating one or running `/wiki-ingest` first.

## Output format

```
=== /context-pull <hub> "<query>" ===
Found <n>/<total> candidates:

1. <path>  [<type>]
   TL;DR: <tldr>
   Updated: <date>  Tags: <tags>  Score: <s>

(...)

Next: read_file any candidate, or run /wiki-query for a synthesized answer.
```

## See also

- [`../../06_Engine/retrieval/build-wiki-index.py`](../../06_Engine/retrieval/build-wiki-index.py) — the indexer
- [`../../06_Engine/retrieval/README.md`](../../06_Engine/retrieval/README.md) — index schema
- [`../../03_Agents-and-Skills/Skills/context-pull/SKILL.md`](../../03_Agents-and-Skills/Skills/context-pull/SKILL.md) — how to consume the index
- [`wiki-query.prompt.md`](../../02_Workflows/prompts/wiki-query.prompt.md) — citation-grounded Q&A; consumes `/context-pull` candidates
