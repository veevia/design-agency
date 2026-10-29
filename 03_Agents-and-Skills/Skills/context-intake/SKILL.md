---
name: context-intake
title: File raw comms as dated hub intake
description: "File an inbound knowledge-work artifact — an email thread, a team-chat or channel export, a pasted chat log, a shared document, or call notes — as a dated Markdown file in a project hub's 00_context_intake/ with a small provenance header (source kind, capture date, evidence-default reported), so the wiki and agents ground on the whole communication surface, not only meeting recordings. Use when pasting an email thread, channel export or chat log into a project hub for grounding, when filing non-recording source material (a shared doc, a stakeholder note) into 00_context_intake/, or when keeping a connector pull as durable hub evidence."
status: draft
when_to_load:
  - Pasting an email thread, a team-chat or channel export, or a chat log into a project hub for grounding
  - Filing non-recording source material (a shared doc, a stakeholder note) into a hub's 00_context_intake/
  - Making communication that no connector pulled available to an agent, or keeping a connector pull as durable hub evidence
inputs:
  - kind: raw-comms
    where: "01_Project-Hubs/*/00_context_intake/**/*.md"
    note: "pasted or exported email, chat, channel, document or call-note text, filed as dated Markdown"
outputs:
  - kind: dated-intake-file
    where: "01_Project-Hubs/*/00_context_intake/**/*.md"
    schema: "01_Project-Hubs/<hub>/00_context_intake/YYYY-MM-DD-<topic>-<kind>.md (customer-confidential: …_TENANT.md) with front matter source-kind, captured, project, tenant and evidence-default: reported; body = the raw text"
done_when:
  - "The file is named `YYYY-MM-DD-<topic>-<kind>.md` with `<kind>` one of email, chat, channel, doc, call, and sits in a project hub's `00_context_intake/`"
  - "Front matter carries `source-kind`, `captured`, `project`, `tenant` and `evidence-default: reported`"
  - "Customer-confidential content carries the `_TENANT.md` suffix, and `git check-ignore` confirmed the path is ignored before the content was written"
  - "The body is the raw text, unedited except for noted credential redactions, and no wiki page was written (promotion is `wiki-ingest`)"
lints:
  - id: intake-missing-capture-date
    severity: warning
    where: "01_Project-Hubs/[!_]*/00_context_intake/**/*.md"
    pattern: "^source-kind:\\s*\\S"
    must_also_match: "^captured:\\s*\\d{4}-\\d{2}-\\d{2}"
    message: "Intake file declares a source-kind but no `captured: YYYY-MM-DD`; the capture date is part of its provenance."
  - id: intake-evidence-not-reported
    severity: warning
    where: "01_Project-Hubs/[!_]*/00_context_intake/**/*.md"
    pattern: "^source-kind:\\s*\\S"
    must_also_match: "^evidence-default:\\s*reported\\b"
    message: "Raw comms are a sender's claims: set `evidence-default: reported`, never `observed` (evidence-tagging)."
budget:
  context_tokens_max: 1500
loads: [evidence-tagging]
---

# Context Intake

**TL;DR:** File every inbound comms artifact — email threads, channel exports, chat logs, shared docs — as a dated, provenance-stamped Markdown file in the hub's `00_context_intake/`, so agents ground on the whole conversation, not only the recordings.

## When to use

- You have raw comms text (an email thread, a team-chat or channel export, a pasted chat, a shared doc) that project work depends on.
- Material arrived outside any automated pull, or a connector pull is worth keeping as durable hub evidence.
- Not for meeting notes you author yourself — those follow the template named in the hub's
  [intake README](../../../01_Project-Hubs/_template-project/00_context_intake/README.md) — and not for wiki pages.

## How it fits with connector pulls

| | Connector pull (optional) | `context-intake` (this skill) |
|---|---|---|
| Trigger | A question that needs data from a connected work suite | You already have raw comms text to file |
| Source | Machine pull through your tenant connector, if your fork has one | Manual paste or export |
| Destination | The connector's own cache | `01_Project-Hubs/<hub>/00_context_intake/` |
| Lifecycle | Ephemeral cache | Durable hub source material |

A connector result becomes durable evidence only when you file it through this skill; promotion into the wiki
is a separate step (`wiki-ingest`).

## Steps

1. **Pick the hub**: `01_Project-Hubs/<hub>/00_context_intake/`. Sub-folder by kind once volume grows, as the
   folder README describes.
2. **Classify confidentiality before writing** ([CONVENTIONS §4](../../../00_README/CONVENTIONS.md#4-customer-data-labels)).
   Customer-confidential content — and anything in a customer hub — gets the `_TENANT.md` suffix, which the root
   `.gitignore` ignores. Confirm before pasting real content:

   ```sh
   git check-ignore -v 01_Project-Hubs/<hub>/00_context_intake/<file>_TENANT.md
   ```

   No output means the path is not ignored: stop and fix the name (exclusions live only in the root `.gitignore`).
   Process customer content only with tools the customer approved.
3. **Name it** `YYYY-MM-DD-<topic>-<kind>.md`, with `<kind>` one of `email`, `chat`, `channel`, `doc`, `call` —
   for example `2026-01-27-pricing-review-email.md`. The prefix is the capture date; the message range goes in
   front matter.
4. **Add the provenance header:**

   ```yaml
   ---
   title: Pricing review — email thread
   source-kind: email                    # email | chat | channel | doc | call
   captured: 2026-01-27                  # the day you filed it
   date-range: 2026-01-20..2026-01-23    # optional: first..last message
   project: <hub-slug>
   tenant: internal                      # customer | internal | personal (CONVENTIONS §3)
   evidence-default: reported            # raw comms are reported, never observed
   ---
   ```

5. **Paste the content below the header, raw.** Light structure only — a `## <date> <time> — <sender>` heading
   per message. Don't summarize, reword or correct it; the wiki cites it as evidence. Strip any credential or
   token the paste happens to contain ([CONVENTIONS §8](../../../00_README/CONVENTIONS.md#8-credentials-and-secrets))
   and leave `[redacted: credential]` in its place.
6. **Stop at intake.** Run `wiki-ingest` on the new file to promote what is durable into `_wiki/sources/`.

## Output format

```text
✓ Filed: 01_Project-Hubs/<hub>/00_context_intake/2026-01-27-pricing-review-email.md
  source-kind: email · captured: 2026-01-27 · tenant: internal · evidence-default: reported
  Confidentiality: not customer content (tracked) | _TENANT.md, confirmed by git check-ignore
  Next: /wiki-ingest 00_context_intake/2026-01-27-pricing-review-email.md
```

## Watch-outs

- **Raw comms are `reported`.** A pasted email is its sender's claim, not an observed fact; never tag intake
  content `observed` (`intake-evidence-not-reported`).
- **Date-prefix or it rots.** Undated intake files don't sort and get lost
  ([CONVENTIONS §1](../../../00_README/CONVENTIONS.md#1-file-naming)).
- **Confidential before write, verified.** `00_context_intake/` is tracked by default; only `_TENANT.md` files and
  `_drafts/` are ignored. Check, don't assume.
- **Hub, not wiki — and immutable.** The wiki cites intake later. Never edit a filed intake file; file a new one.
- **Binary exports** (PDF, Office, audio): convert with the [MarkItDown adapter](../../../04_MCP/markitdown/README.md)
  and keep the `.md` beside the original; recordings follow [CONVENTIONS §9](../../../00_README/CONVENTIONS.md#9-large-media).

## See also

- `wiki-ingest` — promote durable intake into an evidence-tagged `_wiki/sources/` page
- `evidence-tagging` — why raw comms are `reported` (loaded by this skill)
- `context-pull` — retrieve the wiki context that intake later feeds
- Hub intake folder rules: [`00_context_intake/README.md`](../../../01_Project-Hubs/_template-project/00_context_intake/README.md)
