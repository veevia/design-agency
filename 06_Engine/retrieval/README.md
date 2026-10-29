# Retrieval — wiki index + just-in-time context pull

Two pieces:

- **`build-wiki-index.py`** — scans every `01_Project-Hubs/*/_wiki/` and emits an agent-readable `index.jsonl` plus a human-readable `index.md` for that program.
- **`/context-pull`** prompt (in [`../../02_Workflows/prompts/`](../../02_Workflows/prompts/)) — reads the JSONL index, scores by query, returns top-N candidate page paths *before* any page body is loaded.

This implements the "just-in-time retrieval" pattern (lightweight identifiers, full content loaded on demand) — see [Anthropic — context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

## What goes in the index

Each line of `index.jsonl` is one wiki page:

```json
{"path":"entities/operations-manager.md","type":"entity","title":"Operations manager","tldr":"Wants urgent-job counts before the weekly review","tags":["#status/draft","#project/example-project"],"sources":["2026-02-03-vendor-demo"],"updated":"2026-02-10","evidence_mix":{"observed":4,"reported":2,"assumed":1}}
```

Fields:
- `path` — wiki-relative path (no program prefix)
- `type` — `entity` | `concept` | `source` | `synthesis` | `decision` (from front-matter or folder)
- `title` — first `# ` heading
- `tldr` — text after `**TL;DR:**` (≤200 chars)
- `tags` — front-matter `tags:` + first-line hashtags in body
- `sources` — front-matter `sources:`
- `updated` — front-matter `updated:` or file mtime
- `evidence_mix` — counts of `[observed]`, `[reported]`, `[assumed]` in body

## How to regenerate

```bash
python 06_Engine/retrieval/build-wiki-index.py            # all programs
python 06_Engine/retrieval/build-wiki-index.py example-project   # one hub (folder slug)
```

Outputs:
- `01_Project-Hubs/<program>/_wiki/index.jsonl`
- `01_Project-Hubs/<program>/_wiki/index.md` (derived; grouped by type)

## When to regenerate

- As the final step of `/wiki-ingest` and `/wiki-lint` (will be wired in Phase 2 polish)
- On demand when several wiki pages have been edited outside the ingest flow
- Before invoking `/context-pull` if you suspect the index is stale

## See also

- [`../../02_Workflows/prompts/context-pull.prompt.md`](../../02_Workflows/prompts/context-pull.prompt.md) — the agent-facing retrieval prompt
- [`../../03_Agents-and-Skills/Skills/context-pull/SKILL.md`](../../03_Agents-and-Skills/Skills/context-pull/SKILL.md) — how an agent should consume index.jsonl
- [`../../03_Agents-and-Skills/Skills/wiki-maintenance/SKILL.md`](../../03_Agents-and-Skills/Skills/wiki-maintenance/SKILL.md)
