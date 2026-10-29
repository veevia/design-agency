---
description: "Answer a question by reading the wiki's index first, drilling into relevant pages, citing claims, and offering to file the answer as a new synthesis page."
agent: agent
---

# /wiki-query

Ask a question of a hub's `_wiki/`. The agent reads the wiki, not the raw sources.

## Inputs

- **question** (required): the question to answer.
- **hub** (optional): folder slug under `01_Project-Hubs/`. If absent, infer from the open file or ask.

## Procedure

1. **Load operating skills**:
   - `03_Agents-and-Skills/Skills/wiki-maintenance/SKILL.md`
   - `03_Agents-and-Skills/Skills/extreme-clarity/SKILL.md`
   - `03_Agents-and-Skills/Skills/evidence-tagging/SKILL.md`
   - `03_Agents-and-Skills/Skills/house-principles/SKILL.md` (for synthesis-style answers)

2. **Read `<hub>/_wiki/index.md` first.** Identify relevant pages by name/category. Do not search the whole wiki blindly.

3. **Drill into relevant pages.** Follow `[[wiki-link]]` references one hop at most before synthesizing. Two hops only if the first level is insufficient.

4. **Synthesize an answer with citations.**
   - Start with a TL;DR (one sentence, conclusion-first).
   - Every claim cites a wiki page by relative path: `[[entities/X]]`, `[[concepts/Y]]`, `[[sources/Z]]`.
   - Carry forward evidence tags from the cited pages (`observed`/`reported`/`assumed`).
   - If you take a position, mark it as a point of view (`house-principles` principle 1).

5. **Offer to file the answer.** If the answer is non-trivial (table, comparison, novel insight, recommendation), ask:
   > "Should I file this as `<hub>/_wiki/syntheses/<slug>.md`?"
   
   If the user accepts:
   - Write to `<hub>/_wiki/syntheses/<slug>.md` using the synthesis template.
   - Update `index.md` to add the new synthesis row.
   - Append to `log.md`: `## [YYYY-MM-DD HH:MM] query | "<question>" → filed as syntheses/<slug>`

6. **Surface gaps.** If a question can't be answered well, list what's missing:
   - Pages that should exist but don't
   - Sources not yet ingested that would help
   - Concepts referenced but undefined

## Output format

```
**TL;DR:** <one-sentence answer>.

**Detail:**
<paragraph(s) with [[wiki-links]] for every claim>

**POV (if taken):** <position>

**Evidence quality:** <observed | reported | assumed mix>

**Gaps:** <list of missing pages/sources, or "none">

**Should I file this as syntheses/<slug>.md? (Y/n)**
```

## When this goes wrong

- **Question requires raw-source reading** (e.g., "what did the sponsor say verbatim?"): note that the wiki is summarized; offer to open the relevant `sources/<slug>.md` page or the raw file in `00_context_intake/`.
- **Wiki is empty / barely seeded**: tell the user; recommend `/wiki-ingest` on the highest-value source first.
- **Multiple wiki pages contradict**: surface the contradiction and ask the user to resolve before answering. Don't pick silently.

## See also

- [`wiki-ingest.prompt.md`](../../02_Workflows/prompts/wiki-ingest.prompt.md) — add sources to the wiki
- [`wiki-lint.prompt.md`](../../02_Workflows/prompts/wiki-lint.prompt.md) — find contradictions, orphans, gaps
- [`03_Agents-and-Skills/Skills/wiki-maintenance/SKILL.md`](../../03_Agents-and-Skills/Skills/wiki-maintenance/SKILL.md)
