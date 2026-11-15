
import json


def record_state(trace, stage, status, reason):
    """Save a snapshot of the scenario's intermediate state."""
    trace.append({
        "stage": stage,
        "status": status,
        "reason": reason
    })


def evaluate_scenario(scenario):
    trace = []

    record_state(trace, "received", "PENDING", "Scenario received")

    required_fields = [
        "lesson_section",
        "asset",
        "threat",
        "control",
        "residual_risk"
    ]

    missing_fields = [
        field for field in required_fields
        if not str(scenario.get(field, "")).strip()
    ]

    if missing_fields:
        reason = "Missing required fields: " + ", ".join(missing_fields)
        record_state(trace, "fields_validated", "FAIL", reason)
        record_state(trace, "finalized", "FAIL", reason)

        return {
            "scenario_id": scenario.get("id", "unknown"),
            "status": trace[-1]["status"],
            "reason": trace[-1]["reason"],
            "trace": trace
        }

    record_state(
        trace,
        "fields_validated",
        "PASS",
        "All required fields are present"
    )

    # Simple local keyword rules.
    # This is a mock consistency check, not an expert security review.
    control_rules = {
        "sql injection": ["parameterized queries", "input validation"],
        "cross-site scripting": ["output encoding"],
        "vulnerable dependency": ["dependency scanning", "sast"]
    }

    threat = scenario["threat"].lower()
    control = scenario["control"].lower()

    matching_controls = None

    for threat_name, controls in control_rules.items():
        if threat_name in threat:
            matching_controls = controls
            break

    if matching_controls is None:
        status = "REVIEW"
        reason = "Threat is not covered by the local keyword rules"

    elif any(item in control for item in matching_controls):
        status = "PASS"
        reason = "Control matches the named threat"

    else:
        status = "REVIEW"
        reason = "Control may be unrelated to the named threat"

    record_state(trace, "consistency_checked", status, reason)
    record_state(trace, "finalized", status, reason)

    return {
        "scenario_id": scenario.get("id", "unknown"),
        "status": trace[-1]["status"],
        "reason": trace[-1]["reason"],
        "trace": trace
    }


def main():
    with open("applied-labs/r34-t034/scenarios.json") as file:
        scenarios = json.load(file)

    results = []

    for scenario in scenarios:
        result = evaluate_scenario(scenario)
        results.append(result)

        print(
            f'{result["scenario_id"]}: '
            f'{result["status"]} - {result["reason"]}'
        )

    print("\nSimulation complete.")
    print(f"Scenarios checked: {len(results)}")


if __name__ == "__main__":
    main()
