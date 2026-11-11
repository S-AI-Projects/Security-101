"""Check three fictional identity and access management answers."""

FIELDS = ("asset", "threat", "control", "residual_risk")
CONTROL_BY_THREAT = {
    "sign in with a stolen password": "require phishing-resistant MFA",
    "keep access after a contract ends": "remove stale role assignments",
}
SCENARIOS = {
    "stolen-password": {
        "asset": "Help desk account",
        "threat": "sign in with a stolen password",
        "control": "require phishing-resistant MFA",
        "residual_risk": "An attacker could still steal an active session token.",
    },
    "missing-asset": {
        "threat": "keep access after a contract ends",
        "control": "remove stale role assignments",
        "residual_risk": "A separate account might still have access.",
    },
    "stale-access": {
        "asset": "Payroll reports",
        "threat": "keep access after a contract ends",
        "control": "require phishing-resistant MFA",
        "residual_risk": "A former contractor can still use the assigned role.",
    },
}


def check_scenario(answer: dict) -> str:
    """Check required text and compare the threat and control with the fixture."""
    for field in FIELDS:
        value = answer.get(field)
        if not isinstance(value, str) or not value.strip():
            return f"FAIL (provide {field})"
    if CONTROL_BY_THREAT.get(answer["threat"].strip()) != answer["control"].strip():
        return "REVIEW (control does not match the threat)"
    return "PASS"


if __name__ == "__main__":
    for name, answer in SCENARIOS.items():
        print(f"{name}: {check_scenario(answer)}")
