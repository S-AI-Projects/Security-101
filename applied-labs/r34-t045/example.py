"""Check fictional infrastructure answers with a local control catalog."""

from collections.abc import Callable

FIELDS = ("asset", "threat", "control", "residual_risk")
CONTROL_CATALOG = {
    "public read access": "block public reads",
    "exploit a known service flaw": "patch the affected service",
}

SCENARIOS = {
    "public-store": {
        "asset": "Report bucket",
        "threat": "public read access",
        "control": "block public reads",
        "residual_risk": "An authorized account can still share a copy.",
    },
    "missing-asset": {
        "threat": "exploit a known service flaw",
        "control": "patch the affected service",
        "residual_risk": "The flaw may have been exploited before the patch.",
    },
    "wrong-control": {
        "asset": "Remote access server",
        "threat": "exploit a known service flaw",
        "control": "block public reads",
        "residual_risk": "The unpatched service can still be exploited.",
    },
}


def lookup_local_control(threat: str) -> str | None:
    """Simulate a catalog lookup with fixed local data."""
    return CONTROL_CATALOG.get(threat)


def check_scenario(answer: dict, lookup: Callable[[str], str | None]) -> str:
    for field in FIELDS:
        value = answer.get(field)
        if not isinstance(value, str) or not value.strip():
            return f"FAIL (missing or invalid {field})"

    expected = lookup(answer["threat"].strip())
    if expected != answer["control"].strip():
        return "REVIEW (no matching control)"
    return "PASS"


if __name__ == "__main__":
    for name, answer in SCENARIOS.items():
        print(f"{name}: {check_scenario(answer, lookup_local_control)}")
