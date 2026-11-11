# R34-T050 check evidence

Environment: Python 3.14.6, standard library, local checkout.

## Example inputs and outputs

See the [worked inputs and expected output](../../applied-labs/r34-t050/README.md).
Run `python3 applied-labs/r34-t050/example.py` from the checkout root.
Expected exit code 0 and an exact match to the documented output.
Actual exit code 0. The output matched line for line.

```text
stolen-password: PASS
missing-asset: FAIL (provide asset)
stale-access: REVIEW (control does not match the threat)
```

## Unit tests

```sh
python3 -m unittest discover -s ./applied-labs/r34-t050 -p "test_*.py"
```

Expected all tests to pass with exit code 0 and a nonzero test count.
Actual exit code 0.

```text
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

## Deliberate failure

In a temporary copy, return PASS even when the proposed control does not match the threat. Run the same unit test command in that copy.

Expected at least one assertion failure and a nonzero exit code.
Actual exit code 1 with 1 assertion failure(s).
The original source stayed in place.

```text
F..
======================================================================
FAIL: test_authentication_control_does_not_remove_an_old_role (test_example.RubricTests.test_authentication_control_does_not_remove_an_old_role)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t050/test_example.py", line 17, in test_authentication_control_does_not_remove_an_old_role
    self.assertEqual(check_scenario(answer), "REVIEW (control does not match the threat)")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'PASS' != 'REVIEW (control does not match the threat)'
- PASS
+ REVIEW (control does not match the threat)


----------------------------------------------------------------------
Ran 3 tests in 0.001s

FAILED (failures=1)
```
