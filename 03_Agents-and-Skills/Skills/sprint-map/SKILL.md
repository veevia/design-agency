---
name: sprint-map
title: Draw the simplified journey with HMWs placed
description: Build a simple, shared journey map that becomes the sprint's working surface — placing HMW notes, the target, and the design solution space on one artefact. Use after Expert Interviews and before Sketching. Use when the team has different understandings of how the user moves through the process, or as the physical surface on which HMW votes are placed and the sprint target is marked.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - After Expert Interviews and before Sketching — to create one shared mental model for the team
  - When the team has different understandings of how the user moves through the process
  - As the physical surface on which HMW votes are placed and the sprint target is marked
applies-to: sprint alignment, design focus, HMW placement, prototype storyboard anchor
done_when:
  - A 5–6 step end-to-end map from actor to goal is drawn
  - Key HMWs/opportunities are placed on the relevant steps
  - The target moment for the sprint is marked on the map
metadata:
  duration: 30–45 min
  team-size: Full sprint team
  sprint-phase: 2 Define
  renamed-from: map
---

# Map

**TL;DR:** The Map is a simplified version of the journey map — built collaboratively by the team in real time rather than researched in advance. It includes the key actors, a left-to-right journey from trigger to resolution, and the HMW notes placed at the moments they address. It becomes the shared reference for the rest of the sprint.

## When to use

- After Expert Interviews and before Sketching — to create one shared mental model for the team
- When the team has different understandings of how the user moves through the process
- As the physical surface on which HMW votes are placed and the sprint target is marked

## Map components

```
ACTORS (left column)                    JOURNEY (horizontal)                    END GOAL (right)

[Primary actor]     ────────────────────────────────────────────────────────►  [Success state]
[Supporting actor]  ──────►  (enters here)  ──────►  (exits here)
[System/tool]       ─────────────────────────────────────────────────────────►

                    Stage 1    Stage 2    Stage 3    Stage 4    Stage 5
                    [name]     [name]     [name]     [name]     [name]

HMW notes           [HMW]                [HMW]      [HMW★]
(placed on stages)                       (voted)    (target ★)
```

## Steps

1. **Draw the spine (5 min):** Draw a horizontal arrow across the board from "Trigger / Start" to "Goal / Success."
2. **Add actors (5 min):** List the key people/systems on the left. Each gets a row.
3. **Name the stages (10 min):** Collaboratively agree on 4–7 stages — the major chapters of the journey. Name them with verbs.
4. **Fill in key steps per actor (10 min):** Brief notes only — what does each actor do or experience at each stage? Not exhaustive — just enough for shared understanding.
5. **Place HMW notes (5 min):** Stick HMW notes from Phase 1 onto the relevant stages. Cluster if many land in the same place.
6. **Vote on HMWs (dot voting, 2 votes each):** Each team member places 2 dots on HMW notes they think are most important.
7. **Circle the target (2 min):** Mark the target moment (from [Target](../sprint-target/SKILL.md)) with a star or circle. This is the sprint focus.

## Simplification principle

The sprint Map is deliberately rough. It's not the detailed journey map from Phase 1 — it's a shared reference surface. Optimise for:
- Speed (30–45 min total)
- Alignment (everyone can see and point to it)
- Clarity (a visitor could read it in 30 seconds)

## Output format

```markdown
## Sprint Map — [Sprint Name]

**Actors:** Lead Coordinator (Primary), Site Supervisor (Site C), Request system (System), Senior specialist (Supporting)

**Journey:**
[Request arrives] → [Spot] → [Check ★] → [Assess] → [Assign] → [Track] → [Request resolved]

★ = Sprint target (Check stage — the coordinator cross-references the CRM, service-contract database, and inventory system and confirms the booking)

**HMW notes placed on map:**

| Stage | HMW notes | Vote count |
|---|---|---|
| Spot | HMW surface the urgent requests without hunting? | ●● |
| Spot | HMW reduce noise from duplicate and routine requests? | ● |
| **Check ★** | **HMW make checking a booking faster + more trustworthy?** | **●●●** (most voted) |
| Check | HMW show how urgent a request really is? | ●● |
| Assign | HMW give the coordinator visibility after they assign? | ● |

**Key actors' end goal:** The coordinator is confident about every urgent request's priority in < 10 min with no manual cross-referencing.
```

## Agent facilitation guide

When building a sprint map from existing artefacts (journey maps, JTBDs, PRD):
1. Extract the key actors from personas + JTBD analysis
2. Define the end goal from the Long-Term Goal statement
3. Map the stages from the existing journey map (simplified to 4–7)
4. Place existing HMW notes from the HMW method
5. Mark the target moment from the Target method
6. Output the map as a markdown table (above format) for async teams

## Watch-outs

- **Too detailed:** If you're writing full sentences per stage, stop. The map is a sketch.
- **Skipping actor rows:** The map shows a multi-actor system. Missing actors create blind spots (e.g., not showing the senior specialist's role in checking a booking).
- **HMW notes without votes:** Don't place notes and skip voting. The vote is what makes the HMWs actionable.
- **Forgetting to mark the target:** The target must be visually obvious. It anchors all subsequent sketch and prototype work.

## Connects to

- [How Might We](../how-might-we/SKILL.md) — HMWs are placed here
- [Target](../sprint-target/SKILL.md) — target moment is marked on this map
- [Solution Sketch](../solution-sketch/SKILL.md) — sketches must address the target stage
- [`00_README/_templates/1-4-Understand_journey-map.template.md`](../../../00_README/_templates/1-4-Understand_journey-map.template.md) — detailed version of this artefact
