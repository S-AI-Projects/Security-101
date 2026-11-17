# Test Evidence: R34-T054 Infrastructure Security Rubric with Adapter

## Environment and Tools

- Python: 3.9.6
- Git: git version 2.50.1 (Apple Git-155)
- Platform: Darwin arm64 (macOS)
- Runtime: Python standard library

## Input Fixtures

Documented in `inputs/fixtures.json` and retrieved via `LocalInfrastructureAdapter`:
- `Cloud compute cluster`: Complete specification (`PASS`)
- `Missing asset infrastructure scenario`: Blank asset (`FAIL`)
- `Mismatched infrastructure control`: Ransomware paired with badge readers (`FLAG_REVIEW`)

## Expected vs Actual

| Scenario | Expected | Actual | Details |
|---|---|---|---|
| Complete scenario | `PASS` | `PASS` | All fields present and patching control matches unpatched vulnerability |
| Missing asset | `FAIL` | `FAIL` | Rejected immediately due to blank `asset` field |
| Mismatched control | `FLAG_REVIEW` | `FLAG_REVIEW` | Control unrelated to threat; flagged for human review |
| Boundary empty | 0 records | 0 records | Custom empty adapter returns empty list without error |
| Deliberate failure | Non-zero exit | Exit code 1 | Captured in `deliberate-failure-output.txt` |

## Test Execution

Command: `python3 -m unittest discover -s ./applied-labs/r34-t054 -p "test_*.py"`
Result: 5 tests passed (saved in `test-output.txt`).
Deliberate failure test exited with code 1 and `AssertionError`.
