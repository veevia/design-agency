---
title: "Initiative Intake — <project name>"
type: template
template-for: intake
status: canonical
owner: OS steward
last-updated: 2026-10-29
loop-phase: understand
source: kickoff-brief + stakeholder-profile + stakeholder-input + alignment-playbook.md + extreme-clarity.md + UX discovery practice
tags: [type/template, type/intake, purpose/discover, purpose/align, loop/understand, status/canonical]
---

<!--
  INITIATIVE INTAKE — the single document that precedes everything else.

  Combines what was 3 separate templates (kickoff-brief, stakeholder
  profile, stakeholder input) into one guided discovery document.

  PURPOSE: Augment your ability to:
    1. Ask the right questions before committing to a direction
    2. Map the people, politics, and priorities in the room
    3. Plan workshop activities that surface real constraints
    4. Lead the initiative conversation from day one

  WHEN TO USE:
    - Day one of any new initiative, feature, or engagement
    - When scope changes materially (rerun sections B–D)
    - When a new senior stakeholder enters (add to section C)

  HOW IT WORKS:
    Section A = YOU fill before the first meeting (5 min)
    Section B = YOU fill during/after the first conversation (30 min)
    Section C = YOU fill per stakeholder as you map them (10 min each)
    Section D = THEY fill async — the questions you send to busy XFNs (20 min)
    Section E = YOU synthesize into a workshop plan (15 min)
    Section F = YOU send as the kickoff to the full team (5 min)

  Total time to a complete intake: ~2 hours across 3–5 days.

  Copy to: 01_Project-Hubs/<hub>/intake.md (the hub root). Its relative
  links are written to resolve from both 00_README/_templates/ and the hub root.

  Remove this comment block before using on a real project.
-->

# Initiative Intake — &lt;project name&gt;

> **TL;DR:** &lt;One sentence — the problem we're solving, for whom, and why now.&gt;

---

## A. Pre-conversation prep *(you fill, 5 min)*

Fill this before your first meeting with the requester. Forces you to name what you know and what you don't — so the conversation fills gaps, not rehearses knowns.

### A1. What I know so far

| Field | Value |
|---|---|
| Requester | &lt;name, role&gt; |
| How this came to me | &lt;email / chat / meeting / escalation&gt; |
| Their words (verbatim) | &lt;paste the exact ask, not your interpretation&gt; |
| Urgency signal | &lt;why now? deadline, exec pressure, user complaint, market move?&gt; |
| My first read | &lt;your hypothesis — will be tested, not defended&gt; |

### A2. What I don't know yet

Write 3–5 questions you need answered before you can frame the problem. These become your conversation guide.

1. &lt;e.g., "Who are the actual users — not the buyers?"&gt;
2. &lt;e.g., "What have they already tried?"&gt;
3. &lt;e.g., "What does success look like in their terms, not ours?"&gt;
4. &lt;...&gt;
5. &lt;...&gt;

---

## B. Initiative framing *(you fill during/after first conversation, 30 min)*

This is the business context. Get this right and the Understand phase runs downhill. Get it wrong and you'll research the wrong problem.

### B1. The problem — in one sentence

&lt;Not a solution. Not a feature. The problem. e.g., "Ops managers lose 40% of their day to sync interrupts they could handle async."&gt;

If you can't write this sentence, you're not ready to proceed. Go back to the requester.

### B2. Why now — the forcing function

| Factor | Detail |
|---|---|
| What changed | &lt;market shift, competitor move, regulation, internal reorg, user revolt?&gt; |
| What happens if we wait | &lt;cost of delay — be specific&gt; |
| Who is pushing | &lt;name + their motivation&gt; |

### B3. Who it's for

| Role | Who | Notes |
|---|---|---|
| Primary user | &lt;the person whose job changes if this works&gt; | |
| Secondary user | &lt;affected but not the focal point&gt; | |
| Buyer / sponsor | &lt;if different from user — often is&gt; | |
| Anti-persona | &lt;who we are NOT optimizing for — state explicitly&gt; | |

### B4. What "good" looks like

Write in the requester's words first, then translate to measurable outcomes.

**Their words:** &lt;paste verbatim&gt;

**Translated to measurable outcomes:**

| Outcome | Metric | Baseline (if known) | Target | Window |
|---|---|---|---|---|
| &lt;what should change&gt; | &lt;signal&gt; | &lt;now&gt; | &lt;goal&gt; | &lt;duration&gt; |
| &lt;guardrail — must not degrade&gt; | &lt;signal&gt; | &lt;now&gt; | &lt;threshold&gt; | |

If the requester can't name a metric, that's a finding — write: *"No metric defined; intake flagged this as a risk."*

### B5. What's been tried

| Prior attempt | What happened | Why it failed or stalled |
|---|---|---|
| &lt;...&gt; | &lt;...&gt; | &lt;...&gt; |

Empty table = either nothing was tried (rare) or no one remembers (common — probe harder).

### B6. Scope boundaries

**In scope:**

- &lt;...&gt;

**Explicitly out of scope (protect this list):**

- &lt;item — with one-line reason&gt;
- &lt;item — with one-line reason&gt;

**Ambiguous (needs a decision before Understand starts):**

- &lt;item — who can decide?&gt;

### B7. Known constraints

| Type | Constraint | Source |
|---|---|---|
| Time | &lt;e.g., "Must ship by Q3 for OKR"&gt; | &lt;who said this&gt; |
| Budget / resourcing | &lt;e.g., "2 designers, 4 engineers for 2 sprints"&gt; | |
| Technical | &lt;e.g., "Must use existing auth — no new SSO"&gt; | |
| Policy / compliance | &lt;e.g., "GDPR Art. 22 applies"&gt; | |
| Brand / design system | &lt;e.g., "Follows DS v4"&gt; | |
| Political | &lt;e.g., "VP of Sales already promised feature X to a customer"&gt; | |

### B8. Open risks (your read, day one)

| # | Risk | Impact if ignored | Who can resolve |
|---|---|---|---|
| 1 | &lt;...&gt; | &lt;...&gt; | &lt;name&gt; |
| 2 | &lt;...&gt; | &lt;...&gt; | |
| 3 | &lt;...&gt; | &lt;...&gt; | |

---

## C. Stakeholder map *(you fill, 10 min per person)*

One row per function that has a voice in this initiative. Not everyone who's "interested" — only people whose sign-off, expertise, or resistance shapes the outcome.

### C1. The map

| # | Name | Function | What they care about (in their words) | What they own on this project | Best channel | Timezone | RACI |
|---|---|---|---|---|---|---|---|
| 1 | &lt;name&gt; | &lt;PM / Eng / Legal / …&gt; | &lt;their KPI, not yours&gt; | &lt;e.g., "PRD sign-off"&gt; | &lt;chat DM / email / …&gt; | &lt;tz&gt; | R / A / C / I |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |

### C2. Power and influence reads

Be honest. This section is for your eyes — it doesn't go in the kickoff.

| Name | Influence level | Likely stance | What moves them | Risk if unmanaged |
|---|---|---|---|---|
| &lt;name&gt; | high / medium / low | champion / neutral / skeptic / blocker | &lt;what they need to see to support&gt; | &lt;what happens if they disengage or resist&gt; |

### C3. Missing voices

Who should be at the table but isn't? Name them now, or they'll surface as a surprise in Build.

- &lt;name / role — why they matter&gt;
- &lt;...&gt;

---

## D. Stakeholder input form *(they fill async, 20 min)*

Send this to each XFN who can't sit for a live conversation. Copy the section below into a doc they can edit, or send as a file link. Set a deadline.

> **👥 For &lt;name&gt;**
>
> Thanks for taking 20 minutes. This replaces a 45-minute interview — same value, on your schedule. Your answers go into our research synthesis with attribution. You'll see the draft before it goes wider.
>
> **Done by:** &lt;deadline&gt;. If that won't work, ping me and we'll shift.

### D1. About you

| Field | Value |
|---|---|
| Name | &lt;your name&gt; |
| Role / function | |
| How this initiative touches your work | &lt;1 sentence&gt; |

### D2. The problem — in your words

**What problem are we solving?** *(Don't match our framing — your version matters.)*

&lt;...&gt;

**Who are the users, and what are they actually trying to do?** *(List jobs, not features.)*

&lt;...&gt;

**What's your evidence?** Tag each point:

- **Observed** — I've watched users do this, or they told me directly
- **Reported** — someone else told me, or I read it somewhere
- **Assumed** — I'm inferring from experience

### D3. What works and what breaks

**What works well today?** *(Things we must not break.)*

&lt;...&gt;

**Where does the current experience fall apart?** *(Specific moments — not general "it's bad.")*

&lt;...&gt;

**What workarounds have you seen?** *(Workarounds are signal — they show where the product fails.)*

&lt;...&gt;

### D4. Your constraints

**Hard constraints — things we cannot violate:**

&lt;...&gt;

**Things we should respect but could negotiate:**

&lt;...&gt;

**Things you're not sure about — where you'd want us to check with you:**

&lt;...&gt;

### D5. Success and risk — in your terms

**How will you know this project succeeded?** *(Your KPI, not ours.)*

&lt;...&gt;

**What would a disaster look like, for your function?**

&lt;...&gt;

**What's your biggest worry right now?**

&lt;...&gt;

### D6. Who else should we talk to?

&lt;Names + why. Inside or outside the org.&gt;

### D7. Anything we didn't ask that we should have?

&lt;...&gt;

---

## E. Workshop and research planning *(you fill, 15 min)*

Now that you have sections A–D filled, synthesize into an action plan. This bridges intake into the Understand phase ([W1](../../02_Workflows/workflows/W1-understand.md)); the [problem frame](../../00_README/_templates/1-0-Understand_problem-frame.template.md) is the next artifact.

### E1. Key themes from intake

Scan your notes from B + C + D. Name the 3–5 themes that keep recurring. These become your research questions.

| # | Theme | Sources (who said it) | Evidence tag | Implication for research |
|---|---|---|---|---|
| 1 | &lt;e.g., "Users don't trust the async channel"&gt; | &lt;C2, D3 from PM, D5 from Eng&gt; | observed / reported / assumed | &lt;e.g., "Interview users about trust signals"&gt; |
| 2 | | | | |
| 3 | | | | |

### E2. Assumption register

Every claim from intake that lacks direct user evidence goes here. These are hypotheses, not facts.

| # | Assumption | Who holds it | How to validate | Priority |
|---|---|---|---|---|
| 1 | &lt;e.g., "Users prefer async to sync"&gt; | &lt;PM&gt; | &lt;user interviews, Q3&gt; | must-validate / nice-to-validate |
| 2 | | | | |

### E3. Research questions (≤5, feeds W1 Step 1)

Derived from E1 themes and E2 assumptions. These directly seed the Understand workflow.

1. &lt;...&gt;
2. &lt;...&gt;
3. &lt;...&gt;

### E4. Workshop plan *(if a kickoff or alignment workshop is needed)*

Use when the stakeholder map (C2) shows misalignment, or when the problem framing (B1) varies across stakeholders.

| Activity | Purpose | Duration | Participants | Outputs |
|---|---|---|---|---|
| **Problem framing** | Align on what we're solving — surface competing framings | 30 min | All RACI-R and RACI-A | Single problem sentence (B1) agreed |
| **User empathy share-out** | Share what's known about users — flag gaps | 20 min | Design + PM + anyone with field exposure | Gap list for research |
| **Constraint harvest** | Each function states their hard constraints aloud | 20 min | All | Constraint table (B7) validated |
| **Success definition** | "How will you know this worked?" — per function | 20 min | All | Outcome table (B4) with per-function metrics |
| **Disagreement round** | "What's the strongest case against this initiative?" | 15 min | All | Named disagreements for intake record |
| **Prioritize research** | Dot-vote on which unknowns matter most | 10 min | All | Ranked research questions (E3) |
| **HMW generation** | Reframe top themes as "How might we…?" questions | 10 min | All | HMW candidates for research to validate |

**Total workshop time: ~2.5 hours** (or split into 2 × 75-min sessions).

### E5. HMW statements

Reframe the top intake themes (E1) as "How Might We" questions. These are the team's first cut at the design challenges — research will filter them.

> **HMW funnel:** Generate many → validate with evidence → prioritize through the journey → commit 1–3 in the POV.

- **How might we** &lt;reframe theme as a design challenge&gt; **so that** &lt;user outcome&gt;?
- **How might we** &lt;...&gt; **in a way that** &lt;...&gt;?
- &lt;...&gt;

### E6. Alignment moves to prepare

From [`alignment-playbook.md`](../../00_README/_frameworks/alignment-playbook.md) — pick the moves you expect to need:

- [ ] **Name the elephant** — something unsaid is blocking: &lt;what?&gt;
- [ ] **Force the POV** — group pitches options but takes no position: &lt;on what topic?&gt;
- [ ] **Strongman the other side** — disagreement feels shallow: &lt;which stakeholder?&gt;
- [ ] **Split the decision** — group is stuck on coupled issues: &lt;which pair?&gt;
- [ ] **Name the cost of delay** — bias toward deferring: &lt;what's the delay cost?&gt;
- [ ] **Time-box the debate** — topic tends to loop: &lt;which topic?&gt;

---

## F. Kickoff message *(send to the full team, 5 min)*

Once A–E are complete, this is what goes out to every XFN. Paste into chat or email. Keep it to one screen.

---

### Kickoff — &lt;project name&gt;

> Welcome to &lt;project&gt;. This one-pager tells you why we're doing this, how we'll work, and what I'll ask of you. Read time: 3 minutes.

**Why this project exists:** &lt;Copy B1 — one sentence.&gt;

**What "good" looks like:** &lt;Copy B4 outcomes — 2–3 bullets.&gt;

**How we'll work:** Understand → Design → Build → Learn. Material decisions close with one Traffic Light (🟢 decided / 🟡 conditional / 🔴 blocked) and one owner. Status: &lt;cadence and channel — or "no standing status; ask any time"&gt;.

Full context: [`HOW-WE-WORK.md`](../../00_README/HOW-WE-WORK.md) · Jargon: [`GLOSSARY.md`](../../00_README/GLOSSARY.md)

**Who's on the crew:**

| Function | Person | What they own |
|---|---|---|
| &lt;function&gt; | &lt;name&gt; | &lt;scope — from C1&gt; |

**What I'll ask of you, by phase:**

| Phase | Your role | Time |
|---|---|---|
| Understand (weeks &lt;N&gt;) | &lt;...&gt; | &lt;hrs&gt; |
| Design (weeks &lt;N&gt;) | &lt;...&gt; | &lt;hrs&gt; |
| Build (weeks &lt;N&gt;) | &lt;...&gt; | &lt;hrs&gt; |
| Learn (weeks &lt;N&gt;) | &lt;...&gt; | &lt;hrs&gt; |

**What we're not doing:** &lt;Copy B6 out-of-scope — 2–3 bullets.&gt;

**First 2 weeks:**

| Week | What happens |
|---|---|
| W1 | &lt;...&gt; |
| W2 | &lt;...&gt; |

**One thing I need from you this week:** &lt;One specific, named ask per key XFN.&gt;

**How to reach me:** &lt;channel + frequency&gt;

—&lt;your name&gt;

---

## Quality check

- [ ] B1 problem sentence is one sentence, no solution language
- [ ] B4 has at least one measurable outcome and one guardrail
- [ ] B5 prior attempts are filled (or explicitly "none found")
- [ ] B6 out-of-scope list is non-empty
- [ ] C1 has at least 3 stakeholders mapped with RACI
- [ ] C2 power reads are honest (skeptics and blockers named)
- [ ] C3 missing voices are named
- [ ] D sent to at least 2 XFNs who couldn't sit for a live conversation
- [ ] E1 themes synthesized from B + C + D (not just B)
- [ ] E2 assumptions tagged — none left unlabeled
- [ ] E3 research questions are ≤5 and derived from themes + assumptions
- [ ] F kickoff message fits on one screen

---

*This template combines what was previously three separate documents (kickoff-brief, stakeholder profile, stakeholder input) into a single guided discovery flow. Sections A–E augment your ability to ask the right questions and plan workshop activities. Section F is the output your team sees. The rest is your operating intelligence.*
