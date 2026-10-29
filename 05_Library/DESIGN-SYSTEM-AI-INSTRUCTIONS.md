---
title: Design system — AI tool instructions
description: How AI tools (coding agents, MCP-driven generators, design-to-code tools) must use your design system so generated UI is on-brand and editable from the start
type: reference
status: canonical
narrative: 00_README/_frameworks/ai-powered-workflows.md
tags: [type/reference, purpose/build, status/canonical, loop/build]
---

# Design system — AI tool instructions

**TL;DR:** In the AI era the design system is *infrastructure* — the encoded taste AI tools generate from — so before producing any UI (code, mock or prototype), an AI tool reaches for your tokens, components and patterns; off-system output is a defect, not a draft.

These are the written instructions for AI tools the playbook calls for ("which components to reach for and which
patterns to follow"). They govern every AI-generated UI artifact in this repository: hub prototypes,
MCP-driven code generation and design-to-code prototypes. Source practice:
[`ai-powered-workflows.md`](../00_README/_frameworks/ai-powered-workflows.md) §3, "Treating your design system as
infrastructure."

---

## Reach for sources in this order

1. **Your design system** — tokens, component anatomy and accessibility specs, registered in
   [`README.md`](README.md#bring-your-own-design-system).
2. **Your icon set** — from the same registry.
3. **The starter's theme** — tokens in `src/app/globals.css` of a prototype copied from
   [`_starters/next-tailwind/`](_starters/README.md). With no registered design system, these tokens *are* the system.
4. **Only then a new component** — built from existing tokens and proposed back to the design system.

If a component exists, **use it**. Rebuilding an existing component is the most common source of drift the
playbook names.

---

## Rules for AI-generated UI

| Rule | Why | Defect if violated |
|---|---|---|
| **Use design tokens, never hardcoded values.** Pull color, space and type from the design system's tokens or the Tailwind theme (`@theme inline` in `globals.css`). | A prototype without real tokens looks off-brand from the start. | Hardcoded hex (`#0a84ff`), raw px spacing, inline font sizes. |
| **Reuse existing components.** Import from the design system and the prototype's `src/components/` before authoring new ones. | Generated code that ignores existing components creates more problems than it solves. | A new `Button` or `Icon` when one already exists. |
| **Match naming and structure.** Kebab-case files, PascalCase components, flex/grid layout over absolute positioning. | Consistent files produce consistent AI output. | One-off naming, magic-number layout. |
| **Carry intent across surfaces.** When moving design → code through MCP, pass component and token context (component-to-code mappings where available). | Closes the interpretation gap between design and code. | Code that looks right but uses arbitrary classes. |
| **Generate the unhappy paths too.** Empty, loading, error and no-results states. | React to the full experience, not just the version where everything goes right. | Only the happy-path screen exists. |
| **Accessibility is non-negotiable.** Follow the design system's accessibility specs and WCAG 2.2 AA: focus order, labels, contrast, reduced motion. | An encoded standard, not an afterthought. | Missing focus states, labels or contrast. |

---

## When generating a new project web app

1. Copy the starter into the hub (from the repository root):
   `cp -R 05_Library/_starters/next-tailwind 01_Project-Hubs/<hub-slug>/03_build/<name>` ([starter guide](_starters/README.md)).
2. Wire your design system in (package, tokens, icons); add new tokens in `src/app/globals.css`, never inline.
3. Point the prototype's `AGENTS.md` at this file (`05_Library/DESIGN-SYSTEM-AI-INSTRUCTIONS.md`).
4. Before sharing, audit it with the
   [`design-system-as-infrastructure`](../03_Agents-and-Skills/Skills/design-system-as-infrastructure/SKILL.md) skill
   and check for drift with [`drift-check`](../03_Agents-and-Skills/Skills/drift-check/SKILL.md).

---

## Prompt-fix library

When a tool applies tokens wrongly or rebuilds a component, use the matching fix prompt instead of hand-patching
the output — then add any new pattern you discover as a row here.

| Symptom | Fix prompt |
|---|---|
| Hardcoded colors, spacing or font sizes | "Replace every hardcoded color, spacing and font size with the matching design token. List any value that has no token instead of inventing one." |
| An existing component was rebuilt | "Before writing a component, search the design system and `src/components/` for an existing one. Reuse it, and explain any gap that forces a new component." |
| Only the happy path exists | "Add empty, loading, error and no-results states for every view that loads data, and show each state." |
| Accessibility gaps | "Audit this view for focus order, accessible names, WCAG 2.2 AA contrast and reduced motion. Fix what fails and list what you couldn't verify." |
| Layout built with absolute positioning | "Rebuild this layout with flex or grid and the spacing tokens; no absolute positioning except overlays." |

## See also

- Library overview and design-system registry: [`README.md`](README.md)
- Skill: [`design-system-as-infrastructure`](../03_Agents-and-Skills/Skills/design-system-as-infrastructure/SKILL.md)
- Drift detection: [`drift-check`](../03_Agents-and-Skills/Skills/drift-check/SKILL.md)
