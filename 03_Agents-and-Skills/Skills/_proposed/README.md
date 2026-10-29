# `Skills/_proposed/` — skill drafts awaiting graduation

**TL;DR:** Proposed skills incubate here as `<slug>/SKILL.md`; the folder is outside discovery and the gates until the owner approves graduation.

- Written by `/capability-spot`, `/workflow-audit`, `/skill-refine`, and `/sprint-graduate-method`.
- Start every draft from `06_Engine/harness/SKILL.template.md`.
- Self-check a draft: `python3 06_Engine/harness/lint-skill.py --contract 03_Agents-and-Skills/Skills/_proposed/<slug>/SKILL.md`.
- Graduate on approval: `git mv 03_Agents-and-Skills/Skills/_proposed/<slug> 03_Agents-and-Skills/Skills/<slug>`, then run the gates listed in [`../../README.md`](../../README.md#capability-lifecycle).

Underscore-prefixed folders are never native skills: discovery, the catalog, and the lints skip them.
