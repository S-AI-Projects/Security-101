"""Classify security incidents by CIA triad impacts and compare two evaluation approaches."""

from typing import Any

# CIA property definitions
CONFIDENTIALITY = "confidentiality"
INTEGRITY = "integrity"
AVAILABILITY = "availability"

ALL_PROPERTIES = {CONFIDENTIALITY, INTEGRITY, AVAILABILITY}

# Rule-based indicators for direct classification
INDICATORS = {
    CONFIDENTIALITY: {
        "unauthorized reading",
        "data exfiltration",
        "credential dumping",
        "viewing private files",
    },
    INTEGRITY: {
        "altered records",
        "unauthorized modification",
        "tampering",
        "file corruption",
    },
    AVAILABILITY: {
        "unavailable service",
        "denial of service",
        "system outage",
        "resource exhaustion",
    },
}

# Standard test fixtures representing distinct single and multi-impact scenarios
SCENARIOS: dict[str, dict[str, Any]] = {
    "unauthorized-reading": {
        "title": "Exposure of customer records",
        "events": ["unauthorized reading"],
        "expected": {CONFIDENTIALITY},
    },
    "altered-records": {
        "title": "Modification of financial transaction database",
        "events": ["altered records"],
        "expected": {INTEGRITY},
    },
    "unavailable-service": {
        "title": "Distributed network flood causing portal downtime",
        "events": ["unavailable service"],
        "expected": {AVAILABILITY},
    },
    "multi-confidentiality-integrity": {
        "title": "Attacker exfiltrates patient history and modifies prescription records",
        "events": ["unauthorized reading", "altered records"],
        "expected": {CONFIDENTIALITY, INTEGRITY},
    },
    "multi-integrity-availability": {
        "title": "Ransomware corrupts critical configuration files and halts billing service",
        "events": ["file corruption", "system outage"],
        "expected": {INTEGRITY, AVAILABILITY},
    },
    "multi-all-triad": {
        "title": "Total compromise: data breach, database tampering, and server shutdown",
        "events": ["data exfiltration", "altered records", "unavailable service"],
        "expected": {CONFIDENTIALITY, INTEGRITY, AVAILABILITY},
    },
    "benign-activity": {
        "title": "Scheduled maintenance and routine audit read",
        "events": [],
        "expected": set(),
    },
}


def classify_direct(scenario: dict[str, Any]) -> set[str]:
    """Approach 1: Direct indicator-matching classifier.

    Iterates through recorded event indicators and matches them against CIA rules.
    Retains all matching properties for multi-impact scenarios.
    """
    events = scenario.get("events", [])
    impacts: set[str] = set()

    for event in events:
        event_lower = str(event).strip().lower()
        for prop, indicators in INDICATORS.items():
            if event_lower in indicators:
                impacts.add(prop)

    return impacts


def classify_reference(scenario_key: str) -> set[str]:
    """Approach 2: Independent reference lookup from benchmark ground-truth table."""
    fixture = SCENARIOS.get(scenario_key)
    if fixture is None:
        raise KeyError(f"Unknown scenario key: '{scenario_key}'")
    return set(fixture.get("expected", set()))


def compare_approaches(scenario_key: str) -> dict[str, Any]:
    """Compare direct classification with reference approach on identical input.

    Returns comparison report with agreement status and impact sets.
    """
    scenario = SCENARIOS[scenario_key]
    direct_result = classify_direct(scenario)
    ref_result = classify_reference(scenario_key)

    agreed = direct_result == ref_result
    return {
        "scenario": scenario_key,
        "direct_impacts": sorted(direct_result),
        "reference_impacts": sorted(ref_result),
        "agreed": agreed,
    }


def run_all_scenarios() -> list[dict[str, Any]]:
    """Execute classification and comparison across all defined fixtures."""
    reports = []
    for key in SCENARIOS:
        reports.append(compare_approaches(key))
    return reports


if __name__ == "__main__":
    for report in run_all_scenarios():
        name = report["scenario"]
        direct = report["direct_impacts"] or ["none"]
        ref = report["reference_impacts"] or ["none"]
        agree = "AGREED" if report["agreed"] else "DISAGREED"
        print(f"{name}: direct={','.join(direct)}, reference={','.join(ref)}, match={agree}")
