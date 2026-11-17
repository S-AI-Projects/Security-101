# Test Evidence: R34-T052 Zero Trust Capability Negotiation

## Environment and Tools

- Python: 3.9.6
- Git: git version 2.50.1 (Apple Git-155)
- Platform: Darwin arm64 (macOS)
- Runtime: Python standard library

## Input Fixtures

- Client capabilities: `{"tools", "resources"}`
- Server capabilities: `{"tools", "prompts"}`
- Smallest valid case: `{"tools"}` vs `{"tools"}`
- Boundary case: `{"resources"}` vs `{"prompts"}`

## Expected vs Actual

| Scenario | Expected | Actual | Details |
|---|---|---|---|
| Normal Negotiation | Intersection `{'tools'}` | `{'tools'}` | Exactly intersects both advertised sets |
| Dispatch 'tools' | `SUCCESS` | `SUCCESS` | Permitted because 'tools' is negotiated |
| Dispatch 'resources' | `REJECTED` | `REJECTED` | Blocked before dispatch; unnegotiated capability error raised |
| Boundary Disjoint | Empty set `set()` | `set()` | Disjoint capabilities yield 0 negotiated features |
| Deliberate Failure | Non-zero exit | Exit code 1 | Captured in `failure-output.txt` and `deliberate-failure-output.txt` |

## Test Execution

Command: `python3 -m unittest discover -s ./applied-labs/r34-t052 -p "test_*.py"`
Result: 6 tests passed (saved in `test-output.txt`).
Deliberate failure test exited with code 1 and `AssertionError`.
