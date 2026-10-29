---
type: wiki-page
subtype: template
purpose: skeleton for entity pages (vendors, stakeholders, systems, personas)
applies-skills:
  - ../../../../03_Agents-and-Skills/Skills/evidence-tagging
  - ../../../../03_Agents-and-Skills/Skills/extreme-clarity
  - ../../../../03_Agents-and-Skills/Skills/alignment-playbook
---

# Entity template — copy and rename

**TL;DR:** Skeleton for an entity page — a person, team, vendor, system or persona the project's sources keep mentioning.

Copy the block below to `_wiki/entities/<slug>.md`, replace the placeholders, and keep only the page itself. Stakeholder positions describe roles and stated views, never private details.

```markdown
---
type: entity
subtype: vendor | stakeholder | system | persona
slug: <kebab-case>
created: YYYY-MM-DD
updated: YYYY-MM-DD
evidence-default: reported          # most claims source-cited unless overridden
sources: []                          # filled as sources reference this entity
references-frameworks: []            # optional pedagogical links
---
# <Entity Name>

**TL;DR:** <one sentence; numbers > adjectives>.

## Key facts
- <claim> [observed | <source-page-slug>]
- <claim> [reported | <source-page-slug>]
- <claim> [assumed]

## Relationships
- Covers / supports: [[concepts/<concept>]]
- Competes with / overlaps: [[entities/<other-entity>]]
- Used by: [[entities/<persona-or-team>]]

## Position on key topics  (stakeholders only — load alignment-playbook)
| Topic | Position | Evidence | Conflicts with |
|---|---|---|---|
| <topic> | <position> | [observed | <source>] | <other-stakeholder> |

## Disagreement / open questions
- <q>

## Sources
- [[sources/<YYYY-MM-DD-slug>]]
```
