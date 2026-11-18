# R34-T015 baseline and refactor results

The fixture inputs are in [`inputs/fixtures.json`](./inputs/fixtures.json).
Baseline fresh-process outputs are `baseline-*-output.txt`; final outputs are
`after-*-output.txt`. The refactored CLI is compared byte-for-byte, including
exit status, with those captured baseline outputs by
`applied-labs/r34-t015/check_results.py`.

| Scenario | Baseline result | Refactored result | Equivalence |
|---|---|---|---|
| Normal | `PASS`, exit 0 | `PASS`, exit 0 | Exact stdout and status match |
| Boundary | Missing `asset`, `FAIL`, exit 1 | Missing `asset`, `FAIL`, exit 1 | Exact stdout and status match |
| Failure | Control alignment `REVIEW`, exit 0 | Control alignment `REVIEW`, exit 0 | Exact stdout and status match |

`baseline-test-output.txt` records the initially passing baseline tests.
`test-output.txt` records tests after extraction of
`review_control_alignment`. `check-output.txt` records the comparison;
`deliberate-failure-output.txt` records its intentional assertion failure
against a wrong expected output. Tool and interpreter versions are in
`tool-versions.txt`.

The extracted helper checks only supplied category labels. Human review still
judges the scenario explanation and whether the control addresses the threat.
