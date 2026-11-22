# R34-T022 Verification Evidence

## Environment

- Python `3.9.6`
- Standard library only
- Command:
  `python3 -m unittest discover -s ./applied-labs/r34-t022 -p "test_*.py"`

## Smallest Valid Boundary

- Asset: `Server`
- Threat: `known server vulnerability`
- Control: `apply vendor patch`
- Residual risk: `zero-day risk remains`
- Expected: `pass`
- Actual: `pass`

## Boundary Control

- Asset: `Cloud storage bucket`
- Threat: `public cloud misconfiguration`
- Control: `container image patch`
- Exact boundary decision: non-empty and unrelated to the named threat
- Expected: `review`
- Actual: `review`

## Invalid Missing Asset

- Asset: empty
- Remaining fields: present
- Exact boundary decision: empty required field
- Expected: `fail`
- Actual: `fail`

## Regression Suite

- Expected: 10 tests run, zero failures
- Actual: `Ran 10 tests in 0.000s`, `OK`
