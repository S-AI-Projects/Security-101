# Expected vs Actual Results for R34-T002

| Role | Action | Resource | Expected Decision | Actual Decision | Match |
| :--- | :--- | :--- | :--- | :--- | :--- |
| reader | read | public | ALLOW | ALLOW | YES |
| reader | write | public | DENY | DENY | YES |
| auditor | audit | logs (Deny Override) | DENY | DENY | YES |
| stranger | read | public (Unknown Role) | DENY | DENY | YES |

## Test Suite Execution
- **Command**: `python3 -m unittest discover -s ./applied-labs/r34-t002 -p "test_*.py"`
- **Result**: OK
