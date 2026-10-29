---
title: MarkItDown
description: Convert PDF, Office, images, audio, HTML and URLs to Markdown for the wiki — CLI and MCP server
tags: [type/reference, purpose/reference, status/canonical]
---

# MarkItDown

**TL;DR:** Turn raw intake — decks, PDFs, spreadsheets, recordings — into Markdown the hub wiki can ingest, from the terminal or as an MCP tool, without leaving your machine.

## What it is

[MarkItDown](https://github.com/microsoft/markitdown) is an open-source utility that converts files to Markdown for
LLM and text-analysis pipelines. It preserves structure (headings, lists, tables, links) rather than aiming for
pixel-faithful human reading.

## What it converts

- PDF; PowerPoint (`.pptx`), Word (`.docx`), Excel (`.xlsx` / `.xls`)
- Images (EXIF metadata + OCR) and audio (metadata + speech transcription)
- HTML, CSV, JSON, XML, ZIP (iterates contents), EPUB, YouTube URLs, and more

## How it's wired

### 1. MCP server (agent-callable)

Add a server entry to your host's MCP configuration ([where](../README.md#where-mcp-servers-are-configured)).
VS Code (`.vscode/mcp.json`), running on demand through `uvx` with no global install:

```json
{
  "servers": {
    "markitdown": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--python", "3.12", "--with", "markitdown[all]", "markitdown-mcp"]
    }
  }
}
```

It exposes a `convert_to_markdown` tool that accepts an `http:`, `https:`, `file:` or `data:` URI and returns Markdown.

### 2. CLI (terminal)

Install it as an isolated `uv` tool, so its Python (3.10+) never disturbs the engine's virtualenv:

```sh
uv tool install --python 3.12 'markitdown[all]'     # install or upgrade
markitdown path/to/deck.pptx -o deck.md             # convert a file
markitdown < report.pdf > report.md                 # or pipe content
```

## Typical use in a hub

Convert raw intake beside the original, then ingest the Markdown:

```sh
markitdown 01_Project-Hubs/<hub-slug>/00_context_intake/2026-01-20-kickoff-deck.pptx \
  -o 01_Project-Hubs/<hub-slug>/00_context_intake/2026-01-20-kickoff-deck.md
```

Then run `/wiki-ingest` on the `.md`. Tag derived facts per the
[`evidence-tagging`](../../03_Agents-and-Skills/Skills/evidence-tagging/SKILL.md) skill: content extracted directly
from a source file is `observed`; anything paraphrased downstream is `reported`.

## Known limits

- Output targets machines — tables and layout may simplify.
- OCR and transcription are basic. Optional cloud converters exist as extras (for example
  `markitdown[az-doc-intel]`); use them only for content approved for that service.
- Image and slide descriptions need an LLM client, which isn't configured by default.
- **Security:** MarkItDown reads with the current process's privileges. Don't feed it untrusted input or URLs, and
  prefer the narrowest conversion path for local files. Customer files stay on tools the customer approved
  ([CONVENTIONS §4](../../00_README/CONVENTIONS.md#4-customer-data-labels)).

## Related

- [`../README.md`](../README.md) — what belongs in `04_MCP/`
- [`01_Project-Hubs/_template-project/00_context_intake/`](../../01_Project-Hubs/_template-project/00_context_intake/README.md) — where raw intake lives
