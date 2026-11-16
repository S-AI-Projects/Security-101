import json
import sys
from pathlib import Path


evidence = Path(__file__).parents[2] / "work" / "R34-T039"

def load_summaries(path):
    summaries = []
    for line in path.read_text().splitlines():
        if line.strip():
            item = json.loads(line)
            summaries.append({
                key: item[key]
                for key in (
                    "group",
                    "input_count",
                    "allowed_count",
                    "rejected_count",
                    "executor_calls",
                )
            })
    return summaries


expected = load_summaries(evidence / "expected.jsonl")
actual = load_summaries(evidence / "actual.jsonl")

if actual != expected:
    print("FAIL: actual results do not match expected results")
    print("Expected:", expected)
    print("Actual:", actual)
    sys.exit(1)

print(f"PASS: all {len(expected)} scenario summaries match")
