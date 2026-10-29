# Optimization Backlog — Design Agency OS (ranked)

**TL;DR:** The one ranked queue for cross-cutting improvements to this template; plug-in defects stay in each plug-in's own tracker.

Owner: OS steward. Pick items through an [initiative](initiatives/README.md); record each cycle in [_runs/](_runs/README.md).
Source presence is not runtime health: close an item only with evidence.

| ID | Work | Acceptance / next action | State |
|---|---|---|---|
| OS-01 | Publish the template without customer or personal data | Done in 2.0.0: privacy gate (`check-privacy.py`, review row), release gate (`agency.py publish-check`: tree, full history, commit identities, remote refs), [RELEASING](../00_README/RELEASING.md), and publication as fresh history. | Done |
| OS-02 | FDE toolkit baseline and first upstream improvement | Run the [plug-in loop](initiatives/plugin-optimization/plugin-optimize.goal.md) on the full edition: report baseline, one agreed hypothesis, upstream change, re-pin, re-measure. | Ready |
| OS-03 | Runtime proof of discovery | Show Copilot (VS Code and CLI) and Claude Code load a native skill, agent and prompt through the generated links; record versions. Static checks only today. | Proposed |
| OS-04 | Windows discovery without symlink privilege | Add a copy mode to `agency.py sync` with drift detection, or document Developer Mode as the requirement after testing. | Proposed |
| OS-05 | More golden evals | Add an eval per executable native skill whose lints guard a discipline (`problem-framing`, `canonical-artifacts`, wiki skills). | Proposed |
| OS-06 | Optional background runtime contract | Define how a scheduler (for example a long-running agent host) consumes this OS without owning its sources. | Proposed |
| OS-07 | PDG test assumes host-relative templates (upstream) | Mounted under any host with `00_README/_templates`, PDG's `tests/test_audit_controls.py::test_every_canonical_template_a_control_document_names_exists` resolves `templates/artifacts/*` against the host root although the files live in PDG. Propose upstream: resolve against the PDG root. Engine checks and dry runs are unaffected. | Upstream issue to file |
| OS-08 | Engine skill-binding coverage | Done in 2.0.0: the 62 design-sprint method skills and four generic skills (`context-intake`, `persona-critic`, `demo-master`, `remotion`) graduated natively; engine profiles name their companion plug-ins (FDE full, Anthropic skills, Impeccable, Video Shotcraft) and `plugin add <engine> --with-companions` adds them. With companions PDG resolves 70/70 bound skills (its own `graph-validate` passes in the host) and VPG 42/44; the two remaining VPG bindings are tenant integrations (OS-09). | Done |
| OS-09 | VPG tenant bindings | VPG binds `azure-foundry-image` and `workiq-grounding`, tenant integrations a blank template cannot ship; the profile declares them as `tenant_skills`, so the review does not count them as gaps. VPG's own `test_skill_bindings_resolve_in_index` still requires every binding in the host catalog. Propose upstream: treat tenant bindings as optional. A fork with those integrations adds them as native skills. | Upstream issue to file |
| OS-10 | PDG validation without the FDE full edition | PDG binds 32 skills that only the private FDE full edition ships; a host without access fails PDG's in-host `graph-validate` (the engine still runs). Options: PDG reports missing workspace bindings as warnings, or the FDE public edition publishes those skills. | Needs owner decision |
| OS-11 | Strip file metadata | The privacy gate finds image, office and PDF metadata but does not remove it; add `agency.py scrub` (or document the per-format commands) so a flagged file can be cleaned in one step. | Proposed |
| OS-12 | Shareable denylists | Teams cannot share `.agency/denylist.txt` without revealing the names in it; support salted-hash entries so a shared list blocks terms without disclosing them. | Proposed |
