---
name: alignment-playbook
title: Surface disagreement before deciding
description: "Force conflicting stakeholder positions onto the page before a decision closes: name names, quote positions verbatim, and classify each topic as aligned, informed disagreement, or misaligned. Laundered consensus ('the team feels') is a defect. Use when multiple stakeholder points of view touch the same page, synthesis, or decision, when authoring or reviewing a stakeholder entity page, or when a decision's disagreement section is empty or says 'none'."
status: stable
when_to_load:
  - Multiple stakeholder points of view touch the same page, synthesis, or decision
  - Authoring or reviewing a stakeholder entity page
  - Reviewing a decision whose consultation or disagreement section is empty or says 'none'
  - Preparing a workshop, readout, or sign-off where silence could be mistaken for consent
applies-to: stakeholder entity pages, synthesis pages, decision records, workshop outputs
narrative: 00_README/_frameworks/alignment-playbook.md
inputs:
  - kind: synthesis
    where: "01_Project-Hubs/*/_wiki/syntheses/**/*.md"
  - kind: stakeholder-entity
    where: "01_Project-Hubs/*/_wiki/entities/**/*.md"
outputs:
  - kind: disagreement-block
    schema: "A 'Disagreement / open questions' section with named, evidence-tagged positions on syntheses and decisions; a positions-on-key-topics table on stakeholder pages"
done_when:
  - Every synthesis that combines more than one point of view has a 'Disagreement / open questions' section
  - Positions are attributed to named people with roles, never 'some stakeholders' or 'the team'
  - Each contested topic is classified as aligned, informed disagreement, or misaligned, with the matching next action
  - Decisions with an empty disagreement section are flagged unless consultation is honestly marked solo
lints:
  - id: laundered-consensus
    severity: warning
    where: "01_Project-Hubs/[!_]*/_wiki/{syntheses,entities,decisions}/**/*.md"
    pattern: "(?i)\\b(some stakeholders|the team feels|everyone agrees|we all agree)\\b"
    message: "Laundered consensus — name the positions instead of 'some stakeholders / the team / everyone'."
  - id: synthesis-without-disagreement
    severity: warning
    where: "01_Project-Hubs/[!_]*/_wiki/syntheses/**/*.md"
    pattern: "^#\\s"
    must_also_match: "(?i)disagreement|open question"
    message: "Synthesis has no 'Disagreement / open questions' section — surface it or note who confirmed alignment."
budget:
  context_tokens_max: 1500
loads: [evidence-tagging]
---

# Alignment Playbook

**TL;DR:** Before a decision closes, put every conflicting position on the page with a name, a verbatim quote, and a classification — silence is not consent.

## When to use

- A synthesis, POV, brief, or decision blends more than one stakeholder's view.
- You are writing or reviewing a stakeholder entity page.
- A decision record says "no disagreement" and nobody can say who was asked.

## Steps

1. **Disagreement before decision.** List the conflicting positions before resolving them. A decision with no recorded dissent is suspicious unless it was genuinely solo.
2. **Name names.** "Some stakeholders feel…" is laundered consensus. Write each person's real name and role: "[Name] (Procurement): single vendor. [Name] (Innovation): build a relevance layer."
3. **Quote, then paraphrase.** Capture the position verbatim first so a reader can audit your interpretation.
4. **Classify each topic** and take the matching action:
   - *Aligned* (same position) → record and move on.
   - *Informed disagreement* (different positions, same facts) → escalate to the decider or pick and record the trade-off.
   - *Misaligned* (different positions, different facts) → reconcile the facts first; do not decide yet.
5. **Tag the evidence** behind each position (`evidence-tagging`).
6. **Probe silence.** If nobody disagrees, ask the tactical prompts below before writing "invited; none surfaced".

Tactical prompts for workshops and 1:1s: "What would change your mind?" · "Who disagrees most strongly?" · "If we picked the opposite, what would you say?" · "Whose interest does this not serve?"

## Output format

On synthesis and decision pages:

```markdown
## Point of view
<the position this page takes>

## Disagreement / open questions
- <Name (role)>: <position> [observed | <source>]
- <Name (role)>: <counter-position> [observed | <source>]
- Open: <unresolved question>
```

On stakeholder entity pages (template: [`assets/stakeholder-entity.template.md`](assets/stakeholder-entity.template.md)):

```markdown
## Position on key topics
| Topic | This stakeholder's position | Evidence | Conflicts with |
|---|---|---|---|
| Vendor strategy | Single vendor for procurement simplicity | [observed | 2026-01-15-scope-workshop] | [Name] (Design lead) |
```

## Watch-outs

- **"The team feels…"** — rewrite with named positions; the `laundered-consensus` lint flags it.
- **Fabricated dissent.** Solo work has no dissent to record; mark consultation `solo` instead of inventing a debate.
- **Deciding while misaligned.** If the facts differ, a vote only hides the gap.
- **Stakeholder page with no positions** once a meeting or intake mentions that person — add the table.

## See also

- `evidence-tagging` — tag the evidence behind every position
- `house-principles` — principle 7 (surface disagreement) and principle 1 (have a point of view)
- `traffic-light-decisions` — consultation semantics (`solo`, `invited`, `reviewed`) on decision records
- Framework: [`00_README/_frameworks/alignment-playbook.md`](../../../00_README/_frameworks/alignment-playbook.md)
- Method: [`stakeholder-map`](../stakeholder-map/SKILL.md) (power/interest grid)
