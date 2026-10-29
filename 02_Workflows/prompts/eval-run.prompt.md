---
description: "Run golden-task evals against the lint contracts declared in upgraded skills. PASS/FAIL per signal."
agent: agent
---

# /eval-run

Run the engine's golden-task evals. Each eval applies its skill's lint rules to fixture files and compares findings to expected signals.

## Inputs

- **target** (optional): a single skill id (e.g. `evidence-tagging`). Omit to run all.

## Procedure

1. **Run the eval script:**
   ```bash
   python3 06_Engine/evals/run-evals.py [<skill-id>]
   ```
2. **Read output line-by-line.** Each signal prints `PASS` or `FAIL` with rule id and counts.
3. **Surface to user:**
   - For each FAIL, name the eval + signal + why it failed.
   - If everything PASSes, confirm and remind: "Run `/eval-run` again after any skill front-matter edit."
4. **If any FAIL:** offer to inspect the fixture, the lint rule, or the skill front-matter.

## When to run

- Before merging any change to a `SKILL.md` with declared `lints[*]`
- Before tightening or relaxing a regex
- Whenever `/skill-lint` behaves unexpectedly on a real wiki page
- After upgrading PyYAML or Python in the workspace `.venv`

## When this goes wrong

- **`expected.yaml` references a rule that doesn't exist** — typo in rule id, or someone renamed a lint without updating the eval. Fix the eval.
- **A signal expects `min_count: 1` but gets 0** — fixture may no longer trigger; or the regex was tightened. Check the fixture, then the regex.
- **PyYAML missing** — install the harness dependencies: `python3 -m pip install -r 06_Engine/requirements.txt`.

## See also

- [`06_Engine/evals/README.md`](../../06_Engine/evals/README.md) — eval schema
- [`06_Engine/harness/lint-skill.py`](../../06_Engine/harness/lint-skill.py) — the lint runner the evals exercise
- [`skill-lint.prompt.md`](../../02_Workflows/prompts/skill-lint.prompt.md) — the workspace-wide lint
