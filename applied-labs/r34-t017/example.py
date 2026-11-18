"""Check fictional threat scenarios and recover after an incomplete record."""

import argparse
from collections.abc import Mapping, Sequence
import sys
from typing import Any


LESSON_SECTION = "1.2 Common cybersecurity threats: What are the most common types?"
REQUIRED_FIELDS = ("asset", "threat", "control", "residual_risk")
SCENARIOS: dict[str, dict[str, str]] = {
    "normal": {
        "lesson_section": LESSON_SECTION,
        "asset": "Fictional employee mailbox credentials",
        "threat": "A phishing message tricks an employee into disclosing a password.",
        "control": (
            "Verify unexpected sender requests and require multi-factor "
            "authentication for mailbox access."
        ),
        "residual_risk": (
            "A stolen active session may still be misused before it is revoked."
        ),
        "threat_category": "credential_theft",
        "control_category": "credential_theft",
    },
    "boundary": {
        "lesson_section": LESSON_SECTION,
        "threat": "Ransomware encrypts files in a shared project folder.",
        "control": "Keep tested offline backups to restore affected files.",
        "residual_risk": "Recent changes may be lost between backups.",
        "threat_category": "ransomware",
        "control_category": "ransomware",
    },
    "failure": {
        "lesson_section": LESSON_SECTION,
        "asset": "Fictional public appointment-booking service",
        "threat": "A DDoS attack makes the booking service unavailable.",
        "control": "Rotate employee passwords on a schedule.",
        "residual_risk": (
            "Password rotation does not reduce the incoming traffic that exhausts "
            "the service."
        ),
        "threat_category": "availability",
        "control_category": "credential_theft",
    },
}

# This boundary fixture intentionally omits the required asset field.
RECOVERY_INPUTS = (SCENARIOS["boundary"], SCENARIOS["normal"])


def evaluate_scenario(scenario: Mapping[str, Any]) -> dict[str, Any]:
    """Check completeness and declared threat/control category consistency."""
    fields = {
        field: value.strip() if isinstance(value, str) else ""
        for field in REQUIRED_FIELDS
        if (value := scenario.get(field)) is not None
    }
    missing_fields = [field for field in REQUIRED_FIELDS if not fields.get(field)]

    threat_category = scenario.get("threat_category")
    control_category = scenario.get("control_category")
    categories_match = (
        isinstance(threat_category, str)
        and bool(threat_category)
        and isinstance(control_category, str)
        and bool(control_category)
        and threat_category == control_category
    )
    if categories_match:
        control_review = "matched"
        review_reasons: list[str] = []
    else:
        control_review = "review"
        review_reasons = [
            "control category does not match the stated threat category"
        ]

    status = "FAIL" if missing_fields else "REVIEW" if review_reasons else "PASS"
    return {
        "status": status,
        "fields": fields,
        "missing_fields": missing_fields,
        "control_review": control_review,
        "review_reasons": review_reasons,
    }


def evaluate_recovery_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    """Process an incomplete scenario, then evaluate the following valid one."""
    failed = evaluate_scenario(RECOVERY_INPUTS[0])
    recovered = evaluate_scenario(RECOVERY_INPUTS[1])
    return failed, recovered


def format_evaluation(evaluation: Mapping[str, Any]) -> str:
    fields = evaluation["fields"]
    missing = ", ".join(evaluation["missing_fields"]) or "none"
    reasons = "; ".join(evaluation["review_reasons"]) or "none"
    return "\n".join(
        (
            f"Asset: {fields.get('asset') or 'MISSING'}",
            f"Threat: {fields.get('threat') or 'MISSING'}",
            f"Control: {fields.get('control') or 'MISSING'}",
            f"Residual risk: {fields.get('residual_risk') or 'MISSING'}",
            f"Missing fields: {missing}",
            f"Control review: {evaluation['control_review']} ({reasons})",
            f"Rubric result: {evaluation['status']}",
        )
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario",
        choices=("normal", "boundary", "failure", "recovery"),
        default="normal",
        help="run a complete, incomplete, mismatched-control, or recovery case",
    )
    arguments = parser.parse_args(argv)

    if arguments.scenario == "recovery":
        failed, recovered = evaluate_recovery_inputs()
        missing_field = failed["missing_fields"][0]
        print("Scenario: recovery (local fictional mock)")
        print("Input 1: boundary (incomplete)")
        print(f"Error: missing required field {missing_field!r}")
        print(f"Result 1: {failed['status']}")
        print("Input 2: normal (valid)")
        print(f"Result 2: {recovered['status']}")
        print("Recovery: next valid input accepted")
        return 0 if failed["status"] == "FAIL" and recovered["status"] == "PASS" else 1

    scenario = SCENARIOS[arguments.scenario]
    evaluation = evaluate_scenario(scenario)
    print(f"Scenario: {arguments.scenario} (local fictional mock)")
    print(format_evaluation(evaluation), flush=True)
    if evaluation["status"] == "FAIL":
        print(
            "Error: missing required field(s): "
            + ", ".join(evaluation["missing_fields"]),
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
