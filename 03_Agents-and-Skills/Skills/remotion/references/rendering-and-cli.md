# Rendering & the CLI surface

Every command Remotion gives you, in pipeline order. Commands are from Remotion's published skill +
docs. The bundled `scripts/*.sh` are thin, PATH-safe launchers around these (so they work under
fnm/nvm where `node` isn't on the bare PATH).

## Scaffold a project

```bash
npx create-video@latest --yes --blank --no-tailwind my-video
```

- `--yes` non-interactive · `--blank` empty template · `--no-tailwind` skip Tailwind.
- `--blank` registers one empty composition, `MyComp` (it renders nothing); copy this skill's
  `templates/Scene.tsx` and `templates/Root.tsx` into `src/` for a working first scene (`MyScene`).
- Drop `--blank` to pick a template (Hello World, Next.js, React Router, …).
- It also offers to install Remotion's **Agent Skills** into the project (for Claude Code / Codex /
  Cursor) — accept if you'll prompt the video with a coding agent.
- Heavy: pulls a headless Chromium for rendering (~hundreds of MB). One-time, ~1–2 min.

## Preview — Remotion Studio

```bash
npx remotion studio
```

Live editor: scrub the timeline, edit props (if you defined a Zod schema), watch animations. Your
main iteration loop. Inline `interpolate()` calls stay editable here.

## One-frame still (fast sanity check)

```bash
npx remotion still <composition-id> out/frame.png --frame=30 --scale=0.25
```

- `--frame` is **0-based**: at 30 fps, `--frame=30` is the 1-second mark.
- `--scale=0.25` renders quick at quarter size — enough to check layout/colors/timing.
- Skip it for trivial edits or pure refactors; use it to catch a layout bug before a full render.

## Render the video

```bash
npx remotion render <composition-id> out/video.mp4
```

- Default output is H.264 `.mp4`. Other codecs/formats via `--codec` (e.g. `--codec=vp8` → webm,
  `--codec=gif`).
- `--props='{"k":"v"}'` (or `--props=file.json`) injects input props for a parameterized composition —
  this is how you render the same template N ways.
- `--frames=0-90` renders a sub-range; `--concurrency=N` tunes parallelism.
- Pin quality with `--crf` / `--jpeg-quality` when it matters.

## Add a package

```bash
npx remotion add @remotion/captions      # installs + wires the package
```

## Scale out — serverless rendering

For bulk/parallel rendering you don't run locally:

- **`@remotion/lambda`** — renders on AWS Lambda; you deploy a function + a site bundle, then trigger
  renders via the CLI or the Node API (`renderMediaOnLambda`). Good for "render 1000 personalized
  videos." Docs: remotion.dev/docs/lambda.
- **`@remotion/cloudrun`** — the GCP equivalent (Cloud Run).
- **Node/SSR API** — `@remotion/renderer` (`renderMedia`, `bundle`, `selectComposition`) drives
  renders from your own server/script. Docs: remotion.dev/docs/ssr.

For **learning and one-off videos**, local `npx remotion render` is all you need — Lambda/Cloud Run are a
later infrastructure, cost and license conversation (programmatic rendering at a licensed organization is an
*automation*; see [`licensing.md`](licensing.md)).

## The thin launchers in this skill (scripts/)

These exist so the commands also run from an agent or cron shell where a version manager (fnm/nvm) hides `node`:

| Script | Wraps |
|---|---|
| `scripts/scaffold.sh my-video [parent-dir]` | `npx create-video@latest --yes --blank --no-tailwind` |
| `scripts/studio.sh [project-dir]` | `npx remotion studio` |
| `scripts/render.sh <id> <out.mp4> [project-dir]` | `npx remotion render` (pass `--still` for a still) |

They locate `node` via fnm/nvm/Homebrew if it's not already on PATH, then `cd` to the project and run
the official CLI. They add no logic of their own — the official CLI is the engine.
