"""Minimal structural rubric for fictional AI-security scenarios (R34-T021).

The fixture is local and deterministic. It illustrates asset/threat/control/
residual-risk evidence for named Module 8 lesson concepts. It does not assess
real AI behavior or grade prose quality.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, List, Literal, TypedDict


LESSON_CITATION = "8.4 End of module quiz.md"


class Scenario(TypedDict):
    name: str
    section: str
    asset: str
    threat: str
    control: str
    residual_risk: str


COMPLETE_SCENARIO: Scenario = {
    "name": "Training data",
    "section": "Data Integrity",
    "asset": "Training dataset",
    "threat": "unauthorized data modification",
    "control": "data integrity validation",
    "residual_risk": "Novel manipulation patterns may remain",
}

MISSING_ASSET_SCENARIO: Scenario = {
    "name": "Missing asset",
    "section": "Adversarial Attacks",
    "asset": "",
    "threat": "adversarial input",
    "control": "adversarial robustness testing",
    "residual_risk": "Unknown perturbations may remain",
}

UNRELATED_CONTROL_SCENARIO: Scenario = {
    "name": "Unrelated control",
    "section": "Responsible AI",
    "asset": "Loan recommendation system",
    "threat": "biased automated decision",
    "control": "runtime model inventory",
    "residual_risk": "Remaining bias may require review",
}


THREAT_CONTROLS: Dict[str, frozenset[str]] = {
    "unauthorized data modification": frozenset({
        "data integrity validation",
        "signed data provenance",
    }),
    "adversarial input": frozenset({
        "adversarial robustness testing",
        "input normalization",
    }),
    "biased automated decision": frozenset({
        "human oversight",
        "bias testing",
        "explainability review",
    }),
}


def check_scenario(scenario: Scenario) -> Literal["pass", "fail", "review"]:
    """Check the minimal structural rubric and threat/control consistency."""
    required = ("asset", "threat", "control", "residual_risk")
    if any(not isinstance(scenario.get(field), str) or not scenario[field].strip()
           for field in required):
        return "fail"

    allowed = THREAT_CONTROLS.get(scenario["threat"], frozenset())
    if scenario["control"] not in allowed:
        return "review"
    return "pass"


def run_scenario(scenario_name: str) -> tuple[int, str]:
    fixtures = {
        "complete": COMPLETE_SCENARIO,
        "missing_asset": MISSING_ASSET_SCENARIO,
        "unrelated_control": UNRELATED_CONTROL_SCENARIO,
    }

    if scenario_name == "normal":
        result = check_scenario(COMPLETE_SCENARIO)
        output = (
            f'Scenario: AI-security rubric based on "{LESSON_CITATION}".\n'
            f"section={COMPLETE_SCENARIO['section']}\n"
            f"asset={COMPLETE_SCENARIO['asset']}\n"
            f"threat={COMPLETE_SCENARIO['threat']}\n"
            f"control={COMPLETE_SCENARIO['control']}\n"
            f"residual_risk={COMPLETE_SCENARIO['residual_risk']}\n"
            f"result={result}"
        )
        return (0, output) if result == "pass" else (1, "Unexpected normal result")

    if scenario_name == "boundary":
        results = {
            name: check_scenario(scenario)
            for name, scenario in fixtures.items()
        }
        output = (
            f'Scenario: AI-security boundary fixtures based on "{LESSON_CITATION}".\n'
            f"complete={results['complete']}\n"
            f"missing_asset={results['missing_asset']}\n"
            f"unrelated_control={results['unrelated_control']}\n"
            "boundary_decision=empty required field is fail; unrelated control is review"
        )
        expected = results == {
            "complete": "pass",
            "missing_asset": "fail",
            "unrelated_control": "review",
        }
        return (0, output) if expected else (1, "Unexpected boundary results")

    if scenario_name == "failure":
        missing = check_scenario(MISSING_ASSET_SCENARIO)
        unrelated = check_scenario(UNRELATED_CONTROL_SCENARIO)
        output = (
            f'Scenario: rubric failures based on "{LESSON_CITATION}".\n'
            f"Missing asset result={missing}\n"
            f"Unrelated control result={unrelated}"
        )
        return 1, output

    if scenario_name == "explain":
        output = (
            f"Worked fixture for {LESSON_CITATION}\n"
            f"complete={check_scenario(COMPLETE_SCENARIO)}\n"
            f"missing_asset={check_scenario(MISSING_ASSET_SCENARIO)}\n"
            f"unrelated_control={check_scenario(UNRELATED_CONTROL_SCENARIO)}\n"
            "human_explanation_review_required=true"
        )
        return 0, output

    return 1, f"Unknown scenario: {scenario_name}"


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Local structural rubric for fictional AI-security scenarios."
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
