---
description: "Host adapter for the Video Production Graph (VPG) plug-in: produce or revise a product demo film in a hub's 03_build/ folder — agents work task packets, deterministic tools measure audio, legibility, captions, and accuracy, defects are reworked at their source node, and named humans make every approval."
agent: agent
---

# /video-production

Drive the VPG engine (25 nodes, seven phases, five human gates) from this workspace. The engine is a plug-in mounted at `02_Workflows/video-production/`; this prompt only drives its CLI. Procedure contract: [SOP `video-production`](../../02_Workflows/SOPs/video-production/SOP.md).

## Inputs

- **hub** (required): the project hub, e.g. `example-project`
- **name** (required): the film folder name, e.g. `triage-demo`
- **goal** (optional): "new film from the brief", "apply feedback on v3", "prepare release"
- **feedback** (optional): reviewer notes, verbatim, with timestamps where given

## Procedure

1. **Check the plug-in first**:
   ```sh
   python3 06_Engine/scripts/agency.py plugin status video-production
   ```
   If it reports that the plug-in is not plugged in, tell the user to run `python3 06_Engine/scripts/agency.py plugin add video-production --with-companions`, and **stop**. VPG also needs `ffmpeg` and `ffprobe` on `PATH` (and `tesseract` when OCR privacy scanning is on).
2. **Load skills**: `goal-harness` (the pass's five elements), `evidence-tagging` and `extreme-clarity` (every summary you show), `whiteboard-storyboard` (storyboards), `design-system-as-infrastructure` (on-brand visuals). Each packet names its node's own capabilities — use local equivalents.
3. **Verify the engine once per machine**: `cd 02_Workflows/video-production && python -m vpg validate` (add `python -m vpg dry-run` on a new machine).
4. **Scope the project** — it lives at `01_Project-Hubs/<hub>/03_build/<name>/`:
   - New: `cd 02_Workflows/video-production && python -m vpg init ../../01_Project-Hubs/<hub>/03_build/<name> --name "<film>" --human "<named reviewer>"`. Put the brief verbatim in `sources/brief.md`, add product evidence (spec, prototype capture, recording) and brand authority, and bind renderer, narration, and assembly commands in `vpg.project.yaml`.
   - Existing: register the reviewer's notes in their exact words as the engine's feedback (or as a project source), only when they asked you to.
5. **Drive the loop** (from `02_Workflows/video-production/`, `<project>` = `../../01_Project-Hubs/<hub>/03_build/<name>`):
   - `python -m vpg run <project>` advances until the run waits; `python -m vpg status <project>` and `python -m vpg tasks <project>` show why.
   - **WAITING_RUNTIME** → work each packet in `<project>/.vpg/tasks/` (or hand it to `demo-deck-producer`): write only its declared outputs, validate them against the packet's schema, and submit with the packet's exact command and `--actor agent:<role>`. Run `vpg run` again after each submission. Never review an attempt you produced.
   - **WAITING_HUMAN** → **stop.** Tell the named human what the gate decides (objective, product truth, creative direction, visual system, or final listening and release) and where the evidence is: review files, frames, measurements.
   - **BLOCKED** → stop and report the escalation in `<project>/.vpg/escalations/`.
6. **Hand off**: status, version, package path and sha256, open human dimensions (listening, taste), and the learning proposal. Verify the ledger with `python -m vpg ledger-verify <project>`. Do not commit, publish, or apply rule changes unless the user asks.

## Never

- Run `approve`, `unblock`, `resolve`, `restore-control`, `accept-config`, `accept-ledger-break`, `rollback`, `grant`, or `memory` commands for a human, or use a person's name in `--actor`.
- Claim a human dimension (voice, music, taste, listening, release) passed.
- Edit `.vpg/` state, the ledger, an approved control document, or the mounted engine by hand.
- Invent product claims, metrics, UI, sources, or rights; restart the whole film to fix one defect.
