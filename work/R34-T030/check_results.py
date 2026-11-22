#!/usr/bin/env python3
"""Standalone verification script for R34-T030 responsibility matrix lab.

Runs validation checks against normal, boundary, and failure contract expectations,
evaluates the three applied questions, and validates that missing ownership is flagged.
Supports --deliberate-wrong-result to trigger an intentional AssertionError and exit code 1.
"""

import os
import sys

# Ensure applied-labs/r34-t030 is in python path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LAB_DIR = os.path.join(BASE_DIR, "applied-labs", "r34-t030")
if LAB_DIR not in sys.path:
    sys.path.insert(0, LAB_DIR)

from example import (  # noqa: E402
    APPLIED_QUESTIONS,
    BOUNDARY_FIXTURE,
    LESSON_CITATION,
    NORMAL_FIXTURE,
    VALID_RESPONSIBLE_PARTIES,
    VALID_SERVICE_MODELS,
    evaluate_matrix,
    evaluate_task_responsibility,
    run_scenario,
)


def run_checks(deliberate_wrong: bool = False) -> None:
    print("Running R34-T030 responsibility matrix checks...", flush=True)

    # 1. Normal scenario contract check
    normal_eval = evaluate_matrix(NORMAL_FIXTURE)
    assert len(normal_eval) == 7, f"Expected 7 rows, got {len(normal_eval)}"
    parties = {r["responsible_party"] for r in normal_eval}
    assert parties == set(VALID_RESPONSIBLE_PARTIES), f"Parties mismatch: {parties}"
    models = {r["service_model"] for r in normal_eval}
    assert models == set(VALID_SERVICE_MODELS), f"Models mismatch: {models}"

    # 2. Lesson citation check
    code_norm, out_norm = run_scenario("normal")
    assert code_norm == 0, "Normal scenario must exit with 0"
    assert LESSON_CITATION in out_norm, f"Missing lesson citation: {LESSON_CITATION}"

    # 3. Boundary check: missing ownership flagged as UNASSIGNED, not provider
    boundary_eval = evaluate_matrix(BOUNDARY_FIXTURE)
    for r in boundary_eval:
        assert r["responsible_party"] == "UNASSIGNED", f"Expected UNASSIGNED, got {r}"
        assert r["status"] == "FLAGGED_UNASSIGNED"
        assert r["responsible_party"] != "provider", "Unassigned task must never default to provider"

    # 4. Failure scenario check: invalid service model produces exit code 1
    code_fail, out_fail = run_scenario("failure")
    assert code_fail == 1, f"Expected exit code 1 for failure, got {code_fail}"
    assert "Error:" in out_fail, "Expected Error in failure scenario output"

    # 5. Applied Question 1 check: Predict output
    q1_row = evaluate_task_responsibility({
        "task": "Patch guest operating system",
        "service_model": "IaaS",
        "responsible_party": "customer",
    })
    assert q1_row["responsible_party"] == "customer", f"Q1 failed: {q1_row}"
    assert q1_row["responsible_party"] == APPLIED_QUESTIONS["question_1"]["expected_answer"]

    # 6. Applied Question 2 check: Diagnose failure
    q2_row = evaluate_task_responsibility({
        "task": "Enforce MFA on user accounts",
        "service_model": "SaaS",
    })
    assert q2_row["responsible_party"] == "UNASSIGNED", f"Q2 failed: {q2_row}"
    assert q2_row["responsible_party"] == APPLIED_QUESTIONS["question_2"]["expected_answer"]

    # 7. Applied Question 3 check: Choose boundary policy
    assert APPLIED_QUESTIONS["question_3"]["expected_answer"] == "UNASSIGNED"

    # 8. Deliberate wrong result check (if requested)
    if deliberate_wrong:
        print(
            "Executing deliberate wrong result assertion (expecting provider for IaaS guest OS patch)...",
            flush=True,
        )
        assert q1_row["responsible_party"] == "provider", (
            f"Deliberate wrong result triggered: expected 'provider', actual was '{q1_row['responsible_party']}'"
        )

    print("All R34-T030 checks passed successfully.", flush=True)


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
