#!/usr/bin/env python3
"""Standalone verification script for R34-T029 IAM policy evaluator.

Validates core IAM evaluation rules, default-deny fallbacks, deny-overriding-allow precedence,
and configuration trade-off metrics. Supports --deliberate-wrong-result to trigger an
intentional AssertionError and exit code 1.
"""

import os
import sys

# Ensure applied-labs/r34-t029 is in python path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LAB_DIR = os.path.join(BASE_DIR, "applied-labs", "r34-t029")
if LAB_DIR not in sys.path:
    sys.path.insert(0, LAB_DIR)

from example import (  # noqa: E402
    LESSON_CITATION,
    compare_configurations,
    evaluate_access,
    run_scenario,
)


def run_checks(deliberate_wrong: bool = False) -> None:
    print("Running R34-T029 IAM access policy evaluator checks...", flush=True)

    # 1. reader may read public -> ALLOW
    r_read = evaluate_access("reader", "read", "public")
    assert r_read["decision"] == "ALLOW", f"Expected ALLOW, got {r_read}"

    # 2. reader cannot write public -> DENY
    r_write = evaluate_access("reader", "write", "public")
    assert r_write["decision"] == "DENY", f"Expected DENY, got {r_write}"

    # 3. Explicit deny overrides matching allow -> DENY
    r_audit = evaluate_access("auditor", "audit", "logs")
    assert r_audit["decision"] == "DENY", f"Expected DENY, got {r_audit}"

    # 4. Unknown role is denied -> DENY
    r_stranger = evaluate_access("stranger", "read", "public")
    assert r_stranger["decision"] == "DENY", f"Expected DENY, got {r_stranger}"

    # 5. Default-deny for unlisted action
    r_del = evaluate_access("reader", "delete", "public")
    assert r_del["decision"] == "DENY", f"Expected DENY, got {r_del}"

    # 6. Scenario citation check
    code_norm, out_norm = run_scenario("normal")
    assert code_norm == 0, "Normal scenario must exit with 0"
    assert LESSON_CITATION in out_norm, f"Missing lesson citation: {LESSON_CITATION}"

    # 7. Boundary scenario check
    code_bound, out_bound = run_scenario("boundary")
    assert code_bound == 0, "Boundary scenario must exit with 0"
    assert "DENY" in out_bound, "Boundary scenario must demonstrate DENY outcomes"

    # 8. Failure scenario check
    code_fail, out_fail = run_scenario("failure")
    assert code_fail == 1, "Failure scenario must exit with 1"
    assert "Error:" in out_fail, "Failure scenario must output error message"

    # 9. Configuration comparison experiment trade-off check
    comp_res = compare_configurations()
    assert len(comp_res) == 3, f"Expected 3 configurations, got {len(comp_res)}"
    for c in comp_res:
        assert c["correctness_rate"] == 100.0, f"Expected 100% correctness, got {c['correctness_rate']}"
    assert comp_res[0]["total_checks"] == 12, f"Expected 12 checks, got {comp_res[0]['total_checks']}"
    assert comp_res[1]["total_checks"] == 24, f"Expected 24 checks, got {comp_res[1]['total_checks']}"
    assert comp_res[2]["total_checks"] == 48, f"Expected 48 checks, got {comp_res[2]['total_checks']}"

    # 10. Deliberate wrong result check (if requested)
    if deliberate_wrong:
        print(
            "Executing deliberate wrong result assertion (expecting ALLOW for reader write public)...",
            flush=True,
        )
        assert r_write["decision"] == "ALLOW", (
            f"Deliberate wrong result triggered: expected 'ALLOW', actual was '{r_write['decision']}'"
        )

    print("All R34-T029 checks passed successfully.", flush=True)


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
