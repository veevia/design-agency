# AGENTS.md — Design Agency OS operating rules

**TL;DR:** Scope the request, retrieve only what it needs, execute, verify against acceptance and hand off with evidence; projects move through Understand → Design → Build → Learn.

These rules bind every agent runtime working in this repository (GitHub Copilot, Claude Code, Codex and others).
[CLAUDE.md](CLAUDE.md) and [.github/copilot-instructions.md](.github/copilot-instructions.md) only route here.
Ownership of every concept is registered in [AUTHORITIES.md](AUTHORITIES.md).

## Always-on rules

1. Establish the requested outcome, scope and permissions before acting. Analysis is not approval to implement.
2. Capability is not permission: publishing, pushing, restarts, external messages and irreversible actions need
   the user's explicit authorization.
3. Protect unrelated work. Make scoped edits, stage explicit paths, never discard changes you did not make.
4. Resolve conflicts with [AUTHORITIES.md](AUTHORITIES.md). Generated views — the catalog, discovery links in
   `.github/` and `.claude/`, indexes, mounted plug-ins — never override their sources; edit the source and regenerate.
5. Tag claims `observed`, `reported` or `assumed` and cite sources. A successful command is not an outcome.
6. Verify the actual requirement with the smallest relevant check and widen with risk. Report failures,
   untested behaviour and known limits plainly.
7. Record a decision only when it is new and durable ([W5](02_Workflows/workflows/W5-decide.md)); routine work
   reuses task evidence.
8. Never commit credentials, customer or personal data. Customer material stays in `*_TENANT.md` files (ignored);
   follow the commit, secret and customer-label rules in [CONVENTIONS](00_README/CONVENTIONS.md). Before anything is
   published, `python3 06_Engine/scripts/agency.py publish-check` must report READY ([RELEASING](00_README/RELEASING.md)).

## Task procedure

Follow the [operating guide](00_Agentic-OS/README.md): **scope → retrieve → execute → verify → hand off**.
Six contracts own the responsibilities behind it — [L0 authority](00_Agentic-OS/decisions/l0-authority-and-safety.md),
[L1 knowledge](00_Agentic-OS/decisions/l1-knowledge-and-context.md), [L2 capabilities](00_Agentic-OS/decisions/l2-capabilities-and-interfaces.md),
[L3 control](00_Agentic-OS/decisions/l3-task-control.md), [L4 delivery](00_Agentic-OS/decisions/l4-delivery-and-outcomes.md),
[L5 verification](00_Agentic-OS/decisions/l5-verification-and-learning.md). Read one only when its question arises;
they are responsibilities, not stages.

## Retrieve only what the task needs

- Find a skill, agent, prompt or SOP in the [capability catalog](03_Agents-and-Skills/INDEX.md), then load only that file
  and the references it names. Do not load the whole catalog, archives or decision history by default.
- Project knowledge: read the hub's `_wiki/index.md` (or run `/context-pull`) before opening pages.
- Paths in instructions are repository-root-relative; run commands from the repository root.

## Project hubs

```
01_Project-Hubs/<hub>/
├── 00_context_intake/   raw sources — read, never rewrite
├── _wiki/               maintained knowledge with evidence tags (ingest / query / lint)
├── 01_understand/ … 04_learn/   phase outputs that cite the wiki; decisions/ per phase (typed, W5)
└── stakeholders/        people and roles
```

Create a hub with `python3 06_Engine/scripts/agency.py hub new <slug>`. `weekly-status/` is opt-in.
Engine projects (PDG prototypes, VPG films) live inside a phase folder, e.g. `01_Project-Hubs/<hub>/03_build/<name>/`.

## Disciplines

- **Evidence tagging** — [House principles §4](00_README/_frameworks/house-principles.md#4-evidence--opinion-but-evidence-is-rare); skill `evidence-tagging`.
- **Traffic Light decisions** — one 🟢🟡🔴 per decision; Yellow needs trigger + expiry, Red an unblock owner —
  [framework](00_README/_frameworks/traffic-light-decisions.md); skill `traffic-light-decisions`.
- **Extreme Clarity** — one-sentence TL;DR, numbers over adjectives — [framework](00_README/_frameworks/extreme-clarity.md).
- **Quality bars** — TL;DR passes a 10-second test; non-goals and scope-out lists are never empty; rollback
  triggers are specific; record only real consultation, never invented agreement or dissent.

## Plug-ins

The FDE Design Toolkit, PDG (prototypes), VPG (demo films) and third-party skill packs are optional plug-ins
([guide](00_README/PLUGINS.md)). Check before use: `python3 06_Engine/scripts/agency.py plugin status <name>`;
add with `plugin add <name>` (engines: `--with-companions`). Never edit a mounted plug-in in place — propose changes upstream
(`/plugin-optimize`). Engines own their human gates; never approve on a person's behalf.

## Memory and handoff

- The repository is durable memory; runtime memory is a cache of it.
- Substantial work keeps one resume point in its task home: outcome, current step, next action, proof, changed
  files, blockers. Reconcile it with current files when you resume.
- Hand off: result, paths, acceptance evidence, blockers or next action. Mark partial work as partial.

## Before handoff

- Changes to OS, harness, capabilities or docs: `python3 00_Agentic-OS/agentic-os-review.py` (every MUST row passes).
- After adding or renaming a skill, agent or prompt: `python3 06_Engine/scripts/agency.py sync` (regenerates the
  discovery links and the capability catalog).

## Voice

Concise, direct, conclusion first. No emojis except the semantic Traffic Light markers. Before a tool call,
say in one sentence what you are about to do.
