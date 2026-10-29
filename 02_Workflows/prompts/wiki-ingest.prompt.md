---
description: "Read a raw source from a project's 00_context_intake/, summarize it as a wiki source page, touch affected entity/concept pages, update index.md and log.md."
agent: agent
---

# /wiki-ingest

Ingest one source from `01_Project-Hubs/<hub>/00_context_intake/` into the corresponding `_wiki/`.

## Inputs

- **source-path** (required): relative path to the raw source file inside `00_context_intake/`.
- **hub** (inferred from source-path; confirm if ambiguous).

## Procedure

1. **Load operating skills**:
   - `03_Agents-and-Skills/Skills/wiki-maintenance/SKILL.md`
   - `03_Agents-and-Skills/Skills/evidence-tagging/SKILL.md`
   - `03_Agents-and-Skills/Skills/extreme-clarity/SKILL.md`
   - `03_Agents-and-Skills/Skills/alignment-playbook/SKILL.md` (if the source contains multiple stakeholder positions)

2. **Read the source end-to-end.** Do not skim. For PPTX/XLSX/PDF, ask the user to point at the markdown / extracted version if one exists; otherwise read what's accessible.

3. **Discuss key takeaways with the user (1–3 bullets).** Confirm framing before writing any wiki files. This step is non-negotiable.

4. **Create the source page** at `<hub>/_wiki/sources/<YYYY-MM-DD>-<slug>.md` using the source template (`_wiki/_templates/source.template.md`). Include:
   - TL;DR (one sentence — extreme-clarity)
   - Origin metadata
   - Key extracted facts, each with an evidence tag (evidence-tagging)
   - Touched entities + concepts (placeholders for now)
   - Open questions surfaced

5. **For each durable entity/concept the source mentions and the promotion gate justifies:**
   - If the page exists: append new facts (tagged), update relationships, add this source to its `sources:` list, bump `updated:` date.
   - If missing: create from the appropriate template (`entity.template.md` or `concept.template.md`) only when the page is likely to be reused. Add to `index.md`.

6. **Update `index.md`:**
   - Bump `Last updated:`
   - Increment page counts
   - Add row for the new source page (and any new entity/concept pages)
   - If current-phase evidence changed, update that block.

7. **Append to `log.md`:**
   ```
   ## [YYYY-MM-DD HH:MM] ingest | <source-slug>
   - Pages touched: <n>
   - Pages created: <list>
   - Pages updated: <list>
   - Open questions surfaced: <list>
   ```

8. **Surface follow-ups to the user**:
   - Open questions that warrant a query or fresh source.
   - Contradictions found vs existing wiki content.
   - Gaps (a concept referenced but with no page yet).
   - Suggest the next source to ingest if a natural one exists.

## Targets / guardrails

- Smallest sufficient wiki update wins. More pages are not healthier; related batches should usually become one corpus source page plus selective synthesis/entity/concept updates.
- Never modify `00_context_intake/`. It is immutable.
- If the source is confidential, keep every page derived from it inside this hub and never copy its content into another hub or a shared framework.

## Output format

After completion, report:

```
✓ Ingest complete: <source-slug>
  Pages touched: <n>
    Created: <list>
    Updated: <list>
  Open questions: <list>
  Suggested next ingest: <source-name or "none">
```

## When this goes wrong

- **Source can't be read** (binary PPTX/XLSX): ask the user to provide a markdown export or transcribe key sections. Don't fabricate content.
- **User declines the proposed framing** in step 3: re-discuss, then re-attempt. Don't write files without alignment.
- **Source contradicts existing wiki claims**: flag in `log.md` and surface to the user. Do not silently overwrite — surface, let user pick the resolution, then update with a citation chain.

## See also

- [`wiki-query.prompt.md`](../../02_Workflows/prompts/wiki-query.prompt.md) — query the wiki
- [`wiki-lint.prompt.md`](../../02_Workflows/prompts/wiki-lint.prompt.md) — health-check the wiki
- [`03_Agents-and-Skills/Skills/wiki-maintenance/SKILL.md`](../../03_Agents-and-Skills/Skills/wiki-maintenance/SKILL.md)
