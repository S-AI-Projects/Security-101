"""Structural rubric checker for fictional application-security scenarios.

This local example is tied to Module 5 AppSec concepts/capabilities. It checks
asset, threat, control, and residual-risk fields plus a small control/threat
relevance table. Human prose quality is not inferred by this checker.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, Iterable, List, Literal, TypedDict


LESSON_CITATION = "5.3 End of module quiz.md"


class Scenario(TypedDict):
    name: str
    section: str
    asset: str
    threat: str
    control: str
    residual_risk: str


COMPLETE_SCENARIO: Scenario = {
    "name": "Web input",
    "section": "Input Validation",
    "asset": "Customer-profile web form",
    "threat": "malformed or malicious input",
    "control": "server-side allowlist validation",
    "residual_risk": "Unknown payloads may remain and require monitoring",
}

MISSING_ASSET_SCENARIO: Scenario = {
    "name": "Missing asset",
    "section": "Dependency Scanning",
    "asset": "",
    "threat": "vulnerable third-party library",
    "control": "dependency vulnerability scan",
    "residual_risk": "New vulnerabilities may appear before the next scan",
}

UNRELATED_CONTROL_SCENARIO: Scenario = {
    "name": "Unrelated control",
    "section": "Secure APIs",
    "asset": "Partner API",
    "threat": "unauthorized API access",
    "control": "dependency vulnerability scan",
    "residual_risk": "Misconfigured scopes may remain",
}


RELEVANT_CONTROLS: Dict[str, frozenset[str]] = {
    "malformed or malicious input": frozenset({
        "server-side allowlist validation",
        "output encoding",
    }),
    "vulnerable third-party library": frozenset({
        "dependency vulnerability scan",
        "dependency patching",
    }),
    "unauthorized API access": frozenset({
        "authentication",
        "authorization",
        "api scope validation",
    }),
}

EXPLICIT_EXPECTED_TABLE: Dict[str, Literal["pass", "fail", "review"]] = {
    "Web input": "pass",
    "Missing asset": "fail",
    "Unrelated control": "review",
}


def check_scenario(scenario: Scenario) -> Literal["pass", "fail", "review"]:
    """Direct structural rubric implementation."""
    required_fields = ("asset", "threat", "control", "residual_risk")
    if any(not isinstance(scenario.get(field), str) or not scenario[field].strip()
           for field in required_fields):
        return "fail"

    allowed_controls = RELEVANT_CONTROLS.get(scenario["threat"], frozenset())
    if scenario["control"] not in allowed_controls:
        return "review"
    return "pass"


def independent_table_check(scenario: Scenario) -> Literal["pass", "fail", "review"]:
    """Independent lookup against a simple explicit expected-result table."""
    return EXPLICIT_EXPECTED_TABLE.get(scenario["name"], "review")


def compare_direct_and_table(scenarios: Iterable[Scenario]) -> tuple[Dict[str, str], bool]:
    direct: Dict[str, str] = {}
    expected: Dict[str, str] = {}
    for scenario in scenarios:
        direct[scenario["name"]] = check_scenario(scenario)
        expected[scenario["name"]] = independent_table_check(scenario)
    return direct, direct == expected


def run_scenario(scenario_name: str) -> tuple[int, str]:
    fixtures = {
        "complete": COMPLETE_SCENARIO,
        "missing_asset": MISSING_ASSET_SCENARIO,
        "unrelated_control": UNRELATED_CONTROL_SCENARIO,
    }

    if scenario_name == "normal":
        result = check_scenario(COMPLETE_SCENARIO)
        output = (
            f'Scenario: structural rubric based on "{LESSON_CITATION}".\n'
            f"fixture=Web input\n"
            f"asset={COMPLETE_SCENARIO['asset']}\n"
            f"threat={COMPLETE_SCENARIO['threat']}\n"
            f"control={COMPLETE_SCENARIO['control']}\n"
            f"residual_risk={COMPLETE_SCENARIO['residual_risk']}\n"
            f"result={result}"
        )
        return (0, output) if result == "pass" else (1, "Unexpected normal result")

    if scenario_name == "boundary":
        direct, equivalent = compare_direct_and_table(fixtures.values())
        output = (
            f'Scenario: direct/table comparison based on "{LESSON_CITATION}".\n'
            + "\n".join(f"{name}={status}" for name, status in direct.items())
            + f"\ndirect_table_equivalent={str(equivalent).lower()}"
        )
        return (0, output) if equivalent else (1, "Direct implementation differs from table")

    if scenario_name == "failure":
        missing = check_scenario(MISSING_ASSET_SCENARIO)
        unrelated = check_scenario(UNRELATED_CONTROL_SCENARIO)
        output = (
            f'Scenario: rubric failures based on "{LESSON_CITATION}".\n'
            f"Missing asset result={missing}\n"
            f"Unrelated control result={unrelated}"
        )
        expected = missing == "fail" and unrelated == "review"
        return (1, output) if expected else (1, "Unexpected failure fixture result")

    if scenario_name == "explain":
        direct, equivalent = compare_direct_and_table(fixtures.values())
        output = (
            f"Worked fixture for {LESSON_CITATION}\n"
            f"complete={direct['Web input']}\n"
            f"missing_asset={direct['Missing asset']}\n"
            f"unrelated_control={direct['Unrelated control']}\n"
            f"direct_table_equivalent={str(equivalent).lower()}\n"
            "human_explanation_review_required=true"
        )
        return 0, output

    return 1, f"Unknown scenario: {scenario_name}"


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Local structural rubric checker for fictional AppSec scenarios."
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
