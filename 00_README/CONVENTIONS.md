# Conventions

**TL;DR:** One place for how files are named, filed, tagged, labeled, linked and kept safe in a Design Agency OS repository; folder READMEs link here instead of restating it.

**Scope:** Naming, tags and front matter apply to authored knowledge and governed assets — not to installed
dependencies, unmodified raw evidence, images, or generated files that follow their own schema. Credential and
link rules apply everywhere. [AUTHORITIES](../AUTHORITIES.md) registers who owns each concept; this file owns
naming, filing, tags and repository hygiene.

## 1. File naming

- **Kebab-case**: `project-brief.md`, not `Project Brief.md` or `projectBrief.md`.
- **Date prefix** for dated artifacts: `YYYY-MM-DD-<slug>.md` (e.g., `2026-01-20-kickoff-notes.md`).
- **Templates**: `<name>.template.md` under a `_templates/` folder; loop templates are numbered
  `<n>-<Phase>_<slug>.template.md` ([catalog](_templates/README.md)).
- **Decisions**: descriptive kebab-case filenames (`checkout-scope.md`). The front-matter `id`
  (`<namespace>-NNNN`) is the identity; never renumber or rename history for display.
- **Capabilities**: skills `03_Agents-and-Skills/Skills/<slug>/SKILL.md`; agents
  `03_Agents-and-Skills/Agents/<slug>.agent.md`; prompts `02_Workflows/prompts/<name>.prompt.md`;
  SOPs `02_Workflows/SOPs/<slug>/SOP.md`; plug-in profiles `06_Engine/plugins/<name>.plugin.yaml`.
- **Drafts**: live in `_drafts/` subfolders, which Git ignores (§5).
- **Indexes**: `INDEX.md` (uppercase) for a folder's generated catalog; `index.md` for a wiki's generated index.
- **Customer-tenant files**: suffix `_TENANT.md` (§4).
- **Underscore prefix** (`_wiki/`, `_templates/`, `_drafts/`, `_runs/`, `_starters/`) marks support folders, not deliverables.

## 2. Folder structure

Top-level folders are numbered for stable sort order. Each top-level folder, and any folder people file work
into, has a `README.md` stating its purpose, what belongs there and any local rules.

| Path | Holds |
|---|---|
| `README.md`, `SETUP.md`, `AGENTS.md`, `CLAUDE.md`, `AUTHORITIES.md`, `CHANGELOG.md`, `agency.yaml` | Entry points, always-on agent rules, the authority registry, history and OS configuration |
| `00_Agentic-OS/` | Task operating guide, the L0–L5 decisions, optimization backlog, initiatives, run evidence (`_runs/`) |
| `00_README/` | Architecture, plug-in guide, capability map, these conventions, glossary, frameworks, templates |
| `01_Project-Hubs/` | One hub per project, created from `_template-project/` |
| `02_Workflows/` | Workflows W1–W5, prompts, SOPs; engine plug-ins mount here |
| `03_Agents-and-Skills/` | Native skills and agents (flat), the generated catalog; skill plug-ins mount here |
| `04_MCP/` | Runtime integration notes (MCP servers, adapters) — never credentials |
| `05_Library/` | Reference material and frozen starters |
| `06_Engine/` | Harness, retrieval, evals, plug-in profiles, the `agency` package and CLI, tests |
| `.github/`, `.claude/` | Host discovery folders — generated links only (§10) |

- **Hubs** follow `01_Project-Hubs/_template-project/`: `README.md`, `intake.md`, `00_context_intake/`,
  `_wiki/`, `01_understand/` … `04_learn/` (each with `decisions/`), `stakeholders/`, and an opt-in `weekly-status/`.
- **Engine projects** — a prototype-design (PDG) run, a video-production (VPG) film — live inside a hub
  phase folder, e.g. `01_Project-Hubs/<hub>/03_build/<name>/`, never at the repository root.
- **Plug-in mounts** are checked-out folders owned by their upstream ([PLUGINS](PLUGINS.md)). Don't edit
  inside a mount; keep host-side wiring (prompts, agents, SOPs) in this repository's own folders.
- **Retire in place.** Superseded decisions keep their path and gain lifecycle metadata; retired artifacts get
  `#status/archived`. A top-level `Archive/` that mirrors original paths is optional.

## 3. Tag taxonomy

Tags are namespaced, lowercase hashtags inline or in front-matter `tags:` (written without `#` there).
Listed enumerations are **closed** — a new value needs a change to this section in the same commit that
first uses it. Authored artifacts carry at least one `#type/*` and one `#status/*`; don't inject tags into
raw intake or executable data.

### 3.1 Core namespaces (closed)

| Namespace | Values | Purpose |
|---|---|---|
| `#type/*` | `problem-frame`, `research-report`, `survey`, `persona`, `jtbd`, `journey-map`, `pov`, `brief`, `prd`, `handoff`, `test-plan`, `evidence-brief`, `retro`, `intake`, `plan`, `status`, `decision`, `meeting`, `workshop`, `project`, `goal`, `evaluation`, `entity`, `concept`, `source`, `synthesis`, `playbook`, `spec`, `framework`, `reference`, `template`, `workflow`, `prompt`, `sop`, `agent`, `skill`, `output` | What the file is |
| `#status/*` | `draft`, `review`, `published`, `canonical`, `active`, `standing`, `archived`, `exploratory`, `hypothesis`; decision records: `proposed`, `accepted`, `superseded`, `retired` | Lifecycle stage |
| `#tenant/*` | `customer`, `internal`, `personal` | Whose data is in it |
| `#purpose/*` | `discover`, `align`, `decide`, `build`, `measure`, `report`, `reference` | Why the artifact exists |
| `#source/*` | `interview`, `survey`, `workshop`, `meeting`, `deck`, `doc`, `web`, `analytics`, `customer`, `office-suite`, `agent`, `manual`, `hypothesis` | Origin / provenance |

Typed decision records keep their lifecycle in the `status:` field and may mirror it, the record type and the
light in tags ([field reference](../03_Agents-and-Skills/Skills/traffic-light-decisions/references/REFERENCE.md)):

| Namespace | Values | Purpose |
|---|---|---|
| `#record/*` | `adr`, `pdr`, `ops-note`, `release` | Decision record type |
| `#light/*` | `green`, `yellow`, `red` | Traffic Light posture |

### 3.2 Design-thinking loop namespaces (closed)

Canonical values from [`design-thinking-loop.md`](_frameworks/design-thinking-loop.md).

| Namespace | Values | Purpose |
|---|---|---|
| `#loop/*` | `understand`, `design`, `build`, `learn`, `all` | Which phase of the loop this artifact belongs to |
| `#evidence/*` | `observed`, `reported`, `assumed` | Basis for a claim, finding or pain point |
| `#risk/*` | `scope`, `timeline`, `quality`, `adoption`, `accessibility`, `security`, `privacy`, `compliance`, `brand` | Risk surface addressed |

### 3.3 Open namespaces (free values)

| Namespace | Shape | Purpose |
|---|---|---|
| `#project/*` | `<hub-slug>` | Project identifier (kebab-case, same as the hub folder) |
| `#customer/*` | `<customer-slug>` | Customer identifier — use sparingly; prefer `_TENANT.md` labels |
| `#scope/*` | `<area>` (e.g., `workspace`, `harness`, `plugins`, `context`) | Which part of the OS a governance doc covers |

## 4. Customer data labels

- Files with customer-confidential content end in `_TENANT.md`. The root `.gitignore` ignores `*_TENANT.md`
  **by default** — a safety net. To commit one, review it and the destination's visibility first, then
  `git add -f <file>`.
- Treat a customer hub's whole subtree as customer content even where filenames aren't labelled; label raw
  intake and transcripts first.
- Never paste customer-confidential content into tools, models, plug-ins or MCP servers the customer hasn't approved.
- If in doubt, add the suffix. Over-labelling is cheap; a leak isn't.
- Keep a local denylist of customer names, people, codenames and project IDs in `.agency/denylist.txt` (ignored;
  one term per line, `re:` for a pattern; matching ignores case and accents and treats a space as any run of
  spaces, hyphens, underscores or line breaks). The privacy gate (`06_Engine/harness/check-privacy.py`) blocks
  those terms plus emails, tenant/conversation IDs, meeting and document links, credentials and file metadata in
  the blank template, and warns in a workspace. Examples in the template are generic: they name no person,
  organization or real use case.

## 5. Drafts vs published

| Stage | Location | Tag | Committed? |
|---|---|---|---|
| Draft | `_drafts/` subfolder | `#status/draft` | No — `_drafts/` is git-ignored |
| Review | Parent folder | `#status/review` | Yes |
| Published | Parent folder | `#status/published` | Yes |
| Archived | In place, or an optional `Archive/` mirroring the original path | `#status/archived` | Yes |

Promotion is a manual move. Record the promotion date in front matter when it matters. A draft that must
survive a lost laptop belongs in review, not in `_drafts/`.

## 6. Front-matter

Optional for notes, expected for hub artifacts. When used, stick to this schema:

```yaml
---
title: Kickoff notes — example project
tags: [type/meeting, project/example-project, tenant/customer, status/draft, loop/understand]
status: draft
tenant: customer
loop-phase: understand            # hub artifacts
project: example-project          # = hub folder slug
owner: <single name>
created: 2026-01-20
---
```

When you instantiate a template, replace its `type: template` block with the artifact's own front matter:
set `type:` to the template's `template-for` value and fill the fields above. Decision records follow the
decision-record/v2 schema instead (see [W5](../02_Workflows/workflows/W5-decide.md)).

### 6.1 Artifact relationship contract

Canonical artifacts declare at least one outbound relationship so evidence and downstream use stay traceable.

```yaml
type: jtbd
informs: [02_design/checkout-pov.md]
informed-by: [01_understand/2026-03-02-checkout-research.md, stakeholders/product.md]
addresses: [pain-unclear-delivery-cost]          # pain or opportunity slugs
references-personas: [persona-weekend-shopper]
references-wiki: [_wiki/entities/example-project.md]
```

| Field | Relationship | Use when |
|---|---|---|
| `informs` | informs | This artifact feeds a downstream artifact (JTBD → POV → PRD) |
| `informed-by` | informed_by | This artifact derives from upstream evidence or research |
| `addresses` | addresses | This artifact resolves a named pain or opportunity |
| `references-personas` | describes | This artifact is scoped to a persona |
| `references-wiki` | cites | This artifact cites a wiki entity, concept or synthesis |
| `supersedes` | supersedes | This artifact replaces an older one |

Paths are hub-relative (`01_understand/…`) or repo-relative. The
[`canonical-artifacts`](../03_Agents-and-Skills/Skills/canonical-artifacts/SKILL.md) skill's
`artifact-missing-relationship` lint enforces the contract in hub phase folders for `type:` `problem-frame`,
`research-report`, `persona`, `jtbd`, `journey-map`, `pov`, `brief`, `prd`, `handoff`, `test-plan`,
`evidence-brief` and `retro`.

## 7. Maintenance cadence

- **Weekly (15 min):** triage `_drafts/` (promote or delete); review open Yellows against their expiry;
  refresh the checkpoint of any interrupted multi-step task.
- **Monthly (30 min):** triage the [OS backlog](../00_Agentic-OS/OPTIMIZATION-BACKLOG.md) and component
  backlogs without duplicating them; close or retire finished hubs; prune stale drafts.
- **Quarterly (1 hr):** audit tag and naming drift; re-check the [capability map](domain-coverage-map.md)
  against what actually runs; review mounted plug-in editions.

Cadence is not authorization: deleting, archiving or rewriting history still needs the owner's approval.
When the team grows, a `CODEOWNERS` file can gate `02_Workflows/`, `03_Agents-and-Skills/` and `06_Engine/`.

## 8. Credentials and secrets

**Principle: commit work product; never commit credentials; don't commit what a tool can rebuild.**
This template keeps a conservative ignore list on purpose — vendoring dependencies or build output is an
explicit, reviewed decision for a team to make, not a default.

| Category | Rule | Examples |
|---|---|---|
| Credentials and credential-bearing files | 🔴 Never commit | `.env`, `.env.*`, private keys (`*.pem`, `*.key`), tokens, passwords, connection strings, browser auth state and cookies, logs or captures that contain them |
| Rebuildable or machine-local files | Not committed (git-ignored) | Dependencies (`node_modules/`), virtualenvs (`.venv/`), caches (`__pycache__/`, `.pytest_cache/`), build output (`dist/`, `build/`, `.next/`, `.turbo/`), OS/editor noise (`.DS_Store`, `Thumbs.db`), tool scratch (`.playwright-mcp/`, `.copilot-tracking/`) |
| Customer-labelled files and drafts | Ignored by default; opt in after review | `*_TENANT.md`, `_drafts/` |
| Work product | 🟢 Commit | Templates, frameworks, skills, agents, prompts, hub artifacts, wiki pages, starter source, lockfiles, plug-in profiles |

- The root `.gitignore` owns these rules. Keep exclusions there, not in nested ignore files or `.git/info/exclude`.
- `*.key` also matches Keynote decks: export decks to PDF, or add one deliberately with `git add -f` after review.
- **Before every commit**, review the staged diff locally for credentials — by eye or with a secret scanner:
  `sk-…`, `ghp_` / `gho_`, `xoxb-`, `AKIA…`, `-----BEGIN … PRIVATE KEY-----`, passwords inside connection
  strings, and high-entropy values assigned to `*_key` / `*_token` / `*_secret`. Any hit: unstage, remove,
  and rotate the credential. Don't paste candidates into online checkers.
- Ignoring a file neither untracks it nor erases history. A credential that was ever pushed must be rotated.
- Credentials live in an OS keychain, a secret manager or the host's environment variables — never in notes,
  prompts, `agency.yaml`, or MCP configuration committed to the repository.

## 9. Large media

- Recordings, video renders, model weights and large design source files: track them with Git LFS
  (`git lfs track "*.mp4"` writes `.gitattributes`) within your host's quotas — GitHub rejects ordinary files
  over 100 MiB — or keep them in approved external storage and commit a small manifest (location, owner,
  checksum, how to fetch).
- Keep transcripts, captions, manifests and summaries with the work (the hub's `00_context_intake/`), even
  when the raw recording lives elsewhere. A symlink is a pointer, not a backup.
- Storage location never changes confidentiality: customer recordings go only where the customer approved.
- A transcript is not a replacement for the original. Deleting or moving originals needs the owner's
  approval and a recovery plan.

## 10. Generated-output routing

| Output | Lives in | Rule |
|---|---|---|
| Discovery links — `.github/{skills,agents,prompts}/`, `.claude/{skills,agents,commands}/` | Host discovery folders | Generated symlinks only. Author the source under `02_Workflows/` or `03_Agents-and-Skills/`, then run `python3 06_Engine/scripts/agency.py sync` |
| Catalogs and indexes — `03_Agents-and-Skills/INDEX.md`, `_wiki/index.md`, `_wiki/index.jsonl`, `_wiki/_digest.md` | Beside their sources | Generated. Edit the sources, then regenerate |
| Task evidence — QA screenshots, test receipts, review notes, eval reports | With the task that owns it: the hub phase folder (e.g. `03_build/<name>/evidence/`), or `00_Agentic-OS/_runs/<YYYY-MM-DD>-<slug>/` for OS work | Never the repository root or a discovery folder |
| Scratch — automatic browser captures, temporary exports, tool caches | The OS temp directory or user cache, outside the repository | Disposable; never the only copy of evidence |
| Engine project state — PDG runs, VPG films | The hub phase folder that owns the project | The engine's own schema governs its files |

Three scopes stay independent: **Git eligibility** (`.gitignore`), **editor visibility** (search and
file-watcher excludes) and **agent retrieval** (what a task loads). Don't hide files from Git to quiet an
editor, and don't load the whole repository into an agent because Git tracks it.

## 11. Paths and links

- **Relative Markdown links resolve from the file's real location.** `06_Engine/harness/check-links.py`, run by
  `python3 00_Agentic-OS/agentic-os-review.py`, fails on any broken link — including through discovery links.
- **Depth parity.** Native skills (`03_Agents-and-Skills/Skills/<slug>/SKILL.md`, depth 3), agents
  (`03_Agents-and-Skills/Agents/<slug>.agent.md`, depth 2) and prompts (`02_Workflows/prompts/<name>.prompt.md`,
  depth 2) sit at the same depth as their discovery links in `.github/` and `.claude/`, so one relative link
  works through both paths. Keep that property: don't nest these files deeper.
- **Repo-root paths for agents.** In instructions an agent must follow, also give the repo-root-relative path
  in backticks — `02_Workflows/workflows/W5-decide.md` — because agents run from the repository root.
- **No absolute personal paths** — nothing rooted in a home directory (macOS `/Users`, Linux `/home`, Windows
  `C:\Users`). Use repo-relative paths, `<placeholders>` or environment variables; `06_Engine/harness/check-template.py`
  flags them.
- **Never link into a plug-in mount**; it may not be checked out. Name such paths in backticks
  (`02_Workflows/prototype-design/`).
- **Placeholders are not links.** Write placeholder paths in backticks or code fences, not as live links.
- **Templates must survive copying.** Hub-root templates (`intake.md`, `execution-plan.md`) may use `../../…`
  links because the hub root and `00_README/_templates/` sit at the same depth. Phase templates name repo
  files by repo-root path in backticks.
- **Hubs copy as a unit.** Links inside `_template-project/` resolve unchanged in `01_Project-Hubs/<slug>/`.
- **Wiki links** (`[[entities/example-project]]`) are for pages inside a hub's `_wiki/`; use Markdown links elsewhere.
- **Anchors** use GitHub-style heading slugs (`CONVENTIONS.md#4-customer-data-labels`). Renaming a heading
  breaks inbound anchors — search before renaming.

## Changing these conventions

Change the rule here in the same commit as the files that depend on it. If later work must follow the change,
record it through [W5](../02_Workflows/workflows/W5-decide.md); if it changes who owns a concept, update
[AUTHORITIES](../AUTHORITIES.md).
