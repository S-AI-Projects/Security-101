def check_scenario(scenario):
    """Check whether a cybersecurity scenario has all required fields."""

    required_fields = [
        "asset",
        "threat",
        "control",
        "residual_risk"
    ]

    missing_fields = []

    for field in required_fields:
        if not scenario.get(field):
            missing_fields.append(field)

    if missing_fields:
        return {
            "status": "FAIL",
            "missing_fields": missing_fields
        }

    return {
        "status": "PASS",
        "missing_fields": []
    }



def check_control_match(scenario):
    """Flag controls that may not match the named threat."""

    threat = scenario.get("threat", "").lower()
    control = scenario.get("control", "").lower()

    control_hints = {
        "phishing": ["awareness", "email filtering", "multi-factor"],
        "unauthorized access": ["access control", "multi-factor", "authentication"],
        "physical theft": ["lock", "cctv", "security guard"]
    }

    for threat_name, keywords in control_hints.items():
        if threat_name in threat:
            if any(word in control for word in keywords):
                return "MATCH"
            return "REVIEW"

    return "REVIEW"



scenarios = [
    {
        "name": "College portal",
        "lesson_section": "1.3 Understanding risk management",
        "asset": "Student records",
        "threat": "unauthorized access",
        "control": "access control and multi-factor authentication",
        "residual_risk": "An authorized account could still be misused."
    },
    {
    "name": "College email",
    "lesson_section": "1.3 Understanding risk management",
    "asset": "College email accounts",
    "threat": "phishing",
    "control": "email filtering and awareness training",
    "residual_risk": "Some phishing emails may still reach students."
},
    {
        "name": "Computer lab",
        "lesson_section": "1.3 Understanding risk management",
        "asset": "College email accounts",
        "asset": "Lab computers",
        "threat": "physical theft",
        "control": "password awareness training",
        "residual_risk": "Computers may still be stolen."
    }
]

if __name__ == "__main__":
    for scenario in scenarios:
        print("\nScenario:", scenario["name"])
        print("Completeness:", check_scenario(scenario))
        print("Control check:", check_control_match(scenario))

