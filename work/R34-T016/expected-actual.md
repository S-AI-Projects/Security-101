# R34-T016 expected and actual results

Inputs are recorded in [`inputs/fixtures.json`](./inputs/fixtures.json).
`check_results.py` launches each scenario in a fresh process and checks the
complete expected stdout, stderr, and exit status.

| Scenario | Input | Expected | Actual |
|---|---|---|---|
| Normal | `192.0.2.1` | In `192.0.2.0/24`, exit 0 | Match; `Allowlisted: yes` |
| Boundary | `198.51.100.1` | Not in `192.0.2.0/24`, exit 0 | Match; `Allowlisted: no` |
| Failure | `not-an-ip` | Raise `ValueError`, report error, exit 1 | Match; rejected |

`normal-output.txt`, `boundary-output.txt`, and `failure-output.txt` contain
the fresh-process outputs. `test-output.txt` records the unittest count and
result; `check-output.txt` records exact output comparisons. The deliberate
wrong-result run is saved in `deliberate-failure-output.txt` and exits nonzero
with `AssertionError`. Interpreter and tool versions are in
`tool-versions.txt`.

The standard-library `ipaddress` parser and membership check operate only on
these local strings. No network connection or scan is performed.
