# README assets

**TL;DR:** The animated overview at the top of the repository README, in two formats, and its still image live here; all describe Design Agency OS 2.0.0.

| File | What it is |
|---|---|
| `design-agency-os.avif` | 1600 × 900, 25 fps, a 22.4-second loop: the five task steps, what each step uses, the project hub's four phases and the six contracts, with one step in focus at a time. About a sixth of the GIF's size; the README offers it first |
| `design-agency-os.gif` | The same loop as a GIF, for browsers and readers that don't show animated AVIF |
| `design-agency-os.png` | The first frame, the complete overview that the loop fades back to: for print, previews and readers who ask for reduced motion |

- The style matches the PDG, FDE Design Toolkit and VPG overviews: Geist and Geist Mono type (SIL Open Font License 1.1), neutral surfaces, and sub colors only on small entities (violet for agents, blue for tools and evidence gates). The GIF palette holds every color token exactly.
- The facts come from [AGENTS.md](../../AGENTS.md), the [operating guide](../../00_Agentic-OS/README.md), [ARCHITECTURE](../ARCHITECTURE.md) and `agency.py status` at version 2.0.0. Redraw the animation when a count it shows changes: 87 skills, 21 review rows, 136 unit tests, 5 steps, 4 phases or 6 contracts.
- The README shows them through `<picture>`: the still when the reader's system asks for reduced motion, otherwise the AVIF, and the GIF where AVIF can't be shown. The AVIF has a keyframe every 2 seconds, so Safari plays it on time, and color tags, so every browser shows the token colors.
- Images here carry no metadata; the privacy gate scans them before every release.
