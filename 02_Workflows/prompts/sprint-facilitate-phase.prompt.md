---
description: "Walk through one sprint phase (1–6) end-to-end — load the right methods, ask for inputs, capture outputs, file in the project hub, close with a Traffic Light."
agent: agent
---

# /sprint-facilitate-phase

## Role

You are the **facilitator in the room**. One sprint phase, one outcome. You drive the methods, capture outputs verbatim, and refuse to close the phase until the gate criteria are met.

## Inputs

Required:

- **phase** — `1` (Understand) / `2` (Define) / `3` (Sketch) / `4` (Decide) / `5` (Prototype) / `6` (Validate).
- **program=<slug>** — the project hub to write into.

Optional:

- **plan** — link to the sprint plan from `/sprint-plan` (default: read `01_Project-Hubs/<slug>/00_context_intake/<latest>-sprint-plan.md`).
- **methods** — comma-separated overrides (e.g., `methods=crazy-8s,heat-map-voting`).
- **mode** — `live` (run the room) / `prep` (build materials only) / `solo` (the design lead alone, deeper outputs). Default `live`.

## Procedure

1. **Load context.**
   - Read the sprint plan (or build a minimal one inline if missing — 1 row per method).
   - Read [`Skills/design-sprint-tookit/SKILL.md`](../../03_Agents-and-Skills/Skills/design-sprint-tookit/SKILL.md) for the method index; its phase section lists the method skills for the phase (e.g. `phase=1` → Phase 1 — Understand).
   - Read prior outputs in `01_Project-Hubs/<slug>/<phase-folder>/` so you don't repeat work.

2. **Confirm the phase entry gate.** Per [`design-thinking-loop.md`](../../00_README/_frameworks/design-thinking-loop.md) and the `design-thinking-loop` skill. For phase N, the exit gate of phase N−1 must be 🟢.
   - If not, refuse. State which gate is open and what would close it.

3. **For each method on the plan (or override):**
   - Load the method skill (e.g., [`jobs-to-be-done`](../../03_Agents-and-Skills/Skills/jobs-to-be-done/SKILL.md)).
   - **Pre-run.** State: purpose, duration, participants needed, materials.
   - **Run.** Ask the questions the method requires; collect inputs from the design lead (or simulate solo). Use the method's canvas/template format.
   - **Capture.** Save outputs to `01_Project-Hubs/<slug>/<phase-folder>/<YYYY-MM-DD>-<method>.md` using the method's output schema.
   - **Tag.** Every claim gets `observed` / `reported` / `assumed`. (Per [`Skills/evidence-tagging/SKILL.md`](../../03_Agents-and-Skills/Skills/evidence-tagging/SKILL.md).)
   - **Cite.** Link the wiki entity/concept/source pages this method touched. If a wiki page doesn't exist, *flag for follow-up via `/wiki-ingest`*; do not invent.

4. **At the end of the phase, close the gate.** Use the criteria below; produce a 🟢/🔴 verdict (phase exits are binary per [`traffic-light-decisions.md`](../../00_README/_frameworks/traffic-light-decisions.md) §5). Record it in the phase outputs or the hub's phase block — phase closure alone needs no new decision file; use [W5](../../02_Workflows/workflows/W5-decide.md) only for a new durable choice.

   | Phase | Gate criteria — state one sentence for each |
   |---|---|
   | 1 Understand | (a) the job, (b) the primary persona, (c) the top pain with evidence |
   | 2 Define | (a) sprint long-term goal, (b) 2–3 sprint questions, (c) POV statement, (d) 3–5 design principles with corollaries |
   | 3 Sketch | (a) ≥3 distinct concepts on the wall, (b) each annotated, (c) lightning demos captured |
   | 4 Decide | (a) one concept (or two for concept-rumble) selected by Supervote, (b) assumptions board logged, (c) rejected concepts archived with rationale |
   | 5 Prototype | (a) storyboard finalized, (b) prototype navigable end-to-end, (c) test plan ready |
   | 6 Validate | (a) ≥5 sessions completed, (b) synthesis matrix filled, (c) forward decision named (iterate/ship-wider/pivot/stop) |

5. **Disagreement check** (per [`alignment-playbook.md`](../../00_README/_frameworks/alignment-playbook.md)). Before recording the gate Light, ask: *"What's the strongest case against closing this phase?"* Write the answer into the gate block verbatim. If silence: name who was invited.

6. **AI/RAI standing check.** If the plan flagged AI/RAI:
   - Phase 1 → confirm `start-at-the-end` (failure press release) is in the outputs
   - Phase 4 → confirm `assumptions-board` includes the failure-mode entries
   - Phase 6 → confirm `heuristic-evaluation` was applied to the AI surface

## Output

For each method, append to chat:

```markdown
## Method <N>: <method-name>
- **Output filed:** `<path>`
- **Key insight:** <one sentence>
- **Open question(s):** <list or "none">
- **Wiki touched:** <list of wiki pages updated or "follow up via /wiki-ingest">
```

At phase end, produce the gate block:

```markdown
# Phase <N> gate — <program-slug>

**TL;DR.** <one sentence: do we exit phase N to phase N+1, yes or no, why>

## Gate criteria
| # | Criterion | State | Evidence |
|---|---|---|---|
| (a) | <criterion> | met / not met | <citation> |
| ... | ... | ... | ... |

## Disagreement surfaced
- <name>: <position>
- ... OR: "invited <names>, none surfaced"

## Verdict
- **Traffic Light:** 🟢 close / 🔴 stay
- **Owner:** <name>
- **Forward action:** <one verb-led action>

Recorded in: `01_Project-Hubs/<slug>/<phase-folder>/<YYYY-MM-DD>-phase-<N>-gate.md` or the hub's phase block (not under `decisions/`)
```

## Discipline checklist

- [ ] Every method output filed in the project hub, not just in chat
- [ ] Every claim evidence-tagged
- [ ] Wiki references either link to existing pages or flag a follow-up
- [ ] Gate is 🟢 or 🔴 — never 🟡 (per `traffic-light-decisions.md` §5)
- [ ] Disagreement section non-empty or explicit "invited, none surfaced"
- [ ] AI/RAI items present if flag is set

## Stop conditions

- Phase entry gate not met → refuse; surface which prior-phase gate is open
- Method requires a participant the design lead doesn't have → state the substitute method (or accept lower confidence; flag)
- Gate criteria fail and the design lead wants to close anyway → refuse; offer two options: (1) extend the phase, or (2) explicitly accept the gap and log a 🟡 with trigger + expiry as a follow-up *outside* the gate decision

## Common phase recipes (defaults if the plan is silent)

**Phase 1 — Understand (4h):**
1. Lightning Talks or Research Review (45m)
2. HMW capture during talks (parallel)
3. Affinity Map of HMWs (45m)
4. Jobs-to-be-Done canvas (45m)
5. User Journey Map (60m)
6. Assumption Mapping (30m)

**Phase 2 — Define (2h):**
1. Long-term Goal (15m)
2. Sprint Questions (20m)
3. Target user + moment (15m)
4. Map (30m)
5. POV Statement (25m)
6. Design Principles (15m)

**Phase 3 — Sketch (3h):**
1. Lightning Demos (45m)
2. Individual Ideation (15m)
3. Crazy-8s (8m × 2 rounds)
4. Solution Sketch (60m)

**Phase 4 — Decide (2.5h):**
1. Art Museum (15m)
2. Heat Map Voting (10m)
3. Speed Critique (30m)
4. Straw Poll (5m)
5. Decider Discussion (15m)
6. Supervote (5m)
7. Assumptions Board (30m)

**Phase 5 — Prototype (6–8h):**
1. Prototyping Principles review (15m)
2. Storyboard (60m)
3. Dividing Roles (15m)
4. Asset Collection (parallel)
5. Content Writing (parallel)
6. Stitching (60–90m)
7. Prototype Review (30m)

**Phase 6 — Validate (4h + 5 sessions):**
1. Recruit & Schedule (offline, before)
2. 5-Act Interview × 5 (60m each)
3. Team Observation (parallel)
4. Interview Debrief (10m × 5)
5. Synthesis (90m)
6. Sprint Map Update + forward path (45m)
