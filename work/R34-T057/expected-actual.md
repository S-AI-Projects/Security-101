# Test Evidence: R34-T057 Typed Tool Dispatch

## Environment and Tools

- Python: 3.9.6
- Git: git version 2.50.1 (Apple Git-155)
- Platform: Darwin arm64 (macOS)
- Runtime: Python standard library

## Input Fixtures

- `add(2, 3)` -> 5
- `multiply(2, 3)` -> 6
- `system_exec(cmd='id')` -> `UNKNOWN_TOOL` error
- `add('2', 3)` -> `INVALID_ARGUMENT` error

## Expected vs Actual

| Invocation | Expected Status | Actual Status | Details |
|---|---|---|---|
| `add(2, 3)` | `SUCCESS` (5) | `SUCCESS` (5) | Allowlisted tool executed |
| `multiply(2, 3)` | `SUCCESS` (6) | `SUCCESS` (6) | Allowlisted tool executed |
| `system_exec` | `ERROR` | `ERROR` | Unknown tool rejected before invocation |
| `add('2', 3)` | `ERROR` | `ERROR` | String rejected during numeric type check |
| Q1 (Predict output) | `SUCCESS` (5) | `SUCCESS` (5) | Verified via unit test |
| Q2 (Diagnose failure)| `INVALID_ARGUMENT` | `INVALID_ARGUMENT` | Verified via unit test |
| Q3 (Boundary policy)| `UNKNOWN_TOOL` | `UNKNOWN_TOOL` | Verified via unit test |
| Deliberate failure | Non-zero exit | Exit code 1 | Captured in `deliberate-failure-output.txt` |

## Test Execution

Command: `python3 -m unittest discover -s ./applied-labs/r34-t057 -p "test_*.py"`
Result: 9 tests passed (saved in `test-output.txt`).
Deliberate failure test exited with code 1 and `AssertionError`.
