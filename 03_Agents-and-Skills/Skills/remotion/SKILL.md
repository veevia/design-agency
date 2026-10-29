---
name: remotion
title: Make real MP4 videos in React with Remotion (compose, preview, render)
description: >
  Create real .mp4 videos by writing React components with Remotion. A video is a function of frames:
  a component reads useCurrentFrame() and draws that frame; animate with interpolate() — CSS transitions
  and Tailwind animate-* classes are forbidden because they don't render. Scaffold with create-video,
  preview in Remotion Studio, parameterize with props and a Zod schema, then render to MP4 locally (or
  serverless). Use when the user asks to make a video, render an MP4, use Remotion, animate something in
  React, or graduate a demo-master HTML deck into a shareable video file. LICENSING: free for individuals,
  organizations of up to 3 people, non-profits and evaluation; any larger for-profit organization needs a
  paid Company License — read references/licensing.md before producing work for an organization.
status: beta
applies-to: motion graphics, explainer videos, promos, captioned clips, data-driven video, graduating an HTML deck to MP4
when_to_load:
  - "make a video / render an MP4 / animate this in React / motion graphics"
  - "Remotion / create-video / Remotion Studio / render a composition"
  - "turn this deck / script / data into a real video file"
  - graduating a demo-master HTML presentation into a rendered, shareable .mp4
inputs:
  - kind: content-source
    where: "01_Project-Hubs/*/**/*.script.md"
    note: "a script (e.g. a demo-master <deck>.script.md), a data object/JSON, or a creative brief for the video"
outputs:
  - kind: remotion-project
    schema: "a create-video project: src/Root.tsx registers <Composition>s; each composition is a React component animated by useCurrentFrame()+interpolate()"
  - kind: rendered-video
    schema: "a real .mp4 (or .webm / still .png) produced by `npx remotion render` — the openable artifact the user asked for"
contract-exempt: "Tool-recipe skill — drives the Remotion CLI (create-video / remotion studio / remotion render) and the React composition model; it produces a video project and a rendered MP4, not a workspace file a linter contracts over. Verification: Studio previews and a render (or a one-frame still) succeeds with 0 errors."
done_when:
  - "A Remotion project exists (scaffolded via create-video) or an existing one is edited, and `npx remotion studio` previews the composition with no console errors"
  - "Animation is driven by useCurrentFrame()+interpolate() — zero CSS transitions/animations and zero Tailwind animate-* classes (they silently fail to render)"
  - "Composition duration/fps/width/height are declared in src/Root.tsx (or via calculateMetadata)"
  - "The deliverable the user asked for is produced and verified: a real render (`npx remotion render <id> out.mp4`) or at least a one-frame still (`npx remotion still <id> --frame=N`) completes"
  - "For work made by or for an organization, references/licensing.md was checked and the Company License question was raised, not silently assumed free"
budget:
  context_tokens_max: 3500
metadata:
  upstream: "github.com/remotion-dev/skills (skills/remotion) — Remotion's own published Agent Skill, maintained by the Remotion team"
  docs: https://www.remotion.dev/docs/
  license_model: "source-available; free for individuals, organizations of up to 3 people, non-profits and evaluation; paid Company License otherwise (remotion.dev/docs/license)"
  duration: "5 min (scaffold + first render) to hours (a polished piece)"
  connects_to: demo-master
  credits: "API patterns, the forbidden-CSS rule, scaffold/studio/still commands and the captions model are distilled from Remotion's published skill (remotion-dev/skills), re-authored into this repository's skill schema with a licensing gate and a demo-master graduation bridge."
---

# Remotion — make real MP4 videos in React

**TL;DR:** A video is a function of frames — a React component reads `useCurrentFrame()` and renders the stage for that frame; scaffold with `create-video`, preview in Remotion Studio, render a real `.mp4`, and animate only with `interpolate()`, never CSS transitions.

> **Lineage (credit).** This skill distills Remotion's own published Agent Skill
> (`github.com/remotion-dev/skills`) into this repository's skill schema. The API patterns, the forbidden-CSS
> rule and the CLI commands are theirs, verbatim where it matters. Two additions: a **licensing gate** (the
> free/paid line) and a **bridge to `demo-master`** so an HTML show-and-tell deck can graduate into a real
> rendered video.

> **Licensing — read once, decide once.** Remotion is *source-available, not open-source.* It is **free** for an
> individual (personal or commercial use), an organization of up to 3 people, a non-profit, or while *evaluating*
> it before commercial use. Any other organization — a for-profit with 4 or more people, even if only one of them
> uses Remotion — needs a paid **Company License** (remotion.pro). For client work, headcounts can aggregate, and
> the owner of the Remotion project buys the license. A personal learning project you own is 🟢 free; work for a
> company of 4+ people is 🔴 a Company License question for its procurement owner. Full rule →
> [`references/licensing.md`](references/licensing.md).

## When to use

- "Make a video", "render an MP4", "animate this in React", motion graphics, a captioned clip, a data-driven video.
- A `demo-master` deck has earned a real, shareable video file.
- Not for a quick click-through show-and-tell: `demo-master` is faster and free, and its `render_mp4.sh` turns a
  deck into a rough MP4 without a rewrite.

## The mental model (4 primitives)

| Primitive | What it is | API |
|---|---|---|
| **Frame** | the current frame number; everything is derived from it | `useCurrentFrame()` |
| **Interpolate** | map a frame range → a value range (the animation) | `interpolate(frame, [0, 30], [0, 1])` |
| **Sequence** | place/delay/trim a chunk of the timeline | `<Sequence from={30} durationInFrames={60}>` |
| **Composition** | a registered video: component + duration + fps + size | `<Composition>` in `src/Root.tsx` |

`AbsoluteFill` is your full-stage canvas (a `position:absolute; inset:0` div). `useVideoConfig()` gives you
`{ fps, width, height, durationInFrames }` so you can write durations in *seconds* (`2 * fps`) instead of magic
frame numbers.

## Steps

```
Phase 1  SCAFFOLD   empty folder → a project        (scripts/scaffold.sh  ·  npx create-video)
   ▼
Phase 2  COMPOSE    write the React component(s)     (references/api-patterns.md)
   ▼                animate with useCurrentFrame()+interpolate(); NEVER CSS transitions
Phase 3  REGISTER   declare duration/fps/size        src/Root.tsx <Composition> (or calculateMetadata)
   ▼
Phase 4  PREVIEW    live-scrub in Studio             (scripts/studio.sh  ·  npx remotion studio)
   ▼
Phase 5  RENDER     produce the real .mp4            (scripts/render.sh  ·  npx remotion render)
                    sanity-check fast with a one-frame still first
```

### Phase 1 — Scaffold

In an empty folder, for a fresh idea (the canonical command from Remotion's own skill):

```bash
npx create-video@latest --yes --blank --no-tailwind my-video
# or the thin launcher:  scripts/scaffold.sh my-video [parent-dir]
```

The blank template registers one empty composition, `MyComp`, that renders nothing. For a working first scene,
copy `templates/Scene.tsx` and `templates/Root.tsx` into `src/` (they register `MyScene`).

**Where the project lives.** Project work goes in the hub phase folder that owns it —
`01_Project-Hubs/<hub>/03_build/<video-slug>/` ([CONVENTIONS §2](../../../00_README/CONVENTIONS.md#2-folder-structure));
`node_modules/` stays git-ignored, and rendered media follows
[CONVENTIONS §9](../../../00_README/CONVENTIONS.md#9-large-media). Keep personal learning projects in a folder you
own, outside any work repository, so the license boundary stays obvious.

### Phase 2 — Compose (the core, and the one hard rule)

A composition is a React component. The current frame drives everything:

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";

export const FadeIn: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = interpolate(frame, [0, 2 * fps], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  return <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
    <div style={{ opacity, fontSize: 100 }}>Hello World!</div>
  </AbsoluteFill>;
};
```

**Forbidden (they silently fail to render):**
- CSS `transition:` / `@keyframes` / `animation:` — Remotion renders frame by frame; CSS time-based motion has no
  wall clock. Drive *every* animated value through `interpolate()` instead.
- Tailwind `animate-*` classes — same reason.

**Prefer** individual transform props so the animation stays editable in Studio:
`style={{ scale: interpolate(...), translate: interpolate(...), rotate: interpolate(...) }}` — *not* a composed
`transform: \`scale(${s})\`` string.

Assets go in `public/`, referenced with `staticFile()`; media via `@remotion/media` (`<Img>`, `<Video>`, `<Audio>`).
Full pattern bank → [`references/api-patterns.md`](references/api-patterns.md).

### Phase 3 — Register the composition

Duration, fps and dimensions live in `src/Root.tsx`:

```tsx
<Composition id="MyComp" component={FadeIn} durationInFrames={100} fps={30} width={1080} height={1080} />
```

For data-driven length/size (fetch, then size to the data), use `calculateMetadata` — see
[`references/api-patterns.md`](references/api-patterns.md) and `templates/Root.tsx`.

### Phase 4 — Preview in Studio (never skip)

```bash
npx remotion studio          # or scripts/studio.sh
```

Studio is the live editor: scrub the timeline, tweak props, watch the animation. This is where you iterate.
**Inline `interpolate()` in the `style` prop** (not extracted to a const) so Studio's visual editor can manipulate
it. When an agent starts Studio, open the printed URL in your own browser — the agent's browser session is not yours.

### Phase 5 — Render the real artifact

```bash
# fast sanity check — one frame (frame is 0-based; at 30fps frame=30 is the 1s mark):
npx remotion still MyComp out/frame.png --frame=30 --scale=0.25

# the real video:
npx remotion render MyComp out/video.mp4
# or the thin launcher:  scripts/render.sh MyComp out/video.mp4
```

Render locally for learning and one-off videos. For scale or bulk, `@remotion/lambda` renders serverless on AWS —
overview in [`references/rendering-and-cli.md`](references/rendering-and-cli.md). An organization that needs a
Company License and wires renders into a pipeline or agent workflow may count as an *automation* — check
[`references/licensing.md`](references/licensing.md). **Always actually render (or at least a still) before
claiming done** — a composition that previews can still fail to render.

## Connects to `demo-master` — graduate an HTML deck into a real MP4

`demo-master` makes a single openable `.html` deck (instant, no install, captions instead of audio). **Remotion is
its production path:** when you need a *real shareable video file* (to send to someone who won't open an HTML file
or a localhost URL, to post, to embed), the **same script beats** (`<deck>.script.md`) become a Remotion
composition. The primitives map 1:1:

| demo-master (HTML deck) | Remotion (MP4) |
|---|---|
| script beat (split by `---`) | a `<Sequence from={…} durationInFrames={…}>` |
| global `step` counter (click advances) | `frame` (auto-advances at fps) |
| CC caption line per beat | `@remotion/captions` `Caption[]` (synced to frames) |
| content-driven CSS/SVG animation | `useCurrentFrame()` + `interpolate()` |
| `:root` CSS tokens | the same tokens as a theme object/CSS |
| full-stage 16:9 scene | `<Composition width height>` |
| output: one `.html` | output: one `.mp4` |

The worked conversion (a demo-master script → a Remotion composition) is in
[`references/from-demo-master.md`](references/from-demo-master.md). Rule of thumb: **demo-master = the fast, free,
openable show-and-tell; Remotion = the rendered, shareable, polished video.** Lock the script and rhythm cheaply
in demo-master, then graduate the winner to Remotion when it earns a real MP4.

## Output format

```text
<project>/src/Root.tsx        compositions: id, durationInFrames, fps, width, height
<project>/src/<Scene>.tsx     frame-driven scenes (interpolate(), no CSS animation)
<project>/out/<name>.mp4      the rendered video (plus out/frame.png from the still check)
Report: openable path · composition id · duration/fps/size · render command used · license light 🟢/🟡/🔴
```

## Watch-outs

- **A CSS transition that "works" in the browser but renders blank or static** — the #1 Remotion bug. It animates
  in a normal browser preview, but Remotion's frame renderer ignores it. Move the value into
  `interpolate(frame, …)`. No exceptions.
- **Forgetting `extrapolateLeft/Right: "clamp"`** — without it, `interpolate` keeps extrapolating past your range
  (values shoot past 1 or below 0). Clamp unless you *want* the overshoot.
- **Magic frame numbers** — write durations in seconds via `fps` (`2 * fps`), so changing fps doesn't silently
  change your timing.
- **Editing the rendered `.mp4` by hand** — it's an output. Re-render from the composition.
- **Assuming it's free because it's "just a tool"** — the license keys on the organization that uses Remotion
  (its total headcount) and, for client work, on who owns or operates the project — not on which machine renders.
  Check [`references/licensing.md`](references/licensing.md).
- **Heavy install surprise** — `create-video` plus `npm install` pulls a headless Chromium (hundreds of MB) for
  rendering. Expect a minute or two on first scaffold; it's normal.
- **Claiming done from Studio alone** — Studio previewing ≠ render succeeding. Run a still or a full render before
  reporting the artifact.

## Bundled files

The runnable "engine" is the Remotion npm toolchain (installed per project via `create-video`), not code vendored
here — the scripts are thin launchers around the official CLI.

```
remotion/
├── SKILL.md                         ← you are here
├── references/                      ← the knowledge (read before composing)
│   ├── api-patterns.md              — useCurrentFrame/interpolate/Sequence/Composition, assets, FORBIDDEN CSS, calculateMetadata, Zod props
│   ├── rendering-and-cli.md         — create-video / studio / still / render / lambda; the full CLI surface
│   ├── captions.md                  — the @remotion/captions Caption type + display/transcribe/import (the demo-master CC bridge)
│   ├── licensing.md                 — the free vs paid Company License rule, decision-framed
│   └── from-demo-master.md          — the worked HTML-deck → MP4 conversion (beat→Sequence, caption→Caption[])
├── templates/                       ← copy → edit
│   ├── Root.tsx                     — composition registry (static + calculateMetadata variants)
│   ├── Scene.tsx                    — a content-driven scene (the canonical interpolate patterns)
│   └── captioned-scene.tsx          — a scene that renders synced captions (demo-master parity)
├── scripts/                         ← thin launchers around the official CLI (PATH-safe for fnm/nvm)
│   ├── scaffold.sh                  — npx create-video@latest --yes --blank
│   ├── studio.sh                    — npx remotion studio
│   └── render.sh                    — npx remotion render (and --still mode)
└── assets/
    └── README.md                    — the worked example walkthrough ("what good looks like")
```

## See also

- [`references/api-patterns.md`](references/api-patterns.md) · [`references/rendering-and-cli.md`](references/rendering-and-cli.md) · [`references/captions.md`](references/captions.md) · [`references/licensing.md`](references/licensing.md) · [`references/from-demo-master.md`](references/from-demo-master.md)
- `demo-master` — the fast HTML-deck path this skill graduates to MP4; its `<deck>.script.md` is the input here
- `design-system-as-infrastructure` — take a composition's theme from design-system tokens, not hard-coded colors
- Remotion docs: https://www.remotion.dev/docs/ · upstream skill: https://github.com/remotion-dev/skills
