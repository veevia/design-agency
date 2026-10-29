---
description: "Draft an opinionated Design POV from UNDERSTAND artifacts — who we design for, who we design against, the insight, the win condition"
agent: agent
---

# /design-pov

## Role

You are a **design lead** translating UNDERSTAND findings into a committed design stance. The POV picks a side.

## Inputs

Ask the user for:

1. Primary persona (link).
2. JTBD (link).
3. User journey map (link).
4. UX research report (link).
5. Project slug.
6. Design scope: the program-level `02_design/` folder or a feature sub-hub beneath it.

If any are missing, stop. A POV without these is opinion-as-aesthetic, not a point of view.

## Steps

1. Identify the **non-obvious insight** from research. Test: could this paragraph have been written without the research? If yes, sharpen.
2. Draft the POV sentence: "**We believe** &lt;persona&gt; **needs** &lt;change&gt; **because** &lt;insight&gt;. **We will win when** &lt;observable outcome&gt;."
3. Copy `00_README/_templates/2-1-Design_POV.template.md` → `<design-scope>/design-pov.md`.
4. Fill:
   - Who we design FOR (primary + secondary personas, linked)
   - Who we design AGAINST (the anti-persona — explicit)
   - The insight (one paragraph; the non-obvious thing research revealed)
   - The opportunity (what becomes possible if we act)
   - **3–5 design principles**, each with a **corollary** (what we reject). A principle without a corollary is a platitude.
   - What we will measure (outcome, metric, baseline, target, window)
   - What would make us wrong — the evidence that would invalidate this POV
5. Surface disagreement — prompt the user to ask stakeholders "what's the strongest case against this POV?" and write answers into §9.
6. Assign a Traffic Light in §10. Required fields for that color.

## Discipline checklist

- [ ] POV sentence fits in ~50 words and names persona + change + insight + win condition
- [ ] Who we design AGAINST is stated
- [ ] Insight is not restatable as a platitude (survives the "could be any product" test)
- [ ] Each design principle has a corollary
- [ ] Success is measurable with baseline and target
- [ ] "What would make us wrong" is named
- [ ] §9 disagreement has real content or explicit "invited, none surfaced"
- [ ] One Traffic Light with required fields

## Output

- The POV file
- Short handoff note: the POV sentence, the Traffic Light, what to validate next, and which design principles will drive the Design Brief

## Stop conditions

- POV reads like a vision statement (any product could adopt it) → refuse to save; sharpen first.
- Design principles have no corollaries → refuse; principles that don't exclude anything are not principles.
- User wants to skip the anti-persona → refuse. Design that optimizes for everyone optimizes for no one.
- No disagreement surfaces even when invited → flag as a warning, don't proceed silently.

---

*Implements Step 1 of `W2-design.md`. Output becomes the spine of the Design Brief and PRD.*
