---
name: research-review
title: Synthesise existing research before the sprint
description: Synthesise existing research — reports, prior studies, usage data — before the sprint starts, so the team builds on what's already known. Use before the sprint starts. Use when the team has conducted prior user research, usability studies, or surveys relevant to the sprint topic, or when the Decider or stakeholders have specific claims about user behaviour that need to be validated or surfaced.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Before the sprint starts — the Research Review is prepared by the facilitator or researcher in the days before Day 1
  - When the team has conducted prior user research, usability studies, or surveys relevant to the sprint topic
  - When the Decider or stakeholders have specific claims about user behaviour that need to be validated or surfaced
  - When different team members have seen different research and may hold conflicting mental models
  - Whenever "we did a study on this last year" is said during the sprint — surface it before it becomes a sidebar
applies-to: research synthesis, prior study integration, evidence baseline, assumption reduction, sprint preparation
done_when:
  - Existing research is summarised into what we know vs don’t know
  - “What we don’t know” entries become top-tier assumptions
  - Findings carry evidence tags and source citations
metadata:
  duration: 30–60 min (prep before sprint day 1) + 15 min team walkthrough
  team-size: 1–2 researchers/analysts pre-sprint; full team for walkthrough
  sprint-phase: 1 Understand
---

# Research Review

**TL;DR:** The sprint team rarely starts from zero. There are prior studies, customer feedback logs, support tickets, NPS data, usage analytics, and competitive analyses — often scattered across people, folders, and formats. A Research Review gathers the best of that existing knowledge into a one-page synthesis that the sprint team reads before Lightning Talks begin. It reduces the time spent rediscovering what's already known and focuses the sprint on the real unknowns.

## When to use

- Before the sprint starts — the Research Review is prepared by the facilitator or researcher in the days before Day 1
- When the team has conducted prior user research, usability studies, or surveys relevant to the sprint topic
- When the Decider or stakeholders have specific claims about user behaviour that need to be validated or surfaced
- When different team members have seen different research and may hold conflicting mental models
- Whenever "we did a study on this last year" is said during the sprint — surface it before it becomes a sidebar

## What counts as research for this review

| Source type | Use | Caution |
|---|---|---|
| **Direct observation notes** | Highest value — what users actually did | May be dated; check sample size |
| **Moderated usability tests** | Strong — observed behaviour in structured context | Context may differ from sprint's context |
| **User interviews** | Strong — direct reported experience | Self-report bias; validate with observed behaviour |
| **Survey data** | Useful for scale — how many users affected | Check question framing for leading bias |
| **Usage analytics / funnel data** | Objective but context-free | Shows what, not why |
| **Support tickets / NPS verbatims** | Rich in pain signal | Selection bias — only people with strong feelings respond |
| **Previous sprint findings** | Very relevant — learnings from prior validate sessions | Check if product has changed since |
| **Competitive analysis** | Provides analogous landscape | Doesn't substitute for primary user research |

## Research Review one-pager format

```markdown
## Research Review — [Sprint Topic] · Prepared by [Name] · [Date]

### What we already know (observed / reported)

| Finding | Source | Date | Evidence type | Still relevant? |
|---|---|---|---|---|
| The Lead Coordinator spends 40 min every morning on manual request triage | 2026-02-17-coordinator-deepdive | Feb 2026 | Observed | Yes |
| Coordinators open 2–4 other systems per request to cross-reference | Usability study, booking inbox pilot | Jan 2026 | Observed | Yes |
| 63% of specialists report a wrong or incomplete request assignment ≥1x/week | Q1 specialist pulse survey (n=47) | Feb 2026 | Reported | Yes |
| Users with call-centre experience learn the booking inbox faster | Onboarding research | Nov 2025 | Reported | Probably (check if inbox changed) |

### What we thought we knew but should re-examine

| Prior belief | Source | Reason to revisit |
|---|---|---|
| "Coordinators want AI to set priorities automatically" | PM assumption | No user research supports this — may be wishful thinking |
| "Mobile access is a priority" | Stakeholder request | Only 2/12 users in prior study accessed on mobile |

### Key gaps — what we don't know yet

1. What is the coordinator's actual mis-prioritisation rate vs. the AI ranking's error rate? (Prototype test can surface this)
2. Would coordinators trust the suggested priority if its reasons were shown? (Core sprint assumption)
3. Does assignment friction vary by coordinator seniority? (May need secondary research)

### Research sources consulted
- [coordinator-deepdive 2026-02-17] — contextual interview, Lead Coordinator, 90 min
- [booking inbox pilot usability study Jan 2026] — 6 participants, moderated sessions
- [Q1 specialist pulse survey] — 47 respondents, 12 questions
- [Onboarding research Nov 2025] — 12 new booking-inbox users (coordination and customer care), 2-week diary study
```

## Steps

**Pre-sprint (researcher/facilitator):**
1. Collect all relevant prior research — interviews, studies, analytics, surveys
2. Extract findings that directly relate to the sprint topic and the primary persona
3. Categorise by evidence type (`observed`, `reported`, `assumed`) and recency
4. Flag findings that need revisiting (old data, small sample, or contradicting other findings)
5. Note explicit gaps — what the team doesn't know that the sprint should address
6. Produce the one-pager; share with the Decider and Facilitator before Day 1

**Sprint Day 1 (full team walkthrough, 15 min):**
1. Facilitator shares the Research Review one-pager (posted on wall or shared screen)
2. Team reads silently (3 min)
3. Facilitator highlights 2–3 key findings and 1–2 gaps
4. Team asks clarifying questions (not debate — fact-finding)
5. Any team member who has additional research not in the review adds it now

## When there is no prior research

If the team has no existing research on the sprint topic, acknowledge this explicitly:
- Document it as a "starting from zero" assumption
- Increase the weight placed on Lightning Talks and Expert Interviews
- Set the expectation that Sprint Questions will be more hypothetical — the Validate phase will be the first real data point

A sprint can start without prior research. It cannot start *pretending* to have prior research that doesn't exist.

## Agent facilitation guide

When synthesising research for a sprint:
1. List all available research sources (ask the team: "what have we already studied about this?")
2. For each source: extract the 1–2 most relevant findings for the sprint topic
3. Tag each finding with evidence type and date
4. Identify 2–3 findings that the team may be taking for granted but which are actually `assumed`
5. List the top 3 gaps — what the team would most benefit from learning in the sprint
6. Generate the Research Review one-pager in the format above

## Watch-outs

- **Research Review becomes a presentation:** The purpose is a shared baseline, not a detailed replay of every study. Keep it to one page. Depth goes in the appendix, not the wall.
- **Only including research that confirms the team's direction:** A Research Review that omits contradicting findings isn't a review — it's advocacy. Include the inconvenient data.
- **Old research treated as current:** A usability study from 18 months ago on a product that's changed significantly is not strong evidence. Flag date and note whether it's still valid.
- **Using it as a substitute for the sprint:** "We already know everything from our research" is a reason to skip ideation, not to skip the sprint. Research tells you about the problem; the sprint addresses the solution.
- **Skipping it because "everyone already knows this":** Everyone has a different slice of the data. The Research Review creates shared facts, which is different from everyone assuming they know the facts.

## Connects to

- [Lightning Talks](../lightning-talks/SKILL.md) — prior research supplements expert talks; gaps in research direct talk topics
- [Expert Interviews](../expert-interviews/SKILL.md) — interview questions target the gaps identified in the Research Review
- [Assumption Mapping](../assumption-mapping/SKILL.md) — "what we don't know" entries become the top-tier assumptions
- [Persona](../persona/SKILL.md) — persona attributes are grounded in Research Review findings
- [`evidence-tagging`](../evidence-tagging/SKILL.md) — evidence tagging rules apply throughout the Research Review
