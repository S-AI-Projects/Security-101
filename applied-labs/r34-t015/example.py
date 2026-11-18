"""Check fictional data-security scenarios against a structural rubric."""

import argparse
from collections.abc import Mapping, Sequence
from typing import Any


LESSON_SECTION = "7.1 Data security key concepts: What is data loss prevention (DLP)?"
REQUIRED_FIELDS = ("asset", "threat", "control", "residual_risk")
SCENARIOS: dict[str, dict[str, str]] = {
    "normal": {
        "lesson_section": LESSON_SECTION,
        "asset": "Fictional customer invoice files",
        "threat": "A restricted invoice could be sent to an unauthorized external recipient.",
        "control": (
            "Inspect outbound email for restricted invoice content and warn or block "
            "unapproved external sharing."
        ),
        "residual_risk": (
            "A renamed or otherwise unrecognized attachment could evade inspection."
        ),
        "threat_category": "data_exfiltration",
        "control_category": "data_exfiltration",
    },
    "boundary": {
        "lesson_section": LESSON_SECTION,
        "threat": "A restricted invoice could be sent to an unauthorized external recipient.",
        "control": "Inspect outbound email and block unapproved sharing.",
        "residual_risk": "Unrecognized attachment formats could evade inspection.",
        "threat_category": "data_exfiltration",
        "control_category": "data_exfiltration",
    },
    "failure": {
        "lesson_section": LESSON_SECTION,
        "asset": "Fictional employee payroll records",
        "threat": "Payroll data could be exposed through an unauthorized external email.",
        "control": "Test backup restoration to reduce downtime after data loss.",
        "residual_risk": (
            "A successful restore does not prevent payroll data from being emailed "
            "to an unauthorized recipient."
        ),
        "threat_category": "data_exfiltration",
        "control_category": "availability",
    },
}


def review_control_alignment(
    threat_category: object,
    control_category: object,
) -> tuple[str, list[str]]:
    """Assess only whether the supplied threat and control categories agree."""
    if (
        isinstance(threat_category, str)
        and threat_category
        and isinstance(control_category, str)
        and control_category
        and threat_category == control_category
    ):
        return "matched", []
    return "review", [
        "control category does not match the stated threat category"
    ]


def evaluate_scenario(scenario: Mapping[str, Any]) -> dict[str, Any]:
    """Validate required answer fields and the declared control category."""
    fields = {
        field: value.strip() if isinstance(value, str) else ""
        for field in REQUIRED_FIELDS
        if (value := scenario.get(field)) is not None
    }
    missing_fields = [field for field in REQUIRED_FIELDS if not fields.get(field)]

    control_review, review_reasons = review_control_alignment(
        scenario.get("threat_category"),
        scenario.get("control_category"),
    )

    status = "FAIL" if missing_fields else "REVIEW" if review_reasons else "PASS"
    return {
        "scenario": scenario.get("scenario", "unnamed"),
        "status": status,
        "fields": fields,
        "missing_fields": missing_fields,
        "control_review": control_review,
        "review_reasons": review_reasons,
    }


def format_evaluation(evaluation: Mapping[str, Any]) -> str:
    fields = evaluation["fields"]
    missing = ", ".join(evaluation["missing_fields"]) or "none"
    reasons = "; ".join(evaluation["review_reasons"]) or "none"
    lines = [
        f"Asset: {fields.get('asset') or 'MISSING'}",
        f"Threat: {fields.get('threat') or 'MISSING'}",
        f"Control: {fields.get('control') or 'MISSING'}",
        f"Residual risk: {fields.get('residual_risk') or 'MISSING'}",
        f"Missing fields: {missing}",
        f"Control review: {evaluation['control_review']} ({reasons})",
        f"Rubric result: {evaluation['status']}",
    ]
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario",
        choices=tuple(SCENARIOS),
        default="normal",
        help="check the complete, missing-asset, or unrelated-control mock scenario",
    )
    arguments = parser.parse_args(argv)
    scenario = dict(SCENARIOS[arguments.scenario], scenario=arguments.scenario)
    evaluation = evaluate_scenario(scenario)

    print(f"Scenario: {arguments.scenario} (local fictional mock)")
    print(format_evaluation(evaluation))
    return 1 if evaluation["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
