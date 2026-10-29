---
name: storyboard
title: Script the prototype scene-by-scene
description: Translate the winning Solution Sketch into a scene-by-scene prototype script — 10–15 panels, each with a clear purpose and realistic content. Use first thing on Prototype day, after team roles are assigned. Use when translating the Supervote winning concept into buildable screen definitions, or to ensure every Assumptions Board item has a corresponding screen.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - First thing on Prototype day, after team roles are assigned
  - To translate the Supervote winning concept into buildable screen definitions
  - To ensure every Assumptions Board item has a corresponding screen
  - When the team needs to divide build work across multiple Makers
applies-to: prototype planning, screen mapping, content scripting, build sequencing, assumption coverage verification
done_when:
  - A 10–15 panel scene-by-scene script from the winning sketch exists
  - Each panel names the screen/state and the user action
  - The storyboard is detailed enough to build the prototype from
metadata:
  duration: 60–90 min
  team-size: Full sprint team (Facilitator + Makers)
  sprint-phase: 5 Prototype
  redirect-host: whiteboard-storyboard
---

# Storyboard

**TL;DR:** The storyboard is the script for the prototype. It converts the winning Solution Sketch — a single annotated panel — into a scene-by-scene plan that the Makers can execute. Every screen, every click path, every piece of content is decided here, collaboratively, before anyone opens a design tool. Decisions made in the storyboard prevent scope debates during the build.

## When to use

- First thing on Prototype day, after team roles are assigned
- To translate the Supervote winning concept into buildable screen definitions
- To ensure every Assumptions Board item has a corresponding screen
- When the team needs to divide build work across multiple Makers

## Materials

- Whiteboard or large sticky notes
- The winning Solution Sketch (posted on the wall)
- The Assumptions Board (critical assumptions visible throughout)
- A timer (90 min max for the full storyboard)

## Panel types

A storyboard is a sequence of panels. Each panel represents one screen or one interaction state.

| Panel type | Purpose | Example |
|---|---|---|
| **Entry point** | Where does the user begin? What brings them here? | Email notification → opens the tool |
| **Setup screen** | Context that makes the key moment make sense | Request queue with unconfirmed bookings shown |
| **Key moment** | The interaction that tests the critical assumption | User reads urgency score; decides whether to act |
| **Response / feedback** | What the product shows after the key action | Priority saved; request moves to reviewed queue |
| **Secondary path** | Alternative route (only include if it's on the Assumptions Board) | User opens the records list instead of acting immediately |
| **Outcome** | End state — what has the user accomplished? | Work order card shows the confirmed request attached |
| **Error state** | Only include if error recovery is a sprint assumption | Assignment fails — what now? |

## Steps

1. **Read the winning sketch aloud (5 min):** Facilitator reads the Solution Sketch annotations. Team confirms they understand what the Decider chose and why.

2. **Identify the entry point (5 min):** "Where does the user start?" Define the realistic context — not a blank home screen. A specific email, a specific notification, a specific task in their day.

3. **Walk the critical path (30 min):** Starting from the entry point, walk through what the user sees, does, and needs to see next. Draw each step as a rough rectangle on the whiteboard. Name it.
   - Aim for 10–12 panels minimum (fewer is usually too sparse to test assumptions)
   - Maximum 15 panels — more than that and build day runs out of time

4. **Check against the Assumptions Board (10 min):** For each critical assumption, identify which panel tests it. If an assumption doesn't map to any panel, either add a panel or move the assumption to "out of sprint scope."

5. **Write content notes per panel (20 min):** For each panel, note:
   - The screen name (what the Maker will call this file in Figma)
   - The content needed (real names, realistic numbers, specific copy)
   - Any interactions (what happens on click/tap)
   - The assumption it's testing (or "navigation only")

6. **Sequence and handoff (10 min):** Number the panels. Assign each to a Maker. The Stitcher notes the click-through connections between panels.

## Storyboard output format

```markdown
## Storyboard — [Sprint Name] · [Date]

**Entry scenario:** The coordinator receives a request-system notification: "3 new unconfirmed requests in the overnight queue"

| Panel | Screen name | Content notes | Interaction | Tests assumption |
|---|---|---|---|---|
| 01 | Email notification | From: Request system · Subject: "3 unconfirmed requests need review" | Click "Review requests" | Entry point — none |
| 02 | Request queue | Shows 12 Site C requests; 3 flagged Unconfirmed in yellow; urgency scores visible | Scroll to first Unconfirmed | Urgency score visible at queue level |
| 03 | Request detail | Request: "Unit U-200 · fault E9 · out of service · Urgency: 78 · Records: 3" | Read score + records | Users interpret the urgency score correctly |
| 04 | Records list (inline) | Three record cards: CRM, service-contract database, inventory system · Each: summary + date | Tap record card | Inline records reduce system-switching |
| 05 | Priority panel | "Set priority for this request" · Options: Urgent / Routine / Escalate | Tap "Urgent" | Suggested priority acted on without checking |
| 06 | Confirmation | Request moves to Confirmed; counter updates: "2 remaining" | Auto-advance | Feedback state — tests flow completion |
| 07 | Queue updated | Previously unconfirmed request now shows Confirmed badge | Continue reviewing | Navigation only |
| 08 | Assign to specialist | "Assign" appears as secondary CTA after confirmation | Tap "Assign" | One-tap assign eliminates 3-step manual flow |
| 09 | Work order card | Request attached to Work Order #4471 · specialist pre-populated (Site C) | Confirm or change specialist | Specialist is correctly pre-selected |
| 10 | Completion | Queue shows 0 unconfirmed; "All caught up" state | End task | End state — none |

**Assumption coverage check:**
- ✅ Users interpret the urgency score correctly → Panel 03
- ✅ Inline records reduce system-switching → Panel 04
- ✅ Suggested priority acted on → Panel 05
- ✅ One-tap assign → Panel 08
```

## Simplification principles

- **One key moment per panel.** A panel trying to test two assumptions usually tests neither.
- **No hypothetical paths.** If it's not in the storyboard, it doesn't get built. Resist adding "what if they want to X" — that's a future sprint question.
- **Prototype flows forward.** The participant should be able to complete the test task by clicking forward. Dead ends are acceptable at the end of a flow; they are not acceptable mid-task.
- **Real content, typed in now.** Don't leave "TBD" in the content notes. Decide the realistic scenario now. Makers who have to invent content during build will invent inconsistent content.

## Agent facilitation guide

When generating a storyboard from a winning Solution Sketch and Assumptions Board:
1. Read the Solution Sketch — note the entry point the sketch implies
2. Read the Assumptions Board — list the critical assumptions in order
3. Walk the minimum path that covers all critical assumptions, in realistic sequence
4. Generate the storyboard table with specific content notes
5. Run the assumption coverage check — flag any unmet assumption
6. Estimate panel count and flag if > 15 (may need to cut secondary paths)

## Watch-outs

- **Starting with screens instead of story:** The storyboard should describe the *user's experience*, not the screens the designer wants to build. Start from "what is the coordinator doing right before this?" not "what screens do we need?"
- **Storyboard growing past 15 panels:** Every panel added is 30–60 minutes of build time. If the storyboard exceeds 15, cut secondary paths first, then defer non-critical assumption tests to a follow-up sprint.
- **No content notes:** Vague content ("some requests") leads to inconsistent prototype content. Specific content ("3 requests; Unit U-200 outage, a safety-risk report, a replacement-part delay") leads to a realistic test session.
- **Forgetting the entry point:** Prototype tests often fail because the scenario isn't believable. A strong entry point (realistic notification, realistic trigger) puts participants in the coordinator's shoes before the first task begins.

## Connects to

- [Supervote](../supervote/SKILL.md) — winning concept is the input to this storyboard
- [Assumptions Board](../assumptions-board/SKILL.md) — critical assumptions must map to specific panels
- [Dividing Roles](../dividing-roles/SKILL.md) — panels are divided among Makers using this storyboard
- [Prototyping Principles](../prototyping-principles/SKILL.md) — fidelity guidance applies per panel
- [Five-Act Interview](../five-act-interview/SKILL.md) — interview tasks are designed around the critical panels
