"""Assertion checks for R34-T059 infrastructure rubric evaluation experiment."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "applied-labs/r34-t059"))

from example import (
    check_scenario,
    get_canonical_scenarios,
    run_evaluation_experiment,
)


def main() -> int:
    scenarios = get_canonical_scenarios()
    assert len(scenarios) == 3

    assert check_scenario(scenarios[0])[0] == "PASS"
    assert check_scenario(scenarios[1])[0] == "FAIL"
    assert check_scenario(scenarios[2])[0] == "FLAG_REVIEW"

    exp = run_evaluation_experiment()
    assert len(exp) == 3
    for name, data in exp.items():
        assert data["correctness_rate"] == 1.0

    if "--deliberate-wrong-result" in sys.argv:
        assert check_scenario(scenarios[1])[0] == "PASS", "Deliberate wrong result check"

    print("All R34-T059 checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
