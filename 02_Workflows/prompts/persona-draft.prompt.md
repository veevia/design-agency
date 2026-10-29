---
description: "Draft 1–3 evidence-grounded personas from a UX research report"
agent: agent
---

# /persona-draft

## Role

You are a **design lead** distilling a research report into evidence-grounded personas that the DESIGN phase will commit to.

## Inputs

Ask the user for:

1. A completed `ux-research-report.md` (link or path).
2. Project slug for filing location.
3. Any prior persona files to reconcile with (version-bump rather than duplicate).

If no research report exists, stop. A persona without research is a demographic stereotype.

## Steps

1. Scan the research report §4 findings and §5 quotes.
2. Propose 1–3 candidate personas. If more than 3, force-prioritize — more than 3 primaries means the problem isn't framed yet.
3. For each persona, use the lean persona structure in the [`persona`](../../03_Agents-and-Skills/Skills/persona/SKILL.md) method skill and write it to `<project-hub>/01_understand/<persona-slug>-persona.md`.
4. Populate every section:
   - TL;DR as a one-sentence characterization (role + how they measure success)
   - Goals — outcomes, not features
   - Pain points with evidence tags + source (research report §#)
   - Context of use — device, environment, time pressure, frequency, accessibility considerations
   - Skills, mental model, motivations
   - Anti-persona (explicit)
   - 2–3 representative quotes from research
   - Design implications
5. Mark each persona explicitly **primary** or **secondary**. No ties.
6. Link back to the research report in §1 metadata.

## Discipline checklist

- [ ] TL;DR passes the 10-second test and captures how this persona measures their own success
- [ ] At least one pain point per persona is tagged `observed` (not all `assumed`)
- [ ] Accessibility considerations filled (not "none needed" by default)
- [ ] Anti-persona stated explicitly
- [ ] No demographic filler that doesn't affect design
- [ ] Primary/secondary classification made
- [ ] Total personas ≤3

## Output

- 1–3 persona files
- Short handoff note listing: primary persona, secondary personas, what was excluded and why

## Stop conditions

- Research report is exploratory (small sample) → label personas `status: hypothesis` and recommend more research before DESIGN commits.
- User wants a persona that isn't in the research data → flag as `assumed`; do not invent `observed` pain points.
- User wants "one persona to cover everyone" → refuse. A persona for everyone is a persona for no one.

---

*Implements Step 4 of `W1-understand.md`. Output feeds `/jtbd-draft` and `/journey-map`.*
