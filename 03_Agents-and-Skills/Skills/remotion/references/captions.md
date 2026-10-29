# Captions — the @remotion/captions model (and the demo-master CC bridge)

This is the most important reference for connecting Remotion to `demo-master`: demo-master's whole
deliverable is **synced closed captions instead of audio**, and Remotion has a first-class captions
system. The beats line up almost exactly.

Content here is from Remotion's published skill (`rules/subtitles.md`, `rules/display-captions.md`).

## The Caption type

All captions are JSON in the `Caption` shape:

```ts
import type { Caption } from "@remotion/captions";

type Caption = {
  text: string;
  startMs: number;        // when this caption starts (ms)
  endMs: number;          // when it ends (ms)
  timestampMs: number | null;
  confidence: number | null;
};
```

Install if needed:

```bash
npx remotion add @remotion/captions
```

## Three things you can do

1. **Generate** captions from audio/video (Whisper) — upstream `rules/transcribe-captions.md`.
2. **Import** from a `.srt` file — upstream `rules/import-srt-captions.md`.
3. **Display** captions synced to the timeline — below.

## Displaying captions (the core pattern)

Fetch the caption JSON (hold the render until it loads with `useDelayRender`), group into pages, and
render each page in a `<Sequence>` timed from its ms → frames.

```tsx
import { useMemo } from "react";
import { createTikTokStyleCaptions } from "@remotion/captions";
import { Sequence, useVideoConfig, AbsoluteFill } from "remotion";

const SWITCH_CAPTIONS_EVERY_MS = 1200;   // higher = more words per page

const { pages } = useMemo(
  () => createTikTokStyleCaptions({ captions, combineTokensWithinMilliseconds: SWITCH_CAPTIONS_EVERY_MS }),
  [captions],
);

// then map pages → <Sequence from={startFrame} durationInFrames={...}>
const startFrame = (page.startMs / 1000) * fps;
```

- `createTikTokStyleCaptions()` groups raw captions into **pages** (how many words show at once).
- Each page becomes a `<Sequence>`; compute `startFrame` / `durationInFrames` from the page's ms.
- **Whitespace matters** — include the leading space in each token's `text` and use
  `whiteSpace: "pre"`.
- Put captioning logic in its **own component/file**.

## Word highlighting (karaoke)

A page carries `tokens` with `fromMs`/`toMs`; highlight the currently-spoken word by comparing to the
absolute time (`page.startMs + (frame / fps) * 1000`):

```tsx
const isActive = token.fromMs <= absoluteTimeMs && token.toMs > absoluteTimeMs;
<span style={{ color: isActive ? "#39E508" : "white" }}>{token.text}</span>
```

## Bridge: demo-master beats → Remotion captions

demo-master uses a flat `CAPTIONS[]` (one line per global step) and a synced CC bar. To graduate that
deck to Remotion, convert each beat into a `Caption` with explicit timing:

| demo-master | Remotion |
|---|---|
| `CAPTIONS[i]` (one line per beat) | a `Caption { text, startMs, endMs }` |
| beat advances on click (no fixed time) | assign each beat a duration → cumulative `startMs/endMs` |
| CC bar shows `CAPTIONS[step]` | a caption `<Sequence>` shows the active page |

Because demo-master beats are **click-advanced** (no inherent duration), pick a per-beat duration when
graduating — e.g. read-time = `max(2s, words * 0.35s)` — to turn the ordered beats into a timed
`Caption[]`. Once timed, the captions render exactly like any transcribed set. `templates/captioned-scene.tsx`
shows a minimal synced-caption scene you can drop a `Caption[]` into.
