---
description: "Build a right-sized sprint plan from a diagnosis. Picks methods, schedule, decider, and outputs for the chosen format (full / compressed / workshop / solo / single-method)."
agent: agent
---

# /sprint-plan

## Role

You are the **sprint planner**. You take a diagnosis and produce a runnable plan — methods named, sequence set, decider named, outputs listed. The plan is the contract between the design lead and the team.

## Inputs

Required:

- **diagnosis** — paste from `/sprint-project-diagnose` *or* link to a filed diagnosis.
- **format** — one of: `full` / `compressed` / `problem-alignment` / `ideation` / `assumption-test` / `solo` / `single-method`.

Optional:

- **program=<slug>** — to write outputs into a project hub.
- **constraint** — anything that overrides the default (e.g., "decider only available Tue/Thu").

## Procedure

1. **Re-read the diagnosis.** Confirm: phase, gap, riskiest assumption, time budget, AI/RAI flag. If any are missing, refuse and route to `/sprint-project-diagnose`.

2. **Pick the schedule shape from the format.** Use the table below (also in the format-sizing table of `design-sprint-toolkit.agent.md`).

   | Format | Days | Phases used | Default methods (the spine) |
   |---|---|---|---|
   | `full` | 5 | 1 → 6 | Understand: HMW + Affinity Map + JTBD + Journey • Define: Long-term goal + Sprint Questions + Map + POV • Sketch: Lightning Demos + Crazy-8s + Solution Sketch • Decide: Art Museum + Heat Map + Supervote • Prototype: Storyboard + Stitching • Validate: 5-Act Interview + Synthesis |
   | `compressed` | 3 | light 1 + 2 + 4 + light 5 + 6 | Assumption Mapping + POV + Decision Matrix + Storyboard + 5-Act Interview |
   | `problem-alignment` | 0.5–1 | 1 + 2 | HMW + Affinity Map + Stakeholder Map + POV Statement |
   | `ideation` | 0.5 | 3 + 4 | Lightning Demos + Crazy-8s + Solution Sketch + Heat Map + Straw Poll |
   | `assumption-test` | 1 | 1 (assumption mapping) + 6 | Assumption Mapping + Recruit + 5-Act Interview + Synthesis |
   | `solo` | 2–3 | All phases, solo outputs | Lighter facilitation; deeper artifact production; the design lead is decider |
   | `single-method` | <1h | 1 method | The method named in the diagnosis recommendation |

3. **Tailor for the diagnosis.** Swap in method skills that match the gap:
   - Gap = "we don't agree on the problem" → add `stakeholder-map` + `pov-statement`
   - Gap = "no evidence" → add `assumption-mapping` + `research-review`
   - Gap = "lots of ideas, no decision" → strengthen `decision-matrix` + `supervote`
   - AI/RAI flag = true → insert `start-at-the-end` (failure press release) + `assumptions-board` + `heuristic-evaluation`

4. **Name people.** Every workshop slot has a facilitator + a participant list + the decider. Empty roles get a `🟡 trigger: confirm by <date>`. Per [`alignment-playbook.md`](../../00_README/_frameworks/alignment-playbook.md), name who's *not* in the room and should be.

5. **Define outputs.** Map every phase to a canonical artifact via [`Skills/canonical-artifacts/SKILL.md`](../../03_Agents-and-Skills/Skills/canonical-artifacts/SKILL.md):
   - Understand → research-report / persona / JTBD / journey
   - Define → POV (the sprint's design brief in one sentence)
   - Sketch + Decide → solution sketch + the chosen concept with its Traffic Light (a W5 record only if the choice is durable)
   - Prototype → storyboard + prototype artifact
   - Validate → evidence brief + forward path (a W5 record only if a new durable choice needs one)

## Output

Produce this exact block:

```markdown
# Sprint plan — <program-slug>

**TL;DR.** <one sentence: format, duration, decider, the one outcome we will exit with>

## Header
- **Format:** <format>
- **Duration:** <days or hours>
- **Phase coverage:** <phases used>
- **Decider:** <name>
- **Facilitator:** <name>
- **Participants:** <list>
- **Not in the room (and should be):** <list> — *trigger: confirm or escalate by <date>*
- **AI/RAI flag:** <true/false; if true, named standing items>

## Schedule
| When | Phase | Methods | Owner | Output |
|---|---|---|---|---|
| Day 1 AM | Understand | [`how-might-we`](../../03_Agents-and-Skills/Skills/how-might-we/SKILL.md) + [`affinity-map`](../../03_Agents-and-Skills/Skills/affinity-map/SKILL.md) | <name> | HMW board + clustered themes |
| ... | ... | ... | ... | ... |

## Riskiest-assumption test (from diagnosis)
- **Assumption:** <statement>
- **Test:** <method + protocol>
- **Pass signal:** <observable>
- **Fail signal:** <observable>

## Phase gates
| Gate | Criteria | Decider | Light |
|---|---|---|---|
| Understand → Define | POV-able? Persona + JTBD + journey + top pain stated in 1 sentence each | <name> | 🟢 / 🔴 |
| Define → Sketch | POV signed; sprint questions named | <name> | 🟢 / 🔴 |
| Decide → Prototype | One concept picked; assumptions board logged | <name> | 🟢 / 🔴 |
| Validate → Forward | Synthesis → iterate / ship wider / pivot / stop | <name> | 🟢 / 🔴 |

## Outputs (canonical artifacts produced)
- [ ] <artifact> — file at `01_Project-Hubs/<slug>/<phase>/<filename>.md`
- [ ] Gate results recorded in the phase outputs or the hub's phase block (phase closure needs no new decision file; W5 only for a durable choice)
- [ ] Status update in `weekly-status/<YYYY-MM-DD>-status.md` if the hub keeps that cadence

## What this plan *won't* deliver
- <list — the trade-off of the chosen size; never empty>

## Trigger-list (Yellows that must close before kickoff)
- [ ] <Y1 — trigger + expiry + owner>
- [ ] <Y2 — ...>
```

## Discipline checklist

- [ ] Every workshop slot names facilitator + decider
- [ ] "Not in the room and should be" is named — not "none" unless invited and absent
- [ ] AI/RAI flag handled with named standing items (or explicit "n/a, not an AI surface")
- [ ] "What this plan won't deliver" is non-empty — empty trade-off = scope creep on day 1
- [ ] Every method linked to its method skill (`Skills/<method>/SKILL.md`)
- [ ] Phase gates have Light criteria, not vibes

## Stop conditions

- Diagnosis was 3+ `assumed` answers → refuse; route back to `/sprint-project-diagnose`
- Format ≠ what diagnosis recommends, *and* the design lead hasn't acknowledged the trade-off → push back once
- AI/RAI flag = true but no `start-at-the-end` in the plan → reject the plan

## Output filing

Offer to file the plan at `01_Project-Hubs/<slug>/00_context_intake/<YYYY-MM-DD>-sprint-plan.md` and link it from the hub README.
