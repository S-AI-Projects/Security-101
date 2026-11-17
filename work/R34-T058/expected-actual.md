# Test Evidence: R34-T058 Network Range Classification

## Environment and Tools

- Python: 3.9.6
- Git: git version 2.50.1 (Apple Git-155)
- Platform: Darwin arm64 (macOS)
- Runtime: Python standard library (`ipaddress`)

## Input Fixtures

- Network range: `192.0.2.0/24`
- Test addresses:
  - `192.0.2.1` -> Member
  - `198.51.100.1` -> Non-member
  - `999.999.999.999` -> Malformed
  - `""` -> Missing data

## Expected vs Actual

| Input IP | Expected Status | Actual Status | Details |
|---|---|---|---|
| `192.0.2.1` | `ALLOW` | `ALLOW` | In-subnet member verified |
| `198.51.100.1` | `DENY` | `DENY` | External IP outside CIDR |
| `999.999.999.999` | `ERROR` | `ERROR` | `MALFORMED_IP` structured error returned |
| `""` | `ERROR` | `ERROR` | `MISSING_DATA` structured error returned |
| Recovery on next valid | `ALLOW` | `ALLOW` | Following error, parser handles next valid input cleanly |
| Deliberate failure | Non-zero exit | Exit code 1 | Captured in `deliberate-failure-output.txt` |

## Test Execution

Command: `python3 -m unittest discover -s ./applied-labs/r34-t058 -p "test_*.py"`
Result: 6 tests passed (saved in `test-output.txt`).
Deliberate failure test exited with code 1 and `AssertionError`.
