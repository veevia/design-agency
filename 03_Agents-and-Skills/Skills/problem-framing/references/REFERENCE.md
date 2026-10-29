# Problem Frame — section-by-section guide

On-demand detail for the `problem-framing` skill: what good looks like in each section and the
failure each section prevents.

Framework: [`00_README/_frameworks/design-thinking-loop.md`](../../../../00_README/_frameworks/design-thinking-loop.md)

## Why the frame exists

The recurring failure in client engagements: a team decides what to build before agreeing what
decisions the system must enable, and stakeholders name solutions before the problem is stable. The
cost arrives later as rework, circling feedback, and a deck of unvalidated claims. Frame first;
design second.

## The seven sections

| Section | What good looks like | Failure it prevents |
|---|---|---|
| TL;DR | One sentence: the people-problem and who has it, with numbers if known | A frame nobody can restate |
| Problem statement | The user's language, no solution nouns | Solutioning before the problem is stable |
| Decisions to enable | Concrete decisions; who makes each, cadence, data today | Listing features instead of decisions |
| Feasibility gap | Want versus achievable now; the overlap is the target | Designing for a want the platform can't deliver |
| Known/unknown data map | Known-known · known-unknown · unknown-unknown | Discovering a blocking data gap in Build |
| Stakeholder alignment map | Who wants what and where they conflict — by name | Silent disagreement resurfacing at sign-off |
| Readiness Traffic Light | 🟢/🟡/🔴 on entering research, with rationale | Researching an ungrounded problem |

## The no-solution-noun rule

Banned in the problem statement as proposals: agent, dashboard, ontology, platform, app, model,
copilot, tool, portal, pipeline, API, hub. Disclaimers are fine — `check_frame.py` ignores nouns that
are negated or quoted.

- ❌ "Coordinators need a dashboard that shows urgent requests in real time."
- ✅ "Coordinators cannot connect an incoming request to the service-contract and parts data needed to act on it,
  so the same request is checked twice — once by the coordination team and again by the site." [reported | 2026-01-20-coordinator-survey]

## Worked example (generic)

```markdown
---
type: problem-frame
hub: example-project
owner: Lead Coordinator
light: yellow
trigger: three coordinators confirm the decision list in interviews
expiry: 2026-03-15
informed-by: ../00_context_intake/2026-01-12-kickoff-notes.md
---
# Request triage — Problem Frame

**TL;DR:** Coordinators spend ~40 minutes each morning deciding which of ~40 overnight requests are urgent, and
cannot see whether a site already picked one up.

## Decisions to enable
- Which requests need a specialist today — coordinator, daily, today from the booking inbox + a spreadsheet
- Which site takes a request — lead coordinator, per request, today by phoning the sites
```

## See also

- Skill: [`../SKILL.md`](../SKILL.md)
- Validator: [`../scripts/check_frame.py`](../scripts/check_frame.py)
- Template: [`../assets/problem-frame.template.md`](../assets/problem-frame.template.md)
