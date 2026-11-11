# R34-T044 check evidence

Environment: Python 3.14.6, standard library, local checkout.

## Example inputs and outputs

See the [worked inputs and expected output](../../applied-labs/r34-t044/README.md).
Run `python3 applied-labs/r34-t044/example.py` from the checkout root.
Expected exit code 0 and an exact match to the documented output.
Actual exit code 0. The output matched line for line.

```text
Negotiated capabilities: ['tools']
Call to 'tools': status=SUCCESS, output=Executed tool action: query_siem
Call to 'resources': status=REJECTED, error=UNNEGOTIATED_CAPABILITY
```

## Unit tests

```sh
python3 -m unittest discover -s ./applied-labs/r34-t044 -p "test_*.py"
```

Expected all tests to pass with exit code 0 and a nonzero test count.
Actual exit code 0.

```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.039s

OK
```

## Deliberate failure

In a temporary copy, bypass the check for unnegotiated capabilities. Run the same unit test command in that copy.

Expected at least one assertion failure and a nonzero exit code.
Actual exit code 1 with 4 assertion failure(s).
The original source stayed in place.

```text
.FFFF..
======================================================================
FAIL: test_calling_unnegotiated_capability_is_rejected_before_dispatch (test_example.CapabilityNegotiationTests.test_calling_unnegotiated_capability_is_rejected_before_dispatch)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t044/test_example.py", line 37, in test_calling_unnegotiated_capability_is_rejected_before_dispatch
    CAPABILITY_HANDLERS["resources"].assert_not_called()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/usr/local/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/unittest/mock.py", line 947, in assert_not_called
    raise AssertionError(msg)
AssertionError: Expected 'mock' to not have been called. Called 1 times.
Calls: [call({'uri': 'file:///var/log/audit.log'})].

======================================================================
FAIL: test_disjoint_capabilities_yields_empty_negotiation (test_example.CapabilityNegotiationTests.test_disjoint_capabilities_yields_empty_negotiation)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t044/test_example.py", line 76, in test_disjoint_capabilities_yields_empty_negotiation
    self.assertEqual(res["status"], "REJECTED")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'SUCCESS' != 'REJECTED'
- SUCCESS
+ REJECTED


======================================================================
FAIL: test_documented_command_output (test_example.CapabilityNegotiationTests.test_documented_command_output)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t044/test_example.py", line 63, in test_documented_command_output
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        result.stdout.splitlines(),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<4 lines>...
        ],
        ^^
    )
    ^
AssertionError: Lists differ: ["Neg[134 chars]atus=SUCCESS, output=Accessed resource: file:/[16 chars]log"] != ["Neg[134 chars]atus=REJECTED, error=UNNEGOTIATED_CAPABILITY"]

First differing element 2:
"Call[19 chars]atus=SUCCESS, output=Accessed resource: file:/[15 chars].log"
"Call[19 chars]atus=REJECTED, error=UNNEGOTIATED_CAPABILITY"

  ["Negotiated capabilities: ['tools']",
   "Call to 'tools': status=SUCCESS, output=Executed tool action: query_siem",
+  "Call to 'resources': status=REJECTED, error=UNNEGOTIATED_CAPABILITY"]
-  "Call to 'resources': status=SUCCESS, output=Accessed resource: "
-  'file:///var/log/audit.log']

======================================================================
FAIL: test_exact_issue_fixture_regression (test_example.CapabilityNegotiationTests.test_exact_issue_fixture_regression)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private<temporary copy>/applied-labs/r34-t044/test_example.py", line 54, in test_exact_issue_fixture_regression
    self.assertEqual(res_resources["status"], "REJECTED")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'SUCCESS' != 'REJECTED'
- SUCCESS
+ REJECTED


----------------------------------------------------------------------
Ran 7 tests in 0.038s

FAILED (failures=4)
```
