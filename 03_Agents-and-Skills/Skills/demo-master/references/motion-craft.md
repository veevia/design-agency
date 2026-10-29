# Motion Craft (Layer 2) — the motion grammar

> **TL;DR.** Calm by default, one focal motion per beat, obey physics, and make every transition
> *resolve and clear* before any loop. Tokens live in [`design-tokens.json`](design-tokens.json);
> this file is the grammar that uses them.

Scored by [`rubric.md`](rubric.md) under *Physics*, *Transition hygiene*, *Calm/noise*, *Pacing*,
*Continuity*, and *Performance*. The golden [`reference-deck.html`](../templates/reference-deck.html) is the worked example.

## 1. Element lifecycle — ENTER → HOLD → EXIT
Every animated element declares phase windows:
- **ENTER** — appears with a little anticipation/overshoot, then settles. Never pops.
- **HOLD** — steady, or static. Most of a beat is HOLD.
- **EXIT** — resolves and **clears**. Intro scaffolding must leave the stage.

## 2. Transition vs Loop contract (the #1 rule)
- A **transition** is one-time, bounded `[start, end]`, and **must fully fade/clear before the first
  loop frame**. (Example: an intro waterfall that fades out by frame 174, before the loop restarts at frame 182.)
- A **loop** is subtle, **seamless** (its period divides the loop span), and holds **≤ 1 focal motion**.
- Symptom of breaking this: "the intro thing is still sitting there." Fix: add the EXIT fade and gate it
  before the loop restarts.

## 3. Choreography
- **Reveal order = narrative/reading order.** Left-to-right, top-to-bottom, or first-mentioned-first.
- **Stagger** by a small token (≈3–9 frames) so a group enters as a wave, not a flash.
- **1 list item = 1 beat.** The speaker says them one at a time.
- **Enter from the source** — an element that "comes from" a prior scene enters from that direction/color
  (continuity).

## 4. Physics over keyframes
Anything that *moves through space* (fall / throw / settle / orbit) uses the physics tokens, not ad-hoc
keyframes, so it reads as believable:
- `gravity ≈ 0.14`, `restitution ≈ 0.32`, `spring damping 13–14`, drift via **smoothstep**, ambient wobble
  via a low-amplitude sine. (See `physics` in [`design-tokens.json`](design-tokens.json).)
- Fall: `y = y0 + 0.5·G·t²`; on landing, a damped bounce for *some* (not all) elements.

## 5. Calm budget (color = meaning)
- **≤ 1 primary motion per beat.** Everything else is ambient (muted grey, low amplitude) or static.
- **Color is reserved for meaning** — the semantic palette marks categories; ambient motion is grey
  (`--rule #C8C4BE`). Decorative color is noise.

## 6. Pace to the spoken beat
- The build completes **inside** the narration line — no dead air, nothing missed.
- Ambient loops run at a calm period (≈2–6 s); never faster than the eye can rest.

## 7. Capture-safety (STILL)
- Every motion settles **deterministically** at a STILL frame (`?still=1&start=N` in the engine; `?still&b=N` in reference-deck-style decks): non-loop → final frame,
  loop → a representative mid frame. This makes verification and MP4 capture clean (no blank frames).
- Non-loop motions **stop their RAF** when done (render the final frame and `return`) — zero idle CPU.

## Pitfalls
- **Perpetual intro.** A transition that never clears (fix: EXIT fade before `loopFrom`).
- **Floaty motion.** Movement without gravity/easing — it breaks the spell.
- **>1 focal motion.** Two things competing for the eye reads as noise.
- **Idle RAF.** A finished non-loop motion still spinning `update(N)` at 60fps — stop it.
- **Off-token values.** Colors/sizes/durations not in [`design-tokens.json`](design-tokens.json) — snap to scale.
