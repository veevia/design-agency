---
name: design-sprint-tookit
title: Plan and facilitate a right-sized design sprint
description: "Plan, facilitate, and close design-sprint workshops with a library of 62 method skills across six phases (Understand, Define, Sketch, Decide, Prototype, Validate), from a half-day alignment session to a five-day sprint. Use when planning a workshop or sprint, when a team is stuck on the problem, the ideas, or the choice, when you need the right facilitation method for the moment, or when a prototype needs user signal before a decision."
status: stable
when_to_load:
  - Planning a workshop, sprint, or solo design session and choosing its format
  - A team disagrees on the problem, has no ideas, or cannot pick between ideas
  - Facilitating one sprint phase and needing the method steps, timings, and outputs
  - A prototype exists and needs structured user validation
  - A Yellow decision is blocked on an untested assumption
applies-to: workshop planning, problem framing, stakeholder alignment, ideation, convergence, prototyping decisions, user testing sessions
narrative: 00_README/_frameworks/design-thinking-loop.md
contract-exempt: "facilitation method library — a knowledge skill the agent reads per method; it emits no files of its own and has no file globs to lint"
done_when:
  - The sprint format matches the time, people, and customer readiness available, and its trade-off is stated
  - Every method used is cited by its method skill and produced its named output
  - Each phase closes with its outputs filed in the project hub and a Traffic Light on the phase decision
  - Assumptions surfaced in Understand are either tested in Validate or carried forward as named Yellow conditions
loads: [design-thinking-loop, evidence-tagging, alignment-playbook]
---

# Design Sprint Toolkit

**TL;DR:** Pick the smallest sprint format that answers the team's real question, run the matching method skills for each of the six phases, and close every phase with filed outputs and a Traffic Light.

## When to use

- A fuzzy problem needs to become an aligned, tested solution in two to five days.
- A team is stuck — on the problem (Understand, Define), on ideas (Sketch), or on the choice (Decide).
- A concept needs a realistic-enough prototype and five user sessions before anyone commits.

## Steps

1. **Diagnose first.** Name the phase the team is in, the gap it cannot state in one sentence, the decider, the time available, and the riskiest assumption. If three or more are unknown, run Phase 1 + 2 before anything else.
2. **Right-size the format** with the format table below and state what the chosen size will not give you.
3. **Pick methods per phase** from the method index. Load only the method skills you will run.
4. **Facilitate and capture verbatim.** Follow each method skill's steps and timing; record outputs as evidence-tagged notes (`evidence-tagging`).
5. **Surface disagreement before each convergence** (`alignment-playbook`): who disagrees, and with what evidence.
6. **Close each phase** — file outputs in the project hub phase folder and set a Traffic Light on the phase decision (`traffic-light-decisions` via W5 only when a durable record is needed).

## The six phases

| Phase | Goal | Key question | Duration |
|---|---|---|---|
| **1 — Understand** | Shared knowledge of the problem space | What do we know? What don't we know? | 2–4 h |
| **2 — Define** | Aligned direction: goal, questions, target | Where are we going? What must be true? | 1–2 h |
| **3 — Sketch** | Divergent ideas — many possibilities | What could the solution look like? | 2–4 h |
| **4 — Decide** | Converge on one (or two) concepts to build | What are we building and why? | 2–3 h |
| **5 — Prototype** | Build a realistic-enough artefact to test | What does it feel like to use? | 4–8 h |
| **6 — Validate** | Test with real users; update beliefs | Were we right? What did we learn? | 4–6 h |

## Method index

Each method is a native skill at `03_Agents-and-Skills/Skills/<method>/SKILL.md`.

### Phase 1 — Understand (18 methods)
- [`lightning-talks`](../lightning-talks/SKILL.md) — Expert presentations to the full team; HMW captured in parallel
- [`expert-interviews`](../expert-interviews/SKILL.md) — 1:1 structured talks with domain experts
- [`how-might-we`](../how-might-we/SKILL.md) — Convert problems into opportunity questions
- [`affinity-map`](../affinity-map/SKILL.md) — Cluster HMW notes into themes silently, then name
- [`note-and-vote`](../note-and-vote/SKILL.md) — Silent simultaneous prioritisation; used across all phases
- [`user-journey-map`](../user-journey-map/SKILL.md) — Map current-state experience end-to-end
- [`empathy-map`](../empathy-map/SKILL.md) — What users say, think, do, and feel
- [`persona`](../persona/SKILL.md) — Evidence-grounded user profile; primary vs. secondary
- [`competitive-landscape`](../competitive-landscape/SKILL.md) — Rapid audit of analogous solutions
- [`research-review`](../research-review/SKILL.md) — Synthesise existing research before the sprint starts
- [`assumption-mapping`](../assumption-mapping/SKILL.md) — Surface and rank the riskiest beliefs
- [`jobs-to-be-done`](../jobs-to-be-done/SKILL.md) — "When [situation], I want to [motivation], so I can [outcome]" canvas
- [`stakeholder-map`](../stakeholder-map/SKILL.md) — Power/interest grid of everyone who influences the problem
- [`start-at-the-end`](../start-at-the-end/SKILL.md) — Write the failure press release before designing anything
- [`five-whys`](../five-whys/SKILL.md) — Iterative root cause analysis
- [`fishbone-diagram`](../fishbone-diagram/SKILL.md) — Cause-and-effect map with six cause categories
- [`rose-bud-thorn`](../rose-bud-thorn/SKILL.md) — What's working, what's emerging, what's painful
- [`ecosystem-map`](../ecosystem-map/SKILL.md) — Map all actors, tools, and data flows in the system

### Phase 2 — Define (10 methods)
- [`long-term-goal`](../long-term-goal/SKILL.md) — Aspirational 2-year north star
- [`sprint-questions`](../sprint-questions/SKILL.md) — Questions this sprint must answer
- [`sprint-target`](../sprint-target/SKILL.md) — User and moment to design for
- [`sprint-map`](../sprint-map/SKILL.md) — Simplified journey + HMW placement
- [`pov-statement`](../pov-statement/SKILL.md) — "[User] needs [need] because [insight]" — the sprint's design brief in one sentence
- [`how-might-we-voting`](../how-might-we-voting/SKILL.md) — Prioritise HMW notes from Understand with dot voting
- [`design-criteria`](../design-criteria/SKILL.md) — Testable standards a winning concept must meet
- [`success-metrics`](../success-metrics/SKILL.md) — Observable signals that define sprint success
- [`constraint-mapping`](../constraint-mapping/SKILL.md) — Hard constraints vs. soft assumptions the team must respect
- [`design-principles`](../design-principles/SKILL.md) — 3–5 guiding values the team commits to in every design decision

### Phase 3 — Sketch (5 methods)
- [`lightning-demos`](../lightning-demos/SKILL.md) — 3-min demos of inspiring existing solutions
- [`individual-ideation`](../individual-ideation/SKILL.md) — Solo notes and ideas before group sketching
- [`mind-mapping`](../mind-mapping/SKILL.md) — Free-association expansion of one concept
- [`crazy-8s`](../crazy-8s/SKILL.md) — 8 variations in 8 minutes
- [`solution-sketch`](../solution-sketch/SKILL.md) — Detailed 3-panel concept + annotation

### Phase 4 — Decide (9 methods)
- [`art-museum`](../art-museum/SKILL.md) — Silent review of all sketches
- [`heat-map-voting`](../heat-map-voting/SKILL.md) — Dot stickers on compelling elements
- [`speed-critique`](../speed-critique/SKILL.md) — Structured 3-min sketch critique
- [`straw-poll`](../straw-poll/SKILL.md) — Non-binding team preference vote
- [`supervote`](../supervote/SKILL.md) — Decider's binding final vote
- [`assumptions-board`](../assumptions-board/SKILL.md) — Risk matrix: importance × certainty
- [`decision-matrix`](../decision-matrix/SKILL.md) — Weighted scoring of concepts against criteria
- [`i-like-i-wish-what-if`](../i-like-i-wish-what-if/SKILL.md) — Structured appreciative critique: positive, wish, generative
- [`concept-rumble`](../concept-rumble/SKILL.md) — Parallel prototyping of two competing concepts with an explicit decision trigger

### Phase 5 — Prototype (10 methods)
- [`prototyping-principles`](../prototyping-principles/SKILL.md) — What makes a testable prototype; goldilocks fidelity guidance
- [`storyboard`](../storyboard/SKILL.md) — 10–15 panel scene-by-scene script from the winning sketch
- [`dividing-roles`](../dividing-roles/SKILL.md) — Makers, Stitcher, Writer, Asset Collector, Interviewer
- [`wizard-of-oz`](../wizard-of-oz/SKILL.md) — Simulate AI/complex backend with a human operator
- [`paper-prototype`](../paper-prototype/SKILL.md) — Low-fidelity physical prototype for flow and structure testing
- [`video-prototype`](../video-prototype/SKILL.md) — Narrated screen walkthrough for async testing and stakeholder sharing
- [`content-writing`](../content-writing/SKILL.md) — Write realistic copy for every prototype screen
- [`asset-collection`](../asset-collection/SKILL.md) — Gather images, icons, and data before Makers start building
- [`prototype-review`](../prototype-review/SKILL.md) — Internal quality check before participants arrive
- [`stitching`](../stitching/SKILL.md) — Assemble components into a coherent navigable click-through flow

### Phase 6 — Validate (10 methods)
- [`recruit-and-schedule`](../recruit-and-schedule/SKILL.md) — Find and confirm 5 participants; screener + logistics
- [`five-act-interview`](../five-act-interview/SKILL.md) — Structured 60-min user interview protocol
- [`team-observation`](../team-observation/SKILL.md) — Live observation + assumption tracking grid
- [`research-synthesis`](../research-synthesis/SKILL.md) — Pattern finding, insight voting, forward decision + ADR
- [`heuristic-evaluation`](../heuristic-evaluation/SKILL.md) — Expert review against the 10 usability heuristics
- [`desirability-testing`](../desirability-testing/SKILL.md) — Product Reaction Cards for emotional response and brand fit
- [`post-test-survey`](../post-test-survey/SKILL.md) — SUS or custom quantitative questionnaire after each session
- [`usability-metrics`](../usability-metrics/SKILL.md) — Task completion rate, time-on-task, and error rate
- [`interview-debrief`](../interview-debrief/SKILL.md) — 10-min team debrief immediately after each session
- [`sprint-map-update`](../sprint-map-update/SKILL.md) — Update sprint artifacts with validated knowledge; file forward ADR

## When to load which phase

| Situation | Start here |
|---|---|
| Team doesn't agree on the problem | Phase 1 + 2 |
| Problem is clear, ideas are missing | Phase 3 |
| Too many ideas, can't pick | Phase 4 |
| Decision made, need to communicate it | Phase 5 |
| Prototype exists, need user signal | Phase 6 |
| Assumptions are blocking a 🟡 decision | Phase 1 ([`assumption-mapping`](../assumption-mapping/SKILL.md)) + Phase 4 ([`assumptions-board`](../assumptions-board/SKILL.md)) |

## Output format

Sprint formats — pick one and name its trade-off:

| Format | Phases used | Duration |
|---|---|---|
| Full sprint | 1 → 6 | 5 days |
| Compressed sprint | 2 → 4 → 6 (with lightweight 1 + 5) | 3 days |
| Problem alignment workshop | 1 + 2 | Half day |
| Ideation workshop | 3 + 4 | Half day |
| Assumption testing session | 1 (assumption mapping) + 6 | 1 day |
| Solo sprint (design lead) | All phases, solo outputs | 2–3 days |

Each phase closes with this block in the project hub phase folder:

```markdown
## <Phase> — closed YYYY-MM-DD
**TL;DR:** <what the team now knows or decided, one sentence>
- Methods run: <method skills>
- Outputs: <paths>
- Disagreement heard: <Name (role): position> or "invited; none surfaced"
- Phase decision: 🟢|🟡|🔴 <one line> (Yellow: trigger + expiry)
```

## How sprint concepts map to this OS

| Design Sprint concept | Design Agency OS equivalent |
|---|---|
| Long-term goal | POV TL;DR + goals section |
| Sprint questions | Design brief: open debate questions |
| Target user + moment | Persona + journey moment of truth |
| Assumptions board | Traffic Light (🟡 with trigger = assumption) |
| Supervote | Decider in the sign-off row |
| Forward decision | Learn-phase forward path (iterate / pivot / ship wider) |

## Watch-outs

- **Method before diagnosis.** Picking a workshop format before naming the gap produces a busy day and no decision.
- **Five days nobody can attend.** Right-size to the people actually available; a compressed sprint beats an absent decider.
- **Fictional examples are not evidence.** The worked examples inside the method skills are illustrations; never cite them as research.
- **Skipping Validate.** A sprint that ends at Prototype has produced an opinion, not a learning.

## See also

- `design-thinking-loop` — the four-phase loop these sprint phases map into
- `canonical-artifacts` — where sprint outputs land as POV, brief, PRD, and test plan
- `alignment-playbook`, `evidence-tagging`, `traffic-light-decisions` — the disciplines every phase closes with
- Agent: [`design-sprint-toolkit.agent.md`](../../../03_Agents-and-Skills/Agents/design-sprint-toolkit.agent.md) and its `sprint-*` prompts in `02_Workflows/prompts/`
- Templates: [`00_README/_templates/2-1-Design_POV.template.md`](../../../00_README/_templates/2-1-Design_POV.template.md) (Define outputs) · [`00_README/_templates/3-1-Build_test-plan.template.md`](../../../00_README/_templates/3-1-Build_test-plan.template.md) (Validate structure)
