---
name: content-writing
title: Write realistic prototype content, not lorem ipsum
description: Write realistic, specific placeholder copy for every prototype screen — so the prototype tests the experience of the real product, not the experience of Lorem Ipsum. Use when the sprint question is about whether users understand the UI, on every prototype, or when AI-generated text is part of the concept (score explanations, priority labels, assignment suggestions).
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - On every prototype — even a click-through Figma prototype needs real labels and data
  - When the sprint question is about whether users understand the UI — language is the primary variable
  - When AI-generated text is part of the concept (score explanations, priority labels, assignment suggestions) — write realistic AI copy, not placeholder tags
  - When the concept's value proposition is communicated primarily through copy (onboarding flows, empty states, error recovery messages)
  - When participants are subject-matter experts who will immediately detect unrealistic data
applies-to: UI copy, placeholder data, error messages, CTA labels, confirmation text, notification copy, onboarding language
done_when:
  - Prototype copy is realistic and domain-true, not placeholder
  - Tone matches the target user and product voice
  - Content is ready to drop into the prototype
metadata:
  duration: 1–2 h (concurrent with Maker build)
  team-size: 1 Writer; input from Facilitator and domain expert
  sprint-phase: 5 Prototype
---

# Content Writing

**TL;DR:** Content writing in a sprint prototype means producing all the text that appears in the interface: headlines, button labels, helper text, error messages, empty states, notification copy, and inline data. This is not Lorem Ipsum work. Realistic, specific copy changes how participants respond — "Assign to Site C" produces a completely different reaction than "Assign to [Team]." The Writer role owns this output for the full prototype; it is produced in parallel with visual and interaction building on Prototype day.

## When to use

- On every prototype — even a click-through Figma prototype needs real labels and data
- When the sprint question is about whether users understand the UI — language is the primary variable
- When AI-generated text is part of the concept (score explanations, priority labels, assignment suggestions) — write realistic AI copy, not placeholder tags
- When the concept's value proposition is communicated primarily through copy (onboarding flows, empty states, error recovery messages)
- When participants are subject-matter experts who will immediately detect unrealistic data

## What the Writer produces

| Content type | Example (generic) | Worked example (request triage) |
|---|---|---|
| **Screen headlines** | "Review Requests" | "38 requests · 8 unconfirmed" |
| **Button labels** | "Submit" → "Assign Request" | "Assign to Site C" |
| **Inline data** | "[Request Name]" | "Unit U-200 · fault E9 · out of service" |
| **AI-generated copy** | "Urgency: [score]" | "78 · Based on 3 matching records (phone line, service-contract database, inventory system)" |
| **Helper text** | "Select a category" | "Suggested priority appears below after AI review (usually < 2s)" |
| **Error messages** | "Error occurred" | "Assignment failed — specialist not available. Try the on-call rota or escalate to the site supervisor." |
| **Empty states** | "No items" | "No unconfirmed requests — all 38 requests have been reviewed this morning. Next batch arrives at 14:00." |
| **Confirmation copy** | "Submitted" | "Assigned to Site C · Site Supervisor notified · Ref: REQ-20260224-042" |
| **Notification text** | "New request" | "Urgent: 3 new outage requests since your last review" |

## Content writing process

**Step 1 — Inventory all text-bearing screens (15 min):**

Walk through the storyboard panels. For each panel, list every text element:
- Navigation labels
- Screen titles and subtitles
- Button / action labels
- Data fields (any number, name, date, status that appears)
- System-generated copy (AI responses, status messages)
- Error and edge-case copy

**Step 2 — Write screen by screen (45–60 min):**

Rules:
- **Use real domain vocabulary.** "Outage — Urgent — Site C" not "Category A — Subcategory B — Status 3."
- **Write for the persona, not the writer.** The Lead Coordinator has 5 years of triage experience — their interface doesn't explain basics.
- **AI copy must include reasoning.** "Urgency 78" is incomplete. "78 · 3 records confirmed, 1 record conflicting" is testable.
- **Error copy includes recovery paths.** "Cannot assign — specialist unavailable" is not a recovery path. Name the alternative.
- **Empty states answer the question "what do I do now?"** — they include an action, not just a message.

**Step 3 — Consistency pass (15 min):**

Check:
- Button labels consistent across screens ("Assign" vs "Assign Request" vs "Send to Site" — pick one)
- Status labels consistent ("Unconfirmed" / "Confirmed" / "In Review" — use same set everywhere)
- Dates and numbers realistic and internally consistent (if the scenario is Tuesday morning, request timestamps should be Monday evening or early Tuesday)

## Content spec format

```markdown
## Prototype Content Spec — [Sprint Name] · [Date]

### Screen: Morning Triage Queue
**Headline:** "38 requests · 8 unconfirmed"
**Sub-header:** "Last updated 06:47 · Next batch 14:00"
**Filter labels:** Unconfirmed | Confirmed | In Review | Assigned
**Active filter:** "Unconfirmed (8)"

### Screen: Request Detail — Unit U-200
**Request title:** "Unit U-200 · fault E9 · out of service"
**Channel:** Phone line, Feb 24 2026, 05:52
**AI urgency score:** 78
**Suggested priority:** "Outage — Urgent — Site C"
**Records inline:**
  - Phone line booking (High reliability) — "Unit out of service since last night; display shows E9…"
  - Service-contract database (High reliability) — "Unit U-200 under service contract; recalled part fitted at install"
  - Inventory system (Medium reliability) — "Replacement part: 2 in stock at Site C"
**Urgency explanation:** "78 · 3 records support the priority. Conflicting on parts: the inventory system shows 2 replacement parts in stock; the site's last manual count shows 1."
**Primary CTA:** "Assign Request"
**Secondary CTA:** "Change priority"

### Screen: Assignment Confirmation
**Confirmation headline:** "Request Assigned"
**Body:** "Assigned to: Site C · Assigned by: Lead Coordinator · Reference: REQ-20260224-042 · Customer notified ✓"
**Action:** "Back to requests (7 remaining)"
```

## Watch-outs

- **Lorem Ipsum destroys realism:** Participants respond to Lorem Ipsum as if the prototype is a wireframe — they give interface feedback ("I'd put the button here") instead of experience feedback ("I'd never assign a request without knowing who receives it"). Replace all filler text.
- **AI copy as black box:** If the prototype shows "Urgency 78" with no explanation, participants either accept it blindly or reject it blindly — neither produces useful data. Always show the reasoning.
- **Over-writing:** Every word in the prototype must earn its space. If it wouldn't be in the real product, don't put it in the prototype — it will generate feedback about copy you never intended to ship.
- **Inconsistent data:** If Panel 1 shows 38 requests and Panel 3 shows 35 requests without an assignment action between them, participants notice and lose trust in the prototype — even if it's "just a prototype."
- **Using the writer as a bottleneck:** The Writer should be producing copy while Makers are building frames. Don't wait until screens are complete to start writing — work from the storyboard panels directly.

## Agent facilitation guide

When generating prototype content:
1. Read the storyboard — identify every screen that requires text
2. For each screen: list headline, body copy, CTAs, data labels, and system-generated text as separate items
3. Use domain vocabulary from the research phase (POV Statement, JTBD canvases, expert interview notes) — match the language the user uses
4. For AI-generated copy: always include reasoning — score + source count + a brief explanation of what drove the score
5. For error states and empty states: include a specific recovery action, not just a status message
6. Output as a content spec table — one row per text element, one column per screen

## Connects to

- [Storyboard](../storyboard/SKILL.md) — storyboard panels drive the content inventory
- [Dividing Roles](../dividing-roles/SKILL.md) — Writer is a dedicated Prototype day role
- [Prototyping Principles](../prototyping-principles/SKILL.md) — realistic content is part of "goldilocks fidelity"
- [Design Principles](../design-principles/SKILL.md) — principles like "show the evidence, not just the verdict" drive what AI copy must include
- [Five-Act Interview](../five-act-interview/SKILL.md) — realistic copy prevents participants from commenting on placeholders instead of the experience
