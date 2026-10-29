---
description: "Force the trade-off conversation — for each candidate direction, name what it gives up, so the team chooses from shared context instead of debating in the abstract."
agent: agent
---

# /trade-off

Don't ask which direction works. Ask what each one gives up. The decision gets easier when you can see what you're saying no to.

## Inputs

- **directions** (required): 2+ candidate directions/approaches (paths, links, or descriptions)
- **hub** (optional): folder slug under `01_Project-Hubs/` for context

## Procedure

1. **Load operating skills**:
   - `03_Agents-and-Skills/Skills/alignment-playbook/SKILL.md`
   - `03_Agents-and-Skills/Skills/evidence-tagging/SKILL.md`

2. **Normalize fidelity.** Confirm all directions are described at the *same* level of detail. If not, level them first — comparing a sketch to a built flow is not a fair trade-off.

3. **For each direction, name the cost** across these axes: speed, clarity, flexibility, complexity, and any program-specific constraint. Tag claims `observed | reported | assumed`.

4. **Surface disagreement by name** (alignment-playbook) — who prefers what and why. Silence is not consent.

5. **Recommend one**, stating explicitly what it gives up, then close with a Traffic Light in the answer. Record it through [W5](../../02_Workflows/workflows/W5-decide.md) only if it is a new durable choice (load `traffic-light-decisions` then).

6. **Output shape:**
   ```
   === /trade-off ===
   | Direction | Gives up | Strength | Best when |
   |---|---|---|---|
   ...
   Disagreement: <names + positions>
   Recommendation: <direction> — accepting the cost of <X>
   Decision: 🟢|🟡|🔴 <one line>
   ```
