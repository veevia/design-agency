# Templates — the *what*

**TL;DR:** Sixteen copy-ready artifact templates, one per deliverable of the Understand → Design → Build → Learn loop; copy one into a hub only when you start that artifact.

## Catalog

| Template | Phase | Use it for | Drafting prompt | Copy to |
|---|---|---|---|---|
| [`0-0-Ops_execution-plan`](0-0-Ops_execution-plan.template.md) | Ops | Phased plan for a multi-hub program or OS rollout | — | `<hub>/execution-plan.md` |
| [`0-1-Intake_initiative`](0-1-Intake_initiative.template.md) | Intake | Day-one discovery, stakeholder map, async input, kickoff message | — | `<hub>/intake.md` |
| [`0-2-Ops_operating-rhythm`](0-2-Ops_operating-rhythm.template.md) | All | Meeting capture, decision routing, opt-in weekly status | `/decision-log` | `<hub>/00_context_intake/`, `<hub>/weekly-status/` |
| [`1-0-Understand_problem-frame`](1-0-Understand_problem-frame.template.md) | Understand | Pre-research frame: problem, decisions to enable, feasibility gap | [`problem-framing`](../../03_Agents-and-Skills/Skills/problem-framing/SKILL.md) skill | `<hub>/01_understand/` |
| [`1-1-Understand_research-report`](1-1-Understand_research-report.template.md) | Understand | Evidence-tagged findings from real users | `/research-synthesize` | `<hub>/01_understand/` |
| [`1-2-Understand_UX_survey`](1-2-Understand_UX_survey.template.md) | Understand | AI-assisted survey instrument grounded in source material | — | `<hub>/01_understand/` |
| [`1-3-Understand_jtbd`](1-3-Understand_jtbd.template.md) | Understand | One persona's jobs, challenges, signals and opportunity canvases | `/jtbd-draft` | `<hub>/01_understand/` |
| [`1-3b-Understand_jtbd-synthesis`](1-3b-Understand_jtbd-synthesis.template.md) | Understand | Roll several JTBD analyses into ranked workstreams | — | `<hub>/01_understand/` |
| [`1-4-Understand_journey-map`](1-4-Understand_journey-map.template.md) | Understand | One persona doing one job, with emotions and moments of truth | `/journey-map` | `<hub>/01_understand/` |
| [`2-1-Design_POV`](2-1-Design_POV.template.md) | Design | The opinionated stance: for whom, against what, why now | `/design-pov` | `<hub>/02_design/` |
| [`2-2-Design_brief`](2-2-Design_brief.template.md) | Design | One-page alignment on why, who, outcomes and constraints | `/design-brief` | `<hub>/02_design/` |
| [`2-3-Design_PRD`](2-3-Design_PRD.template.md) | Design → Build | The buildable spec, with non-goals, guardrails and rollback | `/prd-draft` | `<hub>/02_design/` |
| [`2-4-Design_handoff`](2-4-Design_handoff.template.md) | Design → Build | Screens, states, interactions and accessibility for engineering | — | `<hub>/02_design/` |
| [`3-1-Build_test-plan`](3-1-Build_test-plan.template.md) | Build | Protocol, metrics and rollback trigger before anything ships | — | `<hub>/03_build/` |
| [`4-1-Learn_evidence-brief`](4-1-Learn_evidence-brief.template.md) | Learn | What shipped vs. what we learned, and the forward path | — | `<hub>/04_learn/` |
| [`4-2-Learn_retro`](4-2-Learn_retro.template.md) | Learn | Blameless retro with owned action items | — | `<hub>/04_learn/` |

Personas have no standalone template: `/persona-draft` synthesizes them from the research report.
Decision records are not here — W5 routes to the typed templates in
[`traffic-light-decisions/assets/`](../../03_Agents-and-Skills/Skills/traffic-light-decisions/assets/decision-record.template.md).
Prompts live in [`02_Workflows/prompts/`](../../02_Workflows/prompts/).

## Using a template

1. Copy it into the hub folder shown above; drop the `.template` infix and use a kebab-case name (`design-pov.md`).
2. Replace the template front matter with the artifact's own: set `type:` to the `template-for` value, add `project`, `owner`, `status: draft`, `loop-phase` and at least one relationship field ([CONVENTIONS §6](../CONVENTIONS.md#6-front-matter)).
3. Delete the HTML comment block and any section you deliberately skip — say why in one line.
4. Keep links valid. Hub-root templates (`0-0`, `0-1`) use `../../` links that resolve from both places; phase templates name repo files with repo-root paths in backticks so copies never break ([CONVENTIONS §11](../CONVENTIONS.md#11-paths-and-links)).

## Adding or changing a template

- Name it `<n>-<Phase>_<slug>.template.md`, matching the loop phase number; keep the standard front matter (`type: template`, `template-for`, `status`, `owner`, `last-updated`, `loop-phase`, `source`, `tags`).
- Open with a one-sentence TL;DR placeholder and end with a quality checklist.
- Add one row to the catalog above. Do not maintain a second template list elsewhere — other docs link here.
