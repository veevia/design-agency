---
name: evidence-tagging
title: Tag every claim as observed, reported, or assumed
description: "Label every non-trivial claim, finding, or pain point as observed, reported, or assumed, cite the source for observed and reported claims, and name the cheapest test for each assumption — so unvalidated, load-bearing claims are visible before they reach a decision or a customer. Use when writing or editing any wiki page under _wiki/, when authoring research reports, personas, JTBDs, or journey maps, or when reviewing claims before promoting them into a synthesis or decision."
status: stable
when_to_load:
  - Writing or editing any wiki page under _wiki/
  - Authoring research reports, personas, JTBDs, or journey maps
  - Reviewing claims before promotion into a synthesis, POV, PRD, or decision
  - Running /wiki-lint or /skill-lint evidence-tagging
applies-to: wiki entities, concepts, sources, syntheses, research reports, JTBDs, journey maps, decisions
narrative: 00_README/_frameworks/house-principles.md
inputs:
  - kind: wiki-page
    where: "01_Project-Hubs/*/_wiki/**/*.md"
  - kind: research-report
    where: "01_Project-Hubs/*/01_understand/**/*.md"
outputs:
  - kind: tagged-claim
    schema: "<claim> [observed|reported|assumed | <source-slug>]"
done_when:
  - Every non-trivial claim bullet carries an evidence tag or inherits a declared evidence-default
  - Every observed and reported claim cites a source (`| <slug>`)
  - Every assumed claim names the cheapest test that would resolve it
  - Single-source observed claims are softened to reported or marked n=1
lints:
  - id: untagged-claim-bullet
    severity: error
    where: "01_Project-Hubs/*/_wiki/{entities,concepts,sources,syntheses}/**/*.md"
    pattern: "^- (?!.*\\[(observed|reported|assumed)\\b).{20,}$"
    # Suppress bullets that are not claims: wiki-link cross-refs, markdown-link citations,
    # questions, [open] markers, "- **Key:**" metadata rows, structural relationship keys,
    # italic notes, the Open:/Qn question register, survey-response source lines, and
    # single-source caveats. Tested against the matched line; a hit means "not a claim".
    exclude: '\[\[|\]\(|\?\s*$|\[open\]\s*$|^-\s*\*\*[^*]+:\*\*|^-\s*(Created|Updated|Deleted|Raw file|Date range|Type|Source|Sources|Owner|Status|Inputs|Outputs|Consumer functions|Used by|Consumed by|Served by|Feeds|Pairs with|Part of|Member|Consumes|Hands off|Produces):|^-\s*_[^_]+_|^-\s*Open:\s|^-\s*Q\d+\b|^-\s*[A-Z]{2,6}\s+Survey\s+response\b|^-\s*Single-source\b|^-\s*\*\*New (observation|constraint):'
    # A page that declares evidence-default sets its evidence class at page level; its
    # untagged bodies inherit it. Pages without a declared default are still checked.
    skip_if_frontmatter: [evidence-default]
    message: "Bullet asserts a claim without an evidence tag (or set evidence-default in front-matter)."
  - id: observed-without-source
    severity: error
    # Knowledge pages only; index.md, log.md, and README.md mention tag names in prose.
    where: "01_Project-Hubs/*/_wiki/{entities,concepts,sources,syntheses}/**/*.md"
    pattern: "\\[observed\\]"
    skip_if_frontmatter: [evidence-default]
    message: "`observed` claims must cite a source: `[observed | <source-slug>]` (or set evidence-default in front-matter)."
  - id: assumed-without-test
    severity: warning
    where: "01_Project-Hubs/*/_wiki/{entities,concepts,sources,syntheses,decisions}/**/*.md"
    pattern: "\\[assumed\\]\\s*$"
    message: "`assumed` claim should name the cheapest test that would resolve it (inline or in a sub-bullet)."
budget:
  context_tokens_max: 2000
---

# Evidence Tagging

**TL;DR:** Every non-trivial claim carries `observed`, `reported`, or `assumed` — assumptions aren't wrong, being unaware of them is.

## When to use

- Any time you write or edit a wiki page or an Understand-phase artifact.
- Before a claim is promoted into a synthesis, POV, PRD, or decision.
- When a review asks "how do we know that?"

## Steps

1. **Classify each claim** with the closed three-label enum:

   | Label | Definition | Threshold | Cite a source? |
   |---|---|---|---|
   | `observed` | Direct evidence: a participant did or said it, you saw it, telemetry shows it | ≥2 independent participants or data points; single-source → note `n=1` | Required |
   | `reported` | A third-party claim not validated here: vendor docs, secondary research, a colleague's summary, any AI paraphrase | Cite it; don't promote without re-verification | Required |
   | `assumed` | A team hypothesis listed for traceability | Name the cheapest test that would resolve it | Optional |

2. **Write it inline**: `<claim> [<label> | <source-page-slug>]`.
3. **Use the page shortcut** when the whole page is one class: set `evidence-default:` (and `sources:`) in front-matter; tag only the claims that deviate.
4. **Promote deliberately**: `assumed → reported` when a third party confirms; `reported → observed` only after first-hand validation. Log every promotion with a date in the page's sources.
5. **Check from disk** while drafting: `python3 03_Agents-and-Skills/Skills/evidence-tagging/scripts/check_tags.py <file-or-folder>`; before commit, `python3 06_Engine/harness/lint-skill.py evidence-tagging --severity error`.

## Output format

```markdown
- Covers ~140 regulation feeds [observed | 2026-01-10-vendor-demo]
- Costs about $50K a year [reported | 2026-01-10-vendor-demo]
- May surface drafts earlier than email alerts [assumed]
  - cheapest test: compare alert timestamps for 2 weeks on 10 topics
```

Template: [`assets/tagged-page.template.md`](assets/tagged-page.template.md).

## Watch-outs

- An AI summary or meeting recap is `reported`, never `observed` — it is a paraphrase, not a primary observation.
- One interview is `observed | n=1`, not a pattern.
- There is no fourth label; if you can't pick one, the claim isn't ready for the page.
- Never fabricate a source slug to clear a lint — soften the claim instead.

## See also

- Reference: [`references/REFERENCE.md`](references/REFERENCE.md) — decision table, promotion rules, worked example
- Validator: [`scripts/check_tags.py`](scripts/check_tags.py) (stdlib-only, honours `evidence-default`)
- `extreme-clarity` · `house-principles` (principle 4) · `alignment-playbook` · `traffic-light-decisions`
- Conventions: [`00_README/CONVENTIONS.md`](../../../00_README/CONVENTIONS.md)
