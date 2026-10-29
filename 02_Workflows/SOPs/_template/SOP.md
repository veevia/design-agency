---
# SOP front-matter contract — copy and rename

# REQUIRED
id: <kebab-case unique id; matches folder name>
title: <human-readable name>
status: draft | beta | stable
trigger: <one-sentence English; what kicks this off>

# REQUIRED — outputs
produces_artifacts:
  - <artifact name or template path>
done_when:
  - <checkable English sentence>

# OPTIONAL — orchestration
owner_agent: <agent slug or "none — human-driven">
sub_agents: [<agent slug>]
loads_skills:                  # ordered; loaded in this order
  - <skill slug>
invokes_prompts:               # ordered
  - <prompt slug, e.g. wiki-ingest>
inputs:
  - kind: <what kind of input>
    where: <glob or path hint>
outputs:
  - kind: <output kind>
    location: <path or pattern>

# OPTIONAL — context budget
context_budget_tokens_max: <int>

# OPTIONAL — narrative pointer
narrative_link: <relative path to framework or workflow narrative>
---

# SOP — <title>

> Copy this file to `SOPs/<id>/SOP.md`. Fill the front-matter, then replace the body sections.

## TL;DR
<one sentence — what does this workflow accomplish?>

## When to run
- <natural-language trigger conditions>

## Inputs
- <input 1>
- <input 2>

## Procedure

1. **<Step name>** — what happens; which skill or prompt it invokes.
2. **<Step name>** — …
3. …

## Outputs
- <artifact 1; location pattern>
- <artifact 2>

## Done when
- <gate 1>
- <gate 2>

## Failure modes
- **<symptom>:** <what to do>
- **<symptom>:** <what to do>

## See also
- <links>
