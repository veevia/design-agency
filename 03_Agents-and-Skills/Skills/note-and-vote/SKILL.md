---
name: note-and-vote
title: Prioritise options by silent note-then-vote
description: A cross-phase silent prioritisation technique — everyone writes ideas or votes on sticky notes simultaneously, then the group reveals and clusters. Use after Affinity Mapping, after generating Sprint Questions, or after Lightning Demos. Use when a group needs to prioritise a list without a long discussion, or when the team has 4+ options and needs to narrow to 1–3.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - After Affinity Mapping — to rank which HMW clusters the team wants to focus on
  - After generating Sprint Questions — to rank which questions matter most
  - After Lightning Demos — to identify which demo ideas are worth exploring
  - Any time a group needs to prioritise a list without a long discussion
  - When the team has 4+ options and needs to narrow to 1–3
applies-to: prioritisation, decision-making, group alignment, HMW clustering, sprint question selection, concept voting
done_when:
  - Each participant generated notes silently before any discussion
  - Votes are cast simultaneously to avoid anchoring
  - The top-voted options are named and carried forward
metadata:
  duration: 5–10 min per round
  team-size: Full sprint team (equal weight per person)
  sprint-phase: 1 Understand
---

# Note-and-Vote

**TL;DR:** Note-and-Vote is the sprint's workhorse prioritisation method. It appears in every phase: ranking HMW clusters in Understand, selecting Sprint Questions in Define, evaluating lightning demo elements in Sketch, and narrowing concepts in Decide. The mechanic is always the same — everyone writes or votes silently and simultaneously — but the input changes. It removes the social pressure of verbal voting and surfaces genuine individual preferences before any group discussion.

## When to use

- After Affinity Mapping — to rank which HMW clusters the team wants to focus on
- After generating Sprint Questions — to rank which questions matter most
- After Lightning Demos — to identify which demo ideas are worth exploring
- Any time a group needs to prioritise a list without a long discussion
- When the team has 4+ options and needs to narrow to 1–3

## The core mechanic

**Note (silent writing):** Each person writes their top choice(s) on a sticky note or votes with a dot sticker — without seeing what others are writing.

**Reveal (simultaneous):** Everyone reveals at the same time.

**Discuss (only if needed):** If results are aligned, move on. If split, the top minority argument gets 1 minute of air time. The Decider makes the call.

The silence before reveal is what makes Note-and-Vote work. Any verbal signal ("I think this one is most important") before the reveal contaminates the group's independent thinking.

## Common applications

### Application 1: HMW cluster ranking (Phase 1, after Affinity Map)

Each person writes the name of the 1–2 clusters they believe should drive the sprint on a sticky note. Reveal. Count. Top clusters with the most votes become the Sprint Questions.

### Application 2: Sprint Question ranking (Phase 2)

After generating 8–12 candidate Sprint Questions, the team votes on which 3–5 are most important. Each person writes their top 3 on a sticky. Reveal. The Facilitator marks all that appear on ≥2 stickies as "top tier." Decider makes the final selection.

### Application 3: Lightning Demo element ranking (Phase 3)

After Lightning Demos, each person identifies the 2–3 demo elements most relevant to the sprint. Write on a sticky. Reveal. Elements with multiple mentions are the inspiration anchors for sketching.

### Application 4: Concept selection (Phase 4 supplement)

If the team is overwhelmed by the number of solution sketches, a Note-and-Vote round before Heat Map Voting can quickly narrow to the 3–4 concepts worth detailed critique.

## Steps

1. **Set up the list (1 min):** Post the items to be ranked on the wall — HMW clusters, Sprint Questions, concepts, or demo elements.

2. **Individual writing (2–3 min, silent):** Each person writes their top choice(s) on a sticky note. Do not discuss, do not look at what others are writing.

3. **Reveal (simultaneous):** Facilitator counts down: "3, 2, 1 — post." Everyone posts their sticky at the same time.

4. **Read the results (1 min):** Facilitator reads out the distribution. Count how many votes each option received.

5. **Discussion (only if split) (2 min):** If results are clear (≥60% on one option), move on. If split, ask: "Who voted for [minority option]? Can you name one reason in one sentence?"

6. **Decider decides (1 min):** The Decider names the top-ranked items. This is not always the plurality — the Decider may see strategic reasons to prioritise a minority choice. Their decision is final.

## Format variations

| Format | When to use |
|---|---|
| **Single vote** | Force a clear choice — 1 sticky per person |
| **Multi-vote (2–3)** | When multiple items will be carried forward |
| **Dot stickers** | When voting on items already posted (physical version) |
| **Silent 1–5 ranking** | When relative priority matters, not just top pick |
| **Written rationale** | After a multi-vote round, each person writes one sentence justifying their pick before reveal |

## Note-and-Vote vs. open discussion

| | Note-and-Vote | Open discussion |
|---|---|---|
| Social pressure | Eliminated — votes are private until reveal | High — first strong voice influences others |
| Speed | Fast (5–10 min) | Slow (can easily run 30+ min) |
| Coverage | Surfaces all positions | Surfaces loudest positions |
| Best for | Choosing between defined options | Exploring undefined space |

## Agent facilitation guide

When facilitating a Note-and-Vote round:
1. List the items to be voted on (HMW clusters, Sprint Questions, concepts, etc.)
2. Ask: "If you could only focus on [1 / 2 / 3] of these, which would it be?"
3. Produce a simulated vote result based on sprint question coverage and team composition
4. Flag the minority argument (if any) worth naming
5. Recommend a Decider selection with rationale

Output:
```markdown
## Note-and-Vote — HMW Cluster Priority · [Sprint Name]

**Items voted on:**
1. Morning triage time
2. Priority trust gap
3. Assignment friction
4. Cross-site visibility
5. Mobile access

**Simulated vote (5 team members, 2 votes each = 10 votes):**
| Cluster | Votes | % |
|---|---|---|
| Morning triage time | 4 | 40% |
| Priority trust gap | 3 | 30% |
| Assignment friction | 2 | 20% |
| Cross-site visibility | 1 | 10% |
| Mobile access | 0 | 0% |

**Recommendation:** Morning triage time + Priority trust gap as co-primary focus.
**Minority argument:** Assignment friction is high-pain and more solvable in a single sprint — worth noting as a potential quick win even if not the primary focus.
**Decider call:** Your choice — both the top 2 or assignment friction as the sprint's core focus are defensible.
```

## Watch-outs

- **Voting sequentially:** If one person posts their sticky first and others see it before posting their own, the reveal is no longer blind. Enforce simultaneous reveal.
- **Skipping the Decider step:** Note-and-Vote surfaces preferences; the Decider makes the call. A plurality vote doesn't override the Decider's judgment.
- **Using it for exploration:** Note-and-Vote works for prioritising a defined list. If the team doesn't know what the options are yet, use HMW or Mind Mapping first to generate options, then vote.
- **Over-voting:** If the team does 4 rounds of Note-and-Vote in a row, decision fatigue sets in. Reserve it for genuine prioritisation moments, not every micro-decision.

## Connects to

- [Affinity Map](../affinity-map/SKILL.md) — clusters are the items voted on in Phase 1 Note-and-Vote
- [Sprint Questions](../sprint-questions/SKILL.md) — Note-and-Vote selects the final Sprint Questions
- [Lightning Demos](../lightning-demos/SKILL.md) — demo elements are ranked after Note-and-Vote
- [Straw Poll](../straw-poll/SKILL.md) — Straw Poll is a concept-level variant of Note-and-Vote
