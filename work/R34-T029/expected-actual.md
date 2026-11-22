# Test Evidence: R34-T029 IAM Access Policy Evaluation & Comparison

## Environment and Tool Versions

- **Python**: Python 3.9.6
- **Git**: git version 2.50.1 (Apple Git-155)
- **Operating System**: Darwin 27.2.0 arm64 (macOS)
- **Dependencies**: Python standard library only (no external packages or network needed)

## Standard Fixture & Request Summary

1. **Standard Policy Matrix (`STANDARD_POLICY_MATRIX`)**:
   - `reader` | `read` | `public` -> `ALLOW`
   - `reader` | `write` | `public` -> `DENY`
   - `editor` | `read` | `public` -> `ALLOW`
   - `editor` | `write` | `public` -> `ALLOW`
   - `auditor` | `audit` | `logs` -> `ALLOW`
   - `auditor` | `audit` | `logs` -> `DENY` (deny-override)

2. **Controlled Configurations Evaluated**:
   - **Config 1 (Minimal, N=3 rules)**: `reader` read/write, `editor` read
   - **Config 2 (Standard, N=6 rules)**: Standard matrix with explicit deny-override
   - **Config 3 (Comprehensive, N=12 rules)**: Extended matrix with admin and visitor rules

## Expected vs Actual Results

| Check / Scenario | Command / Target | Expected Status / Value | Actual Status / Value | Details |
| :--- | :--- | :--- | :--- | :--- |
| `reader` read `public` | `evaluate_access("reader", "read", "public")` | `ALLOW` | `ALLOW` | Allowed by explicit rule |
| `reader` write `public` | `evaluate_access("reader", "write", "public")` | `DENY` | `DENY` | Denied by explicit DENY rule |
| Explicit Deny Override | `evaluate_access("auditor", "audit", "logs")` | `DENY` | `DENY` | DENY strictly overrides matching ALLOW |
| Unknown Role | `evaluate_access("stranger", "read", "public")` | `DENY` | `DENY` | Unknown role blocked under default-deny |
| Unlisted Action | `evaluate_access("reader", "delete", "public")` | `DENY` | `DENY` | Blocked under default-deny |
| Boundary Requests | `example.py --scenario boundary` | Exit code 0, all DENY | Exit code 0, all DENY | Handles unlisted resources and blank fields |
| Failure Scenario | `example.py --scenario failure` | Exit code 1, `ValueError` | Exit code 1, `Invalid policy effect 'PERMIT'` | Rejects malformed policy effect |
| Config Comparison | `example.py --compare` | 100.0% correctness, checks scale 12 -> 24 -> 48 | 100.0% correctness, checks 12 -> 24 -> 48 | O(N) evaluation search trade-off verified |
| Unit Test Suite | `unittest discover` | 15 passed, exit code 0 | 15 passed in 0.001s, exit code 0 | Non-zero test count, green test suite |
| Deliberate Failure | `check_results.py --deliberate-wrong-result` | Exit code 1, `AssertionError` | Exit code 1, `AssertionError` | Deliberate wrong assertion exits non-zero |

## Fresh Process Execution Evidence

- `work/R34-T029/normal-output.txt`: Captured output from running `example.py`
- `work/R34-T029/boundary-output.txt`: Captured output from running `example.py --scenario boundary`
- `work/R34-T029/failure-output.txt`: Captured output from running `example.py --scenario failure`
- `work/R34-T029/test-output.txt`: Captured output from running unit tests (15 tests passed)
- `work/R34-T029/deliberate-failure-output.txt`: Captured output from deliberate wrong assertion (exit code 1)
- `work/R34-T029/tool-versions.txt`: Environment tool version strings
