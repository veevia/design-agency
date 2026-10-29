---
type: wiki-page
subtype: template
purpose: skeleton for concept pages (capabilities, architectures, taxonomies, methods)
applies-skills:
  - ../../../../03_Agents-and-Skills/Skills/evidence-tagging
  - ../../../../03_Agents-and-Skills/Skills/extreme-clarity
---

# Concept template — copy and rename

**TL;DR:** Skeleton for a concept page — a capability, architecture, taxonomy or method the project keeps reusing.

Copy the block below to `_wiki/concepts/<slug>.md`, replace the placeholders, and keep only the page itself.

```markdown
---
type: concept
slug: <kebab-case>
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
references-frameworks: []
---
# <Concept Name>

**TL;DR:** <one sentence>.

## Definition
<2–4 sentences. Concrete. Numbers where possible.>

## Why it matters
<one paragraph; ≤3 sentences>

## Components / sub-concepts
- <name> [observed | <source>] — <one-line description>
- ...

## Related entities
- [[entities/<vendor>]] — covers this concept
- [[entities/<persona>]] — uses this concept

## Open questions
- <q>

## Sources
- [[sources/<YYYY-MM-DD-slug>]]
```
