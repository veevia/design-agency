---
title: "Design Thinking Loop — the canonical 4-phase process"
type: framework
status: canonical
owner: OS steward
last-updated: 2026-10-29
source: Design-thinking practice, synthesized with Extreme Clarity + Alignment Playbook + Traffic Light discipline
tags: [type/framework, purpose/align, status/canonical, loop/understand, loop/design, loop/build, loop/learn]
---

# Design Thinking Loop

> **TL;DR:** Four phases, iterated — **Understand → Design → Build → Learn**. Every engagement and every feature moves through this loop. Clarity at each gate; alignment before moving on.

```
    ┌────────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ UNDERSTAND │───▶│  DESIGN  │───▶│  BUILD   │───▶│  LEARN   │
    └────────────┘    └──────────┘    └──────────┘    └──────────┘
         ▲                                                   │
         └───────────────────────────────────────────────────┘
```

It deliberately replaces heavier stage-gate engagement flows and generic "Understand → Prompt → Evaluate → Ship → Learn" AI primers. It's the spine of this OS, and it fits forward-deployed (FDE) work: short loops, real users, evidence before scale.

This is the project lifecycle, not a required workflow for every question or small change. Individual
tasks use the [Agentic-OS operating guide](../../00_Agentic-OS/README.md) proportionately.

---

## The four phases

### 1. UNDERSTAND — "What's the real problem, and for whom?"

The phase most often skipped. Most failed features trace back to missing this phase.

**Intent:** Before proposing a solution, know the users, the job they're hiring the product to do, and the current journey — including where it fails.

**Canonical artifacts:**

- **Problem Frame** (`1-0-Understand_problem-frame.template.md`) — the pre-research frame: the problem in the user's language, the decisions to enable, the feasibility gap; gates entry into research
- **UX Research Report** (`1-1-Understand_research-report.template.md`) — evidence from interviews, observation, analytics
- **UX Survey** (`1-2-Understand_UX_survey.template.md`) — structured input from many users to quantify and validate what interviews surface
- **JTBD** (`1-3-Understand_jtbd.template.md`) — the job, the current solution, the switching triggers; `1-3b-Understand_jtbd-synthesis.template.md` rolls several JTBD analyses into workstreams
- **User Journey Map** (`1-4-Understand_journey-map.template.md`) — stages, thoughts, feelings, pain points, opportunities
- **Persona** — evidence-grounded user archetype synthesized from the research (no standalone template; not demographic fiction)

**Discipline (evidence tagging — [House principle §4](house-principles.md#4-evidence--opinion-but-evidence-is-rare)):** Every claim in UNDERSTAND is tagged as **observed** (direct user evidence), **reported** (third-party claim), or **assumed** (team hypothesis). Assumptions aren't forbidden — unlabeled assumptions are.

**Gate to DESIGN:** You can state the job in one sentence, the primary persona in one sentence, and the top pain point with evidence. If not, stay in UNDERSTAND.

### 2. DESIGN — "What point of view are we taking, and what are we asking to be built?"

**Intent:** Translate understanding into a committed design stance and a brief a team can build from.

**Canonical artifacts:**

- **Design POV** (`2-1-Design_POV.template.md`) — the opinionated stance: for whom, against what, why now
- **Design Brief** (`2-2-Design_brief.template.md`) — the client/team-facing framing: problem, audience, outcomes, constraints
- **Product PRD** (`2-3-Design_PRD.template.md`) — the buildable spec: users, stories, requirements, rollout, open questions
- **Design Handoff** (`2-4-Design_handoff.template.md`) — the bridge to engineering: screens, states, interactions, accessibility, what's not in Figma

**Discipline (from `extreme-clarity.md`):** TL;DR at the top of every artifact. One sentence that survives the 10-second test. Numbers, not adjectives.

**Gate to BUILD:** PRD is signed (Traffic Light 🟢) by the decision owner. Open questions are either answered or logged as 🟡 with a trigger and expiry.

### 3. BUILD — "Make the smallest thing that proves the point."

**Intent:** Prototype and ship the thinnest possible slice that tests the riskiest assumption.

**Canonical artifacts:**

- **Prototype** (Figma, code, paper — format fits the fidelity needed)
- **Test plan** (`3-1-Build_test-plan.template.md`) — hypothesis, metrics, counter-metrics, protocol, rollback trigger
- **Decision rationale** — reuse existing task/artifact evidence; new durable choices go through [W5](../../02_Workflows/workflows/W5-decide.md) only when needed
- Weekly **status** (`0-2-Ops_operating-rhythm.template.md` §C) — opt-in, only when the project has a real reporting cadence

**Discipline (from `traffic-light-decisions.md`):** Every ADR and PDR closes with exactly one 🟢🟡🔴. Yellow has a trigger + expiry; Red has an unblock owner.

**Gate to LEARN:** Something is shippable to a real user or representative test audience.

### 4. LEARN — "What did we learn, and what does it change?"

**Intent:** Measure against the PRD's success metrics. Decide: iterate, ship wider, or pivot.

**Canonical artifacts:**

- **Evidence brief** (`4-1-Learn_evidence-brief.template.md`) — what shipped vs. what we learned, with metrics actuals
- **Retro** (`4-2-Learn_retro.template.md`) — what worked, what didn't, owned action items
- **Updated artifacts** — journey map, persona, POV amended with evidence

**Discipline:** Distinguish **what we shipped** from **what we learned**. Most teams skip the second; it's the only thing that compounds.

**Gate back to UNDERSTAND:** Learnings feed the next loop. The journey map isn't frozen — it's versioned.

---

## Loop discipline

### The loop is not a waterfall

You will move backwards. UNDERSTAND insights surface in BUILD. LEARN results send you back to DESIGN. That's the point. The failure mode is pretending you finished UNDERSTAND when you didn't — and building on shaky ground.

### Each phase has a single exit gate

Named in the framework above. The gate is binary: met or not met. Don't negotiate exit gates — if you can't state the TL;DR, stay in the phase.

### Every phase produces at least one artifact

No invisible work. If UNDERSTAND is "done" but no research report or journey map exists, UNDERSTAND isn't done.

### Disagreement surfaces at gates

Per `alignment-playbook.md`: before closing a phase, explicitly ask "what's the strongest case against
moving on?" Preserve real feedback in the existing phase artifact or gate evidence; do not fabricate
dissent. Phase closure alone needs no new decision file. Use W5 for a new durable choice, explicit
capture request, or lifecycle change.

---

## How it maps to workflows

Each phase has a workflow in [`02_Workflows/workflows/`](../../02_Workflows/workflows/) that walks the artifact chain:

| Phase | Workflow | Produces |
|---|---|---|
| Understand | [`W1-understand.md`](../../02_Workflows/workflows/W1-understand.md) | Problem frame → Research report → Persona → JTBD → Journey Map |
| Design | [`W2-design.md`](../../02_Workflows/workflows/W2-design.md) | POV → Brief → PRD → Handoff |
| Build | [`W3-build.md`](../../02_Workflows/workflows/W3-build.md) | Prototype + test plan (+ weekly status, if the hub opted in) |
| Learn | [`W4-learn.md`](../../02_Workflows/workflows/W4-learn.md) | Evidence brief + retro + updated artifacts |
| Cross-cutting | [`W5-decide.md`](../../02_Workflows/workflows/W5-decide.md) | Typed decision record (ADR only for architecture), invoked from any phase when needed |

Engine plug-ins can run inside a phase: a prototype-design (PDG) run or a video-production (VPG) film lives in the hub's `03_build/<name>/` folder. See [`PLUGINS.md`](../PLUGINS.md).

---

## How it relates to the disciplines

The disciplines operate across all four phases; they're the connective tissue.

- **[`extreme-clarity.md`](extreme-clarity.md)** — how every artifact is written (TL;DR, numbers, no hedge)
- **[`alignment-playbook.md`](alignment-playbook.md)** — how gates close (surface disagreement, commit verbatim)
- **[`traffic-light-decisions.md`](traffic-light-decisions.md)** — how decisions are logged (one light, required fields)
- **[`house-principles.md`](house-principles.md)** — working principles
- **[`long-horizon-execution.md`](long-horizon-execution.md)** — how agents run long tasks to a verified finish

---

## Anti-patterns to catch

- **Solution-first:** jumping from client request to DESIGN without UNDERSTAND
- **Research theatre:** UNDERSTAND phase with a 40-page report that nobody references in DESIGN
- **PRD by committee:** DESIGN phase where nobody is the decision owner
- **Forever-POC:** BUILD phase that never ships anything a real user sees
- **Ship-and-forget:** no LEARN phase; no measurement against PRD metrics
- **Frozen artifacts:** journey map from Month 1 that nobody updated when evidence changed

---

*This is the canonical process. Everything else in this OS either supports it or is retired.*
