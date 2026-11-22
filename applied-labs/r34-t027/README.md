# Infrastructure Security Scenario Rubric Checker with State Trace (R34-T027)

This applied lab extends **[6.1 Infrastructure security key concepts.md](../../6.1%20Infrastructure%20security%20key%20concepts.md)** by implementing a local structural rubric checker for infrastructure security threat scenarios, recording intermediate state transitions, and verifying the state invariants that link those transitions to the final evaluation outcome.

## Overview

In infrastructure security (covering servers, containers, posture management, and patching), evaluating proposed security controls requires understanding both structural completeness and semantic reasoning:
1. **Structural Rubric Checker**: Verifies that every required dimension (`asset`, `threat`, `control`, `residual_risk`) is provided.
2. **Control Alignment**: Confirms whether the stated control aligns with benchmark pairings for the threat.
3. **Limits of Automated Grading**: The checker verifies structural validity and flags mismatched pairings as `REVIEW`. A human reviewer assesses the justification and residual risk.

## Fictional Scenarios

| Scenario | Asset | Threat | Control | Residual Risk | Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **kubernetes-host-patching** | Production Kubernetes container host | unpatched kernel vulnerability allowing container escape | automated os kernel patch management and reboot scheduling | Zero-day kernel flaws remain exposed until vendor patch release. | `PASS` |
| **missing-asset-image-scan** | *(Omitted)* | vulnerable base image deployed to cluster | container registry image vulnerability scanning before deployment | Vulnerabilities discovered post-deployment require runtime detection. | `FAIL (asset is required)` |
| **mismatched-control-registry** | Container registry repository | vulnerable base image deployed to cluster | automated os kernel patch management and reboot scheduling | Host kernel patching does not detect vulnerable application dependencies in images. | `REVIEW (control needs a rationale)` |

## Contribution Focus: Intermediate State Trace and Invariant Verification

During evaluation, the system executes discrete evaluation steps and records intermediate state:
- **Step 1 (`FIELD_PRESENCE`)**: Checks that `asset`, `threat`, `control`, and `residual_risk` exist and are non-blank.
- **Step 2 (`CONTROL_ALIGNMENT`)**: Evaluates whether the proposed control matches the expected threat mitigation strategy.
- **Step 3 (`FINAL_DISPOSITION`)**: Synthesizes the final status (`PASS`, `FAIL`, or `REVIEW`).

### Verified State Invariants
1. **Completeness Invariant**: If Step 1 records `missing_fields`, `final_decision` MUST start with `FAIL`.
2. **Review Invariant**: If Step 1 passes and Step 2 records `is_aligned == False`, `final_decision` MUST start with `REVIEW`.
3. **Pass Invariant**: If Step 1 passes and Step 2 records `is_aligned == True`, `final_decision` MUST be `PASS`.
4. **Transition Invariant**: Trace length is exactly 2 for missing-field failures or 3 for complete evaluations; the final disposition matches the status of the terminal evaluation step.

## Prerequisites and Invocation

- **Prerequisites**: Python 3 standard library. No third-party packages, cloud credentials, GPUs, or container runtimes required.
- **Invocation**:

From the repository root:

```bash
# Run normal scenario (evaluates all three fictional scenarios)
python3 ./applied-labs/r34-t027/example.py

# Run boundary scenario (tests empty/blank field edge cases)
python3 ./applied-labs/r34-t027/example.py --scenario boundary

# Run failure scenario (rejects non-dictionary input with exit code 1)
python3 ./applied-labs/r34-t027/example.py --scenario failure

# Inspect intermediate state traces and invariant validations
python3 ./applied-labs/r34-t027/example.py --scenario trace
```

## Expected Output (`--scenario normal`)

```text
Scenario: Illustrative infrastructure scenario rubric evaluation based on "6.1 Infrastructure security key concepts.md"; structural evaluation, not automated human grading.
kubernetes-host-patching: PASS
missing-asset-image-scan: FAIL (asset is required)
mismatched-control-registry: REVIEW (control needs a rationale)
```

## Running the Automated Test Suite

Run unit tests via unittest discovery:

```bash
python3 -m unittest discover -s ./applied-labs/r34-t027 -p "test_*.py" -v
```

Expected result: 13 tests passing with zero failures.

## Scope and Limitations

This implementation is a local educational demonstration of rubric evaluation and state trace verification. It performs in-memory string and dictionary validation. It does not interface with live Kubernetes clusters, cloud posture scanners (CSPM), or real container registries, and makes no claims regarding actual hardware security or machine learning model performance.
