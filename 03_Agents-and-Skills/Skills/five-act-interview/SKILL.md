---
name: five-act-interview
title: Run the 5-act user test interview
description: Run a 60-minute structured user interview in five acts — from warm-up to debrief — that tests prototype assumptions without leading the participant. Use on Validate day. Use when a prototype needs to be tested with real users before a build decision, or when a 🟡 Yellow traffic light names "user reaction to [X]" as its trigger condition.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Validate day — five sessions back-to-back (or across two days)
  - Any time a prototype needs to be tested with real users before a build decision
  - When a 🟡 Yellow traffic light names "user reaction to [X]" as its trigger condition
applies-to: usability testing, assumption validation, prototype testing, user research, interview facilitation
done_when:
  - The interview follows the 5 acts (welcome → tasks → debrief)
  - Observations are captured per task without leading the user
  - Notes are ready for team synthesis
metadata:
  duration: 60 min per participant (5 participants across validate day)
  team-size: 1 Interviewer (in room) + full team (observing remotely)
  sprint-phase: 6 Validate
---

# Five-Act Interview

**TL;DR:** The Five-Act Interview is the sprint's primary validation instrument. Five participants, one at a time, each spending 60 minutes with the Interviewer and the prototype. The structure is the same for every session: a gentle welcome, open-ended context questions, prototype tasks, and a debrief. The Interviewer follows the guide; the team watches silently and takes notes. What participants say and do in these five hours determines the forward decision.

## When to use

- Validate day — five sessions back-to-back (or across two days)
- Any time a prototype needs to be tested with real users before a build decision
- When a 🟡 Yellow traffic light names "user reaction to [X]" as its trigger condition

## The five acts

### Act 1 — Friendly Welcome (5 min)
Put the participant at ease and set honest expectations.

**Script:**
> "Thanks for coming in today. Before we start, I want to be clear: we're testing the design, not you. There are no right or wrong answers. If something is confusing, that's incredibly useful feedback for us — it means we need to fix it. I'd also ask you to think out loud as you go. Tell me what you're looking at, what you expect to happen, what's surprising. Do you have any questions before we start?"

Key rules:
- Do not tell the participant what the product does. Let them discover it.
- Do not say "prototype" — say "something we've been working on" or "an early version."
- If they ask "did I do that right?" respond: "What do you think?" Never confirm or deny.

### Act 2 — Open Questions (10 min)
Understand the participant's current behaviour before showing anything.

These questions establish the context — how they actually work today — which makes their reactions to the prototype meaningful. Questions should be open-ended, never leading.

Example questions for a morning triage scenario:
- "Tell me about your typical morning when you're sorting the overnight requests."
- "How do you currently decide whether a request is urgent?"
- "What tools do you use today? Walk me through what you'd normally do."
- "What's the most frustrating part of that process?"

**Rules:**
- Ask one question at a time. Do not compound.
- Follow up with "tell me more" or "why?" — never with a leading interpretation.
- Do not mention the prototype. Do not ask about specific features.
- Listen for evidence of the assumptions on the Assumptions Board.

### Act 3 — Context Introduction (5 min)
Set the scenario that frames the prototype tasks.

> "Now I'm going to show you something we've been working on. Imagine you've just received a notification — we'll set the scene — and I'd like you to walk through what you'd do next. Remember to think out loud as you go."

Give the participant the scenario card:
> *"It's Tuesday morning. You've received a notification from the request system: 3 new unconfirmed requests in the overnight queue need review before the 8am start. Please show me what you'd do."*

The scenario card anchors the test in a realistic moment from their day. It is not a task instruction — it is a context-setter. The tasks follow naturally from exploring the prototype.

### Act 4 — Prototype Tasks (30–35 min)
Observe the participant attempting to complete tasks that test the critical assumptions.

Task format:
- Give the task as a realistic scenario, not a system instruction
- One task at a time — do not preview the next task
- Observe silently. Do not help. Do not redirect.
- Note: what they say, what they do, where they pause, where they misunderstand

**Task cards (example):**

| Task | Sprint assumption tested | Success signal |
|---|---|---|
| T1: "Walk me through what you'd do with these requests." | Urgency score interpreted correctly | Explains the urgency score without prompting |
| T2: "You're not sure about this one — what would you do next?" | Inline records reduce system-switching | Opens the records list; does not open another system |
| T3: "You've decided this request is urgent. What do you do?" | Suggested priority acted on without additional checking | Sets the priority without asking to double-check the AI suggestion |
| T4: "Now assign this to the right specialist." | One-tap assign is faster than 3-step manual process | Completes assignment with ≤2 taps; no confusion |

**Interviewer behaviour during tasks:**
- Silence is productive. Resist filling it.
- If participant is completely stuck (> 2 min silent): "What are you thinking right now?" — not "click here."
- If prototype breaks: "Let's pause there. What were you expecting to happen?"
- Never say "good" or "exactly" — it cues the participant to the "right" answer.

### Act 5 — Debrief (10 min)
Surface beliefs, preferences, and unanswered questions after the tasks.

Debrief questions:
- "Looking back at what you just saw — what was most useful? What was least useful?"
- "If you came back to this tool tomorrow, what would you use it for?"
- "What would make you more confident acting on the suggested priority without checking manually?"
- "Was there anything you expected to see that wasn't there?"
- "What questions do you still have about how this would work?"

The debrief captures attitudes and stated preferences. During tasks you observed behaviour; here you get the participant's mental model and their perceived value.

**Never ask:** "Would you use this?" — the answer is almost always "yes" and it is not predictive of actual behaviour.

## Interview guide template

```markdown
## Five-Act Interview Guide — [Sprint Name] · [Date]

**Participant:** [Name / Role / Company]
**Session number:** [1–5]
**Interviewer:** [Name]
**Observer notes lead:** [Name]

---

### Act 1 — Welcome (5 min)
[ ] Welcomed; comfort established
[ ] Explained: testing the design, not the person
[ ] Requested think-aloud
[ ] Confirmed no questions

### Act 2 — Open questions (10 min)
Q1: Current morning triage workflow
Q2: How they decide a request is urgent
Q3: Frustrations with current tools
[ ] Heard evidence about: [assumption name]
[ ] Key quote: "..."

### Act 3 — Context intro (5 min)
Scenario card given: Tuesday morning; 3 unconfirmed requests; review before the 8am start

### Act 4 — Tasks (30–35 min)

| Task | Completed? | Time | Key observations |
|---|---|---|---|
| T1: Walk through requests | ☐ Yes ☐ Partial ☐ No | | |
| T2: Unsure request — what next? | ☐ Yes ☐ Partial ☐ No | | |
| T3: Prioritise urgent request | ☐ Yes ☐ Partial ☐ No | | |
| T4: Assign to specialist | ☐ Yes ☐ Partial ☐ No | | |

### Act 5 — Debrief (10 min)
Most useful: 
Least useful:
Would return to use for:
Missing expectation:
Remaining questions:

---

### Post-session (Interviewer only, 5 min)
Top insight from this session:
Assumption confirmed / challenged:
One quote worth sharing with the team:
```

## Scheduling guide

| Time | Session |
|---|---|
| 09:00–10:00 | Participant 1 |
| 10:15–11:15 | Participant 2 |
| 11:30–12:30 | Participant 3 |
| 13:30–14:30 | Participant 4 |
| 14:45–15:45 | Participant 5 |
| 16:00–17:00 | Synthesis session |

15-minute buffers between sessions allow the team to update observation notes and the Interviewer to reset.

## Agent facilitation guide

When generating a Five-Act Interview guide from an Assumptions Board and storyboard:
1. Read the Assumptions Board — extract each critical assumption and its success signal
2. Write one task card per critical assumption — scenario language, not system language
3. Write Act 2 questions that surface the participant's current behaviour relevant to the assumptions
4. Write Act 5 debrief questions that surface attitudes and mental models around the critical assumptions
5. Estimate task count — aim for 3–5 tasks in 30 minutes; flag if more than 5 (sessions run over)

## Watch-outs

- **Leading questions:** "Did you find the urgency score helpful?" vs. "What did you make of the numbers you saw?" The first tells the participant what they should have noticed.
- **Rescuing the participant:** If a participant is stuck, silence feels unbearable to the Interviewer. Resist. The stuck moment is data — what exactly caused the pause is more valuable than completing the task.
- **Sessions running long:** Keep Act 2 to 10 minutes. Overlong context-gathering eats task time.
- **Only 1–2 participants:** Five participants is the minimum for meaningful pattern detection. With fewer, you'll see individual behaviour, not patterns. If you can only get 3, be explicit that findings are directional only.
- **Observer talking during the session:** The team observes silently. One voice (the Interviewer) per room. Observer messages go into the shared notes doc only.

## Connects to

- [Assumptions Board](../assumptions-board/SKILL.md) — tasks are built around critical assumptions
- [Storyboard](../storyboard/SKILL.md) — prototype panels map to task flow
- [Team Observation](../team-observation/SKILL.md) — team watches and logs concurrently
- [Synthesis](../research-synthesis/SKILL.md) — session notes become the input to pattern finding
