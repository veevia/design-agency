---
name: asset-collection
title: Gather the assets the prototype needs
description: Gather all visual assets, data samples, and media required for the prototype before Makers start building — so building is never blocked by missing content. Use when the concept involves real product interfaces (screenshots of existing tools, competitor screenshots), or for every sprint prototype that includes images, icons, charts, or real data.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - Every sprint prototype that includes images, icons, charts, or real data
  - When the concept involves real product interfaces (screenshots of existing tools, competitor screenshots)
  - When the prototype includes AI-generated content with real-world data (urgency scores against real requests, assignment suggestions from real specialist rotas)
  - When the persona is an expert who will immediately identify unrealistic or placeholder data as non-credible
applies-to: image gathering, icon sourcing, real data samples, screenshot collection, brand assets, API mock data
done_when:
  - Every asset the prototype needs is listed and sourced
  - Gaps (missing copy, images, data) are assigned to owners
  - Assets are staged so stitching isn’t blocked
metadata:
  duration: 1–2 h (parallel with Storyboard review at start of Prototype day)
  team-size: 1 Asset Collector; assisted by domain expert for real data
  sprint-phase: 5 Prototype
---

# Asset Collection

**TL;DR:** Asset collection is the first job on Prototype day. Before Makers open Figma, someone must have gathered every visual and data asset the prototype requires — logos, icons, screenshots, sample data records, product imagery, charts, maps, and any other content that cannot be typed. An Asset Collector who finishes in the first 60 minutes prevents Makers from losing 20 minutes per missing asset throughout the day. The total cost of skipping this step is always higher than the time it takes to do it.

## When to use

- Every sprint prototype that includes images, icons, charts, or real data
- When the concept involves real product interfaces (screenshots of existing tools, competitor screenshots)
- When the prototype includes AI-generated content with real-world data (urgency scores against real requests, assignment suggestions from real specialist rotas)
- When the persona is an expert who will immediately identify unrealistic or placeholder data as non-credible

## Asset categories

| Category | Examples | Source |
|---|---|---|
| **Product screenshots** | Existing booking inbox, specialist calendar, email client | Screenshot on a real machine; or use design team's asset library |
| **Icons** | Navigation icons, status indicators, action icons | The design system's icon set, Figma Community, or one open-source icon library |
| **Real data samples** | Actual request titles, booking channels, urgency-score examples | Subject-matter expert or sanitised production export |
| **User avatars / org data** | Coordinator names, site names, specialist rotas | HR org chart (anonymised); use fictional-but-realistic names |
| **Brand assets** | Client logo, product wordmark, brand colours (hex) | Brand portal or slide deck |
| **Charts / graphs** | Trend line for request volume over time, urgency-score distribution histogram | Screenshot from data tool, or fabricate using Figma charts plugin |
| **Images / photos** | Context photos (coordination office, site floor), product photography | A free or licensed stock-photo library (sprint-internal use only) |
| **Map tiles / geo data** | Site area map for request locations, specialist travel-time zones | A map screenshot from any mapping service |

## Asset collection checklist

```markdown
## Asset Collection Checklist — [Sprint Name] · [Date]

### Data assets
- [ ] 8–12 real request titles from the target domain (or realistic fictional equivalents)
- [ ] Booking channels and systems with reliability levels (e.g. phone line = High, inventory-system stock count = Medium)
- [ ] 3–5 realistic urgency score values (e.g. 78, 45, 91, 62, 34)
- [ ] Priority labels used in the domain (e.g. Outage — Urgent — Site C)
- [ ] Assignment destinations from the specialist rota (specialist names, site names)

### UI assets
- [ ] Product logo / wordmark (SVG or high-res PNG)
- [ ] Navigation icons (from agreed icon set — the design system's icons or one open-source icon library)
- [ ] Status icons: confirmed ✓, unconfirmed !, in-review ⏳, assigned →
- [ ] Avatar placeholder (consistent 32px or 40px round placeholder images)

### Screenshots
- [ ] Existing product screenshot (for "before" context in storyboard)
- [ ] Competitor or adjacent tool screenshot (if Lightning Demos surface was referenced)

### Organised into
- [ ] One shared Figma Assets page or
- [ ] One shared cloud folder with subfolders by category
```

## Organisation method

All assets must be accessible to all Makers without interruption:
- **Figma:** Create an "Assets" page in the sprint Figma file; paste all images, icon frames, and data tables there; Makers copy from this page
- **Shared folder:** Subfolders by category; all Makers have edit access; Asset Collector pastes file names into a team-chat message so Makers know what exists

Name assets descriptively: `request-unit-u200-title.txt`, `icon-confirmed-check.svg`, `screenshot-existing-booking-inbox.png`. Never: `image1.png`, `icon.svg`, `screenshot.png`.

## Real data vs. realistic fictional data

**Use real data when:**
- The domain expert is in the sprint and can provide sanitised samples quickly
- The participant persona will immediately identify fictional data as unrealistic ("No coordinator would send a Unit U-200 outage to a specialist without the required skill")
- The urgency score values matter to the assumption being tested

**Use realistic fictional data when:**
- Real data requires approval processes that would take longer than the sprint
- The prototype will be shown externally and real data is sensitive
- The assumption being tested is about the *structure* of the information, not the specific content

Realistic fictional data follows real patterns:
- Realistic asset models and fault codes from the domain (Unit U-200, fault E9), not generic "Product A"
- Urgency scores in plausible ranges for the feature being tested (if the team expects 60–80 as "normal," don't use 99)
- Assignment destinations that reflect actual org structure patterns ("Certified specialist — Site C" not "User B")

## Watch-outs

- **Starting Makers before assets are ready:** If a Maker needs the booking inbox screenshot and the Asset Collector hasn't fetched it yet, the Maker either blocks, invents a placeholder, or interrupts the Asset Collector. One wasted hour per Maker compounds across the whole team. Asset collection must happen in the first 60 minutes.
- **Icons from the wrong library:** If the Asset Collector pulls icons from a different library than the Maker is using in Figma, the prototype will look inconsistent. Agree on the icon set before Day 5.
- **Placeholder avatars that look like stock photos:** Participants immediately distrust stock imagery. Use abstract initials-based avatars or real (consented) team member avatars — both are more credible than a stock photo of a person.
- **Forgetting the "before" screenshot:** The storyboard often opens with the current painful state — if the Asset Collector doesn't capture the existing tool screenshot early, the Makers build the "before" screen from memory and it loses fidelity.
- **Proprietary data in shareable assets:** If the prototype uses real customer data, ensure the Asset Collector flags anything that cannot leave the sprint room. Set up a separate "public" version if the prototype will be shared outside the core team.

## Agent facilitation guide

When generating an asset collection plan:
1. Read the storyboard — identify every screen that requires a non-typable asset (images, icons, data, charts)
2. Categorise by asset type: data samples, UI icons, screenshots, images, brand assets
3. For each asset: identify source (where to get it), format (SVG/PNG/text/CSV), responsible person
4. Estimate time: data collection is typically 30–45 min; UI assets 15–20 min; screenshots 10–15 min
5. Output as a checklist — one checkbox per asset, with source and owner noted
6. Flag any asset that requires approval (proprietary data, licensed imagery, client brand materials)

## Connects to

- [Dividing Roles](../dividing-roles/SKILL.md) — Asset Collector is a named Prototype day role
- [Storyboard](../storyboard/SKILL.md) — storyboard panels are the primary source for asset inventory
- [Content Writing](../content-writing/SKILL.md) — textual data (request titles, labels) is produced by the Writer; visual assets by the Asset Collector
- [Prototyping Principles](../prototyping-principles/SKILL.md) — realistic assets support goldilocks fidelity
