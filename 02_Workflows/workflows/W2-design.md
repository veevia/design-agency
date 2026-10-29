---
title: "W2 — Design"
type: workflow
workflow-id: W2
status: canonical
owner: OS steward
last-updated: 2026-10-29
loop-phase: design
inputs:
  - Signed-off UNDERSTAND artifacts (research, persona, JTBD, journey map)
outputs:
  - design-pov.md
  - design-brief.md
  - product-prd.md
source: design-thinking-loop.md + 2-1-Design_POV.template.md + 2-2-Design_brief.template.md + 2-3-Design_PRD.template.md
tags: [type/workflow, loop/design, purpose/align, status/canonical]
---

# W2 — Design

> **TL;DR:** Translate understanding into a committed design stance (POV), a client/team-facing brief, and a buildable PRD. Exit the phase with a signed PRD.

## When to run

- After **W1 — Understand** gate has cleared
- When scope changes materially mid-build (revisit POV, amend brief + PRD via new versions)
- When evidence from LEARN invalidates the POV — go back to W2 before re-entering Build

## Who runs it

| Role | Responsibility |
|---|---|
| Design lead | Drives POV and brief |
| PM (or design lead wearing PM hat) | Drives PRD |
| Engineering lead | Reviews PRD for feasibility; signs |
| Sponsor | Signs brief + PRD |

## Capabilities used

- Skills: `house-principles`, `alignment-playbook`, `canonical-artifacts`, `extreme-clarity`, `traffic-light-decisions` (only through W5)
- Prompts: `/design-pov`, `/design-brief`, `/prd-draft`, `/trade-off`, `/go-wider`
- Agent: `design-synthesist`; `design-sprint-toolkit` (Define, Sketch, Decide phases)

## What cross-functional partners will see

| Partner | They'll receive | They'll be asked to | Time |
|---|---|---|---|
| PM | POV draft; brief draft; co-ownership of PRD | Debate POV; co-author PRD; sign brief + PRD; own non-goals + guardrail metrics | 4–6 hrs |
| Engineering lead | POV; brief; full PRD | Review PRD for feasibility; flag anything needing a prototype to answer; sign | 2–3 hrs |
| Marketing / GTM | POV; brief | Review POV for market fit and positioning; sign brief | 1 hr |
| Legal / Privacy / Security | PRD §Privacy / §Security / §Compliance sections | Sign their sections 🟢 or flag 🔴. Binary, not 🟡 | 1 hr |
| Executive sponsor | Brief; PRD | Sign brief and PRD; break ties when the room can't | 1 hr |
| Everyone | Relevant rationale in the design artifacts; new durable choices typed through W5 only when needed | Review when invited; retain real feedback and disagreements | ongoing |

## Steps

### Step 1 — Draft the Design POV

1. Use `/design-pov` prompt with UNDERSTAND artifacts as inputs.
2. Fill `2-1-Design_POV.template.md`. The POV is one sentence: "We believe &lt;persona&gt; needs &lt;change&gt; because &lt;insight&gt;. We will win when &lt;outcome&gt;."
3. Name who we design AGAINST — the anti-persona.
4. Write 3–5 design principles, each with a corollary (what we reject).
5. Name "what would make us wrong" — the evidence that would invalidate the POV.

**Exit criterion:** POV passes the "could this be the POV for any product?" test — if yes, sharpen.

### Step 2 — Surface disagreement on the POV

1. Per `alignment-playbook.md`: ask each stakeholder privately "what's the strongest case against this POV?"
2. Write answers into POV §9. By name where appropriate.
3. If no one disagrees, probe harder. Silent agreement on a POV is usually compliance.

**Exit criterion:** POV §9 has real content or explicit "invited, none surfaced."

### Step 3 — Commit the POV (Traffic Light)

1. Design lead decides. Log Traffic Light on POV §10.
2. 🟢 if team commits; 🟡 if a named research question must close first (set trigger + expiry); 🔴 if fundamental disagreement remains.
3. Preserve the rationale in the POV. Use [W5 — Decide](W5-decide.md) if a separate durable record is
   needed: product/design choices are PDRs; ADRs are reserved for architecture. Do not duplicate the POV.

**Exit criterion:** POV Traffic Light set.

### Step 4 — Draft the Design Brief

1. Use `/design-brief` prompt with POV + UNDERSTAND artifacts.
2. Fill `2-2-Design_brief.template.md`. Keep it short — a brief over 2 pages usually isn't a brief.
3. Copy the POV sentence verbatim into §4. Not a rewrite.
4. Name three outcomes with metrics (baseline, target, window). Not more.
5. Fill scope-out explicitly. Scope-out that reads "we'll think about that later" is scope creep waiting to happen — name it as a risk.

**Exit criterion:** Brief passes the "could a new team member build from this?" test.

### Step 5 — Review the Design Brief with sponsor and engineering

1. 30–45 min review. TL;DR + outcomes + scope + risks.
2. Surface disagreement. Update brief if warranted.
3. Sponsor + engineering lead sign off with Traffic Lights in §12.

**Exit criterion:** Brief signed 🟢 by sponsor and engineering lead.

### Step 6 — Draft the Product PRD

1. Use `/prd-draft` prompt with brief + POV + UNDERSTAND artifacts.
2. Fill `2-3-Design_PRD.template.md`.
3. Be strict with non-goals (§5). This is the section most likely to prevent scope creep.
4. Name guardrail metrics (§6) — things that must NOT degrade.
5. Write user stories with acceptance criteria summaries.
6. Non-functional requirements cover performance, accessibility, security, privacy — not "TBD."
7. Enumerate edge cases and error states.
8. Rollout plan has trigger and mechanism for rollback. A PRD without a rollback plan is a wish.

**Exit criterion:** PRD drafted; open questions are listed with owners and due dates.

### Step 7 — PRD review cycle

1. Silent review first (document comments, PR review, or equivalent). No meeting yet.
2. Resolve comments → version 2.
3. Review meeting (~60 min) with engineering, design, sponsor, data, security/privacy as relevant.
4. Version 3 incorporates meeting feedback.

**Exit criterion:** No open blockers; open questions have closure plans.

### Step 8 — Close open questions

1. Resolve each open question in PRD §11 with current evidence, reused rationale, or scheduled research.
   Use W5 only for a new durable choice, explicit capture request, or lifecycle change.
2. Block PRD approval until questions close — or explicitly defer with a trigger for reopening.

**Exit criterion:** PRD §11 open questions either closed with evidence/reused rationale or explicitly deferred with a trigger.

### Step 9 — PRD sign-off

1. Every row in PRD §13 gets a name, date, and Traffic Light.
2. PRD is approved when all required rows are 🟢 (or 🟡 with named trigger + expiry).

**Exit criterion:** PRD approved.

### Step 10 — Close the phase gate

Per `design-thinking-loop.md` DESIGN → BUILD gate:

- [ ] PRD is signed 🟢 by decision owner
- [ ] Open questions are either answered or logged as 🟡 with trigger and expiry
- [ ] Engineering lead confirms PRD is buildable within constraints

Record the gate result, sign-off, and next phase in the existing PRD or project phase block.
Phase closure alone needs no new decision file.

## Stop conditions

- Cannot name three outcomes with metrics → go back to UNDERSTAND. The evidence isn't concrete enough.
- Non-goals section is empty → PRD is not ready; force the team to name what's out.
- Engineering lead refuses sign-off citing feasibility → either PRD scope shrinks, constraints change, or the engagement descopes. Don't push through a red feasibility signal.

## Artifacts produced

- `<design-scope>/design-pov.md`
- `<design-scope>/design-brief.md`
- `<design-scope>/product-prd.md`
- Phase-gate evidence in the PRD or project phase block
- `<design-scope>/decisions/<topic>.md` only for a durable choice needing its own typed record through W5

`<design-scope>` is either `<project-hub>/02_design/` or a feature sub-hub beneath it. Keep all artifacts and decisions for one workstream in the same scope.

## Next workflow

→ **W3 — Build**

---

*Workflow grounded in `design-thinking-loop.md` DESIGN phase. PRD sign-off is the hard gate; soft gates inside are POV commit and brief sign-off. Move on only when Traffic Lights are green.*
