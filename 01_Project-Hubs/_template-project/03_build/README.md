# 03_build/

**TL;DR:** Phase 3 — ship the smallest slice that tests the riskiest assumption, with the test plan written before anything reaches users.

**Workflow:** [W3 — Build](../../../02_Workflows/workflows/W3-build.md) (`02_Workflows/workflows/W3-build.md`)

## Fidelity ladder

Pick the lowest fidelity that can answer the current riskiest question.

| Fidelity | When | Lives where |
|---|---|---|
| Paper / sketch | Testing core flow logic | `03_build/<name>-sketch.md` + photos |
| Wireframe | Testing structure and navigation | Design-tool link; notes here |
| Hi-fi prototype | Testing visual design and interaction | Design-tool link; notes here |
| Thin vertical slice | Testing end-to-end feasibility | `03_build/<name>/` or a code repository linked here |
| Full release | After all of the above pass | Code repository; rollout plan here |

## Web-app prototypes

When the riskiest assumption needs real interaction, start from the default starter (run from the repository root):

```sh
cp -R 05_Library/_starters/next-tailwind 01_Project-Hubs/<hub-slug>/03_build/<name>
cd 01_Project-Hubs/<hub-slug>/03_build/<name> && npm install && npm run dev
```

- Generate UI from your design system, not around it:
  [`DESIGN-SYSTEM-AI-INSTRUCTIONS.md`](../../../05_Library/DESIGN-SYSTEM-AI-INSTRUCTIONS.md).
- Add a `BUILD-NOTES.md` in the prototype folder: the riskiest assumption it tests, how to run it, what is
  mocked vs. real, and links to the PRD and any decisions it depends on.
- `node_modules/`, `.next/` and other build output stay out of Git ([CONVENTIONS §8](../../../00_README/CONVENTIONS.md#8-credentials-and-secrets)).

## Engine projects

With the prototype-design (PDG) or video-production (VPG) plug-in mounted, create the engine project in this
folder — `01_Project-Hubs/<hub-slug>/03_build/<name>/` — and run the engine from its mount. The engine keeps
its state inside the project folder and owns its human gates. Commands:
[Plug-ins → Engine projects](../../../00_README/PLUGINS.md#engine-projects).

## What to capture here

- **Design handoff** —
  [`2-4-Design_handoff.template.md`](../../../00_README/_templates/2-4-Design_handoff.template.md) when it
  hasn't been written in `02_design/`
- **Test plan** — [`3-1-Build_test-plan.template.md`](../../../00_README/_templates/3-1-Build_test-plan.template.md),
  approved before the slice ships
- **Prototype notes** — what each prototype tests, what it skips, what "good" looks like
- **Evidence** — QA screenshots, test receipts and review notes in `03_build/<name>/evidence/`, never the
  repository root ([CONVENTIONS §10](../../../00_README/CONVENTIONS.md#10-generated-output-routing))

## Exit gate — Build → Learn

- [ ] The riskiest assumption is named in one sentence
- [ ] The build artifact actually tests that assumption, not a different one
- [ ] The test plan and its measurement exist before the slice ships
- [ ] The PRD's rollback trigger is still valid

Record the result in the hub README's [phase-gate table](../README.md#phase-gates). **🟢** shippable to real
users or a representative test audience; **🟡** shippable once a named dependency clears, with a trigger and
expiry (e.g., "until analytics instrumentation is verified by <date>"); **🔴** not shippable — a named blocker
and unblock owner. Privacy, security and accessibility checks are binary — 🟢 or 🔴, never 🟡
([Traffic Light](../../../00_README/_frameworks/traffic-light-decisions.md#5-integration-with-the-4-phase-loop)).

## Decisions

Fidelity choices, architecture trade-offs, scope cuts and prototype releases that later work must follow go in
[`decisions/`](decisions/README.md) as typed records.
