import json
import sys
from pathlib import Path

folder = Path(__file__).parent
evidence = folder.parents[1] / "work" / "R34-T038"

expected_path = evidence / "expected.jsonl"
actual_path = evidence / "actual.jsonl"

with expected_path.open(encoding="utf-8") as file:
    expected = [json.loads(line) for line in file if line.strip()]

with actual_path.open(encoding="utf-8") as file:
    actual = [json.loads(line) for line in file if line.strip()]

if expected != actual:
    print("FAIL: Actual results do not match expected results.")
    sys.exit(1)

print(f"PASS: All {len(expected)} results match.")
