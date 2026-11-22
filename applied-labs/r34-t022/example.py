"""Boundary-focused structural rubric for fictional infrastructure scenarios.

This local mock supports 6.2 lesson concepts: vulnerability management, CSPM,
and CNAPP. It checks structure only; human review judges explanation quality.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, List, Literal, TypedDict


LESSON_CITATION = "6.2 Infrastructure security capabilities.md"


class Scenario(TypedDict):
    name: str
    section: str
    asset: str
    threat: str
    control: str
    residual_risk: str


SMALLEST_VALID: Scenario = {
    "name": "Smallest valid",
    "section": "Vulnerability Management",
    "asset": "Server",
    "threat": "known server vulnerability",
    "control": "apply vendor patch",
    "residual_risk": "zero-day risk remains",
}

# Boundary: every field is present, but control uses a non-empty string that
# belongs to a different threat category, so this exact case is review.
BOUNDARY_CONTROL: Scenario = {
    "name": "Boundary control",
    "section": "CSPM",
    "asset": "Cloud storage bucket",
    "threat": "public cloud misconfiguration",
    "control": "container image patch",
    "residual_risk": "policy drift may recur",
}

INVALID_NO_ASSET: Scenario = {
    "name": "Missing asset",
    "section": "CNAPP",
    "asset": "",
    "threat": "cloud workload vulnerability",
    "control": "runtime workload protection",
    "residual_risk": "unknown workloads may remain",
}


THREAT_CONTROL_MAP: Dict[str, frozenset[str]] = {
    "known server vulnerability": frozenset({"apply vendor patch", "network segmentation"}),
    "public cloud misconfiguration": frozenset({"remediate insecure cloud configuration"}),
    "cloud workload vulnerability": frozenset({"runtime workload protection", "container patch"}),
}


def check_scenario(scenario: Scenario) -> Literal["pass", "fail", "review"]:
    """Apply exact structural boundary: empty required field is fail."""
    required = ("asset", "threat", "control", "residual_risk")
    if any(not isinstance(scenario.get(field), str) or not scenario[field].strip()
           for field in required):
        return "fail"

    # At the exact boundary, a non-empty but unrelated control is review.
    if scenario["control"] not in THREAT_CONTROL_MAP.get(scenario["threat"], frozenset()):
        return "review"
    return "pass"


def run_scenario(scenario_name: str) -> tuple[int, str]:
    fixtures = (SMALLEST_VALID, BOUNDARY_CONTROL, INVALID_NO_ASSET)

    if scenario_name == "normal":
        result = check_scenario(SMALLEST_VALID)
        output = (
            f'Scenario: smallest-valid rubric based on "{LESSON_CITATION}".\n'
            f"fixture={SMALLEST_VALID['name']}\n"
            f"asset={SMALLEST_VALID['asset']}\n"
            f"threat={SMALLEST_VALID['threat']}\n"
            f"control={SMALLEST_VALID['control']}\n"
            f"residual_risk={SMALLEST_VALID['residual_risk']}\n"
            f"result={result}"
        )
        return (0, output) if result == "pass" else (1, "Unexpected normal result")

    if scenario_name == "boundary":
        results = {scenario["name"]: check_scenario(scenario) for scenario in fixtures}
        output = (
            f'Scenario: smallest-valid/boundary/invalid based on "{LESSON_CITATION}".\n'
            f"Smallest valid={results['Smallest valid']}\n"
            f"Boundary control={results['Boundary control']}\n"
            f"Missing asset={results['Missing asset']}\n"
            "Boundary decision=non-empty unrelated control is review; empty required field is fail"
        )
        expected = results == {
            "Smallest valid": "pass",
            "Boundary control": "review",
            "Missing asset": "fail",
        }
        return (0, output) if expected else (1, "Unexpected boundary decisions")

    if scenario_name == "failure":
        missing = check_scenario(INVALID_NO_ASSET)
        unrelated = check_scenario(BOUNDARY_CONTROL)
        output = (
            f'Scenario: invalid/boundary fixtures based on "{LESSON_CITATION}".\n'
            f"Missing asset result={missing}\n"
            f"Boundary control result={unrelated}"
        )
        return 1, output

    if scenario_name == "explain":
        results = {scenario["name"]: check_scenario(scenario) for scenario in fixtures}
        output = (
            f"Worked fixture for {LESSON_CITATION}\n"
            f"smallest_valid={results['Smallest valid']}\n"
            f"boundary_control={results['Boundary control']}\n"
            f"invalid_missing_asset={results['Missing asset']}\n"
            "boundary_rule=empty required field -> fail; non-empty unrelated control -> review\n"
            "human_explanation_review_required=true"
        )
        return 0, output

    return 1, f"Unknown scenario: {scenario_name}"


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Boundary-focused infrastructure scenario structural rubric."
    )
    parser.add_argument(
        "--scenario",
        choices=["normal", "boundary", "failure", "explain"],
        default="normal",
    )
    args = parser.parse_args(argv)
    exit_code, output = run_scenario(args.scenario)
    print(output, file=sys.stderr if exit_code != 0 else sys.stdout)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
