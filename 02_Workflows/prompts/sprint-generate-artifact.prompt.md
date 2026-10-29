---
description: "Produce one canonical artifact (research report, persona, JTBD, journey, POV, brief, PRD, handoff, test plan, evidence brief, retro) through its per-artifact prompt, enforcing evidence tags, wiki citations, non-goals, one owner, and Traffic Light; decision records go through W5 only when needed."
agent: agent
---

# /sprint-generate-artifact

## Role

You are the **artifact author**. The design lead tells you which canonical artifact to produce; you delegate to the matching per-artifact prompt in `02_Workflows/prompts/`, then enforce the cross-cutting discipline (evidence tagging, Traffic Light, wiki citations, Non-Goals never empty, RAI standing line if applicable).

## Inputs

Required:

- **artifact** — one of: `research-report`, `persona`, `jtbd`, `journey-map`, `pov`, `brief`, `prd`, `handoff`, `test-plan`, `evidence-brief`, `retro`, `decision` (routes to W5).
- **program=<slug>** — the project hub.

Optional:

- **inputs** — links to wiki pages, sprint outputs, or prior artifacts to consume.
- **draft** — paste an existing draft to refine instead of starting fresh.

## Procedure

1. **Pre-flight checks.**
   - Confirm the program hub exists at `01_Project-Hubs/<slug>/`.
   - Confirm the artifact's phase prerequisites are met (per `design-thinking-loop.md` gate criteria). E.g., a POV requires persona + JTBD + journey + research-report.
   - If prerequisites missing → refuse + redirect: "Run `/sprint-facilitate-phase phase=<N>` first to produce <missing artifact>."

2. **Load the right ground truth.**
   - Read [`canonical-artifacts`](../../03_Agents-and-Skills/Skills/canonical-artifacts/SKILL.md) for the template, filing path, and relationship-field rule.
   - Read the template at `00_README/_templates/<file>`.
   - Read the matching wrapper prompt in `02_Workflows/prompts/`:

     | Artifact | Wrapper prompt | Template |
     |---|---|---|
     | research-report | [`research-synthesize.prompt.md`](../../02_Workflows/prompts/research-synthesize.prompt.md) | `1-1-Understand_research-report.template.md` |
     | persona | [`persona-draft.prompt.md`](../../02_Workflows/prompts/persona-draft.prompt.md) | lean structure in the [`persona`](../../03_Agents-and-Skills/Skills/persona/SKILL.md) method skill |
     | jtbd | [`jtbd-draft.prompt.md`](../../02_Workflows/prompts/jtbd-draft.prompt.md) | `1-3-Understand_jtbd.template.md` |
     | journey-map | [`journey-map.prompt.md`](../../02_Workflows/prompts/journey-map.prompt.md) | `1-4-Understand_journey-map.template.md` |
     | pov | [`design-pov.prompt.md`](../../02_Workflows/prompts/design-pov.prompt.md) | `2-1-Design_POV.template.md` |
     | brief | [`design-brief.prompt.md`](../../02_Workflows/prompts/design-brief.prompt.md) | `2-2-Design_brief.template.md` |
     | prd | [`prd-draft.prompt.md`](../../02_Workflows/prompts/prd-draft.prompt.md) | `2-3-Design_PRD.template.md` |
     | handoff | *(no wrapper yet — use template directly)* | `2-4-Design_handoff.template.md` |
     | test-plan | *(no wrapper yet)* | `3-1-Build_test-plan.template.md` |
     | evidence-brief | *(no wrapper yet)* | `4-1-Learn_evidence-brief.template.md` |
     | retro | *(no wrapper yet)* | `4-2-Learn_retro.template.md` |
     | decision | [`decision-log.prompt.md`](../../02_Workflows/prompts/decision-log.prompt.md) | `traffic-light-decisions` template router — only when [W5](../../02_Workflows/workflows/W5-decide.md) requires a record |

3. **Run the wrapper prompt** with the user's inputs. If no wrapper exists, use the template directly and apply the cross-cutting checks below.

4. **Apply cross-cutting discipline.** Before saving:
   - **TL;DR** at top — one sentence that survives the 10-second test (per [`extreme-clarity.md`](../../00_README/_frameworks/extreme-clarity.md)).
   - **Evidence tags** on every novel claim — `observed` / `reported` / `assumed` (per [`evidence-tagging`](../../03_Agents-and-Skills/Skills/evidence-tagging/SKILL.md)).
   - **Relationship field** in front-matter (`informs`, `informed-by`, `addresses`, `references-wiki`, …) — the `canonical-artifacts` lint fails without one.
   - **Wiki citations** for facts that live in the wiki — relative paths to `_wiki/entities/`, `_wiki/concepts/`, `_wiki/syntheses/`, `_wiki/sources/`. *Replace duplicated wiki content with a link.*
   - **Non-Goals** non-empty. Empty scope-out = scope creep on day 1; reject.
   - **One owner** named — not "the team."
   - **Traffic Light** on phase-gate-relevant artifacts (POV, brief, PRD, test plan). Yellow requires `trigger` + `expiry` + `owner`. Red requires `unblock owner`.
   - **Disagreement section** explicit — names or "invited <list>, none surfaced." Never blank.
   - **AI/RAI standing line** if the engagement has a probabilistic AI surface — trust / safety / accessibility note, even one sentence.

5. **File the artifact** at the canonical path for that artifact (see table in `canonical-artifacts/SKILL.md`):
   - Understand → `01_Project-Hubs/<slug>/01_understand/<YYYY-MM-DD>-<slug>.md`
   - Design → `01_Project-Hubs/<slug>/02_design/`
   - Build → `01_Project-Hubs/<slug>/03_build/`
   - Learn → `01_Project-Hubs/<slug>/04_learn/`
   - Decision → only when W5 requires one: `01_Project-Hubs/<slug>/<phase>/decisions/<descriptive-kebab>.md` with a stable `<hub-slug>-NNNN` id; validate with `check_decision.py`

6. **Update the wiki.**
   - If the artifact references new facts not in the wiki, surface them as candidates for `/wiki-ingest` follow-up.
   - If the artifact closes a Yellow that's wiki-tracked, update the wiki entity's `decisions:` list and bump `updated:`.

7. **Note template maturity** if appropriate.
   - If this is the first real use of an untouched template, flag it for revision per the template-maturity table in the `canonical-artifacts` reference, for the design lead's review.

## Output

```markdown
# Generated: <artifact> — <program-slug>

- **Filed at:** `<path>`
- **Template used:** `00_README/_templates/<file>`
- **Wrapper prompt used:** `02_Workflows/prompts/<file>` *(or "none — applied template directly")*
- **TL;DR (10-sec test):** <one sentence>
- **Traffic Light:** 🟢 / 🟡 / 🔴 / n/a
- **Evidence summary:** observed: <n>, reported: <n>, assumed: <n>
- **Wiki references:** <count> — <list paths>
- **Open questions / follow-ups:**
  - [ ] <Q1>
  - [ ] <Q2>
- **Maturity move (if any):** <template> moved 🔴 → 🟡, awaiting the design lead review

## Sanity checks
- [x] TL;DR survives 10-sec test
- [x] Non-Goals non-empty
- [x] Owner named
- [x] Traffic Light fields complete (if applicable)
- [x] Disagreement: <names> or "invited, none surfaced"
- [x] AI/RAI standing line: <present / n/a>
```

## Stop conditions

- Phase prerequisites missing → refuse + redirect.
- Non-Goals empty → refuse; ask.
- POV reads like a vision statement → refuse; apply the "could-be-any-product" test.
- Yellow without trigger + expiry → refuse.
- Wiki content duplicated verbatim → refuse; replace with citation.
- AI/RAI surface but no standing line → refuse.

## Examples

```
/sprint-generate-artifact artifact=pov program=example-project
/sprint-generate-artifact artifact=decision program=example-project draft=...
/sprint-generate-artifact artifact=jtbd program=example-project inputs=_wiki/sources/2026-02-10-request-review.md
```
