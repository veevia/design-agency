# Changelog

**TL;DR:** Version 2.0.0 is the first public release of the Design Agency OS: a blank, reusable template with one rule set for every agent, six L0–L5 contracts, generated discovery for Copilot and Claude, plug-and-go plug-ins (FDE Design Toolkit, PDG, VPG and the skill packs they bind), a privacy and release gate, and a single integrity review.

## Unreleased

### Changed

- [README](README.md) rewritten as one argument: why a team needs the OS, how it works and what changes when
  you adopt it, then a three-step quickstart with example prompts, plug-ins and validation.

### Added

- An animated overview of the OS and its still image in [00_README/_assets/](00_README/_assets/README.md),
  in the same style as the FDE Design Toolkit and VPG overviews.

## 2.0.0 — 2026-10-29

First public release. The repository starts with fresh history and ships no customer or personal data; every
example is generic and names no person, organization or real use case.

### Added

- **Operating system:** [AGENTS.md](AGENTS.md) (canonical rules; [CLAUDE.md](CLAUDE.md) and
  [copilot-instructions](.github/copilot-instructions.md) route to it), [AUTHORITIES.md](AUTHORITIES.md),
  the [operating guide](00_Agentic-OS/README.md) and six canonical contracts `aos-0001`–`aos-0006` (L0–L5).
- **Review:** [agentic-os-review.py](00_Agentic-OS/agentic-os-review.py) aggregates every gate into one verdict;
  CI runs it on every push and pull request; hooks run it before commits and pushes.
- **Engine:** `06_Engine/agency` (configuration, catalog, discovery, plug-ins, portfolio report) and the
  `agency.py` CLI (`status`, `sync`, `check`, `hub new`, `plugin list|add|status|check|smoke|report|remove`).
- **Plug-ins:** profiles for the FDE Design Toolkit (public and full editions), PDG, VPG, UI/UX Pro Max,
  Anthropic's Apache-2.0 skills (five wired; the proprietary document skills are not), Impeccable and Video
  Shotcraft; pinned-submodule mounts (shallow for large histories), edition detection, host adapters gated
  until their plug-in is mounted, declared check side effects (an undeclared write into a mount fails), and a
  skill portfolio report as an optimization baseline. Guide: [PLUGINS](00_README/PLUGINS.md).
- **Engine skill bindings:** engine profiles name the companion plug-ins that supply the skills their graphs
  bind and the tenant integrations a fork supplies; `plugin add <engine> --with-companions` mounts everything
  an engine needs; the catalog lists plug-in skills so engines that validate bindings pass in the host.
- **Method library:** the 62 design-sprint methods as flat native skills with fictional worked examples,
  routed by the `design-sprint-tookit` hub, plus generic `context-intake`, `persona-critic`, `demo-master`
  and `remotion` skills.
- **Discovery:** generated links in `.github/{skills,agents,prompts}` and `.claude/{skills,agents,commands}`;
  depth parity so relative links resolve through them; `.vscode/settings.json` avoids duplicate listings.
- **Gates:** portable skill spec (name equals folder, "Use when" trigger), contract gate, link checker with
  depth-parity pass, hygiene and template-mode checks, catalog drift, capability map integrity.
- **Improvement loops:** [initiatives](00_Agentic-OS/initiatives/README.md) for OS and plug-in optimization,
  a ranked [backlog](00_Agentic-OS/OPTIMIZATION-BACKLOG.md) and a run-evidence home.
- **Tests:** engine suite with a fixture plug-in mounted as a real git submodule; adapted decision-validator
  and retrieval suites.
- **Privacy and release gate:** [check-privacy.py](06_Engine/harness/check-privacy.py) blocks emails, tenant and
  conversation IDs, meeting and document links, credentials, file metadata and locally denylisted terms, also
  inside archives, office files, encoded text and notebooks (a review row: blocking in the blank template,
  advisory in a workspace, and part of the pre-commit hook); `agency.py publish-check` adds the full history,
  tags, ref names, commit identities and every remote ref. Procedure: [RELEASING](00_README/RELEASING.md).
- **License:** [MIT](LICENSE).

### Evidence

Recorded 2026-10-29 on macOS with Python 3.14 and 3.11, against the release tree as a single fresh commit.

- Engine (70), retrieval (27) and decision-validator (39) tests pass on both interpreters.
- A fresh clone that follows [SETUP](SETUP.md) passes the full review (21 of 21 rows), installs the hooks, creates a
  hub, mounts the FDE Design Toolkit and a companion, and commits through the pre-commit gate; a teammate clone
  without submodules shows no catalog or discovery drift.
- A disposable workspace host mounted all six plug-ins (FDE full, Anthropic skills, Impeccable, Video Shotcraft,
  PDG, VPG) and passed the full review: 21 of 21 rows, no warnings.
  - PDG: 70 of 70 bound skills resolve; its graph validation, docs check, offline dry run and ledger
    verification pass.
  - VPG: 42 of 44 bound skills resolve (2 tenant integrations); its checks and offline dry run pass.
  - FDE full edition: its unit tests and authoring gates pass.
  - Every mount was unchanged after all checks; removing a shallow plug-in deleted its cached clone.
- In a host with PDG but no companions, PDG's own validation reports exactly the 37 bound skills the host's
  coverage report lists as missing.
- PDG's own suite inside a host without companions: 628 passed, 1 skipped, 3 failed. With companions the two
  binding tests pass; the remaining failure is an upstream test assumption (OS-07).
- VPG's own suite inside a host: 1095 passed, 1 skipped; its binding test fails only on the two tenant
  integrations (OS-09).
- Privacy gate: 23 reproduced leak cases are caught — credentials in URLs, JWTs, webhooks, signed URLs, registry
  tokens and secret assignments; text in UTF-16, binaries, zip, tar and gzip archives, data URIs, notebook
  outputs and PDFs (hex and compressed metadata); denylisted terms split across lines, accented or in lockfiles;
  oversized files; symlink targets; and, in history, removed paths, annotated tags and author names. The new
  detectors add no findings on six plug-in repositories.

### Known limits

- Discovery is verified statically; runtime loading in each agent host is backlog OS-03.
- PDG validation in a host needs the private FDE full edition (OS-10); VPG binds two tenant integrations (OS-09).
- The privacy gate finds patterns and the terms you denylist; it does not strip metadata (OS-11) and cannot
  recognise a customer it was never told about.
