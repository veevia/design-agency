---
name: research-synthesis
title: Turn raw research into themed, tagged findings
description: Find patterns across five interviews, vote on insights, and make the forward decision — iterate, ship wider, pivot, or stop — with a Traffic Light ADR. Use after the last interview session on Validate day, within 24 hours of completing the interviews (memory and shared context decay fast). Use when a team needs to go from qualitative observations to a scoped decision.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Immediately after the last interview session on Validate day
  - Within 24 hours of completing the interviews (memory and shared context decay fast)
  - Any time a team needs to go from qualitative observations to a scoped decision
applies-to: research synthesis, pattern finding, insight voting, forward decision, ADR filing, sprint retrospective
done_when:
  - Observations are clustered into patterns across participants
  - Each finding carries an evidence tag and source
  - A forward decision/next step is recorded (ADR if needed)
metadata:
  duration: 60–90 min
  team-size: Full sprint team
  sprint-phase: 6 Validate
  redirect-host: wiki-query
---

# Synthesis

**TL;DR:** The synthesis session is the moment the sprint turns data into a decision. After five interviews, the team has raw observation notes, an assumption tally, and a set of "interesting moments." Synthesis takes 60–90 minutes to move from observations to patterns to a forward decision. The output is not a report — it is an ADR with a Traffic Light and a one-sentence forward action.

## When to use

- Immediately after the last interview session on Validate day
- Within 24 hours of completing the interviews (memory and shared context decay fast)
- Any time a team needs to go from qualitative observations to a scoped decision

## The synthesis arc

```
Raw notes (5 sessions)
    → Observations (what happened)
        → Patterns (what it means)
            → Insights (what we now know)
                → Decision (what we do next)
                    → ADR (filed, with Traffic Light)
```

Each step is a distinct act. Do not jump from "what happened" to "what we do next" without the pattern-finding steps.

## Steps

### Step 1 — Review the assumption tally (10 min)

Display the running tally from Team Observation. Each assumption has a status across 5 participants. Go through the tally together:

- For each ✅ Confirmed assumption: "We can proceed with confidence on this."
- For each ❌ Challenged assumption: "This is a problem. What did we see?"
- For each ⚠️ Partial assumption: "This needs nuance — what conditions made it work vs. not work?"

This step establishes shared facts before interpretation begins.

### Step 2 — Read the "interesting moments" (10 min)

The Note Lead reads the top moments from the observation log — quotes, unexpected behaviours, patterns that surfaced across sessions but weren't original assumptions.

The Facilitator posts each one on a sticky note (physical or digital). No discussion yet. The goal is to surface the raw material before clustering.

### Step 3 — Cluster into patterns (15 min)

Silently, each team member groups the observation stickies into themes. Then the group aligns on 3–5 clusters. Each cluster gets a name that states the pattern, not the observation:

- ✗ "Participants asked about urgency scores" (observation)
- ✓ "Numeric urgency scores require explanation before users trust them" (pattern)
- ✗ "P2 and P4 didn't open another system" (observation)
- ✓ "Inline records eliminate system-switching for most users" (pattern)

Name each cluster with a verb. If you can't state it as a pattern, keep clustering.

### Step 4 — Dot vote on insights (10 min)

Give each team member 2 dot stickers. Vote on the patterns that feel most important for the forward decision — not the most interesting, not the most surprising, but the ones that should change what the team builds next.

The top-voted patterns become the sprint's named insights.

**Insight format:**
```
Insight: [Pattern statement]
Evidence: [Number of participants] / 5 showed this
Implication: [What this means for the product or the build decision]
```

### Step 5 — Make the forward decision (15 min)

Look at the full picture — confirmed assumptions, challenged assumptions, and top insights — and make one of four decisions:

| Decision | When | Next action |
|---|---|---|
| **Iterate and re-test** | Core concept is right; specific execution failed | Redesign the failing elements; run another test round |
| **Ship wider** | Concept validated; assumptions confirmed; ready to build | Move to production build with findings as input to PRD |
| **Pivot** | Core assumption failed; a different concept may work better | Return to Phase 3/4 with new insight; new sprint or design iteration |
| **Stop** | The sprint question is answered negatively; this problem isn't worth solving | Document the learning; redirect the team |

The forward decision requires a rationale. What specifically did you see that justifies this decision? Name the assumption results that drive it.

### Step 6 — File the ADR (10 min)

Write the sprint's final Traffic Light decision record. This closes the sprint.

```markdown
## ADR — Sprint Validate: [Sprint Name] · [Date]

**Sprint question(s) tested:**
1. Can coordinators act on the suggested priority without manual checks?
2. Do inline CRM, service-contract, and inventory-system records reduce system-switching in the morning triage workflow?

**Prototype:** Reasons-First Triage (Supervote winner, Phase 4)
**Test method:** 5×60min Five-Act Interviews; participants: the Lead Coordinator (P1), three coordinators from their team (P2–P4), the Site Supervisor at Site C (P5)

### Assumption results

| Assumption | Result | Evidence |
|---|---|---|
| Urgency score interpreted correctly | ❌ Failed | 3/5 needed explanation; 1/5 ignored score entirely |
| Inline records reduce system-switching | ✅ Confirmed | 4/5 did not open another system; average 1.3 record reads per request |
| Suggested priority acted on without checking | ❌ Failed | 4/5 asked "how is this worked out?" or "how do I know it's right?" |
| One-tap assign is faster than 3-step | ✅ Confirmed | 5/5; average 1.8 taps vs. current 7-step assignment |

### Top 3 insights
1. **Priority trust requires transparency:** Coordinators will not act on the suggested priority without understanding how it was worked out. An urgency score alone is insufficient — they need "why this score."
2. **Record visibility is immediately valued:** All participants noticed and used the inline records panel. This feature needs zero explanation.
3. **Assignment is the clearest win:** One-tap assign solved a real, named pain. No friction. Immediate adoption signal.

### Forward decision
**🟡 Yellow — Iterate and re-test on priority trust; build assignment and record display now**

- Build one-tap assign + record display (fully confirmed) → move to the request system's Build phase
- Redesign the urgency score: add its basis ("learned from 18,000 past requests with known outcomes") and an explanation (why 62, not just 62)
- Run a second test round on the redesigned urgency explanation before filing 🟢

**Trigger:** Urgency score explanation validated with ≥3/5 participants correctly interpreting the score AND acting on the suggested priority without additional checking
**Expiry:** 2026-03-31 — if not re-tested by this date, escalate to PM

### Disagreement
None — team unanimous on the two confirmed findings; Decider accepted the 🟡 on priority trust.
```

## Output quality checklist

Before closing synthesis:
- [ ] Every original sprint question has a direct answer (confirmed / challenged / no signal)
- [ ] Every critical assumption has an evidence-backed status
- [ ] The forward decision names what will be built, changed, or dropped
- [ ] The ADR Traffic Light has a trigger condition and expiry date if Yellow
- [ ] Disagreement is captured (or explicitly noted as absent)
- [ ] One insight connects directly back to the original Long-Term Goal

## Agent facilitation guide

When synthesising sprint observation notes into a forward decision:
1. Read the assumption tally — count confirmed vs. challenged for each assumption
2. Extract the top "interesting moments" across all 5 sessions
3. Cluster into 3–5 named patterns using the "verb + subject" format
4. Identify the forward decision based on confirmed/challenged balance:
   - All critical confirmed → Ship wider
   - Mixed (some confirmed, some challenged) → Iterate on challenged items
   - Core assumption challenged → Pivot or stop
5. Draft the ADR with the correct Traffic Light — include trigger + expiry if Yellow
6. Flag any discovered finding (recurring behaviour outside original assumptions) as a future sprint question

## Watch-outs

- **Jumping to solutions before finishing synthesis:** "We should add a tooltip!" is a solution. Finish the pattern-finding and forward decision first. Solutions belong in the next sprint's Phase 3, not in the synthesis session.
- **Voting without reading the moments first:** Dot votes before the full observation log is shared will over-weight whatever was loudest in the room (usually the last session).
- **No ADR filed:** A sprint that doesn't end in a decision record leaves the team without an auditable trail. The ADR is not bureaucracy — it's the mechanism by which the Validate phase informs the next Build phase.
- **Forward decision as "continue building":** "Continue building" is not a decision. Name what is confirmed (and will be built), what is challenged (and will be iterated), and what the trigger condition is for the Yellow items.
- **Only sharing positive findings with the Decider:** The Decider needs to hear the challenged assumptions too. A synthesis that leads with wins and buries failures is not synthesis — it's advocacy.

## Connects to

- [Team Observation](../team-observation/SKILL.md) — assumption tally and observation log are the primary inputs
- [Five-Act Interview](../five-act-interview/SKILL.md) — session structure produces the observation data
- [Assumptions Board](../assumptions-board/SKILL.md) — synthesis closes the loop on every critical assumption
- [Supervote](../supervote/SKILL.md) — the winning concept is assessed against its original assumptions
- [`00_README/_frameworks/traffic-light-decisions.md`](../../../00_README/_frameworks/traffic-light-decisions.md) — ADR Traffic Light rules apply in full
- [`00_README/_templates/4-1-Learn_evidence-brief.template.md`](../../../00_README/_templates/4-1-Learn_evidence-brief.template.md) — sprint synthesis feeds the Learn phase Evidence Brief
