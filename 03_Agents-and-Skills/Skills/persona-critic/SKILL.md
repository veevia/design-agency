---
name: persona-critic
title: Critique a draft through a sourced decision-maker persona
description: "Build an evidence-tagged persona of a specific reviewer or decision-maker (a sponsor, an executive, a skeptical engineering lead) from public or explicitly shared material only, then run your own draft past that persona — loves, hates, rude questions, what they would do differently — to surface the hard questions before the real review does. Use when preparing a PRD, brief, POV or deck for a review with a known skeptical or senior reader, or when rehearsing a pre-mortem or rude Q&A before a pitch, design review or executive read."
status: draft
when_to_load:
  - Before sending a PRD, brief, POV or deck into a review with a known skeptical or senior reader
  - Pre-mortem or rude-Q&A rehearsal before a pitch, design review or executive read
  - You want a critique from a specific viewpoint your team may share and miss
inputs:
  - kind: persona-file
    where: "01_Project-Hubs/*/stakeholders/_personas/**/*.persona*.md"
    note: "an evidence-tagged persona; a persona of a real person is <slug>.persona_TENANT.md (git-ignored)"
  - kind: artifact-under-review
    where: "01_Project-Hubs/*/02_design/**/*.md"
    note: "the PRD, brief, POV or deck draft to harden (a draft in another phase folder or pasted text also works)"
outputs:
  - kind: critique-block
    schema: "Loves / Hates / Rude questions / If I were you — each point tied to a cited persona source — closing with a Traffic Light read on review-readiness"
done_when:
  - "The persona draws only on public or explicitly shared material, and every trait cites its source with an evidence tag — no invented traits"
  - "A persona of a real person lives in a git-ignored `*_TENANT.md` file (confirmed with `git check-ignore`) and is never force-added, committed or pasted into unapproved tools"
  - "The critique returns all four sections: Loves, Hates, Rude questions, If I were you"
  - "The output names the persona that spoke and stays in character — a viewpoint, not generic advice"
  - "The critique closes with a Traffic Light verdict on review-readiness; a Yellow names its trigger and expiry"
  - "Persona traits are tagged `reported` or `assumed`; a trait tagged `observed` quotes its source"
lints:
  - id: persona-without-sources
    severity: error
    where: "01_Project-Hubs/[!_]*/stakeholders/_personas/**/*.persona*.md"
    pattern: "(?i)^#\\s"
    must_also_match: "(?i)source|wisdom|interview|talk|podcast|authored|transcript"
    message: "A persona with no cited sources is a fabrication — list the public talks, interviews, published writing or explicitly shared documents it was built from, tagged."
  - id: persona-critic-fabricated-observed
    severity: error
    where: "01_Project-Hubs/[!_]*/stakeholders/_personas/**/*.persona*.md"
    pattern: "\\[observed\\]"
    forbid: "\\[observed\\][^|]*$"
    message: "An `observed` persona trait must cite the source quote: `[observed | <source-slug>]`. Inferred traits are `reported` or `assumed`."
  - id: persona-critic-missing-rude-q
    severity: warning
    where: "03_Agents-and-Skills/Skills/persona-critic/**/*.md"
    pattern: "(?i)loves|hates"
    must_also_match: "(?i)rude question|would you do differently|if i were you"
    message: "A persona critique that only flatters is useless — include the rude questions and the 'if I were you' section."
budget:
  context_tokens_max: 2200
loads: [evidence-tagging, traffic-light-decisions, problem-framing]
---

# Persona Critic

**TL;DR:** Before a review, build a sourced persona of the reader who will judge your draft, have the model critique the draft in that reader's voice — loves, hates, rude questions, what they would change — and close the gaps before the room finds them.

Adapted from a field demo: a team built a persona of a customer executive from the executive's public talks and
interviews, ran its own internal review past that persona, and walked into the pitch with the hard questions
already answered. The same move works internally — run a PRD past a skeptical security lead or your sponsor.

## When to use

- A PRD, brief, POV or deck is about to meet a known skeptical or senior reader.
- Pre-mortem or rude-Q&A rehearsal before a pitch, design review or executive read.
- Your team shares a viewpoint, and you want the one it is missing.

## What this is not

- **Not a UX research persona.** Those model the user you are building for (`type: persona` in `01_understand/`).
  This models the critic you are presenting to, pointed at your own artifact.
- **Not generic AI feedback.** The value is one specific viewpoint. If the critique reads like generic best
  practice, the persona is too thin — enrich its sources.
- **Not a profile of someone's private life.** Work positions and public statements only.

## Sourcing and confidentiality

- **Public or explicitly shared material only:** talks, interviews, podcasts and published writing; documents the
  person — or your team, with the right to share them — gave you for this work; meetings you attended. Never mine
  private messages, inboxes or chat history through a connector to profile someone.
- **Every trait cites a source** in `evidence-tagging` form: `[reported | <source-slug>]`, `[assumed]` plus the
  cheapest test, and `[observed | <source-slug>]` only with a quote.
- **A persona of a real person is confidential.** Name it
  `01_Project-Hubs/<hub>/stakeholders/_personas/<slug>.persona_TENANT.md`; the root `.gitignore` ignores
  `*_TENANT.md` ([CONVENTIONS §4](../../../00_README/CONVENTIONS.md#4-customer-data-labels)). Confirm with
  `git check-ignore -v <path>` before writing, never `git add -f` it, keep it only as long as the engagement needs
  it, and don't paste it into tools, models or plug-ins the person's organization hasn't approved.
- **Archetypes** that describe no real person ("a skeptical security lead") may be committed as
  `<slug>.persona.md`; they still cite the public material they generalize from.

## Steps

1. **Build the persona file.** Gather what the person has actually said in public or shared with you (transcribe
   a public talk locally if no transcript exists). Distil it into the persona file: mission, what they care
   about, hot buttons, known objections, how they decide. Cite every source and tag every trait — an unsourced
   persona is a fabrication, and the `persona-without-sources` lint blocks it.
2. **Frame the artifact** with `problem-framing`: state the problem the artifact claims to solve, so the critic
   judges it against the right job.
3. **Run the critique in character.** A prompt that works:

   ```text
   Take the persona of <name> (<role>), using only the attached persona file. Review <artifact>. Tell me what
   you love, what you hate, the rude questions you would ask, and — if you were in our seat — what you would do
   differently. Cite the persona source behind each point.
   ```

   Return four sections: **Loves** (what they would champion, tied to their record) · **Hates** (what they would
   reject or distrust) · **Rude questions** (the uncomfortable asks — "where's the cost story?", "who owns the
   risk?") · **If I were you** (what they would change before backing it).
4. **Close with a Traffic Light read** on review-readiness: 🟢 ready · 🟡 conditional — name the trigger and the
   expiry you will fix first · 🔴 not ready — name the blocker. A Yellow without trigger and expiry is invalid
   (`traffic-light-decisions`).
5. **Fix, then reuse.** Change the draft or rehearse answers to the rude questions. Keep a small set of personas
   for recurring reviewers and run any draft past any of them.

## Output format

```markdown
## Persona critique — <artifact> as read by <persona name> (<role>)

**Loves**
- <point> — because <what they said or did> [reported | <source-slug>]

**Hates**
- <point> [reported | <source-slug>]

**Rude questions** (rehearse answers before the room asks)
- <question>

**If I were you**
- <change they would demand before backing it>

**Review-readiness:** 🟡 conditional — fix <X>. trigger: <event>; expiry: <date>.
```

Persona file shape:

```markdown
---
title: <Name> — critic persona
persona-of: <name>, <role>, <organization>   # a real person → this file is *_TENANT.md
kind: real-person                            # real-person | archetype
tenant: customer                             # customer | internal | personal
sources:
  - <source-slug>: <talk | interview | published article | shared memo>, <date>, <URL or hub path>
updated: YYYY-MM-DD
---

# <Name> — critic persona

- Mission: <what they are trying to achieve> [reported | <source-slug>]
- Cares about: <priority> [reported | <source-slug>]
- Hot button: <trigger> [observed | <source-slug>: "<quote>"]
- Likely objection: <objection> [assumed] — test: <ask in the pre-read>
```

## Watch-outs

- **Garbage persona, confident wrong critique.** The model will happily role-play someone it knows nothing real
  about. A thin source list makes the critique theater; enrich the sources first.
- **It de-risks; it doesn't replace the person.** A 🟢 persona verdict is not the stakeholder's sign-off. Never
  record it as their agreement or dissent — record only real consultation ([AGENTS.md](../../../AGENTS.md)).
- **One voice per pass.** A critique that blends three viewpoints is mush. One persona per pass; name it.
- **Personal data.** A persona of a real person is personal data: public or shared sources only, a git-ignored
  `_TENANT.md` file, no private-message mining, no unapproved tools.
- **Don't skip the rude questions.** A flattering critique is a comfort blanket; the loves-only version is the
  failure mode the `persona-critic-missing-rude-q` lint exists for.

## See also

- `evidence-tagging` · `traffic-light-decisions` · `problem-framing` — the skills this loads
- `alignment-playbook` — records real stakeholder positions; a persona critique is rehearsal, never a position
- The design-sprint method library's critique rituals — a persona pass slots in before a speed critique
- Hub stakeholder profiles: [`stakeholders/README.md`](../../../01_Project-Hubs/_template-project/stakeholders/README.md)
