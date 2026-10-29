# Frameworks — the *why*

**TL;DR:** Seven short frameworks explain why the OS works the way it does; skills operationalize them and templates apply them, so other docs link here instead of restating them.

| Framework | Use it to… | Operationalized by |
|---|---|---|
| [Design Thinking Loop](design-thinking-loop.md) | Run a project through Understand → Design → Build → Learn, with one exit gate per phase | [`design-thinking-loop`](../../03_Agents-and-Skills/Skills/design-thinking-loop/SKILL.md) skill, workflows W1–W4 |
| [Traffic Light Decisions](traffic-light-decisions.md) | Close every ADR and PDR with exactly one 🟢🟡🔴 | [`traffic-light-decisions`](../../03_Agents-and-Skills/Skills/traffic-light-decisions/SKILL.md) skill, W5 |
| [Extreme Clarity](extreme-clarity.md) | Write so a busy reader can act without a follow-up | [`extreme-clarity`](../../03_Agents-and-Skills/Skills/extreme-clarity/SKILL.md) skill |
| [Alignment Playbook](alignment-playbook.md) | Get a cross-functional group aligned — not merely agreeing | [`alignment-playbook`](../../03_Agents-and-Skills/Skills/alignment-playbook/SKILL.md) skill |
| [House principles](house-principles.md) | Gut-check a design decision against the house principles | [`house-principles`](../../03_Agents-and-Skills/Skills/house-principles/SKILL.md) skill |
| [Long-horizon execution](long-horizon-execution.md) | Run long agent tasks to a verified finish with goals, rubrics and evals | [`goal-harness`](../../03_Agents-and-Skills/Skills/goal-harness/SKILL.md) and [`rubric-authoring`](../../03_Agents-and-Skills/Skills/rubric-authoring/SKILL.md) skills, [evals](../../06_Engine/evals/README.md) |
| [AI-Powered Workflows](ai-powered-workflows.md) | Move between code, canvas and conversation without drifting | [`drift-check`](../../03_Agents-and-Skills/Skills/drift-check/SKILL.md) and [`design-system-as-infrastructure`](../../03_Agents-and-Skills/Skills/design-system-as-infrastructure/SKILL.md) skills |

Evidence tagging (`observed` / `reported` / `assumed`) has no framework file of its own: its *why* is
[House principle §4](house-principles.md#4-evidence--opinion-but-evidence-is-rare), and the
[`evidence-tagging`](../../03_Agents-and-Skills/Skills/evidence-tagging/SKILL.md) skill applies it.

## Rules

- One concept, one framework. A new discipline lands here (or in [CONVENTIONS](../CONVENTIONS.md)) first; everything else links.
- Frameworks explain; they don't carry procedures. Procedures belong to a workflow or skill, and ownership is registered in [AUTHORITIES](../../AUTHORITIES.md).
- Keep each file short, with a one-sentence TL;DR and front matter (`type: framework`).
