"""Apply a small structural rubric to fictional network security answers."""

FIELDS = ("asset", "threat", "control", "residual_risk")
CONTROL_BY_THREAT = {
    "guest network reaches the admin interface": "block guest-to-admin traffic",
    "intercept traffic in transit": "use end-to-end encryption",
}
SCENARIOS = {
    "guest-segment": {
        "asset": "Switch admin interface",
        "threat": "guest network reaches the admin interface",
        "control": "block guest-to-admin traffic",
        "residual_risk": "A device on the admin network can still reach the interface.",
    },
    "missing-asset": {
        "threat": "intercept traffic in transit",
        "control": "use end-to-end encryption",
        "residual_risk": "An attacker who controls an endpoint can still read the data.",
    },
    "mismatched-control": {
        "asset": "Inventory app traffic",
        "threat": "intercept traffic in transit",
        "control": "block guest-to-admin traffic",
        "residual_risk": "Traffic on an allowed path can still be intercepted.",
    },
}


def check_scenario(answer: dict) -> str:
    for field in FIELDS:
        value = answer.get(field)
        if not isinstance(value, str) or not value.strip():
            return f"FAIL ({field} is required)"
    if CONTROL_BY_THREAT.get(answer["threat"].strip()) != answer["control"].strip():
        return "REVIEW (control needs a rationale)"
    return "PASS"


if __name__ == "__main__":
    for name, answer in SCENARIOS.items():
        print(f"{name}: {check_scenario(answer)}")
