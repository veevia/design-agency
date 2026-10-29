# From demo-master deck → Remotion MP4 (the worked conversion)

This is the bridge that levels up `demo-master`. demo-master produces a single openable `.html` deck
(instant, free, captions-not-audio). When you need a **real shareable video file**, that same script
(`<deck>.script.md`) graduates into a Remotion composition that renders a `.mp4`. Nothing is re-invented — the
primitives map 1:1.

## When to graduate (and when NOT to)

| Situation | Use |
|---|---|
| Show-and-tell, internal review, "let me click through it", fast iteration | **demo-master** (HTML deck — free, instant, no install) |
| Send to someone who won't open an HTML/localhost; post/embed; a polished asset | **Remotion** (rendered `.mp4`) |
| Lock the script + rhythm cheaply, THEN make the winner a real video | **demo-master first → Remotion** |

Rule of thumb: **demo-master is the draft and the free show-and-tell; Remotion is the production
render.** Don't graduate every deck — only the one that earns a real MP4. (If the video is made by or for an
organization of 4+ people, settle [`licensing.md`](licensing.md) first.)

## The 1:1 primitive map

| demo-master (HTML) | Remotion (MP4) | Note |
|---|---|---|
| script beat in `<deck>.script.md` (split by `---`) | a `<Sequence from={…} durationInFrames={…}>` | one beat = one timeline slot |
| global `step` counter (click advances) | `frame` (auto-advances at `fps`) | time replaces clicks |
| CC line per beat (`CAPTIONS[step]`) | a `Caption { text, startMs, endMs }` | see `captions.md` |
| content-driven CSS/SVG animation | `useCurrentFrame()` + `interpolate()` | the FORBIDDEN-CSS rule applies |
| `:root` CSS tokens | a theme object / CSS imported into the comp | same palette |
| full-stage 16:9 scene | `<Composition width={1920} height={1080}>` | same aspect |
| reveal 1 list item per step | a `<Sequence>` per item, staggered `from` | progressive reveal |
| output: one `.html` (open it) | output: one `.mp4` (`npx remotion render`) | the deliverable |

## The conversion, step by step

### 1. Beats → timed scenes
demo-master beats are **click-advanced** (no inherent duration). Assign each beat a duration to turn
the ordered beats into a timeline. A good default read-time:

```
durationSec(beat) = max(2.0, wordCount(caption) * 0.35)
```

Then lay scenes back-to-back: scene *i* starts at the cumulative frame
`sum(durationSec[0..i-1]) * fps`, lasts `durationSec[i] * fps` frames.

### 2. Each beat's visual → a frame-driven scene
Take the beat's content-driven animation (a number counting, a flywheel turning, nodes lighting up)
and re-express it with `interpolate(frame, …)`. The animation logic is the same idea; only the driver
changes from "CSS over time" to "value as a function of frame." (See `api-patterns.md` — and remember
CSS transitions are forbidden in Remotion.)

```tsx
// demo-master: a CSS @keyframes count-up   →   Remotion:
const n = Math.round(interpolate(frame, [0, 1.2 * fps], [0, 1287], { extrapolateRight: "clamp" }));
<div style={{ fontSize: 120 }}>{n.toLocaleString()}</div>
```

### 3. CC bar → captions
Convert the flat `CAPTIONS[]` to a `Caption[]` with the timing from step 1 (`startMs`/`endMs` =
cumulative ms). Render with the `@remotion/captions` pattern in `captions.md`, or for a simple
bottom-center CC bar (demo-master parity), just show the active line per `<Sequence>` —
`templates/captioned-scene.tsx` is a minimal version.

### 4. Tokens → a theme
demo-master's `:root` CSS variables become a plain theme object (or a CSS file imported into the
composition). Same hex values, same font families — the video stays on-brand with the deck.

### 5. Register + render
Put each scene in `src/Root.tsx` as a `<Composition>` (total `durationInFrames` = sum of all scene
frames). Preview in Studio, then `npx remotion render <id> out.mp4`.

## A concrete walkthrough

Say `demo-master` produced `flywheel.script.md` with 6 beats and a deck at
`01_Project-Hubs/<hub>/03_build/flywheel/flywheel.html`. To graduate it:

1. `03_Agents-and-Skills/Skills/remotion/scripts/scaffold.sh flywheel-video 01_Project-Hubs/<hub>/03_build` (run
   from the repository root) — or a personal folder outside any work repository when you're learning. For
   organization work, settle [`licensing.md`](licensing.md) first.
2. Read `flywheel.script.md`; for each `---` beat compute a duration (step 1 formula).
3. Build one scene component per beat from `templates/Scene.tsx`, re-expressing each beat's visual
   with `interpolate()`.
4. Convert the 6 caption lines to a `Caption[]` (step 3) and render them with
   `templates/captioned-scene.tsx`.
5. Register the 6 scenes under one `<Composition id="Flywheel">` in `src/Root.tsx` (`templates/Root.tsx`),
   total duration = Σ scene frames.
6. `npx remotion studio` to preview → fix → `npx remotion render Flywheel out/flywheel.mp4`.

Result: the same story you clicked through as HTML is now a real `.mp4` you can send or post.

## Keep both — they're complementary

Don't replace demo-master. The deck stays the **fast, free, openable** path (and the place to lock the
script). Remotion is its **production output**. The shared `<deck>.script.md` is the single source of truth
that feeds both — write it once, show it as HTML, render it as MP4.
