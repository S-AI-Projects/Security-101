# R34-T014 expected and actual results

The exact input fields and declared categories are recorded in
[`inputs/fixtures.json`](./inputs/fixtures.json). Full pipeline snapshots for
each input are in [`intermediate-states.json`](./intermediate-states.json).
The direct implementation is `applied-labs/r34-t014/example.py`; independent
expected process results are recorded in
`applied-labs/r34-t014/check_results.py`.

| Scenario | Expected structural result | Expected control review | Expected process status | Actual |
|---|---|---|---:|---|
| Normal | All four required fields present | `matched` | 0 | Match: `PASS` |
| Boundary | Missing `asset` | `matched` | 1 | Match: `FAIL` |
| Failure | All four required fields present | `review` due to differing declared categories | 0 | Match: `REVIEW` |

`normal-output.txt`, `boundary-output.txt`, and `failure-output.txt` contain the
fresh-process outputs. `test-output.txt` records the unit test count and result;
`check-output.txt` records the direct-vs-expected comparison. The deliberate
wrong-result run is saved in `deliberate-failure-output.txt` and exits nonzero
with `AssertionError`.

The checker verifies required fields, compares the declared threat and control
categories, and validates that the final result recomputes from the recorded
intermediate state. It does not interpret prose or decide whether a control is
actually adequate; that explanation requires human review.
