---
name: jobs-to-be-done
title: Frame the job a user is hiring the product for
description: Understand what job a user is really hiring the product to do — the functional, emotional, and social progress they are trying to make. Use when early in Phase 1, before or alongside Expert Interviews, when the team is debating features without agreement on the underlying user motivation, or when prior research exists but the team can't agree on "what the user really wants".
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Early in Phase 1, before or alongside Expert Interviews — JTBD frames the research questions
  - When the team is debating features without agreement on the underlying user motivation
  - When prior research exists but the team can't agree on "what the user really wants"
  - When a sprint question involves whether a solution will be adopted (adoption is always a jobs question)
  - "As the anchor for Sprint Questions: \"Can users hire this to do [job]?\""
applies-to: user motivation, product strategy, outcome framing, HMW generation, sprint question anchoring
done_when:
  - Each job is written as “When [situation], I want [motivation], so I can [outcome]”
  - Functional, emotional, and social dimensions are distinguished
  - The primary job for the in-scope user is identified
metadata:
  duration: 30–45 min per canvas; 90 min for team synthesis
  team-size: 1–2 researchers; full team for review
  sprint-phase: 1 Understand
  redirect-host: canonical-artifacts
---

# Jobs-to-be-Done (JTBD)

**TL;DR:** Jobs-to-be-Done reframes user understanding away from demographics and toward motivation: not "who is this user?" but "what progress are they trying to make?" A "job" is a specific outcome a person wants to achieve in a given situation — functional (get every urgent request assigned before the 8am start), emotional (feel confident I haven't missed anything), and social (be recognised as the coordinator who catches what others miss). When the team understands the job, they can evaluate concepts by asking: does this help the user make that progress?

## When to use

- Early in Phase 1, before or alongside Expert Interviews — JTBD frames the research questions
- When the team is debating features without agreement on the underlying user motivation
- When prior research exists but the team can't agree on "what the user really wants"
- When a sprint question involves whether a solution will be adopted (adoption is always a jobs question)
- As the anchor for Sprint Questions: "Can users hire this to do [job]?"

## The JTBD formula

> **When** [situation], **I want to** [motivation / job], **so I can** [expected outcome].

The job is the middle clause. The situation is the trigger. The outcome is the measure of success.

Example:
> "When I'm sorting the overnight requests before the 8am start, I want to quickly spot which requests are urgent and assign them to the right specialist, so I can release the day's assignments confident that nothing urgent was missed."

## Three layers of every job

| Layer | Question | Example |
|---|---|---|
| **Functional** | What task are they trying to complete? | Sort 38 overnight requests and assign the 3 urgent ones before 8am |
| **Emotional** | How do they want to feel? | Confident, not anxious about missing an urgent request |
| **Social** | How do they want to be perceived? | Recognised as thorough and reliable by their manager |

All three layers matter. Functional jobs are easier to see; emotional and social jobs are more powerful drivers of adoption.

## The JTBD canvas

```markdown
## JTBD Canvas — [User Name / Role] · [Context] · [Date]

### The job
When [situation trigger]:
"When I arrive at my desk and open the booking inbox for the morning sort..."

I want to:
"...quickly see which requests are urgent and get them to the right specialist..."

So I can:
"...be confident the day starts at 8am with nothing urgent missed."

### Job layers
**Functional:** [What task must be completed]
**Emotional:** [Desired feeling at completion]
**Social:** [Desired perception by others]

### Current solution (how they do this job today)
[Tool / workaround / process they use now — observed behaviour]

### Job struggles (where the current solution fails)
1. [Struggle 1 — specific pain in doing the job today]
2. [Struggle 2]
3. [Struggle 3]

### Desired outcomes (how they'd measure success)
1. [Outcome 1 — specific, measurable if possible]
2. [Outcome 2]
3. [Outcome 3]

### Switch triggers (what would make them adopt something new)
[What condition would make them change their current behaviour?]

### Evidence quality
[ ] Observed — derived from direct behaviour observation
[ ] Reported — user stated this directly in interview
[ ] Assumed — team inference; needs validation
```

## Identifying the right job to sprint on

Teams often surface multiple competing jobs for the same user. Use these filters to select the sprint-worthy job:

| Filter | Question |
|---|---|
| **Frequency** | How often does this job occur? (Daily jobs are higher priority than annual ones) |
| **Pain intensity** | How frustrated are users when the current solution fails? |
| **Switching potential** | Would users change tools/behaviour if a better solution existed? |
| **Business relevance** | Does solving this job serve the team's Long-Term Goal? |
| **Testability** | Can a prototype surface whether a concept does this job better? |

## Example — Lead Coordinator

```markdown
## JTBD Canvas — Lead Coordinator · Morning Request Triage · 2026-02-17

### The job
When: I arrive at my desk and open the booking inbox with 35–50 overnight requests pending
I want to: quickly identify which requests are urgent, confirm their details, and assign them to the right specialist
So I can: release the day's assignments at 8am confident no urgent request was missed

### Job layers
Functional: Triage and assign 35–50 requests before the 8am start
Emotional: Feel confident, not anxious about gaps
Social: Be seen as thorough and reliable — the person who doesn't miss things

### Current solution
Opens the booking inbox → manually scans for urgent-sounding requests → opens 2–4 other systems per request (CRM, service-contract database, inventory system) to check details → updates personal tracking spreadsheet → manually assigns via 7-step process in the specialist calendar

### Job struggles
1. Checking details requires switching systems — no single request record inside the inbox
2. Assignment errors mean requests reach the wrong specialist; the coordinator follows up by phone
3. "Routine" queue is skipped on busy mornings — creates risk of a missed urgent request

### Desired outcomes
1. All urgent requests assigned before 8am (zero misses)
2. Assignment correct the first time — no follow-up call needed
3. Able to show why a request was prioritised if challenged — request history inside the tool

### Switch triggers
- If the tool showed customer, service-contract, and parts details inline, they'd stop opening other systems
- If the suggested priority showed its reasoning, they'd trust it enough to act without re-checking

### Evidence quality
[x] Observed — system-switching and spreadsheet use directly observed
[x] Reported — "I need to see why it's marked urgent" stated directly
[ ] Assumed — showing the reasoning would build trust (inference; needs prototype test)
```

## Agent facilitation guide

When generating a JTBD canvas from sprint research:
1. Identify the user and the specific context (situation trigger)
2. Write the job statement using the "When / I want to / So I can" formula
3. Derive the three layers from observed behaviour (functional), stated frustrations (emotional), and social context
4. List the current solution — the workaround or tool they use today
5. Extract struggles from pain points: where does the current solution fail to do the job?
6. Convert the struggles into desired outcomes (the positive flip side of each struggle)
7. Tag each entry with evidence type
8. Generate 2–3 HMW notes from the top struggles

## Watch-outs

- **Conflating job with feature:** "I want to see an urgency score" is a feature, not a job. Push back to the motivation: "Why does the score matter? What outcome does it help them reach?"
- **One-layer jobs:** A JTBD canvas that only has a functional layer will produce functional solutions. The emotional and social layers generate the ideas that create real differentiation.
- **Multiple users, one canvas:** Each distinct user has their own job. The Lead Coordinator's job (triage and assign) is different from the Site Supervisor's job (get an assigned request done right the first time). Separate canvases, not a combined one.
- **Using JTBD to justify a pre-decided solution:** JTBD should surface the job; the solution comes in Phase 3. If the canvas is being written backward from a feature the team has already decided to build, it's not useful.

## Connects to

- [Expert Interviews](../expert-interviews/SKILL.md) — interviews surface the job statement directly
- [Empathy Map](../empathy-map/SKILL.md) — emotional and social layers deepen the empathy map
- [Persona](../persona/SKILL.md) — JTBD enriches the persona's "primary job" field
- [Assumption Mapping](../assumption-mapping/SKILL.md) — assumed job layers become the highest-priority assumptions
- [Sprint Questions](../sprint-questions/SKILL.md) — sprint questions are framed around whether concepts can do the job
