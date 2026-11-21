# Expected vs Actual Results for R34-T008

| Step | Scenario Type | Expected Status | Actual Status | System Recovered? |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Missing Asset (Invalid) | FAIL | FAIL | YES (Handled Error) |
| 2 | Normal (Valid) | PASS | PASS | YES (Clean Execution) |
| 3 | Unrelated Control | FLAGGED_FOR_REVIEW | FLAGGED_FOR_REVIEW | YES |

## Test Suite Execution
- **Command**: `python3 -m unittest discover -s ./applied-labs/r34-t008 -p "test_*.py"`
- **Result**: OK
