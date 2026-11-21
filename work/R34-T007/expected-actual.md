# Expected vs Actual Results for R34-T007

| Scenario | Asset | Threat | Expected Status | Actual Status | Match |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Normal | Corporate Employee Laptops | Spear-phishing attachment executing ransomware | PASS | PASS | YES |
| Missing Asset | (empty string) | Credential stuffing attack against portal | FAIL | FAIL | YES |
| Unrelated Control | Corporate Mail Server | Distributed Denial of Service (DDoS) | FLAGGED_FOR_REVIEW | FLAGGED_FOR_REVIEW | YES |

## Test Suite Execution
- **Command**: `python3 -m unittest discover -s ./applied-labs/r34-t007 -p "test_*.py"`
- **Result**: OK
