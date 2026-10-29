---
type: goal
slug: plugin-optimize-loop
owner: OS steward
created: 2026-10-29
updated: 2026-10-29
agent: goal-runner
status: standing
rubric: ./plugin-optimize.rubric.md
source: ../../OPTIMIZATION-BACKLOG.md
tags: [type/goal, purpose/measure, status/standing, scope/plugins, scope/fde, scope/design-ops]
outcome: >-
  Raise the measured quality of one plug-in's capabilities per cycle — for example FDE toolkit skill triggers
  and contracts, or a PDG/VPG workflow's reliability — and deliver the change upstream to the plug-in's own
  repository, then re-pin the host to the improved commit.
verification: >-
  Capture the baseline with python3 06_Engine/scripts/agency.py plugin report <name> --json plus
  plugin check and, for engines, plugin smoke. After the upstream change is merged and the mount re-pinned,
  rerun the same commands; the targeted metric improves and no check regresses. Keep
  python3 00_Agentic-OS/agentic-os-review.py at VERDICT PASS in the host.
constraints: >-
  Never edit a mounted plug-in in place or commit plug-in changes through the host. Respect the plug-in's own
  contribution rules, license and review. Do not tune a metric the plug-in's maintainers did not accept as a
  quality signal; agree the measure first. Publishing a branch or opening a pull request needs authorization.
iteration_policy: >-
  Pick one capability family or workflow; record the baseline; form one hypothesis; change the smallest set of
  files in a checkout of the plug-in repository; run the plug-in's own tests and gates; propose it upstream;
  after merge, update the submodule pin in the host and re-measure. Do not retry an unchanged failing hypothesis.
error_handling: >-
  Stop for missing access to the plug-in repository, failing plug-in gates you cannot explain, a disputed
  measure or a regression in another capability. Record the blocker and the resume step in the run record.
output_expectation: >-
  A run record in 00_Agentic-OS/_runs/ with baseline and after reports, the upstream change reference, the new
  pinned commit, checks and verdict; an updated backlog row.
---

# Standing plug-in optimization loop (FDE and design ops)

**TL;DR:** Measure a plug-in in the host, improve it in its own repository, re-pin and re-measure; the host is the harness, never the editing surface.

## Typical measures

| Plug-in | Baseline command | Signals |
|---|---|---|
| FDE Design Toolkit | `agency.py plugin report fde-design-toolkit --json` and `plugin check` | Skills with spec issues, missing "Use when" triggers, contract coverage, toolkit gates |
| PDG | `agency.py plugin check prototype-design` and `plugin smoke prototype-design` | Graph validity, docs drift, offline dry-run and ledger verification |
| VPG | `agency.py plugin check video-production` and `plugin smoke video-production` | Graph validity, docs drift, offline dry-run result |

## The loop

Baseline → one hypothesis → change in the plug-in repository → plug-in gates → upstream review →
re-pin the submodule (`git -C <mount> fetch && git -C <mount> checkout <commit>`, then commit the pin) →
re-measure → [run record](../../_runs/README.md). Score with [plugin-optimize.rubric.md](plugin-optimize.rubric.md).

## Non-goals

- No in-place edits to a mounted plug-in; no vendored forks hidden in the host.
- No metric chosen after the fact to make a change look better.
