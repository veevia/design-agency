---
name: video-prototype
title: Fake a feature with a video prototype
description: Record a narrated walkthrough of the prototype concept as a video — to communicate the experience, gather async reactions, or simulate a live demo for remote participants. Use when the sprint's key assumption involves how something *feels over time* (a loading sequence, an onboarding flow, an AI response animation), or when testing with remote participants who can't interact with a click-through prototype asynchronously.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - When the sprint's key assumption involves how something *feels over time* (a loading sequence, an onboarding flow, an AI response animation)
  - When testing with remote participants who can't interact with a click-through prototype asynchronously
  - When the team needs to share the sprint concept with senior stakeholders before Validate day and a static screenshot won't communicate it
  - When the concept involves a narrative or journey that is clearer in motion than in static screens
  - As a complement to the Wizard of Oz — record the Wizard-controlled interaction as a video for stakeholders who weren't in the test
applies-to: remote testing, async concept sharing, stakeholder communication, concept fidelity simulation, Wizard of Oz for narrative-driven flows
done_when:
  - A short video conveys the concept/experience convincingly
  - The illusion holds for the moment being tested
  - It’s ready to gauge desirability without a built product
metadata:
  duration: 1–2 h build (scripting + recording + light editing)
  team-size: 1–2 people (narrator + screen recorder)
  sprint-phase: 5 Prototype
---

# Video Prototype

**TL;DR:** A video prototype is a recorded walkthrough of the concept — narrated, click-through, or animated — that shows how the product would work in a real scenario. It is not a polished product demo. It is a fast-produced video that communicates the experience of the concept well enough to test key reactions or share the idea with stakeholders who weren't in the sprint room. Video prototypes are particularly useful when the interaction is temporal (animations, loading states, transitions) or when participants need to react to a narrative rather than explore freely.

## When to use

- When the sprint's key assumption involves how something *feels over time* (a loading sequence, an onboarding flow, an AI response animation)
- When testing with remote participants who can't interact with a click-through prototype asynchronously
- When the team needs to share the sprint concept with senior stakeholders before Validate day and a static screenshot won't communicate it
- When the concept involves a narrative or journey that is clearer in motion than in static screens
- As a complement to the Wizard of Oz — record the Wizard-controlled interaction as a video for stakeholders who weren't in the test

## Video prototype types

| Type | Description | Best for |
|---|---|---|
| **Narrated screen walkthrough** | Narrator talks over a click-through prototype, explaining the scenario | Stakeholder communication; async concept sharing |
| **Storyboard animation** | Animated version of the storyboard panels — sketches move and transition | Early-stage concept communication; team alignment |
| **Recorded Figma interaction** | Screen recording of a Figma click-through prototype in action | Showing transitions, gestures, navigation flow |
| **Live demo recording** | Recorded session of a real (or Wizard-controlled) prototype interaction | Capturing the "real feel" of a complex interaction |
| **Concept film** | Produced video showing the user in context using the product | High-fidelity communication; stakeholder buy-in |

For sprint purposes: **Narrated screen walkthrough** and **Recorded Figma interaction** are fastest and most appropriate.

## Build process (narrated screen walkthrough)

**Step 1 — Write the script (20–30 min):**

Structure the script around the scenario card from Phase 2:
> "It's Tuesday morning. The coordinator has just opened the request system and sees 38 requests waiting for review. They filter by unconfirmed — there are 8. They click the first one: Unit U-200, fault E9, out of service, at Site C. In the top right, they see an urgency score: 78. Below it, three records are listed inline — the CRM, the service-contract database, and the inventory system — so they don't need to open another system. They agree with the suggested priority and assign the request in two taps. Total time: 45 seconds."

The script drives the recording — no improvisation during capture.

**Step 2 — Record the prototype walkthrough (20–30 min):**

- Use Figma, slides, or any prototype tool with screen recording (a built-in OS recorder or any screen-capture tool)
- Navigate through the prototype while narrating the script
- One take per section; edit by concatenation (no need for seamless cuts in a sprint prototype)

**Step 3 — Light edit (15–20 min):**

- Remove dead air and false starts
- Add the scenario title card at the start: "Concept: Reasons-First Triage — [Date]"
- Add a "Sprint Questions this tests" end card
- No music, no graphics, no production value beyond legibility

**Total build time target: < 2 hours**

## Script template

```markdown
## Video Prototype Script — [Concept Name] · [Sprint Name] · [Date]

**Opening scenario card (10 sec):**
"Concept: [Name]. Sprint Question: [SQ]. Participant scenario: [one sentence context]."

**Scene 1 — [Screen name] (30–60 sec):**
[What the user sees. What they do. What the system responds with. Narrate as the user, in present tense.]

**Scene 2 — [Screen name] (30–60 sec):**
[Next interaction. What's key to notice.]

**[...repeat for each storyboard panel...]**

**Closing (10 sec):**
"This concept tests: [assumption 1], [assumption 2]. Validate session will measure: [success signal]."

**Total target length: 2–4 minutes**
```

## Using video in testing

**Async testing:** Send the video to participants; ask them to record a reaction video or fill a short survey while watching. Useful for geographically distributed users.

**In-session:** Play the video at the start of the Five-Act Interview's context-setting phase instead of a scenario card — it grounds the participant in the concept before they interact with a click-through prototype.

**Stakeholder review:** Share with the Decider and any sponsor who wasn't in the sprint room — faster than scheduling a live demo.

## Agent facilitation guide

When producing a video prototype script:
1. Read the storyboard — each panel becomes one scene in the script
2. Write the narration for each scene in present tense, from the user's perspective
3. Note which scene tests which critical assumption — this determines what to emphasise
4. Identify any Wizard-of-oz moments (AI responses, real-time data) and note them as "Wizard: [response to simulate]" in the script
5. Target total video length: 2–4 minutes — long enough to show the flow, short enough to watch twice

## Watch-outs

- **Over-producing:** Sprint video prototypes are not marketing films. Rough narration, visible mouse cursor, and basic editing are fine. Over-production wastes build time and may raise participant expectations unrealistically.
- **No scenario framing:** A video that starts with "here's the dashboard" without context produces shallow reactions. Always open with the scenario: who is this person, what are they trying to do right now?
- **Video replacing interaction:** For most sprint assumptions, participants need to interact with the prototype, not watch it. Use video to communicate context; use click-through for interaction testing.
- **Length over 5 minutes:** Attention drops sharply after 3–4 minutes. If the concept needs more than 4 minutes to explain, it's either too complex or insufficiently focused.

## Connects to

- [Storyboard](../storyboard/SKILL.md) — panels become script scenes
- [Wizard of Oz](../wizard-of-oz/SKILL.md) — Wizard-controlled interactions can be captured as video for async sharing
- [Prototyping Principles](../prototyping-principles/SKILL.md) — video prototype fills the gap between static screens and click-through
- [Five-Act Interview](../five-act-interview/SKILL.md) — video can be used as the Act 3 context-setting material
