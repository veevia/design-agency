---
name: figma-icon-sync
title: Sync Figma icons into a project with one command
description: "Keep a React or Vite project's SVG icons in lock-step with a Figma library: list icons in a reviewable figma-icons.json manifest and pull fresh SVGs through the Figma REST API with npm run icons:sync. Use when adding or refreshing icon assets from a Figma library, when setting up the manifest and sync script in a new project, or when mixing icon sources (a public icon library plus a brand library) per icon."
status: stable
when_to_load:
  - Adding or refreshing icon assets in a React or Vite project from a Figma library
  - Setting up figma-icons.json and npm run icons:sync in a new project
  - Mixing icon sources (a public library plus custom brand icons) per icon
applies-to: project web apps and prototypes that render icons designed in Figma
contract-exempt: "tool recipe — a portable sync script copied into a project; it reads no workspace files a regex lint could check"
done_when:
  - The project has scripts/sync-figma-icons.mjs and a figma-icons.json manifest under version control
  - FIGMA_TOKEN is supplied through .env.local or the shell and never committed
  - npm run icons:sync writes one SVG per manifest entry into the configured outDir
  - Components render icons through a wrapper with a library fallback so a missing asset never breaks the build
metadata:
  runtime: "Node 18+ (built-in fetch); no npm dependencies"
---

# Figma Icon Sync

**TL;DR:** Add an icon by adding one manifest line, run `npm run icons:sync`, and the project's SVGs match the Figma library — reviewable as code, no manual exports.

## When to use

- Icons are designed in a Figma library and must reach the app without manual export round-trips.
- Several projects share the same icon set.
- You want icon changes reviewed in pull requests (`figma-icons.json` diffs).

## Steps

1. Copy [`scripts/sync-figma-icons.mjs`](scripts/sync-figma-icons.mjs) to `<project>/scripts/` and [`assets/figma-icons.example.json`](assets/figma-icons.example.json) to `<project>/figma-icons.json`.
2. Add the script to `package.json`: `"icons:sync": "node scripts/sync-figma-icons.mjs"`.
3. Make sure `.env.local` (or `*.local`) is gitignored, then set `FIGMA_TOKEN` (a personal access token with `file_read`) there or in your shell.
4. Edit the manifest: `defaultFileKey` is the segment after `/design/` in a Figma URL; add `{ "name": "kebab-case-name", "nodeId": "123:456" }` per icon (`123-456` also works). A per-icon `fileKey` overrides the default.
5. Run `npm run icons:sync`; review the SVG diff.
6. Render through a wrapper that falls back to a library icon when an SVG is missing.

## Output format

```jsonc
{
  "outDir": "public/icons",
  "defaultFileKey": "REPLACE_WITH_FIGMA_FILE_KEY",
  "icons": [
    { "name": "example-icon", "nodeId": "1:2" },
    { "name": "alert", "nodeId": "12-345", "fileKey": "OTHER_FILE_KEY" }
  ]
}
```

```tsx
export function BrandIcon({ name, alt, fallback: Fallback, size = 24 }: {
  name: string; alt: string; fallback: React.ComponentType; size?: number;
}) {
  const [failed, setFailed] = React.useState(false);
  if (failed) return <Fallback />;
  return <img src={`/icons/${name}.svg`} alt={alt} width={size} height={size}
              onError={() => setFailed(true)} style={{ display: 'block', objectFit: 'contain' }} />;
}
```

## Watch-outs

- The Figma API returns SVGs only for explicit node IDs — that is why the manifest exists; there is no "scan a frame".
- Never commit `FIGMA_TOKEN`; rotate it if it ever lands in history.
- Re-running overwrites existing SVGs by design; hand edits to synced files are lost.

## See also

- `design-system-as-infrastructure` — library icons first; sync only what the library lacks
