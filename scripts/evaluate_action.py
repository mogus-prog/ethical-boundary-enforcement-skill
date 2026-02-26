#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime, timezone


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def has_any(tags, blocked):
    t = set(tags or [])
    b = set(blocked or [])
    return len(t.intersection(b)) > 0


def evaluate(action, policy):
    tags = action.get("risk_tags", [])
    kind = action.get("kind", "internal")
    requires_external = bool(action.get("external", False))
    has_approval = bool(action.get("has_explicit_approval", False))

    hard = policy.get("hard_blocks", {})
    soft = policy.get("soft_constraints", {})
    ctx = policy.get("context_rules", {})

    reasons = []
    modifications = []

    # Hard blocks
    if has_any(tags, hard.get("blocked_tags", [])):
        reasons.append("matches hard-block tag")
        return "reject", reasons, modifications

    if kind in hard.get("blocked_kinds", []):
        reasons.append(f"action kind '{kind}' is hard-blocked")
        return "reject", reasons, modifications

    # Context rules
    if requires_external and ctx.get("external_requires_approval", True) and not has_approval:
        reasons.append("external action without explicit approval")
        modifications.append("request explicit approval before execution")

    # Soft constraints
    if has_any(tags, soft.get("redact_tags", [])):
        reasons.append("contains tags requiring redaction")
        modifications.append("redact sensitive content before execution")

    if kind in soft.get("review_kinds", []):
        reasons.append(f"kind '{kind}' requires human review")
        modifications.append("route for human review")

    if modifications:
        return "modify", reasons, modifications

    return "allow", ["policy-compliant"], modifications


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--action", required=True)
    ap.add_argument("--policy", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--audit", required=True)
    args = ap.parse_args()

    action = load_json(args.action, {})
    policy = load_json(args.policy, {})

    decision, reasons, modifications = evaluate(action, policy)

    result = {
        "timestamp": now_iso(),
        "decision": decision,
        "reasons": reasons,
        "modifications": modifications,
        "action": action,
    }

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    os.makedirs(os.path.dirname(args.audit) or ".", exist_ok=True)
    with open(args.audit, "w", encoding="utf-8") as f:
        f.write(f"# Ethical Compliance Audit ({result['timestamp']})\n\n")
        f.write(f"- Decision: **{decision.upper()}**\n")
        f.write(f"- Action kind: `{action.get('kind','unknown')}`\n")
        f.write(f"- External: `{action.get('external', False)}`\n")
        f.write(f"- Risk tags: `{action.get('risk_tags', [])}`\n\n")
        f.write("## Reasons\n")
        for r in reasons:
            f.write(f"- {r}\n")
        if modifications:
            f.write("\n## Required Modifications\n")
            for m in modifications:
                f.write(f"- {m}\n")

    print(f"Wrote {args.out}")
    print(f"Wrote {args.audit}")


if __name__ == "__main__":
    main()
