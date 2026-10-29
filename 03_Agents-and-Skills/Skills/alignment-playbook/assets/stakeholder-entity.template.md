---
type: entity            # entity = vendor / stakeholder / system / persona
slug: <entity-slug>
evidence-default: reported
sources: [<source-page-slug>]
tags: [type/entity, status/draft]
---
# <Stakeholder name> — <role>

**TL;DR:** <one line — who this is and why their position matters to the decision>.

## Position on key topics

<!--
  alignment-playbook: capture positions with NAMED conflicts. "The team feels" is a defect.
  Classify each topic: aligned / informed disagreement / misaligned.
  Quote verbatim before paraphrasing so a reader can audit the leap.
-->

| Topic | This stakeholder's position | Evidence | Conflicts with |
|---|---|---|---|
| <topic> | "<verbatim quote>" — <paraphrase> | [observed \| <source-slug>] | <Name (role)> |
| <topic> | <position> | [reported \| <source-slug>] | <nobody / Name (role)> |

## Relationships

- Works with: <names>
- Reports to / influences: <names>

## Sources

- `[[sources/<source-slug>]]` — <one-line origin>

<!--
  VALIDATE: python3 06_Engine/harness/lint-skill.py alignment-playbook --severity warning
-->
