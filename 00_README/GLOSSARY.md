# Glossary

**TL;DR:** Plain-language definitions of every term this OS uses — design loop, decisions, evidence, metrics and the agent OS itself — so humans and agents share one vocabulary.

Terms are grouped, then A–Z within each group. If a word you hit isn't here, that's a gap: add it.

---

## The loop and its artifacts

**4-phase loop** — The project lifecycle: **Understand → Design → Build → Learn**, iterated. See [How we work](HOW-WE-WORK.md) and the [loop framework](_frameworks/design-thinking-loop.md).

**Artifact** — A versioned output of the work: a research report, design, prototype, media asset or verification receipt. Document shapes come from the [template catalog](_templates/README.md); a generated file is not automatically authoritative.

**Design brief** — A short (1–2 page) document that aligns everyone on *why* a project exists, *who* it's for, *what outcomes* we chase and *which constraints* we respect. Written in Design, before the PRD.

**Design handoff** — The bridge from "what to build" (PRD) to "how it looks and behaves": every screen, state, interaction, copy string and accessibility annotation engineering needs.

**Design POV (point of view)** — Our opinionated stance: *for whom, against what, why now.* Anchors the brief and PRD. If you can't state a POV, you're not ready to design.

**Evidence brief** — The Learn-phase synthesis that separates *what we shipped* from *what we learned* and recommends a forward path.

**HMW (How Might We)** — A problem reframed as a design challenge: "How might we X so that Y?" Generated at intake, filtered by research, prioritized through the journey, and committed (1–3) in the POV.

**Journey map** — One persona doing one job, stage by stage: what they *do, think and feel*, plus pain points, moments of truth and opportunities.

**JTBD (Jobs-to-be-Done)** — The job a user "hires" the product to do: *"When \[situation\], I want to \[action\], so I can \[outcome\]."* Focuses on the underlying goal, not the feature request.

**Persona** — A specific user archetype grounded in research. Not demographics, not a stereotype. A persona that can't cite research isn't a persona.

**PRD (Product Requirements Document)** — The buildable spec: users, stories, requirements (functional and non-functional), edge cases, rollout plan and rollback trigger.

**Problem frame** — The pre-research artifact: the problem in the user's language (no solution nouns), the decisions the product must enable, and the gap between what stakeholders want and what's achievable. It gates entry into research.

**Retro** — A blameless review of a cycle: what worked, what didn't, at most five owned action items — starting with last retro's actions.

**Test plan** — The protocol written *before* a build slice reaches users: hypothesis, method, participants, metrics, counter-metric, rollback trigger.

**TL;DR (Too Long; Didn't Read)** — The one-sentence summary at the top of every document. A reader should get the point from it alone; if it's longer than one sentence, it isn't a TL;DR.

**UX research report** — The evidence base of Understand: methods, participants, findings with evidence tags, limitations.

**UX survey** — A structured instrument sent to many respondents before interviews, to quantify and validate what interviews will explore.

---

## Decisions and alignment

**ADR (Architecture Decision Record)** — A typed decision record for a durable architecture or trust boundary, or a choice that is expensive to reverse. Product choices are PDRs, not ADRs.

**Alignment** — Not agreement. Everyone heard the same thing, named their objections and committed to one direction. See the [alignment playbook](_frameworks/alignment-playbook.md).

**Consultation** — How a decision was reviewed: `solo` (one accountable author), `invited` (review requested; name the invitees) or `reviewed` (review happened; record the real dissent). Never invent reviewers or objections.

**Decision owner** — The single person accountable for a decision. Not a team. One name.

**Disagreement heard** — Real dissent recorded when consultation happens. "Invited; none surfaced" is honest; silence is not approval.

**Extreme Clarity** — Writing so a busy reader can act without a follow-up: TL;DR first, the ask and deadline, the evidence, and what could make you wrong. See [`extreme-clarity.md`](_frameworks/extreme-clarity.md).

**Lifecycle status** — A decision record's state, separate from its light: `proposed`, `accepted`, `superseded` (replaced — names exactly one successor) or `retired` (ended without replacement).

**Ops note** — A typed decision record for a reversible operational action: a setting, maintenance step, incident response or cleanup, with evidence and a rollback.

**PDR (Product Decision Record)** — A typed decision record for a product, design, scope or experience choice, with options, evidence and a review trigger.

**Release record** — A typed decision record attesting a promotion, launch or release: subject, gates, result and immutable evidence.

**Rollback trigger** — The specific condition that would make us reverse a decision or stop a rollout. Named before we ship, not discovered after.

**Traffic Light** — The three-state posture of a decision: 🟢 green (proceed), 🟡 yellow (conditional — needs a *trigger* that closes it and an *expiry* date), 🔴 red (blocked — needs a blocker and an *unblock owner*). Every ADR and PDR closes with exactly one. See [`traffic-light-decisions.md`](_frameworks/traffic-light-decisions.md).

**Typed decision record** — A decision file with `decision-record/v2` front matter and one `record_type`: `adr`, `pdr`, `ops-note` or `release`. Its stable `id` (`<namespace>-NNNN`) is its identity. Created only through W5, and only when a new durable choice needs its own record.

**W5 (Decide)** — The cross-cutting workflow for decisions: reuse existing rationale first; otherwise write the smallest truthful typed record and validate it. See [W5](../02_Workflows/workflows/W5-decide.md).

**House principles** — The house principles of this template (have a POV, solve the right problem, evidence over opinion, defaults are decisions…), named after the template's author. See [`house-principles.md`](_frameworks/house-principles.md).

---

## Evidence and claims

**Assumed** — An evidence tag meaning "this is a team hypothesis, not yet proven." An agent's unverified "it's done" is assumed too. Listing assumptions is good; *hiding* them is the bug.

**Evidence tag** — A label on every claim: `observed`, `reported` or `assumed`. Forces us to name our basis instead of presenting opinions as facts. The *why* is [House principle §4](_frameworks/house-principles.md#4-evidence--opinion-but-evidence-is-rare); the [`evidence-tagging`](../03_Agents-and-Skills/Skills/evidence-tagging/SKILL.md) skill applies it.

**Observed** — We directly saw or heard it from a user (interview, diary, session recording), or watched a check run and pass.

**Reported** — A third party told us (stakeholder claim, prior report, an analytics summary we didn't collect).

---

## Metrics and outcomes

**Counter-metric** — The metric a test must not degrade; without one, a test can't fail.

**Goal metric** — The upside metric we're trying to move (e.g., "checkout completion rate").

**Guardrail metric** — A metric we promise not to hurt while chasing the goal (e.g., "support ticket volume must not rise more than 5%").

**Non-goal** — Something the project explicitly will *not* do, named as clearly as a goal.

**North Star metric** — The single top-level metric a team aligns on; usually one per product, not per project.

---

## Journey, test and build

**Edge case** — A rare or extreme scenario (empty, error, very large input, offline, accessibility need) that a happy-path design ignores.

**Fidelity** — How realistic a prototype is: paper → wireframe → hi-fi → thin slice → full release. Pick the lowest fidelity that answers the question.

**Moment of truth** — A step in the journey where the whole experience is won or lost.

**Riskiest assumption** — The belief that, if wrong, breaks the whole design. Build tests it first.

**Thin slice** — The smallest end-to-end working version that can prove or disprove the riskiest assumption.

---

## The agent OS

**Agent** — A named AI role with instructions, tools and boundaries, defined once in `03_Agents-and-Skills/Agents/<slug>.agent.md`.

**Agent OS (Design Agency OS)** — This repository's operating system for design work done by humans and agents together: shared rules, knowledge, capabilities, workflows and checks, all as plain files.

**Approval** — An explicit commitment by a named human under the current task or workflow contract. A name typed by an agent is not proof of consent.

**Authority registry** — [`AUTHORITIES.md`](../AUTHORITIES.md): the table that says which file is the source of truth for each concept. Everything else — indexes, dashboards, summaries — is a derived view.

**Capability catalog** — The generated list of installed skills and agents, [`03_Agents-and-Skills/INDEX.md`](../03_Agents-and-Skills/INDEX.md). Load entries selectively, never the whole catalog.

**Checkpoint** — A saved resume point for interrupted multi-step work: goal, state, next action, evidence. It does not prove the saved result passed.

**Discovery link** — A generated symlink under `.github/` or `.claude/` that lets a host find a skill, agent or prompt. Never edited by hand; regenerated from the source.

**Edition** — One declared variant of a plug-in (for example `full` or `public`), with its own source and marker file; the engine detects which edition is mounted.

**Engine** — [`06_Engine/`](../06_Engine/README.md): the harness, retrieval tools, evals, plug-in profiles and the `agency` CLI.

**Engine project** — A run of an engine plug-in (a PDG prototype, a VPG film). It lives inside a hub phase folder, e.g. `01_Project-Hubs/<hub>/03_build/<name>/`.

**Eval** — A golden task with an expected result that a skill must pass, run by the engine's eval harness — the regression test for agent behavior.

**FDE (forward-deployed engineering)** — Embedding builders with a customer to ship working solutions in the customer's real context. *FDE design* is the design practice that keeps those engagements fast and honest: tight discovery, prototypes against real constraints, handoffs the customer team can own.

**Goal** — A long task made explicit in five parts — outcome, verification, constraints, iteration policy, error handling — so an agent knows what "done" means and when to stop. Written with the [`goal-harness`](../03_Agents-and-Skills/Skills/goal-harness/SKILL.md) skill; see [`long-horizon-execution.md`](_frameworks/long-horizon-execution.md).

**Harness** — The checks that keep the OS honest: skill and agent linters, schema checks, evals, the decision validator and commit hooks.

**Host** — The AI tool that runs agents here, such as GitHub Copilot or Claude Code. `agency.yaml` → `discovery.targets` chooses which hosts get discovery links.

**Host adapter** — A native prompt, agent, skill or SOP in this repository that drives a plug-in (for example `/prototype-design`). It stays hidden from discovery until the plug-in is mounted, and it lives outside the mount, so updating the plug-in never overwrites it.

**Hub (project hub)** — One folder per project under `01_Project-Hubs/`, created from `_template-project/` with `python3 06_Engine/scripts/agency.py hub new <slug>`.

**L0–L5** — The six responsibilities of the OS, each owned by one canonical ADR in `00_Agentic-OS/decisions/`: **L0** authority & safety, **L1** knowledge & context, **L2** capabilities & interfaces, **L3** task control, **L4** delivery & outcomes, **L5** verification & learning. Responsibilities, not folders, privilege levels or mandatory stages. See [Architecture](ARCHITECTURE.md).

**Mode** — `agency.yaml` → `mode:`: `template` (the blank harness — no hubs but the skeleton, no plug-ins) or `workspace` (doing real work). Creating a hub or adding a plug-in switches it.

**Mount** — The fixed folder where a plug-in is checked out (e.g. `02_Workflows/prototype-design/`). Owned upstream: improve the plug-in in its own repository and re-pin; don't edit inside the mount or link into it from Markdown.

**Operating guide** — [`00_Agentic-OS/README.md`](../00_Agentic-OS/README.md): the task procedure every agent follows — scope → retrieve → execute → verify → hand off.

**PDG (prototype design graph)** — The prototype-design plug-in: an engine that runs prototype work as a graph of nodes with task packets, rubric checks, scoped rework and human gates. Mounted at `02_Workflows/prototype-design/`. See [Plug-ins](PLUGINS.md).

**Plug-in** — An optional capability package — skills, an engine, or both — kept in its own repository, mounted here as a pinned git submodule with `python3 06_Engine/scripts/agency.py plugin add <name>`, and described by a *profile* (`06_Engine/plugins/<name>.plugin.yaml`). It counts as plugged in when its mount is checked out and an edition marker is found; the skills, agents and commands it exposes are its *contributions*. See [Plug-ins](PLUGINS.md).

**Prompt (slash command)** — A file in `02_Workflows/prompts/<name>.prompt.md` that wraps a template with inputs and steps; hosts expose it as `/<name>` (e.g. `/persona-draft`).

**Provenance** — The source and transformation trail of an output. A hash chain or log can show that something changed; it can't certify the claim is true.

**Rubric** — A scoring guide that turns subjective quality ("feels on-brand") into concrete criteria and reference cases a reviewer — human or agent — can apply round after round. Written with the [`rubric-authoring`](../03_Agents-and-Skills/Skills/rubric-authoring/SKILL.md) skill.

**Run folder** — `00_Agentic-OS/_runs/<YYYY-MM-DD>-<slug>/`: dated evidence of OS maintenance or improvement work.

**Skill** — A reusable, self-describing capability (`03_Agents-and-Skills/Skills/<slug>/SKILL.md`) that an agent loads when its task matches: when to use it, inputs, outputs, done-when checks and lints.

**SOP** — A standard operating procedure for a repeatable multi-step job, `02_Workflows/SOPs/<slug>/SOP.md`.

**Task procedure** — Scope → retrieve → execute → verify → hand off: how any single task runs, at any size. Distinct from the project loop, which spans many tasks.

**VPG (video production graph)** — The video-production plug-in: an engine for governed product-demo films where agents create, tools measure and named humans approve. Mounted at `02_Workflows/video-production/`.

**Wiki (hub wiki)** — A hub's `_wiki/`: an LLM-maintained knowledge base that distills raw intake into entities, concepts, sources and syntheses. Artifacts cite it; it cites raw sources and never edits them.

**Workflow (W1–W5)** — A procedure in `02_Workflows/workflows/` that chains prompts, templates and gates: W1 Understand, W2 Design, W3 Build, W4 Learn, W5 Decide (cross-cutting).

**Workflow graph / node / attempt** — Inside an engine plug-in: the declared graph of work, one bounded unit of work, and one execution of that unit. Retry, rework and acceptance rules belong to the engine.

---

## Roles

**Design lead** — Owns the loop for a project; usually also owns research, POV, brief and journey.

**PM (Product Manager)** — Co-owns the JTBD, the PRD and the forward-path decision after Learn. Accountable for outcomes.

**Stakeholder** — Anyone affected by the work who isn't building it: sponsors, XFN partners, sometimes end users.

**XFN (cross-functional partner)** — A non-design, non-PM partner the project depends on: engineering, marketing, legal, privacy, security, sales, finance, support.

---

*Missing a term? It's a gap. Add it here, in plain language.*
