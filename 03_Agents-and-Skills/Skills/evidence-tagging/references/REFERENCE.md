# Evidence tagging — label reference and promotion rules

On-demand detail for the `evidence-tagging` skill: the exhaustive decision rules, the front-matter
shortcut, and a worked example to pull in only when a claim is ambiguous.

Framework: [`00_README/_frameworks/house-principles.md`](../../../../00_README/_frameworks/house-principles.md) — principle 4, evidence over opinion.

## 1. The three labels

| Label | Definition | Threshold | Source |
|---|---|---|---|
| `observed` | Direct, unprompted evidence: a participant did or said it, you saw it, telemetry shows it | ≥2 independent participants or data points for a non-trivial finding; single-source → `n=1` | Required — `[observed \| <slug>]` |
| `reported` | Third-party claim not validated here: vendor docs, secondary research, a colleague's summary | Cite it; do not promote without re-verification | Required — `[reported \| <slug>]` |
| `assumed` | Team hypothesis, listed for traceability | Name the cheapest test that would resolve it | Optional — `[assumed]` |

The enum is closed. If no label fits, the claim is not ready for the page.

## 2. The page-level shortcut

When an entire page is one evidence class, declare it once:

```yaml
---
type: entity
evidence-default: reported     # most claims here come from vendor documentation
sources: [2026-01-10-vendor-demo]
---
```

Individual claims then need an inline tag only when they deviate. Both `check_tags.py` and the
workspace lint honour this. A `type: source` page is self-citing — the page *is* the source — so it
may declare `evidence-default` without a separate `sources:` list.

## 3. Promotion rules — never silent

- `assumed → reported` when a third-party source confirms it.
- `reported → observed` only after first-hand validation (interview, usability session, telemetry).
- Any AI-generated summary, transcript recap, or search answer stays `reported`.
- Log each promotion, with its date, in the page's source list.

## 4. Why it matters

A customer deck full of untested `reported` claims is how a design gets walked back in the room.
Tags make the unvalidated, load-bearing claims visible so you validate them first.

## 5. Worked example — a mixed-evidence finding

```markdown
## Finding: the same request is checked twice — once by the coordination team and again by the site

- The same booking is re-checked against the CRM, service-contract database and inventory system by the coordination team and again by the site [observed | 2026-01-20-coordinator-survey, 2026-01-22-interviews]
- Request data is "spread across too many systems" [reported | 2026-01-20-coordinator-survey]
- Connecting the systems would save ~60% of duplicate effort [assumed]
  - cheapest test: time-box two coordinators on the same morning queue and measure overlap
```

Two independent sources → `observed`. One survey quote → `reported`. An untested estimate →
`assumed`, with its test named.

## 6. `check_tags.py` versus the workspace lint

- `check_tags.py <file>` — author-time, single file, standard library only.
- `lint-skill.py evidence-tagging` — workspace-wide, exclude-calibrated; the pre-commit bar.

## See also

- Skill: [`../SKILL.md`](../SKILL.md)
- Validator: [`../scripts/check_tags.py`](../scripts/check_tags.py)
- Template: [`../assets/tagged-page.template.md`](../assets/tagged-page.template.md)
