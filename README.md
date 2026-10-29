# Design Agency OS

**TL;DR:** A blank, plug-and-go operating system for design and FDE work: agents follow one rule set, capabilities reach Copilot and Claude through generated discovery, plug-ins (FDE Design Toolkit, PDG, VPG) mount with one command, and one review proves the repository is sound.

```
    ┌────────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ UNDERSTAND │───▶│  DESIGN  │───▶│  BUILD   │───▶│  LEARN   │     project lifecycle
    └────────────┘    └──────────┘    └──────────┘    └──────────┘
    scope ─▶ retrieve ─▶ execute ─▶ verify ─▶ hand off                   every task
```

This repository is a **template and harness**. It holds the method (frameworks, templates, workflows, skills,
agents), the operating system around it (authority, contracts, discovery, plug-ins, review) and no client
work. Fork it, then add hubs and plug-ins.

## Quick start

```sh
python3 -m pip install -r 06_Engine/requirements.txt      # PyYAML; Python 3.11+
python3 00_Agentic-OS/agentic-os-review.py                # VERDICT: PASS on a fresh clone
python3 06_Engine/scripts/agency.py status                # mode, capabilities, plug-ins, discovery
python3 06_Engine/scripts/agency.py hub new example-project          # your first project hub
python3 06_Engine/scripts/agency.py plugin add fde-design-toolkit   # optional plug-ins
```

Full setup, editor notes and hooks: [SETUP.md](SETUP.md).

## Start here

| If you want to… | Read |
|---|---|
| Know the rules every agent follows | [AGENTS.md](AGENTS.md) |
| Run a task the OS way | [Operating guide](00_Agentic-OS/README.md) |
| Understand the architecture | [ARCHITECTURE](00_README/ARCHITECTURE.md) · [Authority registry](AUTHORITIES.md) |
| Add FDE, PDG or VPG | [PLUGINS](00_README/PLUGINS.md) |
| Join a project as a teammate | [How we work](00_README/HOW-WE-WORK.md) · [Glossary](00_README/GLOSSARY.md) |
| Find a skill, agent, prompt or SOP | [Capability catalog](03_Agents-and-Skills/INDEX.md) · [Workflows](02_Workflows/README.md) |
| Improve the OS or a plug-in | [Initiatives](00_Agentic-OS/initiatives/README.md) · [Backlog](00_Agentic-OS/OPTIMIZATION-BACKLOG.md) |
| Follow naming, tags and commit rules | [Conventions](00_README/CONVENTIONS.md) |

## Repository layout

| Folder | Purpose |
|---|---|
| [`00_Agentic-OS/`](00_Agentic-OS/) | Operating guide, six L0–L5 contracts, review, initiatives, backlog, run evidence |
| [`00_README/`](00_README/) | Frameworks, artifact templates, architecture, plug-in guide, conventions, capability map |
| [`01_Project-Hubs/`](01_Project-Hubs/) | One folder per project; the blank template ships only `_template-project/` |
| [`02_Workflows/`](02_Workflows/) | W1–W5 workflows, prompts (`/commands`), SOP contracts, plug-in host adapters |
| [`03_Agents-and-Skills/`](03_Agents-and-Skills/) | Native skills and agents, generated catalog, plug-in mounts for skill packages |
| [`04_MCP/`](04_MCP/) | Optional tool integrations (Playwright, MarkItDown) |
| [`05_Library/`](05_Library/) | Web-app starter and design-system guidance (bring your own design system) |
| [`06_Engine/`](06_Engine/) | `agency` engine and CLI, plug-in profiles, harness gates, retrieval, evals, tests, hooks |

`.github/` and `.claude/` carry generated discovery links plus CI; `agency.yaml` configures the OS.

## Plug-ins

| Plug-in | What it adds | Add it |
|---|---|---|
| FDE Design Toolkit | Forward-deployed design skills (public: 12; full: 68 plus reviewer agents and commands) | `agency.py plugin add fde-design-toolkit [--edition full]` |
| PDG — Prototype Production Graph | Graph engine from brief to verified prototype, driven by `/prototype-design` | `agency.py plugin add prototype-design --with-companions` |
| VPG — Video Production Graph | Graph engine for governed demo films, driven by `/video-production` | `agency.py plugin add video-production --with-companions` |
| UI/UX Pro Max | Third-party UI/UX design intelligence | `agency.py plugin add ui-ux-pro-max` |

Plug-ins mount as pinned git submodules and are improved upstream, never edited in place.

## Disciplines

- **Evidence tagging** — every claim is `observed`, `reported` or `assumed`, with a source.
- **Traffic Light decisions** — 🟢🟡🔴 on every durable decision; Yellow needs a trigger and expiry.
- **Extreme Clarity** — one-sentence TL;DR, numbers over adjectives.

## Status and privacy

Version history: [CHANGELOG.md](CHANGELOG.md). Licensed under [MIT](LICENSE); plug-ins keep their own licenses.
The template ships no customer or personal data — examples are generic and name no person, organization or real use case. Customer
material belongs only in a fork's project hubs, under the [customer-label rules](00_README/CONVENTIONS.md), and a
release passes the [privacy gate](00_README/RELEASING.md) first.
