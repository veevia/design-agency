# API patterns — the Remotion composition model

Distilled from Remotion's published skill (`remotion-dev/skills`) and docs. These are the patterns
you actually write. The golden rule sits at the top because it's the #1 failure.

## 🚫 The golden rule: animate with interpolate(), never CSS

```
CSS transition / @keyframes / animation:  → FORBIDDEN (won't render)
Tailwind  animate-*  classes              → FORBIDDEN (won't render)
```

Remotion renders the page **one frame at a time** — there is no wall clock, so any CSS that animates
"over time" is invisible to the renderer (it may animate in a normal browser preview, then render
blank/static). Drive **every** animated value through `interpolate(frame, …)` or `spring()`.

## useCurrentFrame() + interpolate()

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const opacity = interpolate(frame, [0, 2 * fps], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",                 // ALWAYS clamp unless you want overshoot
  easing: Easing.bezier(0.16, 1, 0.3, 1),
});
```

- `interpolate(frame, inputRange, outputRange, options)` maps one range to another.
- **Prefer `interpolate()` over `spring()`** unless you explicitly need physics-based motion.
- `Easing.bezier(...)` customizes timing (incl. jumpy/overshoot curves).
- Write time in **seconds via fps** (`2 * fps`), not magic frame numbers.

## Keep animations editable in Studio

Inline the `interpolate()` in the `style` prop and use **individual transform props**, not a composed
`transform` string — Studio's visual editor can then manipulate them:

```tsx
// PREFER
style={{
  scale:     interpolate(frame, [0, 100], [0, 1]),
  translate: interpolate(frame, [0, 100], ["0px 0px", "100px 100px"]),
  rotate:    interpolate(frame, [0, 100], ["20deg", "90deg"]),
}}

// OVER
const scale = interpolate(frame, [0, 100], [0, 1]);
style={{ transform: `scale(${scale})` }}
```

## Stage + layout

- `<AbsoluteFill>` = a full-stage `position:absolute; inset:0` div. Your scene canvas.
- `useVideoConfig()` → `{ fps, width, height, durationInFrames }`.

## Assets

- Put files in **`public/`** at the project root.
- Reference with **`staticFile()`**.
- Remote URLs work too.

```tsx
import { Img, staticFile } from "remotion";
<Img src={staticFile("logo.png")} style={{ width: 100, height: 100 }} />
```

Media uses `@remotion/media`:

```tsx
import { Video, Audio } from "@remotion/media";
import { staticFile } from "remotion";
<Video src={staticFile("clip.mp4")} style={{ opacity: 0.5 }} />
<Audio src={staticFile("track.mp3")} />
```

## Sequencing — delay, limit, place on the timeline

```tsx
import { Sequence } from "remotion";

<AbsoluteFill>
  <Sequence><Background /></Sequence>
  <Sequence from={1 * fps} durationInFrames={2 * fps} layout="none"><Title /></Sequence>
  <Sequence from={2 * fps} durationInFrames={2 * fps} layout="none"><Subtitle /></Sequence>
</AbsoluteFill>
```

- `from` delays the content; `durationInFrames` limits how long it shows.
- `<Sequence>` is an `AbsoluteFill` by default — for **inline** content use `layout="none"`.
- Inside a Sequence, `useCurrentFrame()` is **rebased to 0** at the sequence's start. This is the key
  to per-scene timing (a beat's animation always starts at its own frame 0).

## Registering compositions — src/Root.tsx

Duration, fps, and dimensions are declared here, not in the component:

```tsx
import { Composition } from "remotion";
import { MyComposition } from "./MyComposition";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="MyComposition"
    component={MyComposition}
    durationInFrames={100}
    fps={30}
    width={1080}
    height={1080}
  />
);
```

## Dynamic metadata — calculateMetadata

Fetch data first, then size the video to it (duration/dimensions/props computed at render time):

```tsx
import { Composition, CalculateMetadataFunction } from "remotion";

const calculateMetadata: CalculateMetadataFunction<MyProps> = async ({ props, abortSignal }) => {
  const data = await fetch(`https://api.example.com/video/${props.videoId}`, { signal: abortSignal })
    .then((res) => res.json());
  return {
    durationInFrames: Math.ceil(data.duration * 30),
    props: { ...props, videoUrl: data.url },
    width: 1080,
    height: 1080,
  };
};

<Composition
  id="MyComposition"
  component={MyComposition}
  fps={30}
  width={1080}
  height={1080}
  defaultProps={{ videoId: "abc123" }}
  calculateMetadata={calculateMetadata}
/>
```

## Parameterized videos (Zod schema)

Expose props so an app/automation (or Studio's props panel) can drive the video. Define a Zod schema
on the composition; Remotion renders an editable props form in Studio and type-checks the inputs.
This is how one composition becomes a reusable template rendered N ways. (Upstream rule:
`rules/parameters.md`; docs: remotion.dev/docs/parameterized-rendering.)

## The ecosystem (load a package when you need it)

Official packages cover most needs — pull them with `npx remotion add <pkg>`:
`@remotion/captions` (subtitles), `@remotion/media` (Img/Video/Audio), `@remotion/google-fonts`,
`@remotion/shapes`, `@remotion/lottie`, `@remotion/gif`, `@remotion/three` (3D), `@remotion/skia`,
`@remotion/motion-blur`, `@remotion/transitions`, `@remotion/lambda` (serverless render),
`@remotion/openai-whisper` / `@remotion/install-whisper-cpp` (caption generation),
`@remotion/elevenlabs` (voiceover). The upstream skill's `rules/` folder has a focused guide per topic.
