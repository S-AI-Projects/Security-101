# Expected vs Actual Results for R34-T001

| Scenario | Input Asset | Input Threat | Expected Status | Actual Status | Match |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Normal | Production Kubernetes Container Cluster | Unpatched container runtime vulnerability | PASS | PASS | YES |
| Missing Asset | (empty string) | Unauthorized SSH brute-force attack | FAIL | FAIL | YES |
| Unrelated Control | Payment Processing Database Host | Remote buffer overflow vulnerability | FLAGGED_FOR_REVIEW | FLAGGED_FOR_REVIEW | YES |

## Test Suite Execution
- **Command**: `python3 -m unittest discover -s ./applied-labs/r34-t001 -p "test_*.py"`
- **Result**: OK
