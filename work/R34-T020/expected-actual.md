# R34-T020 — Test Evidence

## Environment and tools

- Python: 3.13.15
- Git: 2.55.0
- Operating system: macOS 27.2.0, arm64
- Runtime and tests: Python standard library only

## Input fixtures

Inputs are saved in [`inputs/fixtures.json`](inputs/fixtures.json). The normal
case contains seven explicitly assigned tasks across IaaS, PaaS, and SaaS, with
customer, provider, and shared ownership represented. Separate fixtures show
missing and invalid ownership. The empty fixture is the boundary case.

## Expected versus actual

| Scenario | Expected | Actual |
|---|---|---|
| Normal | Seven fixture rows; every owner is customer, provider, or shared; deterministic order and output | Seven expected rows; output saved in `normal-output.txt` and matches the lesson |
| Empty boundary | Empty matrix; header only; process succeeds | Header only; exit status 0; output saved in `boundary-output.txt` |
| Missing owner | `responsible_party` is `UNASSIGNED`; never silently provider | Covered by unittest and `check_results.py`; result is `UNASSIGNED` |
| Invalid owner | `responsible_party` is `INVALID` | Covered by unittest and `check_results.py`; result is `INVALID` for unknown strings and non-string values |
| Malformed rows | Explicit `MatrixInputError` for a non-list result, non-dictionary row, absent/empty task, or unsupported service model | All cases are rejected in unittest |
| Adapter failure | Clear error and a nonzero command exit status | `Error: responsibility adapter failed: mock source unavailable`; exit status 1; saved in `failure-output.txt` |

## Test command

```bash
python3 -m unittest discover -s ./applied-labs/r34-t020 -p "test_*.py"
```

Actual result, saved in `test-output.txt`:

```text
...........
----------------------------------------------------------------------
Ran 11 tests in 0.000s

OK
```

The tests cover the normal scenario, all three service models, each valid
owner, missing and invalid ownership, empty input, an adapter error, malformed
inputs, and a deliberately wrong expectation. The last test confirms the
wrong expectation raises `AssertionError` while keeping the normal suite green.

## Assertion check and deliberate failure

Run the standalone assertion check:

```bash
python3 ./work/R34-T020/check_results.py
```

It exits successfully when its checks hold. To demonstrate failure without
changing the normal tests:

```bash
python3 ./work/R34-T020/check_results.py --deliberate-wrong-result
```

That command asserts that the first fixture's customer owner is `provider`.
The actual value is `customer`; the captured result is `AssertionError` and
process exit status 1 (`deliberate-failure-output.txt`).

## Process runs

The normal, boundary, failure, and deliberate-failure commands were run as
separate fresh Python processes. Their captured outputs are:

- `normal-output.txt`
- `boundary-output.txt`
- `failure-output.txt`
- `deliberate-failure-output.txt`

All records are local deterministic mock data. They establish no real cloud
provider or hardware behavior, security guarantee, or trained-model
performance.
