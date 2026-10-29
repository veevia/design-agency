---
title: Playwright MCP
description: Browser automation through the accessibility tree, with scratch kept outside the repository and evidence kept with its task
tags: [type/reference, purpose/reference, status/canonical]
---

# Playwright MCP

**TL;DR:** Let agents drive a real browser through the accessibility tree; route automatic captures to scratch outside the repository, and save evidence you keep — with an explicit filename — into the task that owns it.

## What it is

[`@playwright/mcp`](https://github.com/microsoft/playwright-mcp) is an open-source MCP server that lets an agent
drive a browser through Playwright. It works on **structured accessibility snapshots**, not screenshots — fast,
deterministic, no vision model needed.

## What grounding it provides

- Navigate, click, type and fill forms on any page
- Read structured page content without parsing HTML
- Wait for network or element events; read console messages
- Take screenshots or PDFs when explicitly asked

## How it's wired

Add a server entry to your host's MCP configuration ([where](../README.md#where-mcp-servers-are-configured)).
VS Code (`.vscode/mcp.json`):

```json
{
  "servers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y", "@playwright/mcp@<validated-version>",
        "--output-dir", "${userHome}/.cache/playwright-mcp/design-agency"
      ]
    }
  }
}
```

Claude Code: `claude mcp add playwright -- npx -y @playwright/mcp@<validated-version> --output-dir <scratch-dir>`.

- Pin a version you have tried rather than `@latest` once others rely on the setup; recheck output routing when
  you upgrade.
- The browser runs **headed by default**; add `--headless` for unattended runs and `--isolated` to keep the
  profile in memory instead of on disk.
- The first run downloads the package and a browser; later runs use the cache.

## Two kinds of output

| Output | Where it goes | Lifetime |
|---|---|---|
| Automatically named screenshots, snapshots, logs | `--output-dir`: a scratch folder **outside** the repository (user cache or temp dir) | Disposable — never the only copy of anything useful |
| Evidence you keep — QA or design screenshots | An explicit `filename` inside the owning task's folder, e.g. `01_Project-Hubs/<hub>/03_build/<name>/evidence/` | Kept and committed with the task |

Explicit filenames resolve against the MCP workspace root, not `--output-dir`. Create the evidence folder first
and pass a task-owned, repository-relative path; never a bare filename that lands at the repository root. Don't
point `--output-dir` into the repository, and don't enable automatic output eviction on a folder that holds the
only copy of evidence. The repository ignores `.playwright-mcp/`, the default scratch folder, as a safety net.
Routing rules: [CONVENTIONS §10](../../00_README/CONVENTIONS.md#10-generated-output-routing).

## When to use it

- **Public-web research** (W1): competitor positioning, pricing pages, documentation sites → wiki sources
- **Page-to-artifact pipelines**: open a URL, extract structured content, file it in a hub
- **Repeatable QA and smoke checks** on prototypes in `01_Project-Hubs/<hub>/03_build/`

## When NOT to use it

- **Authenticated vendor surfaces** (mail, files, CRM) — use a vendor integration under `04_MCP/<vendor>/`, so
  tokens stay scoped to it and no capture of protected content leaves the host
- **Mandatory training or compliance flows** — completion records are auditable; automating them is a policy violation
- **Desktop apps** — this server drives browsers only

## Safety posture

- Browser content is **untrusted input** — a prompt-injection vector. The task's permissions still apply.
- `--allowed-origins` / `--blocked-origins` narrow where the browser goes, but upstream states they are **not a
  security boundary**. Name allowed domains in the task too.
- Auth state, cookies and credential-bearing console logs are secrets, not ordinary captures
  ([CONVENTIONS §8](../../00_README/CONVENTIONS.md#8-credentials-and-secrets)). Use `--isolated` unless a task
  explicitly needs a signed-in profile.
- Don't retarget a server another active task is using; start a separate instance when the owner or output
  location changes.

## Known limits

- First run is slow (browser download)
- No persistent sign-in unless you configure a profile or storage state — deliberately
- Snapshots of very large pages are long; ask for the region you need
