# How we work

**TL;DR:** Projects move through Understand → Design → Build → Learn; every task inside them runs scope → retrieve → execute → verify → hand off; and three rules hold everywhere — tag evidence, close decisions with one light and one owner, lead with a TL;DR.

> **For everyone on the team** — designers, PMs, engineers, marketing, legal, sales, research partners — and the agents working beside them. Five minutes. Come back whenever you're unsure what happens next.

## The project loop

```
    ┌────────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ UNDERSTAND │───▶│  DESIGN  │───▶│  BUILD   │───▶│  LEARN   │
    └────────────┘    └──────────┘    └──────────┘    └──────────┘
         ▲                                                   │
         └───────────────────────────────────────────────────┘
```

| Phase | The question | Evidence to move on |
|---|---|---|
| **Understand** | Who needs what, and why? | A problem frame without solution nouns; evidence-tagged research; a named primary user and a one-sentence job |
| **Design** | Which direction and scope are we committing to? | POV, brief and PRD reviewed by the people they affect; non-goals and guardrails named |
| **Build** | What is the smallest thing that tests the riskiest assumption? | A prototype or slice, a test plan written *before* it ships, mocked seams stated honestly |
| **Learn** | What happened, and what changes? | Outcomes vs. promises, what surprised us, updated artifacts, one forward path with an owner |

It's a loop, not a waterfall: Learn sends us back to Understand or Design whenever evidence breaks a belief.
It's also a *project* lifecycle — a small fix doesn't need every artifact. Details: [design-thinking loop](_frameworks/design-thinking-loop.md).

## The task procedure

Every piece of work inside the loop — done by a person or an agent — runs the same five steps, sized to the task:

1. **Scope** — the outcome, the files affected, the permissions, how we'll know it's done.
2. **Retrieve** — only the context this task needs: the hub's wiki and artifacts, the relevant skill.
3. **Execute** — advance the work in the existing plan; routine progress needs no ceremony.
4. **Verify** — check real behavior; a passing lint or synthetic test is not acceptance.
5. **Hand off** — the result, where it lives, the evidence, and what's still open.

Agents create outputs, checks verify them, and named humans make the consequential commitments. The
[operating guide](../00_Agentic-OS/README.md) owns this procedure.

## Three rules that hold everywhere

1. **Tag evidence.** Every claim is `observed` (we saw it), `reported` (someone told us) or `assumed` (we're
   guessing). Unlabeled assumptions are the bug. ([House principle §4](_frameworks/house-principles.md#4-evidence--opinion-but-evidence-is-rare))
2. **One light, one owner.** A decision closes with exactly one 🟢🟡🔴 and one named owner — never "the team".
   🟡 names a trigger and an expiry; 🔴 names a blocker and who unblocks it. No hidden yellows.
   ([Traffic Light](_frameworks/traffic-light-decisions.md))
3. **TL;DR first.** One sentence a busy reader can act on: numbers, not adjectives; the ask and its deadline.
   ([Extreme Clarity](_frameworks/extreme-clarity.md))

## Decisions: reuse first, then the smallest typed record

Most decisions already live in an artifact — a meeting note, a PRD section, an evidence brief. Cite it.
[W5 — Decide](../02_Workflows/workflows/W5-decide.md) writes a separate record only for a new durable choice,
an explicit request, or a change to an existing record's lifecycle:

| The durable fact is… | Record |
|---|---|
| An architecture or trust boundary, or a choice that's expensive to reverse | **ADR** |
| A product, design, scope or experience choice | **PDR** |
| A reversible setting, maintenance step, incident response or cleanup | **Ops note** |
| A promotion, launch or release | **Release** |

Consultation is recorded honestly — `solo`, `invited` or `reviewed` — and nobody invents dissent.
Closing a phase needs gate evidence, not a new decision file.

## What we'll ask of you

| You are… | Understand | Design | Build | Learn |
|---|---|---|---|---|
| **PM** | Join kickoff; review research questions (30 min) | Co-own the PRD; sign scope, non-goals, guardrails (2–4 h) | Keep the riskiest assumption first; unblock scope | Decide the forward path (1 h) |
| **Engineer** | Flag constraints early, not after the brief (30 min) | Feasibility review; flag what needs a prototype (1–2 h) | Pick the fidelity, own the slice, name the rollback trigger | Bring ops and performance evidence (1 h) |
| **Marketing / GTM / sales** | Share what the field says (30 min) | Check the POV for market fit and message (1 h) | Preview the slice (30 min) | Bring adoption and qualitative feedback (1 h) |
| **Legal / privacy / security** | Review consent and data handling before sessions (30 min) | Review the PRD's privacy and security sections: 🟢 or 🔴 (1 h) | Be in the loop before real users see it | Bring incident signal; review before shipping wider |
| **Sponsor** | Name the outcomes and non-negotiables (30 min) | Sign the brief and PRD; break ties (1 h) | Only if a 🔴 escalates | Read the one-page readout: scale, hold or stop (15 min) |
| **Research participant** | A 45-minute conversation or a short diary | — | — | A 15-minute follow-up if you used the prototype |

Review effort follows risk, not a meeting quota. Simulated sessions are never presented as real research.

## How we communicate

- **Kickoff:** one screen, from the [initiative intake](_templates/0-1-Intake_initiative.template.md) §F.
- **Status:** opt-in. A hub with a real reporting cadence sends a one-page status with Scope / Timeline /
  Quality / Stakeholders lights; others don't invent one.
- **Decisions:** findable in each phase's `decisions/` folder; every open 🟡 is visible with its trigger and expiry.
- **Customer content** stays in tools and storage the customer approved ([Conventions §4](CONVENTIONS.md#4-customer-data-labels)).

## Plug-ins

The blank OS runs on its own. When a project needs more, add an optional plug-in — the FDE design toolkit,
the prototype-design engine (PDG), the video-production engine (VPG) or the ui-ux-pro-max skill — with
`python3 06_Engine/scripts/agency.py plugin add <name>`. Engine projects live inside a hub phase folder, e.g.
`01_Project-Hubs/<hub>/03_build/<name>/`. What each plug-in adds and where it mounts: [Plug-ins](PLUGINS.md).

## Start a project

1. `python3 06_Engine/scripts/agency.py hub new <slug>` — copies the [hub skeleton](../01_Project-Hubs/_template-project/README.md)
   and switches `agency.yaml` to workspace mode.
2. Fill in the hub README (owner, one-sentence goal, current phase), run the initiative intake, and send §F as the kickoff.
3. Frame the problem, then start in `01_understand/`. Each phase folder's README says what comes next.

## If you're lost

- Jargon: [Glossary](GLOSSARY.md) · Naming, tags, links: [Conventions](CONVENTIONS.md)
- Artifacts: [template catalog](_templates/README.md) · Procedures: [workflows](../02_Workflows/README.md)
- What the OS can do today: [capability map](domain-coverage-map.md) · Gaps and ideas: [OS backlog](../00_Agentic-OS/OPTIMIZATION-BACKLOG.md)
