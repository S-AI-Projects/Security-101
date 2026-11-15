
def local_relevance_adapter(threat, control):
    """
    Deterministic local mock for checking whether a control
    appears related to a threat.
    This is not a real external review service.
    """
    relationships = {
        "unauthorized access": ["multi-factor authentication", "access control"],
        "ransomware": ["offline backups", "immutable backups"],
        "phishing": ["email filtering", "security awareness training"]
    }

    threat_key = threat.lower()
    control_text = control.lower()

    expected_controls = relationships.get(threat_key, [])

    return any(
        expected in control_text
        for expected in expected_controls
    )


def check_scenario(scenario, relevance_checker):
    """
    Check the structural rubric and request a control relevance check.
    """

    required_fields = [
        "asset",
        "threat",
        "control",
        "residual_risk"
    ]

    # Check that every required field exists and has content.
    for field in required_fields:
        if not scenario.get(field) or not scenario[field].strip():
            return {
                "status": "FAIL",
                "reason": f"Missing or empty field: {field}"
            }

    # Put the external dependency behind a callable interface.
    related = relevance_checker(
        scenario["threat"],
        scenario["control"]
    )

    if not related:
        return {
            "status": "REVIEW",
            "reason": "Control may be unrelated to the named threat."
        }

    return {
        "status": "PASS",
        "reason": "All structural checks passed."
    }


# Three fictional security scenarios.
scenarios = {
    "complete": {
        "asset": "Customer records",
        "threat": "unauthorized access",
        "control": "Multi-factor authentication and access control",
        "residual_risk": "A compromised authorized account may still be misused."
    },

    "missing_asset": {
        "asset": "",
        "threat": "ransomware",
        "control": "Offline backups and immutable backups",
        "residual_risk": "Some recent data may not be recoverable."
    },

    "unrelated_control": {
        "asset": "Employee email accounts",
        "threat": "phishing",
        "control": "Physical server room locks",
        "residual_risk": "Employees may still respond to deceptive messages."
    }
}


if __name__ == "__main__":
    for name, scenario in scenarios.items():
        result = check_scenario(
            scenario,
            local_relevance_adapter
        )

        print(f"{name}: {result['status']} - {result['reason']}")
