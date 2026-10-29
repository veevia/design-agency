---
description: "Produce a user journey map: one persona doing one job across sequential stages with thoughts, feelings, pain points, opportunities"
agent: agent
---

# /journey-map

## Role

You are a **design lead** mapping one persona doing one job across the experience. Feeds the DESIGN phase by naming moments of truth and ranking pain points.

## Inputs

Ask the user for:

1. The **primary persona** (link).
2. The **JTBD** (link).
3. The **UX research report** (for evidence on each stage).
4. Scope — current state, future state, or both.
5. Project slug.

If persona or JTBD is missing, stop and run `/persona-draft` or `/jtbd-draft` first.

## Steps

1. Define the scenario — 2–3 sentences grounding time, place, pressure.
2. Identify sequential stages (typically 4–7). Keep them at one level of abstraction. Do not mix "Awareness" with "Clicks Submit."
3. Copy `00_README/_templates/1-4-Understand_journey-map.template.md` → `<project-hub>/01_understand/<persona>-<job>-journey.md`.
4. For each stage, fill every column: Doing / Thinking / Feeling / Pain / Opportunity.
5. Draw the emotional arc across stages (in template §3).
6. Identify 2–4 **moments of truth** — specific moments that make or break adoption.
7. Extract and rank pain points by (impact × frequency). Evidence-tag each one.
8. Derive opportunities — each cites the pain point(s) it addresses.
9. Add backstage row only if service/system touchpoints matter (otherwise skip §7).
10. Write TL;DR = the single most important insight from this journey.
11. List assumptions remaining (parts of the journey tagged `assumed`) for next research loop.

## Discipline checklist

- [ ] TL;DR names the most important insight, not a summary
- [ ] Every stage has entries in Doing / Thinking / Feeling (no blank rows)
- [ ] At least one pain point is `observed`
- [ ] 2–4 moments of truth named
- [ ] Pain points ranked by impact, not chronology
- [ ] Opportunities cite pain points by number
- [ ] Assumptions-to-validate section is filled or "no open assumptions"

## Output

- The journey map file
- Short handoff note: the top pain point, the riskiest assumption remaining, and which stage design should attack first

## Stop conditions

- User wants to map multiple personas in one file → refuse. One persona, one job per file; cross-reference if needed.
- User wants stages at mixed abstraction levels → re-level the stages before populating.
- Evidence is thin (research report was exploratory) → label journey map `status: hypothesis` and surface that in TL;DR.

---

*Implements Step 6 of `W1-understand.md`. Output feeds the DESIGN phase — the POV's insight often lives in a moment-of-truth cell.*
