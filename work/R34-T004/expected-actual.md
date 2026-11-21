# Expected vs Actual Results for R34-T004

| Capability Requested | Client Offered | Server Supported | Negotiated? | Expected Action | Actual Action | Match |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| tools | YES | YES | YES | DISPATCHED | DISPATCHED | YES |
| resources | YES | NO | NO | REJECTED | REJECTED | YES |
| prompts | NO | YES | NO | REJECTED | REJECTED | YES |

## Test Suite Execution
- **Command**: `python3 -m unittest discover -s ./applied-labs/r34-t004 -p "test_*.py"`
- **Result**: OK
