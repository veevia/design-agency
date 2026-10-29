---
name: design-thinking-loop
title: Check a project's design-loop phase gate
description: "Verify a project is in the phase it claims — Frame, Understand, Design, Build, Learn — and has not skipped a gate, by checking the named evidence each gate requires; match prototype fidelity to the phase and file outputs in the right phase folder. Use when checking whether a project is ready to exit its current phase, when recording a phase-gate result, when a build appears to have started before a PRD landed, or when reviewing a hub's _wiki/index.md for its current-phase block."
status: stable
when_to_load:
  - Checking whether a project is ready to exit its current phase
  - Recording a phase-gate result in a phase artifact or the hub's phase block
  - A build appears to have started before a PRD landed in 02_design/
  - Reviewing a hub's _wiki/index.md for its current-phase block
  - Choosing prototype fidelity for the current phase
applies-to: project hub READMEs, phase artifacts, _wiki/index.md, weekly status
narrative: 00_README/_frameworks/design-thinking-loop.md
inputs:
  - kind: wiki-index
    where: "01_Project-Hubs/*/_wiki/index.md"
  - kind: phase-artifact
    where: "01_Project-Hubs/*/0[1-4]_*/**/*.md"
outputs:
  - kind: phase-gate-check
    schema: "A readiness verdict naming the gate, the required evidence present or absent with paths, and a Traffic Light on exiting the phase"
done_when:
  - The hub's _wiki/index.md carries a current-phase block
  - Each claimed phase exit lists the evidence pages that support the gate
  - Artifacts are filed in the phase folder that matches their type
  - The gate verdict is 🟢 or 🔴 (the Frame readiness light may be 🟡 with trigger and expiry)
lints:
  - id: index-missing-phase-block
    severity: warning
    where: "01_Project-Hubs/[!_]*/_wiki/index.md"
    pattern: "^#\\s"
    must_also_match: "(?i)current (loop )?phase|phase:\\s*\\**\\s*(frame|understand|design|build|learn)"
    message: "_wiki/index.md has no current-phase block — name the phase the project is in (Frame | Understand | Design | Build | Learn)."
budget:
  context_tokens_max: 2000
loads: [canonical-artifacts, evidence-tagging]
---

# Design Thinking Loop

**TL;DR:** A project exits a phase only when the named evidence for that gate exists; building before the PRD or designing without personas and jobs is a gate violation.

```
FRAME ──▶ UNDERSTAND ──▶ DESIGN ──▶ BUILD ──▶ LEARN
                ▲                                │
                └────────────────────────────────┘
```

## When to use

- Someone claims a project is "ready for design" or "ready to build".
- A deliverable looks out of order (a POV before any research, code before a PRD).
- You are choosing how polished a prototype should be.

Individual scoped tasks do not automatically need a PRD, every phase, or a decision record — the loop governs projects, not one-off fixes.

## Steps

1. **Read the hub's current-phase block** in `01_Project-Hubs/<hub>/_wiki/index.md`.
2. **Check the gate's evidence** against the table; mark each item present (with its path) or absent.

   | Gate | Decision | Evidence required |
   |---|---|---|
   | Frame → Understand | Problem grounded, not solutioned | Problem frame with no solution nouns, decisions to enable, feasibility gap, readiness light 🟢/🟡 (`problem-framing`) |
   | Understand → Design | Problem space understood | ≥1 research report, ≥1 persona, JTBDs for in-scope users, journey map |
   | Design → Build | PRD signed, scope locked | POV, brief, PRD; 🟢 on scope and quality |
   | Build → Learn | Shippable to real users | Test plan, working prototype, acceptance and rollback evidence |
   | Learn → next | Forward path decided | Evidence brief, retro, updated artifacts, next workflow named |

3. **Set the verdict**: 🟢 exit — all required evidence present · 🔴 stay — name the missing pages and who unblocks them. Phase exits are binary; an open item that does not block the exit is tracked as its own 🟡 with trigger and expiry. The Frame → Understand readiness light is the one gate that may be 🟡 (proceed with named conditions).
4. **Record it** in the existing phase artifact or the hub's phase block using [`assets/phase-gate-check.template.md`](assets/phase-gate-check.template.md). Keep gate evidence there: phase closure alone needs no new decision file. Use [W5](../../../02_Workflows/workflows/W5-decide.md) only for a new durable choice, an explicit capture request, or a lifecycle change; it selects the record type, not this phase table.
5. **Match prototype fidelity** to the phase:

   | Fidelity | Format | Use when | Phase |
   |---|---|---|---|
   | Low | Sketch, whiteboard, paper | Framing the problem, aligning on the brief | Understand |
   | Mid | Clickable flow | Exploring how the experience should work | Design |
   | Functional | Prototype with real system components | Testing interactions with users | Design → Build |
   | Production-adjacent | Working code with real data | Validating against real constraints | Build |

6. **Check filing**: Understand → `01_understand/`; Design → `02_design/`; Build → `03_build/`; Learn → `04_learn/`; knowledge → `_wiki/`.

Need a facilitation method for the moment? Load the matching method skill (the `design-sprint-tookit` hub indexes all 62) — for example [`how-might-we`](../how-might-we/SKILL.md) (reframe a problem), [`assumption-mapping`](../assumption-mapping/SKILL.md) (rank bets), [`decision-matrix`](../decision-matrix/SKILL.md) (choose between options), or [`five-act-interview`](../five-act-interview/SKILL.md) (test with users).

## Output format

```markdown
## Current loop phase
**Phase:** Understand
**Entered:** 2026-02-01
**Evidence supporting the next gate:**
- research report: 01_understand/2026-02-10-request-triage-research-report.md
- persona: 01_understand/lead-coordinator-persona.md
- journey map: missing
**Gate verdict:** 🔴 stay — journey map missing; unblock owner: Design Lead
**Open item:** 🟡 booking-inbox data access — trigger: export received; expiry: 2026-03-01
```

## Watch-outs

- **Skipping Understand** ("we already know the problem") — ask for the persona and JTBD pages.
- **Designing without a POV** — `house-principles` principle 1.
- **Building without a PRD** — the gate stays 🔴 until the PRD lands.
- **Learning without measurement** — the evidence brief needs numbers (`extreme-clarity`).
- **High fidelity too early** — it slows the team and narrows options; go wider at low fidelity first.

## See also

- `canonical-artifacts` (what each phase produces) · `problem-framing` (the front gate) · `design-sprint-tookit` (methods)
- Workflows: [W1](../../../02_Workflows/workflows/W1-understand.md) · [W2](../../../02_Workflows/workflows/W2-design.md) · [W3](../../../02_Workflows/workflows/W3-build.md) · [W4](../../../02_Workflows/workflows/W4-learn.md) · [W5](../../../02_Workflows/workflows/W5-decide.md)
- Framework: [`00_README/_frameworks/design-thinking-loop.md`](../../../00_README/_frameworks/design-thinking-loop.md)
