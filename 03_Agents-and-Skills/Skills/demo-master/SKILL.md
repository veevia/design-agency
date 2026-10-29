---
name: demo-master
title: Turn a talk transcript into a self-contained animated HTML presentation (CC-synced)
description: >
  Transform a raw meeting or talk transcript into an optimized presentation script, then generate a
  single self-contained .html file that plays like a video: each click advances one narration beat,
  every beat takes over the full 16:9 stage, animations are content-driven (the thing being said is
  shown happening), and the narration rides along as synced closed captions (CC) — no audio needed.
  Use when the user says "turn this transcript/talk into a presentation", "make an animated deck from my
  meetup", "demo master", or wants a reusable, openable presentation artifact for a show-and-tell.
  Output is ONE local .html file (no dev server, no build) that anyone can open from its file path.
status: stable
when_to_load:
  - "turn this transcript / talk / meetup into a presentation or animated deck"
  - "make a show-and-tell / keynote from my notes or transcript"
  - "demo master / animated html presentation / presentation with synced captions"
inputs:
  - kind: transcript-or-article
    where: "01_Project-Hubs/*/00_context_intake/**/*.md"
    note: "a transcript, meeting notes or article (the raw source; convert .docx/.pdf to Markdown first); pasted text also works"
outputs:
  - kind: presentation-html
    schema: "ONE self-contained 01_Project-Hubs/<hub>/03_build/<deck>/<deck>.html (inline CSS+JS, no external build) that opens in a browser; click/→ advances beats; each beat = full-stage scene with a content-driven animation + a synced CC line"
  - kind: script-md
    schema: "<deck>.script.md — the optimized presentation script (beats split by ---), saved next to the html"
done_when:
  - "A single .html exists at the requested path and OPENS in a browser with no console errors"
  - "Clicking / pressing → advances one beat at a time; each beat takes over the full stage"
  - "Every beat shows a content-driven visual (not just text), revealed progressively (1 item = 1 beat for lists)"
  - "Each beat's CC line matches the script beat; CC is readable and on-screen"
  - "Verified by actually loading the file in a browser tool and reading the console (0 errors)"
budget:
  context_tokens_max: 3000
---

# Demo Master — transcript → animated HTML presentation (CC-synced)

**TL;DR:** Turn a raw transcript into a tight script, then into ONE openable `.html` that plays like a video — each click is one narration beat, each beat a full-stage content-driven animation with a synced caption — and verify it in a real browser before you hand it over.

Click to advance; each click plays the next **narration beat**; the beat takes over the whole 16:9 stage with a
**content-driven animation**; the narration shows as a **synced caption (CC)**. No audio, no dev server, no build
step — open the file and it runs.

> **Lineage (credit).** Method adapted from the open-source `web-video-presentation` skill in the `garden-skills`
> collection (`github.com/ConardLi/garden-skills`). That skill outputs a Vite + React + TS project driven by TTS
> audio. This skill keeps its **methodology** — script optimization, step = narration beat, content-driven
> animation, anti-AI-slop craft — but re-targets the **deliverable** to a single self-contained HTML file where
> **closed captions replace audio**. Two reasons:
> 1. A localhost dev server started by an agent often shows up blank, or not at all, for the person who needs the
>    result — the agent's browser owns that session. A real file path anyone can open is more reliable, so
>    everything is inlined into one `.html`.
> 2. Captions instead of a TTS track: no voice dependency, the deck works muted, and the narration stays editable
>    text. Same beat structure, caption instead of voice.

## When to use

- "Turn this transcript / talk / meetup into a presentation", "make an animated deck", "demo master".
- A show-and-tell, internal review or keynote that people should click through.
- Not when a polished, rendered video is the deliverable from the start: lock the script here, then graduate it
  with `remotion` (or use Phase 5 for a quick MP4).

## Steps

```
Phase 1  SCRIPT     transcript → optimized presentation script (beats split by ---)
   ▼                (references/script-style.md — English keynote register by default)
Phase 2  OUTLINE    script → scene plan: N scenes, each = a focused topic, beats per scene,
   ▼                + an "info pool" of concrete details pulled from the transcript
Phase 3  BUILD      outline → ONE animated .html (references/scene-craft.md + templates/engine.html)
   ▼                each beat: full-stage scene + content-driven animation + synced CC line
Phase 4  VERIFY     open the .html in a browser tool, click through, read console (0 errors)
```

**Where files go.** Read the raw transcript from the hub's `00_context_intake/` and never edit it. Build in the
phase folder that owns the deck, `01_Project-Hubs/<hub>/03_build/<deck>/`: `<deck>.script.md`, `<deck>.html`,
and verification evidence in `evidence/` ([CONVENTIONS §10](../../../00_README/CONVENTIONS.md#10-generated-output-routing)).

### Phase 1 — Optimize the script

A raw transcript is NOT a script. It rambles, repeats, has filler and cross-talk. Convert it to a tight spoken
script following [`references/script-style.md`](references/script-style.md). Key rules:

- **Keep ≥ 60% of the real information** — this is a *re-say*, not a summary. Cut filler, keep facts, examples,
  the argument chain, the speaker's actual points.
- **Keep the source language** (an English transcript → an English script).
- **Lead with a hook** — the first beat grabs in ~3 seconds (a tension, a contrast, a stake). No
  "Hi everyone, today I'll talk about…".
- **One focused idea per beat**, split by `---`. Each `---` becomes one click / one scene-step.
- **Strip AI-slop** — no "in essence / fundamentally / at its core", no fake empathy, no 3-clause parallelism, no
  "in conclusion". Read it aloud; if a human wouldn't say it, cut it.
- Save it as `<deck>.script.md` next to where the HTML will go. Keep the raw transcript too — it's the detail
  source for Phase 3 visuals.

### Phase 2 — Outline the scenes

Group beats into **scenes** (each scene = one focused topic, ~3–8 beats). For each scene write an **info pool**:
concrete numbers, quotes, names and examples pulled from the transcript that the scene's visuals can hang on. The
outline plans **rhythm + content density only** — NOT specific animations (those are designed per scene in
Phase 3, so scenes don't degrade into templated fades).

**Narrative design (Layer 0) — do this first.** Before the scene plan, read the content's *deep structure* and
choose the **story shape + one carrying metaphor** for the deck (route / gravity / flow / flywheel…). See
[`references/narrative-architecture.md`](references/narrative-architecture.md). The metaphor picks the motion;
defaulting to fades is the failure.

### Phase 3 — Build the animated HTML

Build ONE `.html` from [`templates/engine.html`](templates/engine.html) (the runtime: fixed 16:9 stage, global step
counter, click/→ advance, hidden progress bar, CC bar) + per-scene content following
[`references/scene-craft.md`](references/scene-craft.md). Non-negotiables:

- **Every beat takes over the full stage** — `step === N` renders one full scene, no slide chrome.
- **Content-driven animation every scene** — show the thing happening (a number counts, a flywheel turns, nodes
  light up, a list reveals one item at a time). Never a whole list at once.
- **CC synced to the beat** — the engine shows `CAPTIONS[globalStep]` in the caption bar; it must match that
  beat's script line.
- **Colors + fonts via CSS variables (theme tokens)** — restyle by swapping `:root`, not per scene.
- **No AI-slop visuals** — no purple/pink gradients, no emoji-as-icons, no fake data or logos. Missing asset →
  labeled placeholder, never fake.
- The whole thing is **self-contained**: inline CSS + vanilla JS, no external libraries that need a build (a CDN
  `<script>` is OK only if it degrades gracefully offline; prefer zero dependencies).

### Phase 4 — Verify (never skip)

1. Open the file in a browser tool (for example a Playwright MCP `browser_navigate` to its `file://` path).
2. Click/advance through several beats; confirm each is a full-stage scene that advances one beat per click and
   the CC line changes with it.
3. Read the browser console — **0 uncaught errors**. Fix any before reporting done.
4. **Run the gates** — `python3 scripts/score_deck.py <deck.html>` (static lint + headless-Chrome runtime; Chrome
   may need to run outside an agent sandbox). Then score the deck against [`references/rubric.md`](references/rubric.md):
   every MUST row 🟢 and ≥ L2. The deterministic rows are *proven* by the scripts; the taste rows (narrative /
   metaphor / engagement) you score against the craft layers.
5. Tell the user the real path they can open, plus the theme and scene choices you made.

### Phase 5 (optional) — Compose to a shareable MP4 (no rewrite)

The `.html` is perfect for presenting live, but you can't *send* it as a video. When you need a **shareable MP4**
— to drop into a team chat or an email, or for someone who won't open an HTML file — compose the deck you already
have into video with **no rewrite and no Remotion license**:

```bash
scripts/render_mp4.sh <deck.html> <total_beats> [out.mp4] [seconds_per_beat]
# e.g.  scripts/render_mp4.sh my-demo.html 14 my-demo.mp4 2.5
```

It drives headless Chrome over each beat at `?start=N&still=1` (the capture-safe mode baked into the engine —
settles keyframe animations so no frame is blank), screenshots the **real** deck (not a redraw), and stitches the
frames to MP4 with ffmpeg at a fixed seconds-per-beat. Requires Google Chrome (or Chromium) and ffmpeg. **Verify
the output**: extract a frame (`ffmpeg -ss <t> -i out.mp4 -frames:v 1 f.png`) and look at it — a blank frame means
the still-mode parameter didn't apply.

This closes the agent → final-video loop at demo-master's scale: same script, same `.html`, one extra command →
a video. **Two graduation paths, pick by need:**

| Need | Path | Cost |
|---|---|---|
| Send the deck as a video, fast | **Phase 5 `render_mp4.sh`** (screenshot → MP4) | free, no rewrite, ~1 min |
| A polished, frame-interpolated, audio-capable video | **`remotion`** (rewrite to React) | needs the React port; a Company License for organizations of 4+ people |

## Graduate to a real MP4 — the `remotion` skill

This skill's output is a single openable `.html` deck: instant, free, no install, captions instead of audio. That's
the right form for a **show-and-tell** and for **locking the script cheaply**. When you need a **real shareable
video file** instead — to send to someone who won't open an HTML file, to post, or to embed — graduate the deck to
a rendered `.mp4` with the **`remotion`** skill.

It's not a rewrite of the story: the **same `<deck>.script.md` is the single source of truth**, and the primitives
map 1:1.

| this deck (HTML) | Remotion (MP4) |
|---|---|
| script beat (`---`) | a `<Sequence from durationInFrames>` |
| global `step` (click advances) | `frame` (auto-advances at fps) |
| CC line per beat | a `@remotion/captions` `Caption[]` (timed) |
| content-driven CSS/SVG animation | `useCurrentFrame()` + `interpolate()` |
| `:root` CSS tokens | the same tokens as a theme |
| output: one `.html` | output: one `.mp4` |

Rule of thumb: **demo-master = the fast, free, openable show-and-tell; Remotion = the rendered, shareable,
polished video.** Lock the script and rhythm here cheaply, then graduate the winner. The worked conversion (beats
→ Sequences, CC → `Caption[]`, CSS animation → `interpolate()`) is in the remotion skill's
[`references/from-demo-master.md`](../remotion/references/from-demo-master.md). If the video is made by or for a
for-profit organization of 4+ people, Remotion needs a Company License — check the remotion skill's
[`references/licensing.md`](../remotion/references/licensing.md) first. Individuals, organizations of up to 3
people, non-profits and evaluation are free.

## Output format

```text
01_Project-Hubs/<hub>/03_build/<deck>/
├── <deck>.script.md   the optimized script, beats split by ---   (Phase 1)
├── <deck>.html        the self-contained deck                    (Phase 3)
├── evidence/          score_deck.py output, beat screenshots     (Phase 4)
└── <deck>.mp4         optional (Phase 5); large media per CONVENTIONS §9
Report: openable path · scenes/beats · carrying metaphor · theme · score_deck verdict
```

## Watch-outs

- **Dumping the transcript as bullet slides** — that's PPT, not a video. Each beat is a designed full-stage scene
  with a content-driven animation. If a scene is only text, redo it.
- **Revealing a whole list at once** — 1 list item = 1 beat. The speaker says them one by one.
- **CC drift** — caption count must equal total steps, in order. The engine derives total steps from the `SCENES`
  array; keep each scene's `steps` === its caption slice length.
- **Localhost-only output** — the person who needs the deck may not reach a dev server. Ship the single `.html`,
  verify via `file://`. (This is the whole reason the skill exists in this form.)
- **Over-long animation on a short beat** — keep each animation readable within its beat; don't make the viewer
  wait on a 4-second animation for a one-line caption.
- **Building blind** — always load the file in a browser tool and read the console before claiming it works. The
  user will open it; open it first yourself.

## See also

- [`references/script-style.md`](references/script-style.md) — transcript → optimized script rules
- [`references/scene-craft.md`](references/scene-craft.md) — content-driven animation + anti-slop craft
- **Craft system** — [`references/narrative-architecture.md`](references/narrative-architecture.md) (story shape + metaphor) · [`references/motion-craft.md`](references/motion-craft.md) (motion grammar) · [`references/design-tokens.json`](references/design-tokens.json) (scales) · [`references/rubric.md`](references/rubric.md) (0–4 ladder)
- **Quality gates** — [`scripts/lint_deck.py`](scripts/lint_deck.py) (static) · [`scripts/check_runtime.py`](scripts/check_runtime.py) (headless Chrome) · [`scripts/score_deck.py`](scripts/score_deck.py) (combined) · [`eval/run_evals.py`](eval/run_evals.py) (golden-test the linter) · [`templates/reference-deck.html`](templates/reference-deck.html) (golden exemplar)
- [`templates/engine.html`](templates/engine.html) — the self-contained runtime (stage + stepper + CC)
- `remotion` — graduate this HTML deck into a real rendered `.mp4`; shares the same script. See its [`references/from-demo-master.md`](../remotion/references/from-demo-master.md) and [`references/licensing.md`](../remotion/references/licensing.md).
- `context-intake` — file the raw transcript or notes into the hub before you start
- Source method (credit): `github.com/ConardLi/garden-skills` → `skills/web-video-presentation`
