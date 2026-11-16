import json
from pathlib import Path

FIXTURE = Path(__file__).with_name("scenarios.json")

CONTROL_HINTS = {
    "phishing": ("multi-factor", "email filtering", "email security"),
    "ransomware": ("backup", "endpoint protection", "anti-malware"),
    "unauthorized access": ("access control", "authentication", "multi-factor"),
}

REQUIRED = ("asset", "threat", "control", "residual_risk")


def check_scenario(scenario):
    missing = [
        field for field in REQUIRED
        if not isinstance(scenario.get(field), str)
        or not scenario[field].strip()
    ]

    if missing:
        return {
            "id": scenario.get("id", "unknown"),
            "status": "FAIL",
            "message": "Missing required fields: " + ", ".join(missing)
        }

    threat = scenario["threat"].lower()
    control = scenario["control"].lower()

    matching_hints = next(
        (hints for name, hints in CONTROL_HINTS.items() if name in threat),
        None
    )

    if matching_hints and not any(hint in control for hint in matching_hints):
        return {
            "id": scenario["id"],
            "status": "REVIEW",
            "message": "Control may be unrelated to the named threat; human review required."
        }

    return {
        "id": scenario["id"],
        "status": "PASS",
        "message": "Required fields complete; control matches the structural rubric."
    }


def main():
    scenarios = json.loads(FIXTURE.read_text())
    for scenario in scenarios:
        print(json.dumps(check_scenario(scenario)))


if __name__ == "__main__":
    main()
