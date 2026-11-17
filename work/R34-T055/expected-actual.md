# Test Evidence: R34-T055 Data Security Scenario Rubric with Worked Example

## Environment and Tools

- Python: 3.9.6
- Git: git version 2.50.1 (Apple Git-155)
- Platform: Darwin arm64 (macOS)
- Runtime: Python standard library

## Input Fixtures

- `Customer PII Database`: Complete scenario (`PASS`)
- `Missing asset data scenario`: Empty asset field (`FAIL`)
- `Mismatched data protection control`: Re-identification paired with snapshot replication (`FLAG_REVIEW`)

## Expected vs Actual

| Scenario | Expected | Actual | Details |
|---|---|---|---|
| Complete scenario | `PASS` | `PASS` | All fields present and TDE control matches exfiltration threat |
| Missing asset | `FAIL` | `FAIL` | Rejected with "Missing required field: asset" |
| Mismatched control | `FLAG_REVIEW` | `FLAG_REVIEW` | Snapshot replication does not address re-identification; flagged for review |
| Boundary empty | 0 records | 0 records | Handled cleanly |
| Deliberate failure | Non-zero exit | Exit code 1 | Captured in `deliberate-failure-output.txt` |

## Test Execution

Command: `python3 -m unittest discover -s ./applied-labs/r34-t055 -p "test_*.py"`
Result: 5 tests passed including regression test (saved in `test-output.txt`).
Deliberate failure test exited with code 1 and `AssertionError`.
