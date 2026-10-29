---
description: "Health-check a hub's wiki — run discipline lint (skills) and structural lint (orphans, stale, contradictions, gaps) and return a triage table."
agent: agent
---

# /wiki-lint

Lint a hub's `_wiki/`. Returns a severity-tagged triage list. Apply each discipline skill as a check, then run structural checks.

## Inputs

- **hub** (required): folder slug under `01_Project-Hubs/`.

## Procedure

1. **Run the engine lint first** for the discipline skills that declare contracts:
   ```bash
   python3 06_Engine/harness/lint-skill.py --all --severity warning --target "01_Project-Hubs/<hub>/_wiki/**/*.md"
   ```
   Capture findings; group by skill. This catches `evidence-tagging`, `traffic-light-decisions`, `extreme-clarity`, `alignment-playbook`, `house-principles`, and the wiki skills automatically.

2. **Load the discipline skills for the judgement checks** the regexes cannot make:
   - `03_Agents-and-Skills/Skills/alignment-playbook/SKILL.md`
   - `03_Agents-and-Skills/Skills/house-principles/SKILL.md`
   - `03_Agents-and-Skills/Skills/design-thinking-loop/SKILL.md`
   - `03_Agents-and-Skills/Skills/wiki-maintenance/SKILL.md`

3. **Read `<hub>/_wiki/index.md`** to get the page inventory.

4. **Apply the judgement checks** (alignment, `house-principles`, design-thinking-loop) to the pages the index names.

5. **Structural checks:**
   - **Orphans** — wiki pages with no inbound links from `index.md` or other wiki pages.
   - **Stale** — `updated:` >30 days ago AND source count unchanged → check if superseded.
   - **Missing concepts** — concept referenced 3+ times in entities/sources/syntheses but has no `concepts/<slug>.md` page → suggest creation.
   - **Contradictions** — same factual claim with conflicting evidence between pages → list both pages and the conflict.
   - **Index drift** — pages in `entities/`, `concepts/`, `sources/`, `syntheses/`, `decisions/` not listed in `index.md` → flag.
   - **Log gap** — last `log.md` entry >14 days old → flag (wiki may be neglected).

6. **Regenerate the wiki index** as the final step:
   ```bash
   python3 06_Engine/retrieval/build-wiki-index.py <hub>
   ```
   Surfaces orphans the structural check missed; keeps `/context-pull` accurate.

7. **Output the triage table** (markdown):

   | Severity | Skill / Check | Page | Suggested action |
   |---|---|---|---|
   | 🔴 high | evidence-tagging | entities/vendor-a.md | 3 untagged claims (lines 12, 14, 17) → tag or remove |
   | 🟡 med | traffic-light | decisions/vendor-strategy.md | Yellow without expiry → add ISO date |
   | 🟡 med | structural / orphan | concepts/some-concept.md | No inbound links → link from index.md or merge |
   | 🟢 low | extreme-clarity | sources/2026-...md | TL;DR is 32 words → trim to ≤25 |

   Group rows by severity. Include a one-line summary at the top (counts per severity) and `Index regenerated: yes|no`.

8. **Append to `log.md`:**
   ```
   ## [YYYY-MM-DD HH:MM] lint
   - Discipline issues: <n> (breakdown by skill)
   - Structural issues: <n> (breakdown by check)
   - Top recommendation: <one line>
   ```

## Severity rubric

- 🔴 **high** — breaks a rule (untagged claim, Yellow without trigger, missing TL;DR on a synthesis or decision).
- 🟡 **med** — best-practice violation (orphan page, undefined acronym, stale claim).
- 🟢 **low** — style/polish (TL;DR length, adjective use, alphabetical ordering).

## When this goes wrong

- **Wiki is too small to lint** (<5 pages): say so; recommend more ingest first.
- **Many high-severity issues in one batch**: don't dump all; show top 10 + counts, offer to drill in.

## See also

- [`wiki-ingest.prompt.md`](../../02_Workflows/prompts/wiki-ingest.prompt.md)
- [`wiki-query.prompt.md`](../../02_Workflows/prompts/wiki-query.prompt.md)
- [`03_Agents-and-Skills/Skills/wiki-maintenance/SKILL.md`](../../03_Agents-and-Skills/Skills/wiki-maintenance/SKILL.md)
