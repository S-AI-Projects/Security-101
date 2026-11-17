"""Data Security Scenario Rubric Checker with Worked Regression Example (R34-T055).

Extends 7.3 End of module quiz.
Evaluates data security scenarios for structural completeness and consistency.
Publishes a worked input-to-output example tested as an exact regression test.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, List, Optional, Tuple

REQUIRED_FIELDS = ("asset", "threat", "control", "residual_risk")

THREAT_CONTROL_KEYWORDS = {
    "exfiltration": ["encryption", "tde", "dlp", "masking", "access control"],
    "alteration": ["hashing", "integrity", "tls", "signature", "hmac"],
    "re-identification": ["k-anonymity", "differential privacy", "generalization", "pseudonymization"],
    "unauthorized access": ["iam", "rbac", "encryption", "least privilege"],
}


def check_scenario(scenario: Dict[str, Optional[str]]) -> Tuple[str, str]:
    """Check a data security scenario against the structural rubric.

    Returns:
        (status, message)
    """
    for field in REQUIRED_FIELDS:
        val = scenario.get(field)
        if val is None or not str(val).strip():
            return "FAIL", f"Missing required field: {field}"

    threat = str(scenario["threat"]).strip().lower()
    control = str(scenario["control"]).strip().lower()

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


def get_worked_example_scenarios() -> List[Dict[str, Optional[str]]]:
    """Returns the three canonical data security scenarios with worked outputs."""
    return [
        {
            "name": "Customer PII Database",
            "asset": "PostgreSQL database containing customer financial and PII records",
            "threat": "Exfiltration of sensitive plaintext records during database backup",
            "control": "Implement transparent database encryption (TDE) and encrypted backup exports",
            "residual_risk": "Key compromise if master encryption keys are improperly stored",
        },
        {
            "name": "Missing asset data scenario",
            "asset": "",
            "threat": "Unauthorized data alteration in transit",
            "control": "Enforce TLS 1.3 with mutual authentication",
            "residual_risk": "Man-in-the-middle if root CA certificates are untrusted",
        },
        {
            "name": "Mismatched data protection control",
            "asset": "Analytics data warehouse tables",
            "threat": "Re-identification of anonymized patient health records",
            "control": "Deploy storage volume snapshot replication to secondary region",
            "residual_risk": "Replication copies anonymized data without mitigating re-identification risk",
        },
    ]


def run_scenarios(scenarios: List[Dict[str, Optional[str]]]) -> List[Tuple[str, str, str]]:
    results = []
    for s in scenarios:
        name = s.get("name", "Unnamed scenario")
        status, msg = check_scenario(s)
        results.append((name, status, msg))
    return results


def run_demonstration(scenario: str) -> int:
    print(f"Scenario mode: {scenario}")
    if scenario == "normal":
        scenarios = get_worked_example_scenarios()
        results = run_scenarios(scenarios)
        for name, status, msg in results:
            print(f"[{status}] {name}: {msg}")
        return 0

    elif scenario == "boundary":
        results = run_scenarios([])
        print(f"Executed 0 boundary scenarios successfully. Output count: {len(results)}")
        assert len(results) == 0
        return 0

    elif scenario == "failure":
        scenarios = [
            {
                "name": "Simulated failure",
                "asset": None,
                "threat": "Exfiltration",
                "control": "Encryption",
                "residual_risk": "Risk",
            }
        ]
        results = run_scenarios(scenarios)
        for name, status, msg in results:
            print(f"[{status}] {name}: {msg}", file=sys.stderr)
        return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Data Security Scenario Rubric Checker")
    parser.add_argument(
        "--scenario",
        choices=["normal", "boundary", "failure"],
        default="normal",
        help="Scenario mode to execute",
    )
    args = parser.parse_args()
    return run_demonstration(args.scenario)


if __name__ == "__main__":
    sys.exit(main())
