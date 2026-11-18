# R34-T017 expected and actual results

The inputs and recovery sequence are recorded in
[`inputs/fixtures.json`](./inputs/fixtures.json). The direct evaluator checks
four required fields and compares the fixture's declared threat/control
categories; it does not judge the prose.

| Case | Expected | Actual |
|---|---|---|
| Normal | Complete phishing scenario passes | `PASS` |
| Boundary | Missing `asset` is reported; command exits 1 | `FAIL`, missing `asset` |
| Failure | DDoS threat with credential-rotation control flagged for review | `REVIEW` |
| Recovery | Incomplete input fails, then valid input passes | `FAIL` for boundary, then `PASS` for normal |

`normal-output.txt`, `boundary-output.txt`, `failure-output.txt`, and
`recovery-output.txt` contain fresh-process output. `test-output.txt` records
the unittest count and result; `check-output.txt` records the independent
expected-output comparison. The deliberate wrong-result output is in
`deliberate-failure-output.txt` and exits nonzero with `AssertionError`.
Interpreter/tool versions are in `tool-versions.txt`.

All records are fictional local fixtures. The recovery case demonstrates the
checker processing the next input after an incomplete record without retaining
the prior failure.
