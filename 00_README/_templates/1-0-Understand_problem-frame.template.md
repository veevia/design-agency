---
title: "Problem Frame — <engagement>"
type: template
template-for: problem-frame
status: canonical
owner: OS steward
last-updated: 2026-10-29
loop-phase: understand
source: Problem-framing practice + extreme-clarity.md + alignment-playbook.md + House principles §2 and §4
tags: [type/template, type/problem-frame, purpose/discover, loop/understand, status/canonical]
---

<!--
  PROBLEM FRAME
  The front link of the design loop — the pre-research artifact that grounds
  an engagement before any persona, JTBD, or solution work. It gates entry
  into research: if you can't fill the problem statement without a solution
  noun, you're not ready to research yet.

  Draft it after the initiative intake, with W1
  (`02_Workflows/workflows/W1-understand.md`) and the `problem-framing`
  skill (`03_Agents-and-Skills/Skills/problem-framing/SKILL.md`).

  Copy to: 01_Project-Hubs/<hub>/01_understand/problem-frame.md, then
  replace this file's front matter with the artifact's own:

    type: problem-frame
    project: <hub-slug>
    owner: <single name>
    status: draft
    light: green | yellow | red
    trigger: <what closes a yellow>      # yellow only
    expiry: <YYYY-MM-DD>                  # yellow only
    references-wiki: [<_wiki/sources/...>]
    informs: [<downstream artifact or scope decision>]
    tags: [type/problem-frame, project/<hub-slug>, status/draft, loop/understand]

  Remove this comment block before sharing.
-->

# &lt;engagement&gt; — Problem Frame

**TL;DR:** &lt;one-sentence people-problem + who has it&gt;.

## Problem statement

&lt;The problem in the user's language. NO solution noun — not "an agent", "a dashboard",
"an ontology", "a platform". Name the decision the user cannot make today.&gt;
[observed|reported|assumed | &lt;source-slug&gt;]

## Decisions to enable

The future system exists to let specific people make specific decisions. Design backward from these:

- &lt;decision the product must let a user make&gt; — made by &lt;role&gt;, &lt;cadence&gt;, with &lt;data&gt; today [tag | source]
- ...

## Feasibility gap (want vs achievable — the Venn center)

- **Want:** &lt;stakeholder ask&gt; [reported | &lt;source&gt;]
- **Achievable now:** &lt;constraint-bounded reality&gt; [observed | &lt;source&gt;]
- **Design target (the overlap):** &lt;where we play — the thing to build against&gt;

## Known / unknown data map

- **Known-known:** &lt;data we have and trust&gt;
- **Known-unknown:** &lt;data we know we lack&gt; [open | &lt;source&gt;]
- **Unknown-unknown (riskiest):** &lt;the assumption that, if wrong, breaks the concept&gt;

## Stakeholder alignment map

| Stakeholder | Wants | Conflicts with |
|---|---|---|
| &lt;name (role)&gt; | &lt;position&gt; | &lt;whom / what&gt; |

## Readiness to research

🟢🟡🔴 — &lt;one-line rationale&gt;
- **trigger:** &lt;what closes a yellow&gt; *(yellow only — required)*
- **expiry:** &lt;YYYY-MM-DD&gt; *(yellow only — required)*

> Evidence note: tag every claim `observed` / `reported` / `assumed`. Before any of this
> enters a customer deck, validate the load-bearing claims against primary sources
> (House principle §4: evidence > opinion).

---

## Quality check

- [ ] Problem statement contains no solution noun
- [ ] At least one decision to enable names a role, a cadence and today's data
- [ ] The design target sits inside "achievable now", not just "want"
- [ ] The riskiest unknown is named
- [ ] Every claim carries an evidence tag
- [ ] Exactly one readiness light; a 🟡 has trigger + expiry
