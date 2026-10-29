---
name: recruit-and-schedule
title: Recruit and schedule the right test participants
description: Find and schedule five test participants before the sprint ends — the right users, confirmed, with logistics handled, ready for Validate day. Use when starting Day 3 or 4 of the sprint, in parallel with the storyboard and prototype build, or for any research session that requires real users (not surrogates or internal stand-ins).
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Starting Day 3 or 4 of the sprint — participant recruitment has a lead time
  - In parallel with the storyboard and prototype build — the Interviewer's Day 4 job
  - For any research session that requires real users (not surrogates or internal stand-ins)
  - When the sprint has identified a specific persona (e.g., the Lead Coordinator) whose real-world counterparts must be tested
applies-to: participant logistics, research ops, interview preparation, validate day readiness, user access planning
done_when:
  - Participants match the target persona/screener
  - 5× sessions are scheduled with buffers
  - Logistics (consent, incentive, tooling) are confirmed
metadata:
  duration: 2–3 hours total (can run in parallel with prototype build on Day 4)
  team-size: 1–2 people (recruiter role; often the Interviewer from Prototype day)
  sprint-phase: 6 Validate
---

# Recruit and Schedule

**TL;DR:** Without participants, there is no Validate day. Recruiting and scheduling five test participants is a logistical method that runs in parallel with the prototype build — typically on Day 4. It's often underestimated as "just sending calendar invites." Done well, it ensures that the five participants who arrive on Day 5 are the right users, in the right context, properly briefed, and protected by appropriate consent. Done poorly, it produces a validate day with no-shows, wrong users, or last-minute cancellations.

## When to use

- Starting Day 3 or 4 of the sprint — participant recruitment has a lead time
- In parallel with the storyboard and prototype build — the Interviewer's Day 4 job
- For any research session that requires real users (not surrogates or internal stand-ins)
- When the sprint has identified a specific persona (e.g., the Lead Coordinator) whose real-world counterparts must be tested

## Five participant rule

Five is the target. This number comes from research on diminishing returns in qualitative usability testing: five participants surface ~85% of the patterns a larger study would find. With fewer than five, patterns are unreliable — findings from 3 participants can be overturned by a fourth. With more than five in a single sprint day, observation fatigue degrades the team's synthesis quality.

| Number of participants | Risk |
|---|---|
| 1–2 | Cannot distinguish pattern from individual quirk; high noise |
| 3–4 | Directional only; not sufficient for a build decision |
| **5** | Target: sufficient to identify patterns, manageable in one day |
| 6–7 | Buffer for no-shows; run 5, have 6–7 scheduled |
| 8+ | Too many for one day; split across two days or narrow scope |

**Always recruit 6–7 to guarantee 5 show up.** No-show rate in user research is typically 15–25%.

## Who to recruit

Participants must match the primary persona. Recruiting the wrong users is worse than recruiting fewer — wrong-user sessions produce invalid findings that can mislead the build decision.

### Screener criteria

Write a screener before reaching out to anyone:

```markdown
## Participant Screener — [Sprint Name] · [Date]

**Target persona:** the Lead Coordinator archetype, or an equivalent role

**Required criteria (all must be true):**
- [ ] Works in a service organization that triages incoming requests, in a coordination or scheduling role
- [ ] Uses a triage or scheduling tool professionally (a request-management system, a shared specialist calendar, or equivalent)
- [ ] Has decision authority or direct input on request priority or specialist assignment
- [ ] Available for 60 minutes on [Date] between 9am and 4pm

**Disqualifying criteria (any one = no):**
- Works for a direct competitor of the product being tested
- Has previously participated in a sprint or usability test for this product
- Is a friend or family member of any sprint team member

**Ideal:** Current or former coordinator or lead coordinator with 2–5 years experience.
**Acceptable:** Adjacent roles (scheduling manager, help-desk lead, customer care lead) with request triage in their workflow.
```

### Where to find participants

| Source | Speed | Quality | Notes |
|---|---|---|---|
| **Product's existing user base** | Fast | High | Best match; requires CRM or CS access |
| **Sprint Decider's network** | Fast | High | Decider often knows exactly who to call |
| **Sales pipeline (prospects)** | Medium | Medium | Motivated but not yet users; consent considerations |
| **Professional-network outreach** | Slow | Medium | Good for B2B; requires personalised message |
| **Research recruitment agency** | Slow | Variable | Useful if internal access is blocked |
| **Internal surrogates** | Immediate | Low | Use only as last resort; primes responses |

## The participant brief

Every participant receives a brief confirming:
1. What the session involves ("You'll be looking at an early version of a product and sharing your reactions — no preparation required")
2. Time and location (or video link)
3. Recording consent if sessions will be recorded
4. NDA if the product is confidential
5. Incentive (if applicable)

Template:
```
Subject: User research session — [Date, Time] — [Sprint topic]

Hi [Name],

We'd love to get your input on something we're working on. The session is 60 minutes — you'll be looking at an early prototype and sharing your reactions. No preparation needed.

Details:
- Date: [Date]
- Time: [Start time] – [End time]
- Format: [In person at / Video call via]
- Incentive: [If applicable]

This will be recorded for our internal team's review only. A brief consent form will be sent before the session.

Please reply to confirm or suggest an alternative time if this doesn't work.

[Name]
```

## Day 4 recruit-and-schedule checklist

```
Sprint Day 4 — Recruit and Schedule tasks (Interviewer role)

□ Screener written and agreed with Decider/Facilitator
□ 6–7 candidates identified (internal CRM + Decider network)
□ Outreach sent to all candidates by 10am Day 4
□ Confirmations received for ≥5 participants by 3pm Day 4
□ Calendar invites sent to all confirmed participants
□ Participant brief sent (session details + consent form)
□ Video call links set up if remote (one per session slot)
□ Incentives arranged (gift card, voucher, etc.)
□ Prototype access link / location confirmed for Day 5
□ Day 5 session schedule distributed to full sprint team
□ Backup participant identified (in case of Day 5 no-show)
```

## Day 5 session schedule template

```markdown
## Validate Day — Session Schedule · [Date]

| Time | Participant | Role/Company | Notes |
|---|---|---|---|
| 09:00–10:00 | P1 — [Name] | Lead Coordinator, [Company] | Primary persona; highest priority |
| 10:15–11:15 | P2 — [Name] | Scheduling Manager, [Company] | Adjacent persona; watch for different mental model |
| 11:30–12:30 | P3 — [Name] | Coordinator, [Company] | Junior — note differences vs. senior |
| 13:30–14:30 | P4 — [Name] | Facilities Help-desk Lead, [Company] | Facilities context; different but valid |
| 14:45–15:45 | P5 — [Name] | Lead Coordinator, [Company] | Most similar to primary persona |
| [Backup] | P6 — [Name] | [Role] | Contact if P2 cancels |

**Session room / video link:** [Location or URL]
**Observation channel:** [Team chat channel / video side channel for team notes]
**Interviewer:** [Name]
**Note lead rotation:** P1=[Name], P2=[Name], P3=[Name], P4=[Name], P5=[Name]
```

## Agent facilitation guide

When supporting participant recruitment for a sprint:
1. Write the screener based on the sprint's primary persona (required and disqualifying criteria)
2. Suggest 3 recruitment channels specific to the product domain
3. Draft the participant outreach email (personalised, non-technical language)
4. Generate the Day 5 session schedule with 15-minute buffers
5. Flag the no-show risk if fewer than 6 participants are confirmed — recommend a backup

## Watch-outs

- **Starting recruitment on Day 5 morning:** "We'll find people tomorrow" is a guarantee of a failed validate day. Recruitment starts on Day 3 or 4 at the latest.
- **Internal substitutes:** Using colleagues or internal stakeholders as test participants produces systematically biased results — they know too much about the product, the company, and the design thinking behind it. Reserve for prototypes where real users are genuinely inaccessible.
- **Wrong persona:** "We could only get specialists, not coordinators" — a participant mismatch invalidates the findings for the sprint's primary persona. Better to delay the session than to test with wrong users.
- **No consent form:** Recording sessions without consent is a legal and trust risk. Send consent materials before Day 5, not in the lobby.
- **Forgetting incentives:** Participants who took an hour out of their day deserve acknowledgment. Even a small token (£25 voucher, charitable donation in their name) is meaningful and improves completion rate for future sprints.

## Connects to

- [Five-Act Interview](../five-act-interview/SKILL.md) — recruitment feeds directly into the interview session
- [Persona](../persona/SKILL.md) — screener criteria derive from the primary persona
- [Target](../sprint-target/SKILL.md) — Sprint Target defines which user type to recruit
- [Team Observation](../team-observation/SKILL.md) — confirmed participant schedule drives the observation room setup
