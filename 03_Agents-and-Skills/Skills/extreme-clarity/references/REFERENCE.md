# Extreme clarity — the three tests, with worked rewrites

On-demand detail for the `extreme-clarity` skill: the rewrite playbook, acronym discipline, and the
TL;DR style for each artifact.

Framework: [`00_README/_frameworks/extreme-clarity.md`](../../../../00_README/_frameworks/extreme-clarity.md)

## 1. The three tests

| Test | What it asks | Fails when |
|---|---|---|
| 10-second | After the TL;DR, does the reader know what this is, why it matters, and the conclusion? | TL;DR missing, over 25 words, or buries the point |
| Repeat-back | Could a cross-functional stakeholder restate it in their own words? | Undefined acronyms, nested sentences, jargon |
| Numbers | Are key magnitudes numbers, not adjectives? | "many users", "significant", "soon", "fast" |

## 2. The TL;DR contract

1. `**TL;DR:**` at the very top, within the first ~200 characters of the body.
2. One sentence, conclusion first, period at the end.
3. At most 25 words — if it won't fit, the point isn't crisp yet.
4. No throat-clearing.

`check_clarity.py` reports a missing TL;DR as an error; length, late placement, throat-clearing,
and unquantified adjectives are notes.

## 3. Rewrite playbook — adjective → number

| Vague | Replace with |
|---|---|
| "fast" | "< 300 ms" |
| "many users" | "~60 specialists across 3 sites" |
| "soon" | an ISO date, e.g. "by 2026-06-18" |
| "significant savings" | "~60% of duplicate effort" |
| "a few systems" | "4 systems" |
| "large dataset" | "18k past requests" |

## 4. Acronym discipline

Define any acronym of three or more capitals on first use unless it is in
[`00_README/GLOSSARY.md`](../../../../00_README/GLOSSARY.md):

> The Regional Service Desk (RSD) coordination team… *(first use)* … RSD's triage queue… *(later uses)*

## 5. TL;DR style by artifact

| Artifact | The TL;DR is… |
|---|---|
| Research report | the one-sentence finding |
| POV | the position, not the situation |
| PRD | what the user can do that they couldn't before |
| Problem frame | the people-problem and who has it |
| Decision record | the choice and the condition it hangs on |

## 6. Worked example

**Before (fails all three tests):**
> This document describes our current thinking on the request-triage situation, which involves many
> stakeholders and various data sources, and we should consider several approaches that could
> potentially improve things significantly in the near future.

**After (passes):**
> **TL;DR:** Coordinators re-check every urgent request by hand because request data spans 6 disconnected
> systems; connecting them cuts ~60% of duplicate effort.

## See also

- Skill: [`../SKILL.md`](../SKILL.md)
- Validator: [`../scripts/check_clarity.py`](../scripts/check_clarity.py)
- Template: [`../assets/clear-page.template.md`](../assets/clear-page.template.md)
