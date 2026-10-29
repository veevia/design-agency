---
name: heuristic-evaluation
title: Audit a UI against usability heuristics
description: Evaluate the prototype against the 10 usability heuristics — a structured expert review that surfaces systematic design problems before user testing exposes them. Use when time allows a quality gate before Day 6 participant sessions, or when the team includes a UX evaluator who wasn't involved in building the prototype.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - When time allows a quality gate before Day 6 participant sessions
  - When the team includes a UX evaluator who wasn't involved in building the prototype
  - When the prototype covers a complex flow (multi-step assignment, dashboard with multiple data layers) where system-level inconsistencies are likely
  - As a complement to Prototype Review — review catches broken links; heuristic evaluation catches design reasoning failures
  - When testing with users is high-stakes and the team wants to eliminate knowable problems before consuming participant sessions
applies-to: usability problem identification, expert review, pre-participant quality gate, interface standards compliance, systematic design critique
done_when:
  - The UI is scored against each heuristic
  - Each violation is rated by severity
  - Fixes are prioritised by severity × effort
metadata:
  duration: 45–60 min (1–2 evaluators working independently, then comparing notes)
  team-size: 1–2 evaluators with UX or product expertise; not the prototype builders
  sprint-phase: 6 Validate
---

# Heuristic Evaluation

**TL;DR:** A heuristic evaluation is an expert review of the prototype against a set of established usability principles. One or two evaluators work independently through the prototype, noting every violation of the 10 usability heuristics. They then compare notes, deduplicate, and rate each issue by severity. The output is a prioritised problem list — ready before the first participant arrives. Heuristic evaluation finds the systematic, predictable usability failures quickly; it complements user testing but does not replace it (experts miss context-specific problems that real users surface).

## When to use

- When time allows a quality gate before Day 6 participant sessions
- When the team includes a UX evaluator who wasn't involved in building the prototype
- When the prototype covers a complex flow (multi-step assignment, dashboard with multiple data layers) where system-level inconsistencies are likely
- As a complement to Prototype Review — review catches broken links; heuristic evaluation catches design reasoning failures
- When testing with users is high-stakes and the team wants to eliminate knowable problems before consuming participant sessions

## The 10 usability heuristics (sprint-adapted)

| # | Heuristic | Sprint-specific check |
|---|---|---|
| 1 | **Visibility of system status** | Does the interface show what it's doing? (AI loading, assignment in progress, priority status) |
| 2 | **Match between system and real world** | Does the vocabulary match the user's vocabulary? (coordinator terminology, not developer labels) |
| 3 | **User control and freedom** | Can the user undo, cancel, or go back from any point without losing progress? |
| 4 | **Consistency and standards** | Are the same actions labelled and positioned consistently across all screens? |
| 5 | **Error prevention** | Does the design prevent mistakes before they happen? (e.g., assignment confirmation before irreversible action) |
| 6 | **Recognition rather than recall** | Can the user act without having to remember information from a previous screen? |
| 7 | **Flexibility and efficiency** | Are there shortcuts for experienced users? (keyboard shortcuts, batch assignment, filter presets) |
| 8 | **Aesthetic and minimalist design** | Is every element earning its screen space? Any irrelevant information competing with critical data? |
| 9 | **Help users recognise, diagnose, and recover from errors** | Are error messages specific, in plain language, and actionable? |
| 10 | **Help and documentation** | Is any task complex enough to require in-context guidance? Is it provided? |

## Severity rating scale

| Rating | Description | Sprint action |
|---|---|---|
| **0** | Not a usability problem | No action |
| **1** | Cosmetic — fix only if time allows | Backlog |
| **2** | Minor — low priority fix | Fix after Day 6 |
| **3** | Major — important to fix | Fix before Day 6 if possible |
| **4** | Catastrophic — must fix before testing | Fix immediately |

## Evaluation output format

```markdown
## Heuristic Evaluation — [Sprint Name] · [Prototype Version] · [Date]

### Evaluator: [Name]

| # | Screen | Heuristic | Violation | Severity |
|---|---|---|---|---|
| 1 | Request Detail | H1 — Visibility | No loading indicator while the AI ranking runs. User has no feedback for 2–3 seconds. | 3 |
| 2 | Request Queue | H4 — Consistency | "Assign" button is primary blue on Request Queue but secondary grey on Request Detail. Inconsistent affordance. | 3 |
| 3 | Assignment Form | H5 — Error prevention | No confirmation before assignment is final. Assignment notifies the specialist immediately; one-click submit is dangerous. | 4 |
| 4 | Request Detail | H2 — Real-world match | "Suggested priority" label — coordinators call this "the triage call" in interviews. Terminology mismatch. | 2 |
| 5 | Assignment Confirmation | H3 — Control and freedom | No "undo assignment" or "revise" option. User is locked in once confirmation appears. | 3 |
| 6 | Request Queue | H8 — Minimalism | 4 filter tabs visible at once; user likely only uses "Unconfirmed" in daily flow. 3 tabs compete for attention. | 1 |

### Summary
Catastrophic (severity 4): 1 issue — fix before Day 6
Major (severity 3): 3 issues — fix if time permits
Minor (severity 2): 1 issue — backlog
Cosmetic (severity 1): 1 issue — ignore for sprint
```

## How to run the evaluation

1. **Brief the evaluator (5 min):** Give them the scenario card, the persona, and the task they're evaluating against. They should know *who* is using this and *what they're trying to do* — heuristic evaluation in a vacuum produces generic findings.

2. **Independent walk-through (20–30 min):** Evaluator navigates the prototype alone, noting every violation as they encounter it. No discussion with the team.

3. **Second evaluator (optional, 20–30 min):** If a second evaluator is available, they do the same independently. Research shows 2 evaluators catch ~70% of problems; 3–5 evaluators approach 80%.

4. **Deduplication and severity rating (15 min):** If two evaluators: compare notes, merge duplicates, agree on severity ratings.

5. **Fix triage (10 min):** Facilitator reviews the output. Severity-4 issues are fixed before Day 6. Severity-3 issues are fixed if time allows. Everything else is noted for post-sprint iteration.

## Watch-outs

- **Evaluator who built the prototype:** The builders know the intended behaviour and unconsciously navigate around the problems. Use someone who hasn't touched the prototype.
- **Heuristic evaluation replacing user testing:** Expert evaluators reliably find system-level consistency issues; they are poor predictors of task completion problems, vocabulary confusion, and emotional reactions. Heuristic evaluation is a complement to user testing, not a substitute.
- **Severity inflation:** If every issue is rated severity 3 or 4, the team will try to fix everything and won't finish. Push evaluators to reserve severity 4 for issues that would prevent task completion; reserve severity 3 for issues that would cause significant difficulty.
- **Fixing everything before testing:** Prototype day is over — the team is tired. Only catastrophic issues justify significant rework. Don't rebuild screens to address severity-1 or severity-2 findings before Day 6.

## Agent facilitation guide

When conducting a heuristic evaluation:
1. Receive the storyboard scenario and prototype flow description
2. Walk through each screen against all 10 heuristics — generate one row per violation
3. Rate each violation using the 0–4 severity scale; err toward lower severity for sprint context
4. Flag any severity-4 violations with a specific fix recommendation (actionable for the Stitcher)
5. Output as a table: screen, heuristic number, violation description, severity
6. Summarise: count per severity level; recommend which to fix before Day 6

## Connects to

- [Prototype Review](../prototype-review/SKILL.md) — prototype review checks mechanical correctness; heuristic evaluation checks design reasoning
- [Design Criteria](../design-criteria/SKILL.md) — design criteria define what "correct" looks like; heuristics define universal usability standards
- [Five-Act Interview](../five-act-interview/SKILL.md) — heuristic evaluation informs which tasks to prioritise in the interview; severity-4 issues often map to the critical task
- [Usability Metrics](../usability-metrics/SKILL.md) — heuristic issues map to predicted task failure points; compare predictions to observed metrics
