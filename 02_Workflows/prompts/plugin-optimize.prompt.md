---
description: "Improve a mounted plug-in's capabilities (for example FDE Design Toolkit skills, or a PDG or VPG workflow) from a measured baseline: report it with agency.py plugin report, check, and smoke, form one hypothesis, change it in the plug-in's own repository under its gates, propose it upstream, then re-pin and re-measure in the host — never editing the mount in place without the user's say-so."
agent: agent
---

# /plugin-optimize

Runs one cycle of the plug-in optimization initiative (`00_Agentic-OS/initiatives/plugin-optimization/`). The host is the harness; the plug-in's own repository is the editing surface.

## Inputs

- **plugin** (required): a name from `python3 06_Engine/scripts/agency.py plugin list` — for example `fde-design-toolkit`, `prototype-design`, `video-production`, `ui-ux-pro-max`
- **focus** (optional): a capability family or workflow, e.g. "discover-stage skill triggers"
- **checkout** (optional): a local clone of the plug-in repository to edit (never the mount itself)

## Procedure

1. **Check the plug-in**: `python3 06_Engine/scripts/agency.py plugin status <plugin>`. If it is not plugged in, tell the user to run `python3 06_Engine/scripts/agency.py plugin add <plugin>`, and stop.
2. **Load skills**: `goal-harness`, `rubric-authoring`, `evidence-tagging`; read the initiative's goal and rubric (see [`00_Agentic-OS/initiatives/README.md`](../../00_Agentic-OS/initiatives/README.md)).
3. **Baseline** — record the plug-in, edition, pinned commit, and the output of:
   ```sh
   python3 06_Engine/scripts/agency.py plugin report <plugin> --json   # spec, "Use when" triggers, contract coverage
   python3 06_Engine/scripts/agency.py plugin check <plugin>           # the plug-in's read-only gates
   python3 06_Engine/scripts/agency.py plugin smoke <plugin>           # engines: offline dry run in a temp folder
   ```
4. **Hypothesis** — name one change and the metric it should move (for example "add 'Use when' triggers to the 9 discover-stage skills; triggers missing 9 → 0"). Agree the measure with the user before changing anything.
5. **Change upstream** — in a separate checkout of the plug-in's repository (never `02_Workflows/prototype-design/`, `02_Workflows/video-production/`, `03_Agents-and-Skills/Skills/fde-design-toolkit/`, or `03_Agents-and-Skills/Skills/ui-ux-pro-max-skill/`), make the smallest change, then run the plug-in's own tests and gates. Apply the host's skill standards where they fit (`06_Engine/harness/skill-schema.md`).
6. **Propose** — prepare the branch and pull-request text. **Pushing a branch or opening a pull request requires the user's explicit authorization**; respect the plug-in's contribution rules and license.
7. **Re-pin and re-measure** — after the change merges and the user approves, update the submodule pin (`git -C <mount> fetch && git -C <mount> checkout <commit>`), rerun the identical baseline commands, and run `python3 00_Agentic-OS/agentic-os-review.py`. The targeted metric must move and nothing may regress; `repo-steward` commits only the new pin.
8. **Record** the cycle in `00_Agentic-OS/_runs/<YYYY-MM-DD>-<slug>.md` (baseline, change reference, old and new pin, checks, rubric verdict, rollback = re-pin the previous commit) and update the backlog row.

## Output format

```
=== /plugin-optimize <plugin> (<edition> @ <pin>) ===
Baseline: <metric = value> · check <pass/fail> · smoke <pass/fail/n.a.>
Hypothesis: <change> → <metric> <from> → <target>
Upstream: <branch / PR reference, or "awaiting authorization">
After re-pin: <metric = value> · regressions <none | list>
Verdict: PASS | ITERATE | BLOCKED — run record <path>
```

## Never

- Edit a mounted plug-in in place, or commit plug-in source through the host, without the user's explicit say-so.
- Pick the metric after the change to make it look better.
- Push, open pull requests, or publish without authorization.
