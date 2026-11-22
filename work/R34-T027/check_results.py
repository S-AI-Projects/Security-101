#!/usr/bin/env python3
"""Standalone verification script for R34-T027 infrastructure rubric checker.

Validates that complete scenarios pass, missing-asset scenarios fail, and control
mismatches are routed to review. Verifies that intermediate state traces and invariants
link correctly to the final output. Supports --deliberate-wrong-result to trigger an
intentional AssertionError and exit code 1.
"""

import os
import sys

# Ensure applied-labs/r34-t027 is in python path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LAB_DIR = os.path.join(BASE_DIR, "applied-labs", "r34-t027")
if LAB_DIR not in sys.path:
    sys.path.insert(0, LAB_DIR)

from example import (  # noqa: E402
    LESSON_CITATION,
    SCENARIOS,
    check_scenario,
    evaluate_scenario_with_trace,
    run_scenario,
    verify_state_invariants,
)


def run_checks(deliberate_wrong: bool = False) -> None:
    print("Running R34-T027 infrastructure rubric checker checks...", flush=True)

    # 1. Complete scenario passes -> PASS
    r1 = check_scenario(SCENARIOS["kubernetes-host-patching"])
    assert r1 == "PASS", f"Expected PASS, got {r1}"

    # 2. Scenario without asset fails -> FAIL (asset is required)
    r2 = check_scenario(SCENARIOS["missing-asset-image-scan"])
    assert r2 == "FAIL (asset is required)", f"Expected FAIL, got {r2}"

    # 3. Control unrelated to threat flagged for review -> REVIEW (control needs a rationale)
    r3 = check_scenario(SCENARIOS["mismatched-control-registry"])
    assert r3 == "REVIEW (control needs a rationale)", f"Expected REVIEW, got {r3}"

    # 4. State trace and invariant verification
    for name, s in SCENARIOS.items():
        dec, trace = evaluate_scenario_with_trace(s)
        assert len(trace) in (2, 3), f"Trace length invalid: {len(trace)}"
        assert verify_state_invariants(trace, dec) is True, f"Invariant failed for {name}"

    # 5. Lesson citation check
    code_norm, out_norm = run_scenario("normal")
    assert code_norm == 0, "Normal scenario must exit with 0"
    assert LESSON_CITATION in out_norm, f"Missing citation: {LESSON_CITATION}"

    # 6. Boundary scenario check
    code_bound, out_bound = run_scenario("boundary")
    assert code_bound == 0, "Boundary scenario must exit with 0"
    assert "FAIL" in out_bound, "Boundary scenario must demonstrate FAIL outcomes"

    # 7. Failure scenario check
    code_fail, out_fail = run_scenario("failure")
    assert code_fail == 1, "Failure scenario must exit with 1"
    assert "Error:" in out_fail

    # 8. Deliberate wrong result check (if requested)
    if deliberate_wrong:
        print(
            "Executing deliberate wrong result assertion (expecting PASS for mismatched scenario)...",
            flush=True,
        )
        assert r3 == "PASS", (
            f"Deliberate wrong result triggered: expected 'PASS', actual was '{r3}'"
        )

    print("All R34-T027 checks passed successfully.", flush=True)


def main() -> int:
    deliberate_wrong = "--deliberate-wrong-result" in sys.argv
    try:
        run_checks(deliberate_wrong=deliberate_wrong)
        return 0
    except AssertionError as exc:
        print(f"AssertionError: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
