
import json
import runpy
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
LAB = BASE / "applied-labs" / "r34-t034"
EVIDENCE = BASE / "work" / "R34-T034"

expected = {
    "APPSEC-01": "PASS",
    "APPSEC-02": "FAIL",
    "APPSEC-03": "REVIEW"
}

module = runpy.run_path(str(LAB / "example.py"))
evaluate = module["evaluate_scenario"]

with open(LAB / "scenarios.json") as file:
    scenarios = json.load(file)

actual_results = [evaluate(item) for item in scenarios]

lines = []
mismatches = []

for result in actual_results:
    scenario_id = result["scenario_id"]
    actual = result["status"]
    wanted = expected.get(scenario_id)

    line = (
        f"{scenario_id}: expected={wanted}, actual={actual}"
    )
    lines.append(line)
    print(line)

    if wanted != actual:
        mismatches.append(scenario_id)

EVIDENCE.mkdir(parents=True, exist_ok=True)

output = "\n".join(lines) + "\n"

with open(EVIDENCE / "comparison-results.txt", "w") as file:
    file.write(output)

if mismatches:
    print("COMPARISON FAILED:", ", ".join(mismatches))
    sys.exit(1)

print("COMPARISON PASSED")
