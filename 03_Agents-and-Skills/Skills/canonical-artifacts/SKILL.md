---
name: canonical-artifacts
title: File and validate a canonical design artifact
description: "Author or review one of the design loop's canonical deliverables (problem frame, research report, persona, JTBD, journey map, POV, brief, PRD, handoff, test plan, evidence brief, retro) so it cites the wiki instead of duplicating it, declares its relationships, names one owner and non-goals, and lands in the right phase folder. Use when drafting any deliverable from a template, when reviewing a deliverable for citations, relationships, non-goals, or owner, or when deciding which phase folder an artifact belongs in."
status: stable
when_to_load:
  - Drafting any canonical deliverable from a template or an artifact prompt
  - Reviewing a deliverable for wiki citations, relationship fields, non-goals, and owner
  - Deciding which phase folder an artifact belongs in
  - A deliverable restates wiki content instead of citing it
applies-to: 01_understand/, 02_design/, 03_build/, 04_learn/ phase folders and the artifacts filed there
narrative: 00_README/_frameworks/design-thinking-loop.md
inputs:
  - kind: template
    where: "00_README/_templates/*.template.md"
  - kind: artifact
    where: "01_Project-Hubs/*/0[1-4]_*/**/*.md"
outputs:
  - kind: canonical-artifact
    schema: "Markdown with a TL;DR, relative-path wiki citations, evidence tags on novel claims, at least one relationship field, a non-empty non-goals section, and one named owner"
done_when:
  - The artifact opens with a TL;DR and cites wiki pages rather than restating them
  - At least one relationship field is declared (informs, informed-by, addresses, references-personas, references-wiki, supersedes)
  - Non-goals or scope-out is non-empty and the owner is one named person
  - The file sits in the phase folder that matches its type
lints:
  - id: artifact-missing-relationship
    severity: error
    where: "01_Project-Hubs/[!_]*/{01_understand,02_design,03_build,04_learn}/**/*.md"
    pattern: "^type:\\s*(problem-frame|research-report|jtbd|journey|persona|pov|brief|prd|handoff|test-plan|evidence-brief|retro)\\b"
    must_also_match: "^(informs|informed-by|addresses|references-personas|references-wiki|supersedes):"
    message: "Canonical artifact must declare at least one relationship field (informs, informed-by, addresses, references-personas, references-wiki, supersedes). See 00_README/CONVENTIONS.md."
budget:
  context_tokens_max: 2000
loads: [extreme-clarity, evidence-tagging]
---

# Canonical Artifacts

**TL;DR:** Every deliverable comes from its template, cites the wiki instead of copying it, declares how it relates to other artifacts, names one owner and its non-goals, and is filed in its phase folder.

## When to use

- You are about to draft a deliverable with an artifact prompt (`/research-synthesize`, `/persona-draft`, `/jtbd-draft`, `/journey-map`, `/design-pov`, `/design-brief`, `/prd-draft`).
- You are reviewing a deliverable before a phase gate.
- You are unsure where a file belongs.

## Steps

1. **Pick the artifact and its template** from the table below; copy the template into the matching phase folder of the project hub.
2. **Write the TL;DR first** (`extreme-clarity`) in the style of the artifact: a research report's TL;DR is its finding; a POV's is its position; a PRD's is what the user can do that they couldn't before.
3. **Cite, don't duplicate.** Every factual claim links a wiki page by relative path (for example `../_wiki/entities/vendor-a.md`). Claims not yet in the wiki carry an evidence tag (`evidence-tagging`).
4. **Declare relationships** in front-matter — at least one of `informs`, `informed-by`, `addresses`, `references-personas`, `references-wiki`, `supersedes`.
5. **Fill non-goals and the owner.** Empty scope-out is scope creep on day one; "the team" is not an owner.
6. **Take a position** on design artifacts (POV, brief, PRD) — `house-principles` principle 1 — and set a Traffic Light on gate artifacts (the PRD is a gate; the POV prepares one).
7. **Validate**: `python3 06_Engine/harness/lint-skill.py canonical-artifacts`.

| # | Artifact | Phase | Template or source | Prompt | Filed at |
|---|---|---|---|---|---|
| 0 | Problem frame | Understand (front gate) | `problem-framing` skill asset | — | `<hub>/01_understand/` |
| 1 | UX research report | Understand | `00_README/_templates/1-1-Understand_research-report.template.md` | `/research-synthesize` | `<hub>/01_understand/` |
| 2 | Persona | Understand | lean structure in the [`persona`](../persona/SKILL.md) method skill | `/persona-draft` | `<hub>/01_understand/` |
| 3 | JTBD | Understand | `1-3-Understand_jtbd.template.md` (+ `1-3b` synthesis) | `/jtbd-draft` | `<hub>/01_understand/` |
| 4 | User journey map | Understand | `1-4-Understand_journey-map.template.md` | `/journey-map` | `<hub>/01_understand/` |
| 5 | Design POV | Design | `2-1-Design_POV.template.md` | `/design-pov` | `<hub>/02_design/` |
| 6 | Design brief | Design | `2-2-Design_brief.template.md` | `/design-brief` | `<hub>/02_design/` |
| 7 | Product PRD | Design → Build | `2-3-Design_PRD.template.md` | `/prd-draft` | `<hub>/02_design/` |
| 8 | Design handoff | Design → Build | `2-4-Design_handoff.template.md` | — | `<hub>/02_design/` |

Downstream: test plan (`3-1`, `03_build/`), evidence brief (`4-1`, `04_learn/`), retro (`4-2`, `04_learn/`). Cross-cutting: typed decision records through W5 (`traffic-light-decisions`).

## Output format

```markdown
---
type: pov                      # one of the canonical types
owner: <one named person>
informed-by: ../01_understand/<persona-slug>-persona.md
references-wiki: [../_wiki/syntheses/<topic>.md]
---
# <Artifact title>

**TL;DR:** <finding / position / capability, one sentence>.

…body that cites wiki pages and tags novel claims…

## Non-goals
- <explicitly out of scope>
```

## Watch-outs

- **Restating the wiki.** Replace copied paragraphs with a citation.
- **Persona without JTBDs.** Jobs are how personas earn their keep.
- **A POV that is a situation.** A POV takes a position.
- **PRD without scope-out or rollback.** Reject it.
- **Build before the PRD lands in `02_design/`.** Phase-gate violation — see `design-thinking-loop`.

## See also

- Reference: [`references/REFERENCE.md`](references/REFERENCE.md) — relationship-field rule, the wiki–artifact contract, template maturity
- `design-thinking-loop` (phase gates) · `extreme-clarity` · `evidence-tagging` · `house-principles` · `problem-framing`
- Templates: [`00_README/_templates/`](../../../00_README/_templates/) · Prompts: [`02_Workflows/prompts/`](../../../02_Workflows/prompts/)
- Conventions: [`00_README/CONVENTIONS.md`](../../../00_README/CONVENTIONS.md)
