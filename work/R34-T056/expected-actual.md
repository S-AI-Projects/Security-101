# Test Evidence: R34-T056 Binary Classification Evaluation

## Environment and Tools

- Python: 3.9.6
- Git: git version 2.50.1 (Apple Git-155)
- Platform: Darwin arm64 (macOS)
- Runtime: Python standard library

## Input Fixtures

- Normal: `y_true = [1, 1, 0, 0]`, `y_pred = [1, 0, 1, 0]`
- Boundary: `y_true = [1, 0]`, `y_pred = [0, 0]`

## Expected vs Actual

| Metric / Scenario | Expected | Actual | Details |
|---|---|---|---|
| TP / FN / FP / TN | 1 / 1 / 1 / 1 | 1 / 1 / 1 / 1 | Counts match expected contingency matrix |
| Precision | 0.5 | 0.5 | `1 / (1 + 1) = 0.5` |
| Recall | 0.5 | 0.5 | `1 / (1 + 1) = 0.5` |
| Zero-Denominator Precision | 0.0 | 0.0 | Safely handled via explicit zero-denominator policy |
| Refactoring Equivalence | 100% Match | 100% Match | Proven across all fixtures |
| Deliberate failure | Non-zero exit | Exit code 1 | Captured in `deliberate-failure-output.txt` |

## Test Execution

Command: `python3 -m unittest discover -s ./applied-labs/r34-t056 -p "test_*.py"`
Result: 7 tests passed (saved in `test-output.txt`).
Deliberate failure test exited with code 1 and `AssertionError`.
