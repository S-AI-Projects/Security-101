# Test Evidence: R34-T059 Infrastructure Scenario Rubric Evaluation Experiment

## Environment and Tools

- Python: 3.9.6
- Git: git version 2.50.1 (Apple Git-155)
- Platform: Darwin arm64 (macOS)
- Runtime: Python standard library

## Input Fixtures

- `Kubernetes API Server`: Complete scenario (`PASS`)
- `Missing asset infra quiz scenario`: Blank asset (`FAIL`)
- `Mismatched infrastructure quiz control`: DDoS paired with BIOS password (`FLAG_REVIEW`)

## Expected vs Actual

| Scenario | Expected | Actual | Details |
|---|---|---|---|
| Complete scenario | `PASS` | `PASS` | All fields present and mTLS/RBAC matches unauthorized execution threat |
| Missing asset | `FAIL` | `FAIL` | Rejected with "Missing required field: asset" |
| Mismatched control | `FLAG_REVIEW` | `FLAG_REVIEW` | BIOS controls do not mitigate volumetric DDoS; flagged for review |
| Config 1 (N=1) Correctness | 100% | 100% | Stable across iterations |
| Config 2 (N=3) Correctness | 100% | 100% | Stable across iterations |
| Config 3 (N=6) Correctness | 100% | 100% | Stable across iterations |
| Deliberate failure | Non-zero exit | Exit code 1 | Captured in `deliberate-failure-output.txt` |

## Test Execution

Command: `python3 -m unittest discover -s ./applied-labs/r34-t059 -p "test_*.py"`
Result: 5 tests passed (saved in `test-output.txt`).
Deliberate failure test exited with code 1 and `AssertionError`.
