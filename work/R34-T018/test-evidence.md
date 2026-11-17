# R34-T018 — Test Evidence

## Environment

- Python: 3.13.15
- Git: 2.55.0
- Operating system: macOS 27.2.0, arm64
- Test framework: Python standard-library `unittest`
- Dependencies: none beyond Python 3

## Fixed-label example

Invocation:

```bash
python3 ./applied-labs/r34-t018/example.py
```

The true-label fixture is `y_true=[1,1,0,0]`. Positive means label `1`; every prediction configuration is compared against that same fixture.

| Configuration | `y_pred` | Expected TP/FN/FP/TN | Actual TP/FN/FP/TN | Expected precision/recall | Actual precision/recall |
|---|---|---|---|---|---|
| Balanced example | `[1,0,1,0]` | `1/1/1/1` | `1/1/1/1` | `0.500/0.500` | `0.500/0.500` |
| Recall-oriented predictions | `[1,1,1,0]` | `2/0/1/1` | `2/0/1/1` | `0.667/1.000` | `0.667/1.000` |
| Precision-oriented predictions | `[1,0,0,0]` | `1/1/0/2` | `1/1/0/2` | `1.000/0.500` | `1.000/0.500` |

Observed trade-off: compared with the precision-oriented configuration, the recall-oriented configuration raises recall from `0.500` to `1.000` and lowers precision from `1.000` to `0.667`. These are exact counts over small mock fixtures, not a model benchmark or a claim about real-world accuracy.

## Boundary and failure cases

- No positive predictions: `y_true=[1,1,0,0]`, `y_pred=[0,0,0,0]`; expected and actual counts are `TP=0, FN=2, FP=0, TN=2`; expected and actual precision/recall are `0.000/0.000`. Precision is defined as zero when `TP + FP == 0`.
- No positive true labels: `y_true=[0,0]`, `y_pred=[0,1]`; expected and actual recall are `0.000`. Recall is defined as zero when `TP + FN == 0`.
- Unequal sequence lengths, non-binary labels, and empty sequences each raise `ValueError`.

## Test run

Command:

```bash
python3 -m unittest discover -s ./applied-labs/r34-t018 -p "test_*.py"
```

Expected: seven tests pass.

Actual:

```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.000s

OK
```

## Deliberately wrong expected result

A fresh `unittest` process asserted that the known fixture had `TP=2` instead of `TP=1`.

Expected: the assertion fails and the test process exits non-zero.

Actual: `AssertionError: 1 != 2`; `FAILED (failures=1)`; process exit status `1`.

## Scope

The example is a deterministic local simulation using fixed integer labels. It does not load or train a model and does not call a cloud provider or physical device. The balanced four-label fixture illustrates the metric arithmetic only; it does not represent class prevalence or evaluate any real system.
