
import json
import sys
from pathlib import Path


def compare_results(expected_path, actual_path):
    expected = json.loads(Path(expected_path).read_text())
    actual = json.loads(Path(actual_path).read_text())

    print("Expected:", expected)
    print("Actual:", actual)

    if expected != actual:
        print("RESULT: MISMATCH")
        return 1

    print("RESULT: MATCH")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python3 compare_results.py "
            "expected.json actual.json"
        )
        sys.exit(2)

    sys.exit(compare_results(sys.argv[1], sys.argv[2]))
