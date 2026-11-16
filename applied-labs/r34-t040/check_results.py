import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
WORK = BASE / "work" / "R34-T040"


def summarize(path):
    lines = path.read_text().splitlines()
    results = []

    for line in lines:
        item = json.loads(line)

        if "input" not in item:
            results.append(
                f"total_executor_calls: {item['total_executor_calls']}"
            )
            continue

        scenario_id = item["input"]["id"]
        decision = item["decision"]

        results.append(
            f"{scenario_id}: {decision['status']}; "
            f"executor_called={str(decision['executor_called']).lower()}"
        )

    return results


def main():
    expected = (WORK / "expected.txt").read_text().splitlines()
    actual = summarize(WORK / "actual.txt")

    if expected != actual:
        print("FAIL: Expected and actual results differ.")
        print("Expected:", expected)
        print("Actual:", actual)
        sys.exit(1)

    print("PASS: Evidence matches all expected results.")


if __name__ == "__main__":
    main()
