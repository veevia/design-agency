---
description: "Generate real alternatives before deciding — break out of low-conviction debate by producing concrete directions to compare side by side."
agent: agent
---

# /go-wider

When the team can't pick a direction, the problem is usually too few real options. Go wide, generate actual alternatives, then narrow with `/trade-off`.

## Inputs

- **problem** (required): the design problem or screen/flow stuck without conviction
- **hub** (optional): folder slug under `01_Project-Hubs/` for context
- **n** (optional, default 3): number of distinct directions to generate

## Procedure

1. **Load operating skills**:
   - `03_Agents-and-Skills/Skills/design-system-as-infrastructure/SKILL.md`
   - `03_Agents-and-Skills/Skills/design-thinking-loop/SKILL.md` (fidelity ladder)

2. **Match fidelity to the moment.** Pick the lowest fidelity that lets the team react meaningfully (see fidelity ladder). Don't over-build options you'll throw away.

3. **Generate N genuinely distinct directions** — not variations of one idea. Each should make a different bet about the core problem. Build them from real design-system components/tokens so comparison is fair and on-brand.

4. **Lay them side by side** and state, for each, the bet it makes and where it might break.

5. **Hand off to `/trade-off`** to force the cost conversation, then to a Traffic Light decision. If the team is still split, recommend putting the top contenders in front of users.

6. **Output shape:**
   ```
   === /go-wider: <problem> ===
   Direction A — <bet>; breaks if <X>
   Direction B — <bet>; breaks if <Y>
   Direction C — <bet>; breaks if <Z>
   Next: run /trade-off on these, or test top 2 with users.
   ```
