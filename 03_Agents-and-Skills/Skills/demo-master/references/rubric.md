# Deck Rubric (Layer 3) — a craft-maturity ladder

> **TL;DR.** Score every dimension on a **0–4 ladder** so quality is a number that climbs. The
> deterministic rows are gated by the scripts; the taste rows are scored by eye/agent. Ship when every
> MUST row is 🟢 and ≥ L2.

This rubric grades a *built deck*. The deterministic ~70% is enforced by
[`../scripts/lint_deck.py`](../scripts/lint_deck.py) + [`../scripts/check_runtime.py`](../scripts/check_runtime.py)
(run both via [`../scripts/score_deck.py`](../scripts/score_deck.py)); the taste ~30% is scored against
the layers ([`narrative-architecture.md`](narrative-architecture.md), [`motion-craft.md`](motion-craft.md)).

## The ladder (apply to each dimension)
| L | name | feel |
|---|---|---|
| 0 | Slop | AI-default: gradients, whole-list reveals, floaty motion, fake data |
| 1 | Functional | advances, shows content, 0 errors |
| 2 | Clean | tokens applied, calm, one motion/beat, **real** data |
| 3 | Crafted | physical motion, cross-beat continuity, paced to narration |
| 4 | Signature | the motion *is* the argument; nothing left to remove |

## The 15 dimensions
`⚙` = machine-checked (a script proves it). `👁` = agent/human-scored against a layer.

| # | Dimension | Bar | Check |
|---|---|---|---|
| 1 | Narrative fit — right form for the content's structure | MUST | 👁 narrative-architecture §1 |
| 2 | Metaphor coherence — one true carrying metaphor, consistent vocabulary | MUST | 👁 narrative-architecture §2 |
| 3 | Engagement / wayfinding — signposting, setup→payoff, continuity, earned reveals | SHOULD | 👁 narrative-architecture §3–4 |
| 4 | Hook + one-idea-per-beat + CC thread flows | MUST | 👁 |
| 5 | Motion is meaning — every animated beat maps to a real relationship | MUST | 👁 motion-craft §1 |
| 6 | Physics — fall/throw/settle obey gravity + easing; nothing floats | SHOULD | 👁 (STILL mid-frame) |
| 7 | Transition hygiene — intro scaffolding clears before any loop | MUST | 👁 (STILL steady frame) |
| 8 | Calm — ≤1 focal motion/beat; ambient muted; color = meaning | SHOULD | 👁 motion-craft §5 |
| 9 | Continuity — cross-beat color/motif/position consistency | SHOULD | 👁 |
| 10 | Composition / fit — hierarchy clear, focal-aligned, **no clipping/overflow** | MUST | 👁 (runtime overflow check: roadmap) |
| 11 | Grounding — names/numbers/inventory/architecture real | MUST | ⚙ `lint_deck` fake-data + 👁 |
| 12 | Tokens — color/type/motion on the scale | SHOULD | ⚙ `lint_deck` off-palette / off-type / slop-color |
| 13 | Captions & copy — CC ≤1 line & never occludes; tight; CTA present | MUST | 👁 |
| 14 | Performance — idle loops stop, no dead DOM | SHOULD | ⚙ `lint_deck` no-still + 👁 |
| 15 | Verification — loads live, STILL-safe, **0 console errors**, self-contained | MUST | ⚙ `check_runtime` + `lint_deck` not-self-contained |

## Ship gate (rises over time)
- **All MUST rows 🟢 and ≥ L2**, and `score_deck.py` → PASS (lint + runtime green).
- Portfolio target moves **L2 → L3** as decks accumulate — raise the bar deliberately.

## Calibration (first runs, per goal-harness)
Manually confirm the gate verdicts match the eye. If a 🟢 gate hides a real defect, the **linter/rubric**
is wrong, not the deck — fix the checker (and add a fixture under `../eval/decks/` so it can't regress).

## Compounding
When a new kind of feedback appears, graduate it *down* the determinism ladder: prose insight → a
`lint_deck` rule (+ an eval fixture) → a baked-in template default. The same mistake then becomes
impossible, not just caught.
