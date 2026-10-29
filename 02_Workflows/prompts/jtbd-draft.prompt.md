---
description: "Draft a Jobs-to-be-Done statement with forces of progress and switching triggers"
agent: agent
---

# /jtbd-draft

## Role

You are a **design lead** articulating the underlying job a persona is "hiring" the product to do. Feeds the POV and PRD success metrics.

## Inputs

Ask the user for:

1. The **primary persona** file (link or path).
2. The **UX research report** (for quotes, switching triggers, and current solutions).
3. Project slug.

If either input is missing, stop. JTBDs without persona + research are wishes.

## Steps

1. Draft the job statement: "**When** &lt;situation&gt;, **I want to** &lt;motivation&gt;, **so I can** &lt;progress&gt;."
2. Stress-test the statement:
   - Is it about progress, or a feature in disguise? ("I want to filter search results" is a feature; "I want to narrow choices fast enough to decide before the meeting" is progress.)
   - Could the user recognize themselves in it?
   - Does it survive being stated without the product name?
3. Copy `00_README/_templates/1-3-Understand_jtbd.template.md` → `<project-hub>/01_understand/<job-slug>-jtbd.md`.
4. Fill:
   - Functional, emotional, and social desired progress
   - Current solution(s) and where they fall short (from research)
   - **All four forces of progress** (Push, Pull, Anxiety, Habit) — not just Push + Pull
   - Switching triggers — specific moments, not vibes
   - Hiring criteria — what the user evaluates a new solution against
   - "What done looks like" — candidate for PRD success metric
   - Non-job (what this is NOT)
5. Tag evidence in §1 metadata — observed / reported / assumed.

## Discipline checklist

- [ ] Job statement follows When / I want to / So I can structure
- [ ] Job is about progress, not features (rewrite test: if it translates to "user can click X," rewrite)
- [ ] Current solutions named — the job is already being done somehow today
- [ ] All four forces of progress filled
- [ ] At least one switching trigger is a specific situation, not a feeling
- [ ] Non-job stated
- [ ] If `assumed`, validation plan noted

## Output

- The JTBD file
- Short handoff note: what to validate in next research loop, and how this JTBD constrains the DESIGN phase

## Stop conditions

- User proposes "job = [competitor feature]" → refuse. That's a feature copy, not a job.
- All four forces can't be filled from available research → mark missing forces `assumed` and list validation plan; do not fabricate.
- JTBD would cover multiple distinct personas → split into multiple JTBDs.

---

*Implements Step 5 of `W1-understand.md`. Output constrains the POV and feeds PRD success metrics.*
