# Narrative Architecture (Layer 0) — choose the story shape before a pixel moves

> **TL;DR.** Read the content's *deep structure*, then commit to one **physical metaphor** that does
> the explaining. The metaphor picks the motion; the motion picks the tokens. Decide this in Phase 2
> (Narrative design) — never default to fades.

This is the top layer of the demo-master craft system. It sits above the design tokens
([`design-tokens.json`](design-tokens.json)) and the motion grammar ([`motion-craft.md`](motion-craft.md)),
and it is scored by the rubric ([`rubric.md`](rubric.md)) under *Narrative fit*, *Metaphor coherence*,
and *Engagement / wayfinding*.

## 1. The core move — content shape → form → metaphor → motion

| Content's deep structure | Narrative form | Carrying metaphor | Motion signature |
|---|---|---|---|
| Process / steps in time | Wayfinding journey | **Map & route** — "you are here," stop-by-stop | camera pans a road; a traveler advances stop→stop; the path fills behind |
| Transformation (raw→refined) | Pipeline / distillation | **Water & filter** — flow, pool, sieve | items flow through stages and pool |
| Selection / convergence | Funnel / survival | **Gravity** — fall, drop the misses, survivors settle | physics fall + bounce; rejects fade, keepers land |
| System of parts | Blueprint / map | **Architecture / city map** | columns build L→R, arrows connect, clusters feed |
| Cycle / feedback | Engine / orbit | **Flywheel / loop** | continuous rotation; one signal travels the loop |
| Tension / comparison | Fork / scale | **Split-screen / balance** | two paths diverge, or a scale tips |
| Quantity / proof | Accumulation | **Counter / wall** | numbers climb; a grid amasses |
| Emergence / scale | Growth | **Seed → cluster → bloom** | a small cluster expands and replicates |

The golden [`reference-deck.html`](../templates/reference-deck.html) demonstrates three of these (route, gravity, flywheel).

## 2. The metaphor library — each carries meaning *and* a motion fingerprint

| Metaphor | Use it for | Motion fingerprint | Failure mode (slop) |
|---|---|---|---|
| **Map / journey** | sequence, progress, engagement | pan + advance + "you are here" | forced when content isn't sequential |
| **Water / flow** | data throughput, transformation | flow along channels, pool, filter | literal pipes everywhere = noise |
| **Gravity / weight** | selection, convergence | fall, settle, bounce (physics tokens) | floaty motion breaks the spell |
| **Machine / engine** | systems, cycles | rotation, cycle, gates | over-detailed gears = clutter |
| **Growth / organic** | emergence, scale | expand, replicate, spread | cute / off-register for technical |
| **Light / signal** | attention, knowledge-state | pulse, glow, illuminate | glow on everything = noise |

**Rule: one carrying metaphor per scene, one spine metaphor per deck.** Mixing metaphors inside a beat
is the noise to cut.

## 3. The spine (macro arc across the whole deck)
- **Through-line** — one sentence the whole deck proves.
- **Act structure** — the chapters; chapter dividers double as the route's **stops**.
- **Setup → payoff** — plant a question early, pay it off late ("open on a question, not a chart").
- **Escalation** — every beat raises a stake or deepens the idea; no flat stretches.

## 4. Engagement mechanics (how to keep them following)
- **Wayfinding** — the route/map spine kills "where are we?" load.
- **Continuity hooks** — an element re-enters the next scene (a color, a position, a shape).
- **Curiosity gaps** — pose, then reveal; earn the payoff, don't dump it.
- **Recognition** — real names and real numbers beat abstractions.

## 5. The choosing protocol (run this in Phase 2)
1. Name the content's deep structure (process? transformation? cycle? proof?).
2. Pick the matching **form** + **one** carrying metaphor.
3. Stress-test: is the metaphor *true* to the content, or decorative? Say it aloud — if it's cute, cut it.
4. Map metaphor → motion fingerprint → tokens ([`motion-craft.md`](motion-craft.md) → [`design-tokens.json`](design-tokens.json)).
5. If multi-scene, lay the **route/map spine** over the top for wayfinding.

## Pitfalls
- **Defaulting to fades** because no story shape was chosen. Every motion beat must trace to row 1's table.
- **Two metaphors in one beat.** Pick one. The other is noise.
- **Decorative metaphor.** If it doesn't make the content *clearer*, it's slop — cut it.
