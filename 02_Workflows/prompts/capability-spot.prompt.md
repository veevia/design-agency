---
description: "Close the self-evolution loop: scan recent session snapshots, run records, and the optimization backlog for patterns seen three or more times, and draft one proposal per pattern (SOP, skill, agent, or backlog item) under _proposed/ — never auto-graduated."
agent: agent
---

# /capability-spot

Reads the trail the OS already keeps — session snapshots, run records, the backlog — surfaces recurring patterns, and drafts proposals for the owner to review.

## Inputs

- **lookback** (optional, default 7): days of snapshots and run records to scan
- **hub** (optional): scope to one hub; omit to scan all

## Procedure

1. **Load skills**: `wiki-maintenance`, `extreme-clarity` (`03_Agents-and-Skills/Skills/<slug>/SKILL.md`).
2. **Gather evidence within the lookback window**:
   - `01_Project-Hubs/*/_wiki/sessions/<recent>.md` (session snapshots)
   - `00_Agentic-OS/_runs/<recent>.md` (optimization run records)
   - `01_Project-Hubs/*/_wiki/log.md` (recent operations)
3. **Read the queues before proposing**: [the OS backlog](../../00_Agentic-OS/OPTIMIZATION-BACKLOG.md), the catalog [`03_Agents-and-Skills/INDEX.md`](../../03_Agents-and-Skills/INDEX.md), and existing proposals under `02_Workflows/SOPs/_proposed/`, `03_Agents-and-Skills/Skills/_proposed/`, and `03_Agents-and-Skills/Agents/_proposed/`. Link existing work instead of duplicating it.
4. **Identify candidates**:
   - the same next action in 3+ snapshots → SOP or prompt candidate
   - the same manual command sequence 3+ times → SOP or automation candidate
   - skills loaded together 3+ times → composite-skill candidate
   - the same review correction 3+ times → rubric line or skill refinement (`/skill-refine`)
5. **Write one paragraph per candidate**: pattern name, frequency with links to the evidence, target (SOP · skill · agent · prompt · backlog item), effort (low · medium · high).
6. **On acceptance, draft the stub**:
   - SOP → `02_Workflows/SOPs/_proposed/<id>/SOP.md` from [`../../02_Workflows/SOPs/_template/SOP.md`](../../02_Workflows/SOPs/_template/SOP.md)
   - Skill → `03_Agents-and-Skills/Skills/_proposed/<slug>/SKILL.md` from `06_Engine/harness/SKILL.template.md`
   - Agent → `03_Agents-and-Skills/Agents/_proposed/<slug>.agent.md`
   - Backlog item → a row in `00_Agentic-OS/OPTIMIZATION-BACKLOG.md` with owner, evidence, and acceptance
7. **Stop.** The owner graduates proposals (see the lifecycle in [`03_Agents-and-Skills/README.md`](../../03_Agents-and-Skills/README.md)); `skill-agent-smith` runs the gates.

## Guardrails

- **Minimum frequency: 3.** Two occurrences are not a pattern.
- **One proposal per candidate**, not three options.
- **Never auto-graduate.** Stubs stay in `_proposed/` until the owner moves them.
- **Cite the evidence** for every proposal.

## Output format

```
=== /capability-spot (lookback=<n>d, hub=<scope>) ===
Snapshots scanned: <n> · run records scanned: <n>
Proposals (<m>):
1. <pattern name>  [SOP candidate, low effort]
   Seen: 3 snapshots — <links>
   Proposed: 02_Workflows/SOPs/_proposed/<id>/SOP.md
Below threshold: <observations seen fewer than 3 times>
```

If nothing meets the threshold, say so: `No new patterns this lookback window.`

## See also

- [`/session-snapshot`](../../02_Workflows/prompts/session-snapshot.prompt.md) — produces the snapshots this scans
- [`/workflow-audit`](../../02_Workflows/prompts/workflow-audit.prompt.md) — the forward-looking counterpart
- SOP: [`capability-spot`](../../02_Workflows/SOPs/capability-spot/SOP.md)
