---
name: how-might-we-voting
title: Prioritise HMW notes by dot voting
description: Vote on the HMW clusters from Phase 1 to select which ones become Sprint Questions — the specific prioritisation step that closes Understand and opens Define. Use after Affinity Map is completed and clusters are named. Use when there are more than 5 clusters and the team needs to narrow to a focus, or before writing the Long-Term Goal and Sprint Questions.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Immediately after Affinity Map is completed and clusters are named
  - When there are more than 5 clusters and the team needs to narrow to a focus
  - Before writing the Long-Term Goal and Sprint Questions — the voted clusters are the input
  - Whenever the team has diverged significantly in Phase 1 and needs a convergence point before Phase 2
applies-to: HMW prioritisation, sprint focus selection, research synthesis closure, Phase 1→2 transition
done_when:
  - All HMWs are visible and clustered before voting
  - Votes are cast and the top HMWs are ranked
  - The winning HMWs are carried onto the sprint map/target
metadata:
  duration: 15–20 min
  team-size: Full sprint team; Decider makes final selection
  sprint-phase: 2 Define
  renamed-from: hmw-voting
---

# HMW Voting

**TL;DR:** After Affinity Mapping, the team has named clusters of HMW notes — but clusters are still just categories. HMW Voting is the explicit selection step: each person votes on the clusters they believe are most important for this sprint, and the Decider uses the vote results to select the 3–5 clusters that will become Sprint Questions. It is the formal close of the Understand phase and the opening of Define.

## When to use

- Immediately after Affinity Map is completed and clusters are named
- When there are more than 5 clusters and the team needs to narrow to a focus
- Before writing the Long-Term Goal and Sprint Questions — the voted clusters are the input
- Whenever the team has diverged significantly in Phase 1 and needs a convergence point before Phase 2

## How it differs from Note-and-Vote

[Note-and-Vote](../note-and-vote/SKILL.md) is the general-purpose silent prioritisation technique used throughout the sprint. HMW Voting is a specific application of that mechanic, with a particular input (Affinity Map clusters) and a particular output (cluster selection that feeds Sprint Questions). The mechanic is the same; the context and the stakes are different — this vote sets the sprint's direction.

## Steps

1. **Review the clusters (3 min):** All clusters are named and posted on the wall. Facilitator reads each cluster name and a sample of the stickies inside it. Everyone should understand what's in each cluster before voting.

2. **Allocate votes (1 min):** Each person gets 2 dot stickers (or digital equivalents). The Decider gets 3 dots — their vote has more weight in this step because they will ultimately own the Sprint Questions.

3. **Silent voting (3–5 min):** Each person places their dots on the clusters they believe are most important for the sprint. Dots go on the cluster label, not on individual stickies. No discussion until all dots are placed.

4. **Count and rank (2 min):** Facilitator counts dots per cluster. Call out the ranking: "Morning triage time: 7 dots. Priority trust gap: 6 dots. Assignment friction: 4 dots."

5. **Decider selects (3–5 min):** The Decider looks at the ranked list and selects 3–5 clusters to carry into Sprint Questions. The vote is advisory — the Decider may select a cluster with fewer dots if they have strategic reason to. They state their rationale in one sentence.

6. **Record the selection (2 min):** Facilitator writes the selected clusters on a separate sheet. These become the candidate Sprint Questions in the next method.

## Voting weight

| Person | Dots | Rationale |
|---|---|---|
| General team member | 2 | Equal voice; captures diverse perspectives |
| Facilitator | 0 | Neutral; facilitator doesn't vote |
| Decider | 3 | Higher weight; accountable for the decision |

The Decider's extra dot weight reflects their accountability — they own the outcome of the sprint direction, so their preference carries more weight in selecting the focus.

## Interpreting results

| Result | Interpretation | Action |
|---|---|---|
| One cluster with 60%+ of dots | Strong consensus | Decider likely agrees; proceed quickly |
| Two clusters roughly equal | Genuine choice | Decider chooses one, or names both as co-primary Sprint Questions |
| Spread across 4+ clusters | Team sees the problem broadly | Decider must scope — select the 2–3 most strategically important |
| Decider overrides plurality | Different strategic read | Decider explains rationale; team may challenge once before accepting |

## Output

```markdown
## HMW Voting Results — [Sprint Name] · [Date]

### Clusters ranked by votes
| Cluster | Dots | Selected? |
|---|---|---|
| Morning triage time | 8 | ✅ Sprint Question 1 |
| Priority trust gap | 7 | ✅ Sprint Question 2 |
| Assignment friction | 5 | ✅ Sprint Question 3 |
| Cross-site visibility | 3 | 🟡 Held — revisit if sprint scope allows |
| Mobile access | 1 | ❌ Out of scope this sprint |

### Decider's rationale
"I selected all three top clusters. Cross-site visibility is real but secondary — it would be a follow-on sprint. Mobile access is a corner case for this team."

### Clusters forwarded to Sprint Questions
1. Morning triage time
2. Priority trust gap
3. Assignment friction
```

## Agent facilitation guide

When facilitating HMW Voting:
1. List all clusters from the Affinity Map with their note counts
2. Assign synthetic dot weights based on: sprint strategic relevance + research signal strength (note count + evidence quality)
3. Rank clusters by synthetic vote score
4. Recommend the top 3 for Sprint Questions with rationale
5. Flag any cluster that has strong research signal but may be out of sprint scope — recommend it as a future sprint candidate, not just "dropped"

## Watch-outs

- **Voting on individual stickies, not clusters:** The vote is on the cluster (the theme), not on a specific HMW within it. Keep the scope at the cluster level here — the Sprint Questions step will make the focus more specific.
- **Decider deferring to the vote:** "Whatever the team chose" is not a Decider decision. The team's vote is input; the Decider's selection is the output.
- **Forgetting low-vote clusters:** A cluster with 1–2 dots from a single informed person may still be worth noting. Ask: "Did someone see something here that others missed?" before discarding it.
- **Treating this as final Sprint Questions:** HMW Voting selects the focus *areas*; Sprint Questions translates them into testable questions. Don't skip the Sprint Questions step.

## Connects to

- [Affinity Map](../affinity-map/SKILL.md) — clusters are the input
- [Note-and-Vote](../note-and-vote/SKILL.md) — the general mechanic this applies
- [Sprint Questions](../sprint-questions/SKILL.md) — selected clusters become Sprint Questions
- [Long-Term Goal](../long-term-goal/SKILL.md) — the dominant cluster shapes the Long-Term Goal framing
