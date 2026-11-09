from example import (
    scenarios,
    check_scenario,
    check_control_match
)

# Expected results written independently
expected_results = {
    "College portal": ("PASS", "MATCH"),
    "College email": ("PASS", "MATCH"),
    "Computer lab": ("PASS", "REVIEW")
}

all_passed = True

for scenario in scenarios:
    name = scenario["name"]

    actual_status = check_scenario(scenario)["status"]
    actual_control = check_control_match(scenario)

    actual = (actual_status, actual_control)
    expected = expected_results[name]

    print(f"\nScenario: {name}")
    print("Expected:", expected)
    print("Actual:  ", actual)

    if actual != expected:
        print("RESULT: FAIL")
        all_passed = False
    else:
        print("RESULT: PASS")

if not all_passed:
    raise SystemExit("Comparison failed!")

print("\nAll expected results match.")
