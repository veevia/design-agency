---
name: whiteboard-storyboard
title: Render a five-panel whiteboard storyboard
description: "Compress a user journey, before/after story, or flywheel concept into one hand-drawn five-panel storyboard a stakeholder understands in 10 seconds — rendered offline from a YAML spec (deterministic, version-controlled PNG or SVG) or as a polished image-generation prompt. Use when making a one-glance picture of a user journey or workflow, when telling a before/after story with numbers (40 minutes of morning triage → under 10), or when introducing a new mental model to cross-functional stakeholders where a paragraph is too dense and a deck too slow."
status: stable
when_to_load:
  - Making a one-glance picture of a user journey, workflow, or flywheel
  - Telling a before/after story with numbers (for example 40 minutes of morning triage → under 10)
  - Introducing a new mental model to cross-functional stakeholders
  - Adding a vision frame to a readout, POV, or status update
applies-to: journey maps, POVs, PRDs, pitches, retros, and readouts that need a visual summary
narrative: 00_README/_frameworks/extreme-clarity.md
inputs:
  - kind: parent-artifact
    where: "01_Project-Hubs/*/0[1-4]_*/**/*.md"
  - kind: storyboard-spec
    where: "01_Project-Hubs/*/**/*-storyboard.yml"
outputs:
  - kind: storyboard-image
    schema: "<slug>-storyboard.png or .svg (Mode A) and/or <slug>-storyboard.prompt.md (Mode B) beside the parent artifact; five panels, one named persona, a number in every panel"
done_when:
  - Panel 1 and panel 5 show the same named persona
  - Every panel contains at least one number; no adjective-only magnitudes
  - The title fits on one line and the subtitle defines the acronyms used
  - Any verdict or value claim in the image carries a source or effective date
  - The spec and the rendered image are filed next to the parent artifact
lints:
  - id: storyboard-spec-missing-persona
    severity: warning
    where: "01_Project-Hubs/[!_]*/**/*-storyboard.yml"
    pattern: "^panels:"
    must_also_match: "^persona_name:\\s*\\S"
    message: "Storyboard spec has no persona_name — name the one character who appears in panels 1 and 5."
budget:
  context_tokens_max: 2000
loads: [extreme-clarity]
---

# Whiteboard Storyboard

**TL;DR:** Five hand-drawn panels — before, the mechanism, a worked example, the secret sauce, the value — turn a 20-page journey into one image, rendered offline for traceability or prompted for polish.

## When to use

- One paragraph is too dense and a five-slide deck is too slow.
- A readout needs a before/after with real numbers.
- A new concept (a loop, an agent, a data model) needs a shared picture.

Not for dense data (use a chart), decisions (use a record via `traffic-light-decisions`), roadmaps (use a phase table), or system architecture diagrams.

## Steps

1. **Read the parent artifact** (journey map, POV, PRD). Identify the persona, the manual cost, the mechanism, and the after-state with its number.
2. **Copy the spec** [`templates/storyboard-input.template.yml`](templates/storyboard-input.template.yml) next to the artifact as `<slug>-storyboard.yml` and fill the five panels (≤22 lines per panel). Every word in the render comes from the spec; a few line shapes become drawings — `Thought: …` a thought bubble, an indented `a · b · c` a row of system windows, `S1 STAGE …` a flywheel stage, `a ↔ b ↔ c` a chain of linked records, an indented `· item` a checklist item (the spec's header lists them all).

   | # | Panel | Job |
   |---|---|---|
   | 1 | **Before** | The pain with a number; persona at a desk; the manual cost |
   | 2 | **The mechanism** | The new concept as one diagram — loop, agent, pipeline |
   | 3 | **Worked example** | A concrete run with receipts (table, list, or trace with sources) |
   | 4 | **The secret sauce** | The structural insight that makes panel 2 work |
   | 5 | **Value** | One after-number plus ≤4 impact bullets; the persona, now happy |

3. **Render Mode A** (offline, deterministic) from the repository root; the SVG renderer needs only PyYAML and
   drew the [example output](templates/storyboard-output.template.svg) from the
   [example spec](templates/storyboard-input.template.yml):

   ```sh
   python3 03_Agents-and-Skills/Skills/whiteboard-storyboard/scripts/render_storyboard_svg.py \
     <path>/<slug>-storyboard.yml <path>/<slug>-storyboard.svg
   ```

   For a PNG, `scripts/render_storyboard.py` (same arguments, needs matplotlib) draws typed panels —
   `type: flywheel` (`stages`, `center`), `type: stages` (`rows`), `type: value` (`metric_before`, `metric_after`,
   `bullets`); untyped panels render as a simple scene with the body text. Iterate the YAML until the image passes
   the 10-second test.
4. **Generate Mode B** (polish) from [`templates/imagegen-prompt.template.md`](templates/imagegen-prompt.template.md) and paste it into your image-generation tool.
5. **File both** beside the parent artifact; reference them from it.

## Output format

| Artifact | Path |
|---|---|
| Spec | `<workstream>/<slug>-storyboard.yml` |
| Offline render | `<workstream>/<slug>-storyboard.png` (or `.svg`) |
| Image-generation prompt | `<workstream>/<slug>-storyboard.prompt.md` |
| Polished render (optional) | `<workstream>/<slug>-storyboard.hifi.png` |

Style: hand-drawn strokes and fonts; one colour = one meaning (black outline, blue structure, green value, red problem, amber review); the same named persona in panels 1 and 5; every number numeric.

## Watch-outs

- A bullet list in panel 2 is not a diagram — draw the mechanism.
- Panel 3 without named entities and sources reads as a mock-up, not evidence.
- Red and green for the same concept confuses the colour code.
- The bundled example spec is a generic worked example (request triage across three regional sites); replace every value before sharing.

## See also

- `extreme-clarity` (the numbers test, applied visually) · `canonical-artifacts` (parent artifacts)
- Sprint method: [`storyboard`](../storyboard/SKILL.md) (frame-by-frame prototype walkthrough)
- Example output: [`templates/storyboard-output.template.svg`](templates/storyboard-output.template.svg)
