---
name: fishbone-diagram
title: Map cause-and-effect to find a problem's roots
description: Map all contributing causes of a problem on a single diagram — visualise the full cause structure before deciding which root cause to address. Use when a problem has multiple suspected causes and the team can't agree on which is primary, after Five Whys chains have been run on multiple branches, or when a problem has persisted despite multiple previous fix attempts (suggests multiple causes).
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - When a problem has multiple suspected causes and the team can't agree on which is primary
  - After Five Whys chains have been run on multiple branches — the Fishbone organises them visually
  - When a problem has persisted despite multiple previous fix attempts (suggests multiple causes)
  - Before Sprint Question selection — to see the full cause map before picking a focus
applies-to: root cause mapping, complex problem analysis, multi-cause identification, team alignment on cause vs. symptom
done_when:
  - The problem statement sits at the head; causes branch by category
  - Each major bone has its contributing sub-causes
  - The most likely root causes are marked for testing
metadata:
  duration: 20–30 min
  team-size: Full sprint team
  sprint-phase: 1 Understand
---

# Fishbone Diagram

**TL;DR:** A Fishbone Diagram (also called a Cause-and-Effect diagram) maps all the contributing causes of a problem on a single visual. Where the Five Whys explores one causal chain in depth, the Fishbone shows the full landscape of causes at once — useful when a problem has multiple independent contributing factors and the team needs to see them all before deciding which to target.

## When to use

- When a problem has multiple suspected causes and the team can't agree on which is primary
- After Five Whys chains have been run on multiple branches — the Fishbone organises them visually
- When a problem has persisted despite multiple previous fix attempts (suggests multiple causes)
- Before Sprint Question selection — to see the full cause map before picking a focus

## The diagram structure

```
                                                    ┌─────────────┐
                                                    │   PROBLEM   │
    CAUSE CATEGORY A      CAUSE CATEGORY B          │  (Effect)   │
         │                       │                  └──────┬──────┘
    ─────┼───────────────────────┼──────────────────────── │ ──────→
         │                       │                         │
    Cause 1a  Cause 1b      Cause 2a  Cause 2b
    
    CAUSE CATEGORY C      CAUSE CATEGORY D
```

The "spine" (horizontal arrow) points to the problem. "Bones" (diagonal lines) are cause categories. Each category branches into specific causes.

## Standard cause categories

The original fishbone used 6Ms (for manufacturing). For product/UX sprints, use adapted categories:

| Category | What it captures |
|---|---|
| **People** | User behaviour, skills, attitudes, mental models |
| **Process** | Workflow steps, procedures, handoffs, sequencing |
| **Tools / Technology** | Software limitations, integrations, API constraints |
| **Data / Content** | Data quality, availability, format, latency |
| **Environment** | Physical context, time pressure, organisational culture |
| **Policy / Governance** | Rules, compliance requirements, approval chains |

Not all categories will be relevant for every problem. Use the ones that surface causes.

## Steps

1. **Write the problem on the right (2 min):** The effect — the symptom you're analysing. Be specific: "Coordinators spend 40+ min on the morning triage of overnight requests" not "slow workflow."

2. **Draw the spine and label categories (3 min):** Draw the horizontal arrow pointing to the problem box. Add 4–6 diagonal bones for the cause categories.

3. **Brainstorm causes per category (15 min, parallel):** Team silently writes cause stickies, then places them on the relevant bone. Each cause goes on a single sticky — one idea per note.

4. **Read back and cluster (5 min):** Facilitator reads back causes per category. Team discusses: are causes in the right category? Any duplicates?

5. **Identify the primary causes (5 min):** Vote (dot stickers) on the 2–3 causes that seem most influential. These are candidates for Sprint Questions.

## Worked example (generic)

```markdown
## Fishbone — Problem: Coordinators spend 40+ min every morning on manual request triage

### People
- Mental model: coordinators don't trust the suggested priority to be accurate enough to act on
- Habit: "I always check every system myself — it's been my routine for 3 years"
- Skill gap: new coordinators take 2× longer than seniors; no tool assistance

### Process
- No defined triage workflow — each coordinator has their own approach
- Checking is manual: open 3–4 systems per request
- Assignment requires a 7-step form; phoning the site is faster

### Tools / Technology
- Booking inbox shows the customer's free-text description only — no urgency indicator
- AI ranking exists in backend but is not surfaced in the UI
- Assignment form has no auto-suggest or pre-fill

### Data / Content
- Service-contract and inventory data not exposed through the booking inbox API
- Past work-order outcomes (was this request really urgent? which parts were used?) not queryable
- Customer IDs disagree across 3 of 6 systems — no single request record
- Suggested-priority accuracy varies by request type (higher for outages, lower for safety risks)

### Environment
- Morning triage happens under time pressure (specialists start at 8am)
- Desk-bound workflow — no mobile access for early review
- Request volume on the first morning of peak season overwhelms the process

### Policy / Governance
- All priority decisions must be logged with coordinator identity (legal requirement)
- AI-only priorities not permitted without human review
- New integrations require IT approval (6-week process)

### Primary causes (voted)
1. AI ranking not surfaced in UI (Tools) — most impactful, addressable in sprint
2. Service-contract and inventory data not exposed in the inbox (Data) — directly removes system-switching
3. Manual assignment form UX (Process) — one-tap assign addresses this
```

## Fishbone vs. Five Whys

| | Fishbone | Five Whys |
|---|---|---|
| **Structure** | Wide — all causes mapped simultaneously | Deep — one causal chain explored in detail |
| **Best for** | Complex problems with multiple causes | Problems where root cause is unclear or disputed |
| **Output** | Visual cause map; identifies primary cause clusters | Root cause statement; generates HMW directly |
| **Team size** | Full team | Small group (2–3) |
| **Use together** | Yes — Fishbone to map, Five Whys to drill into the primary cause |

## Agent facilitation guide

When constructing a Fishbone diagram from sprint research:
1. State the problem (effect) clearly
2. For each cause category: extract relevant causes from research notes (interviews, Lightning Talks, Research Review)
3. Tag each cause: `observed` / `reported` / `assumed`
4. Identify which causes are: addressable in this sprint / constraint (can't change) / upstream (would require separate initiative)
5. Recommend the top 2–3 causes to target as Sprint Questions
6. Flag any cause tagged `assumed` that the prototype should validate

## Watch-outs

- **Confusing causes with solutions:** "We need an urgency score" is a solution, not a cause. If this surfaces on a bone, reframe: "No urgency indicator in the inbox" is the cause; the urgency score is a potential solution.
- **All causes in one category:** If every sticky lands on "Tools," the team may be anchored on technical solutions. Push for causes in People and Process categories too.
- **Not using it to narrow scope:** A fishbone with 30 causes isn't a decision — it's a wall of complexity. The voting step at the end must produce a manageable focus.

## Connects to

- [Five Whys](../five-whys/SKILL.md) — drill into the primary Fishbone cause with a Five Whys chain
- [Expert Interviews](../expert-interviews/SKILL.md) — interview questions target the most contentious cause branches
- [Stakeholder Map](../stakeholder-map/SKILL.md) — Policy / Governance causes often trace back to outer-ring stakeholders
- [Assumption Mapping](../assumption-mapping/SKILL.md) — `assumed` causes become assumptions on the map
