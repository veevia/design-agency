---
name: prototype-review
title: Dry-run the prototype before user testing
description: Run an internal quality check of the assembled prototype before participants arrive — catching broken links, missing screens, pacing issues, and fidelity gaps that would corrupt test data. Use when at the end of Prototype day, after Stitching is complete, before any dry run of the Wizard of Oz setup, or when any significant change was made to the prototype after the Stitcher's first assembly.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - At the end of Prototype day, after Stitching is complete
  - Before any dry run of the Wizard of Oz setup
  - If any significant change was made to the prototype after the Stitcher's first assembly
  - Before the first interview on Validate day (final 10-minute sanity check)
applies-to: prototype quality gate, pre-test readiness check, broken link detection, pacing rehearsal, Wizard script rehearsal
done_when:
  - The prototype is walked end-to-end against the test script
  - Dead ends, gaps, and confusing states are fixed or noted
  - It’s confirmed ready for the five-act interview
metadata:
  duration: 30–45 min (end of Prototype day, after Stitching)
  team-size: Stitcher + 1 reviewer (ideally someone who didn't build the prototype)
  sprint-phase: 5 Prototype
---

# Prototype Review

**TL;DR:** A prototype review is the structured internal walkthrough the team runs after the prototype is assembled but before any participant sees it. One person plays the participant; another observes and catches errors. The goal is not design critique — the decision was made on Day 4. The goal is to catch the mechanical failures, missing states, and flow gaps that would force the Interviewer to improvise during a real test session, corrupting the results. A 30-minute review eliminates the category of failures that come from testing a broken prototype.

## When to use

- At the end of Prototype day, after Stitching is complete
- Before any dry run of the Wizard of Oz setup
- If any significant change was made to the prototype after the Stitcher's first assembly
- Before the first interview on Validate day (final 10-minute sanity check)

## Review checklist

### Flow integrity
- [ ] Every screen the participant is expected to navigate to is linked and reachable
- [ ] No dead ends: every primary path has a next state (even if it's a "back to home" screen)
- [ ] No accidental clickable areas that go nowhere
- [ ] The storyboard flow matches the prototype flow — same screens in the same order
- [ ] Any branching paths (e.g., participant says "change priority") lead somewhere — even if that somewhere is a "thank you for your input" placeholder

### Fidelity check
- [ ] No Lorem Ipsum or placeholder text on screens that will be shown to participants
- [ ] All data elements are realistic (request titles, urgency scores, assigned specialists)
- [ ] Icons are consistent across screens (not mixed from different icon sets)
- [ ] Critical elements are legible at the screen resolution participants will use

### Timing
- [ ] The review team walks through the full participant scenario at realistic pace
- [ ] Estimated session time: intro (5 min) + tasks (20–25 min) + debrief (10 min) ≤ 45 min total
- [ ] If session is estimated > 50 min, cut a task — not reduce time per task

### Wizard of Oz (if applicable)
- [ ] Wizard is at their station and has tested the signal mechanism with the Interviewer
- [ ] All Wizard script responses are prepared and tested (urgency scores updated, explanation panels pre-built)
- [ ] Wizard latency is acceptable: response appears within 2–3 seconds of participant action
- [ ] Signal between Interviewer and Wizard has been rehearsed (gesture, chat message, screen indicator)

### Device and environment
- [ ] Prototype works on the exact device and browser participants will use (don't review on desktop if testing on a tablet)
- [ ] Screen share / remote setup is tested if participants are remote
- [ ] Recording is set up (if the team will record sessions with consent)
- [ ] Observation room / remote observer channel is active and silent

## Review session format

**Run the scenario, not the screens:**

Don't navigate the prototype in "tour mode" — run it as a participant would, following the task script.

1. Stitcher or Facilitator reads the participant scenario aloud: "It's Tuesday morning. You've opened the request system and you see 38 requests waiting. Your task is to review the unconfirmed requests and assign the most urgent one."
2. The reviewer navigates as if they were a real participant — using only what the screen shows, not prior knowledge of the prototype
3. The observer notes every moment the reviewer pauses, hesitates, or has to break character
4. Each break in the scenario is a potential break in the test session — fix before Validate day

## Review output

```markdown
## Prototype Review Log — [Sprint Name] · [Date]

### Flow issues found
- Screen 3 (Request Detail — Unit U-200): "Change priority" button navigates to a dead screen. Fix: wire to confirmation modal (Stitcher — 10 min)
- Screen 5 (Assignment Confirmation): "Back to requests" button missing. Fix: add back-link (Stitcher — 5 min)

### Content issues found
- Screen 2 (Request Queue): urgency score column header says "[Score]" — not updated. Fix: Writer — 5 min
- Screen 4 (Assignment Form): assigned specialist says "Specialist Name" — not filled. Fix: Writer — 10 min

### Timing issue
- Full scenario took 55 min in review. Cut Task 3 (manual re-prioritisation) — teams agree it's not testing the critical assumption.

### Wizard rehearsal
- Wizard latency on urgency score update: ~4 seconds — too slow. Fix: pre-load all urgency score states before session starts.
- Interviewer + Wizard signal (chat message) tested: working.

### Ready status: 🟡 Yellow — 4 fixes required before Day 6
Expected fix time: 30 min
```

## What prototype review is NOT

- **Not a design critique.** If a reviewer says "I don't like the colour of the urgency score," the Facilitator notes it and moves on. Design decisions were made on Day 4 — they are not revisited during prototype review.
- **Not a stakeholder demo.** The prototype is incomplete by design — it tests one critical path, not the whole product. Showing it to stakeholders during prototype review risks generating requests to scope-expand before testing.
- **Not a participant rehearsal.** The reviewer should play the role of a critical but good-faith participant — they're looking for broken mechanics, not trying to sabotage the test.

## Watch-outs

- **Reviewing too quickly:** A rushed review finds obvious breaks but misses the ones that surface when a participant takes an unexpected path. Run it at the pace a real participant would — they're slower than the team.
- **Building team reviewing their own work:** The person who built a screen sees what they intended, not what they built. Have someone who was in a different role run the review.
- **Skipping the Wizard rehearsal:** Wizard failures destroy test sessions. A two-minute rehearsal eliminates the category of "Wizard wasn't ready" failures. Never skip.
- **Fixing during the review:** Note issues, finish the review, then fix them. Stopping to fix mid-review resets the observer's attention and causes second-order issues to be missed.

## Agent facilitation guide

When conducting a prototype review:
1. Walk through the storyboard — match each panel to a prototype screen; flag missing screens
2. Run the scenario end-to-end — note every navigation point that requires a link
3. Check all links: primary path, secondary paths, back navigation, error/edge states
4. Check content: no placeholders, no inconsistent data, no missing labels
5. Estimate session time against the Five-Act Interview structure (45 min total)
6. Output a review log: flow issues, content issues, timing, Wizard rehearsal status, and a ready status using the Traffic Light

## Connects to

- [Stitching](../stitching/SKILL.md) — prototype review runs after Stitching is complete
- [Wizard of Oz](../wizard-of-oz/SKILL.md) — Wizard rehearsal is part of prototype review
- [Dividing Roles](../dividing-roles/SKILL.md) — Stitcher owns prototype review logistics
- [Five-Act Interview](../five-act-interview/SKILL.md) — the review validates the prototype against the interview structure
- [Assumptions Board](../assumptions-board/SKILL.md) — the prototype must reach every assumption being tested; review confirms coverage
