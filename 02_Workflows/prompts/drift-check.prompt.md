---
description: "Compare a hub's current build against its original brief/PRD and design system, detect drift across four signals, and close with a Traffic Light decision."
agent: agent
---

# /drift-check

Catch drift early — before the gap between intent and build is expensive to fix.

## Inputs

- **hub** (required): folder slug under `01_Project-Hubs/` (e.g. `example-project`)
- **scope** (optional): a specific feature sub-hub or flow to focus on

## Procedure

1. **Load operating skills**:
   - `03_Agents-and-Skills/Skills/drift-check/SKILL.md`
   - `03_Agents-and-Skills/Skills/evidence-tagging/SKILL.md`
   - Load `traffic-light-decisions` only if [W5](../../02_Workflows/workflows/W5-decide.md) requires authoring or changing a record.

2. **Gather the two reference points:**
   - Original intent → `01_Project-Hubs/<hub>/02_design/` (brief, PRD, POV)
   - Current build → `01_Project-Hubs/<hub>/03_build/`
   - Design system → `05_Library/DESIGN-SYSTEM-AI-INSTRUCTIONS.md`

3. **Score each of the four drift signals** (present / absent), citing specific evidence tagged `observed | reported | assumed`:
   - Feedback keeps circling the same question
   - Something feels off but no one can say why
   - The build feels far from the original pitch
   - The team can't pick one direction over another

4. **Map each present signal to its response** (see skill table). Where "go wider" is the response, offer to run `/go-wider`; where trade-offs are unclear, offer `/trade-off`.

5. **Close with an evidence-backed Traffic Light assessment** in the answer or existing build/task notes:
   - 🟢 stay the course — intent and build aligned
   - 🟡 watch — requires `trigger` + `expiry`
   - 🔴 go wider now — drift confirmed

   A routine assessment needs no new decision file. Use W5 only for a new durable choice, explicit
   capture request, or lifecycle change; it chooses the record type. Do not default a finding to ADR.

6. **Output shape:**
   ```
   === /drift-check <hub> ===
   Signal 1 — circling feedback:  present|absent  [evidence]
   Signal 2 — feels off:          present|absent  [evidence]
   Signal 3 — far from pitch:     present|absent  [evidence]
   Signal 4 — no conviction:      present|absent  [evidence]

   Responses: <mapped responses>
   Assessment: 🟢|🟡|🔴 <one line> → <existing evidence reference or this answer>
   Decision record: <reused/new path only if W5 required one; otherwise none>
   ```

## See also

- Skill: [`drift-check`](../../03_Agents-and-Skills/Skills/drift-check/SKILL.md) · evaluation template: [`drift-finding.template.md`](../../03_Agents-and-Skills/Skills/drift-check/assets/drift-finding.template.md)
- [`/go-wider`](../../02_Workflows/prompts/go-wider.prompt.md) · [`/trade-off`](../../02_Workflows/prompts/trade-off.prompt.md)
