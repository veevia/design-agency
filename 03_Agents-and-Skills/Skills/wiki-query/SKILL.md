---
name: wiki-query
title: Answer a question from a hub wiki with citations
description: "Answer a question from a hub's wiki by reading index.md first, drilling into only the few relevant pages, and citing a wiki page for every claim — then offer to file a non-trivial answer as a synthesis page and surface the gaps when the wiki can't answer. Use when answering a question that depends on a hub's wiki content, when deciding whether to file an answer as a synthesis, or when running /wiki-query."
status: stable
when_to_load:
  - Answering a question that depends on a hub's wiki content
  - Deciding whether to file a non-trivial answer as a synthesis page
  - Running the /wiki-query prompt
applies-to: 01_Project-Hubs/<hub>/_wiki/ query operations
narrative: 06_Engine/retrieval/README.md
inputs:
  - kind: wiki-index
    where: "01_Project-Hubs/*/_wiki/index.md"
  - kind: wiki-page
    where: "01_Project-Hubs/*/_wiki/{entities,concepts,sources,syntheses}/**/*.md"
outputs:
  - kind: cited-answer
    schema: "TL;DR + answer where every claim cites a wiki page and carries its evidence tag; optionally filed as _wiki/syntheses/<slug>.md with an index row and a log entry"
done_when:
  - index.md (or index.jsonl via context-pull) was read before any page body
  - Every claim in the answer cites a wiki page and carries its evidence tag forward
  - A non-trivial answer was offered for filing as a synthesis; gaps were listed when the wiki could not answer
  - Contradictions between pages were surfaced, not silently resolved
lints:
  - id: synthesis-missing-tldr
    severity: warning
    where: "01_Project-Hubs/[!_]*/_wiki/syntheses/**/*.md"
    pattern: "^#\\s"
    must_also_match: "\\*\\*TL;DR"
    message: "Filed synthesis has no TL;DR (extreme-clarity)."
budget:
  context_tokens_max: 2500
loads: [context-pull, evidence-tagging]
---

# Wiki Query

**TL;DR:** Read the index, open only the pages that matter, cite a page for every claim, and offer to file the answer as a synthesis when it is worth keeping.

## When to use

- A question depends on what a hub already knows.
- A stakeholder asks for a comparison or recommendation the wiki can support.
- You are running `/wiki-query`.

Part of the wiki trio (`wiki-ingest` · `wiki-query` · `wiki-lint`); pair with `context-pull` to score the index before loading bodies.

## Steps

1. **Read `index.md` first** (or run `context-pull` on `index.jsonl`). Never read the whole wiki blindly.
2. **Open the few relevant pages.** Follow wiki links one hop; two only if the first level is insufficient.
3. **Answer with citations**: TL;DR first; every claim cites a page by relative path and keeps its evidence tag; mark any position you take as a point of view (`house-principles`).
4. **Offer to file** a non-trivial answer (a table, comparison, or recommendation) as `_wiki/syntheses/<slug>.md`; if accepted, add the index row and a log entry.
5. **Surface gaps**: missing pages, sources not yet ingested, undefined concepts.

## Output format

```markdown
**TL;DR:** <one-sentence answer>.

**Detail:** <claims, each citing a wiki page, e.g. ../_wiki/entities/vendor-a.md, with its evidence tag>

**Point of view (if taken):** <position>
**Evidence quality:** <observed / reported / assumed mix>
**Gaps:** <missing pages or sources, or "none">
**File as `_wiki/syntheses/<slug>.md`? (y/n)**
```

## Watch-outs

- Reading every page "to get a feel" wastes context — score the index first.
- An uncited wiki answer is indistinguishable from a guess.
- Not every answer deserves a synthesis; ephemeral answers stay in chat.
- Verbatim quotes live in the raw intake; say so and point to the source page.

## See also

- `context-pull` · `wiki-maintenance` · `wiki-ingest` · `wiki-lint` · `evidence-tagging`
- Prompt: [`/wiki-query`](../../../02_Workflows/prompts/wiki-query.prompt.md)
