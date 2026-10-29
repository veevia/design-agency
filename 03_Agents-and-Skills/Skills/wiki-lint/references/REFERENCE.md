# Wiki lint — triage output format and check order

`/wiki-lint` returns a severity-ranked triage table, never a wall of prose.

## Output shape

```markdown
## Wiki lint — <Hub> — YYYY-MM-DD

| Severity | Check | Page | Suggested action |
|---|---|---|---|
| error   | observed-without-source | entities/vendor-a.md:42 | Add `[observed | <slug>]` or soften to reported |
| warning | missing-tldr            | concepts/alert-routing.md | Add a `**TL;DR:**` line at the top |
| warning | laundered-consensus     | syntheses/vendor-strategy.md:18 | Replace "the team feels" with named positions |
| info    | adjective-magnitude     | sources/2026-02-03-interviews.md:7 | Quantify "many" |

**Summary:** 1 error · 2 warnings · 1 info · 0 contradictions
```

## Check order

1. **Discipline lints** — each skill's declared `lints[]`, then the judgement checks the regexes miss.
2. **Structural checks** — orphans, stale pages, concepts referenced ≥3 times without a page, index
   drift, contradictions, log gaps.
3. **Emit the table** sorted error → warning → info.

## Running the real lints

```sh
# every declared lint at error severity (the pre-commit bar)
python3 06_Engine/harness/lint-skill.py --all --severity error

# one skill, narrowed to one hub
python3 06_Engine/harness/lint-skill.py evidence-tagging --severity warning \
  --target "01_Project-Hubs/<hub>/_wiki/**/*.md"
```

Author-time single-file checkers live in the discipline skills' `scripts/` folders:
`check_tags.py` (evidence-tagging), `check_clarity.py` (extreme-clarity), `check_frame.py`
(problem-framing), and `check_decision.py` (traffic-light-decisions).

## See also

- Skill: [`../SKILL.md`](../SKILL.md)
