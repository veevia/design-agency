---
title: House Principles — Design Principles
type: framework
status: draft
owner: OS steward
last-updated: 2026-10-29
source: House design principles of this OS
tags: [type/framework, purpose/reference, status/draft, loop/all]
---

# House Principles — Design Principles

> **TL;DR:** Working principles to gut-check design decisions — take a point of view, solve the real problem first, let evidence beat opinion, name your defaults, and treat disagreement as a feature.

The house principles of this template. Used as a gut-check during `problem-frame`, `design-brief`, charter drafting, and concept critiques. Every principle is an opinion — use them to sharpen, not to conform. Teams may add their own; keep the numbering stable because skills and templates cite principles by number (e.g., "House principle §4"). The [`house-principles`](../../03_Agents-and-Skills/Skills/house-principles/SKILL.md) skill operationalizes them.

> **Status:** Draft. Refine with your team's examples as you use it.

## 1. Have a point of view

Design without an explicit POV is design-by-committee. State the opinion in writing before asking for feedback.

- **Prompt:** What do we believe is true? What would make us change our mind?
- **Counter-prompt:** If everyone agrees, we haven't said anything.

## 2. Solve the right problem first

The requested feature is rarely the real problem. Re-pose the problem in the user's language before proposing a solution.

- **Prompt:** What is the user hiring this for?
- **Counter-prompt:** Would a different problem framing make this solution unnecessary?

## 3. Rigor compounds

Sloppy inputs produce sloppy outputs at scale. Tight definitions, clear labels, and versioned artifacts are not bureaucracy; they are leverage.

- **Applies to:** prompt cards, eval rubrics, decision records, dataset cards.

## 4. Evidence > opinion, but evidence is rare

Tag every claim with `#evidence/{observed, reported, assumed}`. Assumptions are not wrong — being *unaware* of them is wrong.

- **Prompt:** What would break if this assumption is wrong?
- **Counter-prompt:** What's the cheapest experiment to test it?

## 5. Clarity is a craft

If a stakeholder can't repeat back your concept in their own words, it is not clear enough yet. Keep reducing.

- See: [`extreme-clarity.md`](extreme-clarity.md) for the full technique set.

## 6. Defaults are decisions

Every unstated assumption becomes the default. Surface them. Name them. Choose them.

- **Applies to:** model defaults, tool selection, HITL trigger thresholds, eval pass-rate targets.

## 7. Disagreement is a feature

Structured disagreement surfaces problems early. Alignment without disagreement is often compliance.

- See: [`alignment-playbook.md`](alignment-playbook.md) for disagreement moves.

## 8. Design for the hand-off

Most artifacts are read more than written. Design for the next reader — the customer engineer, the responsible-AI reviewer, the future you.

- **Applies to:** every `evidence-brief`, every charter, every decision record.

---

## Usage

- At kickoff: pick three principles that most apply to this engagement; make them explicit in the charter.
- At gate reviews: ask "which principles did we violate and why?"
- At retro: capture which principles produced the sharpest decisions; feed the `evidence-brief`.

