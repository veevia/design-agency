---
name: usability-metrics
title: Measure task success, time, and error rates
description: Measure objective task performance — completion rate, time-on-task, and error rate — to quantify usability and anchor qualitative observations with behavioural data. Use when the sprint question includes performance or efficiency components ("can coordinators assign an urgent request in < 45 seconds?"), or when the team needs to compare two concepts objectively (Concept Rumble follow-up).
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - When the sprint question includes performance or efficiency components ("can coordinators assign an urgent request in < 45 seconds?")
  - When the team needs to compare two concepts objectively (Concept Rumble follow-up)
  - When the Decider or stakeholders need quantitative evidence to commit to a build decision
  - When the team wants to identify specific failure points for a follow-up prototype iteration
  - Any time task completion data would strengthen a go/no-go recommendation
applies-to: task completion rate, time-on-task, error rate, quantitative usability benchmarking, concept comparison, sprint go/no-go evidence
done_when:
  - Task success/failure, time, and errors are recorded per task
  - Metrics are summarised across participants
  - Problem areas are ranked for the synthesis and fixes
metadata:
  duration: Measured during Five-Act Interview tasks; calculated in Synthesis
  team-size: Observer logs metrics during sessions; Stitcher or Facilitator calculates after all sessions
  sprint-phase: 6 Validate
---

# Usability Metrics

**TL;DR:** Usability metrics are objective measurements of participant behaviour during prototype testing. Unlike survey scores (self-reported) or interview quotes (interpreted), usability metrics record what actually happened: did the participant complete the task, how long did it take, and how many errors occurred along the way. With 5 participants, these metrics are directional signals — not statistically significant measurements — but they provide a category of evidence that qualitative observation alone cannot give: "4 of 5 participants failed to locate the assign button on the first attempt" is harder to dismiss than "participants seemed to have trouble with assignment."

## When to use

- When the sprint question includes performance or efficiency components ("can coordinators assign an urgent request in < 45 seconds?")
- When the team needs to compare two concepts objectively (Concept Rumble follow-up)
- When the Decider or stakeholders need quantitative evidence to commit to a build decision
- When the team wants to identify specific failure points for a follow-up prototype iteration
- Any time task completion data would strengthen a go/no-go recommendation

## Core usability metrics

### 1. Task Completion Rate

The percentage of participants who successfully complete each task without assistance.

**Success criteria must be defined before testing begins — not after.**

| Outcome | Definition |
|---|---|
| **Complete success** | Participant completes the task without any help from the Interviewer |
| **Partial success** | Participant completes the task only after a hint or redirect from the Interviewer |
| **Failure** | Participant cannot complete the task even with a hint; or gives up; or completes the wrong task |

```
Task completion rate = (Complete successes / Total participants) × 100
```

Sprint benchmark: ≥ 80% complete success on the primary task for a first-round prototype is a strong signal.

### 2. Time-on-Task

Elapsed time from "task begins" to "task complete or abandoned."

- **Start:** When the Interviewer finishes reading the task prompt
- **End:** When the participant says "done" or the Interviewer records completion / failure

Time-on-task is most valuable as a comparison:
- Between tasks within one prototype (which task is hardest?)
- Between concepts in a Concept Rumble
- Against a baseline (if the existing workflow was timed)

**Sprint benchmark for request assignment:** If the coordinator assigns an urgent request in < 45 seconds, the concept meets the speed hypothesis.

### 3. Error Rate

The number of incorrect actions (wrong taps, wrong selections, back-navigation after a mistake) per participant per task.

Count an error when:
- Participant taps a wrong element
- Participant navigates to a dead end and must back out
- Participant misunderstands a label and selects the wrong option (before self-correcting or giving up)

```
Mean errors per task = Total errors for task across all participants / Number of participants
```

### 4. Lostness Score (advanced, optional)

A more precise navigation efficiency metric for complex flows:

```
L = √[(N/Sopt − 1)² + (R/N − 1)²]
```
- `N` = number of steps taken by participant
- `Sopt` = optimal (minimum) number of steps
- `R` = number of steps revisited

L = 0 is perfect navigation. L > 0.5 indicates significant navigation difficulty. Useful when the prototype has multiple paths to the same destination.

## Observation log format

Observer records during each session:

```markdown
## Usability Metrics Log — P[N] · [Sprint Name] · [Date]

### Task 1: Locate and open the most urgent unconfirmed request
Start time: 10:02:14
End time: 10:02:52
Duration: 38 sec
Outcome: ✓ Complete success
Errors: 1 (tapped "Confirmed" filter tab before self-correcting to "Unconfirmed")
Notes: Hesitated on filter tabs — scanned all 4 before selecting

### Task 2: Interpret the urgency score for the Unit U-200 request
Start time: 10:03:05
End time: 10:04:10
Duration: 65 sec
Outcome: ~ Partial success (required Interviewer hint: "What information does the score give you?")
Errors: 0 (didn't tap wrongly, just didn't understand the display)
Notes: Read "Urgency 78" aloud; then said "but 78 out of what?" — never clicked the explanation link

### Task 3: Assign the request to the right specialist
Start time: 10:04:30
End time: 10:05:52
Duration: 82 sec
Outcome: ✓ Complete success
Errors: 2 (first tried to assign from the list view; found the assignment form; then submitted without checking the specialist)
Notes: "This is like email — I just wanted to hit send"
```

## Cross-participant summary

```markdown
## Usability Metrics Summary — [Sprint Name] · [Concept Name] · [Date]

| Task | P1 | P2 | P3 | P4 | P5 | Completion Rate | Mean Time | Mean Errors |
|---|---|---|---|---|---|---|---|---|
| T1: Find urgent request | ✓ | ✓ | ✓ | ✓ | ~ | 80% | 41 sec | 0.6 |
| T2: Interpret urgency score | ✓ | ~ | ~ | ~ | ✗ | 20% | 58 sec | 0.4 |
| T3: Assign request | ✓ | ✓ | ✓ | ~ | ✓ | 80% | 74 sec | 1.4 |

### Interpretation
Task 2 (urgency score interpretation) is the critical failure: 20% unaided completion rate against an 80% benchmark. Aligns with qualitative observation that all 5 participants asked "what does this score mean?" SUS item 3 (urgency score understanding) scored 3.4 / 5, confirming the signal.

Task 3 assignment performance is adequate (80% completion) but mean time of 74 sec is above the 45-sec hypothesis. Error rate of 1.4 errors/participant suggests assignment form friction — 3 participants tried to assign from the list view before finding the detail-level assign button.
```

## Watch-outs

- **Defining success criteria after testing:** If the team decides what "success" looks like after seeing the data, they will unconsciously move the goalposts. Define task completion criteria in the prototype review, before Day 6.
- **Using metrics to dismiss qualitative findings:** "4 of 5 completed the task, so the assignment flow is fine" is incorrect if all 4 struggled significantly, made multiple errors, and expressed frustration. Metrics and observations triangulate — neither overrides the other.
- **Overprecision with n=5:** Reporting "83.3% completion rate" implies false precision. With 5 participants, say "4 of 5 completed" or "80% completion" — enough resolution without implying statistical validity.
- **Timing yourself into paralysis:** Don't sacrifice session flow for perfect metric capture. If the observer misses a start time because a task began unexpectedly, note it as approximate. Rough timing is far better than no timing.

## Agent facilitation guide

When calculating usability metrics:
1. Receive the observation log from each session
2. For each task and participant: classify outcome (complete / partial / failure) using pre-defined criteria
3. Calculate task completion rate: (complete successes / n) × 100
4. Calculate mean time-on-task: average elapsed seconds per task
5. Calculate mean error rate: total errors / n per task
6. Cross-reference with the sprint's performance hypothesis: did the concept meet the benchmark?
7. Output: summary table + 2–3 sentences interpreting the patterns, with specific reference to the most critical task

## Connects to

- [Five-Act Interview](../five-act-interview/SKILL.md) — tasks in Act 4 generate the raw metrics data
- [Team Observation](../team-observation/SKILL.md) — observers log metric data alongside qualitative notes
- [Post-Test Survey](../post-test-survey/SKILL.md) — SUS scores complement completion rate and error rate
- [Synthesis](../research-synthesis/SKILL.md) — usability metrics are one of three input streams to the synthesis session
- [Assumptions Board](../assumptions-board/SKILL.md) — performance hypotheses on the Assumptions Board are validated against these metrics
