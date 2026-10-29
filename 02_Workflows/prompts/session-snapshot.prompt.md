---
description: "Compact the current session into a wiki `_wiki/sessions/<YYYY-MM-DD>-<slug>.md` handoff. Decisions, files touched, open questions, next action. Resume by reading the latest snapshot."
agent: agent
---

# /session-snapshot

Apply Anthropic's compaction pattern to the current working session. Produces a durable handoff that the next session can read first instead of re-crawling.

## Inputs

- **hub** (required): folder slug under `01_Project-Hubs/`. If the session spanned hubs, write one snapshot in the hub that owns the next action and link the others.
- **slug** (optional): kebab-case 2–5 word summary; if omitted, derive from the session's main topic.

## Procedure

1. **Load operating skills**:
   - `03_Agents-and-Skills/Skills/wiki-maintenance/SKILL.md`
   - `03_Agents-and-Skills/Skills/extreme-clarity/SKILL.md`

2. **Discuss the snapshot scope with the user.** One paragraph: "Here's what I think we did this session. Want me to add/remove anything before I write?"

3. **Write the snapshot** at `01_Project-Hubs/<hub>/_wiki/sessions/<YYYY-MM-DD>-<slug>.md`.

   Structure:
   ```markdown
   ---
   type: session
   date: <YYYY-MM-DD>
   duration_turns: <approximate>
   hub: <hub slug>
   files_touched: [<rel paths>]
   tools_used: [<tool names>]
   ---
   # <Snapshot title>

   **TL;DR:** <one sentence — what changed this session>.

   ## Decisions made
   - [<traffic-light>] <decision> — <one-line rationale>

   ## Files touched
   - <rel path>: <one-line what changed>

   ## Open questions
   - <question>

   ## Next action
   - <single, specific next step>

   ## Resume by reading
   1. <top relevant wiki page>
   2. <top relevant artifact>
   3. <this snapshot>
   ```

4. **Update `_wiki/log.md`** (if hub-scoped):
   ```
   ## [YYYY-MM-DD HH:MM] session-snapshot | <slug>
   - Files touched: <n>
   - Decisions: <n>
   - Next action: <link>
   ```

5. **Surface to user:**
   - The snapshot file path
   - Remind: "Next session, start with `read_file <snapshot path>` before anything else"

## Targets / guardrails

- **TL;DR ≤25 words.** It's the first thing the next session sees.
- **`Next action` is single and specific.** "Continue work" is not a next action.
- **Decisions carry a Traffic Light.** Most need no record; only a new durable choice goes through [W5](../../02_Workflows/workflows/W5-decide.md).
- **Don't snapshot tiny sessions.** If duration_turns < ~10 or no files touched, just write a one-paragraph memory note instead.

## When this goes wrong

- **User disagrees with the framing in step 2**: re-discuss, don't write.
- **Session touched confidential material**: keep the snapshot in that hub's `_wiki/sessions/` and summarize without quoting restricted content.

## See also

- [`/capability-spot`](../../02_Workflows/prompts/capability-spot.prompt.md) — the loop-closure prompt that reads snapshots
- SOP: [`session-snapshot`](../../02_Workflows/SOPs/session-snapshot/SOP.md)
- [Anthropic — compaction pattern](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
