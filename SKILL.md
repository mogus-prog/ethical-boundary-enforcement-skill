---
name: ethical-boundary-enforcement
description: Evaluate proposed actions against customizable ethical/policy rules before execution, then allow, modify, or reject actions with explicit rationale to support safe autonomy.
---

# Ethical Boundary Enforcement

This skill provides a policy gate before action execution.

## Core Behavior
1. Load user-defined norms/policies
2. Evaluate action intent + risk tags
3. Determine outcome:
   - `allow`
   - `modify`
   - `reject`
4. Emit compliance report and safe alternative suggestions

## Quick Start

```bash
python3 skills/ethical-boundary-enforcement/scripts/evaluate_action.py \
  --action skills/ethical-boundary-enforcement/references/sample-action.json \
  --policy skills/ethical-boundary-enforcement/references/sample-policy.json \
  --out memory/ethics/compliance-result.json \
  --audit memory/ethics/compliance-audit.md
```

## Policy Model
- **Hard blocks**: immediate reject (e.g., secrets exposure, harmful/illegal behavior)
- **Soft constraints**: modify before allow (e.g., needs approval, redact sensitive fields)
- **Context constraints**: conditional rules (e.g., external send requires explicit consent)

## Safety
- Default is advisory gating (no direct side effects)
- Enforces least-privilege and approval-aware operation patterns
- Produces full rationale for every decision
