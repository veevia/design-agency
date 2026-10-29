---
name: affinity-map
title: Cluster scattered notes into named themes
description: Cluster all HMW sticky notes from talks and interviews into themes — silently, then label — to reveal the problem space structure. Use after all Lightning Talks and HMW note-taking are complete, before defining Sprint Questions. Use when the team has more than 20 HMW sticky notes and needs to find themes.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Immediately after all Lightning Talks and HMW note-taking are complete
  - Before defining Sprint Questions — the clusters show which problem areas have the most signal
  - When the team has more than 20 HMW sticky notes and needs to find themes
  - Any time you need to move from raw observations to named patterns
applies-to: HMW synthesis, theme identification, shared vocabulary, sprint question prep, problem space mapping
done_when:
  - Every sticky/note is placed in exactly one cluster
  - Each cluster has a 1–2 word name that states its theme
  - Clusters are ranked or voted so the top themes are explicit
metadata:
  duration: 20–30 min
  team-size: Full sprint team
  sprint-phase: 1 Understand
---

# Affinity Map

**TL;DR:** After Lightning Talks and Expert Interviews, the team has a wall of HMW sticky notes — sometimes 50–100 or more. Affinity Mapping is the synthesis step that turns a pile of individual observations into a structured view of the problem space. The team clusters the notes silently, then names each cluster. The clusters become the candidate focus areas for the sprint's Long-Term Goal and Sprint Questions.

## When to use

- Immediately after all Lightning Talks and HMW note-taking are complete
- Before defining Sprint Questions — the clusters show which problem areas have the most signal
- When the team has more than 20 HMW sticky notes and needs to find themes
- Any time you need to move from raw observations to named patterns

## Materials

- All HMW sticky notes from the session (one idea per note, written during talks)
- A large blank wall or whiteboard
- Markers for labeling clusters (different colour from HMW stickies)
- Timer

## The two-step structure

Affinity Mapping happens in two distinct steps:

1. **Silent clustering (divergent):** Team members move stickies into groups based on similarity — without explaining their choices.
2. **Naming (convergent):** Team names each cluster with a short phrase that captures the theme.

The silence in step 1 is essential. Verbal discussion while clustering produces social dynamics — people defer to whoever speaks first, move stickies to please the loudest voice, or get into semantic debates about individual notes. Silent clustering produces an honest picture of where the team perceives patterns.

## Steps

1. **Post all HMW notes on the wall (3 min):** Everyone posts their stickies — randomly, without pre-sorting. Large wall, notes spread out.

2. **Read the wall (2 min):** Everyone silently reads the full set of notes. Get a sense of the volume and variety before touching anything.

3. **Silent clustering (10–15 min):** Everyone simultaneously moves stickies into groups. If two people keep separating a note into different groups, let it be in both (duplicate it). No talking. If someone moves a note you just placed, move it back or leave it — this is information about genuine ambiguity.

4. **Observe the clusters (2 min):** Step back. Where are the big clusters? Where are isolated notes? What surprised you?

5. **Name each cluster (5–10 min):** Now the team talks. Collaboratively name each cluster — one short phrase that captures the theme, written on a different colour sticky and posted above the cluster. Names should be HMW-style ("How might we reduce morning triage time?") or theme-style ("Priority trust gap").

6. **Identify the top clusters (3 min):** Quickly vote — each person places a small dot on the 2–3 clusters that feel most important for the sprint. This dot vote is non-binding; it feeds into Sprint Questions selection.

## Reading the affinity map

| Pattern | Interpretation |
|---|---|
| One very large cluster | Team sees this as the central problem; likely a Sprint Question |
| Many small clusters | Problem space is fragmented; team may need to scope down more |
| Isolated notes (no cluster) | Either a hidden insight worth naming, or an outlier — ask who wrote it |
| Two clusters that keep merging | The boundary between them is fuzzy; they may be one theme |
| Clusters with no HMW notes | You have a gap in your research — missing a user or a workflow |

## Naming clusters

Good cluster names are:
- Specific enough to distinguish clusters from each other
- Short enough to fit on one sticky
- Phrased as a theme, not a solution ("Priority trust" not "Add AI explainability")
- Honest about the problem, not aspirational ("Assignment friction" not "Efficient assignment")

Examples:

| Cluster name | What it captures |
|---|---|
| Morning triage time | All notes about the effort the coordinator spends sorting unconfirmed requests |
| Priority trust gap | Notes about coordinator hesitation to act on the suggested priority alone |
| Assignment friction | Notes about the 7-step manual assignment process |
| Cross-site visibility | Notes about requests that need more than one site or coordinator |
| Mobile access | Notes about accessing the tool away from the coordination desk |

## Agent facilitation guide

When synthesising HMW notes into an affinity map:
1. Read all HMW notes collected from the sprint
2. Identify recurring themes — group by semantic similarity, not by surface word matching
3. Name each cluster (2–5 words; theme-style, not solution-style)
4. Count notes per cluster — clusters with ≥5 notes represent high-signal areas
5. Flag isolated notes with strong specificity ("One-tap assign to the right specialist") — these are candidates for Sprint Questions even without a cluster

Output:
```markdown
## Affinity Map — [Sprint Name] · [Date]

| Cluster name | Note count | Theme summary | Candidate for Sprint Question? |
|---|---|---|---|
| Morning triage time | 14 | Speed of manual sorting is the primary daily friction | ✅ High |
| Priority trust gap | 11 | Coordinators won't act on a suggested priority without understanding the basis | ✅ High |
| Assignment friction | 9 | 7-step assignment process creates delays and wrong assignments | ✅ Medium |
| Cross-site visibility | 5 | Requests that cross site boundaries fall through gaps | ⚠️ Medium |
| Mobile access | 3 | Intermittent: some coordinators work from the site floor, most are desktop | ❌ Low (limited evidence) |

**Top clusters by vote:** Morning triage time (4 dots), Priority trust gap (4 dots), Assignment friction (3 dots)

**Isolated notes worth naming:**
- "What if the system pre-filled the assignment form based on request type?" — assignment solution seed
- "How might we show coordinators which urgent requests they almost missed?" — visibility angle

**Recommendation for Sprint Questions:** Prioritise the top 3 clusters; cross-site visibility is a candidate if the Decider sees it as high-stakes.
```

## Watch-outs

- **Clustering before everyone has read the notes:** Give the team 2 minutes to read the full wall before touching anything. Clustering without reading produces arbitrary groups.
- **One person dominating the clustering:** If the Decider starts clustering and others follow their lead, you've lost the independent signal. Enforce silence.
- **Naming clusters too quickly:** Rushed cluster names tend to be generic ("User experience issues"). Good names take a second pass. Read the notes inside the cluster before writing the name.
- **Treating the map as final:** The affinity map is an input to Sprint Questions, not a deliverable. It will be refined as the sprint progresses.
- **Forgetting isolated notes:** Notes that don't cluster can be the most surprising insights. Before discarding them, ask "Is this an outlier, or is this something no one else noticed yet?"

## Connects to

- [How Might We](../how-might-we/SKILL.md) — HMW notes are the raw material for the affinity map
- [Lightning Talks](../lightning-talks/SKILL.md) — the primary source of HMW notes
- [Expert Interviews](../expert-interviews/SKILL.md) — additional HMW notes from interviews add to the map
- [Sprint Questions](../sprint-questions/SKILL.md) — top clusters become candidate Sprint Questions
- [Long-Term Goal](../long-term-goal/SKILL.md) — the dominant cluster theme often shapes the Long-Term Goal framing
