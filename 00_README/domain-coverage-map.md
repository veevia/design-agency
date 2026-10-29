# Task → capability → evidence

**TL;DR:** Route work to the capability that owns it; source presence, local tests and runtime execution are different claims, and each row says which one it makes.

Owner: OS steward. Coverage snapshot: **2026-10-29**. Review every row within 90 days
(`python3 06_Engine/harness/check-capability-map.py` warns when a row goes stale).

`source-checked` means the named implementation and verification route exist. `tested` means a local test
exercised it; the runtime column says what was not tested. `reported` means a plug-in owns the evidence and it
was observed in a disposable host, not certified here. `proposed` and `blocked` never count as capability.

<!-- CAPABILITY-MAP:START -->
| ID | Task | Authority | State | Owner | Verified | Runtime evidence |
|---|---|---|---|---|---|---|
| CAP-01 | Run a scoped task under explicit authority | [AGENTS.md](../AGENTS.md), [operating guide](../00_Agentic-OS/README.md) | source-checked | OS steward | 2026-10-29 [OS review](../00_Agentic-OS/agentic-os-review.py) | Static contract and entry-point checks; agent behaviour not runtime-tested |
| CAP-02 | Research, frame and specify a project | [W1](../02_Workflows/workflows/W1-understand.md), [W2](../02_Workflows/workflows/W2-design.md) | source-checked | OS steward | 2026-10-29 [Artifact contract](../03_Agents-and-Skills/Skills/canonical-artifacts/SKILL.md) | Runtime-neutral documents; delivery quality needs project evidence |
| CAP-03 | Record typed decisions (ADR, PDR, ops note, release) | [W5](../02_Workflows/workflows/W5-decide.md), [validator](../03_Agents-and-Skills/Skills/traffic-light-decisions/scripts/check_decision.py) | tested | OS steward | 2026-10-29 [Validator tests](../03_Agents-and-Skills/Skills/traffic-light-decisions/tests/test_check_decision.py) | Local unit tests; not runtime-tested through agents |
| CAP-04 | Discover skills, agents and prompts in Copilot and Claude | [Catalog engine](../06_Engine/agency/catalog.py), [discovery](../06_Engine/agency/discovery.py) | tested | OS steward | 2026-10-29 [Discovery tests](../06_Engine/tests/test_discovery.py) | Link generation and depth parity tested locally; not runtime-tested in Copilot or Claude |
| CAP-05 | Add, check, smoke-test, report and remove plug-ins | [Plug-in engine](../06_Engine/agency/plugins.py), [CLI](../06_Engine/scripts/agency.py) | tested | OS steward | 2026-10-29 [Lifecycle tests](../06_Engine/tests/test_plugin_lifecycle.py) | Fixture submodule tested locally; real plug-ins observed in a disposable host (CHANGELOG 2.0.0); not runtime-tested in agent hosts |
| CAP-06 | Apply FDE Design Toolkit skills | [Profile](../06_Engine/plugins/fde-design-toolkit.plugin.yaml) | reported | OS steward | 2026-10-29 [Plug-in guide](PLUGINS.md) | Requires the plug-in; both editions mounted, wired and checked in a disposable host |
| CAP-07 | Prototype through the PDG engine | [Profile](../06_Engine/plugins/prototype-design.plugin.yaml), [SOP](../02_Workflows/SOPs/prototype-design/SOP.md) | reported | OS steward | 2026-10-29 [Plug-in guide](PLUGINS.md) | Requires the plug-in and its companions (`--with-companions`); with them all 70 bound skills resolve and PDG's own graph validation, docs check and offline smoke pass in a disposable host |
| CAP-08 | Produce a demo film through the VPG engine | [Profile](../06_Engine/plugins/video-production.plugin.yaml), [SOP](../02_Workflows/SOPs/video-production/SOP.md) | reported | OS steward | 2026-10-29 [Plug-in guide](PLUGINS.md) | Requires the plug-in, its companions and ffmpeg; with them 42 of 44 bound skills resolve (2 tenant integrations) and checks and the offline smoke pass in a disposable host |
| CAP-09 | Retrieve maintained knowledge | [Retrieval](../06_Engine/retrieval/README.md) | tested | OS steward | 2026-10-29 [Index tests](../06_Engine/retrieval/tests/test_build_wiki_index.py) | Local tests; not runtime-tested through agents |
| CAP-10 | Run measured improvement loops for the OS and plug-ins | [Initiatives](../00_Agentic-OS/initiatives/README.md), [backlog](../00_Agentic-OS/OPTIMIZATION-BACKLOG.md) | source-checked | OS steward | 2026-10-29 [OS review](../00_Agentic-OS/agentic-os-review.py) | Procedure and gates exist; the blank template has no completed cycle |
| CAP-11 | Plan and facilitate design-sprint methods | [Sprint hub](../03_Agents-and-Skills/Skills/design-sprint-tookit/SKILL.md), [agent](../03_Agents-and-Skills/Agents/design-sprint-toolkit.agent.md) | source-checked | OS steward | 2026-10-29 [Skill spec gate](../06_Engine/harness/spec-compliance.py) | 62 contract-exempt method skills pass the spec, link and hygiene gates; facilitation quality needs workshop evidence |
| CAP-12 | Turn a talk into a captioned deck or rendered video | [demo-master](../03_Agents-and-Skills/Skills/demo-master/SKILL.md), [remotion](../03_Agents-and-Skills/Skills/remotion/SKILL.md) | tested | OS steward | 2026-10-29 [Deck evals](../03_Agents-and-Skills/Skills/demo-master/eval/run_evals.py) | Deck evals, lint, score and per-beat checks ran locally; not runtime-tested through agents; the Remotion scaffold and render were not run end to end |
| CAP-13 | Keep customer and personal data out of commits and releases | [Privacy gate](../06_Engine/harness/check-privacy.py), [release gate](RELEASING.md) | tested | OS steward | 2026-10-29 [Privacy tests](../06_Engine/tests/test_privacy.py) | Detectors, binary and embedded metadata, archives, denylists, history, tags, ref names and remote refs tested locally; not runtime-tested through agents; finds only patterns and denylisted terms |
<!-- CAPABILITY-MAP:END -->

## Runtime interpretation

- **Copilot and Claude:** generated links and prompts describe when and how to act; static checks do not prove
  that a host loaded them, nor that tools and permissions work there (backlog OS-03).
- **Plug-ins:** each owns its own quality evidence; the host records what it observed when mounting and checking.
- **Engines (PDG, VPG):** distinct execution contracts with their own gates, not synonyms for an agent host.

## Maintain and verify

```sh
python3 06_Engine/harness/check-capability-map.py                    # integrity + 90-day freshness
python3 06_Engine/harness/check-capability-map.py --integrity-only   # what the OS review requires
```

The checker validates IDs, owners, states, dates and that authority and evidence links resolve. It does not
execute them. Never advance a verification date without reviewing the row's scope.
