---
name: team-observation
title: Observe sessions together and note patterns live
description: The sprint team observes each interview session live — silently, with structured notes — so synthesis is already half-done when the last session ends. Use when a sprint team wants to build a shared understanding of user research without a summary presentation, during all five interview sessions on Validate day, or when the team needs to go from sessions to a build decision in the same afternoon.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - During all five interview sessions on Validate day
  - Any time a sprint team wants to build a shared understanding of user research without a summary presentation
  - When the team needs to go from sessions to a build decision in the same afternoon
applies-to: live research observation, pattern detection, note-taking discipline, assumption tracking, synthesis prep
done_when:
  - The team observed sessions and logged notes in a shared grid
  - Notes are tagged by participant and task
  - Cross-participant patterns are surfaced for synthesis
metadata:
  duration: 60 min per session × 5 sessions
  team-size: Full sprint team (except Interviewer)
  sprint-phase: 6 Validate
---

# Team Observation

**TL;DR:** While the Interviewer runs the Five-Act Interview, the rest of the sprint team watches. Not passively — they are taking structured notes in a shared document, tracking each assumption in real time, flagging moments, and debating nothing. The discipline of structured observation means that by the end of session 5, the team already has a rough synthesis rather than a pile of raw notes.

## When to use

- During all five interview sessions on Validate day
- Any time a sprint team wants to build a shared understanding of user research without a summary presentation
- When the team needs to go from sessions to a build decision in the same afternoon

## Setup

### Before sessions start

1. **Observation room or remote channel:** The team watches via a live stream, a screen share, or through a one-way mirror. The participant must not be aware of the full team.
2. **Shared notes document:** One collaborative doc (an online document, a shared whiteboard, or a shared sticky wall) — one section per participant, one row per assumption.
3. **Assumption tracking grid (prepared in advance):** The grid has the sprint's critical assumptions as column headers and participant slots as rows. During each session, an assigned note-taker marks each assumption as Confirmed / Challenged / Unclear based on live behaviour.
4. **"Interesting moment" log:** A running list — timestamped — of specific participant quotes, unexpected behaviours, or surprising moments. These become synthesis anchors.

### Role during sessions

| Role | Responsibility |
|---|---|
| **Interviewer** | Runs the session; no contact with the observation team during session |
| **Note lead** | Fills the observation doc for this session; responsible for the assumption grid row |
| **Moment logger** | Logs timestamped notable moments ("P2 14:22 — didn't notice the urgency score at all") |
| **Silent team** | Watch, think, type notes — do not speak until between sessions |

Rotate the Note Lead role between sessions so no one person carries all five sessions.

## Observation note format

For each session, the team completes one row of the assumption tracking grid:

```markdown
## Participant [N] — [Initials/Role] · [Session time]

### Assumption tracking
| Assumption | Evidence | Status |
|---|---|---|
| Users interpret the urgency score correctly | Named "High" without prompting on T1; asked "what does 62 mean?" on T2 | ⚠️ Partial |
| Inline records reduce system-switching | Opened records panel; did not open another system | ✅ Confirmed |
| Suggested priority acted on without checking | Asked "how sure is the system?" before setting the priority — paused 40 seconds | ❌ Challenged |
| One-tap assign faster than 3-step | Completed in 2 taps; said "oh that's easy" | ✅ Confirmed |

### Interesting moments
- [14:07] Scrolled past the urgency score entirely on first pass — only noticed on return
- [14:22] "Where does this go once I set the priority?" — expected a request card view
- [14:44] Reacted positively to records list: "I like that I can see where this came from"

### One sentence summary
Confirmed record visibility value; challenged the priority trust assumption — wants to understand how the score is worked out before acting on the suggested priority alone.
```

## The assumption status system

Use three states only. Do not introduce nuance during sessions — save interpretation for synthesis:

| Status | Meaning |
|---|---|
| ✅ Confirmed | Participant behaved in the way that validates the assumption (matched success signal) |
| ❌ Challenged | Participant behaved in a way that contradicts the assumption |
| ⚠️ Partial | Mixed evidence — assumption partially validated, or validated for some users but not others |

Fill the grid row **immediately after each session** — not at the end of the day. Memory degrades fast.

## Between-session routine (15 min)

After each session, the team has 15 minutes before the next participant arrives:

1. **Note lead completes the grid row (5 min):** Fill in all assumption statuses while memory is fresh.
2. **Team shares top 2 moments (5 min):** Each observer names one thing that surprised them — one sentence each. No discussion or debate.
3. **Pattern flag (2 min):** Did this session reinforce or contradict any pattern from previous sessions? Note it.
4. **Reset (3 min):** Interviewer debrief; prototype reset if needed; Stitcher fixes any broken prototype links.

**No synthesis during between-session breaks.** The team shares observations, not conclusions. Conclusions are drawn in the synthesis session after all 5 interviews.

## Running assumption tally

After each session, update the running tally:

```markdown
## Assumption Tally (updated after each session)

| Assumption | P1 | P2 | P3 | P4 | P5 | Pattern |
|---|---|---|---|---|---|---|
| Urgency score interpreted correctly | ⚠️ | ❌ | ✅ | ⚠️ | ❌ | Failing — needs legend |
| Inline records reduce system-switching | ✅ | ✅ | ✅ | ✅ | ⚠️ | Strong confirm |
| Suggested priority acted on | ❌ | ❌ | ⚠️ | ❌ | ✅ | Failing — trust gap |
| One-tap assign is fast | ✅ | ✅ | ✅ | ✅ | ✅ | Confirmed |
```

This tally is visible to the full team in real time. By session 3, patterns are usually visible. By session 5, the synthesis session is mostly confirming what the tally already shows.

## Agent facilitation guide

When processing observation notes from a sprint validate day:
1. Read all five session notes — extract the assumption grid rows
2. Build the consolidated assumption tally
3. For each assumption: determine the pattern (confirmed / challenged / partial) with evidence count
4. Extract the top 3 "interesting moment" quotes per challenged assumption — these are the most important findings
5. Flag any unexpected behaviour that appears across 3+ participants but wasn't an original assumption — this is a discovered finding

Output:
```markdown
## Observation Summary — [Sprint Name] · [Date]

### Assumption tally (5/5 sessions complete)

| Assumption | Result | Evidence |
|---|---|---|
| Urgency score interpreted correctly | ❌ Challenged (3/5 failed) | P1, P2, P4 did not explain the urgency score without prompting |
| Inline records reduce system-switching | ✅ Confirmed (4/5) | Only P5 opened another system |
| Suggested priority acted on | ❌ Challenged (4/5 challenged) | Participants wanted to know how the score is worked out before acting |
| One-tap assign is fast | ✅ Confirmed (5/5) | Unanimous positive reaction |

### Discovered finding (not an original assumption)
3/5 participants expected a "request history" view after setting the priority — asked "where does this go?" This suggests a downstream request-history need not addressed by the prototype.

### Quotes (top 3 per challenged assumption)

**Urgency score:**
- P1: "What does 62 mean? Is that out of 100? Out of what?"
- P2: "I'd want to know what makes it high vs. low before I trust this"
- P4: [scrolled past score entirely on first pass]

**Suggested-priority trust:**
- P1: "I'd still want to check this myself before putting my name on it"
- P2: "How sure is the system? What is it based on?"
- P3: "I'd use this as a starting point, but I'd want a second opinion"
```

## Watch-outs

- **Team discussing findings between sessions:** "That participant confirmed X" is fine. "That means we need to change Y" is not. Save synthesis for after session 5. Mid-session conclusions bias subsequent observation.
- **Note lead too slow to capture:** Notes taken 20 minutes after a session are reconstructed memory, not observation. Enforce the between-session routine.
- **Assumption grid left blank for "unclear" sessions:** Partial evidence is still evidence. An "unclear" assumption is a data point — it means the prototype didn't surface enough signal to confirm or challenge, which itself may warrant redesign.
- **Team losing focus by session 4:** Observation fatigue is real. Rotate the Note Lead role. Name someone specifically responsible for the "interesting moments" log to keep attention high.
- **Ignoring unexpected findings:** Participants regularly reveal needs outside the original sprint questions. Log these as "discovered findings" — they inform future sprint questions even if not immediately actionable.

## Connects to

- [Five-Act Interview](../five-act-interview/SKILL.md) — the sessions being observed
- [Assumptions Board](../assumptions-board/SKILL.md) — the assumption grid is built from this
- [Synthesis](../research-synthesis/SKILL.md) — observation notes are the primary input; the tally is pre-synthesis
