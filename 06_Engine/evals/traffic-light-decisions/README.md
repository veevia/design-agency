# Eval \u2014 traffic-light-decisions

Three fixtures, each violating one Traffic Light rule:

| Fixture | Violation |
|---|---|
| `0001-vendor-x-yellow-missing.md` | Yellow without `trigger:` or `expiry:` |
| `0002-partner-api-red-missing-unblock.md` | Red without `unblock_owner:` |
| `0003-team-owner-violation.md` | `owner: the team` (must be single name) |

Run: `python 06_Engine/evals/run-evals.py traffic-light-decisions`

Lifecycle, canonical-set, and supersession-chain behavior is covered by the stricter Python suite at
`03_Agents-and-Skills/Skills/traffic-light-decisions/tests/test_check_decision.py`.
