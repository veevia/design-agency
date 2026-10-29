# _runs — evidence of improvement cycles

**TL;DR:** One dated Markdown record per loop cycle: what was measured, what changed, how it was checked and how to roll it back.

The blank template ships with no runs. Name records `<YYYY-MM-DD>-<slug>.md` and keep them unchanged once
written; a later cycle adds a new record instead of rewriting history.

## Record shape

```markdown
# <YYYY-MM-DD> — <slug>

- Initiative: <optimization | plugin-optimization | …> · Backlog: <OS-NN or plug-in issue>
- Acceptance: <what must be true at the end>
- Baseline: <commands and results before the change> [observed | <source>]
- Change: <summary> · Paths: <exact paths> · Plug-in pin: <old> → <new> (if any)
- Checks: <commands and results after>; OS review verdict: <PASS | ITERATE>
- Rubric verdict: <PASS | ITERATE | BLOCKED | NOT-SCORED> — <reason>
- Rollback: <safe reversal>
- Next action: <next item or blocker with resume step>
```
