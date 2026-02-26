# Ethical Boundary Enforcement (OpenClaw Skill)

A customizable ethical/policy gate that evaluates proposed actions before execution and returns one of: `allow`, `modify`, or `reject` with explicit rationale.

## What it does

- Loads user-defined policy rules
- Applies hard-block checks (immediate reject)
- Applies soft constraints (modify before allow)
- Enforces contextual rules (e.g., external actions require approval)
- Emits machine-readable decision output + human audit report

## Included files

- `SKILL.md` — skill behavior and policy model
- `scripts/evaluate_action.py` — compliance decision engine
- `references/sample-policy.json` — sample ethical policy
- `references/sample-action.json` — sample action payload
- `_meta.json` — metadata

## Quick Start

```bash
python3 scripts/evaluate_action.py \
  --action references/sample-action.json \
  --policy references/sample-policy.json \
  --out ./out/compliance-result.json \
  --audit ./out/compliance-audit.md
```

## Policy model

- **Hard blocks**: reject immediately
- **Soft constraints**: require modifications/redactions/review
- **Context rules**: conditional requirements (like explicit consent)

## Safety

- Advisory gate by default (no direct side effects)
- Supports least-privilege and approval-first workflows
- Full rationale/audit trail for every decision

## Commercial Support & Custom Builds

Want this adapted to your workflow or stack?

- Custom implementation
- Integration with your existing OpenClaw setup
- Security hardening + approval-gated actions
- Ongoing optimization and support

Contact: **DirtyLeopard.com**

## Service Packages

| Package | Price | Includes |
|---|---:|---|
| Starter Skill | $399 | 1 custom skill, setup docs, 1 revision |
| Growth Bundle | $1,200 | 3 custom skills, workflow integration, 14-day support |
| Operator Suite | $3,000+ | 5–8 skills, orchestration, security/reliability tuning |

For commercial licensing or retainers, open an issue in this repo or contact via DirtyLeopard.com.

## License

MIT
