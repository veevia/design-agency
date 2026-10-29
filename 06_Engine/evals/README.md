# Evals — golden-task harness

Each subdirectory is a golden task for one skill. Run with:

```bash
python 06_Engine/evals/run-evals.py            # all
python 06_Engine/evals/run-evals.py evidence-tagging
```

## Structure

```
evals/
├── _template/
│   ├── README.md
│   ├── input/             # fixture files the lint runs against
│   └── expected.yaml      # signals to match
├── <skill-id>/
│   ├── README.md
│   ├── input/
│   └── expected.yaml
└── run-evals.py
```

## What a Phase-1 eval verifies

For each skill with `lints[*]`:

1. Apply the lint rules to `input/` files.
2. Count findings per rule.
3. Compare to `expected.yaml`.
4. Report PASS / FAIL per signal.

Phase-1 evals test the **lint contract**, not the agent. They run in CLI without an LLM and catch regressions if someone edits a skill's regexes.

Later phases may add agent-driven evals (the agent fixes the input; we check the output). The schema accommodates that — add `agent_task: <prompt>` and `verify_after_fix: true` to `expected.yaml`.

## `expected.yaml` schema

```yaml
skill: <skill-id>
description: <one sentence>
signals:
  - id: <kebab-case>
    rule: <lint-rule-id>             # which rule should fire
    min_count: <int>                 # at least this many findings
    max_count: <int>                 # at most this many findings
    forbid: false | true             # if true, rule must NOT fire
```

Either `min_count`/`max_count` OR `forbid: true`. Mutually exclusive.

## Adding a new eval

1. Copy `_template/` to `<skill-id>/`.
2. Drop deliberately broken fixtures into `input/`.
3. Declare expected signals in `expected.yaml`.
4. Run `python 06_Engine/evals/run-evals.py <skill-id>`.
5. If PASS, commit.

## See also

- [`../harness/skill-schema.md`](../harness/skill-schema.md) \u2014 the lint contract
- [`../harness/lint-skill.py`](../harness/lint-skill.py) \u2014 the lint runner
