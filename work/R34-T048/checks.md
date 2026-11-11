# R34-T048 check evidence

Environment: Python 3.14.6, standard library, local checkout.

## Example inputs and outputs

See the [worked inputs and expected output](../../applied-labs/r34-t048/README.md).
Run `python3 applied-labs/r34-t048/example.py` from the checkout root.
Expected exit code 0 and an exact match to the documented output.
Actual exit code 0. The output matched line for line.

```text
guest-segment: PASS
missing-asset: FAIL (asset is required)
mismatched-control: REVIEW (control needs a rationale)
```

## Unit tests

```sh
python3 -m unittest discover -s ./applied-labs/r34-t048 -p "test_*.py"
```

Expected all tests to pass with exit code 0 and a nonzero test count.
Actual exit code 0.

```text
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
```

## Deliberate failure

In a temporary copy, change the boundary policy to fail a complete answer with a control mismatch. Run the same unit test command in that copy.

Expected at least one assertion failure and a nonzero exit code.
Actual exit code 1 with 1 assertion failure(s).
The original source stayed in place.

```text
...F
======================================================================
FAIL: test_route_complete_control_mismatch_to_review (test_example.AssessmentTests.test_route_complete_control_mismatch_to_review)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t048/test_example.py", line 17, in test_route_complete_control_mismatch_to_review
    self.assertEqual(check_scenario(answer), "REVIEW (control needs a rationale)")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'FAIL (control needs a rationale)' != 'REVIEW (control needs a rationale)'
- FAIL (control needs a rationale)
? ^^ ^
+ REVIEW (control needs a rationale)
? ^^^ ^^


----------------------------------------------------------------------
Ran 4 tests in 0.005s

FAILED (failures=1)
```
