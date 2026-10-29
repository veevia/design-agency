# Canonical artifacts — relationship fields, the wiki contract, template maturity

On-demand detail for the `canonical-artifacts` skill. `SKILL.md` carries the artifact table and the
review checklist; this file carries the one hard lint, the wiki–artifact contract in depth, and how
to treat templates that have not yet been used on a real project.

Canonical framework: [`00_README/_frameworks/design-thinking-loop.md`](../../../../00_README/_frameworks/design-thinking-loop.md)

## 1. The relationship-field rule (the one `error` lint)

Every canonical artifact (front-matter `type:` of `problem-frame`, `research-report`, `jtbd`,
`journey`, `persona`, `pov`, `brief`, `prd`, `handoff`, `test-plan`, `evidence-brief`, or `retro`)
must declare at least one relationship field. Without one, the artifact is an island that no
reviewer or agent can navigate to.

```yaml
informs: <path>               # this artifact drives that one
informed-by: <path>           # that artifact drove this one
addresses: <path>             # this answers a problem or job stated there
references-personas: [<slug>]
references-wiki: [<path>]     # the wiki pages this cites
supersedes: <path>            # this replaces an older version
```

`python3 06_Engine/harness/lint-skill.py canonical-artifacts` reports an error for any typed artifact
in a project hub that declares none of these. Template hubs (folders starting with `_`) are skipped.

## 2. The wiki–artifact contract: cite, don't duplicate

```
_wiki/entities/inventory-system.md   ← knowledge (agent-maintained)
_wiki/syntheses/request-triage.md    ← the evolving thesis (agent-maintained)
        │  cited by ↓
02_design/2026-02-24-request-triage-pov.md   ← the artifact (human co-authored)
   "We will show inventory stock inline, not replace the inventory system — see
    ../_wiki/entities/inventory-system.md and ../_wiki/syntheses/request-triage.md."
```

If you find yourself pasting a wiki paragraph into an artifact, replace it with a link. When the
wiki changes, the artifact stays true; when the artifact restates the wiki, the two drift.

## 3. Review checklist

1. TL;DR at the top, in the artifact's style (`extreme-clarity`).
2. Relative-path wiki citations for every factual claim.
3. Evidence tags on novel claims not yet in the wiki (`evidence-tagging`).
4. A stated position on POV, brief, and PRD (`house-principles` principle 1).
5. Non-goals — never empty.
6. One named owner.
7. A Traffic Light on gate artifacts (PRD = gate; POV = gate preparation).

## 4. Template maturity — treat first use as a revision

A blank template becomes trustworthy only after real use. Track maturity in your hub:

| Maturity | Meaning | What to do on use |
|---|---|---|
| 🔴 untouched | Never used on a real project | Expect to revise it; add a real (anonymised) example |
| 🟡 v1 | Used once or twice | Note friction; fix sections nobody fills |
| 🟢 stable | Used on 3+ projects without structural change | Change only through a reviewed proposal |

Record template changes through the capability lifecycle (`/skill-refine`, `/capability-spot`) rather
than editing silently, so other hubs inherit the improvement.

## 5. Anti-patterns to reject

- Artifact restates wiki content verbatim → replace with a citation.
- Persona without JTBDs cited → add the jobs or drop the persona.
- POV that describes a situation → rewrite as a position.
- PRD without scope-out → reject.
- Build started before a PRD lands in `02_design/` → phase-gate violation (`design-thinking-loop`).

## See also

- Skill: [`../SKILL.md`](../SKILL.md)
- Templates: [`00_README/_templates/`](../../../../00_README/_templates/)
- Prompts: [`02_Workflows/prompts/`](../../../../02_Workflows/prompts/)
- Conventions: [`00_README/CONVENTIONS.md`](../../../../00_README/CONVENTIONS.md)
