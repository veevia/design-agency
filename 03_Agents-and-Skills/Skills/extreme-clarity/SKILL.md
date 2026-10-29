---
name: extreme-clarity
title: Lead every page with a one-sentence, numbers-first TL;DR
description: "Make any page pass three tests — the 10-second test (a conclusion-first TL;DR of at most 25 words at the top), the repeat-back test (a cross-functional reader can restate it), and the numbers test (magnitudes as numbers, not adjectives). Use when writing or editing any markdown meant for people, when reviewing a page's TL;DR, or when turning a wiki page into an artifact whose TL;DR must carry forward."
status: stable
when_to_load:
  - Writing or editing any markdown meant for people
  - Reviewing the TL;DR slot of any page
  - Producing an artifact from a wiki page (the TL;DR carries forward)
  - Writing a status update, readout, or handoff
applies-to: every wiki page, artifact, README, status update, prompt output, and decision record
narrative: 00_README/_frameworks/extreme-clarity.md
inputs:
  - kind: markdown-page
    where: "01_Project-Hubs/**/*.md"
outputs:
  - kind: tldr
    schema: "`**TL;DR:**` line in the first 200 characters of the body; ≤25 words; conclusion first"
done_when:
  - Every page has a `**TL;DR:**` slot within the first 200 characters of its body
  - The TL;DR is one sentence of at most 25 words and starts with the conclusion
  - Adjective-only magnitudes are replaced with numbers, ranges, or dates where feasible
  - Acronyms are defined on first use unless they are in 00_README/GLOSSARY.md
lints:
  - id: missing-tldr
    severity: warning
    where: "01_Project-Hubs/*/_wiki/{entities,concepts,sources,syntheses}/**/*.md"
    pattern: "^# "
    must_also_match: "\\*\\*TL;DR:\\*\\*"
    message: "Page is missing a `**TL;DR:**` slot."
  - id: adjective-magnitude
    severity: info
    where: "01_Project-Hubs/*/_wiki/**/*.md"
    pattern: "\\b(many|several|various|significant|soon|fast|slow|small|large)\\b"
    message: "Adjective magnitude — replace with a number where feasible."
budget:
  context_tokens_max: 1500
---

# Extreme Clarity

**TL;DR:** Open with one conclusion-first sentence of at most 25 words, use numbers instead of adjectives, and define acronyms — if a stakeholder can't repeat it back, it isn't clear yet.

## When to use

- Before anything you write is read by someone else.
- When a page "buries the lede" or a review asks "so what?".
- When a wiki page's TL;DR becomes an artifact's TL;DR.

## Steps

1. **Write the TL;DR first**, directly under the H1: `**TL;DR:** <conclusion>.` One sentence, ≤25 words, period at the end.
2. **Cut throat-clearing.** Delete "This document describes…", "It's important to note…", "We should consider…".
3. **Quantify.** "fast" → "< 300 ms"; "many users" → "~60 specialists across 3 sites"; "soon" → an ISO date. A range beats an adjective.
4. **Define acronyms** on first use unless they are in [`00_README/GLOSSARY.md`](../../../00_README/GLOSSARY.md).
5. **Match the artifact's TL;DR style**: research report → the finding; POV → the position; PRD → what the user can now do; problem frame → the people-problem and who has it; decision → the choice and the condition it hangs on.
6. **Check from disk**: `python3 03_Agents-and-Skills/Skills/extreme-clarity/scripts/check_clarity.py <file-or-folder>`.

## Output format

```markdown
# <Page title — name the thing>

**TL;DR:** <conclusion with a number>.

## Why it matters
<≤3 sentences, quantified>
```

Template: [`assets/clear-page.template.md`](assets/clear-page.template.md).

## Watch-outs

- A TL;DR that describes the document instead of stating its conclusion fails the 10-second test.
- Stacked qualifiers ("may potentially possibly") — pick one or none.
- "In the future" without a date is not a plan.
- Don't hide a number you have; don't invent a number you don't — say "unmeasured".

## See also

- Reference: [`references/REFERENCE.md`](references/REFERENCE.md) — rewrite playbook, before/after, TL;DR styles per artifact
- Validator: [`scripts/check_clarity.py`](scripts/check_clarity.py)
- `evidence-tagging` · `house-principles` (principle 5) · `canonical-artifacts`
- Framework: [`00_README/_frameworks/extreme-clarity.md`](../../../00_README/_frameworks/extreme-clarity.md)
