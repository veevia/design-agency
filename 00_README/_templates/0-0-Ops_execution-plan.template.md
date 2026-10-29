---
title: "Execution Plan — <program or OS rollout>"
type: template
template-for: execution-plan
status: canonical
owner: OS steward
last-updated: 2026-10-29
loop-phase: all
source: Phased-delivery practice + design-thinking-loop.md + traffic-light-decisions.md
tags: [type/template, type/plan, purpose/build, loop/all, status/canonical]
---

<!--
  EXECUTION PLAN
  A phased plan for standing up or running something bigger than one
  project loop: a multi-hub design program, a team's adoption of this OS,
  or a capability rollout. One file per program. It records the stack you
  run on, the phases you commit to, what each phase leaves behind, and
  what you deliberately deferred.

  Not a project plan for a single feature — that's the hub README plus
  the Design Brief and PRD.

  Copy to: 01_Project-Hubs/<hub>/execution-plan.md (program) or
  00_Agentic-OS/initiatives/<name>-execution-plan.md (OS rollout). Both sit
  at the same depth as this template, so its relative links keep working.
  Remove this comment block before using.
-->

# Execution Plan — &lt;program or rollout name&gt;

> **TL;DR:** &lt;One sentence — what we are standing up, for whom, by when, and the single riskiest dependency.&gt;

| Field | Value |
|---|---|
| Owner | &lt;single name&gt; |
| Sponsor | &lt;name, role&gt; |
| Timeframe | YYYY-MM-DD → YYYY-MM-DD |
| Current phase | &lt;phase # and name&gt; |
| Overall light | 🟢 🟡 🔴 — &lt;one-sentence reason with a number&gt; |

---

## 1. The stack we run on

Name what this program uses instead of restating it. Delete rows that don't apply.

| Layer | We use | Source |
|---|---|---|
| Process | Understand → Design → Build → Learn | [`design-thinking-loop.md`](../../00_README/_frameworks/design-thinking-loop.md) |
| Artifacts | &lt;which templates, e.g., problem frame, JTBD, POV, PRD&gt; | [Template catalog](../../00_README/_templates/README.md) |
| Workflows | &lt;W1–W5 subset&gt; | [`02_Workflows/`](../../02_Workflows/README.md) |
| Decisions | Typed records via W5, Traffic Light on ADRs/PDRs | [`traffic-light-decisions.md`](../../00_README/_frameworks/traffic-light-decisions.md) |
| Plug-ins | &lt;none, or e.g. prototype-design for PDG runs&gt; | [`PLUGINS.md`](../../00_README/PLUGINS.md) |
| Rhythm | &lt;meeting capture, opt-in weekly status&gt; | [`0-2-Ops_operating-rhythm.template.md`](../../00_README/_templates/0-2-Ops_operating-rhythm.template.md) |

---

## 2. Phase plan

Each phase leaves something behind that the next phase stands on. A phase without exit evidence is a wish.

| # | Phase | Goal (one sentence) | Leaves behind | Exit evidence | Owner | Target | Light |
|---|---|---|---|---|---|---|---|
| 1 | &lt;e.g., "Stand up the first hub"&gt; | &lt;e.g., "The design team runs one loop end to end in the OS"&gt; | &lt;hub, intake, problem frame&gt; | &lt;e.g., "Problem frame reviewed by PM and eng lead"&gt; | &lt;name&gt; | YYYY-MM-DD | 🟢 🟡 🔴 |
| 2 | &lt;...&gt; | | | | | | |
| 3 | &lt;...&gt; | | | | | | |

Yellow rows name a trigger and an expiry in the notes below; Red rows name a blocker and an unblock owner.

---

## 3. Phase log

Append one entry when a phase closes. Facts first: what was introduced, what was retired, where the evidence lives.

### Phase &lt;N&gt; — &lt;name&gt; (closed YYYY-MM-DD)

- **Introduced:** &lt;templates, workflows, skills, plug-ins, hubs&gt;
- **Retired:** &lt;what was removed and why — recover from Git history if needed&gt;
- **Evidence:** &lt;links to the artifacts, run folders or decision records that prove the exit&gt;
- **Learned:** &lt;one or two sentences that change the next phase&gt;

*Example (fictional):* **Phase 1 — First hub (closed 2026-03-14).** Introduced the `pilot-project` hub, intake and problem frame. Retired the old slide-based kickoff. Evidence: `01_Project-Hubs/pilot-project/01_understand/problem-frame.md`. Learned: stakeholders answered the async input form faster than they booked interviews.

---

## 4. Deferred candidates

Things we chose not to do yet. Each has a trigger that would make us pick it up. Cross-workspace improvements belong in the OS backlog (`00_Agentic-OS/OPTIMIZATION-BACKLOG.md`), not here.

| Candidate | Why deferred | Pick up when |
|---|---|---|
| &lt;e.g., "Video demo via the video-production plug-in"&gt; | &lt;e.g., "No external audience yet"&gt; | &lt;e.g., "First customer showcase is scheduled"&gt; |

---

## 5. Open questions

Discovery questions, not blockers. Blockers go in §2 as 🔴 with an unblock owner.

1. &lt;question — owner — by when&gt;
2. &lt;...&gt;

---

## Quality check

- [ ] TL;DR names the riskiest dependency
- [ ] Every phase has exit evidence a skeptic could open
- [ ] Every 🟡 has a trigger + expiry; every 🔴 has an unblock owner
- [ ] Deferred candidates each have a pick-up trigger
- [ ] Nothing in this plan restates policy that lives in CONVENTIONS or a framework — it links instead
