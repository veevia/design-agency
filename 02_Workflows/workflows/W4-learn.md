---
title: "W4 — Learn"
type: workflow
workflow-id: W4
status: canonical
owner: OS steward
last-updated: 2026-10-29
loop-phase: learn
inputs:
  - Shippable slice from W3
  - PRD success metrics (§6) with baselines
outputs:
  - Measurement notes against PRD metrics
  - Retro (what worked, what didn't)
  - Updated artifacts (journey map, persona, POV) reflecting new evidence
  - Decision: iterate, ship wider, or pivot
source: design-thinking-loop.md + 1-1-Understand_research-report.template.md + 0-2-Ops_operating-rhythm.template.md
tags: [type/workflow, loop/learn, purpose/measure, status/canonical]
---

# W4 — Learn

> **TL;DR:** Measure what shipped against what was promised. Distinguish what we shipped from what we learned. Send the loop back to Understand with updated artifacts, or forward to shipping wider.

## When to run

- After **W3 — Build** gate has cleared and the slice has been tested with real users (or representative audience)
- At release milestones (end of sprint, stage-gate release, or calendar review)
- Whenever a build slice has run long enough to show measurement signal

## Who runs it

| Role | Responsibility |
|---|---|
| Design lead | Owns the learn-phase synthesis |
| PM | Owns metric analysis against PRD §6 |
| Researcher (or design lead wearing that hat) | Runs post-ship usability or interview studies |
| Engineering lead | Contributes to retro; owns technical learnings |
| Sponsor | Attends the decision meeting; signs the forward path |

## Capabilities used

- Skills: `evidence-tagging`, `extreme-clarity`, `wiki-ingest`, `wiki-lint`, `canonical-artifacts`
- Prompts: `/research-synthesize`, `/session-snapshot`, `/capability-spot`, `/skill-refine`
- Agent: `demo-deck-producer` for the readout; a product demo film runs through `/video-production` (Video Production Graph plug-in, checked with `python3 06_Engine/scripts/agency.py plugin status video-production`)

## What cross-functional partners will see

| Partner | They'll receive | They'll be asked to | Time |
|---|---|---|---|
| PM | Metric analysis against PRD §Success Metrics; retro | Own metric analysis; co-decide the forward path (iterate / ship wider / pivot / stop) | 2–3 hrs |
| Engineering lead | Ops, perf, reliability data; retro | Bring technical learnings; separate "what shipped" from "what broke" | 1–2 hrs |
| Marketing / GTM | Adoption + qualitative user feedback; outside signal | Bring field reactions; help frame the outside story | 1 hr |
| Legal / Privacy / Security | Any incident signal; evidence before ship-wider | Review before scaling; re-sign if scope shifts | 30 min |
| Executive sponsor | One-page readout; forward-path recommendation | Decide: scale, hold, or stop. Sign the forward path in the evidence brief | 15 min |
| Research participants (if re-interviewed) | Follow-up invite | 15 min; share what worked and what didn't | 15 min each |

## Steps

### Step 1 — Gather the evidence

1. Pull measurement against PRD §6 metrics:
   - North star: what changed vs baseline?
   - Supporting metrics: adoption, engagement, quality, errors
   - Guardrails: did anything we promised not to degrade degrade?
2. Collect qualitative data:
   - Post-ship interviews (5–8 participants) or usability sessions if applicable
   - Support tickets, feedback channels, analytics anomalies
3. If measurement gaps exist (metric not instrumented, sample too small), say so explicitly. Do not paper over.

**Exit criterion:** All PRD §6 metrics have either a measured value or a documented gap.

### Step 2 — Synthesize learnings

1. Fill [`4-1-Learn_evidence-brief.template.md`](../../00_README/_templates/4-1-Learn_evidence-brief.template.md) (2 pages max):
   - **What we shipped** (facts, release notes)
   - **What we learned** (insights — not the same thing)
   - **What surprised us** (always exists — write it down even if small)
   - **What we got wrong** (hypotheses that didn't hold)
   - **What we still don't know** (open questions for the next loop)
2. Use `/research-synthesize` prompt if post-ship interviews were conducted.

**Exit criterion:** Evidence brief drafted.

### Step 3 — Run the retro

1. Team retro (45–60 min). Keep it blameless.
2. Use [`4-2-Learn_retro.template.md`](../../00_README/_templates/4-2-Learn_retro.template.md). Review last retro's actions first.
3. Each change-item gets an owner and a timeline, or it doesn't count.
4. Capture retro as `<project-hub>/04_learn/YYYY-MM-DD-retro.md`.

**Exit criterion:** Retro complete with owned action items.

### Step 4 — Update artifacts (the compounding step)

Most teams skip this. It's the only step that compounds learning across loops.

1. **Journey map** — update stages, pain points, moments of truth with new evidence. Change evidence tags from `assumed` to `observed` where appropriate.
2. **Persona** — update pain points, quotes, mental model if research surfaced changes.
3. **JTBD** — revisit current solutions and switching triggers. Did we see new hiring criteria?
4. **POV** — does the insight still hold? Does "what would make us wrong" now apply?
5. **PRD** — version-bump if scope or metrics change materially.

Use `v2`, `v3` versioning in the artifact front-matter. Do not silently overwrite v1 — history matters.

**Exit criterion:** Every affected UNDERSTAND / DESIGN artifact either updated with `last-updated: <today>` or marked "reviewed, no change needed."

### Step 5 — Decide the forward path

Three options; pick one:

**A. Iterate within Build** (most common)

- Slice was directionally right; refine and re-ship.
- Back to W3 with tightened scope.

**B. Ship wider**

- Slice validated; widen rollout per PRD §10 staged plan.
- Keep measuring against PRD §6.

**C. Pivot**

- Evidence invalidates the POV or PRD.
- Back to W2 (DESIGN) to rewrite POV / brief / PRD, or back to W1 (UNDERSTAND) if the research itself was off.
- Do not "just change a feature" — if the POV moves, version-bump every downstream artifact.

Record the forward path, owner, Traffic Light, evidence, and next workflow in the existing evidence
brief. Use [W5 — Decide](W5-decide.md) only for a new durable choice needing separate capture, an explicit
capture request, or a lifecycle change. Reuse sufficient rationale without another file.
Phase closure alone needs no new decision file.

**Exit criterion:** Forward path accepted with a clear next-workflow reference and supporting evidence.

### Step 6 — Close the loop

Per `design-thinking-loop.md` LEARN → UNDERSTAND (or forward to shipping) gate:

- [ ] Metrics reviewed against PRD §6
- [ ] Learn-brief written and shared
- [ ] Artifacts updated or reviewed
- [ ] Forward path decided and logged
- [ ] Retro action items have owners

## Discipline checks

- [ ] "What we shipped" is separated from "what we learned" — they're not the same
- [ ] At least one learning is inconvenient (if none, probably confirmation bias)
- [ ] Guardrail metrics reviewed, not just north star
- [ ] Measurement gaps named explicitly, not hidden in footnotes
- [ ] Retro produced owned action items, not just sentiments

## Stop conditions

- Metrics can't be measured at all (instrumentation missing, data latency too long) → do not declare Learn complete. Surface the measurement debt as a blocker, fix it, then re-run.
- Team pressure to declare "Learn done, ship wider" without measurement → push back. "Shipping wider" based on vibes is how bad features scale.
- Retro devolves into blame → reset the retro with a blameless framing or postpone.

## Artifacts produced

- `<project-hub>/04_learn/YYYY-MM-DD-learn-brief.md`
- `<project-hub>/04_learn/YYYY-MM-DD-measurement-notes.md`
- `<project-hub>/04_learn/YYYY-MM-DD-retro.md`
- Updated artifacts (journey, persona, POV, PRD) with version bump
- Forward-path evidence in the existing learn brief; a separate typed record only when W5 requires one

## Next workflow

Depends on forward-path decision:

- **Iterate →** W3 with tightened scope
- **Ship wider →** continue rollout per PRD §10; next Learn cycle at next milestone
- **Pivot →** W2 (or W1 if research itself is invalidated)

Either way: the journey map and persona get updated. That's non-negotiable.

---

*Workflow grounded in `design-thinking-loop.md` LEARN phase. The compounding move is Step 4 (update artifacts). Teams that skip it re-learn the same lessons every quarter.*
