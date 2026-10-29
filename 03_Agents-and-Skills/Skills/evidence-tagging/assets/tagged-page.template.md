---
type: <entity | concept | source | synthesis>
slug: <YYYY-MM-DD>-<kebab-slug>
# evidence-default sets the page's default evidence class; claims then need an inline tag only
# when they DEVIATE from it. Omit it to tag every claim inline.
evidence-default: reported          # observed | reported | assumed
sources: [<source-page-slug>]       # omit only on type: source (self-citing) pages
tags: [type/<type>, status/draft]
---
# <Page title>

**TL;DR:** <one-sentence conclusion, with a number where possible>.

## <Section>

<!--
  Tag every non-trivial claim: <claim> [observed|reported|assumed | <source-slug>]
  - observed → ≥2 independent sources, MUST cite a source
  - reported → third-party or AI paraphrase, MUST cite a source
  - assumed  → hypothesis; name the cheapest test that would resolve it
-->

- <a claim that deviates from the default> [observed | <source-slug>]
- <a default-class claim inherits evidence-default and needs no inline tag>
- <a hypothesis> [assumed]
  - cheapest test: <the experiment that would resolve it>

## Sources

- `<source-page-slug>` — <one-line origin>

<!--
  VALIDATE before commit:
    python3 03_Agents-and-Skills/Skills/evidence-tagging/scripts/check_tags.py <this-file>
    python3 06_Engine/harness/lint-skill.py evidence-tagging --severity error
-->
