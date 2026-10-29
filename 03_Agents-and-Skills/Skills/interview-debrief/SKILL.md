---
name: interview-debrief
title: Debrief the team right after each interview
description: Run a 10-minute structured team debrief after each interview session — to capture fresh reactions, flag emerging patterns, and prevent insight from degrading before Synthesis. Use after every participant session on Validate day, within 2 minutes of the participant ending the session (not "after lunch"). Use when the team is about to talk informally about what just happened — informal conversation depletes the debrief.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - After every participant session on Validate day — all 5 sessions
  - Within 2 minutes of the participant ending the session (not "after lunch")
  - Before the team talks informally about what just happened — informal conversation depletes the debrief
applies-to: per-session insight capture, pattern emergence, real-time assumption tracking, observer alignment, Synthesis preparation
done_when:
  - The team captured observations immediately after the interview
  - Notes are organised per participant/task
  - Patterns are flagged for the synthesis step
metadata:
  duration: 10 min immediately after each participant session
  team-size: Full observation team (Interviewer + all observers)
  sprint-phase: 6 Validate
---

# Interview Debrief

**TL;DR:** An interview debrief is the 10-minute team conversation that happens immediately after a participant leaves. It is distinct from Synthesis — it doesn't produce final conclusions, it captures raw reactions while they're fresh. By the time 5 sessions are complete and the team moves into Synthesis, the first participant's details will have faded. The debrief creates the notes that make Synthesis reliable. The discipline is to run it before discussing the next participant, before checking messages, and before taking a break.

## When to use

- After every participant session on Validate day — all 5 sessions
- Within 2 minutes of the participant ending the session (not "after lunch")
- Before the team talks informally about what just happened — informal conversation depletes the debrief

## Debrief structure (10 minutes exactly)

**Round 1 — What stood out? (3 min)**

Go around the room. Each observer says the single most striking moment from the session — one sentence each. No discussion, no debate. The Facilitator writes each observation on a sticky.

Examples:
> "She read the urgency score, then immediately looked for the records list — she expected reasons to accompany the number."
> "He completed Task 3 in 28 seconds without hesitation — fastest we've seen."
> "She said 'this looks like work' — not a compliment."

**Round 2 — Critical assumption check (3 min)**

Go through the Assumptions Board, one assumption at a time. For each critical assumption, the Facilitator asks: "What did this participant do that confirms or challenges this assumption?" One sentence per assumption.

Log as: `[A#] [Participant #] [Confirms / Challenges / Neutral] — [one sentence]`

**Round 3 — Patterns (2 min)**

Facilitator asks: "Did anything happen today that we've also seen in a previous session?" If yes, the Facilitator adds a tally mark to that observation's sticky — recurring observations become the candidates for Synthesis clusters.

**Close (2 min)**

- Facilitator reads back the 3–5 stickies from Round 1 so every observer confirms their note was captured correctly
- If a participant gave unusual or contradictory data: Facilitator flags it as `outlier — P[N]` so it doesn't drive pattern-finding unfairly
- Interviewer notes any changes needed to the session guide before the next participant

## Debrief log format

```markdown
## Interview Debrief — P[N] · [Sprint Name] · [Date] · [Start time]

### Round 1 — Standout moments
- [Observer 1]: "Immediately noticed the records list — the first thing she did after seeing the urgency score"
- [Observer 2]: "Expressed frustration with the assignment form — 'why do I have to select the site, doesn't the system know?'"
- [Interviewer]: "Picked 'Efficient' and 'Overwhelming' in desirability — the tension is real"

### Round 2 — Assumption tracking
- A1 (urgency score reduces checking time): CHALLENGES — P3 spent 65 sec on Task 2, longer than current workflow by ~15 sec. But failure was interpretation, not the concept.
- A2 (inline records replace system-switching): CONFIRMS — "I didn't have to open the service-contract database at all — it's right there"
- A3 (assign CTA visible and intuitive): CHALLENGES — P3 tapped the list-level assign button first; then found the detail-level one

### Round 3 — Pattern tally
- "Read score, looked for records" — also occurred with P1, P2. Running total: 3/3. 🔴 STRONG PATTERN
- "Assigning from list vs. detail confusion" — also P2. Running total: 2/3.
- "Expressed satisfaction at speed" — unique to P3 so far.

### Outliers / flags
- P3 completes fastest by 30+ seconds — may be an expert outlier; watch against P4/P5

### Session guide adjustment
- Slow down the briefing for Task 2 — P1 and P3 both seem to miss the explanation link. Either it's not visible or the task isn't priming them to look.
```

## Debrief vs. Synthesis

| | Interview Debrief | Synthesis |
|---|---|---|
| **Timing** | Immediately after each session | After all 5 sessions |
| **Duration** | 10 min | 2–3 h |
| **Purpose** | Capture fresh observations; track emerging patterns | Find patterns, vote on insights, make decisions |
| **Output** | Sticky notes + assumption tallies | Insight clusters + go/no-go decision |
| **Who runs it** | Facilitator | Any designated lead |
| **Decision-making** | No — observational only | Yes — forward decision |

## Watch-outs

- **Skipping debrief to "save time":** Running 5 sessions without debriefs and then doing Synthesis produces lower-quality insights. Teams reconstruct rather than recall. The first participant's data is effectively lost. The 10-minute investment per session returns significantly in Synthesis quality.
- **Debrief becoming Synthesis:** If the team starts drawing conclusions, voting on insights, or deciding what to build during a debrief, they're doing Synthesis without all the data. The debrief question is "what happened?" not "what does it mean?"
- **Observer dominance:** If one observer's reactions dominate the debrief every session, their framing shapes the Synthesis. Go around the room; capture every observer's standout moment first, before any discussion.
- **Forgetting the Assumptions Board:** The debrief is the fastest way to track which assumptions are accumulating confirmations vs. challenges across participants. A team that stops checking the Assumptions Board in debrief will enter Synthesis with no running tally — rebuilding the tally from memory.

## Agent facilitation guide

When generating a post-session debrief:
1. Receive session observation notes from the Interviewer and observers
2. Extract the 3–5 most striking moments (one per observer where possible)
3. Go through each critical assumption on the Assumptions Board: classify as Confirms / Challenges / Neutral based on the session data; write one sentence of evidence
4. Compare to previous sessions: flag any observation that recurs from P1–P[N-1] with a pattern tally
5. Flag outliers explicitly — data points that contradict the emerging pattern
6. Output: debrief log in the format above; mark `🔴 STRONG PATTERN` for any observation tallied by ≥3/5 participants

## Connects to

- [Team Observation](../team-observation/SKILL.md) — observation notes are the raw input to the debrief
- [Five-Act Interview](../five-act-interview/SKILL.md) — each interview session produces one debrief
- [Synthesis](../research-synthesis/SKILL.md) — debrief logs and pattern tallies are the primary input to Synthesis
- [Assumptions Board](../assumptions-board/SKILL.md) — the debrief is the mechanism that tracks confirmation vs. challenge of critical assumptions across sessions
