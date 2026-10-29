---
title: Library — reference material and starters
description: Read-only references and frozen starters that skills, agents and hubs build on; bring your own design system
tags: [type/reference, purpose/reference, status/canonical]
---

# 05_Library

**TL;DR:** Reference material the OS consumes but doesn't author — frozen web-app starters and the rules AI tools follow for UI — plus a slot for *your* design system, which the blank template deliberately doesn't ship.

## What's here

| Path | What it is |
|---|---|
| [`_starters/`](_starters/README.md) | Frozen, copy-to-use web-app starters; `next-tailwind/` is the default prototype stack |
| [`DESIGN-SYSTEM-AI-INSTRUCTIONS.md`](DESIGN-SYSTEM-AI-INSTRUCTIONS.md) | How AI tools must use your design system when they generate UI, plus a prompt-fix library |

## Bring your own design system

The template is design-system-agnostic: no tokens, component library or icon set is bundled. Register yours in
the table below in one of three ways:

1. **Pinned git submodule** for a source repository you consume:
   `git submodule add <https-url> 05_Library/<name>`, then check out a tag and commit the pointer.
2. **Package dependency** inside each prototype (`npm install <package>`) when the system ships as a package.
3. **Link only** to hosted documentation when there's nothing to vendor; agents then follow the link's guidance.

| Name | Upstream | How it's consumed | Used by |
|---|---|---|---|
| *(your design system)* | `<https-url>` | submodule / package / link | `<hubs or skills>` |

Teams often start from an open-source design system and icon set; register it in the table above.
Until you register one, the starter's theme tokens are the system. The
system-agnostic [`design-system-as-infrastructure`](../03_Agents-and-Skills/Skills/design-system-as-infrastructure/SKILL.md)
skill applies either way.

## What does NOT belong here

- Code you write or maintain — that goes in a hub (`01_Project-Hubs/<hub>/03_build/`) or `03_Agents-and-Skills/`.
  Exception: `_starters/` holds frozen starters you copy from.
- Runtime integrations (MCP servers, adapters) — those go in [`04_MCP/`](../04_MCP/README.md).
- Plug-ins — packaged skills and engines mount through `agency.py plugin add` ([Plug-ins](../00_README/PLUGINS.md)).
- Unpinned or hand-copied snapshots of someone else's repository — pin a submodule or depend on a package.

## Updating a submodule reference

```sh
git -C 05_Library/<name> fetch --tags && git -C 05_Library/<name> checkout <tag>
git add 05_Library/<name>      # commit the new pointer, with the reason
```

Fresh clones need `git submodule update --init 05_Library/<name>`. Submodule sources must be https URLs, never
local paths (`06_Engine/harness/check-template.py` checks this).
