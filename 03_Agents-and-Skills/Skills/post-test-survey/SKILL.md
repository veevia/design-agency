---
name: post-test-survey
title: Capture structured post-test feedback
description: Collect structured quantitative feedback from participants after testing — using SUS or a custom instrument — to complement qualitative interview observations with a numeric usability signal. Use when the team needs a comparable numeric signal across all 5 participants (qualitative data alone makes it hard to say "P3 had more difficulty than P2"), or when the sprint is testing two competing concepts (Concept Rumble).
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - When the team needs a comparable numeric signal across all 5 participants (qualitative data alone makes it hard to say "P3 had more difficulty than P2")
  - When the sprint is testing two competing concepts (Concept Rumble) — SUS scores provide a clean comparison
  - When stakeholders expect quantitative evidence and qualitative notes alone won't pass their review
  - When the sprint will inform a go/no-go decision and the team wants one more data point beyond task observations
applies-to: SUS scoring, satisfaction measurement, quantitative usability signal, concept comparison, NPS-equivalent, post-session structured feedback
done_when:
  - Participants complete a consistent post-test instrument
  - Quant signals (e.g. ease, confidence) are recorded
  - Results are ready to combine with qualitative notes
metadata:
  duration: 5–10 min (administered at end of Five-Act Interview, after tasks)
  team-size: Administered by Interviewer; analysed by the full team in Synthesis
  sprint-phase: 6 Validate
---

# Post-Test Survey

**TL;DR:** A post-test survey is a short, standardised questionnaire administered at the end of each participant session. It converts the participant's overall experience into a comparable numeric score. The System Usability Scale (SUS) is the most widely validated instrument: 10 questions, alternating positive/negative, scored 0–100. For sprint purposes, a 5-item custom instrument is often faster and equally useful when targeted at the sprint's specific assumptions. The survey runs after all tasks are complete, before the participant leaves.

## When to use

- When the team needs a comparable numeric signal across all 5 participants (qualitative data alone makes it hard to say "P3 had more difficulty than P2")
- When the sprint is testing two competing concepts (Concept Rumble) — SUS scores provide a clean comparison
- When stakeholders expect quantitative evidence and qualitative notes alone won't pass their review
- When the sprint will inform a go/no-go decision and the team wants one more data point beyond task observations

## The System Usability Scale (SUS)

SUS is 10 statements rated 1 (Strongly Disagree) to 5 (Strongly Agree). Alternating items are positive and negative — this forces the participant to read carefully instead of pattern-rating.

| # | Statement |
|---|---|
| 1 | I think that I would like to use this system frequently. |
| 2 | I found the system unnecessarily complex. |
| 3 | I thought the system was easy to use. |
| 4 | I think that I would need support from a technical person to use this system. |
| 5 | I found the various functions in this system were well integrated. |
| 6 | I thought there was too much inconsistency in this system. |
| 7 | I would imagine that most people would learn to use this system very quickly. |
| 8 | I found the system very cumbersome to use. |
| 9 | I felt very confident using the system. |
| 10 | I needed to learn a lot of things before I could get going with this system. |

**Scoring:**
- Odd items (positive): score = response − 1
- Even items (negative): score = 5 − response
- Total all 10 adjusted scores × 2.5 = SUS score (0–100)

**Benchmarks:**
| Score | Grade | Interpretation |
|---|---|---|
| ≥ 85 | A | Excellent usability |
| 72–84 | B | Good usability |
| 52–71 | C | OK usability — improvements warranted |
| 38–51 | D | Poor usability |
| < 38 | F | Unacceptable usability |

Sprint target: SUS ≥ 68 (industry average) for a first-round prototype. If ≥ 80 with n=5, the concept is strong on usability.

## Sprint custom instrument (alternative to full SUS)

When 10 questions is too long (< 30 min sessions), use a 5-item targeted survey:

```markdown
## Post-Session Survey — [Sprint Name] · [Date]

After your experience with the prototype, please rate the following (1 = Strongly Disagree, 5 = Strongly Agree):

1. I was able to complete the tasks without help.                    1  2  3  4  5
2. The information I needed was easy to find on the screen.          1  2  3  4  5
3. I understood what the AI urgency score meant.                     1  2  3  4  5  ← sprint-specific
4. I would use this tool in place of my current workflow.            1  2  3  4  5  ← sprint-specific
5. I would recommend this tool to a colleague who does my job.       1  2  3  4  5

Any other thoughts? ___________________________________________
```

Items 3–4 in the example above are sprint-specific — targeted at the critical assumptions from the Assumptions Board. Replace with your sprint's assumptions.

## Survey administration

**How to administer:**
1. At the end of Act 4 (tasks), after the participant has experienced the full prototype
2. Say: "Before we finish, I'd like you to fill out a short survey about your experience. There are no right or wrong answers — this helps us understand your overall impressions."
3. Hand them the survey or send the link (for remote sessions, use a form tool)
4. Do not explain or clarify items — this is a standardised instrument; explanations invalidate comparability
5. Give them privacy to fill it out — do not hover and read over their shoulder

## Analysis across participants

```markdown
## Post-Test Survey Results — [Sprint Name] · [Concept Name] · [Date]

### SUS Scores
| Participant | Raw score | Interpretation |
|---|---|---|
| P1 | 77.5 | Good |
| P2 | 62.5 | OK |
| P3 | 80.0 | Good |
| P4 | 72.5 | Good |
| P5 | 55.0 | OK |
| **Mean** | **69.5** | **OK — approaching Good** |

### Sprint-specific question results
Q3 — "I understood the AI urgency score": Mean 3.4 / 5 — below threshold
Q4 — "I would use this in place of my current workflow": Mean 4.0 / 5 — positive signal

### Interpretation
Usability is adequate but not strong. The urgency score explanation is the clearest pain point — aligns with qualitative observation that P2, P3, P4 all asked "what does 78 mean?" during tasks. Assignment workflow appeal is strong — P4 specifically noted "this is faster than phoning the site."
```

## Watch-outs

- **Administering SUS before tasks:** SUS measures the overall experience. Administering it before the participant has used the prototype produces invalid scores.
- **Explaining SUS items:** "What does 'unnecessarily complex' mean?" — do not answer this. The validated instrument depends on each participant interpreting it independently. Say: "Just go with your first instinct."
- **Treating n=5 SUS scores as statistically significant:** With 5 participants, SUS scores are directional signals, not statistically robust measurements. A mean of 69.5 means "probably in the OK-to-Good range" — not "exactly 69.5 on a valid scale."
- **Ignoring the open-ended question:** The final free-text question often produces the single most valuable qualitative data point of the survey. Don't omit it; read it carefully in synthesis.
- **Using SUS score without qualitative context:** A low SUS score with no qualitative notes tells you there's a problem but not what or where. Always read SUS alongside task observations.

## Agent facilitation guide

When analysing post-test survey data:
1. Calculate SUS score for each participant (if using full SUS): apply odd/even scoring formula; multiply by 2.5
2. Calculate mean SUS; compare to benchmarks; state interpretation
3. For custom sprint items: calculate mean per item; flag any item with mean ≤ 3.0 as a concern
4. Cross-reference: map low-scoring survey items to qualitative observations from the same session — do they confirm each other?
5. Note sample size caveat: n=5 produces directional signals, not statistically significant findings
6. Output: score table + mean + benchmark interpretation + 1–2 sentence summary linking to qualitative patterns

## Connects to

- [Five-Act Interview](../five-act-interview/SKILL.md) — survey runs at end of Act 4 or start of Act 5 debrief
- [Usability Metrics](../usability-metrics/SKILL.md) — SUS complements task completion rate and error rate; together they triangulate usability
- [Desirability Testing](../desirability-testing/SKILL.md) — SUS measures ease-of-use; desirability testing measures emotional appeal
- [Synthesis](../research-synthesis/SKILL.md) — SUS scores are one input to the synthesis session alongside qualitative patterns
