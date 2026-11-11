"""Check an AppSec answer and show how to recover from a missing field."""

REQUIRED = ("asset", "threat", "control", "residual_risk")
EXPECTED_CONTROL = {
    "inject SQL through a search field": "use parameterized queries",
    "inject script through a review comment": "encode text for the HTML context",
}

COMPLETE = {
    "asset": "Catalog search database",
    "threat": "inject SQL through a search field",
    "control": "use parameterized queries",
    "residual_risk": "Other query paths may still build SQL from raw input.",
}
SCENARIOS = {
    "missing-asset": {
        "threat": "inject SQL through a search field",
        "control": "use parameterized queries",
        "residual_risk": "Other query paths may still build SQL from raw input.",
    },
    "corrected": COMPLETE,
    "unrelated-control": {
        "asset": "Product review page",
        "threat": "inject script through a review comment",
        "control": "use parameterized queries",
        "residual_risk": "A review can still contain a script that runs in a browser.",
    },
}


def check_scenario(answer: dict) -> str:
    for field in REQUIRED:
        value = answer.get(field)
        if not isinstance(value, str) or not value.strip():
            return f"FAIL (provide {field})"
    if EXPECTED_CONTROL.get(answer["threat"].strip()) != answer["control"].strip():
        return "REVIEW (check threat and control)"
    return "PASS"


if __name__ == "__main__":
    for name, answer in SCENARIOS.items():
        print(f"{name}: {check_scenario(answer)}")
