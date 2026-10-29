---
title: "The New Product Playbook: AI-Powered Workflows"
type: reference
status: published
source: "Figma report — The New Product Playbook: AI-Powered Workflows (figma.com/reports)"
converted_from: "The New Product Playbook_AI Powered Workflows.pdf"
tags: [type/reference, purpose/reference, status/published, loop/all]
---

# The New Product Playbook: AI-Powered Workflows

> **TL;DR:** When building is fast, the hard part isn't making things, it's deciding what's worth making. Move between code, canvas, and conversation in fluid loops; watch for drift; and invest in craft, tool fluency, and your design system because they compound across every AI workflow.

This is a structured Markdown summary of a public Figma report, kept here so wiki pages and artifacts can cite it. The source PDF is not stored in the repository. The [`drift-check`](../../03_Agents-and-Skills/Skills/drift-check/SKILL.md) and [`design-system-as-infrastructure`](../../03_Agents-and-Skills/Skills/design-system-as-infrastructure/SKILL.md) skills operationalize §1 and §3; [`05_Library/DESIGN-SYSTEM-AI-INSTRUCTIONS.md`](../../05_Library/DESIGN-SYSTEM-AI-INSTRUCTIONS.md) applies §3 to this repository.

---

## Introduction

AI tools are opening up new ways of working and raising new questions about what to build, how to stay on track, and where to focus. The product development process no longer follows a straight line from brainstorm → design → code. It can start anywhere, move between surfaces, and loop back on itself in a single day.

Speed lets teams explore more directions and test ideas that were previously too expensive. But it also changes the shape of the work: **when building is fast, the hard part is deciding what's worth making.** The best teams balance exploration and focus by bringing others in early and working in fluid loops between code, canvas, and conversation.

Three sections ahead:

1. How to move fast without losing the thread
2. Code, canvas, and back again: how teams build today
3. What to invest in right now

---

## 1. How to move fast without losing the thread

Speed introduces two risks: **quality slip** and **drift** (the slow accumulation of small changes that pulls the build away from the original intent). Drift compounds with scale, when more people build in parallel, small decisions happen without full context.

### Signals of drift, and what to do

| Signal | What it means | What to do |
|---|---|---|
| **Feedback keeps circling the same question** | Current direction isn't addressing the real problem | Stop refining; generate alternatives and compare side by side. Ask whether you're solving the right problem. |
| **Something feels off but no one can articulate why** | Hidden friction | Review the work for gaps; pull the full flow end-to-end; get an outside perspective; ground it in user research. |
| **The build feels far from the original pitch** | Accumulated small scope shifts | Put build next to original design; compare against the design system; revisit the brief; name what changed and why; rebuild from real components/tokens. |
| **The team can't pick one direction over another** | Lack of conviction; too few options seen | Go wider, generate real alternatives; name the trade-offs; put it in front of users. |

### Turning directions into a decision

Once you've gone wide enough to see trade-offs clearly, zoom out **together** and evaluate options at the **same fidelity** so everyone decides from shared context.

How to test a direction before committing:

- **Compare directions side by side** — which one breaks, which holds across the full flow?
- **Force the trade-off conversation** — don't ask which works; ask what each gives up (speed, clarity, flexibility, complexity).
- **Push the leading option into reality** — take it into code far enough to see where it breaks under real constraints.
- **Make the direction legible** — if an outsider can understand it without a walkthrough, and there's little daylight between spec and result, you're ready to commit.

> *Pattern:* Build test prototypes in a tool you can edit between user sessions, so you can fix bugs and act on suggestions as they come. If the same feedback comes up three times, update the prototype and A/B test the new version on the spot.

---

## 2. Code, canvas, and back again: how teams build today

Moving between code and canvas is easier than ever. The workflows below aren't mutually exclusive, reach for whichever fits where you are and what you need to figure out next.

### Prompt to prototype
**Use when:** exploring many directions fast, aligning stakeholders around something tangible, or validating before investing design/eng resources.

Prototypes are cheap now, so PMs replace PRDs with prototypes to kick off, and designers explore more directions before committing. From a prototype the work can go to: a review deck (a whiteboard or slides), the canvas (lay options side by side), back to code/Make (validate edge cases, interactions), or handoff to developers as reference.

> *Pattern (an AI-driven web page):* Build a page that reorganizes around what a user types; connect the design system via MCP so output matches the library, and let the prototyping tool suggest micro-interactions and handle transitions.

#### Match fidelity to the moment

| Fidelity | Format | Use case |
|---|---|---|
| Low | Whiteboard sketch, paper | Still figuring out the problem / aligning on the brief |
| Mid | Clickable Figma flow | Exploring how the experience should work |
| Functional | Make prototype with system components | Testing interactions or putting something in front of users |
| Production-adjacent | Working prototype in code (e.g., Codex) | Validating against real data and constraints before building |

### Code-first exploration
**Use when:** you need to test against real technical constraints before the team weighs in on design.

Start in code (working UI, real data, real interactions), then bring it to the canvas (code-to-canvas) to see everything at once, catch inconsistencies, explore alternatives, and refine before committing. Loop back to code via MCP as needed.

> *Pattern:* A PM builds a functional drag-and-drop prototype in code; UX rebuilds it against the design system, then uses a code-to-canvas tool to simplify the layout for the people who will actually use it.

### Agentic design to code
**Use when:** ready to move a design into code and want to carry design intent with it.

MCP pulls structured design context (components, tokens, layout) into the coding environment so an AI tool generates an implementation closer to the original. Code Connect carries component↔code mappings. It's not one-way, bring generated code back to the canvas, compare, adjust, push back via MCP.

> *Pattern:* Load design artifacts into the design tool's MCP server and connect it to a coding agent; the agent generates the front-end starting point, and engineers build production from code that already reflects the designs.

### AI-assisted work on the canvas
The canvas is where teams see the full picture. Now AI agents work there too, connected to the design system and team files. Use the agent during exploration (layout variations), after pulling code onto the canvas (audit build vs. system), when refining (apply system, write realistic placeholder content), and when narrowing down (gut-check, flag what's missing).

> *Pattern:* Use the canvas agent at nearly every stage, for layout options, UX gut checks and realistic placeholder copy in a technical domain. The agent speeds up design work; the designer still decides.

### Multi-agent workflows
A product builder supervises a pipeline of specialized agents in parallel rather than one agent per task. Example: Figma Make generates initial screens → Figma's agent audits every element against the design system → a coding tool (Codex) wires up the implementation. Today these steps are still largely sequential and human-directed; as tools become more autonomous, the team's time shifts toward **taste and judgment** over manual execution.

---

## 3. What to invest in right now

The fundamentals haven't changed: framing the problem before jumping to a solution, knowing when to question a direction that looks right but doesn't feel right. When AI can generate a decent v1, the value shifts to knowing what to do with it.

### Fluency across tools
Aim for fluency, not mastery, know enough about each tool to use it confidently when the moment calls for it.

- Know when a design must move beyond the canvas (some questions need real data/constraints).
- Be ready to work with what arrives from code.
- Use Make to prototype interactions, test how something feels.
- Learn prompting best practices, output depends on input.

> *Pattern:* Front-load prompts with requirements and functionality; a team can reach a working, true-to-product prototype within five prompts. A bare "build this" request tends to produce something different from what the requester meant.

### Investing in craft
When anyone can make anything, care and craft set the product apart. Build the muscle to judge whether output **feels** right, not just **looks** right.

- Spend time with the work after AI generates it, push it further.
- Study products you admire, learn what makes flows feel effortless.
- Hold a high bar for craft, the one thing AI can't do for you.

### Treating your design system as infrastructure
In the AI era the design system is the encoded taste and standards AI tools use to produce output. Every Make prototype draws from it; investing in it compounds across every AI workflow.

- Clean up components, tokens, and patterns, messy files produce off-brand output and drifting code.
- Document your standards.
- Set up Make templates with real components and layout rules baked in.
- Write instructions for AI tools (which components to reach for, which patterns to follow).

> *Pattern:* Standardize design files (naming, variables, auto layout), document MCP usage, and build a **prompt library of fixes** for common issues so anyone can look up a recommended prompt. Foundations first → speed without cost to consistency.

---

## Key takeaways

1. **Speed is an advantage for exploration, not just execution.** Use it to try more directions before committing, not to ship the first thing.
2. **Watch for signals of drift.** When feedback keeps circling, gut feelings won't go away, or the team can't explain this direction over another, step back and go wider.
3. **Invest in craft deliberately.** When anyone can generate something that looks good, judging what's actually good, and pushing it further, sets great work apart.
4. **Your design system is infrastructure now.** AI tools use it to generate prototypes and code; the cleaner and more complete it is, the better the output.
