"""A deterministic, local IAM access policy evaluator and configuration comparison.

This module implements role-based access control (RBAC) policy evaluation based on
'2.3 IAM capabilities.md'. It evaluates access decisions under strict default-deny
and deny-overriding-allow semantics, and compares three controlled policy
configurations to report correctness and observed evaluation trade-offs.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from typing import Any, Dict, List, Optional, Tuple

LESSON_CITATION = "2.3 IAM capabilities.md"
VALID_EFFECTS = ("ALLOW", "DENY")

# Normal standard policy matrix (Config 2 - Standard RBAC)
STANDARD_POLICY_MATRIX: tuple[dict[str, str], ...] = (
    {"role": "reader", "action": "read", "resource": "public", "effect": "ALLOW"},
    {"role": "reader", "action": "write", "resource": "public", "effect": "DENY"},
    {"role": "editor", "action": "read", "resource": "public", "effect": "ALLOW"},
    {"role": "editor", "action": "write", "resource": "public", "effect": "ALLOW"},
    {"role": "auditor", "action": "audit", "resource": "logs", "effect": "ALLOW"},
    {"role": "auditor", "action": "audit", "resource": "logs", "effect": "DENY"},
)

# Controlled configurations for trade-off comparison
CONFIG_MINIMAL: tuple[dict[str, str], ...] = (
    {"role": "reader", "action": "read", "resource": "public", "effect": "ALLOW"},
    {"role": "reader", "action": "write", "resource": "public", "effect": "DENY"},
    {"role": "editor", "action": "read", "resource": "public", "effect": "ALLOW"},
)

CONFIG_STANDARD: tuple[dict[str, str], ...] = STANDARD_POLICY_MATRIX

CONFIG_COMPREHENSIVE: tuple[dict[str, str], ...] = STANDARD_POLICY_MATRIX + (
    {"role": "admin", "action": "read", "resource": "public", "effect": "ALLOW"},
    {"role": "admin", "action": "write", "resource": "public", "effect": "ALLOW"},
    {"role": "admin", "action": "delete", "resource": "public", "effect": "ALLOW"},
    {"role": "admin", "action": "delete", "resource": "system", "effect": "DENY"},
    {"role": "visitor", "action": "read", "resource": "public", "effect": "ALLOW"},
    {"role": "visitor", "action": "write", "resource": "public", "effect": "DENY"},
)

CONTROLLED_CONFIGS: dict[str, tuple[dict[str, str], ...]] = {
    "Config 1 (Minimal)": CONFIG_MINIMAL,
    "Config 2 (Standard)": CONFIG_STANDARD,
    "Config 3 (Comprehensive)": CONFIG_COMPREHENSIVE,
}

# Normal scenario requests
NORMAL_REQUESTS: tuple[dict[str, str], ...] = (
    {"role": "reader", "action": "read", "resource": "public"},
    {"role": "reader", "action": "write", "resource": "public"},
    {"role": "auditor", "action": "audit", "resource": "logs"},
    {"role": "stranger", "action": "read", "resource": "public"},
    {"role": "reader", "action": "delete", "resource": "public"},
)

# Boundary scenario requests
BOUNDARY_REQUESTS: tuple[dict[str, str], ...] = (
    {"role": "reader", "action": "read", "resource": "private"},
    {"role": "auditor", "action": "delete", "resource": "logs"},
    {"role": "reader", "action": "", "resource": "public"},
)

# Failure fixture: invalid policy rule effect
FAILURE_POLICY_FIXTURE: tuple[dict[str, str], ...] = (
    {"role": "reader", "action": "read", "resource": "public", "effect": "PERMIT"},
)

SCENARIO_EXPLANATIONS = {
    "normal": (
        f'Scenario: Illustrative IAM policy evaluation based on "{LESSON_CITATION}"; '
        "educational mock matrix, not real identity provider."
    ),
    "boundary": (
        f'Scenario: Boundary checks for IAM policy evaluation based on "{LESSON_CITATION}"; '
        "tests edge inputs and default-deny fallbacks."
    ),
    "failure": (
        f'Scenario: Failure check based on "{LESSON_CITATION}"; '
        "rejects malformed policy entries."
    ),
}


def validate_policies(policies: Sequence[dict[str, Any]]) -> None:
    """Validate policy rules structure and effect fields."""
    if not isinstance(policies, Sequence):
        raise TypeError(f"Policies must be a sequence, got {type(policies).__name__}")
    for idx, rule in enumerate(policies):
        if not isinstance(rule, dict):
            raise TypeError(f"Policy rule at index {idx} must be a dictionary")
        for key in ("role", "action", "resource", "effect"):
            val = rule.get(key)
            if not isinstance(val, str) or not val.strip():
                raise ValueError(f"Policy rule at index {idx} missing required field '{key}'")
        effect = rule["effect"].strip().upper()
        if effect not in VALID_EFFECTS:
            allowed = ", ".join(VALID_EFFECTS)
            raise ValueError(f"Invalid policy effect '{rule['effect']}' for role '{rule['role']}'. Allowed effects: {allowed}")


def evaluate_access(
    role: str,
    action: str,
    resource: str,
    policies: Sequence[dict[str, str]] = STANDARD_POLICY_MATRIX,
) -> dict[str, Any]:
    """Evaluate an authorization request against a policy matrix.

    Contract:
    - Default Deny: any action/resource or unknown role not explicitly permitted is DENY.
    - Explicit Deny Overrides Allow: if both ALLOW and DENY match, decision is DENY.
    - Unknown role is denied.
    """
    validate_policies(policies)

    clean_role = (role or "").strip()
    clean_action = (action or "").strip()
    clean_resource = (resource or "").strip()

    if not clean_role or not clean_action or not clean_resource:
        return {
            "decision": "DENY",
            "reason": "Malformed or empty request attribute (default deny).",
            "rule_checks": 0,
        }

    known_roles = {p["role"] for p in policies}
    if clean_role not in known_roles:
        return {
            "decision": "DENY",
            "reason": f"Role '{clean_role}' is unknown or not recognized (default deny).",
            "rule_checks": len(policies),
        }

    matching_effects: list[str] = []
    checks = 0

    for rule in policies:
        checks += 1
        if (
            rule["role"] == clean_role
            and rule["action"] == clean_action
            and rule["resource"] == clean_resource
        ):
            matching_effects.append(rule["effect"].upper())

    if not matching_effects:
        return {
            "decision": "DENY",
            "reason": f"No policy grants role '{clean_role}' permission to '{clean_action}' on '{clean_resource}' (default deny).",
            "rule_checks": checks,
        }

    # Explicit DENY strictly overrides ALLOW
    if "DENY" in matching_effects:
        if "ALLOW" in matching_effects:
            reason = f"Explicit DENY overrides matching ALLOW for role '{clean_role}' on '{clean_resource}'."
        else:
            reason = f"Explicit DENY rule matched for role '{clean_role}' on '{clean_resource}'."
        return {"decision": "DENY", "reason": reason, "rule_checks": checks}

    if "ALLOW" in matching_effects:
        return {
            "decision": "ALLOW",
            "reason": f"Permission granted for role '{clean_role}' to '{clean_action}' on '{clean_resource}'.",
            "rule_checks": checks,
        }

    return {"decision": "DENY", "reason": "Default deny fallback.", "rule_checks": checks}


def compare_configurations() -> list[dict[str, Any]]:
    """Compare three controlled configurations on correctness and evaluation checks.

    Benchmark test requests evaluate:
    1. reader read public -> ALLOW
    2. reader write public -> DENY
    3. auditor audit logs -> DENY (denied in minimal due to unknown role; denied in standard/comp via deny-override)
    4. stranger read public -> DENY (unknown role)
    """
    benchmark_requests = (
        ("reader", "read", "public", "ALLOW"),
        ("reader", "write", "public", "DENY"),
        ("auditor", "audit", "logs", "DENY"),
        ("stranger", "read", "public", "DENY"),
    )

    results = []
    for name, pol_set in CONTROLLED_CONFIGS.items():
        total_checks = 0
        correct_count = 0
        for r, a, res, expected in benchmark_requests:
            res_dict = evaluate_access(r, a, res, policies=pol_set)
            total_checks += res_dict["rule_checks"]
            if res_dict["decision"] == expected:
                correct_count += 1

        correctness_rate = (correct_count / len(benchmark_requests)) * 100.0
        avg_checks = total_checks / len(benchmark_requests)

        results.append({
            "configuration": name,
            "rules_count": len(pol_set),
            "requests_count": len(benchmark_requests),
            "correctness_rate": correctness_rate,
            "total_checks": total_checks,
            "checks_per_request": avg_checks,
        })
    return results


def format_evaluation_table(evaluations: Sequence[dict[str, Any]]) -> str:
    """Format evaluations into a pipe-delimited table."""
    lines = ["role | action | resource | decision | reason"]
    for row in evaluations:
        lines.append(
            f"{row['role']} | {row['action']} | {row['resource']} | "
            f"{row['decision']} | {row['reason']}"
        )
    return "\n".join(lines)


def format_comparison_table(comparison_results: Sequence[dict[str, Any]]) -> str:
    """Format comparison results into a readable text table."""
    header = (
        f"Configuration Comparison Experiment ({LESSON_CITATION})\n"
        f"{'=' * 80}\n"
        f"{'Config':<26} | {'Rules (N)':<9} | {'Requests':<8} | {'Correctness':<11} | {'Total Checks':<12} | {'Checks/Req'}\n"
        f"{'-' * 80}"
    )
    rows = []
    for r in comparison_results:
        rows.append(
            f"{r['configuration']:<26} | {r['rules_count']:<9} | {r['requests_count']:<8} | "
            f"{r['correctness_rate']:.1f}%{'':<6} | {r['total_checks']:<12} | {r['checks_per_request']:.1f}"
        )
    footer = (
        f"{'-' * 80}\n"
        "Observed Trade-off: Expanding policy granularity increases evaluation checks linearly "
        "(O(N) search), maintaining 100.0% policy correctness with default-deny and deny-override guarantees."
    )
    return "\n".join([header] + rows + [footer])


def run_scenario(scenario_name: str) -> tuple[int, str]:
    """Execute a scenario by name ('normal', 'boundary', 'failure', 'compare')."""
    if scenario_name not in SCENARIO_EXPLANATIONS and scenario_name != "compare":
        return 1, f"Error: unknown scenario '{scenario_name}'"

    if scenario_name == "normal":
        evals = []
        for req in NORMAL_REQUESTS:
            out = evaluate_access(req["role"], req["action"], req["resource"])
            evals.append({**req, **out})
        output = f"{SCENARIO_EXPLANATIONS['normal']}\n{format_evaluation_table(evals)}"
        return 0, output

    if scenario_name == "boundary":
        evals = []
        for req in BOUNDARY_REQUESTS:
            out = evaluate_access(req["role"], req["action"], req["resource"])
            evals.append({**req, **out})
        output = f"{SCENARIO_EXPLANATIONS['boundary']}\n{format_evaluation_table(evals)}"
        return 0, output

    if scenario_name == "failure":
        try:
            validate_policies(FAILURE_POLICY_FIXTURE)
            return 0, f"{SCENARIO_EXPLANATIONS['failure']}\nUnexpected success for invalid policy"
        except ValueError as exc:
            return 1, f"{SCENARIO_EXPLANATIONS['failure']}\nError: {exc}"

    if scenario_name == "compare":
        res = compare_configurations()
        return 0, format_comparison_table(res)

    return 1, f"Unhandled scenario '{scenario_name}'"


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point for running IAM policy evaluation lab."""
    parser = argparse.ArgumentParser(
        description="Local IAM access policy evaluator and configuration comparison."
    )
    parser.add_argument(
        "--scenario",
        choices=["normal", "boundary", "failure"],
        default="normal",
        help="Scenario to run: normal (default), boundary, or failure",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Run configuration comparison experiment and report trade-off metrics.",
    )
    parser.add_argument("--role", help="Specific role to evaluate")
    parser.add_argument("--action", help="Specific action to evaluate")
    parser.add_argument("--resource", help="Specific resource to evaluate")

    args = parser.parse_args(argv)

    if args.compare:
        code, out = run_scenario("compare")
        print(out)
        return code

    if args.role and args.action and args.resource:
        decision = evaluate_access(args.role, args.action, args.resource)
        print(f"Decision: {decision['decision']}")
        print(f"Reason: {decision['reason']}")
        return 0

    exit_code, output = run_scenario(args.scenario)
    if exit_code == 0:
        print(output)
    else:
        print(output, file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
