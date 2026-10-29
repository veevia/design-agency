---
name: persona
title: Build an evidence-grounded user profile
description: Synthesise what's known about a specific user into a named, evidence-grounded profile that the team can design for throughout the sprint. Use after Lightning Talks and Expert Interviews, once the team has enough research to characterise users, before User Journey Mapping. Use when the sprint team includes members who have never met the users directly.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - After Lightning Talks and Expert Interviews, once the team has enough research to characterise users
  - Before User Journey Mapping — the persona is the subject of the journey
  - When the sprint team includes members who have never met the users directly
  - When different team members have different mental models of "who the user is"
  - Before the Sprint Target selection — the Target names which persona × which moment the sprint will focus on
applies-to: user alignment, design target definition, assumption surfacing, sprint target selection, design critique reference
done_when:
  - The persona is grounded in cited research, not invented attributes
  - Primary vs secondary personas are distinguished
  - Assumed attributes are tagged for validation
metadata:
  duration: 20–30 min (collaborative build); 10 min (agent-generated draft for team review)
  team-size: Full sprint team; one persona per primary user type
  sprint-phase: 1 Understand
  redirect-host: canonical-artifacts
---

# Persona

**TL;DR:** A sprint Persona is not a marketing demographic profile. It's a focused, evidence-grounded description of one specific type of user — built collaboratively from research — that the team uses as a concrete design target throughout the sprint. The Persona answers: *who exactly are we designing for, and what do we know about them that should shape every decision?*

Sprint personas are lean: one page, no stock photography, grounded in observed behaviour. They're updated if they're wrong.

## When to use

- After Lightning Talks and Expert Interviews, once the team has enough research to characterise users
- Before User Journey Mapping — the persona is the subject of the journey
- When the sprint team includes members who have never met the users directly
- When different team members have different mental models of "who the user is"
- Before the Sprint Target selection — the Target names which persona × which moment the sprint will focus on

## Lean persona structure

A sprint persona has six fields only. No fictional names for B2B users — use the real role and real observed attributes.

```
## Persona — [Name and Role]

**Who they are:**
[Role, context, team size, relevant background — 2 sentences]

**Primary job:**
[Their main professional responsibility in 1 sentence — JTBD framing preferred]

**How they interact with this problem:**
[What do they actually do today? What tools? What workarounds? Observable behaviour only.]

**Goals in this context:**
[What does success look like to them in this specific workflow?]

**Frustrations:**
[Top 2–3 pain points, grounded in observed or reported evidence]

**What they won't tell you directly:**
[The hidden constraint, the workaround they're embarrassed about, the fear they downplay in interviews]

**Evidence quality:** [observed | reported | assumed] per key claim
```

## Two types: primary and secondary

| Type | Description | Sprint implication |
|---|---|---|
| **Primary persona** | The user the sprint is designing for; the one who will be in the prototype test session | Sprint Target names their specific journey moment |
| **Secondary persona** | A user who is affected by the solution but is not the test participant | Considered in constraints; not the design driver |

A sprint should have one primary persona. If the team names two "primaries," that's a signal that the sprint scope is too broad.

## Steps

1. **Name the candidate users (3 min):** Who did the team hear about in Lightning Talks and Expert Interviews? Write each user type on a sticky note. Post on the wall.

2. **Select the primary persona for this sprint (5 min):** Note-and-Vote or Decider call. Which user is most central to the Long-Term Goal? Who would be most affected by success or failure of the solution?

3. **Build the persona collaboratively (15 min):** Fill in the six fields as a group. For each field, team members contribute what they observed or heard in research. Write on stickies, post on the persona template.

4. **Tag evidence quality (3 min):** Go through each claim. Is it `observed` (we saw this behaviour directly)? `reported` (user told us in an interview)? `assumed` (we believe this based on inference)? Mark each.

5. **Name the open questions (2 min):** What would the team need to know about this persona that they currently don't? These become sprint test questions.

## Worked example (generic)

```markdown
## Persona — Lead Coordinator

**Who they are:**
Lead Coordinator at an organization with three regional sites (Site A, Site B, Site C). Responsible for the morning assignment round — sorting overnight service requests and assigning each one to a specialist before the 8am start. Leads a team of 4 coordinators covering about 60 specialists.

**Primary job:**
Ensure that urgent requests (outage, safety risk) are identified, prioritised, and assigned to the right specialist — with the right parts — before the 8am start each morning. [observed | 2026-02-17-coordinator-deepdive]

**How they interact with this problem:**
Reviews an unsorted booking inbox every morning (currently: 35–50 overnight requests from the web form, phone line, and partner channel). Checks unclear requests by hand against the CRM, the service-contract database, and the inventory system. Assigns requests to specialists via a 7-step manual process in the specialist calendar. Maintains a personal tracking spreadsheet in parallel. [observed]

**Goals in this context:**
No urgent request should still be unassigned at the 8am start. Each request should reach the right specialist, with the right parts, the first time. Their standing with the sites depends on both. [reported | interview notes]

**Frustrations:**
1. Manual triage is too slow — 40 min per morning, no progress toward reducing it [observed]
2. Can't check a booking's details without leaving the inbox — opens 3–4 other systems per request [observed]
3. Assignment unreliability forces phone follow-ups with site supervisors [reported]

**What they won't tell you directly:**
They have low trust in the system's suggested priority but are reluctant to say so directly — they frame it as "wanting to understand the reasoning." The real concern is accountability: if they send a specialist to a routine request while an outage request waits, they own that miss. [assumed | inferred from behaviour patterns]

**Evidence quality:** Most claims observed or reported; the trust claim about suggested priority is assumed — needs prototype test.

**Open questions:**
- What is the coordinator's actual mis-prioritisation rate vs. the system's suggested priority?
- Would they act differently if they could see how the suggested priority is calculated?
- Do the other coordinators work the same way, or is their behaviour specific to their experience?
```

## Secondary persona note

If the sprint also affects other user types (e.g., the site supervisor who receives assigned requests), document them briefly:

```markdown
## Secondary persona — Site Supervisor (Site C)

Receives assigned requests from coordinators like the Lead Coordinator. Current experience: requests arrive by phone and text with inconsistent context. Needs: the request's urgency, the customer's history, and the parts it needs. Not the sprint test participant — but design decisions about assignment must work for them too.
```

## Agent facilitation guide

When generating a persona from sprint research:
1. Identify the primary user from Lightning Talk and Expert Interview notes
2. Extract observable behaviour (what they actually do) from `observed`-tagged claims
3. Extract stated goals and frustrations from `reported`-tagged claims
4. Flag any persona attribute that is inferred, not directly observed — tag as `assumed`
5. Generate the "won't tell you directly" field last — this is the most analytical claim and should be grounded in a contradiction between stated and observed behaviour
6. List 2–3 open questions that the sprint's prototype test should try to answer

## Watch-outs

- **Too many personas:** If the team builds 4 personas and labels them all "primary," the sprint has no focus. One primary persona, named, with a specific scenario.
- **Fictional vs. real:** For B2B enterprise products, real roles and real organisations are more useful than fictional names and composite demographics.
- **Aspirational persona:** "The coordinator wants a seamless, AI-powered experience" is not observed behaviour. Strip aspirations and describe what people actually do today.
- **Persona without evidence tags:** A persona where every claim is unmarked slides into assumption by default. Tagging forces the team to confront what they don't know.
- **Persona as decoration:** A persona posted on the wall but never referenced during Sprint Questions, Target selection, or Speed Critique is decoration. The facilitator should reference the persona explicitly: "Does this concept help the Lead Coordinator with the morning triage?"

## Connects to

- [Expert Interviews](../expert-interviews/SKILL.md) — primary source for observed and reported persona attributes
- [Empathy Map](../empathy-map/SKILL.md) — the emotional layer that deepens the persona's THINKS and FEELS
- [User Journey Map](../user-journey-map/SKILL.md) — the persona is the subject of the journey
- [Target](../sprint-target/SKILL.md) — Sprint Target names the persona + the specific moment
- [Assumption Mapping](../assumption-mapping/SKILL.md) — `assumed` persona attributes become sprint assumptions
