"""Check a fictional AI security scenario against a small structural rubric."""

import argparse
from collections.abc import Mapping, Sequence
from typing import Any


LESSON_SECTION = "8.3 Responsible AI: How can I ensure my AI system is both secure and ethical?"
REQUIRED_FIELDS = ("asset", "threat", "control", "residual_risk")
STATE_STAGES = (
    "received",
    "normalized",
    "completeness",
    "control_review",
    "final",
)

SCENARIOS: dict[str, dict[str, str]] = {
    "normal": {
        "lesson_section": LESSON_SECTION,
        "asset": "Fictional customer-support training transcripts",
        "threat": "Personal information could be exposed from the training transcripts.",
        "control": (
            "Remove direct identifiers and limit dataset access to approved staff "
            "because these steps reduce exposure of transcript data."
        ),
        "residual_risk": (
            "Indirect identifiers may remain, and an authorized user could still "
            "misuse an accessible copy."
        ),
        "threat_category": "data_privacy",
        "control_category": "data_privacy",
    },
    "boundary": {
        "lesson_section": LESSON_SECTION,
        "threat": "Personal information could be exposed from the training transcripts.",
        "control": "Remove direct identifiers and limit dataset access.",
        "residual_risk": "Indirect identifiers may remain in the fictional dataset.",
        "threat_category": "data_privacy",
        "control_category": "data_privacy",
    },
    "failure": {
        "lesson_section": LESSON_SECTION,
        "asset": "Fictional fraud-detection model and transaction review queue",
        "threat": "Crafted inputs could evade the model and hide fraudulent transactions.",
        "control": (
            "Encrypt stored training data to reduce unauthorized access to that data."
        ),
        "residual_risk": (
            "Evasion may still occur because encryption at rest does not assess "
            "the model's behavior on crafted inputs."
        ),
        "threat_category": "model_evasion",
        "control_category": "data_privacy",
    },
}


def evaluate_scenario(scenario: Mapping[str, Any]) -> dict[str, Any]:
    """Return a rubric result and a snapshot after each processing step."""
    received = dict(scenario)
    states: list[dict[str, Any]] = [{"stage": "received", "input": received}]

    fields = {
        field: (
            value.strip()
            if isinstance(value, str)
            else ""
        )
        for field in REQUIRED_FIELDS
        if (value := received.get(field)) is not None
    }
    states.append({"stage": "normalized", "fields": fields.copy()})

    missing_fields = [
        field for field in REQUIRED_FIELDS if not fields.get(field)
    ]
    states.append(
        {"stage": "completeness", "missing_fields": missing_fields.copy()}
    )

    threat_category = received.get("threat_category")
    control_category = received.get("control_category")
    if (
        isinstance(threat_category, str)
        and threat_category
        and isinstance(control_category, str)
        and control_category
        and threat_category == control_category
    ):
        control_review = "matched"
        review_reasons: list[str] = []
    else:
        control_review = "review"
        review_reasons = [
            "control category does not match the stated threat category"
        ]
    states.append(
        {
            "stage": "control_review",
            "threat_category": threat_category,
            "control_category": control_category,
            "result": control_review,
            "reasons": review_reasons.copy(),
        }
    )

    status = "FAIL" if missing_fields else "REVIEW" if review_reasons else "PASS"
    final = {
        "scenario": received.get("scenario", "unnamed"),
        "status": status,
        "fields": fields.copy(),
        "missing_fields": missing_fields.copy(),
        "control_review": control_review,
        "review_reasons": review_reasons.copy(),
    }
    states.append({"stage": "final", "result": final.copy()})
    return {"states": states, "final": final}


def final_matches_recorded_state(evaluation: Mapping[str, Any]) -> bool:
    """Recompute the final rubric result from the recorded intermediate states."""
    states = evaluation.get("states")
    if (
        not isinstance(states, list)
        or len(states) != len(STATE_STAGES)
        or any(not isinstance(state, dict) for state in states)
    ):
        return False
    if tuple(state.get("stage") for state in states) != STATE_STAGES:
        return False
    received, normalized, completeness, control_review, final_state = states
    if not isinstance(received.get("input"), Mapping):
        return False
    fields = normalized.get("fields")
    missing_fields = completeness.get("missing_fields")
    review_reasons = control_review.get("reasons")
    if not isinstance(fields, dict) or not isinstance(missing_fields, list):
        return False
    if not isinstance(review_reasons, list):
        return False

    expected_status = (
        "FAIL" if missing_fields else "REVIEW" if review_reasons else "PASS"
    )
    expected_final = {
        "scenario": received["input"].get("scenario", "unnamed"),
        "status": expected_status,
        "fields": fields,
        "missing_fields": missing_fields,
        "control_review": control_review.get("result"),
        "review_reasons": review_reasons,
    }
    return (
        evaluation.get("final") == expected_final
        and final_state.get("result") == expected_final
    )


def format_evaluation(evaluation: Mapping[str, Any]) -> str:
    final = evaluation["final"]
    fields = final["fields"]
    states = " -> ".join(state["stage"] for state in evaluation["states"])
    missing = ", ".join(final["missing_fields"]) or "none"
    reason = "; ".join(final["review_reasons"]) or "none"
    lines = [
        f"Intermediate states: {states}",
        f"Asset: {fields.get('asset') or 'MISSING'}",
        f"Threat: {fields.get('threat') or 'MISSING'}",
        f"Control: {fields.get('control') or 'MISSING'}",
        f"Residual risk: {fields.get('residual_risk') or 'MISSING'}",
        f"Missing fields: {missing}",
        f"Control review: {final['control_review']} ({reason})",
        f"Rubric result: {final['status']}",
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
    if not final_matches_recorded_state(evaluation):
        raise AssertionError("final result does not match the recorded state trace")
    return 1 if evaluation["final"]["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
