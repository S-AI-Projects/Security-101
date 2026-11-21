"""
IAM Access Policy Evaluator (Task R34-T002)
Evaluates access decisions from a local role/action/resource matrix.
Default deny, and explicit deny overrides allow.
"""
import sys
import json
import argparse

def get_policy_matrix():
    return [
        {"role": "reader", "action": "read", "resource": "public", "effect": "ALLOW"},
        {"role": "reader", "action": "write", "resource": "public", "effect": "DENY"},
        {"role": "editor", "action": "read", "resource": "public", "effect": "ALLOW"},
        {"role": "editor", "action": "write", "resource": "public", "effect": "ALLOW"},
        {"role": "auditor", "action": "audit", "resource": "logs", "effect": "ALLOW"},
        {"role": "auditor", "action": "audit", "resource": "logs", "effect": "DENY"}
    ]

def evaluate_access(role, action, resource, policies=None):
    if policies is None:
        policies = get_policy_matrix()

    known_roles = set(p["role"] for p in policies)
    if role not in known_roles:
        return {"decision": "DENY", "reason": f"Role '{role}' is unknown or not recognized (default deny)."}

    matching_effects = []
    for p in policies:
        if p["role"] == role and p["action"] == action and p["resource"] == resource:
            matching_effects.append(p["effect"])

    if not matching_effects:
        return {"decision": "DENY", "reason": f"No policy grants role '{role}' permission to '{action}' on '{resource}' (default deny)."}

    if "DENY" in matching_effects:
        return {"decision": "DENY", "reason": f"Explicit DENY rule overrides any ALLOW for role '{role}' on '{resource}'."}

    if "ALLOW" in matching_effects:
        return {"decision": "ALLOW", "reason": f"Permission granted for role '{role}' to '{action}' on '{resource}'."}

    return {"decision": "DENY", "reason": "Default deny fallback."}

def main():
    parser = argparse.ArgumentParser(description="IAM Access Policy Evaluator")
    parser.add_argument("--role", default="reader")
    parser.add_argument("--action", default="read")
    parser.add_argument("--resource", default="public")
    args = parser.parse_args()
    result = evaluate_access(args.role, args.action, args.resource)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
