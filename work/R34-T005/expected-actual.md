# Expected vs Actual Results for R34-T005

| Scenario | Asset | Threat | Expected Status | Actual Status | Match |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Normal | Customer Credit Card Records | Data exfiltration via unencrypted public API | PASS | PASS | YES |
| Missing Asset | (empty string) | Unauthorized database backup exfiltration | FAIL | FAIL | YES |
| Unrelated Control | Patient Medical History Database | SQL injection exfiltrating records | FLAGGED_FOR_REVIEW | FLAGGED_FOR_REVIEW | YES |

## Test Suite Execution
- **Command**: `python3 -m unittest discover -s ./applied-labs/r34-t005 -p "test_*.py"`
- **Result**: OK
