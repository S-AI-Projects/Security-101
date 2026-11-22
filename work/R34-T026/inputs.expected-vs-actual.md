# R34-T026 Verification Evidence

## Environment

- `Python 3.9.6`
- Standard library only
- Command:
  `python3 -m unittest discover -s ./applied-labs/r34-t026 -p "test_*.py"`

## Canonical Fixture

- Input: `y_true=[1,1,0,0]`, `y_pred=[1,0,1,0]`
- Expected: `TP=1`, `FN=1`, `FP=1`, `TN=1`, `precision=0.5`,
  `recall=0.5`
- Actual: `TP=1`, `FN=1`, `FP=1`, `TN=1`, `precision=0.500`,
  `recall=0.500`
- Result: matched

## Boundary Fixture

- Input: `y_true=[1,1,0,0]`, `y_pred=[0,0,0,0]`
- Expected: `TP=0`, `FN=2`, `FP=0`, `TN=2`, `precision=0.0`,
  `recall=0.0`
- Actual: matched with `precision=0.000`, `recall=0.000`

- Input: `y_true=[0,0]`, `y_pred=[0,1]`
- Expected: `TP=0`, `FN=0`, `FP=1`, `TN=1`, `precision=0.0`,
  `recall=0.0`
- Actual: matched with `precision=0.000`, `recall=0.000`

## Failure Fixture

- Input: `y_true=[1,0]`, `y_pred=[1]`
- Expected: exit code `1` and
  `Mismatched sequence lengths: len(y_true)=2 != len(y_pred)=1`
- Actual: exit code `1` with the expected error

## Regression Suite

- Expected: 13 tests run, zero failures
- Actual: `Ran 13 tests in 0.001s`, `OK`
