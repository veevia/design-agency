---
name: wizard-of-oz
title: Fake the backend with a human behind the curtain
description: Simulate AI, complex backend logic, or live data with a human operator — so the prototype tests the user experience of intelligent behaviour without building it. Use when the sprint's riskiest assumption requires testing AI, ML, or automated behaviour that isn't built yet, or when a feature depends on a backend that can't be connected to in the sprint timeline.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - When the sprint's riskiest assumption requires testing AI, ML, or automated behaviour that isn't built yet
  - When a feature depends on a backend that can't be connected to in the sprint timeline
  - When the prototype's core interaction involves a "smart" system response (urgency score, recommendation, auto-fill)
  - When testing conversational AI, voice interfaces, or any feature where the system "decides" something
  - When building the real behaviour is technically possible but too slow for a sprint prototype
applies-to: AI prototype testing, complex system simulation, voice/chat interface testing, backend-dependent features, assumption testing without full implementation
done_when:
  - The user-facing experience works while a human simulates the system
  - The seams are invisible to the test participant
  - It tests desirability/behaviour before real engineering
metadata:
  duration: "Build: 1–2h setup; Test: runs throughout Validate day"
  team-size: 1 Wizard (hidden operator) + Interviewer + participant
  sprint-phase: 5 Prototype
---

# Wizard of Oz Prototyping

**TL;DR:** A Wizard of Oz prototype looks real to the participant but has a human operator — "the Wizard" — controlling the responses behind the scenes. The participant interacts with what appears to be an intelligent or automated system; the Wizard listens and manually produces the "AI" response in real time. This technique lets the team test the user experience of a complex, intelligent feature — ranking, assignment suggestions, natural language response — without building the underlying system.

## When to use

- When the sprint's riskiest assumption requires testing AI, ML, or automated behaviour that isn't built yet
- When a feature depends on a backend that can't be connected to in the sprint timeline
- When the prototype's core interaction involves a "smart" system response (urgency score, recommendation, auto-fill)
- When testing conversational AI, voice interfaces, or any feature where the system "decides" something
- When building the real behaviour is technically possible but too slow for a sprint prototype

## The core technique

The participant performs a task in the prototype. At the moment where the "system" should respond intelligently:
1. The Interviewer stalls briefly ("just give it a moment to load")
2. The Wizard — watching via a screen share or through an observation window — manually injects the system's "response" (types the priority, updates the urgency score, fills in the specialist suggestion)
3. The participant sees what appears to be an automated response

The participant must never know the Wizard exists. Their honest reaction to the "AI's" response is the test data.

## Setup requirements

| Role | Position | Equipment |
|---|---|---|
| **Interviewer** | In the room/call with participant | Participant's screen visible; subtle signal to Wizard |
| **Wizard** | Remote or separate room | Access to the prototype backend or a shared editable prototype |
| **Participant** | Sees only the prototype UI | No knowledge of Wizard or observation team |

**Technical setups:**
- **Figma + screen share:** Wizard edits a shared Figma prototype in real time on a hidden layer; participant sees the result after a simulated "loading" delay
- **Spreadsheet / database backend:** Wizard edits a live data source the prototype reads from; prototype refreshes with "AI" output
- **Form-tool flow:** Wizard manually advances the participant to the correct branch based on their input
- **Slide deck:** Wizard controls a presentation on a screen the participant sees; pre-built slides simulate system responses

## What the Wizard controls

| Feature being simulated | What the Wizard does |
|---|---|
| AI urgency score | Updates the score value in the shared prototype when the participant opens a request |
| Specialist suggestion | Fills in the suggested specialist's name based on the request type shown |
| Priority result | Changes the request status from "unsorted" to the appropriate priority |
| Search results | Reveals pre-built results that match what the participant searches for |
| AI explanation ("why 72?") | Types a pre-written explanation that appears in the prototype's explanation panel |

## Wizard script preparation

Before Validate day, the Wizard prepares a response script for the most likely participant actions:

```markdown
## Wizard Script — Reasons-First Urgency Score · Request Triage Sprint

### Request: "Unit U-200 · fault E9 · out of service · Site C"
If participant opens this request:
- Urgency score: set to 78
- Suggested priority: "Outage — Urgent — Site C"
- Explanation: "Urgency 78, based on 3 matching records: phone line booking (high reliability), service-contract database (high reliability), inventory-system stock count (medium reliability). Priority matches 9 similar outage requests this winter."

### Request: "Unit U-115 · minor fault · still in service · Site B"
If participant opens this request:
- Urgency score: set to 45
- Suggested priority: "Minor fault — Unconfirmed — Routine"
- Explanation: "Urgency 45. 2 records found; the web form and the CRM disagree on the address. Check the booking to confirm."

### If participant clicks "Why this score?":
- Display explanation panel (pre-built in Figma layer 3)

### If participant clicks "Change priority":
- Display "Your priority change has been noted" modal (pre-built in Figma)
- Log nothing in real prototype — wizard notes this action in observation doc
```

## Debrief disclosure

After the session, the Interviewer may optionally disclose the Wizard to the participant:
> "I should let you know — the AI responses you saw were simulated by a team member during the session. We wanted to test how you'd react to that kind of intelligent behaviour before we build it. Your reactions were completely genuine and very helpful."

Disclosure is optional but builds participant trust if you plan to work with them again.

## Agent facilitation guide

When advising on Wizard of Oz prototype setup:
1. Identify the specific "intelligent" feature being tested — what does the system decide or generate?
2. Design the Wizard script: for each request/input the participant will encounter, what response does the Wizard inject?
3. Choose the technical setup: shared Figma layer, live data source, or manual response injection
4. Establish the Wizard ↔ Interviewer signal: how does the Interviewer indicate "participant just did X — respond now"?
5. Rehearse: run the Wizard + Interviewer through one full session before Day 5
6. Document what the Wizard will NOT simulate — scope the magic so the test is bounded

## Watch-outs

- **Lag destroying the illusion:** A 10-second delay breaks the participant's belief in the system. The Wizard must be fast and pre-prepared. Pre-build all likely response states before the session.
- **Wizard reacting to preference, not input:** If the Wizard is giving responses they think are "good" rather than responses that match the scenario, they're contaminating the test. Script responses in advance; Wizard follows the script.
- **Over-wizard-ing:** Simulating too much makes the prototype feel magical — and produces unrealistically positive reactions. Only Wizard the features being tested; everything else should be real prototype behaviour.
- **No debrief note:** Note in synthesis which participant reactions were to Wizard-simulated features — these are hypothetical test results, not observed production behaviour. Flag clearly in the Assumptions Board update.

## Connects to

- [Prototyping Principles](../prototyping-principles/SKILL.md) — Wizard of Oz is recommended when coded prototype would take too long
- [Storyboard](../storyboard/SKILL.md) — storyboard panels that involve "smart" system responses are Wizard candidates
- [Five-Act Interview](../five-act-interview/SKILL.md) — Interviewer plays a dual role: facilitating and signalling the Wizard
- [Assumptions Board](../assumptions-board/SKILL.md) — Wizard tests the critical assumptions about AI/automated behaviour
