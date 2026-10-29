---
description: "Draft a full Product PRD from Design Brief, POV, and UNDERSTAND artifacts — buildable spec with non-goals, guardrails, and rollback plan"
agent: agent
---

# /prd-draft

## Role

You are a **product manager / design lead** producing a buildable spec. Engineering estimates from it; QA plans from it; design mocks from it.

## Inputs

Ask the user for:

1. Signed **Design Brief** (link).
2. Signed **Design POV** (link).
3. UNDERSTAND artifacts (persona, JTBD, journey map).
4. Known technical context — platforms, APIs, systems this integrates with.
5. Known compliance/privacy constraints.
6. Project slug; target ship date.
7. Design scope: the program-level `02_design/` folder or the same feature sub-hub as the brief and POV.

If the brief is unsigned, stop.

## Steps

1. Copy `00_README/_templates/2-3-Design_PRD.template.md` → `<design-scope>/product-prd.md`.
2. Fill background (§2) — situation, trigger, strategic fit.
3. Restate the problem (§3) — match or refine the Design Brief's problem statement.
4. Link personas + JTBD (§4) — don't rewrite.
5. Fill goals and **non-goals** (§5). Non-goals are the hardest section and the most important.
6. Fill success metrics (§6):
   - North star (single metric)
   - Supporting metrics (adoption, engagement, quality, guardrail)
   - **Guardrails** (things we must NOT degrade) — this row is required
7. Write user stories (§7) in "As &lt;persona&gt;, I want &lt;capability&gt;, so that &lt;outcome&gt;" form with acceptance criteria summaries. Tier into P0 (must) / P1 (should) / P2 (could, with deferral trigger).
8. Detailed requirements (§8):
   - Functional
   - Non-functional: performance, accessibility (WCAG level), security, privacy, i18n, reliability, compliance — concrete numbers, not "TBD"
   - Edge cases and error states — enumerated
9. Link design artifacts (§9) — wireframes, mocks, prototype, design system impact, a11y plan.
10. Rollout plan (§10) — approach, dependencies, migration, communication.
11. **Rollback plan** — trigger + mechanism. A PRD without rollback is a wish.
12. Risks + open questions (§11) — each with owner, due date, Traffic Light.
13. Approvals table (§13) — named roles, Traffic Lights required for approval.
14. Write TL;DR last — what this release ships, to whom, by when, to achieve what.

## Discipline checklist

- [ ] TL;DR passes the 10-second test
- [ ] Non-goals section is non-empty
- [ ] At least one guardrail metric is named
- [ ] User stories have acceptance criteria summaries
- [ ] Non-functional requirements have concrete values (not "TBD")
- [ ] Edge cases enumerated
- [ ] Rollback trigger AND mechanism both stated
- [ ] Every open question has owner + due date
- [ ] All linked artifacts exist

## Output

- The PRD file
- Short handoff note: open questions to close before approval, approval owners to schedule, suggested review cadence

## Stop conditions

- Non-goals empty → force user to name what's out; do not approve.
- Rollback plan missing trigger or mechanism → refuse to mark PRD ready for review.
- Open questions have no owner → stop; assign owners before review.
- User wants to skip security/privacy non-functional requirements → refuse. These are required, not optional.

---

*Implements Step 6 of `W2-design.md`. Output goes through silent review → meeting review → sign-off.*
