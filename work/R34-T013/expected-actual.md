# R34-T013 expected and actual results

The inputs are in [`inputs/fixtures.json`](./inputs/fixtures.json). The direct
implementation is `applied-labs/r34-t013/example.py`; the independent expected
results are the explicit table in `applied-labs/r34-t013/check_results.py`.
Both use the exact capability sets listed here.

| Scenario | Client | Server | Expected negotiated | Expected request | Expected dispatch | Actual |
|---|---|---|---|---|---|---|
| Normal | `tools`, `resources` | `tools`, `prompts` | `tools` | `tools` | Accepted, handler invoked | Match |
| Boundary | `resources` | `tools`, `prompts` | none | `tools` | Rejected, handler not invoked | Match |
| Failure | `tools`, `resources` | `tools`, `prompts` | `tools` | `resources` | Rejected, handler not invoked | Match |

The captured process outputs are `normal-output.txt`, `boundary-output.txt`,
and `failure-output.txt`. The boundary and failure CLI scenarios correctly exit
with status 1 because their requested capability is not negotiated. The check
script's deliberate-failure output records a nonzero assertion failure when
the expected result is intentionally changed.
