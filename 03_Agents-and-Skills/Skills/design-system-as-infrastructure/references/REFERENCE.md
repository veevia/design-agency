# Design system as infrastructure — source hierarchy and on/off-system examples

On-demand detail for the `design-system-as-infrastructure` skill.

Canonical instructions: [`05_Library/DESIGN-SYSTEM-AI-INSTRUCTIONS.md`](../../../../05_Library/DESIGN-SYSTEM-AI-INSTRUCTIONS.md)

## The rule

The design system is the encoded taste AI tools draw from when they generate UI. Reach for existing
tokens and components before generating new ones. Off-system output is a defect to fix, not a draft
to refine — it is the highest-leverage place to invest because every prototype inherits from it.

## Source hierarchy (reach in this order)

1. **Your component library and tokens** — declared in `05_Library/DESIGN-SYSTEM-AI-INSTRUCTIONS.md`
   (for example a public design system or your own package).
2. **Your icon set** — library icons first; custom or brand icons through `figma-icon-sync`.
3. **Starter theme tokens** — `05_Library/_starters/next-tailwind/src/app/globals.css` (`@theme` block).
4. **New pattern** — only when nothing above fits; propose it back to the system owner.

## What the `hardcoded-hex-color` lint reports

```
warning | design-system-as-infrastructure | hardcoded-hex-color | 01_Project-Hubs/<hub>/web/src/…/X.tsx:NN
  | Hard-coded hex colour in a component — use a theme token …
```

A `#RRGGBB` literal in a `.tsx` component is the most common off-system tell. The fix is always to
promote the literal to a token and reference the token, so every surface stays re-themeable.

## The full bar

- Colour, spacing, and type come from tokens — never inline literals.
- Components are imported, not re-authored.
- kebab-case files, PascalCase components, flex or grid layout over absolute positioning.
- Happy and unhappy paths (empty, loading, error, no-results) are generated together.
- Accessibility follows the system's specs (focus order, contrast, labels).

## When a tool gets it wrong

Write the fix down where the next run will see it: add a "never/always" line to the hub's rubric
(`rubric-authoring`) or propose a refinement with `/skill-refine`. A fix that lives only in chat is
re-learned on every project.

## See also

- Skill: [`../SKILL.md`](../SKILL.md)
- Framework: [`00_README/_frameworks/ai-powered-workflows.md`](../../../../00_README/_frameworks/ai-powered-workflows.md)
