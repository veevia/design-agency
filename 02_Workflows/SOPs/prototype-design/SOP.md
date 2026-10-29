---
id: prototype-design
title: Prototype design — brief to verified prototype through the PDG plug-in
status: beta
trigger: "A product brief must become a validated, functional prototype with traceable evidence, targeted rework, and named human gates, and the prototype-design plug-in is mounted"

owner_agent: prototype-runner-qa
sub_agents:
  - design-synthesist
  - repo-steward
loads_skills:
  - goal-harness
  - design-thinking-loop
  - evidence-tagging
  - extreme-clarity
  - design-system-as-infrastructure
invokes_prompts:
  - prototype-design

produces_artifacts:
  - "01_Project-Hubs/<hub>/03_build/<name>/pdg.project.yaml"
  - "01_Project-Hubs/<hub>/03_build/<name>/controls/"
  - "01_Project-Hubs/<hub>/03_build/<name>/work/"

inputs:
  - kind: brief (the requester's words, verbatim)
    where: "01_Project-Hubs/<hub>/03_build/<name>/sources/brief.md"
  - kind: authorized sources (research, specs, analytics, prior prototypes, design-system authority)
    where: "01_Project-Hubs/<hub>/03_build/<name>/sources/"
outputs:
  - kind: release package, control documents, evidence, ledger, and manifest
    location: "01_Project-Hubs/<hub>/03_build/<name>/work/"
  - kind: run state, hash-chained ledger, task packets, escalation reports
    location: "01_Project-Hubs/<hub>/03_build/<name>/.pdg/"

done_when:
  - "`python3 06_Engine/scripts/agency.py plugin status prototype-design` showed the plug-in mounted before any engine command ran"
  - "`python -m pdg status <project>` reports RUN_PASS and the release approval names a human actor — or the run stops at WAITING_HUMAN/BLOCKED with the gate, evidence, and decider reported"
  - "`python -m pdg ledger-verify <project>` reports ok"
  - "No agent recorded an approval, unblock, risk acceptance, delegation, or rule change on its own judgement"

context_budget_tokens_max: 6000
narrative_link: ../../workflows/W3-build.md
---

# SOP — Prototype design (PDG host adapter)

## TL;DR
Drive the Prototype Production Graph from a brief to a verified prototype in the hub's `03_build/` folder: agents work task packets, checks and a real browser gate quality, defects return to the node that caused them, and named humans decide every gate.

## When to run
- A brief or product idea must become a functional prototype that is validated, not just rendered.
- Evidence, requirements, and design decisions must stay traceable from source to screen.
- A prototype received feedback that needs another loop on only the affected parts.

Not for a quick visual mock or a one-screen tweak — build those directly under W3.

## Inputs
- The brief, verbatim, plus every authorized source the product may cite (including the design-system authority from `05_Library/`).
- The named approvers for the project's human gates.

## Procedure

1. **Check the plug-in.** `python3 06_Engine/scripts/agency.py plugin status prototype-design`; if it is not plugged in, tell the user to run `python3 06_Engine/scripts/agency.py plugin add prototype-design --with-companions` and stop.
2. **Verify the engine** from the mount: `cd 02_Workflows/prototype-design && python -m pdg validate`.
3. **Scope.** `python -m pdg init ../../01_Project-Hubs/<hub>/03_build/<name> --name "<product>"`; write the brief verbatim to `sources/brief.md`; add sources; record the approvers in `pdg.project.yaml`.
4. **Drive the loop** with `/prototype-design`: `pdg run` → `pdg status` / `pdg tasks` → work packets as `agent:<role>` → `pdg check-node` → submit → `pdg run` again.
5. **Stop at every WAITING_HUMAN or BLOCKED** and report the decision, its evidence, and the decider. Record a human's decision only in their own stated words.
6. **Hand off** status, package, open human dimensions, and the learning proposal; commits go through `repo-steward`.

## Outputs
- The PDG project under `<hub>/03_build/<name>/` with its run state, ledger, and package

## Done when
See front-matter.

## Failure modes
- **Plug-in not mounted:** stop after step 1 and give the `plugin add` command.
- **Refused submission (exit 4):** nothing changed; fix the named problem and resubmit.
- **A defect would change a locked control document:** raise a change request for the named human; never edit `.pdg/` or approved controls by hand.
- **The engine itself needs a fix:** propose it upstream with `/plugin-optimize`; never edit the mount.

## See also
- [`/prototype-design`](../../prompts/prototype-design.prompt.md) · agent [`prototype-runner-qa`](../../../03_Agents-and-Skills/Agents/prototype-runner-qa.agent.md) · [W3 — Build](../../workflows/W3-build.md)
