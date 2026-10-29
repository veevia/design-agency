---
type: problem-frame
hub: <hub-slug>
owner: <one named person>
# light = readiness to enter research: green | yellow | red (yellow also needs trigger + expiry)
light: green
trigger: <what closes a yellow>
expiry: <YYYY-MM-DD>
informed-by: <relative path to the intake or source this frame is grounded in>
tags: [type/problem-frame, status/draft, loop/understand]
---
# <Engagement> — Problem Frame

**TL;DR:** <one-sentence people-problem and who has it>.

## Problem statement

<the problem in the USER'S language: the decision they can't make today and who can't make it.
Propose nothing to build here; a solution may appear only to disclaim it (see the skill's
no-solution-noun rule).> [observed | <source>]

## Decisions to enable

- <decision the product must let a user make> — made by <role>, <cadence>, with <data today>
- <decision 2> — …

## Feasibility gap

- Want: <stakeholder ask> [reported | <source>]
- Achievable now: <constraint-bounded reality> [observed | <source>]
- Design target (the overlap): <where we play>

## Known / unknown data map

- Known-known: <data we have>
- Known-unknown: <data we know we lack>
- Unknown-unknown (riskiest): <what we suspect we don't know>

## Stakeholder alignment map

| Stakeholder | Wants | Conflicts with |
|---|---|---|
| <Name (role)> | <want> | <Name (role) / nobody> |

## Readiness to research

🟢 | 🟡 | 🔴 — <one-line rationale: is the problem grounded enough to design against?>

<!--
  VALIDATE before the gate:
    python3 03_Agents-and-Skills/Skills/problem-framing/scripts/check_frame.py <this-file>
-->
