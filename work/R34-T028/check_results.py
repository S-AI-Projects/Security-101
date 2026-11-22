#!/usr/bin/env python3
"""Standalone verification script for R34-T028 network range classification.

Validates that 192.0.2.1 belongs to 192.0.2.0/24, 198.51.100.1 does not, malformed
and missing inputs are rejected, and parser recovers cleanly on the next valid input.
Supports --deliberate-wrong-result to trigger an intentional AssertionError and exit code 1.
"""

import os
import sys

# Ensure applied-labs/r34-t028 is in python path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LAB_DIR = os.path.join(BASE_DIR, "applied-labs", "r34-t028")
if LAB_DIR not in sys.path:
    sys.path.insert(0, LAB_DIR)

from example import (  # noqa: E402
    DEFAULT_ALLOWLIST_CIDR,
    LESSON_CITATION,
    classify_address,
    classify_sequence,
    run_scenario,
)


def run_checks(deliberate_wrong: bool = False) -> None:
    print("Running R34-T028 network range classification checks...", flush=True)

    # 1. 192.0.2.1 belongs to 192.0.2.0/24 -> ALLOW
    r1 = classify_address("192.0.2.1", DEFAULT_ALLOWLIST_CIDR)
    assert r1["status"] == "ALLOW", f"Expected ALLOW, got {r1}"
    assert r1["is_member"] is True, f"Expected is_member True, got {r1}"

    # 2. 198.51.100.1 does not belong -> DENY
    r2 = classify_address("198.51.100.1", DEFAULT_ALLOWLIST_CIDR)
    assert r2["status"] == "DENY", f"Expected DENY, got {r2}"
    assert r2["is_member"] is False, f"Expected is_member False, got {r2}"

    # 3. Malformed input rejected -> ERROR (MALFORMED_IP)
    r3 = classify_address("invalid-ip-string", DEFAULT_ALLOWLIST_CIDR)
    assert r3["status"] == "ERROR", f"Expected ERROR, got {r3}"
    assert r3["error_type"] == "MALFORMED_IP", f"Expected MALFORMED_IP, got {r3}"

    # 4. Missing data rejected -> ERROR (MISSING_DATA)
    r4 = classify_address("", DEFAULT_ALLOWLIST_CIDR)
    assert r4["status"] == "ERROR", f"Expected ERROR, got {r4}"
    assert r4["error_type"] == "MISSING_DATA", f"Expected MISSING_DATA, got {r4}"

    # 5. Recovery on next valid input check
    seq_results = classify_sequence(["invalid-ip-string", "", "192.0.2.42"], DEFAULT_ALLOWLIST_CIDR)
    assert seq_results[0]["status"] == "ERROR"
    assert seq_results[1]["status"] == "ERROR"
    assert seq_results[2]["status"] == "ALLOW", f"Expected recovery ALLOW, got {seq_results[2]}"
    assert seq_results[2]["is_member"] is True

    # 6. Lesson citation check
    code_norm, out_norm = run_scenario("normal")
    assert code_norm == 0, "Normal scenario must exit with 0"
    assert LESSON_CITATION in out_norm, f"Missing citation: {LESSON_CITATION}"

    # 7. Boundary scenario check
    code_bound, out_bound = run_scenario("boundary")
    assert code_bound == 0, "Boundary scenario must exit with 0"
    assert "192.0.2.0" in out_bound and "192.0.2.255" in out_bound

    # 8. Failure scenario check
    code_fail, out_fail = run_scenario("failure")
    assert code_fail == 1, "Failure scenario must exit with 1"
    assert "Error:" in out_fail

    # 9. Deliberate wrong result check (if requested)
    if deliberate_wrong:
        print(
            "Executing deliberate wrong result assertion (expecting ALLOW for 198.51.100.1)...",
            flush=True,
        )
        assert r2["status"] == "ALLOW", (
            f"Deliberate wrong result triggered: expected 'ALLOW', actual was '{r2['status']}'"
        )

    print("All R34-T028 checks passed successfully.", flush=True)


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
