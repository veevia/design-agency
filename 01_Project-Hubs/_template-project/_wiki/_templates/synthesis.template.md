---
type: wiki-page
subtype: template
purpose: skeleton for synthesis pages (the evolving thesis on a topic)
applies-skills:
  - ../../../../03_Agents-and-Skills/Skills/house-principles
  - ../../../../03_Agents-and-Skills/Skills/evidence-tagging
  - ../../../../03_Agents-and-Skills/Skills/extreme-clarity
  - ../../../../03_Agents-and-Skills/Skills/alignment-playbook
---

# Synthesis template — copy and rename

**TL;DR:** Skeleton for a synthesis page — the evolving, evidence-tagged thesis on one topic, where the team's point of view lives.

Copy the block below to `_wiki/syntheses/<slug>.md` and replace the placeholders.

```markdown
---
type: synthesis
slug: <kebab-case>
topic: <one-line topic>
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources-cited: 0
---
# <Topic> — current synthesis

**TL;DR:** <your position in one sentence>.

## Point of view  (House principles §1)
<the position you're taking. Not a situation. Not a question. An opinion.>

## Rationale (evidence)
- <claim> [observed | <source>] — citing [[entities/X]], [[concepts/Y]]
- <claim> [reported | <source>] — citing [[entities/Z]]
- <claim> [assumed] — to be tested via <cheapest test>

## What this synthesis informed
- [[decisions/NNNN-<decision-slug>]]
- Artifact: `../../02_design/<artifact>.md`

## Disagreement / open questions  (load alignment-playbook)
- <Name (role)>: <position> [observed | <source>]
- <Name (role)>: <counter-position> [observed | <source>]
- Open: <unresolved question>

## What would change this synthesis
- New observation: <specific evidence that would force re-examination>
- New constraint: <specific change that would force a pivot>
```
