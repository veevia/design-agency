---
name: concept-rumble
title: Pit two concepts in parallel with a decision trigger
description: When two strong concepts can't be resolved to one, prototype both and let user testing determine the winner — with an explicit decision trigger defined in advance. Use when the Supervote produces a genuine 3/3 split and both concepts address different Sprint Questions strongly, or when the Decider cannot choose between two concepts because they test different, incompatible hypotheses.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - When the Supervote produces a genuine 3/3 split and both concepts address different Sprint Questions strongly
  - When the Decider cannot choose between two concepts because they test different, incompatible hypotheses
  - When the team has sufficient capacity to build two lightweight prototypes in the available build time
  - "As the resolution mechanism for a 🟡 Yellow Supervote: \"We'll build both and the decision trigger is [which result in testing]\""
  - When the concepts are genuinely different architecturally — not variations of the same idea
applies-to: concept tie-breaking, competing hypotheses, parallel prototyping, structured A/B testing, 🟡 Yellow decision resolution
done_when:
  - Two competing concepts are prototyped in parallel
  - An explicit decision trigger/criterion is set in advance
  - The trigger resolves which concept proceeds
metadata:
  duration: 30 min (decision); build time × 2
  team-size: Full sprint team split into two parallel teams
  sprint-phase: 4 Decide
---

# Concept Rumble

**TL;DR:** A Concept Rumble runs two competing concepts into the prototype and validate phases simultaneously. Rather than forcing a premature decision between two genuinely strong and distinct approaches, the team builds both and lets user testing determine the winner. The "rumble" is not a competition for its own sake — it's the mechanism for resolving a specific question the Supervote couldn't answer: "We don't know which approach users will actually prefer, so let's test both."

## When to use

- When the Supervote produces a genuine 3/3 split and both concepts address different Sprint Questions strongly
- When the Decider cannot choose between two concepts because they test different, incompatible hypotheses
- When the team has sufficient capacity to build two lightweight prototypes in the available build time
- As the resolution mechanism for a 🟡 Yellow Supervote: "We'll build both and the decision trigger is [which result in testing]"
- When the concepts are genuinely different architecturally — not variations of the same idea

## When NOT to use

- When concepts are variations of the same approach (different styling, different copy) — pick one
- When build time is tight (< 4 hours) — a Rumble needs two prototypes, each worth testing
- When one concept is clearly stronger on the Design Criteria — use the Decision Matrix instead
- When the disagreement is about preference, not hypothesis — the Supervote should resolve preference

## The Rumble structure

```
Supervote: concepts A and B both strong
            ↓
Define the decision trigger:
"We will choose A if [test condition], B if [test condition]"
            ↓
Split team: Team A builds Concept A; Team B builds Concept B
            ↓
Validate day: participants test both (or alternating participants per concept)
            ↓
Synthesis: which concept met the decision trigger?
            ↓
ADR: 🟢 Green on the winner; document what was learned from the loser
```

## The decision trigger

Before building both prototypes, the team must define the decision trigger — the specific test result that will determine the winner. Without a trigger, the Rumble produces two sets of findings and no decision.

Decision trigger format:
> "We will proceed with [Concept A] if [specific test condition], and [Concept B] if [specific test condition]. If neither or both meet the condition, [what happens]."

Examples:
- "We'll proceed with Reasons-First Triage if ≥3/5 participants act on the suggested priority without switching systems. We'll proceed with One-Tap Assign if ≥4/5 participants complete assignment faster than their reported current process. If both, prioritise Reasons-First Triage because it addresses the higher-weight Sprint Question."
- "We'll proceed with the inline records view (A) if zero participants open another system. We'll proceed with the separate booking-check modal (B) if ≥3/5 participants prefer the detail modal when asked directly. The inline view wins if tied."

## Splitting the team

| Role in Rumble | Responsibility |
|---|---|
| **Concept A team** (2–3 people) | Build Concept A's prototype to test fidelity |
| **Concept B team** (2–3 people) | Build Concept B's prototype to test fidelity |
| **Stitcher** | Works across both — ensures consistent scenario setting, shared screens |
| **Interviewer** | Writes a unified Five-Act Interview guide that tests both concepts |
| **Decider** | Monitors both builds; makes the final call if test results are ambiguous |

## Testing both concepts

Two approaches:

**Approach 1 — Sequential (recommended for 5 participants):**
First 2–3 participants test Concept A first, then B. Last 2–3 test B first, then A. Counterbalance order to control for priming. Each participant sees both — their comparative reaction is the data.

**Approach 2 — Parallel (requires 10 participants):**
5 participants see only Concept A; 5 see only Concept B. Cleaner comparison but requires double the recruitment.

For a one-day sprint validate, use Approach 1.

## Example output

```markdown
## Concept Rumble Decision — Request Triage Sprint · 2026-02-24

**Concepts in rumble:**
- A: Reasons-First Triage (inline records + AI urgency score)
- B: One-Tap Assign (assignment-first; minimal AI features)

**Reason for rumble (not Supervote):**
Straw Poll: 3 votes A, 3 votes B. Both concepts address different Sprint Questions: A → priority trust (SQ2); B → triage and assignment speed (SQ1, SQ3). Decider could not choose — both are valid hypotheses.

**Decision trigger:**
- Proceed with A if: ≥3/5 participants act on the suggested priority without opening another system
- Proceed with B if: ≥4/5 participants complete assignment in ≤2 interactions and rate it "faster than today"
- If both conditions met: A is primary (priority trust is the higher-weight SQ); incorporate B's assignment gesture
- If neither: 🔴 reconsider both concepts; return to Phase 3 with new insight

**Build split:**
- Team A (2 Makers + 1 Writer): Reasons-First Triage screens in Figma — 3.5h
- Team B (2 Makers): One-Tap Assign screens in Figma — 2.5h
- Stitcher: unified scenario setting; shared participant intro screen
- Interviewer: write tasks for both concepts

**Test protocol:**
- P1, P2, P3: see A first, then B (20 min each)
- P4, P5: see B first, then A (20 min each)
- Debrief Q: "If you could combine elements from both, which interaction would you keep from each?"

**Result:**
- A: 4/5 acted on the suggested priority without opening another system ✅
- B: 5/5 completed assignment in ≤2 interactions ✅
- Both conditions met → proceed with A as primary; incorporate B's one-tap assign gesture as a secondary feature

**ADR filed:** 🟢 — Reasons-First Triage + One-Tap Assign hybrid; Assumptions Board updated
```

## Agent facilitation guide

When deciding whether to recommend a Concept Rumble:
1. Check: are the two concepts testing different hypotheses (not different styles)?
2. Check: is there sufficient build capacity for two prototypes?
3. Define the decision trigger before recommending Rumble — if you can't write a trigger, the disagreement is about preference, not hypothesis → use Supervote instead
4. Draft the build split: which team members build which concept?
5. Write the unified test protocol: how will the Interviewer test both concepts fairly?

## Watch-outs

- **Rumble as indecision:** "We'll test both because we can't agree" without a decision trigger is not a Rumble — it's deferred decision-making. The trigger must be defined before building.
- **Unequal build quality:** If Concept A gets 3 Makers and Concept B gets 1, the test is biased. Split build resources fairly.
- **No clear trigger → no decision:** If the Validate results are: "participants liked both" — without a trigger, the team is back to the same deadlock. The trigger forces clarity before testing.
- **Using Rumble to avoid Supervote:** The Decider should still place their dots — even for a Rumble, they're naming which concept they're betting on. The Rumble resolves the uncertainty; it doesn't eliminate the Decider's role.

## Connects to

- [Supervote](../supervote/SKILL.md) — Rumble is triggered when Supervote cannot resolve a genuine tie
- [Assumptions Board](../assumptions-board/SKILL.md) — each concept's riskiest assumption is what the Rumble tests
- [Dividing Roles](../dividing-roles/SKILL.md) — Rumble requires a parallel team structure
- [Five-Act Interview](../five-act-interview/SKILL.md) — interview must be designed to test both concepts fairly
- [`00_README/_frameworks/traffic-light-decisions.md`](../../../00_README/_frameworks/traffic-light-decisions.md) — Rumble trigger condition = 🟡 Yellow trigger
