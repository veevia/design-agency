---
title: "Operating Rhythm — <project>"
type: template
template-for: operating-rhythm
status: canonical
owner: OS steward
last-updated: 2026-10-29
loop-phase: all
source: weekly-status + meeting-notes + decision-record + extreme-clarity.md + traffic-light-decisions.md + alignment-playbook.md
tags: [type/template, type/meeting, type/status, purpose/report, purpose/decide, loop/all, status/canonical]
---

<!--
  OPERATING RHYTHM — how the project runs week to week.

  Three sections, three cadences, one system:
    §A  Meeting capture    — one per meeting (10 min to fill)
    §B  Decision routing   — only when a new durable choice needs its own record
    §C  Status             — opt-in; one per reporting cycle (10 min to fill)

  The flow: meetings (§A) surface decisions; durable ones become typed
  records (§B); relevant outcomes surface in the status rollup (§C) when
  the hub reports. Action items from §A feed the existing task plan.

  HOW TO USE:
    Copy §A → <project-hub>/00_context_intake/YYYY-MM-DD-<slug>.md
    §B     → follow W5; copy the matching typed template into
             <project-hub>/<phase>/decisions/<descriptive-slug>.md
    Copy §C → <project-hub>/weekly-status/YYYY-MM-DD-status.md
             (create weekly-status/ only if the project has a real reporting cadence)

  Links: this template is copied into hub phase folders, so it names repo
  files with repo-root paths in backticks instead of relative links.

  Remove this comment block before using on a real project.
-->

# Operating Rhythm — &lt;project name&gt;

**TL;DR:** Three cadences, one system — capture every meeting (§A), route only durable choices through W5 into typed records (§B), and, if the hub reports, roll outcomes into a one-screen status (§C).

```
  Any meeting          When a durable choice surfaces     Reporting cycle (opt-in)
  ┌─────────┐          ┌──────────────────┐              ┌──────────┐
  │ §A Meet  │────────▶│ §B Decide + 🟢🟡🔴│─────────────▶│ §C Status│
  │ capture  │         │ (typed, via W5)  │              │ rollup   │
  └─────────┘          └──────────────────┘              └──────────┘
       │                                                      ▲
       └──── action items ────────────────────────────────────┘
```

---

## A. Meeting capture

*One per meeting. Copy this section into `<project-hub>/00_context_intake/YYYY-MM-DD-<slug>.md`. Keep it to one page — if you can't, the meeting was too long.*

### &lt;topic&gt; — YYYY-MM-DD

| Field | Value |
|---|---|
| Date | YYYY-MM-DD |
| Duration | &lt;minutes&gt; |
| Source | &lt;link to transcript / recording, or "live notes"&gt; |

**Attendees:** &lt;names, comma-separated&gt;

**Key points** *(3–5 bullets — what someone who wasn't there needs to know):*

- &lt;...&gt;
- &lt;...&gt;
- &lt;...&gt;

**Decisions made** *(reuse sufficient rationale; use §B only when a separate durable record is needed):*

| Decision | Owner | Traffic Light | Rationale / record link |
|---|---|---|---|
| &lt;one sentence&gt; | &lt;name&gt; | 🟢 🟡 🔴 | &lt;existing evidence, inline rationale, or typed-record link&gt; |

**Action items** *(these feed the task plan and the next §C, if the hub reports):*

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | &lt;...&gt; | &lt;name&gt; | YYYY-MM-DD |
| 2 | | | |

**Open questions:**

- &lt;...&gt;

---

## B. Decision record

*First reuse sufficient task/runbook/release rationale. Follow W5 (`02_Workflows/workflows/W5-decide.md`)
only for a new durable choice, explicit capture request, or lifecycle change. Copy the smallest
matching strict template only when needed; do not default every record to ADR.*

| Durable fact | Record type |
|---|---|
| Architecture/trust/cross-component boundary | ADR |
| Product/design/scope/experience choice | PDR |
| Maintenance/incident/reversible setting/cleanup | Ops note |
| Promotion/launch/release result | Release |

Template router:
`03_Agents-and-Skills/Skills/traffic-light-decisions/assets/decision-record.template.md`.

Every record uses a canonical ID (`<hub-slug>-NNNN`), lifecycle `status`, honest `consultation`, and
type-specific evidence. ADRs/PDRs also use a Traffic Light. Validate before filing:

```sh
python3 03_Agents-and-Skills/Skills/traffic-light-decisions/scripts/check_decision.py <record>
```

---

## C. Weekly status *(opt-in)*

*One per reporting cycle, only for hubs with a real stakeholder cadence. Copy this section into `<project-hub>/weekly-status/YYYY-MM-DD-status.md`. Must fit one screen.*

### Weekly Status — &lt;project&gt; — YYYY-MM-DD

> **TL;DR:** &lt;Overall 🟢🟡🔴 — one sentence with a number. e.g., "🟢 PRD signed; Build kicks off Monday. One open 🟡 on analytics instrumentation, closes Wed."&gt;

| Field | Value |
|---|---|
| Week of | YYYY-MM-DD |
| Loop phase | Understand \| Design \| Build \| Learn |
| Lead | &lt;name&gt; |

**Health:**

| Area | Light | Reason (one sentence, with a number) |
|---|---|---|
| Scope | 🟢 🟡 🔴 | &lt;...&gt; |
| Timeline | 🟢 🟡 🔴 | &lt;...&gt; |
| Quality | 🟢 🟡 🔴 | &lt;...&gt; |
| Stakeholders | 🟢 🟡 🔴 | &lt;...&gt; |

**Shipped this week** *(deltas, not totals):*

- &lt;artifact or decision — link&gt;
- &lt;...&gt;

**Planned next week:**

- &lt;item — owner&gt;
- &lt;...&gt;

**Blockers and risks:**

| # | Item | Owner | Light | Action | Due |
|---|---|---|---|---|---|
| 1 | &lt;...&gt; | &lt;name&gt; | 🟢 🟡 🔴 | &lt;...&gt; | YYYY-MM-DD |

**Open Yellows** *(per `00_README/_frameworks/traffic-light-decisions.md` — each has a trigger + expiry):*

- &lt;Yellow from week N — owner — trigger — expiry&gt;

**Decisions this week** *(link existing rationale or a §B record when one was needed):*

| Decision | Light | Owner | Evidence / record |
|---|---|---|---|
| &lt;...&gt; | 🟢 🟡 🔴 | &lt;name&gt; | &lt;link&gt; |

**Asks** *(concrete, named, deadlined):*

- &lt;ask&gt; — from &lt;stakeholder&gt; — by &lt;date&gt;

---

## Quality checks

### §A Meeting capture

- [ ] Key points are ≤5 bullets
- [ ] Every decision has an owner and a Traffic Light
- [ ] Action items have owners and due dates

### §B Decision record

- [ ] Existing rationale was reused when sufficient; new records follow W5's type choice
- [ ] The selected type's required rationale, evidence, and review/rollback fields are present
- [ ] Consultation is honestly solo, invited, or reviewed; no invented reviewers or dissent
- [ ] Stable ID and lifecycle are valid; a Traffic Light has its required fields when applicable
- [ ] A new/changed record passes `check_decision.py`; routine evidence needs no duplicate record

### §C Weekly status

- [ ] TL;DR passes the 10-second test
- [ ] Every Health row has a one-sentence reason with a number
- [ ] Shipped = deltas, not totals
- [ ] Every open Yellow has trigger + expiry
- [ ] Every retained decision links to sufficient rationale; a separate §B record is not mandatory
- [ ] Asks are concrete: named stakeholder + deadline
- [ ] No hedge language ("hoping to", "plan to try")

---

*Three cadences, one system. Meetings (§A) retain rationale, optional typed records (§B) preserve new
durable choices, and relevant outcomes surface in the status rollup (§C) when the hub reports. Action
items feed the existing task plan; routine work does not create a second decision backlog.*
