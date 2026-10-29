---
title: Extreme Clarity
type: framework
status: draft
owner: OS steward
last-updated: 2026-10-29
source: House Extreme Clarity practice
tags: [type/framework, purpose/align, status/draft, loop/all]
---

# Extreme Clarity

> **TL;DR:** Before you hit send, make four things un-fuzzy — the takeaway, the ask + deadline, the evidence, and what could make you wrong.

How to communicate so a busy stakeholder can act on what you said — without a follow-up. Used when drafting charters, design briefs, weekly status, and any customer-facing message. The [`extreme-clarity`](../../03_Agents-and-Skills/Skills/extreme-clarity/SKILL.md) skill operationalizes it.

> **Status:** Draft. Extend it with your team's before/after examples as you use it.

## 1. The Extreme Clarity test

Before sending any material communication, answer:

1. **TL;DR (Too Long; Didn't Read):** what's the single takeaway if they only read one sentence?
2. **Action expected:** what do I need them to do, by when?
3. **Evidence basis:** what am I claiming, and what is it based on?
4. **What could make me wrong:** named explicitly.

If any of the four are fuzzy, the message isn't ready.

## 2. Clarity moves

| Move | Before | After |
|---|---|---|
| **TL;DR** | "Following up on our discussion about the agent architecture options..." | "We should pick Option B. Approval needed by Friday. Here's why." |
| **Name the ask** | "Let me know what you think." | "Confirm Option B by Friday, or propose a blocker." |
| **Show the delta** | "We made progress this week." | "POC latency: 2.4s → 0.9s. Target 1.0s. On track." |
| **Explicit uncertainty** | "I believe this will work." | "Works for 8 of 10 test cases. Failure mode: long inputs. Mitigation: chunking (untested)." |
| **One-sentence summary** | 6-paragraph email | 1-line headline, 3 bullets, details in a link. |

## 3. Structural defaults

- **Headlines are sentences, not labels.** "Status: Green" → "On track for MVP checkpoint; no blockers."
- **Numbers, not adjectives.** "Fast" → "0.9s p95."
- **Deltas, not totals.** "50 tickets" → "+12 new, 8 closed, 54 open."
- **Opinions named as opinions.** "Appears that..." → "I think..."

## 4. The clarity pyramid

```
                    TL;DR (1 sentence)
               ┌─────────────────────────┐
               │   Action + Deadline     │
               │   Top 3 facts           │
          ┌────┴─────────────────────────┴────┐
          │    Evidence + What could break   │
     ┌────┴──────────────────────────────────┴────┐
     │      Full context, numbers, caveats        │
     └─────────────────────────────────────────────┘
```

Most readers stop at the top. Write so the top is self-sufficient.

## 5. Where Extreme Clarity gets used

| Artifact | Clarity discipline |
|---|---|
| `weekly-status` (opt-in) | TL;DR in the first line; status color + one-sentence reason |
| `problem-frame` | One-sentence problem, one-sentence hypothesis, one-sentence proposed next step |
| `design-brief` | Three measurable outcomes; if you can't name them, the design brief isn't ready |
| Decision record (ADR / PDR / ops note / release) | Decision in one sentence; reasoning in ≤3 bullets |
| Every customer-facing message | Passes the Extreme Clarity test (§1) before sending |

## 6. Common failure modes

- **Status as narrative.** "This week we started looking at..." — no action, no decision, no delta.
- **Hedge language.** "We might potentially want to consider..." — means nothing.
- **Everything is green.** Green without reason is not a status; it's a feeling.
- **The meeting is the message.** If the decision only exists in a meeting, it didn't happen. Write it down.

