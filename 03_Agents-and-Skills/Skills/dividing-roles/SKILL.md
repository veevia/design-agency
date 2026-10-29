---
name: dividing-roles
title: Assign prototype build roles to the team
description: Assign prototype build roles before the day starts — Makers, Stitcher, Writer, Asset Collector, and Interviewer each have a clear lane with no overlap. Use after the storyboard is complete, at the start of build day. Use when a sprint team has 4+ members and needs to parallelize build work, or whenever the prototype has both visual screens and connecting copy/content to write.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Immediately after the storyboard is complete, at the start of build day
  - When a sprint team has 4+ members and needs to parallelize build work
  - Whenever the prototype has both visual screens and connecting copy/content to write
  - When one person needs to begin interview preparation while others build
applies-to: build day planning, parallel workstreams, prototype assembly, role clarity, interviewer preparation
done_when:
  - Each prototype workstream has a named owner
  - Roles (maker, writer, stitcher, asset-collector) are covered
  - Hand-offs and the stitch point are agreed
metadata:
  duration: 10 min (role assignment)
  team-size: Full sprint team
  sprint-phase: 5 Prototype
---

# Dividing Roles

**TL;DR:** Prototype day fails when everyone builds together. Five people debating a button label at 11am means the prototype isn't done by 3pm. Dividing roles turns a chaotic group build into a parallel production line. Each role has a clear output, a clear owner, and minimal handoff friction.

## When to use

- Immediately after the storyboard is complete, at the start of build day
- When a sprint team has 4+ members and needs to parallelize build work
- Whenever the prototype has both visual screens and connecting copy/content to write
- When one person needs to begin interview preparation while others build

## The five roles

### 1. Makers (2–3 people)
**Build the screens.**

Makers work from the storyboard. Each Maker owns a set of panels — they design and produce those screens at sprint fidelity (not production fidelity). Makers do not make scope decisions; if something isn't in the storyboard, they flag it to the Facilitator rather than inventing it.

- Work in parallel on assigned panels
- Use existing design system components where available (the design-system component kit, Figma team library)
- Flag storyboard ambiguities immediately — do not guess
- Do not polish. Sprint fidelity means "clear enough to test," not "ready for a portfolio showcase."

**Output:** All storyboard panels built in the prototype tool, handed to Stitcher by the agreed checkpoint time.

### 2. Stitcher (1 person)
**Assemble the panels into a working click-through prototype.**

The Stitcher receives completed panels from Makers and connects them with prototype interactions (links, overlays, transitions). The Stitcher also enforces consistency — if two Makers have used slightly different font sizes or button styles, the Stitcher normalises them.

- Sets up the master prototype file before Makers start (frame sizes, library, naming convention)
- Defines the click path logic from the storyboard
- Assembles panels as Makers complete them — does not wait for all panels before starting
- Runs the click-through before the test session to verify every interaction works

**Output:** A working click-through prototype, tested end-to-end, with consistent styling.

### 3. Writer (1 person)
**Write all copy, labels, microcopy, and placeholder content.**

Poor content kills prototype tests. "Lorem ipsum" and "Button text" break the participant's suspension of disbelief. The Writer is responsible for all words inside the prototype — not just headlines, but signal names, source labels, notification copy, confirmation messages, error text, and navigation labels.

The Writer works from the content notes in the storyboard. If the storyboard notes are thin, the Writer is the person who invents realistic, internally consistent content — not the Makers.

- Creates a content doc with all strings before panels are built (so Makers can build with real content)
- Coordinates with Makers on panel-by-panel copy needs
- Produces the interview script section for each test task (working alongside the Interviewer)

**Output:** All prototype copy finalized and handed to Makers; test task scripts drafted.

### 4. Asset Collector (1 person — may overlap with Maker)
**Source and prepare all non-design assets: logos, icons, images, data, screenshots.**

Many sprint prototypes include UI elements that aren't built from scratch — a company logo, a screenshot of an existing tool for context, an icon set. The Asset Collector handles all of this so Makers can focus on screen design.

- Collects icon assets from the agreed icon set (do not invent new icons mid-day)
- Sources realistic data: names, numbers, dates, company names
- Prepares any screenshots of existing tools used as reference in the prototype
- Ensures all assets are in the shared prototype file before the Stitcher assembles

**Output:** All prototype assets available in the shared file before Stitcher assembly begins.

### 5. Interviewer (1 person — typically the Facilitator or a designated team member)
**Prepare for the test sessions; do not build the prototype.**

The Interviewer's job on prototype day is not to build — it's to prepare. This means writing the interview guide, rehearsing the five-act structure, and coordinating participant logistics. An Interviewer who spent prototype day building will run a weak test on validate day.

- Writes the interview guide using the five-act structure (see [Five-Act Interview](../five-act-interview/SKILL.md))
- Maps each test task to a specific storyboard panel and a specific Assumptions Board item
- Defines success signals for each task ("we'll know this assumption is valid when...")
- Coordinates participant scheduling: confirmed names, arrival times, consent forms
- Runs a dry-run of the prototype click-through at end of build day

**Output:** Complete interview guide; participant logistics confirmed; dry-run completed.

## Role assignment table

```markdown
## Prototype Day — Role Assignments · [Sprint Name] · [Date]

| Role | Assigned to | Panels / Responsibility |
|---|---|---|
| Maker 1 | [Name] | Panels 01–04 (Entry → Signal detail) |
| Maker 2 | [Name] | Panels 05–07 (Classification → Feed update) |
| Maker 3 | [Name] | Panels 08–10 (Routing → Completion) |
| Stitcher | [Name] | Prototype assembly; consistency; end-to-end click test |
| Writer | [Name] | All copy; storyboard content notes → real strings; task scripts |
| Asset Collector | [Name] | Icons, logos, realistic data; asset prep in shared file |
| Interviewer | [Name] | Interview guide; participant logistics; dry-run |

**Build checkpoint:** 2pm — all panels delivered to Stitcher
**Assembly checkpoint:** 4pm — full prototype click-through complete
**Dry-run:** 4:30pm — Interviewer runs through prototype with Stitcher as stand-in participant
```

## Timing guide for a 6-hour build day

| Time | Milestone |
|---|---|
| 9:00 | Storyboard review + role assignment |
| 9:15 | Stitcher sets up master file; Asset Collector starts sourcing |
| 9:30 | Makers start building panels; Writer starts content doc |
| 12:00 | Lunch — informal checkpoint: are all panels on track? |
| 14:00 | Hard checkpoint: all panels delivered to Stitcher |
| 14:00–16:00 | Stitcher assembles; Makers fix flagged issues; Interviewer finalises guide |
| 16:00 | Prototype click-through complete |
| 16:30 | Dry-run with Interviewer |
| 17:00 | Build day done; team confirms validate logistics |

## Agent facilitation guide

When generating role assignments for a prototype day:
1. Count the storyboard panels — divide across available Makers (aim for 3–5 panels per Maker)
2. Identify the person most likely to be the Interviewer — typically the researcher or facilitator, not the lead designer
3. Identify whether an Asset Collector is a distinct role or can be folded into a Maker's scope
4. If fewer than 4 people: collapse Asset Collector into Maker; collapse Writer into Stitcher; note the risk of content quality dropping
5. Output the role assignment table + build day schedule

Minimal team (3 people):
```
Person A: Maker + Asset Collector — builds all screens, sources assets
Person B: Stitcher + Writer — assembles prototype, writes all copy
Person C: Interviewer — prepares guide, coordinates participants
```
Risk: single point of failure on both the prototype and the test guide. Flag this.

## Watch-outs

- **Everyone building together:** If no role is explicitly assigned, default groupthink kicks in. Five people looking at one screen, debating one button, means nothing gets built on time.
- **Interviewer becoming a Maker:** "I'll just help with a few screens and then switch to the guide." This always ends with a bad interview guide. The Interviewer's job on build day is interview prep.
- **Stitcher receiving panels too late:** If Makers deliver panels at 4pm, the Stitcher has 30 minutes to assemble. Set the 2pm checkpoint and enforce it.
- **Writer blocked by Makers:** The Writer needs content notes from the storyboard before Makers start. If content notes are thin, the Writer should interview each Maker for 5 minutes at the start of the day to get the content they need.
- **No dry-run:** Prototype bugs surface in dry-runs, not in the live session. A 30-minute dry-run at the end of build day catches broken links, missing states, and confusing transitions.

## Connects to

- [Prototyping Principles](../prototyping-principles/SKILL.md) — fidelity guidance applies to Makers
- [Storyboard](../storyboard/SKILL.md) — panel list drives Maker assignments
- [Five-Act Interview](../five-act-interview/SKILL.md) — Interviewer prepares this on build day
- [Assumptions Board](../assumptions-board/SKILL.md) — Interviewer maps tasks to critical assumptions
