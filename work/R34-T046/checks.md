# R34-T046 check evidence

Environment: Python 3.14.6, standard library, local checkout.

## Example inputs and outputs

See the [worked inputs and expected output](../../applied-labs/r34-t046/README.md).
Run `python3 applied-labs/r34-t046/example.py` from the checkout root.
Expected exit code 0 and an exact match to the documented output.
Actual exit code 0. The output matched line for line.

```text
Negotiated: ['tools']
tools: ACCEPTED (mock tools handler)
resources: REJECTED (unnegotiated capability)
```

## Unit tests

```sh
python3 -m unittest discover -s ./applied-labs/r34-t046 -p "test_*.py"
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

In a temporary copy, change the intersection to a union so a feature that only one peer offers appears in the agreed list. Run the same unit test command in that copy.

Expected at least one assertion failure and a nonzero exit code.
Actual exit code 1 with 7 assertion failure(s).
The original source stayed in place.

```text
FFFFFFF
======================================================================
FAIL: test_baseline_and_refactor_match (test_example.CapabilityTests.test_baseline_and_refactor_match) (client=frozenset({'resources', 'tools'}), server=frozenset({'tools', 'prompts'}), capability='resources')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t046/test_example.py", line 41, in test_baseline_and_refactor_match
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        dispatch(client, server, capability, after),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        baseline_dispatch(client, server, capability, before),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'ACCEPTED (mock resources handler)' != 'REJECTED (unnegotiated capability)'
- ACCEPTED (mock resources handler)
+ REJECTED (unnegotiated capability)


======================================================================
FAIL: test_baseline_and_refactor_match (test_example.CapabilityTests.test_baseline_and_refactor_match) (client=frozenset({'resources', 'tools'}), server=frozenset({'tools', 'prompts'}), capability='prompts')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t046/test_example.py", line 41, in test_baseline_and_refactor_match
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        dispatch(client, server, capability, after),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        baseline_dispatch(client, server, capability, before),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'ACCEPTED (mock prompts handler)' != 'REJECTED (unnegotiated capability)'
- ACCEPTED (mock prompts handler)
+ REJECTED (unnegotiated capability)


======================================================================
FAIL: test_baseline_and_refactor_match (test_example.CapabilityTests.test_baseline_and_refactor_match) (client=frozenset({'resources', 'tools'}), server=frozenset(), capability='tools')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t046/test_example.py", line 41, in test_baseline_and_refactor_match
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        dispatch(client, server, capability, after),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        baseline_dispatch(client, server, capability, before),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'ACCEPTED (mock tools handler)' != 'REJECTED (unnegotiated capability)'
- ACCEPTED (mock tools handler)
+ REJECTED (unnegotiated capability)


======================================================================
FAIL: test_baseline_and_refactor_match (test_example.CapabilityTests.test_baseline_and_refactor_match) (client=frozenset({'resources', 'tools'}), server=frozenset(), capability='resources')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t046/test_example.py", line 41, in test_baseline_and_refactor_match
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        dispatch(client, server, capability, after),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        baseline_dispatch(client, server, capability, before),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'ACCEPTED (mock resources handler)' != 'REJECTED (unnegotiated capability)'
- ACCEPTED (mock resources handler)
+ REJECTED (unnegotiated capability)


======================================================================
FAIL: test_empty_overlap_rejects_all_requests (test_example.CapabilityTests.test_empty_overlap_rejects_all_requests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t046/test_example.py", line 30, in test_empty_overlap_rejects_all_requests
    self.assertEqual(negotiate(CLIENT, server), set())
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: frozenset({'resources', 'tools', 'prompts'}) != set()

======================================================================
FAIL: test_only_negotiated_capability_dispatches (test_example.CapabilityTests.test_only_negotiated_capability_dispatches)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t046/test_example.py", line 23, in test_only_negotiated_capability_dispatches
    self.assertEqual(dispatch(CLIENT, SERVER, "resources", handle),
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     "REJECTED (unnegotiated capability)")
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'ACCEPTED (mock resources handler)' != 'REJECTED (unnegotiated capability)'
- ACCEPTED (mock resources handler)
+ REJECTED (unnegotiated capability)


======================================================================
FAIL: test_required_intersection (test_example.CapabilityTests.test_required_intersection)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t046/test_example.py", line 17, in test_required_intersection
    self.assertEqual(negotiate(CLIENT, SERVER), {"tools"})
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: frozenset({'resources', 'tools', 'prompts'}) != {'tools'}

----------------------------------------------------------------------
Ran 4 tests in 0.006s

FAILED (failures=7)
```
