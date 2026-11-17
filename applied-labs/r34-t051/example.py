"""Security scenario rubric checker - runnable concept example for Module 1.

Extends 1.7 End of module quiz with a structural rubric checker.
Verifies completeness and consistency of asset, threat, control, and residual-risk fields.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, List, Optional, Tuple

REQUIRED_FIELDS = ("asset", "threat", "control", "residual_risk")

THREAT_CONTROL_KEYWORDS = {
    "credential stuffing": ["mfa", "multi-factor", "rate limit", "lockout", "authenticator"],
    "eavesdropping": ["encryption", "tls", "https", "vpn", "ipsec", "ssl"],
    "sql injection": ["parameterized", "prepared statement", "input validation", "waf"],
    "unauthorized access": ["rbac", "access control", "mfa", "least privilege", "authentication"],
}


def check_scenario(scenario: Dict[str, Optional[str]]) -> Tuple[str, str]:
    """Check a scenario against the structural rubric.

    Returns:
        (status, message) where status is PASS, FAIL, or FLAG_REVIEW.
    """
    # 1. Completeness check
    for field in REQUIRED_FIELDS:
        val = scenario.get(field)
        if val is None or not str(val).strip():
            return "FAIL", f"Missing required field: {field}"

    asset = str(scenario["asset"]).strip()
    threat = str(scenario["threat"]).strip().lower()
    control = str(scenario["control"]).strip().lower()
    residual = str(scenario["residual_risk"]).strip()

    # 2. Control relevance check
    matched_threat_key = None
    for threat_key in THREAT_CONTROL_KEYWORDS:
        if threat_key in threat:
            matched_threat_key = threat_key
            break

    if matched_threat_key:
        expected_keywords = THREAT_CONTROL_KEYWORDS[matched_threat_key]
        has_match = any(kw in control for kw in expected_keywords)
        if not has_match:
            return "FLAG_REVIEW", (
                f"Control '{scenario['control']}' appears unrelated to threat '{scenario['threat']}'; "
                "flagged for human review"
            )

    return "PASS", "Scenario meets structural rubric requirements"


def get_default_scenarios() -> List[Dict[str, Optional[str]]]:
    """Returns the three fictional Module 1 scenarios."""
    return [
        {
            "name": "User credential store",
            "asset": "Customer authentication database",
            "threat": "Credential stuffing and unauthorized access",
            "control": "Enforce multi-factor authentication and rate limiting",
            "residual_risk": "Adversary session hijacking via phishing tokens",
        },
        {
            "name": "Missing asset scenario",
            "asset": "",
            "threat": "Eavesdropping on network communication",
            "control": "Implement TLS 1.3 encryption in transit",
            "residual_risk": "Compromised endpoints could still expose plaintext",
        },
        {
            "name": "Mismatched control scenario",
            "asset": "Public web portal",
            "threat": "SQL injection via search input",
            "control": "Deploy automated offline data backup service",
            "residual_risk": "Backups do not prevent data exfiltration via active injection",
        },
    ]


def run_scenarios(scenarios: List[Dict[str, Optional[str]]]) -> List[Tuple[str, str, str]]:
    results = []
    for s in scenarios:
        name = s.get("name", "Unnamed scenario")
        status, msg = check_scenario(s)
        results.append((name, status, msg))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Module 1 Security Scenario Rubric Checker")
    parser.add_argument(
        "--scenario",
        choices=["normal", "boundary", "failure"],
        default="normal",
        help="Scenario mode to execute",
    )
    args = parser.parse_args()

    print(f"Scenario mode: {args.scenario}")
    if args.scenario == "normal":
        scenarios = get_default_scenarios()
        results = run_scenarios(scenarios)
        for name, status, msg in results:
            print(f"[{status}] {name}: {msg}")
        return 0

    elif args.scenario == "boundary":
        # Boundary case: empty list of scenarios
        results = run_scenarios([])
        print(f"Executed 0 boundary scenarios successfully. Output count: {len(results)}")
        return 0

    elif args.scenario == "failure":
        # Failure case: missing asset scenario triggers non-zero exit in failure simulation mode
        scenarios = [
            {
                "name": "Deliberate failure scenario",
                "asset": None,
                "threat": "Eavesdropping",
                "control": "TLS encryption",
                "residual_risk": "Endpoint risk",
            }
        ]
        results = run_scenarios(scenarios)
        for name, status, msg in results:
            print(f"[{status}] {name}: {msg}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
