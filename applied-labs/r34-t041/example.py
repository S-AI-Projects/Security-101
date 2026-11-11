"""Check a structural rubric for three fictional infrastructure scenarios."""

REQUIRED_FIELDS = ("asset", "threat", "control", "residual_risk")

THREAT_CONTROLS = {
    "exploit unpatched service": "apply security patch",
    "read public files": "restrict public access",
}

SCENARIOS = {
    "smallest-valid": {
        "asset": "Remote access server",
        "threat": "exploit unpatched service",
        "control": "apply security patch",
        "residual_risk": "A different flaw could still expose the server.",
    },
    "review-boundary": {
        "asset": "Internal reports file store",
        "threat": "read public files",
        "control": "apply security patch",
        "residual_risk": "Anyone can still read files while public access is open.",
    },
    "missing-asset": {
        "threat": "exploit unpatched service",
        "control": "apply security patch",
        "residual_risk": "An attacker may have gained access before the patch.",
    },
}


def check_scenario(scenario):
    """Report whether an answer meets the fixture's structural rubric."""
    for field in REQUIRED_FIELDS:
        value = scenario.get(field)
        if not isinstance(value, str) or not value.strip():
            return f"FAIL ({field} must be non-blank text)"

    threat = scenario["threat"].strip()
    control = scenario["control"].strip()
    if THREAT_CONTROLS.get(threat) != control:
        return "REVIEW (threat and control do not match the rubric)"

    return "PASS"


if __name__ == "__main__":
    for name, scenario in SCENARIOS.items():
        print(f"{name}: {check_scenario(scenario)}")
