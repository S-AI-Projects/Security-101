"""Evidence check script for R34-T051.

Runs assertions verifying correct rubric outcomes.
Supports --deliberate-wrong-result which deliberately asserts an incorrect outcome and exits non-zero.
"""

import sys
from pathlib import Path

# Add lab directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "applied-labs/r34-t051"))

from example import check_scenario, get_default_scenarios, run_scenarios


def main() -> int:
    scenarios = get_default_scenarios()
    assert len(scenarios) == 3, "Expected 3 scenarios"

    # Scenario 1: Complete passes
    s1_status, s1_msg = check_scenario(scenarios[0])
    assert s1_status == "PASS", f"Scenario 1 expected PASS, got {s1_status}"

    # Scenario 2: Missing asset fails
    s2_status, s2_msg = check_scenario(scenarios[1])
    assert s2_status == "FAIL", f"Scenario 2 expected FAIL, got {s2_status}"
    assert "asset" in s2_msg.lower()

    # Scenario 3: Mismatched control flags review
    s3_status, s3_msg = check_scenario(scenarios[2])
    assert s3_status == "FLAG_REVIEW", f"Scenario 3 expected FLAG_REVIEW, got {s3_status}"

    # Deliberate wrong result check
    if "--deliberate-wrong-result" in sys.argv:
        # Deliberately assert that missing asset scenario passed
        assert s2_status == "PASS", "Deliberate wrong result check triggered"

    print("All R34-T051 rubric checks passed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
