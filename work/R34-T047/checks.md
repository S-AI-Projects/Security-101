# R34-T047 check evidence

Environment: Python 3.14.6, standard library, local checkout.

## Example inputs and outputs

See the [worked inputs and expected output](../../applied-labs/r34-t047/README.md).
Run `python3 applied-labs/r34-t047/example.py` from the checkout root.
Expected exit code 0 and an exact match to the documented output.
Actual exit code 0. The output matched line for line.

```text
missing-asset: FAIL (provide asset)
corrected: PASS
unrelated-control: REVIEW (check threat and control)
```

## Unit tests

```sh
python3 -m unittest discover -s ./applied-labs/r34-t047 -p "test_*.py"
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

In a temporary copy, return PASS when a required field is missing. Run the same unit test command in that copy.

Expected at least one assertion failure and a nonzero exit code.
Actual exit code 1 with 5 assertion failure(s).
The original source stayed in place.

```text
FFFF.F
======================================================================
FAIL: test_each_required_field_can_be_reported (test_example.RubricTests.test_each_required_field_can_be_reported) (field='threat')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t047/test_example.py", line 28, in test_each_required_field_can_be_reported
    self.assertEqual(check_scenario(answer), f"FAIL (provide {field})")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'PASS' != 'FAIL (provide threat)'
- PASS
+ FAIL (provide threat)


======================================================================
FAIL: test_each_required_field_can_be_reported (test_example.RubricTests.test_each_required_field_can_be_reported) (field='control')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t047/test_example.py", line 28, in test_each_required_field_can_be_reported
    self.assertEqual(check_scenario(answer), f"FAIL (provide {field})")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'PASS' != 'FAIL (provide control)'
- PASS
+ FAIL (provide control)


======================================================================
FAIL: test_each_required_field_can_be_reported (test_example.RubricTests.test_each_required_field_can_be_reported) (field='residual_risk')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t047/test_example.py", line 28, in test_each_required_field_can_be_reported
    self.assertEqual(check_scenario(answer), f"FAIL (provide {field})")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'PASS' != 'FAIL (provide residual_risk)'
- PASS
+ FAIL (provide residual_risk)


======================================================================
FAIL: test_missing_asset_and_next_valid_input (test_example.RubricTests.test_missing_asset_and_next_valid_input)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t047/test_example.py", line 9, in test_missing_asset_and_next_valid_input
    self.assertEqual(check_scenario(invalid), "FAIL (provide asset)")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'PASS' != 'FAIL (provide asset)'
- PASS
+ FAIL (provide asset)


======================================================================
FAIL: test_whitespace_only_asset_fails (test_example.RubricTests.test_whitespace_only_asset_fails)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t047/test_example.py", line 17, in test_whitespace_only_asset_fails
    self.assertEqual(check_scenario(answer), "FAIL (provide asset)")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'PASS' != 'FAIL (provide asset)'
- PASS
+ FAIL (provide asset)


----------------------------------------------------------------------
Ran 4 tests in 0.001s

FAILED (failures=5)
```
