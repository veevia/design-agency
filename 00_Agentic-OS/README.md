# Agentic-OS — task operating guide

**TL;DR:** Scope → retrieve → execute → verify → hand off. Read only the contract the current question needs.

## Six architecture contracts

| Layer / contract | Read it to resolve… |
|---|---|
| [L0 — Authority & safety](decisions/l0-authority-and-safety.md) | Source conflicts, permission, safety, repository and plug-in boundaries |
| [L1 — Knowledge & context](decisions/l1-knowledge-and-context.md) | Retrieval, durable memory, interrupted work |
| [L2 — Capabilities & interfaces](decisions/l2-capabilities-and-interfaces.md) | Choosing a capability, contracts, plug-in profiles, authoring ownership |
| [L3 — Task control](decisions/l3-task-control.md) | Scope, next action, planning, workflows, decision capture, engine gates |
| [L4 — Delivery & outcomes](decisions/l4-delivery-and-outcomes.md) | Required outcome, acceptance, handoff |
| [L5 — Verification & learning](decisions/l5-verification-and-learning.md) | Evidence, failures, regressions, improvement loops, promotion |

Exactly six canonical ADRs, `aos-0001`–`aos-0006`. Layers are responsibilities, not folders, privilege
levels or mandatory stages. [ARCHITECTURE](../00_README/ARCHITECTURE.md) maps them to the repository.

## Execute a task

1. **Scope.** State the outcome, affected files, permissions and acceptance criteria. Inspect existing changes
   and protect other work. A question does not authorize implementation.
2. **Retrieve.** Follow [AGENTS.md](../AGENTS.md) and the [authority registry](../AUTHORITIES.md). Search the
   [capability catalog](../03_Agents-and-Skills/INDEX.md) and the hub's `_wiki/index.md`; load only what applies.
3. **Execute.** Advance the current step with the selected capability. Routine progress, fixes, refactors and
   maintenance need no decision record.
4. **Verify.** Check current behaviour against acceptance; widen regression checks with risk. Record method,
   results, failures and gaps. Schema validity is not runtime health.
5. **Hand off.** Return the result, paths, acceptance evidence and blockers or the next action. Publishing,
   restarts and external changes need the user's authorization.

## Keep context in proportion

| Task | State to keep |
|---|---|
| Question or one-step change | Sources, relevant diff or test, final answer; no journal |
| Multi-step work in one session | One live plan linked to the task's evidence |
| Research-heavy, 5+ steps, interruptible or cross-runtime | One durable checkpoint with [L1's fields](decisions/l1-knowledge-and-context.md#decision), refreshed before handoff |

## When a decision is needed

Use [W5 — Decide](../02_Workflows/workflows/W5-decide.md) for a new durable choice, an explicit capture request
or a lifecycle change. Validate records with
`python3 03_Agents-and-Skills/Skills/traffic-light-decisions/scripts/check_decision.py <file>`.

## Plug-in engines

PDG (prototypes) and VPG (demo films) are graph engines with their own state machines, ledgers and human
gates. Their host adapters (`/prototype-design`, `/video-production` and the matching SOPs) appear once the
plug-in is added. The engine decides completion; adapters and agents never approve on a person's behalf.
See [PLUGINS](../00_README/PLUGINS.md).

## Improve the system

- [OPTIMIZATION-BACKLOG](OPTIMIZATION-BACKLOG.md) — the one ranked queue for cross-cutting improvements.
- [Initiatives](initiatives/README.md) — standing goal + rubric pairs that drive measured loops:
  [OS optimization](initiatives/optimization/os-optimize.goal.md) and
  [plug-in optimization](initiatives/plugin-optimization/plugin-optimize.goal.md) (for example the FDE toolkit).
- [_runs/](_runs/README.md) — dated evidence of each loop cycle.
- [agentic-os-review.py](agentic-os-review.py) — the integrity verdict every cycle must keep green.

```sh
python3 00_Agentic-OS/agentic-os-review.py          # full review; exit 0 only when every MUST row passes
python3 00_Agentic-OS/agentic-os-review.py --fast   # quick pre-commit subset
```
