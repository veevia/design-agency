# Licensing — free vs paid, decision-framed

Remotion is **source-available, not open-source.** Settle the license before you produce video for an
organization. The rule is short; the trap is assuming "it's just a tool, so it's free."

Source: the Remotion license (`LICENSE.md` in `github.com/remotion-dev/remotion`), remotion.dev/docs/license and
the License FAQ (remotion.dev/docs/license/faq), checked 2026-10-29. Remotion has announced license changes for
version 5.0 — re-read the source pages before relying on this summary for a purchase or a new major version.

## The rule — Free License eligibility

You may use Remotion **for free**, including commercially, if you are:

- an individual (personal or commercial use)
- an organization or team of **up to 3 people** (a one-person company qualifies)
- a non-profit or not-for-profit organization (Remotion's definition is narrow: government bodies, educational
  institutions, trade associations and commercial subsidiaries don't qualify without written permission)
- **evaluating** whether Remotion fits, and not yet using it commercially

The free tier has the same functionality as the paid one. If you don't qualify, you need a paid **Company
License** (remotion.pro).

## The key test: the headcount of the organization that uses it

- Eligibility depends on the organization's **total headcount**, not on how many people touch Remotion. A
  20-person company where one person uses Remotion needs a Company License.
- The machine doesn't matter: a personal laptop doesn't make company work free.
- **Client work:**
  - You deliver only a finished video file (an MP4) and the client never receives or runs the Remotion project →
    only your organization's headcount counts.
  - The client owns or operates the Remotion project, or you develop it together → both headcounts aggregate
    toward the 4-person threshold, and the entity that ultimately owns the project's IP is responsible for the
    license.
  - Contractors, freelancers or another studio operating Remotion on the same project → their headcount
    aggregates with yours.

## Company License plans (snapshot — verify current pricing)

As published in the License FAQ on 2026-10-29 (the pricing calculator is at remotion.dev/docs/license/pricing):

- **Remotion for Creators** — per seat (US$25/month per person who writes Remotion code, by hand or with an
  agentic coding tool); for organizations that produce videos without an automation.
- **Remotion for Automators** — per render (US$0.01, minimum US$100/month); for organizations whose code
  programmatically calls the render APIs or the `npx remotion render` / `still` commands — automated pipelines,
  prompt-to-video tools, the Remotion Player. An agent workflow that renders on a schedule or on demand can fall
  here.
- **Enterprise** — Company License pricing with a US$500/month minimum, plus negotiated terms, paperwork and
  priority support.

Organizations eligible for the Free License may run automations without paying.

## Decision table

| What you're making | Who uses Remotion / owns the project | Light | Why |
|---|---|---|---|
| Personal learning, practice or a personal project you own | you, as an individual | 🟢 free | individual clause; commercial use allowed |
| A throwaway proof to see whether Remotion fits | anyone | 🟢 free | evaluation clause — until it's used commercially |
| Work for an organization of up to 3 people | that organization | 🟢 free | small-organization clause |
| Work for a qualifying non-profit | the non-profit | 🟢 free | non-profit clause; Remotion may ask for evidence |
| Work for a for-profit organization of 4+ people | that organization | 🔴 Company License | total headcount counts, not the number of users |
| An agency (≤3 people) delivering only a finished MP4 | the agency | 🟢 free | the client's headcount doesn't count |
| The client owns or co-develops the Remotion project | both organizations | 🔴 if combined headcount ≥ 4 | headcounts aggregate; the IP owner buys |
| An automated render pipeline at a licensed organization | that organization | 🔴 Remotion for Automators | scripted render/still calls count as an automation |

## How to act on it

- **🟢 Personal learning or evaluation:** proceed. Keep personal projects in a folder you own, outside any work
  repository, so the boundary is self-evident.
- **🔴 Organization of 4+ people:** don't proceed as if free. Raise the license question with the project's owner
  — it's a procurement and legal decision, not an `npm install` decision. You can still build a throwaway proof
  under the evaluation clause; flag that using it commercially needs the license first.
- **🟡 Ambiguous ownership or headcount:** treat it as Yellow — trigger: "before the video is used commercially or
  delivered"; expiry: confirm with the project owner within the same work session. Don't ship
  ambiguous-ownership output as "free."
