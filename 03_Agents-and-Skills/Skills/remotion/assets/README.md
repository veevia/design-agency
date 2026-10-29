# Worked example — what good looks like

This skill's "engine" is the per-project Remotion npm toolchain (installed by `create-video`), so the
worked example is a **runnable recipe**, not a vendored binary. Follow it end-to-end to produce a real
`.mp4` and see every `done_when` go green.

## The first render (personal learning, 🟢 free)

Run from the repository root. `<practice-dir>` is any folder you own outside a work repository, which keeps the
free-license boundary clean; for project work, use `01_Project-Hubs/<hub>/03_build` instead and settle
[`../references/licensing.md`](../references/licensing.md) first.

```bash
# 1. scaffold a blank project
03_Agents-and-Skills/Skills/remotion/scripts/scaffold.sh hello <practice-dir>

# 2. give it a real first scene — the blank template's only composition (MyComp) renders nothing
cp 03_Agents-and-Skills/Skills/remotion/templates/Scene.tsx \
   03_Agents-and-Skills/Skills/remotion/templates/Root.tsx <practice-dir>/hello/src/
cd <practice-dir>/hello

# 3. preview live — open the printed URL in your own browser (not the agent's)
npx remotion studio
#    → scrub the timeline; MyScene fades in and counts up

# 4. fast sanity check — one frame
npx remotion still MyScene out/frame.png --frame=30 --scale=0.5

# 5. the real artifact
npx remotion render MyScene out/hello.mp4
#    → out/hello.mp4 is a real, openable, shareable video
```

`done_when` mapped to this run:
- project scaffolded + Studio previews with no console errors ✔ (steps 1–3)
- animation via `useCurrentFrame()`/`interpolate()`, zero CSS transitions ✔ (`templates/Scene.tsx` obeys this)
- duration/fps/size declared in `src/Root.tsx` ✔ (`templates/Root.tsx`)
- a real render (or still) completes ✔ (steps 4–5)
- licensing checked ✔ — personal learning = free (see `references/licensing.md`)

## The "good" composition shape

Copy `templates/Scene.tsx` and `templates/Root.tsx` into `src/`. The hallmarks of a correct Remotion
scene:

1. **Every animated value comes from `interpolate(frame, …)`** — no CSS transition anywhere.
2. **`extrapolateLeft/Right: "clamp"`** on entrance animations so they hold after they finish.
3. **Durations in seconds** (`0.7 * fps`), not magic frame counts.
4. **Individual transform props** (`scale` / `translate` / `rotate`), not a composed `transform`
   string — so it stays editable in Studio.
5. **`AbsoluteFill`** as the stage; `useVideoConfig()` for `fps`/size.

## Graduating a demo-master deck (the connection in action)

If you have a `demo-master` deck and its `<deck>.script.md`, the worked conversion (beats → `<Sequence>`s,
CC lines → `Caption[]`, CSS animation → `interpolate()`) is in
[`../references/from-demo-master.md`](../references/from-demo-master.md). The output is the same story
you clicked through as HTML, now rendered as a real `.mp4`.

> A rendered `.mp4` and a screenshot of the first frame are the proof artifacts. When you run this for
> real, keep them with the task that owns them (for project work, the hub phase folder, e.g.
> `03_build/<video-slug>/evidence/`) and tell the user the openable path — never "it's live somewhere."
