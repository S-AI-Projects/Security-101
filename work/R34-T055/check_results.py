"""Assertion checks for R34-T055 data security scenario rubric."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "applied-labs/r34-t055"))

from example import check_scenario, get_worked_example_scenarios, run_scenarios


def main() -> int:
    scenarios = get_worked_example_scenarios()
    results = run_scenarios(scenarios)
    assert len(results) == 3, f"Expected 3 results, got {len(results)}"

    assert results[0][1] == "PASS"
    assert results[1][1] == "FAIL"
    assert results[2][1] == "FLAG_REVIEW"

    # Exact message check for regression test
    assert results[1][2] == "Missing required field: asset"

    if "--deliberate-wrong-result" in sys.argv:
        assert results[1][1] == "PASS", "Deliberate wrong result check"

    print("All R34-T055 checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
