---
id: video-production
title: Video production — demo film through the VPG plug-in
status: beta
trigger: "A product demo film must be produced or revised to a measured quality bar with named human approvals, and the video-production plug-in is mounted"

owner_agent: demo-deck-producer
sub_agents:
  - repo-steward
loads_skills:
  - goal-harness
  - evidence-tagging
  - extreme-clarity
  - whiteboard-storyboard
  - design-system-as-infrastructure
invokes_prompts:
  - video-production

produces_artifacts:
  - "01_Project-Hubs/<hub>/03_build/<name>/vpg.project.yaml"
  - "01_Project-Hubs/<hub>/03_build/<name>/work/"

inputs:
  - kind: brief (verbatim) and product evidence (spec, prototype capture, recording)
    where: "01_Project-Hubs/<hub>/03_build/<name>/sources/"
  - kind: bound renderer, narration, and assembly commands
    where: "01_Project-Hubs/<hub>/03_build/<name>/vpg.project.yaml"
outputs:
  - kind: measured film versions, reviews, and the release package
    location: "01_Project-Hubs/<hub>/03_build/<name>/work/"
  - kind: run state, ledger, task packets, escalations
    location: "01_Project-Hubs/<hub>/03_build/<name>/.vpg/"

done_when:
  - "`python3 06_Engine/scripts/agency.py plugin status video-production` showed the plug-in mounted before any engine command ran"
  - "`python -m vpg status <project>` reports RUN_PASS after the named humans' gates — or the run stops at WAITING_HUMAN/BLOCKED with the gate, evidence, and decider reported"
  - "`python -m vpg ledger-verify <project>` reports ok"
  - "No agent ran a human-only command (approve, unblock, resolve, grant, memory, rollback) or claimed a listening or taste approval"

context_budget_tokens_max: 6000
narrative_link: ../../workflows/W4-learn.md
---

# SOP — Video production (VPG host adapter)

## TL;DR
Drive the Video Production Graph to a demo film in the hub's `03_build/` folder: agents create through task packets, tools measure audio, legibility, captions, and accuracy, defects are reworked at their source, and named humans approve.

## When to run
- A product demo film or walkthrough must be produced, or a version revised from feedback.
- Product claims, terminology, and UI shown must stay grounded in locked sources.

## Inputs
- The brief, verbatim, product evidence, and brand authority.
- `ffmpeg` and `ffprobe` on `PATH` (and `tesseract` when OCR privacy scanning is enabled).
- The named reviewers for the five human gates.

## Procedure

1. **Check the plug-in.** `python3 06_Engine/scripts/agency.py plugin status video-production`; if it is not plugged in, tell the user to run `python3 06_Engine/scripts/agency.py plugin add video-production --with-companions` and stop.
2. **Verify the engine** from the mount: `cd 02_Workflows/video-production && python -m vpg validate`.
3. **Scope.** `python -m vpg init ../../01_Project-Hubs/<hub>/03_build/<name> --name "<film>" --human "<reviewer>"`; add the brief and sources; bind tools in `vpg.project.yaml`.
4. **Drive the loop** with `/video-production`: `vpg run` → `vpg status` / `vpg tasks` → work packets as `agent:<role>` → submit → `vpg run` again.
5. **Stop at every WAITING_HUMAN or BLOCKED** and report what the gate decides and where its evidence is.
6. **Hand off** status, version, package path and sha256, open human dimensions, and the learning proposal.

## Outputs
- The VPG project under `<hub>/03_build/<name>/` with measured versions, ledger, and package

## Done when
See front-matter.

## Failure modes
- **Plug-in not mounted or media tools missing:** stop and report the exact command or tool needed.
- **A tool fails a MUST dimension:** fix the output; never argue the measurement.
- **A defect needs a locked control document changed:** open a change request for the named human.

## See also
- [`/video-production`](../../prompts/video-production.prompt.md) · agent [`demo-deck-producer`](../../../03_Agents-and-Skills/Agents/demo-deck-producer.agent.md) · [W4 — Learn](../../workflows/W4-learn.md)
