---
name: stitching
title: Stitch screens into one connected flow
description: Assemble individual prototype components — screens, interactions, transitions, and data — into a single navigable prototype the participant experiences as one coherent product. Use after Makers complete their screen components on Prototype day. Use when multiple people have built separate prototype sections that need to be combined, or after any mid-day pivot that changes the flow structure.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - After Makers complete their screen components on Prototype day
  - Whenever multiple people have built separate prototype sections that need to be combined
  - After any mid-day pivot that changes the flow structure
  - As preparation for the Prototype Review — stitching must be complete before the review can run
applies-to: Figma click-through assembly, interaction wiring, prototype flow sequencing, multi-maker output integration, navigation linking
done_when:
  - Individual screens are linked into one coherent walkthrough
  - Transitions and states are consistent end-to-end
  - The stitched flow matches the test script’s path
metadata:
  duration: 1–2 h (afternoon of Prototype day, after Makers complete screens)
  team-size: 1 Stitcher; receives components from all Makers
  sprint-phase: 5 Prototype
---

# Stitching

**TL;DR:** Stitching is the act of connecting independently built prototype components into a single, navigable flow. On Prototype day, multiple Makers build screens simultaneously — each owns a section of the storyboard. Stitching is what turns those disconnected screens into a prototype the participant can actually use. The Stitcher does not redesign or redesign. They wire: every tap leads somewhere, every screen connects to the next, the flow matches the storyboard order, and the whole thing can be navigated from start to finish without a team member hovering to explain what's supposed to happen.

## When to use

- After Makers complete their screen components on Prototype day
- Whenever multiple people have built separate prototype sections that need to be combined
- After any mid-day pivot that changes the flow structure
- As preparation for the Prototype Review — stitching must be complete before the review can run

## What the Stitcher does

| Task | Description |
|---|---|
| **Collect components** | Gather all Maker frames into one Figma page / prototype view |
| **Order the flow** | Sequence screens to match the storyboard panel order |
| **Wire interactions** | Connect every navigable element: buttons, links, tabs, back arrows, CTAs |
| **Add transitions** | Set consistent transition style (Dissolve or Smart Animate for sprint; no per-screen custom animations) |
| **Fill gaps** | If a Maker's section ends on a dead screen, add a placeholder screen or back-navigation to prevent a dead end |
| **Remove duplicates** | Makers often build the same navigation bar or header — merge into a shared component |
| **Test the flow** | Walk through the prototype once before handing off to Prototype Review |

## Stitching in Figma — step by step

**1. Collect all Maker frames onto one page:**
- Ask Makers to move completed screens to a shared "Prototype" page
- Or Stitcher copies frames from each Maker's working page into the Prototype page
- Name each frame clearly: `01_RequestQueue`, `02_RequestDetail_UnitU200`, `03_AssignmentForm`, `04_AssignmentConfirmation`

**2. Order frames left-to-right in storyboard sequence:**
- Left-to-right ordering matters — Figma uses left-to-right frame order as the default prototype start
- Align all frames to the same Y position, spaced consistently (e.g., 200px gaps)

**3. Wire the primary path first:**
- Connect the first CTA on each screen to the next screen in the storyboard order
- Use "On tap → Navigate to" for simple forward navigation
- Use "On tap → Overlay" for modals, tooltips, confirmation dialogs

**4. Wire secondary paths:**
- Back navigation: every screen should have a back arrow or close button wired to the previous screen
- Secondary CTAs: "Change priority," "Cancel assignment," "View record detail"
- Tab navigation: if the prototype has tabs, wire each tab to its corresponding screen

**5. Add transitions:**
- Sprint standard: **Dissolve, 200ms** for all transitions — fast, neutral, doesn't obscure the UI being tested
- Exception: use **Push Left/Right** only if the concept being tested includes navigation direction as a hypothesis
- Never use complex animations that weren't in the storyboard — they add production time and create new hypotheses you weren't testing

**6. Test the prototype flow:**
- Use Figma's Present mode (full-screen, no edit UI)
- Walk through the full scenario once — tap every interactive element; confirm nothing dead-ends

## Stitching issues and fixes

| Issue | Symptom | Fix |
|---|---|---|
| **Maker frames at different scales** | Screens look different sizes | Select all, enforce same W/H; or set consistent device frame |
| **Different font weights across sections** | Body text looks inconsistent between screens | Standardise on one text style; use Figma's "Replace matching fonts" if needed |
| **Missing back navigation** | Participant clicks forward and can't return | Add back arrow frame + wire to previous screen (5 min per screen) |
| **Inconsistent spacing on nav bars** | Navigation bar looks different per screen | Copy one canonical nav bar frame across all screens |
| **Overlapping interaction zones** | Two elements respond to the same tap area | Check Figma layer order; ensure only the intended interactive layer is on top |
| **Prototype starting on wrong screen** | Figma starts on the wrong frame | Set "Starting Frame" explicitly in Prototype Settings |

## Stitching output

A stitched prototype has:
- One starting frame (named `00_Start` or `00_ScenarioCard`)
- All primary-path screens navigable from start to end
- All secondary-path CTAs wired to at least one response state
- No dead ends on any visible interactive element
- Consistent transition type and duration across all connections
- A share link that works on the participant's device/browser

## Watch-outs

- **Stitching too early:** If Makers aren't done when the Stitcher starts, they'll be pulling frames that are still being modified. Set a hard "Makers deliver screens by [time]" deadline and start stitching only after.
- **Stitcher redesigning:** If the Stitcher notices a UI inconsistency and starts redesigning screens, they'll block the prototype flow for everyone. Note the inconsistency; wire it anyway; report to the Facilitator. Do not redesign.
- **Too many prototype paths:** The sprint prototype tests one scenario. If the Stitcher is wiring 20+ interactions across 15 screens, the prototype is too large. Check against the storyboard — only screens that appear in the storyboard need full wiring.
- **Forgetting the starting screen:** The scenario card ("It's Tuesday morning. You are the Lead Coordinator...") is the first screen. Participants need context before they navigate. Make sure it's wired as the starting frame.
- **Non-working share link:** Always test the Figma share link on the actual device before Day 6. Share links that require Figma login, or don't work on mobile Safari, are discovered during the first participant session if not tested in advance.

## Agent facilitation guide

When advising on prototype stitching:
1. Read the storyboard — list all screens in order; this is the frame naming and sequencing guide
2. Identify the primary path: the single most important flow that tests the critical assumption
3. Identify secondary paths: edge states, error states, back navigation, and branching CTAs
4. Define the Stitcher's handoff criteria: what does "complete" look like from each Maker?
5. Specify the transition standard: Dissolve 200ms unless the team has a specific reason for directional navigation
6. Output a stitching checklist: one row per screen, columns for "frame exists," "forward wired," "back wired," "secondary CTAs wired"

## Connects to

- [Dividing Roles](../dividing-roles/SKILL.md) — Stitcher is a named Prototype day role; this file describes their full output
- [Storyboard](../storyboard/SKILL.md) — storyboard panel order is the stitching sequence
- [Prototype Review](../prototype-review/SKILL.md) — stitching must be complete before prototype review can run
- [Prototyping Principles](../prototyping-principles/SKILL.md) — "build only what tests the assumption" constrains the stitching scope
- [Five-Act Interview](../five-act-interview/SKILL.md) — the stitched prototype is the artifact the Interviewer uses in Act 4 (task-based testing)
