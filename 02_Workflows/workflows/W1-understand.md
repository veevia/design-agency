---
title: "W1 — Understand"
type: workflow
workflow-id: W1
status: canonical
owner: OS steward
last-updated: 2026-10-29
loop-phase: understand
inputs:
  - A vague or well-formed problem statement from a stakeholder
  - Access to users (real users, not proxies) or a plan to get access
outputs:
  - problem-frame.md
  - ux-research-report.md
  - persona.md (1-3)
  - jtbd.md
  - user-journey-map.md
source: design-thinking-loop.md + problem-framing skill + 1-1-Understand_research-report.template.md + persona method skill (routed by design-sprint-tookit) + 1-3-Understand_jtbd.template.md + 1-4-Understand_journey-map.template.md
tags: [type/workflow, loop/understand, purpose/discover, status/canonical]
---

# W1 — Understand

> **TL;DR:** Turn a vague problem into four evidence-grounded artifacts (research, persona, JTBD, journey) that let the DESIGN phase commit to a position.

## When to run

- Start of a new product, feature, or engagement
- When research evidence has changed (major LEARN outputs invalidate prior assumptions)
- When stakeholders disagree on who the user is or what the job is — that's a signal UNDERSTAND hasn't actually closed

## Who runs it

| Role | Responsibility |
|---|---|
| Design lead | Owns the workflow end-to-end |
| Researcher (or design lead wearing that hat) | Runs interviews, analyzes, writes the research report |
| Stakeholders | Named, interviewed as participants if relevant; don't replace user research |

## Capabilities used

- Skills: `problem-framing`, `evidence-tagging`, `extreme-clarity`, `canonical-artifacts`, `wiki-ingest`, `context-pull`, `alignment-playbook`
- Agent: `design-synthesist` (research → persona → JTBD → journey); `design-sprint-toolkit` for workshops
- Plug-in: when the FDE Design Toolkit is mounted, its discovery and framing skills appear in discovery automatically (`03_Agents-and-Skills/Skills/fde-design-toolkit/`)

## What cross-functional partners will see

Not every XFN is in every step. This is what they experience from their seat.

| Partner | They'll receive | They'll be asked to | Time |
|---|---|---|---|
| PM | Kickoff brief (day 1); research plan for review; draft research report | Flag field knowledge gaps, review research questions, co-own the JTBD draft | 2–3 hrs |
| Engineering lead | Kickoff brief; early persona draft | Flag any technical constraints that should shape the research | 30–60 min |
| Marketing / GTM | Kickoff brief; final research report | Share what they hear from the field; flag disconnects with research findings | 60 min |
| Legal / Privacy | Research protocol (consent, data handling) before sessions start | Approve protocol; flag recruitment concerns | 30 min |
| Executive sponsor | Kickoff brief; research report executive summary | Confirm outcomes; name non-negotiables | 30 min |
| Research participants | Interview invite + consent form | 45-min conversation; share their real experience | 45 min each |
| XFNs who can't join live | [`0-1-Intake_initiative.template.md §D`](../../00_README/_templates/0-1-Intake_initiative.template.md) async input form | Fill in on their schedule; get draft back for correction | 20 min |

## Steps

### Step 0 — Frame the problem (front gate)

Before scoping research, ground the engagement so research is aimed, not exploratory. Load the `problem-framing` skill; fill its [problem-frame template](../../03_Agents-and-Skills/Skills/problem-framing/assets/problem-frame.template.md).

1. Read the intake (`00_context_intake/` and any `_wiki/sources/`; `/context-pull` scores the wiki first). Tag what you extract.
2. Write the problem statement in the user's language — **no solution nouns** (agent, dashboard, ontology, platform).
3. Inventory the **decisions the system must enable** — research will aim at these.
4. Name the **feasibility gap** (want vs achievable) and the **known/unknown data map**.
5. Close with a readiness Traffic Light. 🟢 = proceed to Step 1. 🟡 = proceed with named conditions (trigger + expiry). 🔴 = not ready; name the blocker and owner.

**Exit criterion:** Problem Frame filed in `01_understand/`; readiness light is 🟢 or 🟡. A 🔴 keeps you here — the problem isn't grounded enough to research.

> **Why Step 0 exists:** stakeholders routinely name solutions ("week one I want an agent, week two a dashboard") before a problem is stable. Framing first stops research from chasing a moving solution target. Skip this step only when a current, evidence-grounded Problem Frame already exists.

### Step 1 — Scope the research

1. Write down the research questions (≤5). Per `1-1-Understand_research-report.template.md §2`.
2. Choose methods: interviews (6–10 default), observation, diary, analytics review, usability test. Mix methods where possible.
3. Recruit participants across at least 2 segments.
4. Document the protocol (questions, script, consent).

**Exit criterion:** Protocol ready; first participant scheduled.

### Step 2 — Collect evidence

1. Run sessions. Record (with consent) or take structured notes.
2. Tag every observation with a source (participant code, timestamp, method).
3. Do not interpret during collection — collect first, analyze second.

**Exit criterion:** Raw notes complete for the planned sample, anonymized and stored.

### Step 3 — Synthesize into research report

1. Use `/research-synthesize` prompt with raw notes as input.
2. Fill `1-1-Understand_research-report.template.md`. Every finding gets an evidence tag (`observed` / `reported` / `assumed`) and an `n supporting` count.
3. Write limitations honestly (convenience sample, self-report bias, etc.).
4. Check: at least one finding is inconvenient for the commissioning team. If not, confirmation bias likely.

**Exit criterion:** Research report drafted, shareable.

### Step 4 — Draft personas

1. Use `/persona-draft` prompt with the research report as input.
2. Produce 1–3 personas. More than 3 = problem isn't framed yet; stop and narrow.
3. Each persona is primary or secondary. No "equally primary" ties.
4. Each persona has an explicit anti-persona.

**Exit criterion:** Personas exist, each linked to research report §4 findings.

### Step 5 — Articulate the JTBD

1. Use `/jtbd-draft` prompt with persona + research report as inputs.
2. Write the job statement in "When / I want to / So I can" form.
3. Fill all four forces of progress (push, pull, anxiety, habit).
4. Name at least one specific switching trigger — a moment when users would abandon the current solution.

**Exit criterion:** JTBD is a statement the primary persona would recognize as describing their life.

### Step 6 — Map the user journey

1. Use `/journey-map` prompt with research report + persona + JTBD as inputs.
2. Map one persona doing one job. Sequential stages, each with Doing / Thinking / Feeling / Pain / Opportunity.
3. Name 2–4 moments of truth.
4. Rank pain points by impact × frequency (not by order in the journey).

**Exit criterion:** Journey map readable in 5 minutes, rings true to someone who has never seen the research.

### Step 7 — Close the phase gate

Per `design-thinking-loop.md` UNDERSTAND → DESIGN gate:

- [ ] Can state the primary job in one sentence
- [ ] Can state the primary persona in one sentence
- [ ] Can state the top pain point with evidence (observed, not assumed)
- [ ] At least one finding contradicts the commissioning team's prior view (or we explicitly confirmed it)

If any box is unchecked, stay in UNDERSTAND for another iteration.

### Step 8 — Preserve the phase-gate evidence

Record the gate result, evidence, owner, and next phase in the existing research report or project
phase block. Traffic Light = 🟢 only if the gate clears. Phase closure alone needs no new decision file.
Use [W5 — Decide](W5-decide.md) only for a new durable choice, explicit capture request, or lifecycle change.

## Stop conditions

- Cannot get access to real users → pause. Do not substitute proxy interviews for the user's own voice. Escalate to sponsor.
- Fewer than 4 participants interviewed → findings are suggestive, not evidence. Label the report as `status: exploratory` and do not close the gate.
- The team skips directly to "solutions" during the research review → facilitate back. Solution talk in UNDERSTAND is a warning sign.

## Artifacts produced

- `<project-hub>/01_understand/YYYY-MM-DD-<topic>-problem-frame.md` (Step 0; via `problem-framing`)
- `<project-hub>/01_understand/YYYY-MM-DD-<topic>-research-report.md`
- `<project-hub>/01_understand/<persona-slug>-persona.md` (1–3 files)
- `<project-hub>/01_understand/<job-slug>-jtbd.md`
- `<project-hub>/01_understand/<persona>-<job>-journey.md`
- Phase-gate evidence in the existing research report or project phase block; a separate typed record only when W5 requires one

## Next workflow

→ **W2 — Design**

---

*Workflow grounded in `design-thinking-loop.md` UNDERSTAND phase and supporting templates. The phase gate is binary: if you can't state the job in one sentence, you haven't understood it.*
