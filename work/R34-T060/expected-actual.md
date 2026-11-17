# Test Evidence: R34-T060 Network Security Scenario Rubric Comparison

## Environment and Tools

- Python: 3.9.6
- Git: git version 2.50.1 (Apple Git-155)
- Platform: Darwin arm64 (macOS)
- Runtime: Python standard library

## Input Fixtures

- `Corporate VLAN Gateway`: Complete segmentation scenario (`PASS`)
- `Missing asset network scenario`: Blank asset (`FAIL`)
- `Mismatched network security control`: BGP route hijacking paired with Wi-Fi WPA3 (`FLAG_REVIEW`)

## Expected vs Actual

| Scenario | Direct Expected | Independent Expected | Direct Actual | Independent Actual | Agreement |
|---|---|---|---|---|---|
| Corporate VLAN Gateway | `PASS` | `PASS` | `PASS` | `PASS` | 100% |
| Missing asset | `FAIL` | `FAIL` | `FAIL` | `FAIL` | 100% |
| Mismatched control | `FLAG_REVIEW` | `FLAG_REVIEW` | `FLAG_REVIEW` | `FLAG_REVIEW` | 100% |
| Boundary empty | `FAIL` | `FAIL` | `FAIL` | `FAIL` | 100% |
| Deliberate failure | Non-zero exit | Non-zero exit | Exit code 1 | Exit code 1 | Verified |

## Test Execution

Command: `python3 -m unittest discover -s ./applied-labs/r34-t060 -p "test_*.py"`
Result: 5 tests passed (saved in `test-output.txt`).
Deliberate failure test exited with code 1 and `AssertionError` (saved in `deliberate-failure-output.txt`).
