
from example import scenarios, check_scenario, local_relevance_adapter

expected = {
    "complete": "PASS",
    "missing_asset": "FAIL",
    "unrelated_control": "REVIEW"
}

all_passed = True

for name, scenario in scenarios.items():
    actual = check_scenario(scenario, local_relevance_adapter)["status"]
    wanted = expected[name]

    print(f"\nScenario: {name}")
    print(f"Expected: {wanted}")
    print(f"Actual:   {actual}")

    if actual != wanted:
        print("RESULT: FAIL")
        all_passed = False
    else:
        print("RESULT: PASS")

if not all_passed:
    raise SystemExit("Comparison failed!")

print("\nAll expected results match.")
