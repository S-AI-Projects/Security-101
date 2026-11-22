"""Infrastructure security scenario rubric checker with state trace and invariant verification.

Extends '6.1 Infrastructure security key concepts.md'. Evaluates fictional infrastructure
security scenarios against a structural rubric (asset, threat, control, residual_risk).
Records the intermediate state after each step and verifies invariants linking intermediate
state transitions to the final evaluation output.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from typing import Any, Dict, List, Optional, Tuple

LESSON_CITATION = "6.1 Infrastructure security key concepts.md"

FIELDS = ("asset", "threat", "control", "residual_risk")

CONTROL_BY_THREAT = {
    "unpatched kernel vulnerability allowing container escape": "automated os kernel patch management and reboot scheduling",
    "vulnerable base image deployed to cluster": "container registry image vulnerability scanning before deployment",
    "exposed unauthenticated kubernetes api server": "enforce private cluster endpoint and mfa rbac authentication",
}

# Three fictional scenarios tied to 6.1 Infrastructure security key concepts
SCENARIOS: dict[str, dict[str, str]] = {
    "kubernetes-host-patching": {
        "asset": "Production Kubernetes container host",
        "threat": "unpatched kernel vulnerability allowing container escape",
        "control": "automated os kernel patch management and reboot scheduling",
        "residual_risk": "Zero-day kernel flaws remain exposed until vendor patch release.",
    },
    "missing-asset-image-scan": {
        "threat": "vulnerable base image deployed to cluster",
        "control": "container registry image vulnerability scanning before deployment",
        "residual_risk": "Vulnerabilities discovered post-deployment require runtime detection.",
    },
    "mismatched-control-registry": {
        "asset": "Container registry repository",
        "threat": "vulnerable base image deployed to cluster",
        "control": "automated os kernel patch management and reboot scheduling",
        "residual_risk": "Host kernel patching does not detect vulnerable application dependencies in images.",
    },
}

# Boundary fixtures for testing edge inputs
BOUNDARY_SCENARIOS: dict[str, dict[str, str]] = {
    "blank-residual-risk": {
        "asset": "Production Kubernetes container host",
        "threat": "unpatched kernel vulnerability allowing container escape",
        "control": "automated os kernel patch management and reboot scheduling",
        "residual_risk": "   ",
    },
    "blank-control": {
        "asset": "Production Kubernetes container host",
        "threat": "unpatched kernel vulnerability allowing container escape",
        "control": "",
        "residual_risk": "Risk remains unmitigated.",
    },
}

SCENARIO_EXPLANATIONS = {
    "normal": (
        f'Scenario: Illustrative infrastructure scenario rubric evaluation based on "{LESSON_CITATION}"; '
        "structural evaluation, not automated human grading."
    ),
    "boundary": (
        f'Scenario: Boundary checks for incomplete scenario answers based on "{LESSON_CITATION}"; '
        "evaluates missing fields and blank entries."
    ),
    "failure": (
        f'Scenario: Failure check based on "{LESSON_CITATION}"; '
        "rejects malformed scenario types or invalid answer structures."
    ),
}


def evaluate_scenario_with_trace(
    answer: dict[str, Any],
) -> tuple[str, list[dict[str, Any]]]:
    """Evaluate a scenario against the rubric while recording intermediate state traces.

    Steps:
    1. Field Presence: verify asset, threat, control, residual_risk exist and are non-empty.
    2. Semantic Consistency: check if stated control addresses the named threat.
    3. Final Disposition: synthesize final status (PASS, FAIL, or REVIEW).

    Returns:
    - final_decision: str
    - trace: list of step-state dictionaries
    """
    if not isinstance(answer, dict):
        raise TypeError(f"Scenario answer must be a dict, got {type(answer).__name__}")

    trace: list[dict[str, Any]] = []

    # Step 1: Field Presence Check
    missing_fields = []
    for field in FIELDS:
        val = answer.get(field)
        if not isinstance(val, str) or not val.strip():
            missing_fields.append(field)

    step1_state = {
        "step": 1,
        "name": "FIELD_PRESENCE",
        "missing_fields": missing_fields,
        "status_so_far": "FAIL" if missing_fields else "VALID_FIELDS",
    }
    trace.append(step1_state)

    if missing_fields:
        final_decision = f"FAIL ({missing_fields[0]} is required)"
        step3_state = {
            "step": 3,
            "name": "FINAL_DISPOSITION",
            "final_decision": final_decision,
            "reason": f"Required field '{missing_fields[0]}' is missing or blank",
        }
        trace.append(step3_state)
        return final_decision, trace

    # Step 2: Control Alignment Check
    normalized_threat = answer["threat"].strip().lower()
    normalized_control = answer["control"].strip().lower()
    expected_control = CONTROL_BY_THREAT.get(normalized_threat)

    is_aligned = (expected_control == normalized_control)

    step2_state = {
        "step": 2,
        "name": "CONTROL_ALIGNMENT",
        "threat": normalized_threat,
        "control": normalized_control,
        "expected_control": expected_control,
        "is_aligned": is_aligned,
        "status_so_far": "PASS" if is_aligned else "REVIEW",
    }
    trace.append(step2_state)

    # Step 3: Final Disposition Synthesis
    if is_aligned:
        final_decision = "PASS"
        reason = "All required fields present and control directly addresses stated threat."
    else:
        final_decision = "REVIEW (control needs a rationale)"
        reason = "All fields present, but control differs from benchmark pairing; human review required."

    step3_state = {
        "step": 3,
        "name": "FINAL_DISPOSITION",
        "final_decision": final_decision,
        "reason": reason,
    }
    trace.append(step3_state)

    return final_decision, trace


def verify_state_invariants(trace: list[dict[str, Any]], final_decision: str) -> bool:
    """Verify core state-transition invariants linking intermediate state to final output.

    Invariants:
    1. If Step 1 has missing_fields, final_decision must be FAIL.
    2. If Step 1 has no missing_fields and Step 2 is_aligned is True, final_decision must be PASS.
    3. If Step 1 has no missing_fields and Step 2 is_aligned is False, final_decision must be REVIEW.
    4. Final decision must match the status_so_far of the last completed intermediate step.
    """
    step1 = trace[0]
    if step1["missing_fields"]:
        if not final_decision.startswith("FAIL"):
            return False
        if len(trace) != 2:
            return False
        return True

    # If step 1 passed, step 2 must exist
    if len(trace) < 2:
        return False
    step2 = trace[1]

    if step2["is_aligned"] is True:
        if final_decision != "PASS":
            return False
    elif step2["is_aligned"] is False:
        if not final_decision.startswith("REVIEW"):
            return False

    # Invariant 4: Last disposition matches step 3
    step3 = trace[-1]
    if step3["final_decision"] != final_decision:
        return False

    return True


def check_scenario(answer: dict[str, Any]) -> str:
    """Convenience wrapper returning final decision string and asserting invariants."""
    decision, trace = evaluate_scenario_with_trace(answer)
    assert verify_state_invariants(trace, decision), "Invariant violation between state trace and final output!"
    return decision


def run_scenario(scenario_name: str) -> tuple[int, str]:
    """Execute scenario by name ('normal', 'boundary', 'failure', 'trace')."""
    if scenario_name not in SCENARIO_EXPLANATIONS and scenario_name != "trace":
        return 1, f"Error: unknown scenario '{scenario_name}'"

    if scenario_name == "normal":
        lines = [SCENARIO_EXPLANATIONS["normal"]]
        for name, ans in SCENARIOS.items():
            lines.append(f"{name}: {check_scenario(ans)}")
        return 0, "\n".join(lines)

    if scenario_name == "boundary":
        lines = [SCENARIO_EXPLANATIONS["boundary"]]
        for name, ans in BOUNDARY_SCENARIOS.items():
            lines.append(f"{name}: {check_scenario(ans)}")
        return 0, "\n".join(lines)

    if scenario_name == "failure":
        try:
            check_scenario("not_a_valid_scenario_dict")  # type: ignore
            return 0, f"{SCENARIO_EXPLANATIONS['failure']}\nUnexpected success for invalid input"
        except TypeError as exc:
            return 1, f"{SCENARIO_EXPLANATIONS['failure']}\nError: {exc}"

    if scenario_name == "trace":
        lines = ["Intermediate State Trace & Invariant Verification:"]
        for name, ans in SCENARIOS.items():
            dec, trace = evaluate_scenario_with_trace(ans)
            inv_ok = verify_state_invariants(trace, dec)
            lines.append(f"\nScenario: {name} -> Decision: {dec} (Invariant Validated: {inv_ok})")
            for entry in trace:
                lines.append(f"  Step {entry['step']} [{entry['name']}]: {entry}")
        return 0, "\n".join(lines)

    return 1, f"Unhandled scenario '{scenario_name}'"


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point for running the infrastructure rubric checker lab."""
    parser = argparse.ArgumentParser(
        description="Infrastructure security scenario rubric checker with state trace."
    )
    parser.add_argument(
        "--scenario",
        choices=["normal", "boundary", "failure", "trace"],
        default="normal",
        help="Scenario to run: normal (default), boundary, failure, or trace",
    )

    args = parser.parse_args(argv)

    exit_code, output = run_scenario(args.scenario)
    if exit_code == 0:
        print(output)
    else:
        print(output, file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
