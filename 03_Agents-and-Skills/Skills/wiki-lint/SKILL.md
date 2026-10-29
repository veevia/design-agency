---
name: wiki-lint
title: Triage a hub wiki for knowledge debt
description: "Run a periodic health check over a hub's _wiki/ — the discipline lints of the evidence, clarity, decision, alignment, principle, and phase skills plus structural checks for orphans, stale pages, missing concept pages, index drift, and contradictions — and return a severity-ranked triage table instead of prose. Use when running a weekly or pre-synthesis wiki health check, before a phase gate, when triaging a wiki for untagged claims, orphans, or contradictions, or when running /wiki-lint."
status: stable
when_to_load:
  - Running a periodic wiki health check (weekly, or before a synthesis or phase gate)
  - Triaging a hub wiki for untagged claims, orphans, stale pages, or contradictions
  - Running the /wiki-lint prompt
applies-to: 01_Project-Hubs/<hub>/_wiki/ lint operations
narrative: 00_README/_frameworks/design-thinking-loop.md
inputs:
  - kind: wiki-page
    where: "01_Project-Hubs/*/_wiki/**/*.md"
outputs:
  - kind: lint-triage
    schema: "Markdown table `severity | check | page | suggested action`, sorted error → warning → info, with a one-line count summary"
done_when:
  - The declared lints of every discipline skill ran against the hub
  - Structural checks ran (orphans, stale pages, concepts referenced ≥3 times without a page, index drift, contradictions)
  - The output is a severity-ranked triage table, not prose, and each finding was classified before any fix
  - The lint run was appended to the hub's _wiki/log.md
lints:
  - id: wiki-knowledge-page-missing-tldr
    severity: warning
    where: "01_Project-Hubs/[!_]*/_wiki/{entities,concepts,syntheses}/**/*.md"
    pattern: "^#\\s"
    must_also_match: "\\*\\*TL;DR"
    message: "Wiki knowledge page has no TL;DR (extreme-clarity)."
budget:
  context_tokens_max: 2500
loads: [extreme-clarity, evidence-tagging, traffic-light-decisions, alignment-playbook, house-principles, design-thinking-loop]
---

# Wiki Lint

**TL;DR:** Run every discipline skill's lints plus structural checks over a hub's wiki and hand back a severity-ranked table of what to fix first — classify each finding before fixing anything.

## When to use

- Weekly, or before a synthesis, readout, or phase gate.
- After a large ingest batch.
- When `/wiki-query` answers start contradicting each other.

Part of the wiki trio (`wiki-ingest` · `wiki-query` · `wiki-lint`).

## Steps

1. **Run the machine lints**: `python3 06_Engine/harness/lint-skill.py --all --severity warning` (or narrow with `--target "01_Project-Hubs/<hub>/_wiki/**/*.md"`).
2. **Apply the judgement checks** the regexes can't make:
   - `extreme-clarity` — TL;DR missing or over 25 words; adjective magnitudes; undefined acronyms
   - `evidence-tagging` — untagged claims; single-source `observed`; `assumed` without a test
   - `traffic-light-decisions` — Yellow without trigger or expiry; Red without unblock owner
   - `alignment-playbook` — laundered consensus; syntheses without a disagreement section
   - `house-principles` — syntheses without a point of view; unstated defaults
   - `design-thinking-loop` — `index.md` without a current-phase block; artifacts in the wrong phase folder
3. **Run structural checks**: orphans (no inbound links), stale pages (`updated:` >30 days with no new sources), concepts referenced ≥3 times without a page, pages missing from `index.md`, contradictions between pages, and a `log.md` gap of >14 days.
4. **Classify before fixing.** A count is a mix of root causes; never fabricate a tag, source, or page to clear a finding.
5. **Emit the triage table** and append a lint entry to `_wiki/log.md`.

## Output format

```markdown
## Wiki lint — <hub> — 2026-02-14

| Severity | Check | Page | Suggested action |
|---|---|---|---|
| error | observed-without-source | entities/vendor-a.md:42 | Add `[observed | <slug>]` or soften to reported |
| warning | missing-tldr | concepts/alert-routing.md | Add a `**TL;DR:**` line |
| info | adjective-magnitude | sources/2026-02-03-interviews.md:7 | Quantify "many" |

**Summary:** 1 error · 1 warning · 1 info · 0 contradictions
```

## Watch-outs

- Batch-fixing a lint count hides different root causes behind one edit.
- Embedding-based search is unnecessary below a few hundred pages; `index.md` plus reading is faster and inspectable.
- A wiki of five pages or fewer is too small to lint; ingest first.

## See also

- Reference: [`references/REFERENCE.md`](references/REFERENCE.md) — triage format and check order
- `wiki-maintenance` · `wiki-ingest` · `wiki-query` · prompt [`/skill-lint`](../../../02_Workflows/prompts/skill-lint.prompt.md)
- Prompt: [`/wiki-lint`](../../../02_Workflows/prompts/wiki-lint.prompt.md)
