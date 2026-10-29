---
name: ecosystem-map
title: Map the actors, tools, and data flows in a system
description: Map the full ecosystem of actors, systems, and relationships surrounding the user — to understand the broader context the solution must fit into. Use when the sprint topic touches multiple integrated systems or data sources, when the team suspects hidden technical constraints that will affect design decisions, or before writing Constraint Mapping.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - When the sprint topic touches multiple integrated systems or data sources
  - When the team suspects hidden technical constraints that will affect design decisions
  - Before writing Constraint Mapping — the Ecosystem Map surfaces the constraints
  - When different team members have different mental models of "how the system works"
  - In B2B / enterprise sprints where the user operates inside a multi-system environment
applies-to: system thinking, service design, integration discovery, constraint identification, scope definition
done_when:
  - All key actors, tools, and data flows are on the map
  - Relationships and dependencies between nodes are drawn, not just listed
  - Gaps, bottlenecks, or unknowns are flagged for follow-up
metadata:
  duration: 30–45 min
  team-size: Full sprint team
  sprint-phase: 1 Understand
---

# Ecosystem Map

**TL;DR:** An Ecosystem Map (also called a System Map or Context Map) shows the full landscape of people, tools, data sources, and external systems that interact with the primary user's workflow. Where the Stakeholder Map focuses on human actors and their interests, the Ecosystem Map shows the technical and service infrastructure — what connects to what, what data flows where, what systems the user touches even indirectly. It prevents the sprint from designing a solution that ignores critical dependencies.

## When to use

- When the sprint topic touches multiple integrated systems or data sources
- When the team suspects hidden technical constraints that will affect design decisions
- Before writing Constraint Mapping — the Ecosystem Map surfaces the constraints
- When different team members have different mental models of "how the system works"
- In B2B / enterprise sprints where the user operates inside a multi-system environment

## The map structure

Three layers:

| Layer | What goes here | Examples |
|---|---|---|
| **User layer** | Primary user + immediate tools they directly interact with | The Lead Coordinator, the booking inbox, their personal spreadsheet |
| **Integration layer** | APIs, data feeds, and systems that those tools connect to | Booking inbox API, partner channel feed, inventory system, specialist calendar |
| **External layer** | Data sources, third parties, regulators — things outside organisational control | Partner channel (a booking source), parts suppliers, equipment manufacturers' recall notices |

Connections show: data flows, human interactions, and system calls — with direction (→ data source to tool; ← user action to system).

## Steps

1. **Post the primary user at the centre (1 min)**

2. **Map the tools the user directly uses (5 min):** What software, documents, or tools does the user touch in this workflow? Post as nodes around the user.

3. **Map the connections from those tools (10 min):** What does each tool connect to? What data does it pull from or push to? Add integration-layer nodes and draw arrows.

4. **Add external layer (5 min):** What's outside the organisation? Third-party data providers, regulatory systems, partner organisations?

5. **Annotate the constraints (5 min):** For each connection: is it a live integration or a manual step? What's the latency? What's restricted? Add annotations where there are known constraints.

6. **Identify the gaps (5 min):** Where is data that should flow, not flowing? Where are manual handoffs that could be automated? Where does the user leave the ecosystem (go external)?

## Worked example (generic)

```markdown
## Ecosystem Map — the Lead Coordinator's morning triage workflow

### User layer
Lead Coordinator
├── Booking inbox (web form, phone line, and partner channel requests)
├── Personal tracking spreadsheet
├── Phone and chat — used as an assignment workaround
└── Specialist calendar (legacy) — used for formal assignment

### Integration layer
Booking inbox
├── → Web form submissions (customer-entered free text)
├── → Partner channel feed (partner terms apply)
├── → AI ranking API (backend only; not surfaced in UI) ⚠️
├── → Specialist calendar (assignment via 7-step form) ⚠️
└── ← Notification engine (alerts the coordinator on requests flagged urgent)

Specialist calendar
├── → Specialist skills and certification database
├── → Request history log (required — every priority decision must be logged)
└── → Site rota tables (Site A, Site B, Site C)

CRM · service-contract database · inventory system · billing
└── ← Checked by hand, one system at a time ⚠️

### External layer
- Partner channel — a booking source (partner terms: channel must be shown; customer details restricted)
- Parts suppliers — restock the inventory system overnight (stock counts can lag by a day)
- Equipment manufacturers — publish recall notices (e.g., a recalled replacement part for Unit U-200)
- Customers — book, reschedule, and chase their requests by phone, web form, and partner channel

### Constraints from map
⚠️ AI ranking API is internal but not exposed in the UI — requires API team involvement to surface
⚠️ Specialist calendar is legacy — new UI must write through existing API, cannot bypass
⚠️ Bookings from a partner channel must show the booking channel in any display
⚠️ Request history log must record coordinator identity + timestamp for every priority decision
⚠️ Site rota tables are maintained by IT — any assignment logic must use existing table structure

### Gaps identified
- Customer, service-contract, and inventory data live in separate systems (customer IDs disagree across 3 of 6) — none of it is visible in the booking inbox
- No cross-site visibility — the coordinator cannot see whether Site B already has a specialist near a Site C request
- Manual spreadsheet is a shadow system — no integration; represents a data reliability risk
```

## Ecosystem Map vs. User Journey Map

| | Ecosystem Map | User Journey Map |
|---|---|---|
| Focus | Systems, data, and technical architecture | Human experience, emotions, and steps |
| Who is central | The system | The user |
| Primary output | Integration constraints and data flows | Emotional arc and pain points |
| Sprint use | Constrains solution design | Generates HMW notes |
| Use together | Yes — Journey Map for human layer; Ecosystem Map for technical layer |

## Agent facilitation guide

When generating an Ecosystem Map from sprint research:
1. Identify the primary user and their immediate tool set (things they touch every session)
2. For each tool: identify what external systems or data sources it connects to (pull from engineering talks)
3. For each connection: note direction, data type, latency, and any known constraints
4. Add the external layer: third-party data providers, regulators, partner organisations
5. Highlight constraints with ⚠️ markers — these feed directly into Constraint Mapping
6. Identify gaps: where manual steps exist that the ecosystem could theoretically automate

## Watch-outs

- **Making it too detailed too early:** The first Ecosystem Map is a sketch, not a system architecture diagram. Start with the main nodes; add detail only where it surfaces constraints.
- **Only the tech team contributes:** Business users, customer success reps, and the Decider know about integration constraints that engineers don't. Include everyone in the mapping step.
- **Missing shadow systems:** Users almost always have personal spreadsheets, email chains, or messaging threads that aren't in the "official" system. These are critical to map — they represent workarounds that any new solution must compete with.
- **Treating the map as a technical spec:** The Ecosystem Map is for strategic awareness, not implementation design. It tells the team what to design around; it doesn't prescribe how to build.

## Connects to

- [Stakeholder Map](../stakeholder-map/SKILL.md) — human actors in the ecosystem; complements the system view
- [Competitive Landscape](../competitive-landscape/SKILL.md) — external systems include analogous products
- [Constraint Mapping](../constraint-mapping/SKILL.md) — ⚠️ annotated constraints from the map become the formal constraint list
- [Assumption Mapping](../assumption-mapping/SKILL.md) — unknown integration behaviours become assumptions
- [Wizard of Oz](../wizard-of-oz/SKILL.md) — gaps in the ecosystem are where Wizard of Oz prototyping is most useful
