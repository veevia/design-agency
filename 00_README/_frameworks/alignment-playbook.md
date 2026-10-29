---
title: Alignment Playbook
type: framework
status: draft
owner: OS steward
last-updated: 2026-10-29
source: House alignment cheat sheet + Design POV practice
tags: [type/framework, purpose/align, status/draft, loop/all]
---

# Alignment Playbook

> **TL;DR:** Alignment isn't consensus — it's everyone knowing what we decided, why, and which disagreement was heard and set aside; this playbook is the moves to get there fast.

Moves to get a cross-functional group aligned on a decision — fast. Used during framing, kickoff, mid-engagement re-scopes, and any stuck moment. The [`alignment-playbook`](../../03_Agents-and-Skills/Skills/alignment-playbook/SKILL.md) skill operationalizes it.

Alignment ≠ consensus. Alignment means everyone knows **what we decided**, **why**, and **what disagreement was heard and set aside**.

> **Status:** Draft. Extend it with your team's worked examples as you use it.

## 1. The alignment loop

```
  Surface ──► State ──► Disagree ──► Decide ──► Document
     │                                              │
     └──────────────(on drift)──────────────────────┘
```

1. **Surface** — what is unspoken? Start by naming what hasn't been said.
2. **State** — articulate the position in one sentence. Avoid "we should explore..."
3. **Disagree** — invite the strongest counter-position. Require it if it isn't offered.
4. **Decide** — pick. Record the decision owner.
5. **Document** — keep the rationale with the work it governs. A new durable choice becomes a typed decision record through [W5](../../02_Workflows/workflows/W5-decide.md), closed with one [Traffic Light](traffic-light-decisions.md).
6. **Drift check** — if the decision is being re-litigated within 2 weeks, loop back to Surface.

## 2. Alignment moves

| Move | When to use | What to say |
|---|---|---|
| **Name the elephant** | Something unsaid is blocking progress | "It feels like we're avoiding X. Can we say it?" |
| **Force the POV** | Group keeps pitching options, no position | "If you had to pick one, which and why?" |
| **Strongman the other side** | Disagreement is shallow | "Can someone make the best case *against* our position?" |
| **Split the decision** | Group is stuck on coupled issues | "What if we decide A now and defer B?" |
| **Escalate deliberately** | Level of decision exceeds the room | "This belongs to <role>. Let's package it and hand over." |
| **Name the cost of delay** | Bias toward deferring | "What does another week of ambiguity cost us?" |
| **Time-box the debate** | Discussion is looping | "15 more minutes, then we decide or defer to <date>." |

## 3. Alignment anti-patterns

- **Silent assent.** "No objections" is not alignment. Ask each person to say it back.
- **Decision-by-chat.** A material decision that lives only in a chat thread didn't happen. Write it down where the work lives.
- **Consensus theater.** The loudest voice was agreed with, not aligned with.
- **Zombie disagreement.** A disagreement that surfaces every meeting but never gets decided. Escalate or document it as a live risk.
- **Invented dissent.** Filling a "disagreement" field with objections nobody raised. Solo work is recorded honestly as solo.

## 4. Alignment artifact: the decision record

Reuse existing rationale first — a meeting note, PRD section or evidence brief often already holds it. When a new durable choice needs its own record, [W5](../../02_Workflows/workflows/W5-decide.md) picks the smallest type (ADR, PDR, ops note or release). Every record carries:

- **Decision** — one sentence, active voice
- **Owner** — a single name
- **Traffic Light** — 🟢 / 🟡 / 🔴 for ADRs and PDRs (see [`traffic-light-decisions.md`](traffic-light-decisions.md))
- **Options considered** — at least two real ones
- **Consultation** — `solo`, `invited` or `reviewed`, with the dissent that was actually heard
- **Reversal or review trigger** — what would make us reopen it

## 5. Cadence integration

- **During framing:** capture material scope choices in the design brief; promote a choice to a typed record only when later work must follow it
- **At kickoff:** the intake's kickoff message names how decisions are made and who owns them
- **Weekly (if the hub reports weekly):** status links any new or changed decision records and every open Yellow
- **Monthly/quarterly checkpoints:** review open, expiring or drifting decisions
