---
name: sprint-target
title: Pick the user and moment to design for
description: Pick the one user and the one moment in their journey that the sprint will solve for. Precision prevents scope sprawl. Use after the journey map is built and HMW notes are clustered. Use when the team has multiple personas and can't agree which one to focus on, or when the sprint scope keeps expanding ("but what about the global admin user?").
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - After the journey map is built and HMW notes are clustered
  - When the team has multiple personas and can't agree which one to focus on
  - When the sprint scope keeps expanding ("but what about the global admin user?")
applies-to: sprint scoping, persona selection, design POV framing, prototype script writing
done_when:
  - A single target user and target moment are chosen
  - The choice is justified against the long-term goal
  - The target is marked on the sprint map
metadata:
  duration: 20–30 min
  team-size: Full sprint team + Decider
  sprint-phase: 2 Define
  renamed-from: target
---

# Target

**TL;DR:** The Target pins down who the sprint is designing for and which specific moment in their journey the solution must improve. Without a target, teams prototype for everyone and test with no one in particular. With a target, every design decision has a reference point.

## When to use

- After the journey map is built and HMW notes are clustered
- When the team has multiple personas and can't agree which one to focus on
- When the sprint scope keeps expanding ("but what about the global admin user?")

## Two questions to answer

1. **Who?** — Which actor (persona) are we designing for in this sprint?
2. **Where in their journey?** — Which moment (stage on the journey map) is the sprint's focus?

## The target format

```
Target User:   [Persona name + role description]
Target Moment: [Stage name from the journey map — the moment the sprint will improve]
```

The target moment is the one stage where:
- Pain is highest (biggest drop on the emotional arc)
- The team has the most design leverage
- A sprint-sized solution could make a meaningful difference

## Steps

1. **Review the journey map (5 min):** Post the journey map visibly. Review the emotional arc and pain points.
2. **Review HMW clusters (5 min):** Which clusters have the most votes? Which stages on the map do they attach to?
3. **Persona vote (5 min):** If there are multiple candidate personas, each person votes for the one that represents the most leverage for the sprint.
4. **Moment vote (5 min):** Each person puts a dot on the stage they think should be the sprint focus. Decider breaks ties.
5. **State the target explicitly:** Write it large on the board. This is the constraint for the rest of the sprint.
6. **Confirm non-targets:** Explicitly name the personas and moments you're *not* targeting in this sprint.

## Choosing between actors

When there are multiple personas (e.g., lead coordinator + site supervisor + senior specialist):

| Actor | Choose if... |
|---|---|
| Primary persona (heaviest user) | Sprint addresses routine high-frequency workflows |
| Influencer/approver persona | Sprint is about adoption or buy-in |
| "Extreme user" (edge case power user) | Sprint needs to uncover hidden requirements |
| New/novice user | Sprint tests the learning curve or onboarding |

## Output format

```markdown
## Sprint Target — [Sprint Name]

**Target User:** Lead Coordinator (sorts and assigns every overnight request)

**Target Moment:** Stage 2 — Check
*The moment the coordinator cross-references several systems and asks a senior specialist to confirm a request's urgency. This is the highest-pain moment and the stage where the most time is lost.*

**Why this moment:**
- Emotional arc lowest point in journey map [observed | 2026-02-17-coordinator-deepdive]
- HMW "make checking a booking faster + more trustworthy" received the most votes on the sprint map
- Assumption: if we reduce checking friction, the coordinator can sort the morning queue 4× faster

**Non-targets (explicitly out of scope for this sprint):**
- Site supervisors (Site A, Site B, Site C) — will be targeted in a second sprint
- Senior specialists (urgency checks on request) — inputs to the flow, not the primary actor
- Post-assignment tracking — deferred to a later sprint
```

## Agent facilitation guide

When helping a team select a sprint target from existing artefacts:
1. Read the journey map and identify the 2–3 highest-pain moments (deepest emotional arc dips)
2. Read the HMW voting results — which clusters got the most votes?
3. Cross-reference: the target moment is where pain + HMW votes + assumed design leverage converge
4. Propose target user + moment with a one-sentence rationale
5. List non-targets explicitly — this is as important as the target itself

## Watch-outs

- **"Everyone is a user":** There is no sprint where "all personas equally" is the right answer. The Decider picks one. Other personas get their sprint later.
- **Targeting a moment with no HMW votes:** If the team mapped a painful moment but no one wrote HMWs for it, it might not be the design opportunity — it might be an ops problem.
- **Target shifting mid-sprint:** Once set, the target is fixed for the sprint. If it needs to change, call a pause and reset explicitly.

## Connects to

- [User Journey Map](../user-journey-map/SKILL.md) — the target moment comes from the map
- [Map](../sprint-map/SKILL.md) — the target is plotted on the simplified sprint map
- [Solution Sketch](../solution-sketch/SKILL.md) — all sketches must address the target moment
- [`00_README/_templates/2-1-Design_POV.template.md`](../../../00_README/_templates/2-1-Design_POV.template.md) — §Who we design FOR
