# Test Evidence: R34-T027 Infrastructure Security Scenario Rubric Checker

## Environment and Tool Versions

- **Python**: Python 3.9.6
- **Git**: git version 2.50.1 (Apple Git-155)
- **Operating System**: Darwin 27.2.0 arm64 (macOS)
- **Dependencies**: Python standard library only (`argparse`, `sys`, `unittest`)

## Fictional Scenarios & Rubric Fields Summary

- **Rubric Dimensions**: `("asset", "threat", "control", "residual_risk")`
- **Fictional Scenarios Evaluated**:
  1. `kubernetes-host-patching`: Complete answer with aligned host patching control -> `PASS`
  2. `missing-asset-image-scan`: Missing required asset dimension -> `FAIL (asset is required)`
  3. `mismatched-control-registry`: Complete dimensions but control unrelated to threat -> `REVIEW (control needs a rationale)`

## Expected vs Actual Results

| Check / Scenario | Command / Target | Expected Status / Value | Actual Status / Value | Details |
| :--- | :--- | :--- | :--- | :--- |
| Complete Scenario | `check_scenario(SCENARIOS["kubernetes-host-patching"])` | `PASS` | `PASS` | All fields present and control matches threat |
| Missing Asset | `check_scenario(SCENARIOS["missing-asset-image-scan"])` | `FAIL (asset is required)` | `FAIL (asset is required)` | Structural rubric rejects missing asset |
| Control Mismatch | `check_scenario(SCENARIOS["mismatched-control-registry"])` | `REVIEW (control needs a rationale)` | `REVIEW (control needs a rationale)` | Unrelated control flagged for human review |
| State Trace & Invariants | `evaluate_scenario_with_trace(...)` | Steps 1-3 recorded, all invariants True | Invariants hold (True) across all scenarios | Completeness, review, pass, and transition invariants hold |
| Boundary Checks | `example.py --scenario boundary` | Exit code 0, all `FAIL` | Exit code 0, all `FAIL` | Blank `residual_risk` and `control` rejected |
| Failure Scenario | `example.py --scenario failure` | Exit code 1, `TypeError` | Exit code 1, `TypeError` | Rejects non-dictionary scenario inputs |
| Unit Test Suite | `unittest discover` | 13 passed, exit code 0 | 13 passed in 0.001s, exit code 0 | Non-zero test count, all assertions hold |
| Deliberate Failure | `check_results.py --deliberate-wrong-result` | Exit code 1, `AssertionError` | Exit code 1, `AssertionError` | Verifies assertion check fails on mismatch |

## Fresh Process Execution Evidence

- `work/R34-T027/normal-output.txt`: Captured output from running `example.py`
- `work/R34-T027/boundary-output.txt`: Captured output from running `example.py --scenario boundary`
- `work/R34-T027/failure-output.txt`: Captured output from running `example.py --scenario failure`
- `work/R34-T027/test-output.txt`: Captured output from running unit tests (13 tests passed)
- `work/R34-T027/deliberate-failure-output.txt`: Captured output from deliberate wrong assertion (exit code 1)
- `work/R34-T027/tool-versions.txt`: Environment tool version strings
