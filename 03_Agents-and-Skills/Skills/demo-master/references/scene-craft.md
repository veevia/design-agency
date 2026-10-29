# Scene craft — content-driven animation in single-file HTML

Each beat is a **full-stage scene**, not a slide. The test is plain: does it feel like *video*, not
a slide deck? Adapted from garden-skills `CHAPTER-CRAFT.md`, re-targeted to vanilla HTML/CSS/JS in one
file (no React, no build). The principles are identical; only the implementation primitive changes.

## This is video, not PPT
- **No chrome** — no header, footer, page numbers, logo bars. Just the stage.
- **Comfortable** — big type (hero text ≥ 64px), generous whitespace, calm palette. No walls of tiny
  text.
- **Visual impact** — the screen is *showing* something, not listing text. Key elements arrive
  progressively with the beats, never all at once.

## Every scene needs a real visual (the floor)
At least one drawn/animated element per scene — CSS, SVG, or canvas. **A text-only scene fails.**
Good content-driven visuals:
- a number counts up / a bar grows / a ranking swaps
- flow nodes light up in sequence / a connector draws itself
- a comparison splits down the middle / a spotlight sweeps
- a flywheel rotates / a loop closes / a path traces
- a fake chat window types / a fake file tree expands / a fake terminal runs

The animation should **be the content** — show the thing the caption is describing happening.

## Progressive reveal — never dump a list
The whole scene is driven by the **global `step` counter** (click / → advances). When the narration
says "first X, then Y, then Z":
- 1 item = 1 step. X appears alone on its step.
- On Y's step, X dims to context + Y lights up. On Z's step, X/Y dim + Z lights up.
- Judge by: would the speaker say them one at a time? Yes → reveal one at a time.

## Two-source rule
- **Rhythm / order / beat-split** follows `script.md` — don't reorder the argument.
- **Visual detail / numbers / quotes** come from the raw transcript — pull more detail than the
  caption says so the *screen is denser than the words*. If the screen only repeats the caption,
  it's PPT.

## Aesthetic basics (video audience, far from screen, drifting attention)
- **Big type** — hero ≥ 64px (ideally 80px+). **Lots of whitespace** — keep the edges clear.
- **Palette via tokens** — colors + font families come from `:root` CSS variables so the whole deck
  restyles by swapping one block. Sizes/spacing/timing can be per-scene.
- **Clean motion** — arrive crisply, settle, don't fidget. "Cool" comes from a smart content-driven
  demo, not from speed or flashing.

## Avoid AI-slop visuals (delete all of these)
- purple/pink diagonal gradient backgrounds
- rounded cards with a colored left border
- gradient pill buttons
- emoji used as icons
- fake data / fake logos / fake "10M users"
- the same entrance animation on every step (whole-stage fade/blur every time)
- a mono badge / number bolted to every corner

Missing an asset? Use a **labeled placeholder** ("image · 16:9 — product chat screen"), never fake it.

## The single-file runtime (what templates/engine.html gives you)
- **Fixed 16:9 stage** — content laid out for 1280×720 (or 1920×1080), `transform: scale()` to fit
  any viewport, letterbox around it. No responsive breakpoints.
- **Global step driver** — click the stage or press →/← to move; Space also advances. Each scene is
  a pure function of `step`. No `setTimeout`-driven animation logic (use CSS keyframes / transitions).
- **Hidden progress bar** — bottom edge, transparent until hover.
- **CC bar** — bottom-center caption that shows the current beat's narration line.

## How scenes + captions stay in sync (the one hard rule)
- The deck is defined by a `SCENES` array. Each scene declares its `steps` (how many beats) and a
  `render(step)` that returns the full-stage HTML for that local step.
- A flat `CAPTIONS` array (or per-scene `captions`) provides one line per **global** step, in order.
- **Invariant:** total steps across all scenes === total captions. The engine asserts this on load
  and logs an error if they drift. Keep them equal.

## Per-scene checklist (run before claiming a scene done)
- [ ] At least one CSS/SVG/canvas visual that animates — not text-only
- [ ] Different scenes use different dominant motions (not all the same fade)
- [ ] Big type, generous whitespace, comfortable palette
- [ ] Lists revealed one item per step
- [ ] Screen shows more detail than the caption (pulled from transcript)
- [ ] No purple/pink gradient, colored-border cards, emoji icons, fake data
- [ ] Colors + fonts use `:root` tokens (no hardcoded hex in scenes where a token exists)
- [ ] This scene's `steps` count === its slice of `CAPTIONS`
- [ ] No header/footer/page-number chrome; no tiny text
