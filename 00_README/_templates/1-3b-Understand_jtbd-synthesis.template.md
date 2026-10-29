---
title: "JTBD Synthesis — <project>"
type: template
template-for: jtbd-synthesis
status: canonical
owner: OS steward
last-updated: 2026-10-29
loop-phase: understand
source: Multi-domain JTBD synthesis practice
tags: [type/template, type/jtbd, purpose/decide, loop/understand, status/canonical]
---

# JTBD Synthesis — `[Project Name]`

> **TL;DR (10 seconds):** `[One sentence: what program scope was analysed, how many JTBDs, what workstreams were selected.]`

---

## 1. Domain inventory

_List every JTBD analysis completed. One row per persona / domain._

| # | Domain | Persona | JTBD file | Opportunity canvases | Evidence quality |
|---|---|---|---|---|---|
| 1 | `[domain]` | `[persona name / role]` | `[filename]` | `[count]` | `observed` / `reported` / `assumed` |
| 2 | | | | | |

**Total:** `[N]` domains · `[N]` JTBD files · `[N]` opportunity canvases

---

## 2. Opportunity cluster map

_Group opportunity canvases across domains by theme. A cluster = the same capability need appearing in ≥2 domains._

| Cluster | Description | Domains where it appears | Canvas count |
|---|---|---|---|
| `[cluster name]` | `[what the shared need is]` | `[domain A, domain B, ...]` | `[N]` |

**How to read:** Each row is a candidate workstream. Frequency = how many domains share it. Use this table to spot cross-domain leverage.

---

## 3. Cross-domain ranking

_Score each cluster. Rank to decide what advances to Design._

| Rank | Cluster | Frequency (domains) | Impact score¹ | Confidence² | Notes |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |

¹ Impact score: 1–5 (1 = low, 5 = high business impact based on stakeholder signals)  
² Confidence: `observed` / `reported` / `assumed`

---

## 4. Workstream selection

_For each candidate cluster, record one Traffic Light here on whether it advances to Design. This table is the rationale; a separate typed record is needed only when W5's criteria apply._

| Workstream | Cluster(s) | Decision | Light | Owner | Rationale |
|---|---|---|---|---|---|
| `[workstream name]` | `[cluster(s)]` | Advance to Design | 🟢 / 🟡 / 🔴 | `[name]` | `[one sentence]` |

**🟡 Yellow conditions:** List any named dependency that must resolve before the workstream advances (e.g., "Yellow until design partner confirmed by [date]").

**Deferred workstreams:** List domains / clusters not advancing and why (capacity, no design partner, lower priority). These remain in scope for future loops — do not delete JTBD files.

---

## 5. Consolidated HMW statements

_One "How Might We" per selected workstream. Each must trace back to ≥1 JTBD canvas._

| Workstream | HMW | Source JTBD(s) | Confidence |
|---|---|---|---|
| `[workstream]` | How might we `[verb]` for `[persona]` so they can `[outcome]`? | `[file(s)]` | `reported` |

---

## 6. Design phase hand-off

_Map each selected workstream to its Design phase sub-hub folder._

| Workstream | Folder to create | Canonical artifacts needed |
|---|---|---|
| `[workstream]` | `02_design/[NN]-[workstream-name]-design/` | Design POV · Design Brief · PRD · phase-gate evidence |

---

## Quality check

Before filing this synthesis as complete:

- [ ] Every domain from the JTBD inventory appears in the cluster map (none silently dropped)
- [ ] Every selected workstream has a 🟢 or 🟡 Traffic Light with owner named
- [ ] Every deferred workstream has a stated reason
- [ ] Each HMW traces to at least one JTBD canvas by filename
- [ ] Understand → Design gate evidence in the existing artifact or phase block references this synthesis

Phase closure alone needs no new decision file. Use W5 (`02_Workflows/workflows/W5-decide.md`)
only for a new durable choice, explicit capture request, or lifecycle change.

---

## Who reviews what

| Role | Focus |
|---|---|
| Design lead | Cluster accuracy, workstream selection rationale |
| PM / Product owner | Priority ranking, business impact scores |
| Engineering lead | Feasibility notes on high-ranked clusters |
| Research partner | Evidence quality, confidence levels |
