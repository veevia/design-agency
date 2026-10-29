---
# ─────────────────────────────────────────────────────────────────────────────
# SKILL.template.md — canonical starting point for a NEW skill in this workspace.
# Copy to 03_Agents-and-Skills/Skills/<slug>/SKILL.md and fill in. Delete every
# comment line before committing. The two pre-commit gates that will judge it:
#   [2b/6] spec-compliance.py  → REQUIRES valid `name` + `description`
#   [3/6]  lint-skill --contract → REQUIRES ≥10/12 decomposition OR `contract-exempt`
# Full rule: 06_Engine/harness/skill-schema.md § "Creating a new skill".
# ─────────────────────────────────────────────────────────────────────────────

# ── SPEC-REQUIRED (agentskills.io — gated, the build fails without these) ──
name: <slug>                  # MUST equal the directory name. lowercase a-z 0-9 + single hyphens,
                              # no leading/trailing/double hyphen, ≤64 chars.
description: <what it does AND when to use it — keyword-rich, ≤1024 chars, one or two sentences>

# ── EXTENDED CONTRACT (born-executable; required unless contract-exempt) ──
title: <Imperative action phrase>   # VERB-FIRST so agents route by action.
                                    # ✅ "Score options against weighted criteria"
                                    # ❌ "Decision Matrix"  (a noun routes poorly)
status: draft                       # draft | beta | stable
when_to_load:                       # the real routing signal — concrete triggers
  - <a situation in which an agent should load this>
  - <another>

# Pick ONE of the two contract modes below ▼

# ── MODE A · EXECUTABLE skill (operates on files: reviewers, linters, filers) ──
inputs:
  - kind: <wiki-page | artifact | template | freeform>
    where: "<PURE glob — no prose suffix; put any gloss in a sibling note: key>"
outputs:
  - kind: <tagged-claim | decision-block | artifact | other>
    schema: "<one-line shape description or regex>"
done_when:
  - <checkable completion assertion>
  - <another>
lints:                              # regex-only, auditable; severity error|warning|info
  - id: <kebab-rule-id>
    severity: warning
    where: "01_Project-Hubs/*/_wiki/**/*.md"
    pattern: "<regex>"
    message: "<human-readable failure message>"
budget:
  context_tokens_max: 2000

# ── MODE B · KNOWLEDGE / TOOL-RECIPE skill (a thinking tool or a recipe; no file I/O) ──
# Delete MODE A above and use this instead. Exempts the skill from the contract gate.
# contract-exempt: "<why — e.g. design-method knowledge skill, a reusable thinking tool, not an executable contract>"
# done_when:                        # still RECOMMENDED — "what good application looks like"
#   - <observable sign the method was applied well>
# applies-to: <comma-separated situations>
# metadata:                         # arbitrary string map (spec-blessed); good for tool recipes
#   duration: <e.g. 20–30 min>

# ── OPTIONAL (any skill) ──
# narrative: 00_README/_frameworks/<file>.md   # pointer to the long-form framework
# loads: [<sibling-skill-slug>]                 # skills to load first
# license: <name or LICENSE.txt>               # spec-optional
# compatibility: <env requirements>            # spec-optional, ≤500 chars — only if real deps
---

# <Skill Display Name>

**TL;DR:** <one sentence — a reader gets the point in 10 seconds. No duplicate paragraph after this.>

## When to use

- <trigger> · <trigger> · <trigger>

## Steps

1. <numbered, concrete, executable step>
2. ...

## Output format

```markdown
<the exact shape this skill should emit>
```

## Watch-outs

- <common failure mode and how to avoid it>

## See also / Connects to

- `<sibling-skill>` — <how they relate> (reference sibling skills by bare slug, not buried path)
- Validator / template / reference, if bundled: `scripts/…` · `assets/…` · `references/REFERENCE.md`
