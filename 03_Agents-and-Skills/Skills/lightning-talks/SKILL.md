---
name: lightning-talks
title: Run expert talks and capture HMWs in parallel
description: Structured short presentations by internal experts — each speaks for 10–20 minutes, team captures HMW notes in parallel. Use as the first activity on Day 1 of the sprint, before any ideation. Use when the sprint team includes people who don't share the same background on the problem space, or to surface competing definitions of the problem before the team commits to one framing.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - First activity on Day 1 of the sprint, before any ideation
  - When the sprint team includes people who don't share the same background on the problem space
  - To surface competing definitions of the problem before the team commits to one framing
  - When the Decider needs the team to hear directly from frontline experts, not summaries
applies-to: domain knowledge transfer, shared understanding, HMW note capture, sprint kickoff, expert alignment
done_when:
  - Each talk’s key facts are captured by the team
  - HMW notes are written in parallel during the talks
  - Open questions and worries are logged as assumptions
metadata:
  duration: 10–20 min per talk; 90–120 min total (4–6 talks)
  team-size: Full sprint team; one speaker at a time
  sprint-phase: 1 Understand
---

# Lightning Talks

**TL;DR:** Lightning Talks are the primary knowledge-transfer mechanism at the start of the sprint. Each expert — a customer success manager, an engineer, a researcher, a salesperson — gives a short, focused presentation to the full team. While they speak, the team listens and simultaneously captures "How Might We" notes. By the end of the morning, the team has a shared mental model of the problem space drawn from multiple perspectives.

## When to use

- First activity on Day 1 of the sprint, before any ideation
- When the sprint team includes people who don't share the same background on the problem space
- To surface competing definitions of the problem before the team commits to one framing
- When the Decider needs the team to hear directly from frontline experts, not summaries

## Difference from Expert Interviews

| Lightning Talk | Expert Interview |
|---|---|
| One speaker to full group | One interviewer + one expert, team observes |
| Speaker prepares a presentation | Interviewer follows a structured question guide |
| 10–20 min; presenter controls flow | 15–20 min; interviewer controls questions |
| Good for domain overviews, data sharing | Good for surfacing nuanced opinions, probing mental models |
| Multiple back-to-back in one morning | One or two per sprint, usually early |

Both often happen on the same day. Lightning Talks first; Expert Interviews after or alongside.

## Speaker selection

Invite 4–6 speakers who cover different angles of the problem:

| Speaker type | What they bring |
|---|---|
| **Business or product owner** | Strategic context; the "why now" |
| **Customer-facing role** (sales, support) | What users actually say; real friction points |
| **Technical lead** | What's feasible; where the hard constraints are |
| **User researcher** (if available) | Prior research findings; validated user needs |
| **External expert** (domain authority) | Industry context; what analogous products have tried |
| **Decider** | Their current mental model of the problem — useful to hear early |

## Materials

- 4–6 speakers briefed in advance (30-min prep call or written brief)
- Sticky notes and markers for HMW capture (one colour per person)
- Whiteboard or wall space for posting HMW notes (used in Affinity Map after talks)
- Timer visible to the speaker

## Briefing speakers in advance

Send each speaker a brief:
> "You have 15 minutes. Cover: (1) What do you know about [problem area]? (2) What have you tried? (3) What's surprised you? (4) What worries you? End with: what's the most important question we need to answer? No slides required — conversational is fine."

The goal is frank knowledge, not polished presentations.

## Steps

1. **Introduce the format (2 min):** Facilitator explains to the team: "While each speaker presents, write HMW notes. One idea per sticky. Capture anything that sparks an idea for how we might improve the user's experience."

2. **Speaker presents (10–20 min):** Speaker covers their angle. Facilitator keeps time and gives a 2-minute warning.

3. **Team captures HMW notes throughout (concurrent):** No verbal discussion during the talk. Team writes silently.

4. **Q&A (5 min):** Two or three quick clarifying questions from the team. Not a debate — fact-finding only. "Did you say the error rate is 40% or 4%?" not "Don't you think we should fix X first?"

5. **Transition (2 min):** Facilitator collects the speaker's top recommendation in one sentence: "If you could only fix one thing, what would it be?" Posts it on the wall.

6. **Repeat for next speaker.** Rotate every 15–25 min.

7. **After all talks:** Move directly to Affinity Mapping to cluster the HMW notes.

## What speakers should NOT do

- Present for 45+ minutes with dense slides
- Propose solutions ("we should build X") — solutions come in Phase 3
- Debate other speakers' claims — the team is gathering, not arbitrating
- Skip the "what worries you" section — the worries are often the most useful input

## Agent facilitation guide

When briefing a team on Lightning Talk logistics:
1. Review the sprint's Long-Term Goal and Sprint Questions (if already defined) — these become the implicit frame for all talks
2. Suggest 4–6 speaker slots with specific perspectives (match to the problem domain)
3. Draft the speaker brief template with 4 questions customized to the sprint topic
4. After the talks: produce a synthesis of "key claims per speaker" and "questions still open" — feeds directly into Assumption Mapping

Output:
```markdown
## Lightning Talk Debrief — [Sprint Name]

| Speaker | Role | Key claim | Key worry | Top question they raised |
|---|---|---|---|---|
| [Name] | Customer Care | "Coordinators abandon the assignment form at step 3 most often" | "We'll add more steps trying to fix it" | "What does 'a successful assignment' mean to the user?" |
| [Name] | Engineering | "The ranking API has a 15% error rate on edge cases" | "The urgency score will mislead users near the boundary" | "Should we surface uncertainty, not certainty?" |
| [Name] | Research | "The coordinator spends 40 min every morning on manual request triage" | "Tools won't replace judgment — and they know it" | "What's the minimum assist that earns trust?" |

**Themes across talks:**
- Trust in the suggested priority is the central tension across all speaker perspectives
- Assignment friction is high-pain but potentially the simpler fix
- No speaker addressed requests that need more than one site

**Open questions (feed into Assumption Mapping):**
- What does the coordinator's actual error rate look like vs. the AI ranking's error rate?
- Is step-3 abandonment a UX issue or a data quality issue?
```

## Watch-outs

- **One speaker going 45 minutes:** Lightning Talks are named for a reason. Politely interrupt at 20 minutes: "We need to move on, but let's capture your remaining points in the Q&A."
- **Team not writing HMW notes:** Some people listen passively. Set the expectation before the first talk: "Every person should have at least 3 stickies by the end of this talk."
- **Only inviting people who agree:** The most valuable Lightning Talk is the one that challenges the team's existing mental model. Include a skeptic or a frontline worker who hasn't been in the room for previous strategy discussions.
- **No Q&A time:** Five minutes per talk for clarifying questions dramatically improves the quality of HMW notes written afterward.

## Connects to

- [How Might We](../how-might-we/SKILL.md) — HMW notes are captured during Lightning Talks
- [Expert Interviews](../expert-interviews/SKILL.md) — deeper 1:1 follow-up with individual speakers
- [Affinity Map](../affinity-map/SKILL.md) — HMW notes from all talks are clustered immediately after
- [Assumption Mapping](../assumption-mapping/SKILL.md) — speaker "worries" and open questions become assumptions
