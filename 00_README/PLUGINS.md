# Plug-ins — mount, wire, check, improve

**TL;DR:** `python3 06_Engine/scripts/agency.py plugin add <name>` mounts a plug-in as a pinned git submodule, wires its skills, agents and commands into Copilot and Claude discovery, unlocks its host adapters and runs its health checks.

## Quick start

```sh
python3 06_Engine/scripts/agency.py plugin list                         # known plug-ins and their state
python3 06_Engine/scripts/agency.py plugin add fde-design-toolkit       # public edition (default)
python3 06_Engine/scripts/agency.py plugin add fde-design-toolkit --edition full   # full edition (needs repository access)
python3 06_Engine/scripts/agency.py plugin add prototype-design --with-companions   # PDG engine + companions
python3 06_Engine/scripts/agency.py plugin add video-production --with-companions   # VPG engine + companions
python3 06_Engine/scripts/agency.py plugin status <name>                # state, pin, contributions, requirements
python3 06_Engine/scripts/agency.py plugin check <name>                 # read-only health checks
python3 06_Engine/scripts/agency.py plugin smoke <name>                 # end-to-end smoke in a temporary folder
python3 06_Engine/scripts/agency.py plugin report <name> [--json]       # skill portfolio baseline
python3 06_Engine/scripts/agency.py plugin remove <name>                # unmount and unwire
```

Engines bind skills that live in other plug-ins (their **companions**). `--with-companions` adds the missing
companions first, in the edition the engine needs, then the engine. The same, one plug-in at a time (the FDE
full edition needs repository access):

```sh
python3 06_Engine/scripts/agency.py plugin add fde-design-toolkit --edition full
python3 06_Engine/scripts/agency.py plugin add anthropic-skills
python3 06_Engine/scripts/agency.py plugin add impeccable
python3 06_Engine/scripts/agency.py plugin add video-shotcraft          # VPG only
python3 06_Engine/scripts/agency.py plugin add prototype-design
python3 06_Engine/scripts/agency.py plugin add video-production
```

`plugin add` also switches `agency.yaml` from `mode: template` to `mode: workspace`, because a repository with a
plug-in is no longer the blank template. Commit the result: `.gitmodules`, the mount (a pinned gitlink),
`agency.yaml` and the generated links in `.github/` and `.claude/`.

## Concepts

| Term | Meaning |
|---|---|
| Profile | `06_Engine/plugins/<name>.plugin.yaml`: how the host mounts, recognises, wires and checks one plug-in |
| Mount | Fixed repository path where the plug-in is checked out as a pinned submodule |
| Edition | A variant recognised by a marker file (for example the FDE toolkit's `public` and `full`) |
| Contribution | A skill, agent or command the plug-in exposes; the engine links it into `.github/` and `.claude/` |
| Host adapter | A native prompt, agent or SOP that drives a plug-in; hidden from discovery until the plug-in is mounted |
| Check / smoke | Declared commands run by `plugin check` / `plugin smoke`, each with a declared side effect |

A plug-in is **plugged in** when its mount is checked out and an edition marker is found. There is no enabled
flag to drift. `agency.yaml` can override a plug-in's `mount`, `edition`, `source` or `branch`, or hide a mounted
plug-in from discovery with `enabled: false`.

## The plug-ins

| Plug-in | Mount | Editions (marker) | Contributes | Needs |
|---|---|---|---|---|
| `fde-design-toolkit` | `03_Agents-and-Skills/Skills/fde-design-toolkit/` | `full` (`.claude-plugin/plugin.json`), `public` (`manifest.json`) | Public: 12 skills. Full: 68 skills, 5 Copilot reviewer agents, 5 Claude agents, 7 Claude commands (prefixed `fde-`) | Python 3.11+, PyYAML |
| `prototype-design` (PDG) | `02_Workflows/prototype-design/` | `standalone` (`pdg/__main__.py`) | Unlocks `/prototype-design`, the `prototype-runner-qa` agent and the prototype-design SOP | Python 3.11+, pydantic, PyYAML, jsonschema; Node.js and Chromium for browser checks |
| `video-production` (VPG) | `02_Workflows/video-production/` | `standalone` (`vpg/__main__.py`) | Unlocks `/video-production` and the video-production SOP | Python 3.11+, pydantic, PyYAML, jsonschema, NumPy, Pillow; ffmpeg/ffprobe for the smoke run |
| `ui-ux-pro-max` | `03_Agents-and-Skills/Skills/ui-ux-pro-max-skill/` | `upstream` (`.claude-plugin/plugin.json`) | The publisher's declared skill | — |
| `anthropic-skills` | `03_Agents-and-Skills/Skills/anthropic-skills/` | `upstream` (`.claude-plugin/marketplace.json`) | Five Apache-2.0 skills the engines bind: `brand-guidelines`, `frontend-design`, `skill-creator`, `web-artifacts-builder`, `webapp-testing`. The repository's document skills are proprietary and stay unwired | — |
| `impeccable` | `03_Agents-and-Skills/Skills/impeccable/` | `upstream` (`.claude-plugin/plugin.json`), shallow | The `impeccable` frontend design-fluency skill | — |
| `video-shotcraft` | `03_Agents-and-Skills/Skills/video-shotcraft/` | `upstream` (`.claude-plugin/plugin.json`), shallow | The `video-shotcraft` skill (the repository is one skill) | Node.js for its Remotion previews |

Engines' own agent role files (`agents/*.yaml`) and node prompts (`prompts/*.md`) are internal to the engine and
are not exposed as runtime agents; the host adapters drive the engine's CLI instead.

## Interpreters for engines

Engine checks run with the first interpreter found: `--python <path>`, the `AGENCY_PYTHON` environment variable,
`<mount>/.venv`, then the interpreter running `agency.py`. `plugin status` lists missing modules. To prepare one:

```sh
python3 -m venv 02_Workflows/prototype-design/.venv
02_Workflows/prototype-design/.venv/bin/python -m pip install -r 02_Workflows/prototype-design/requirements.txt
```

## Engine projects

PDG and VPG keep their state inside each project folder (`.pdg/`, `.vpg/`), never in the engine. Put projects in
a hub phase folder and run the engine from its mount:

```sh
cd 02_Workflows/prototype-design
python -m pdg init ../../01_Project-Hubs/<hub>/03_build/<prototype> --name "<Prototype name>"
python -m pdg run ../../01_Project-Hubs/<hub>/03_build/<prototype>
```

The engines own their human gates. The `/prototype-design` and `/video-production` adapters walk an agent
through them; no agent approves on a person's behalf.

## Engine skill bindings

PDG and VPG name, in their own graphs, the skills each node may load (`skill_bindings` in the profile points
at `graph/workflow.yaml`). Bound skills come from three places:

| Source | PDG (70 bound) | VPG (44 bound) |
|---|---|---|
| Native library (blank host) | 33 | 27 |
| Companion plug-ins (`--with-companions`) | +37: FDE full edition 32, `anthropic-skills` 4, `impeccable` 1 | +15: FDE full edition 10, `anthropic-skills` 3, `impeccable` 1, `video-shotcraft` 1 |
| Tenant integrations a fork supplies (`tenant_skills`) | — | 2: `azure-foundry-image`, `workiq-grounding` |

`plugin add` and `plugin status` report the coverage, the missing skills and the companion commands; the OS review
counts gaps but not declared tenant integrations. The catalog lists every plug-in skill, so engines that check
bindings against it (PDG's `graph-validate`) pass in the host once the companions are in. It writes only skill
names between backticks, brackets or slashes, so such a textual check sees exactly the skills the host has. Without them a node
that binds a missing skill runs with less guidance, and PDG's validation fails. Close gaps by adding companions,
graduating a skill natively, or through the [plug-in optimization loop](../00_Agentic-OS/initiatives/plugin-optimization/plugin-optimize.goal.md);
never by listing skills the host does not have. Profiles declare companions and tenant integrations under
`skill_bindings` (see the schema below).

Both engines also ship test suites. Run them from the mount to prove compatibility in your host:
`cd 02_Workflows/video-production && python -m pytest -q`. Known upstream test assumptions are tracked in the
[backlog](../00_Agentic-OS/OPTIMIZATION-BACKLOG.md) (OS-07, OS-09, OS-10).

## Fresh clones, pins and updates

- A clone without submodules has registered but empty mounts. `plugin add <name>` initialises them
  (`git submodule update --init` works too). Until then their discovery links are reported as deferred, and
  the catalog keeps each plug-in's committed skill list while the recorded pin matches the gitlink; a re-pin
  without a checkout drops the list until the plug-in is checked out. A native skill cannot take a name that
  such a plug-in provides: discovery reports a conflict instead of rewriting the link.
- Update a plug-in: `git -C <mount> fetch && git -C <mount> checkout <commit>`, run `plugin check`, then commit
  the new pin. Roll back by checking out the previous commit.
- Private sources (for example the FDE full edition) need repository access. CI checks out submodules; add a
  repository secret `PLUGINS_TOKEN` that can read private plug-ins.
- `plugin add` refuses a mount that holds a copy or manual clone (not a registered submodule) and refuses a
  `--source` that differs from the registered one; switch editions with `plugin remove` then `plugin add`.
- `plugin remove` refuses when the mount has uncommitted changes or commits no remote holds, and inspects
  git's cached clone the same way when the mount is not checked out; `--force` removes anyway and keeps the
  cached clone so nothing is lost.
- `--source <path>` mounts from a local checkout for development; replace it with an https URL
  (`git submodule set-url -- <mount> <url>`) before sharing. The hygiene check rejects local sources.
- Editions marked `shallow: true` (large third-party histories) are mounted with history depth 1, and
  `.gitmodules` records `shallow = true` so later clones stay small. A shallow clone cannot prove that its
  pinned commit is on a remote, so `plugin remove` may ask for `--force`; the cached clone is then kept.

## Never edit a mounted plug-in

The mount is a derived copy (L0, L2). Improve a plug-in in its own repository and re-pin; the
[plug-in optimization loop](../00_Agentic-OS/initiatives/plugin-optimization/plugin-optimize.goal.md) and the
`/plugin-optimize` prompt guide a measured cycle.

## Profile schema (`agency-plugin/v1`)

| Key | Required | Meaning |
|---|---|---|
| `schema`, `name`, `title`, `summary`, `kind` | yes | `kind`: `skills`, `engine` or `mixed`; file name is `<name>.plugin.yaml` |
| `mount` | yes | Repository-relative mount path |
| `editions.<edition>` | yes | `source` (git URL), `branch`, `marker`, optional `provides`, `provides_from: claude-plugin`, `command_prefix`, `checks`, `smoke`, `shallow` (mount with history depth 1) |
| `default_edition` | no | Edition used by `plugin add` (default: the first) |
| `provides` | no | Shared rules for `skills` (globs ending in `SKILL.md`), `agents` (Copilot `.agent.md`), `claude_agents`, `prompts`; each rule may set `prefix`, `exclude`, `targets` |
| `checks`, `smoke` | no | Shared ordered steps: `name`, `run` (argument list with `{python}`, `{tmp}`, `{mount}`, `{root}`), `side_effects` (`none`, `temp`, `mount`), `requires`, `env`, `timeout`, `cwd`, `optional` |
| `requires` | no | `python` (minimum version), `python_modules`, `commands`, `optional_commands` |
| `host_adapters` | no | Native `prompts`, `agents`, `skills`, `sops` this plug-in unlocks |
| `project` | no | Engine project `marker`, `state_dir`, `location` (informational) |
| `skill_bindings` | no | Where an engine lists the skills its nodes load: `file`, `collection`, `field` (for example `graph/workflow.yaml`, `nodes`, `skills`); optional `companions` (plug-ins that supply bound skills: a name or `{plugin, edition}`) and `tenant_skills` (bound skills a fork supplies itself) |

Steps in one `plugin check` or `plugin smoke` run share one `{tmp}` folder and run in order. A step declared
`none` or `temp` fails as an undeclared side effect when it changes anything inside the mount (ignored files
included) or in the host repository; a `mount` step may change the mount and runs only with
`--allow-mount-writes`. Without a git checkout to compare, steps fail closed. A required step that cannot run
(missing command, mount writes not allowed) is BLOCKED and fails the run unless the step is `optional: true`.
Detection covers the mount and the host repository, not the rest of the machine: plug-ins are trusted, pinned
code that you reviewed when you added or re-pinned them.

A plug-in that ships a Claude plug-in manifest (`.claude-plugin/plugin.json`) can be wired from it with
`provides_from: claude-plugin`: its skill folders, agents and commands become contributions. A manifest whose
`skills` is `"./"` declares that the whole repository is one skill, named after the mount folder.

## Add a new plug-in

1. Write `06_Engine/plugins/<name>.plugin.yaml` (copy the closest existing profile).
2. `python3 06_Engine/scripts/agency.py plugin list` validates every profile.
3. `plugin add <name>`, then `plugin check` and `python3 00_Agentic-OS/agentic-os-review.py`.
4. Add a row to the [capability map](domain-coverage-map.md) when the plug-in covers a new task.
