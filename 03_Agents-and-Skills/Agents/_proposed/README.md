# `Agents/_proposed/` — agent drafts awaiting graduation

**TL;DR:** Proposed agents incubate here as `<slug>.agent.md`; they are not exposed through discovery until the owner moves them up one level.

- Front-matter: `name:` (display name) and `description:` with a "Use when …" trigger; no `tools` or `model`, so the file works in Copilot and Claude.
- Body: the operating contract — inputs, outputs, side effects and required permissions, done-when, skills, handoffs.
- Graduate on approval: `git mv 03_Agents-and-Skills/Agents/_proposed/<slug>.agent.md 03_Agents-and-Skills/Agents/<slug>.agent.md`, then run the gates listed in [`../../README.md`](../../README.md#capability-lifecycle).
