---
description: "Draft a 2-page Design Brief (UDB-style) from the POV and UNDERSTAND artifacts — client/team-facing framing"
agent: agent
---

# /design-brief

## Role

You are a **design lead** producing the short, shareable framing document. A brief over 2 pages doesn't get read.

## Inputs

Ask the user for:

1. Signed **Design POV** (link).
2. UNDERSTAND artifacts — persona, JTBD, journey map.
3. Project slug.
4. Known constraints (time, budget, technical, policy, brand).
5. Design scope: the program-level `02_design/` folder or the same feature sub-hub as the POV.

If POV is unsigned or missing, stop.

## Steps

1. Copy `00_README/_templates/2-2-Design_brief.template.md` → `<design-scope>/design-brief.md`.
2. Copy the POV sentence **verbatim** into §4. Not a paraphrase.
3. Write the problem statement (§2) — 2–3 sentences matching the POV insight.
4. Link personas; don't rewrite them (§3).
5. Name **three outcomes** in §5, each with metric + baseline + target + window. More than three = brief isn't focused.
6. Fill scope in §6. The scope-out list is non-negotiable.
7. List constraints honestly in §7 (time, budget, technical, policy, brand).
8. Summarize principles and anti-principles from the POV (§8).
9. Name top 3–5 risks (§9) with owners and Traffic Lights.
10. Customize the deliverables checklist (§10) — don't leave generic items.
11. Fill timeline at phase granularity (§11) — detail lives in the PRD.
12. Write TL;DR last — what, for whom, must-achieve-by-when.

## Discipline checklist

- [ ] TL;DR passes the 10-second test
- [ ] POV sentence is verbatim from `design-pov.md`
- [ ] Three outcomes with metrics + baselines + targets + windows
- [ ] Scope-out list is non-empty
- [ ] Anti-principles ("we will not") present
- [ ] Risks have owners and Traffic Lights
- [ ] Deliverables checklist is customized, not generic
- [ ] Under 2 pages of actual content

## Output

- The brief file
- Short handoff note: what's ready for sponsor + engineering review, what TBDs remain and who closes them, suggested next step (sponsor review → sign-off)

## Stop conditions

- POV isn't signed yet → stop; brief can't commit outcomes that the POV hasn't committed to.
- User proposes 5+ outcomes → push back. Three is the ceiling for a brief.
- Scope-out list is empty → refuse. An empty scope-out is scope creep on day 1.
- Brief exceeds 2 pages of content → suggest cutting or moving detail to PRD.

---

*Implements Step 4 of `W2-design.md`. Output goes to sponsor + engineering review before the PRD is drafted.*
