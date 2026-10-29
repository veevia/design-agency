---
title: Starters — default web-app stack
description: Frozen, copy-to-use web-app skeletons for hub prototypes
tags: [type/reference, purpose/build, status/canonical]
---

# Web-app starters

**TL;DR:** Frozen project skeletons you copy into a hub's build folder — `next-tailwind/` (Next.js App Router, TypeScript, Tailwind CSS) is the default stack for any new web prototype.

| Starter | Stack | When to use |
|---|---|---|
| [`next-tailwind/`](next-tailwind/README.md) | Next.js 16 (App Router) · React 19 · TypeScript · Tailwind CSS 4 · ESLint | Default for web prototypes in `01_Project-Hubs/<hub-slug>/03_build/<name>/` |

## How to use

```sh
# from the repository root
cp -R 05_Library/_starters/next-tailwind 01_Project-Hubs/<hub-slug>/03_build/<name>
cd 01_Project-Hubs/<hub-slug>/03_build/<name>
rm -rf node_modules .next        # in case someone ran the starter in place
npm install
npm run dev                      # http://localhost:3000
```

Then edit `src/app/page.tsx` and add components under `src/components/`. Before generating UI with an AI tool,
follow [`DESIGN-SYSTEM-AI-INSTRUCTIONS.md`](../DESIGN-SYSTEM-AI-INSTRUCTIONS.md) — the starter's own `AGENTS.md`
points agents there. `node_modules/` and `.next/` are git-ignored; commit source and `package-lock.json`.

## Why this stack

- **Next.js App Router** — file-system routing, server components, streaming.
- **Tailwind CSS 4** — utility-first, with theme tokens declared in `src/app/globals.css` through `@theme inline`.
- **TypeScript + ESLint** — type safety and linting already wired.
- **Fonts and theme** — Geist and Geist Mono via `next/font`; light and dark color tokens follow
  `prefers-color-scheme`. Swap in your design system's tokens and type here.

## Rules

- **Frozen.** Don't develop inside `05_Library/_starters/`; copy first. Change a starter deliberately — bump
  versions, check that it builds and lints, and commit with the reason.
- **Bring your own design system.** The starter ships neutral tokens only; wire your system in per
  [`05_Library/README.md`](../README.md#bring-your-own-design-system).

## Not in scope here

Backend services. Keep a prototype's Python or Node backend next to its frontend inside the same hub build folder
(`01_Project-Hubs/<hub-slug>/03_build/<name>/`), and record how to run both in its `BUILD-NOTES.md`.
