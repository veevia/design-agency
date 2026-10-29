---
name: paper-prototype
title: Build a fast low-fidelity paper prototype
description: Build a fast, low-fidelity physical prototype using paper, sticky notes, and printed screens — to test flows and layouts before committing to digital tools. Use when the sprint needs to test an information architecture, navigation flow, or content structure before any digital tool is opened, or when the concept has never been sketched as a UI before and the team needs rapid feedback before committing to Figma.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - When the sprint needs to test an information architecture, navigation flow, or content structure before any digital tool is opened
  - When the concept has never been sketched as a UI before and the team needs rapid feedback before committing to Figma
  - When iteration speed matters more than visual fidelity — paper can be changed in 60 seconds
  - For testing form flows, wizard steps, or complex navigation without building click-through logic
  - When participants are known to be heavily influenced by visual polish — paper explicitly signals "early concept" and reduces "I don't want to criticise the design" hedging
applies-to: early-stage flow testing, rapid iteration, low-risk concept validation, information architecture testing, mobile/desktop layout exploration
done_when:
  - A testable paper prototype of the key flow exists
  - Screens/states are sketched at the fidelity the test needs
  - It’s ready to put in front of a user without code
metadata:
  duration: 1–2 h build; 30–45 min per test session
  team-size: 2–3 Makers; 1 Interviewer; 1 Facilitator (manual screen controller)
  sprint-phase: 5 Prototype
---

# Paper Prototype

**TL;DR:** A paper prototype is a hand-drawn or printed representation of a UI, assembled from physical materials — paper screens, sticky notes, index cards, and cut-out elements. A team member acts as the "computer" — manually swapping paper screens as the participant "taps" or "clicks." The fidelity is deliberately low: the goal is to test whether the *flow* and *structure* work, not whether the visual design is polished.

## When to use

- When the sprint needs to test an information architecture, navigation flow, or content structure before any digital tool is opened
- When the concept has never been sketched as a UI before and the team needs rapid feedback before committing to Figma
- When iteration speed matters more than visual fidelity — paper can be changed in 60 seconds
- For testing form flows, wizard steps, or complex navigation without building click-through logic
- When participants are known to be heavily influenced by visual polish — paper explicitly signals "early concept" and reduces "I don't want to criticise the design" hedging

## When NOT to use

- When the assumption being tested is about visual communication (e.g., "will users interpret the urgency score correctly?") — visual fidelity matters for visual assumptions
- When the test requires animated transitions or realistic data
- When testing enterprise software where participants expect professional fidelity from the outset

## Materials

- A4 / letter paper or index cards (one per screen)
- Markers (medium nib) for drawing UI elements
- Scissors, tape, sticky notes for interactive elements
- A mobile phone or tablet outline drawn on paper (for mobile prototypes)
- Printer (optional) — for printing screenshots or grid templates

## Roles during paper prototype testing

| Role | Responsibility |
|---|---|
| **Interviewer** | Conducts the Five-Act Interview; gives tasks; does not touch the prototype |
| **Computer** | The team member who swaps paper screens and places elements based on participant actions; acts as the system |
| **Observer** | Takes notes on participant behaviour, confusion points, unexpected actions |

The "Computer" role is critical. When the participant says "I'd tap here," the Computer responds by placing the relevant paper response or swapping to the next screen. No verbal explanation — just the physical response.

## Steps

**Build phase (1–2 h):**
1. Draw or print one screen per paper page — key screens from the storyboard only
2. Draw interactive elements (buttons, tabs, menus) on separate pieces of paper so they can be placed/removed
3. Prepare any dynamic responses: "if participant taps X, place response Y on screen"
4. Number the screens in the flow order; write the Computer's script alongside

**Test session:**
1. Interviewer gives the task ("Show me what you'd do to sort this morning's requests")
2. Participant points or taps on the paper
3. Computer swaps the screen to the next state without speaking
4. Interviewer observes and asks think-aloud questions
5. Observer logs: what did the participant do? What did they say? Where did they pause?

## Paper prototype outputs

```markdown
## Paper Prototype Test Notes — [Sprint Name] · P[N] · [Date]

### Task 1: Find the most urgent request
Participant action: Looked at the header row first, then scanned left column
Unexpected: Tried to click the booking channel (not a link in paper prototype — noted)
Confusion point: The "Priority" column header wasn't immediately noticed — scanned past it
Time to complete: ~35 seconds

### Task 2: Review urgency score
Participant action: Read the number (78); then asked "what does that mean?"
Outcome: Cannot interpret without explanation — supports our critical assumption concern
Computer response: Placed the tooltip card showing explanation
Reaction: "Oh, that makes sense — I'd want to see that every time"

### Task 3: Assign the request
Participant action: Tapped "Assign" button immediately
Confusion point: The assignment form (7 fields) caused immediate hesitation — "This is a lot"
Computer response: Swapped to form screen
Outcome: Participant completed form but said "this is slower than just phoning the site"
```

## Iteration speed advantage

Paper prototypes can be revised mid-session:
- If a participant can't find the assign button, redraw it in 30 seconds and try with the next participant
- If the urgency score label is misread, relabel it with a marker before the next session
- This real-time iteration is impossible with digital prototypes without halting all sessions

## Agent facilitation guide

When recommending a paper prototype:
1. Identify which storyboard screens test *flow and structure* (not visual communication)
2. List the screens to build: typically 4–8 key states
3. Define the Computer's script: "if participant does X, respond with Y"
4. Design the test tasks — same Five-Act structure applies
5. Note: paper prototype results should be tagged as `low-fidelity` in synthesis — assumptions about visual clarity require a higher-fidelity test

## Watch-outs

- **Computer speaking:** The Computer is a silent machine. If they explain "oh, that would normally go to the next screen," they're invalidating the test. Silence only.
- **Too many screens:** A paper prototype with 25 screens is too complex to manage. Limit to the screens that test the critical assumptions — typically 5–8.
- **Dismissing findings as "just paper":** "They only reacted that way because it was paper" is often wrong. Confusion about navigation structure is real regardless of fidelity. Take findings seriously.
- **Not preparing Computer responses in advance:** If the Computer has to improvise mid-session, they'll create inconsistent experiences across participants. Script the responses before testing starts.

## Connects to

- [Prototyping Principles](../prototyping-principles/SKILL.md) — paper prototype is the lowest fidelity option in the ladder
- [Storyboard](../storyboard/SKILL.md) — paper screens are the physical version of storyboard panels
- [Five-Act Interview](../five-act-interview/SKILL.md) — same interview structure applies; Computer role replaces digital prototype
- [Assumptions Board](../assumptions-board/SKILL.md) — paper test results update the assumptions board; flag fidelity level
