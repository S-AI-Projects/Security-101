"""Infrastructure Security Scenario Rubric with Offline Service Adapter (R34-T054).

Extends 6.1 Infrastructure security key concepts.
Decouples scenario sourcing from evaluation via a callable adapter interface.
Provides a deterministic local adapter for offline testing.
"""

from __future__ import annotations

import abc
import argparse
import sys
from typing import Any, Callable, Dict, List, Optional, Tuple

REQUIRED_FIELDS = ("asset", "threat", "control", "residual_risk")

THREAT_CONTROL_KEYWORDS = {
    "unpatched": ["patch", "vulnerability scan", "update", "remediation"],
    "lateral movement": ["segmentation", "micro-segmentation", "firewall", "nsg", "acl"],
    "ransomware": ["backup", "immutable", "air-gap", "endpoint protection", "edr"],
    "unauthorized access": ["iam", "mfa", "rbac", "least privilege", "bastion"],
}


class ScenarioSourceAdapter(abc.ABC):
    """Abstract interface for sourcing infrastructure security scenarios."""

    @abc.abstractmethod
    def fetch_scenarios(self) -> List[Dict[str, Optional[str]]]:
        """Fetch a list of infrastructure scenario records."""
        raise NotImplementedError


class LocalInfrastructureAdapter(ScenarioSourceAdapter):
    """Deterministic offline adapter providing local infrastructure scenarios.

    Note on real-service behavior:
    This mock does NOT establish real cloud provider API behavior (e.g. AWS EC2,
    Azure Resource Manager), live hypervisor metrics, physical server room controls,
    hardware telemetry, or real-time vulnerability scan results.
    """

    def fetch_scenarios(self) -> List[Dict[str, Optional[str]]]:
        return [
            {
                "name": "Cloud compute cluster",
                "asset": "Virtual machine compute cluster",
                "threat": "Unpatched OS vulnerability exploitation",
                "control": "Automated patch management and vulnerability scanning",
                "residual_risk": "Zero-day vulnerabilities prior to vendor patch release",
            },
            {
                "name": "Missing asset infrastructure scenario",
                "asset": "",
                "threat": "Unauthorized lateral movement across subnets",
                "control": "Implement network security group micro-segmentation",
                "residual_risk": "Misconfiguration in security group rules",
            },
            {
                "name": "Mismatched infrastructure control",
                "asset": "Storage area network (SAN) storage volumes",
                "threat": "Ransomware data encryption",
                "control": "Deploy physical security badge readers at server room",
                "residual_risk": "Physical perimeter controls do not prevent network ransomware encryption",
            },
        ]


def check_scenario(scenario: Dict[str, Optional[str]]) -> Tuple[str, str]:
    """Check an infrastructure scenario against the structural rubric."""
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


def evaluate_adapter(adapter: ScenarioSourceAdapter) -> List[Tuple[str, str, str]]:
    """Evaluates scenarios provided by any adapter implementing the interface."""
    scenarios = adapter.fetch_scenarios()
    results = []
    for s in scenarios:
        name = s.get("name", "Unnamed scenario")
        status, msg = check_scenario(s)
        results.append((name, status, msg))
    return results


def run_demonstration(scenario: str) -> int:
    print(f"Scenario mode: {scenario}")
    adapter = LocalInfrastructureAdapter()

    if scenario == "normal":
        results = evaluate_adapter(adapter)
        for name, status, msg in results:
            print(f"[{status}] {name}: {msg}")
        return 0

    elif scenario == "boundary":
        # Boundary case: Custom adapter returning empty scenario list
        class EmptyAdapter(ScenarioSourceAdapter):
            def fetch_scenarios(self):
                return []

        results = evaluate_adapter(EmptyAdapter())
        print(f"Boundary scenario evaluated: {len(results)} records processed.")
        assert len(results) == 0
        return 0

    elif scenario == "failure":
        # Failure case: Adapter raising or scenario missing asset causing failure exit
        class FailingAdapter(ScenarioSourceAdapter):
            def fetch_scenarios(self):
                return [{"name": "Missing asset", "asset": "", "threat": "threat", "control": "control", "residual_risk": "risk"}]

        results = evaluate_adapter(FailingAdapter())
        for name, status, msg in results:
            print(f"[{status}] {name}: {msg}", file=sys.stderr)
        return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Infrastructure Security Rubric with Adapter")
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
