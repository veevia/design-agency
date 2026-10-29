---
description: "Host adapter for the Prototype Production Graph (PDG) plug-in: take a brief to a validated, functional prototype in a hub's 03_build/ folder — agents work task packets and submit through the engine, deterministic and browser checks gate quality, defects are reworked at their source node, and named humans make every gate decision."
agent: agent
---

# /prototype-design

Drive the PDG engine (19 nodes, eight phases, six human gates) from this workspace. The engine is a plug-in mounted at `02_Workflows/prototype-design/`; this prompt only drives its CLI. Procedure contract: [SOP `prototype-design`](../../02_Workflows/SOPs/prototype-design/SOP.md).

## Inputs

- **hub** (required): the project hub, e.g. `example-project`
- **name** (required): the prototype folder name, e.g. `triage-console`
- **goal** (optional): what this pass must achieve — "new prototype from the brief", "apply feedback on v2", "prepare release"
- **feedback** (optional): reviewer notes, verbatim, each with the screen or state it concerns

## Procedure

1. **Check the plug-in first**:
   ```sh
   python3 06_Engine/scripts/agency.py plugin status prototype-design
   ```
   If it reports that the plug-in is not plugged in, tell the user to run `python3 06_Engine/scripts/agency.py plugin add prototype-design --with-companions`, and **stop**.
2. **Load skills in order**: `goal-harness` (state the pass's five elements), `design-thinking-loop` (phase gates), `evidence-tagging` and `extreme-clarity` (every summary you show), `design-system-as-infrastructure` (UI work). Each task packet names its node's own skills — load those per packet, not up front.
3. **Verify the engine once per machine** (from the mount): `cd 02_Workflows/prototype-design && python -m pdg validate` (add `python -m pdg dry-run --out <empty scratch folder>` on a new machine).
4. **Scope the project** — it lives at `01_Project-Hubs/<hub>/03_build/<name>/`:
   - New: `cd 02_Workflows/prototype-design && python -m pdg init ../../01_Project-Hubs/<hub>/03_build/<name> --name "<product>"`. Put the brief **verbatim** in `sources/brief.md`, add the authorized sources (research, specs, the design-system authority from `05_Library/`), and ask the user to name the approvers in `pdg.project.yaml` (`humans:`).
   - Existing: record each feedback note in the reviewer's exact words with `python -m pdg feedback <project> --actor "<reviewer>" --text "<their words>"` — only when the reviewer asked you to transcribe it.
5. **Drive the loop** (all commands from `02_Workflows/prototype-design/`, where `<project>` is `../../01_Project-Hubs/<hub>/03_build/<name>`):
   - `python -m pdg run <project>` advances until the graph waits; then `python -m pdg status <project>` and `python -m pdg tasks <project>`.
   - **WAITING_AGENT** → for each packet in `<project>/.pdg/tasks/`, do the node's work as its bound role (or hand it to `prototype-runner-qa`): write only the declared outputs; dry-run with `python -m pdg check-node <project> <node> --output key=path …`; submit with the packet's exact command and `--actor agent:<role>`. A refused submission (exit 4) changed nothing — fix and resubmit. Tool failures on MUST dimensions are final: fix the output, never argue the score.
   - **WAITING_HUMAN** → **stop.** Show the gate's decision with a one-line TL;DR, evidence-tagged claims, and links to the reviews, screenshots, and gate report. The named human decides; record it only when they state it in their own words (`python -m pdg approve <project> <node> --actor "<their name>" --reason "<their words>" --recorded-by agent:<role> --source "<where and when>"`), or let them run it.
   - **BLOCKED** → stop and report the escalation in `<project>/.pdg/` with the resume step.
6. **Hand off**: status, build version, package path and manifest, open human dimensions, any simulated evidence (labelled as simulated), and the learning proposal. Do not commit, publish, or apply rule or memory changes unless the user asks — commits go through `repo-steward`.

## Never

- Approve, unblock, accept a risk or a ledger break, delegate, ratify, or apply memory changes on a human's behalf without their explicit words.
- Edit `.pdg/` state, the ledger, or an approved control document by hand (use `pdg change-request`).
- Edit the mounted engine; improvements go upstream through [`/plugin-optimize`](../../02_Workflows/prompts/plugin-optimize.prompt.md).
- Present dry-run sessions or approvals as user evidence or human decisions.
- Restart the whole run to fix one defect, or redesign what the defect did not scope.
