# R34-T045 check evidence

Environment: Python 3.14.6, standard library, local checkout.

## Example inputs and outputs

See the [worked inputs and expected output](../../applied-labs/r34-t045/README.md).
Run `python3 applied-labs/r34-t045/example.py` from the checkout root.
Expected exit code 0 and an exact match to the documented output.
Actual exit code 0. The output matched line for line.

```text
public-store: PASS
missing-asset: FAIL (missing or invalid asset)
wrong-control: REVIEW (no matching control)
```

## Unit tests

```sh
python3 -m unittest discover -s ./applied-labs/r34-t045 -p "test_*.py"
```

Expected all tests to pass with exit code 0 and a nonzero test count.
Actual exit code 0.

```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
```

## Deliberate failure

In a temporary copy, skip the check that compares the proposed control with the catalog. Run the same unit test command in that copy.

Expected at least one assertion failure and a nonzero exit code.
Actual exit code 1 with 2 assertion failure(s).
The original source stayed in place.

```text
...FF
======================================================================
FAIL: test_unknown_threat_requires_review (test_example.RubricTests.test_unknown_threat_requires_review)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t045/test_example.py", line 23, in test_unknown_threat_requires_review
    self.assertEqual(check_scenario(answer, lookup_local_control),
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     "REVIEW (no matching control)")
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'PASS' != 'REVIEW (no matching control)'
- PASS
+ REVIEW (no matching control)


======================================================================
FAIL: test_unrelated_control_requires_review (test_example.RubricTests.test_unrelated_control_requires_review)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t045/test_example.py", line 18, in test_unrelated_control_requires_review
    self.assertEqual(check_scenario(SCENARIOS["wrong-control"], lookup_local_control),
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     "REVIEW (no matching control)")
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'PASS' != 'REVIEW (no matching control)'
- PASS
+ REVIEW (no matching control)


----------------------------------------------------------------------
Ran 5 tests in 0.005s

FAILED (failures=2)
```
