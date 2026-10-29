# Skill schema — the executable contract

Every `SKILL.md` under `03_Agents-and-Skills/Skills/<slug>/` MAY declare a structured contract in its YAML front-matter. Skills without a contract continue to work as narrative documents. Skills with a contract become **machine-verifiable**.

## Why a contract

- Tells agents exactly when to load the skill (`when_to_load`)
- Tells agents what shape the output should take (`outputs`)
- Tells `/skill-lint` what to check (`lints`)
- Tells `/eval-run` what success looks like (`done_when`)

## Front-matter spec

```yaml
---
# REQUIRED
title: <human-readable name>
description: <one sentence; shown in agent search results>
status: stable | beta | draft

# OPTIONAL — narrative pointer
narrative: <relative path to framework file in 00_README/_frameworks/>

# OPTIONAL — when this skill should load
when_to_load:
  - <natural-language trigger>
  - <e.g. "Editing any wiki page under _wiki/">

# OPTIONAL — what the skill consumes
inputs:
  - kind: <wiki-page | claim-list | research-report | decision | freeform>
    where: <glob or path hint>

# OPTIONAL — what the skill produces
outputs:
  - kind: <tagged-claim | decision-block | tldr | other>
    schema: <one-line description or regex>

# OPTIONAL — completion assertions (used by /eval-run)
done_when:
  - <checkable English sentence>
  - <e.g. "Every non-trivial claim has a tag">

# OPTIONAL — declarative lint rules (used by /skill-lint)
lints:
  - id: <kebab-case-rule-id>
    severity: error | warning | info
    where: <glob>            # which files to check
    pattern: <regex>          # what to match
    must_also_match: <regex>  # optional secondary constraint
    forbid: <regex>           # optional inverse rule
    message: <human-readable failure message>

# OPTIONAL — context budget (informational)
budget:
  context_tokens_max: <int>

# OPTIONAL — other skills this depends on (loaded before this one)
loads: [<relative skill path>]

# OPTIONAL — workflow SOP IDs that invoke this skill
invoked_by: [<SOP id>]
---
```

## Minimal example

```yaml
---
title: Evidence tagging
description: Tag every non-trivial claim with observed/reported/assumed; evidence > opinion.
status: stable
narrative: 00_README/_frameworks/evidence-tagging.md
when_to_load:
  - Writing or editing any wiki page
  - Authoring research reports, personas, JTBDs, journey maps
inputs:
  - kind: wiki-page
    where: "_wiki/**/*.md"
outputs:
  - kind: tagged-claim
    schema: "<claim> [observed|reported|assumed | <source-slug>]"
done_when:
  - Every non-trivial claim has a tag
  - No `observed` claim missing source citation
  - Every `assumed` has a follow-up test or marker
lints:
  - id: untagged-claims
    severity: error
    where: "01_Project-Hubs/*/_wiki/**/*.md"
    pattern: "^- (?!.*\\[(observed|reported|assumed)\\b).+$"
    message: "Bullet asserts a claim without an evidence tag."
  - id: observed-without-source
    severity: error
    where: "01_Project-Hubs/*/_wiki/**/*.md"
    pattern: "\\[observed\\]"
    forbid: "\\[observed\\][^|]*$"
    message: "`observed` claims must cite a source: `[observed | <source-slug>]`."
budget:
  context_tokens_max: 2000
---
```

## Schema rules

1. **Front-matter only.** The contract lives in YAML; the body stays narrative.
2. **`done_when` is English, not code.** It describes what the eval should look for.
3. **`lints` are regex-only.** No external script calls. Keep them auditable.
4. **`severity` matters.** `error` blocks `/skill-lint` from passing; `warning` and `info` surface but do not block.
5. **`where` globs are project-hub-relative.** Use `01_Project-Hubs/*/_wiki/**/*.md` to cover all programs.

## Lint runner contract

`06_Engine/harness/lint-skill.py` accepts:
```
lint-skill.py <skill-slug-or-path> [--target <glob>] [--severity error|warning|info]
```
- If `--target` omitted, uses each lint rule's own `where`.
- Returns exit code 0 if no `error`-severity findings, 1 otherwise.
- Output format: one finding per line: `<severity> | <skill> | <rule-id> | <file>:<line> | <message>`.

## Migration policy

- **Existing skills stay valid** without a contract. They function as before.
- **Upgrade order:** discipline skills first (`evidence-tagging`, `traffic-light-decisions`, `extreme-clarity`), then artifact skills (`canonical-artifacts`, `wiki-maintenance`), then facilitation skills.
- **Never add `lints` you can't justify** with a real example of a failure mode worth catching.

## Creating a new skill — the RULE (follow the spec up front)

**Every new skill MUST start from [`SKILL.template.md`](SKILL.template.md) and satisfy the
[agentskills.io spec](https://agentskills.io/specification) + this workspace's extended contract
BEFORE it is committed.** Don't author free-hand and discover the gate at commit time — copy the
template, fill it in, self-check, then commit. Two pre-commit gates enforce this
([`../scripts/pre-commit.sh`](../scripts/pre-commit.sh)): `[2b/6]` spec-compliance and `[3/6]` contract.

### The checklist (an author/agent must satisfy all of these)

1. **Directory = name.** Create `03_Agents-and-Skills/Skills/<slug>/SKILL.md`. The `name:` field MUST
   equal `<slug>` exactly. `<slug>` is lowercase `a-z 0-9` + single hyphens, no leading/trailing/double
   hyphen, ≤64 chars. (spec-REQUIRED, gated)
2. **`description:` says what AND when**, keyword-rich, ≤1024 chars — it's how an agent decides to load
   the skill. "Helps with X" is a failure; name the trigger. (spec-REQUIRED, gated)
3. **`title:` is an imperative action phrase**, verb-first (`Score options against weighted criteria`,
   not `Decision Matrix`) — agents route by the verb. The proper noun lives in the H1 + description.
4. **`when_to_load:`** lists concrete trigger situations (the real routing signal).
5. **Choose a contract mode:**
   - **Executable** (operates on files) → declare `inputs.where` (a PURE glob), `outputs.schema`,
     `done_when`, and at least one `lints` rule. Must score **≥10/12** on the contract gate.
   - **Knowledge / tool-recipe** (a thinking tool or recipe, no file I/O) → set
     `contract-exempt: "<reason>"`. Still add `done_when` ("what good application looks like") +
     `applies-to`; use `metadata:` for recipe details (duration, etc.).
   - Picking the wrong mode is the #1 error: a blanket ≥10/12 gate would wrongly fail knowledge skills,
     which is exactly why `contract-exempt` exists. If the skill has no files to read/emit, it's exempt.
6. **Body:** open with a single `**TL;DR:**` line (10-second test, no duplicate paragraph), then
   `## When to use` / `## Steps` / `## Output format` / `## Watch-outs` / `## See also`. Reference sibling
   skills by **bare slug** (`evidence-tagging`), never a buried path. Keep `SKILL.md` lean — push long
   reference detail into `references/REFERENCE.md`, runnable validators into `scripts/`, templates into
   `assets/` (the spec's progressive-disclosure layer).
7. **Self-check before commit** (any Python 3.11+ with PyYAML):
   ```sh
   python3 06_Engine/harness/spec-compliance.py                 # name == folder, description with "Use when"
   python3 06_Engine/harness/lint-skill.py --contract <slug>    # ≥10/12 OR contract-exempt
   python3 06_Engine/harness/lint-skill.py <slug>               # declared lints fire cleanly
   python3 06_Engine/scripts/agency.py sync                     # expose it in .github/ and .claude/ and the catalog
   ```
8. **New capabilities incubate as `status: draft`** in their final folder and graduate to `beta`/`stable` once
   the gates pass and a reviewer accepts the evidence. Plug-in skills follow their own repository's rules.

### Why both axes (they're orthogonal — a skill can pass one and fail the other)

| Axis | Question | Instrument | Gate |
|---|---|---|---|
| **Spec** | Valid `name` (==dir) + `description` with a trigger? Progressively disclosed? | `spec-compliance.py` | OS review row |
| **Contract** | Born-executable — typed I/O, `done_when`, `lints` (or exempt)? | `lint-skill.py --contract` | OS review row |

## See also

- [`SKILL.template.md`](SKILL.template.md) — **copy this to start a new skill** (encodes the rule above)
- [`README.md`](README.md) — the harness overview: both gates + the smoke-test BML loop
- [`spec-compliance.py`](spec-compliance.py) — the agentskills.io spec gate (`name` + `description`)
- [`agent-schema.md`](agent-schema.md) — analogous contract for `AGENT.md`
- [`lint-skill.py`](lint-skill.py) — the lint runner + `--contract` decomposition gate
- [`../evals/`](../evals/) — golden-task harness that consumes `done_when`
- [`../../03_Agents-and-Skills/Skills/`](../../03_Agents-and-Skills/Skills/) — the skills themselves
