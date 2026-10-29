# Agent schema — the executable contract for AGENT.md

Every agent under `03_Agents-and-Skills/Agents/<slug>/` MAY include an `AGENT.md` with a structured contract. Used by `/capability-spot`, sub-agent delegation, and `/skill-lint`-style validation.

## Front-matter spec

```yaml
---
# REQUIRED
title: <human-readable name>
description: <one sentence>
status: stable | beta | draft

# REQUIRED — scope (kills cross-program context bleed)
scope:
  programs: ["*"]                  # ["*"] = any; ["example-project","pilot-project"] = bounded
  reads_only: true | false         # if true, must not write files

# OPTIONAL — what this agent owns
owns_sops: [<SOP id>]              # SOPs whose owner_agent is this agent
must_load_skills: [<skill slug>]   # always loaded before any action
may_load_skills: [<skill slug>]    # load on demand

# OPTIONAL — return contract for sub-agent use
returns:
  format: structured-summary | freeform | none
  max_tokens: <int>                # for sub-agents, keep ≤2000
  must_cite: true | false          # if true, every claim must reference a source/wiki page

# OPTIONAL — invocation hints
when_to_invoke:
  - <natural-language trigger>

# OPTIONAL — context budget
budget:
  context_tokens_max: <int>
---
```

## Minimal example — a bounded sub-agent

```yaml
---
title: Hub researcher (bounded sub-agent)
description: Read-only researcher for one project hub; returns a ≤2k-token structured summary with citations. Use when the main agent needs hub context without filling its own window.
status: beta
scope:
  programs: ["example-project"]
  reads_only: true
must_load_skills:
  - evidence-tagging
  - wiki-maintenance
  - context-pull
returns:
  format: structured-summary
  max_tokens: 2000
  must_cite: true
when_to_invoke:
  - Main agent needs to gather hub wiki context without polluting its own window
  - Parallel research across one hub's sources
budget:
  context_tokens_max: 20000
---
```

## Why this matters

- **Anthropic sub-agent isolation pattern.** Bounded scope + bounded return tokens = the main agent stays focused.
- **Self-documenting.** Reading `AGENT.md` tells you exactly what an agent can and can't do.
- **Verifiable.** A future lint can check that an agent declared `scope.programs: ["example-project"]` never reads files under `01_Project-Hubs/pilot-project/`.

## Migration policy

- Existing agents in `03_Agents-and-Skills/Agents/` are not auto-migrated. Document the schema; maintainers adopt when convenient.
- New per-program bounded sub-agents are introduced as a separate capability backlog item.

## See also

- [`skill-schema.md`](skill-schema.md) — analogous contract for skills
- [`../../03_Agents-and-Skills/Agents/`](../../03_Agents-and-Skills/Agents/)
- [Anthropic — Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (sub-agent architectures section)
