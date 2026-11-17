"""Assertion checks for R34-T060 network security rubric comparison."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "applied-labs/r34-t060"))

from example import (
    check_scenario_direct,
    check_scenario_independent,
    compare_approaches,
    get_canonical_scenarios,
)


def main() -> int:
    scenarios = get_canonical_scenarios()
    assert len(scenarios) == 3

    assert check_scenario_direct(scenarios[0])[0] == "PASS"
    assert check_scenario_direct(scenarios[1])[0] == "FAIL"
    assert check_scenario_direct(scenarios[2])[0] == "FLAG_REVIEW"

    comp = compare_approaches(scenarios)
    for c in comp:
        assert c["matches"] is True

    if "--deliberate-wrong-result" in sys.argv:
        assert check_scenario_direct(scenarios[1])[0] == "PASS", "Deliberate wrong result check"

    print("All R34-T060 checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
