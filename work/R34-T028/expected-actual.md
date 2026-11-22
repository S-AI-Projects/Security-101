# Test Evidence: R34-T028 Network Range Classification & Error Recovery

## Environment and Tool Versions

- **Python**: Python 3.9.6
- **Git**: git version 2.50.1 (Apple Git-155)
- **Operating System**: Darwin 27.2.0 arm64 (macOS)
- **Dependencies**: Python standard library only (`ipaddress`, `argparse`, `sys`, `unittest`)

## Network CIDR & Sample Addresses Summary

- **Allowlist Network**: `192.0.2.0/24` (RFC 5737 TEST-NET-1 documentation block)
- **Sample Addresses Evaluated**:
  - `192.0.2.1`: Valid IPv4 within subnet range
  - `198.51.100.1`: Valid IPv4 outside subnet range (TEST-NET-2)
  - `invalid-ip-string`: Malformed string violating IPv4/IPv6 syntax
  - `""`: Missing input data
  - `192.0.2.42`: Valid IPv4 inside subnet range (proves recovery following error)

## Expected vs Actual Results

| Check / Scenario | Command / Target | Expected Status / Value | Actual Status / Value | Details |
| :--- | :--- | :--- | :--- | :--- |
| In-network Member | `classify_address("192.0.2.1")` | `ALLOW`, `is_member=True` | `ALLOW`, `is_member=True` | Belongs to `192.0.2.0/24` |
| Non-member IP | `classify_address("198.51.100.1")` | `DENY`, `is_member=False` | `DENY`, `is_member=False` | External address rejected |
| Malformed IP | `classify_address("invalid-ip-string")` | `ERROR`, `MALFORMED_IP` | `ERROR`, `MALFORMED_IP` | Structured error explanation returned |
| Missing Data | `classify_address("")` | `ERROR`, `MISSING_DATA` | `ERROR`, `MISSING_DATA` | Structured missing data error returned |
| Recovery on Next Valid | `classify_sequence(..., 192.0.2.42)` | `ALLOW`, `is_member=True` | `ALLOW`, `is_member=True` | State resilient, resumes normal classification |
| Network Boundary (0) | `classify_address("192.0.2.0")` | `ALLOW`, `is_member=True` | `ALLOW`, `is_member=True` | Network address member of subnet |
| Broadcast Boundary (255) | `classify_address("192.0.2.255")` | `ALLOW`, `is_member=True` | `ALLOW`, `is_member=True` | Broadcast address member of subnet |
| Adjacent Subnet | `classify_address("192.0.3.1")` | `DENY`, `is_member=False` | `DENY`, `is_member=False` | Outside subnet boundary |
| Failure Scenario | `example.py --scenario failure` | Exit code 1, `ValueError` | Exit code 1, `ValueError` | Rejects malformed CIDR `192.0.2.0/99` |
| Unit Test Suite | `unittest discover` | 12 passed, exit code 0 | 12 passed in 0.001s, exit code 0 | Non-zero test count, all assertions hold |
| Deliberate Failure | `check_results.py --deliberate-wrong-result` | Exit code 1, `AssertionError` | Exit code 1, `AssertionError` | Verifies assertion check fails on mismatch |

## Fresh Process Execution Evidence

- `work/R34-T028/normal-output.txt`: Captured output from running `example.py`
- `work/R34-T028/boundary-output.txt`: Captured output from running `example.py --scenario boundary`
- `work/R34-T028/failure-output.txt`: Captured output from running `example.py --scenario failure`
- `work/R34-T028/test-output.txt`: Captured output from running unit tests (12 tests passed)
- `work/R34-T028/deliberate-failure-output.txt`: Captured output from deliberate wrong assertion (exit code 1)
- `work/R34-T028/tool-versions.txt`: Environment tool version strings
