---
name: success-metrics
title: Define the observable signals of success
description: Define how success will be measured — quantitative signals that confirm the sprint's goal has been reached, not just that a prototype was tested. Use after Long-Term Goal and Sprint Questions are confirmed, before Design Criteria. Use when the Decider needs to communicate sprint outcomes to senior stakeholders, or when a sprint could end in a "we kind of validated it" ambiguity.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - After Long-Term Goal and Sprint Questions are confirmed, before Design Criteria
  - When the Decider needs to communicate sprint outcomes to senior stakeholders
  - Any time a sprint could end in a "we kind of validated it" ambiguity
  - When the business goal of the sprint needs to connect to a measurable outcome
applies-to: success definition, metric setting, business alignment, validate day criteria, forward decision anchoring
done_when:
  - Each metric is observable/measurable, not a vibe
  - Leading and lagging signals are distinguished
  - Metrics tie back to the long-term goal and sprint questions
metadata:
  duration: 20–30 min
  team-size: Full sprint team; Decider and business stakeholders lead
  sprint-phase: 2 Define
  redirect-host: rubric-authoring
---

# Success Metrics

**TL;DR:** Success Metrics answer the question the sprint will ultimately have to answer: how will the team know — concretely — that the sprint worked? Not "users reacted positively" but "the coordinator completed morning triage in under 10 minutes." Not "the concept seemed promising" but "≥4/5 participants correctly assigned an urgent request on the first attempt." Defining metrics before sketching prevents the team from discovering after Validate that there was no agreed standard against which to assess results.

## When to use

- After Long-Term Goal and Sprint Questions are confirmed, before Design Criteria
- When the Decider needs to communicate sprint outcomes to senior stakeholders
- Any time a sprint could end in a "we kind of validated it" ambiguity
- When the business goal of the sprint needs to connect to a measurable outcome

## Two types of metrics

| Type | What it measures | When evaluated |
|---|---|---|
| **Prototype test metrics** | Behaviour during the Five-Act Interview (task completion, correct interpretation, unprompted actions) | Validate day |
| **Business outcome metrics** | Long-term impact if the solution ships (time saved, error rate reduction, adoption rate) | Post-launch; not measurable in sprint but worth naming |

Prototype test metrics are what the sprint can directly measure. Business outcome metrics are the "if this works, it means..." aspiration that motivates the sprint.

## Format

```markdown
## Success Metrics — [Sprint Name] · [Date]

### Prototype test metrics (measured on Validate day)
| Metric | Target | How measured |
|---|---|---|
| [What users do or interpret correctly] | [Threshold: ≥N/5 participants] | [Which interview task, what behaviour observed] |

### Business outcome metrics (post-launch aspiration)
| Metric | Current baseline | Target | Timeframe |
|---|---|---|---|
| [Business-level outcome] | [What we measure today] | [Target state] | [Expected timeline] |
```

## Worked example (generic)

```markdown
## Success Metrics — Request Triage Sprint · 2026-02-24

### Prototype test metrics (Validate day)
| Metric | Target | How measured |
|---|---|---|
| Urgency score correctly interpreted | ≥4/5 participants explain the urgency score without prompting | T1: Ask "what does this number mean?" — observe unprompted response |
| System-switching eliminated | 0 participants open another system during T2 | Observe screen during the booking-check task |
| Suggested priority acted on | ≥3/5 participants prioritise based on the suggestion without additional checking | T3: Observe without prompting; note hesitation or additional action |
| Assignment completed in ≤2 interactions | ≥4/5 complete assignment in ≤2 taps | T4: Count taps; time the task |
| No increase in perceived cognitive load | 0 participants describe feeling "more overwhelmed" vs. today | Debrief Q: "How did this compare to your current tool?" |

### Business outcome metrics (post-launch aspiration)
| Metric | Baseline | Target | Timeframe |
|---|---|---|---|
| Morning triage time (Lead Coordinator) | ~40 min | < 10 min | 30 days post-launch |
| Wrong-assignment rate | ~15% (manual + system) | < 5% | 60 days post-launch |
| Other systems opened per request | 2–4 systems/request | 0 | Day 1 of launch |
| Urgent requests assigned within 2 hours | Not yet measured | 100% in peak season | 90 days post-launch |
| Resources allocated right first time | 92% | 98% | 90 days post-launch |
| Coordinator trust score (internal survey) | Not yet measured | ≥7/10 | 90 days post-launch |

### Sprint outcome decision thresholds
- 🟢 **Green (proceed to build):** ≥4 of 5 prototype metrics hit their target
- 🟡 **Yellow (iterate):** 3 of 5 hit target; 1–2 near-miss — iterate and re-test
- 🔴 **Red (reconsider):** ≤2 of 5 hit target; core concept may need rethinking
```

## The "so what" test

For each metric, ask: "If this metric is met, what decision does it unlock?"
- If meeting the metric clearly justifies a build decision → it's a good metric
- If meeting it would still leave the team uncertain → the metric doesn't capture what matters

## Metric quality checklist

- [ ] Specific — names an observable action or measurable quantity
- [ ] Threshold defined — not "users liked it" but "≥4/5 users completed the task"
- [ ] Linked to a Sprint Question — each Sprint Question should have at least one test metric
- [ ] Measurable in the sprint — not dependent on post-launch data
- [ ] Not leading — the metric measures user behaviour, not user satisfaction ratings (which are often falsely positive)

## Agent facilitation guide

When setting Success Metrics for a sprint:
1. Read the Sprint Questions — each question needs at least one prototype test metric
2. Read the Assumptions Board — critical assumptions need specific pass/fail success signals
3. For each metric: write the target threshold and the observation method
4. Define the sprint outcome thresholds: what combination of metric results = 🟢/🟡/🔴
5. Add business outcome metrics from the Decider's goals — these aren't tested in the sprint but provide context for the forward decision

## Watch-outs

- **Satisfaction surveys as metrics:** "90% of users say they'd use this" is not a reliable predictor of adoption. Behavioural metrics (what they did, not what they said) are more robust.
- **No threshold defined:** "Most users interpret it correctly" is not a metric. "≥4/5 participants interpret it correctly without prompting" is.
- **Metrics set after Validate:** Defining success after you've seen the results is confirmation bias. Set metrics before any user has touched the prototype.
- **Only measuring positives:** Include at least one "must not" metric: "Zero participants report feeling more confused after using this feature."

## Connects to

- [Sprint Questions](../sprint-questions/SKILL.md) — each Sprint Question maps to at least one metric
- [Design Criteria](../design-criteria/SKILL.md) — criteria and metrics are complementary; criteria describe the standard, metrics measure it
- [Assumptions Board](../assumptions-board/SKILL.md) — "success signal" field = the prototype test metric
- [Synthesis](../research-synthesis/SKILL.md) — metrics are the input to the forward decision
- [`00_README/_frameworks/traffic-light-decisions.md`](../../../00_README/_frameworks/traffic-light-decisions.md) — sprint outcome thresholds map to Traffic Light decisions
