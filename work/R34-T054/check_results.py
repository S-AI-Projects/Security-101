"""Assertion checks for R34-T054 infrastructure security rubric."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "applied-labs/r34-t054"))

from example import LocalInfrastructureAdapter, check_scenario, evaluate_adapter


def main() -> int:
    adapter = LocalInfrastructureAdapter()
    results = evaluate_adapter(adapter)
    assert len(results) == 3, f"Expected 3 results, got {len(results)}"

    assert results[0][1] == "PASS"
    assert results[1][1] == "FAIL"
    assert results[2][1] == "FLAG_REVIEW"

    if "--deliberate-wrong-result" in sys.argv:
        assert results[1][1] == "PASS", "Deliberate wrong result check"

    print("All R34-T054 checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
