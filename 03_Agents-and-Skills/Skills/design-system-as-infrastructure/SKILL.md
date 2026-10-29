---
name: design-system-as-infrastructure
title: Generate UI from the design system, not around it
description: "Treat the design system as the encoded taste that AI tools generate UI from: reach for existing tokens and components first, treat off-system output (hard-coded colours, rebuilt components, magic-number spacing) as a defect, and generate unhappy-path states with the happy path. Use when generating any UI (code, mock, or prototype), when auditing AI-generated UI against the design system, when setting up a project web app from the starter, or when connecting Figma or MCP design context to a coding tool."
status: beta
when_to_load:
  - Generating any UI (code, mock, or prototype) for a project
  - Auditing AI-generated UI against the design system
  - Setting up a project web app from 05_Library/_starters/
  - Connecting Figma or MCP design context to a coding tool
applies-to: project web apps, prototypes, mocks, and any agent-generated interface
narrative: 00_README/_frameworks/ai-powered-workflows.md
inputs:
  - kind: ui-source
    where: "01_Project-Hubs/*/web/src/**/*.{tsx,ts,css}"
  - kind: design-system-instructions
    where: "05_Library/DESIGN-SYSTEM-AI-INSTRUCTIONS.md"
outputs:
  - kind: on-system-ui
    schema: "UI that imports existing components and references theme tokens, with empty/loading/error states generated alongside the happy path"
done_when:
  - No hard-coded hex colours in generated component source; tokens are referenced instead
  - Existing components are reused rather than rebuilt
  - Empty, loading, error, and no-results states exist next to the happy path
  - The project's web app points at 05_Library/DESIGN-SYSTEM-AI-INSTRUCTIONS.md
lints:
  - id: hardcoded-hex-color
    severity: warning
    where: "01_Project-Hubs/[!_]*/web/src/**/*.tsx"
    pattern: "#[0-9a-fA-F]{6}\\b"
    message: "Hard-coded hex colour in a component — use a theme token (the starter's globals.css @theme block or your component library's tokens)."
budget:
  context_tokens_max: 1800
---

# Design System as Infrastructure

**TL;DR:** Every AI-generated screen draws from the design system, so reach for existing tokens and components first — off-system output is a defect to fix, not a draft to refine.

## When to use

- An agent is about to produce UI: a prototype, a mock, a component, or a page.
- You are reviewing generated UI before a stakeholder sees it.
- A new project web app is being scaffolded from `05_Library/_starters/`.

## Steps

1. **Read the instructions**: [`05_Library/DESIGN-SYSTEM-AI-INSTRUCTIONS.md`](../../../05_Library/DESIGN-SYSTEM-AI-INSTRUCTIONS.md) names your team's source hierarchy.
2. **Reach in order**: (1) your component library and its tokens, (2) your icon set (`figma-icon-sync` for custom icons), (3) the starter theme tokens in `05_Library/_starters/next-tailwind/src/app/globals.css`, (4) only then something new — and propose it back to the system.
3. **Generate states together**: happy path plus empty, loading, error, and no-results.
4. **Check accessibility** against the system's specs: focus order, contrast, labels.
5. **Lint**: `python3 06_Engine/harness/lint-skill.py design-system-as-infrastructure`.
6. **Render and look**: judge the screenshot, not the source (`rubric-authoring` explains render-and-score).

Plug-ins extend this skill when mounted: the FDE Design Toolkit (`03_Agents-and-Skills/Skills/fde-design-toolkit/`) and the UI/UX reference kit (`03_Agents-and-Skills/Skills/ui-ux-pro-max-skill/`) are discovered automatically after `python3 06_Engine/scripts/agency.py plugin add <name>`.

## Output format

| Concern | ❌ Off-system (defect) | ✅ On-system |
|---|---|---|
| Colour | `style={{ color: '#0F6CBD' }}` | a theme token such as `text-[--color-brand]` |
| Spacing | `style={{ padding: 13 }}` | a scale step such as `p-3` |
| Component | hand-rolled `<div className="my-button">` | the library's `<Button>` |
| Icon | pasted inline `<svg>` | a library icon or a synced brand icon |
| Layout | `position: absolute; top: 40px` | flex or grid with gap tokens |
| States | happy path only | empty + loading + error + no-results |

## Watch-outs

- **Looks right but off-system.** A pixel match built from divs is a rebuild, not a prototype.
- **Rebuilt components.** If the library has it, import it.
- **Magic numbers.** Promote a literal to a token rather than repeating it.
- **Happy path only.** Stakeholders find the empty state first.

## See also

- Reference: [`references/REFERENCE.md`](references/REFERENCE.md) — source hierarchy, examples, what the lint catches
- `figma-icon-sync` · `design-thinking-loop` (fidelity ladder) · `rubric-authoring` (score the rendered result)
- Framework: [`00_README/_frameworks/ai-powered-workflows.md`](../../../00_README/_frameworks/ai-powered-workflows.md)
