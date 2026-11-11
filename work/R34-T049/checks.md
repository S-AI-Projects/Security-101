# R34-T049 check evidence

Environment: Python 3.14.6, standard library, local checkout.

## Example inputs and outputs

See the [worked inputs and expected output](../../applied-labs/r34-t049/README.md).
Run `python3 applied-labs/r34-t049/example.py` from the checkout root.
Expected exit code 0 and an exact match to the documented output.
Actual exit code 0. The output matched line for line.

```text
Batch size 1: 1/1 exact matches, events examined = 1
Batch size 3: 3/3 exact matches, events examined = 3
Batch size 6: 6/6 exact matches, events examined = 9
```

## Unit tests

```sh
python3 -m unittest discover -s ./applied-labs/r34-t049 -p "test_*.py"
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

In a temporary copy, retain only the most recent label instead of accumulating all labels. Run the same unit test command in that copy.

Expected at least one assertion failure and a nonzero exit code.
Actual exit code 1 with 3 assertion failure(s).
The original source stayed in place.

```text
.FF.F
======================================================================
FAIL: test_every_scenario_matches_the_expected_set (test_example.ClassificationTests.test_every_scenario_matches_the_expected_set) (name='leaked and changed files')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t049/test_example.py", line 10, in test_every_scenario_matches_the_expected_set
    self.assertEqual(classify(events), expected)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Items in the second set but not the first:
'confidentiality'

======================================================================
FAIL: test_every_scenario_matches_the_expected_set (test_example.ClassificationTests.test_every_scenario_matches_the_expected_set) (name='compromised booking app')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t049/test_example.py", line 10, in test_every_scenario_matches_the_expected_set
    self.assertEqual(classify(events), expected)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Items in the second set but not the first:
'confidentiality'
'integrity'

======================================================================
FAIL: test_three_controlled_batch_sizes (test_example.ClassificationTests.test_three_controlled_batch_sizes) (size=6)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t049/test_example.py", line 15, in test_three_controlled_batch_sizes
    self.assertEqual(evaluate(SCENARIOS[:size]), expected)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Tuples differ: (4, 9) != (6, 9)

First differing element 0:
4
6

- (4, 9)
?  ^

+ (6, 9)
?  ^


----------------------------------------------------------------------
Ran 4 tests in 0.001s

FAILED (failures=3)
```
