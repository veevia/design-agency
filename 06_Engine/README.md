# 06_Engine — the machinery under the OS

**TL;DR:** The `agency` engine wires capabilities and plug-ins into every agent runtime; the harness, retrieval tools, evals and tests turn the OS rules into checks that the review aggregates.

| Folder | Purpose | Entry point |
|---|---|---|
| [`agency/`](agency/) | Python package: configuration (`agency.yaml`), plug-in profiles and lifecycle, capability catalog, discovery links, portfolio report | `scripts/agency.py` |
| [`plugins/`](plugins/) | Plug-in profiles (`<name>.plugin.yaml`); schema in [PLUGINS](../00_README/PLUGINS.md#profile-schema-agency-pluginv1) | `agency.py plugin list` |
| [`scripts/`](scripts/) | CLI and git hooks | `agency.py`, `install-hooks.sh` |
| [`harness/`](harness/README.md) | Gates: skill spec, contracts and lints, SOP lint, catalog, links, hygiene, privacy, capability map | `../00_Agentic-OS/agentic-os-review.py` |
| [`retrieval/`](retrieval/README.md) | Wiki indexes, digests and neighbour lookup for `/context-pull` | `retrieval/build-wiki-index.py` |
| [`evals/`](evals/README.md) | Golden tasks proving lint rules still catch their target violations | `evals/run-evals.py` |
| [`tests/`](tests/) | Engine unit and end-to-end tests (fixture plug-in as a real submodule) | `python3 -m unittest discover -s 06_Engine/tests -t 06_Engine/tests` |

## Common commands

```sh
python3 06_Engine/scripts/agency.py status                  # mode, capabilities, plug-ins, discovery
python3 06_Engine/scripts/agency.py sync [--check]          # regenerate links + catalog, or verify both
python3 06_Engine/harness/build-skill-index.py [--check]    # generate or verify the capability catalog
python3 06_Engine/harness/lint-skill.py --all --severity error
python3 06_Engine/harness/lint-skill.py --contract          # every native skill ≥ 10/12 or exempt
python3 06_Engine/harness/spec-compliance.py                # portable name + "Use when" trigger
python3 06_Engine/harness/check-links.py                    # links, wiki-links, depth parity
python3 06_Engine/harness/check-template.py                 # hygiene and template-mode rules
python3 06_Engine/harness/check-privacy.py [--history REF]  # personal/customer data and file metadata
python3 06_Engine/scripts/agency.py publish-check --remote origin   # release gate (see 00_README/RELEASING.md)
python3 06_Engine/evals/run-evals.py
python3 00_Agentic-OS/agentic-os-review.py                  # everything above, one verdict
```

The only third-party dependency is PyYAML ([requirements.txt](requirements.txt)). Plug-in engines bring their
own requirements and run with their own interpreter.
