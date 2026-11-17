# Test Evidence: R34-T053 Bounded Conversation Memory

## Environment and Tools

- Python: 3.9.6
- Git: git version 2.50.1 (Apple Git-155)
- Platform: Darwin arm64 (macOS)
- Runtime: Python standard library

## Input Fixtures

- Capacity: 3
- Records added in order: `[A, B, C, D]`

## Expected vs Actual

| Scenario | Expected | Actual | Details |
|---|---|---|---|
| Bounded retention | `['B', 'C', 'D']` | `['B', 'C', 'D']` | Oldest record 'A' evicted when 'D' added |
| Immutability | Stored remains `['B', 'C', 'D']` | Stored remains `['B', 'C', 'D']` | Caller mutation of returned list or dict does not affect internal memory |
| State trace | 5 states (init + 4 adds) | 5 states | Step-by-step audit trace captured accurately |
| Boundary case | Count <= capacity | Handled cleanly | 0 or 1 record stored without eviction |
| Deliberate failure | Non-zero exit | Exit code 1 | Captured in `deliberate-failure-output.txt` |

## Test Execution

Command: `python3 -m unittest discover -s ./applied-labs/r34-t053 -p "test_*.py"`
Result: 5 tests passed (saved in `test-output.txt`).
Deliberate failure test exited with code 1 and `AssertionError`.
