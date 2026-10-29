# Design system is infrastructure

Before generating any UI, reach for existing tokens and components — off-system output is a defect, not a draft. Follow `05_Library/DESIGN-SYSTEM-AI-INSTRUCTIONS.md`:

- Use theme tokens from `src/app/globals.css` (`@theme inline`); never hardcode hex/px/font sizes.
- Reuse the project's components and its chosen icon set; do not rebuild what exists.
- Generate unhappy-path states (empty / loading / error / no-results), not just the happy path.
- Meet the design system's accessibility rules (focus order, contrast, ARIA); WCAG 2.2 AA at minimum.

When a tool applies tokens wrong or rebuilds a component, use the prompt-fix library in
`05_Library/DESIGN-SYSTEM-AI-INSTRUCTIONS.md#prompt-fix-library`.
