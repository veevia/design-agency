---
title: MCP servers and runtime integrations
description: Optional runtime integrations any agent host can call from this repository
tags: [type/reference, purpose/reference, status/canonical]
---

# 04_MCP

**TL;DR:** Notes for optional runtime integrations — MCP servers and adapters — one folder each, with scope, wiring, safety and limits; the OS never depends on them, and no credential ever lives here.

The Design Agency OS is environment-agnostic: every workflow runs without these integrations. They add richer
grounding when a team has them. For static reference material (design systems, starters) see
[`05_Library/`](../05_Library/README.md); for packaged capabilities with their own skills or engines see
[plug-ins](../00_README/PLUGINS.md).

## What's here

| Folder | What it is | Runtime |
|---|---|---|
| [`playwright/`](playwright/README.md) | Browser automation through the accessibility tree — research, page-to-artifact pipelines, prototype smoke checks | `@playwright/mcp` (open source) |
| [`markitdown/`](markitdown/README.md) | Convert PDF, Office, images, audio, HTML and URLs to Markdown for the wiki — CLI and MCP | `markitdown` (open source) |

**Vendor integrations** — grounding from a team's own systems, for example a workplace suite,
a design tool or a CRM — go in `04_MCP/<vendor>/` with the same README pattern. They stay optional: no workflow,
skill or check may require one, and their authentication stays with the host, never in this repository.

## What does NOT belong here

- Credentials, tokens, secret URLs, browser auth state — see [CONVENTIONS §8](../00_README/CONVENTIONS.md#8-credentials-and-secrets)
- Private server configurations; keep them in your host's user-level settings
- Static reference material — that goes in `05_Library/`
- Automatic captures and logs — scratch goes outside the repository
  ([CONVENTIONS §10](../00_README/CONVENTIONS.md#10-generated-output-routing))

## Where MCP servers are configured

Each host has its own file; each integration README shows the server entry to add.

| Host | Project scope | User scope |
|---|---|---|
| VS Code (GitHub Copilot) | `.vscode/mcp.json` (`"servers"`) | User `mcp.json` via **MCP: Open User Configuration** |
| Claude Code | `.mcp.json` at the repository root (`"mcpServers"`), or `claude mcp add` | `claude mcp add --scope user` |
| Other MCP clients | Their own config file | Their own config file |

A project-scoped config is committed only when it contains no secrets — reference them through the host's
input prompts or environment variables. Pin server versions you have validated instead of `@latest` when
others depend on the setup.

## Adding a new integration

1. Create `04_MCP/<vendor-or-tool>/README.md` with: TL;DR, what it is, what grounding it provides, how it's
   wired (a server snippet without secrets), when to use and when not, safety posture, known limits.
2. Add setup glue in `04_MCP/<vendor-or-tool>/scripts/` only if needed; keep generated output out of the folder.
3. If agents need to know when to use it, add a skill under `03_Agents-and-Skills/Skills/<slug>/`.
4. Add a row to the table above and, if it covers a new task, to the
   [capability map](../00_README/domain-coverage-map.md).

## See also

- [OS backlog](../00_Agentic-OS/OPTIMIZATION-BACKLOG.md) — planned integrations and capability gaps
- [Plug-ins](../00_README/PLUGINS.md) — when an integration ships skills or an engine, package it as a plug-in instead
