# Harness — machine-verifiable contracts

**TL;DR:** Each OS rule that can be checked from disk has a gate here; the [OS review](../../00_Agentic-OS/agentic-os-review.py) runs them all and returns one verdict.

| Gate | Checks | Run |
|---|---|---|
| [spec-compliance.py](spec-compliance.py) | Native skills: `name` equals folder; description ≤1024 chars with a "Use when" trigger; `title`; `status` | `python3 06_Engine/harness/spec-compliance.py` |
| [lint-skill.py](lint-skill.py) | `--contract`: each native skill scores ≥10/12 or is explicitly exempt. Default: runs the `lints[*]` a skill declares against its `where:` globs | `python3 06_Engine/harness/lint-skill.py --all --severity error` |
| [lint-sop.py](lint-sop.py) | SOP front-matter contract in `02_Workflows/SOPs/<slug>/SOP.md` | `python3 06_Engine/harness/lint-sop.py` |
| [build-skill-index.py](build-skill-index.py) | The capability catalog matches its sources (`--check`) | `python3 06_Engine/harness/build-skill-index.py --check` |
| [check-links.py](check-links.py) | Relative links and wiki-links resolve, also through discovery links (depth parity) | `python3 06_Engine/harness/check-links.py` |
| [check-template.py](check-template.py) | Hygiene (no dependency or cache files, no personal paths, URL submodules) and template-mode rules | `python3 06_Engine/harness/check-template.py` |
| [check-privacy.py](check-privacy.py) | No emails, tenant or conversation IDs, meeting and document links, credentials, file metadata or locally denylisted terms, including inside archives, office files, encoded text, data URIs, notebooks and symlink targets; unreadable files are reported; `--history REF` adds every path, message, tag, ref name and identity | `python3 06_Engine/harness/check-privacy.py` |
| [check-capability-map.py](check-capability-map.py) | Capability map records: IDs, owners, states, dated reviews, resolvable evidence | `python3 06_Engine/harness/check-capability-map.py` |

Schemas: [skill-schema.md](skill-schema.md) (start new skills from [SKILL.template.md](SKILL.template.md)) and
[agent-schema.md](agent-schema.md). Decision records are validated by the traffic-light-decisions skill's
`scripts/check_decision.py`.

## Adding a lint to a skill

1. Add a rule under the skill's `lints:` (`id`, `severity`, `where`, `pattern`, `message`).
2. Run `python3 06_Engine/harness/lint-skill.py <skill>` and refine the regex until false positives are rare;
   never lower the severity to hide findings.
3. Add a golden task in [`../evals/`](../evals/README.md) proving the rule still catches its target violation.

Gates enforce discipline and integrity; they are not content review, security scanning or runtime proof.
The privacy gate finds patterns and the terms you denylist; it cannot recognise a customer it was never told about.
