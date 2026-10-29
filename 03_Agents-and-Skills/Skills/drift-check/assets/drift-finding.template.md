---
type: evaluation
status: draft
# light: green = 🟢 stay the course | yellow = 🟡 watch | red = 🔴 go wider now
light: green
owner: <single-name>
# yellow only: trigger + expiry · red only: blocker + unblock_owner
trigger: <what closes a yellow>
expiry: <YYYY-MM-DD>
blocker: <what blocks progress>
unblock_owner: <single-name>
loop-phase: build
informed-by: <relative path to the brief/PRD this build is drifting from>
tags: [type/evaluation, status/draft, loop/build]
---
# Drift check — <Hub> / <build>

**TL;DR:** <one sentence — is the build still on-intent, and the verdict>.

Reuse this structure in the answer or existing build notes. Create a separate evaluation only when
needed; keep it outside `decisions/`. A routine drift assessment needs no new decision file.

## Signals (present / absent, with evidence)

<!--
  drift-check: each PRESENT signal must cite SPECIFIC evidence (tag it observed/reported/
  assumed — load evidence-tagging). "Feels off" is a prompt to investigate, not a finding.
-->

| Signal | Present? | Evidence | Response |
|---|---|---|---|
| Feedback keeps circling the same question | ✅/❌ | <cite> [reported \| <source>] | Stop refining; generate real alternatives, compare side by side |
| Something feels off, no one can say why | ✅/❌ | <cite> | Pull the full flow E2E; outside perspective; ground in research |
| Build feels far from the original pitch | ✅/❌ | <cite> [observed \| <source>] | Put build next to the brief/PRD; name what changed and why |
| Can't pick one direction over another | ✅/❌ | <cite> | Go wider (`/go-wider`); name trade-offs (`/trade-off`); test top contenders |

## What changed vs the original brief

- <named scope shift> — <when / why>

## Verdict

🟢🟡🔴 — <one-line rationale>

- 🟢 Green: on-intent, stay the course.
- 🟡 Yellow: watch — needs `trigger:` + `expiry:` (what would force a course-correct, by when).
- 🔴 Red: drifted — go wider now; name the alternatives to generate.

<!--
  Retain evidence, owner, and any conditional fields in this assessment.
  If a new durable choice, explicit capture request, or lifecycle change needs a decision record,
  follow W5, reuse existing rationale first, and validate THAT typed record with check_decision.py.
  This evaluation is not a decision-record/v2 record.
-->
