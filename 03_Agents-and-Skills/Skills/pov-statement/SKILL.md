---
name: pov-statement
title: Write the one-sentence design brief (POV)
description: Distil research into a single, user-centred problem statement — "[User] needs [need] because [insight]" — that frames every design decision. Use when at the start of Phase 2, as the first synthesis step after Affinity Mapping and research review, before writing Sprint Questions, or when the team has a rich understanding of the user but no shared frame for the design problem.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - At the start of Phase 2, as the first synthesis step after Affinity Mapping and research review
  - Before writing Sprint Questions — the POV is the root that Sprint Questions branch from
  - When the team has a rich understanding of the user but no shared frame for the design problem
  - When different team members would articulate "who we're designing for" differently
applies-to: problem framing, design direction, sprint scope, HMW anchoring, solution evaluation criteria
done_when:
  - The POV reads “[user] needs [need] because [insight]”
  - The need is a verb/goal, not a solution
  - The insight is evidence-grounded, not assumed
metadata:
  duration: 20–30 min
  team-size: Full sprint team; Decider approves final statement
  sprint-phase: 2 Define
  redirect-host: problem-framing
---

# Point of View (POV) Statement

**TL;DR:** A Point of View statement is the sprint's anchor: a single, specific sentence that declares who the team is designing for, what they need, and why that need matters. It converts the research gathered in Phase 1 into a design challenge that the team can rally around. A good POV is narrow enough to be actionable, honest enough to be provocative, and grounded enough to be defensible. It is not a solution — it is a problem made concrete.

## When to use

- At the start of Phase 2, as the first synthesis step after Affinity Mapping and research review
- Before writing Sprint Questions — the POV is the root that Sprint Questions branch from
- When the team has a rich understanding of the user but no shared frame for the design problem
- When different team members would articulate "who we're designing for" differently

## The formula

> **[User]** needs **[need]** because **[insight]**.

| Element | What it is | What makes it strong |
|---|---|---|
| **User** | A specific persona — not a demographic | "The Lead Coordinator" (primary persona), not "office staff" |
| **Need** | What they need to accomplish — JTBD language | Verb-first: "a way to check a request's details without leaving the inbox" |
| **Insight** | The underlying why — emotional, contextual, or structural | Not obvious; reframes the problem: "because every system they open is a moment of doubt that erodes their confidence before the 8am start" |

The insight is the hardest part. It should feel slightly surprising — something that wouldn't appear in a product requirements list but explains *why* the user behaves the way they do.

## Three quality tests

**Test 1 — Is it specific?**
"Users need better tools" fails. "The Lead Coordinator needs to check a request's details without leaving their workflow" passes.

**Test 2 — Is the insight non-obvious?**
"Because they want to be efficient" is obvious. "Because every check they don't need to make is a small sign to themselves that they can trust the system" is an insight.

**Test 3 — Does it open up design space?**
A good POV generates multiple HMW questions. If it only suggests one solution, it's too narrow.

## Steps

1. **Draft individual POVs (8 min, silent):** Each team member writes a draft POV on a sticky using the formula. Focus on the primary persona and the most important need surfaced in research.

2. **Read and compare (5 min):** Post all drafts. Read aloud. Where do they agree? Where do they diverge? Disagreements on the "user" or "need" element reveal unresolved research gaps. Disagreements on "insight" reveal different interpretations of the same research.

3. **Identify the strongest elements (5 min):** Team votes (dot stickers) on: which "user" framing is most specific? Which "need" is most important? Which "insight" is most non-obvious?

4. **Draft the combined POV (5 min):** Facilitator writes a combined draft using the voted elements. Team refines in one or two iterations.

5. **Decider approves (2 min):** The Decider reads the final POV and confirms: "Yes, this is the problem we are solving." Post it prominently — it stays on the wall for the entire sprint.

## Example

```markdown
## POV Statement — Request Triage Sprint · 2026-02-24

**Draft 1 (team member A):**
The Lead Coordinator needs to confirm a request's details quickly because they can't assign a request they don't trust.

**Draft 2 (team member B):**
The Lead Coordinator needs a triage view that shows customer, service-contract, and inventory details inline because leaving the inbox to check a request breaks their concentration and compounds their anxiety about missing an urgent request.

**Draft 3 (team member C):**
The Lead Coordinator needs a way to trust the suggested priority because their standing with the sites depends on never sending a specialist to a routine request while an urgent one waits.

---

**Final POV (voted + combined):**
The Lead Coordinator needs a way to check a request's details and assign it correctly in a single, unbroken workflow — because every time they leave the inbox to check another system, they lose context and add doubt to a process that already feels like a race against the clock before the 8am start.

**Why this works:**
- User: specific persona and role
- Need: "check details and assign correctly in a single workflow" — functional + emotional
- Insight: "lose context and add doubt... race against the clock" — explains the emotional cost of the current workaround, not just the mechanical friction
```

## POV → HMW bridge

Once the POV is written, it generates HMW questions directly:

| POV element | HMW question |
|---|---|
| Needs to check details without leaving | HMW show customer, service-contract, and inventory details inline so the coordinator never needs to open another system? |
| Assign correctly in a single workflow | HMW reduce the assignment decision to one interaction from within the request view? |
| Loses context when they leave | HMW keep the coordinator's mental context intact throughout the full triage workflow? |
| Race against the clock | HMW make clear-cut urgent requests immediately recognisable so the coordinator can skip manual review? |

## Agent facilitation guide

When generating a POV statement from sprint research:
1. Identify the primary persona (from Persona canvas)
2. Identify the most important unfulfilled need — the one that, if addressed, would most change their experience
3. Identify the non-obvious insight — not what they said, but what you inferred from the gap between their behaviour and their stated preference
4. Write 2–3 draft POV statements using the formula
5. Evaluate each against the three quality tests
6. Select or combine the strongest elements into a final statement
7. Generate 3–5 HMW questions directly from the POV

## Watch-outs

- **POV as solution:** "The Lead Coordinator needs an urgency score" is a solution masquerading as a need. Reframe: "The Lead Coordinator needs a way to know how much to trust a request's suggested priority without looking it up themselves."
- **Generic user:** "Users" or "coordination staff" does not create the shared empathy a specific persona does. The team should be able to picture the Lead Coordinator specifically when they read the POV.
- **Weak insight:** If the "because" clause is something everyone already knew, it won't generate new design thinking. Push for the insight that makes someone say "I hadn't thought of it that way."
- **Two users in one POV:** If the Lead Coordinator's need and the Site Supervisor's need are both in the same POV, the team has two design problems. Write separate POVs; the Sprint Target selects which to focus on.

## Connects to

- [Persona](../persona/SKILL.md) — the user element comes from the persona
- [Empathy Map](../empathy-map/SKILL.md) — the insight element comes from the THINKS/FEELS contradiction
- [Jobs-to-be-Done](../jobs-to-be-done/SKILL.md) — the need element matches the JTBD formula
- [How Might We](../how-might-we/SKILL.md) — POV generates the strongest HMW questions
- [Sprint Questions](../sprint-questions/SKILL.md) — Sprint Questions test whether solutions address the POV
