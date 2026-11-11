# R34-T042 check evidence

Tools used are Python 3.14.6, its bundled `unittest` module, and 2.56.0 of Git. Each command ran in a fresh Python process.

## Fixture inputs

```json
{
  "add-success": [
    {"tool": "add", "args": {"a": 2, "b": 3}}
  ],
  "multiply-success": [
    {"tool": "multiply", "args": {"a": 2, "b": 3}}
  ],
  "unknown-tool-error": [
    {"tool": "quarantine_host", "args": {"a": 2, "b": 3}}
  ],
  "string-arg-error": [
    {"tool": "add", "args": {"a": "2", "b": 3}}
  ],
  "pipeline-fail-stop": [
    {"tool": "add", "args": {"a": "2", "b": 3}},
    {"tool": "multiply", "args": {"a": 2, "b": 3}}
  ],
  "pipeline-all-success": [
    {"tool": "add", "args": {"a": 2, "b": 3}},
    {"tool": "multiply", "args": {"a": 2, "b": 3}}
  ]
}
```

## Scenario run

```sh
python3 applied-labs/r34-t042/example.py
```

Expected output:

```text
add-success: status=SUCCESS, result=5, invariant=OK
multiply-success: status=SUCCESS, result=6, invariant=OK
unknown-tool-error: status=ERROR, error=UNKNOWN_TOOL, executed=1, blocked=0, invariant=OK
string-arg-error: status=ERROR, error=INVALID_ARGUMENT, executed=1, blocked=0, invariant=OK
pipeline-fail-stop: status=ERROR, error=INVALID_ARGUMENT, executed=1, blocked=1, invariant=OK
pipeline-all-success: status=SUCCESS, results=[5, 6], invariant=OK
```

Actual output (exit 0):

```text
add-success: status=SUCCESS, result=5, invariant=OK
multiply-success: status=SUCCESS, result=6, invariant=OK
unknown-tool-error: status=ERROR, error=UNKNOWN_TOOL, executed=1, blocked=0, invariant=OK
string-arg-error: status=ERROR, error=INVALID_ARGUMENT, executed=1, blocked=0, invariant=OK
pipeline-fail-stop: status=ERROR, error=INVALID_ARGUMENT, executed=1, blocked=1, invariant=OK
pipeline-all-success: status=SUCCESS, results=[5, 6], invariant=OK
```

The commands and expected outputs in `4.3 SecOps capabilities.md` and the lab guide match this run.

## Automated check

```sh
python3 -m unittest discover -s ./applied-labs/r34-t042 -p "test_*.py"
```

Expected 11 passing tests and exit code 0. Actual output (exit code 0):

```text
...........
----------------------------------------------------------------------
Ran 11 tests in 0.000s

OK
```

The test suite validates:
1. `add(2, 3)` returns `5`.
2. `multiply(2, 3)` returns `6`.
3. Unknown tool requests return structured `UNKNOWN_TOOL` errors.
4. Non-numeric parameter `a` returns structured `INVALID_ARGUMENT` errors.
5. In a pipeline with an error, the subsequent tool call is blocked and never executed.
6. Multi-step valid pipelines execute all steps sequentially and record complete intermediate state traces.
7. Corrupted trace states or altered final statuses fail the invariant verification checks.

## Deliberate failure

In a temporary directory copy of `applied-labs/r34-t042/`, change the `tool_add` implementation from `result = a + b` to `result = 999`. Run the automated check command in that directory.

Expected 11 tests, 3 failures, and non-zero exit code (exit 1). Actual result (exit code 1):

```text
F..F....F..
======================================================================
FAIL: test_add_success_returns_five (test_example.TypedToolDispatchTests.test_add_success_returns_five)
----------------------------------------------------------------------
Traceback (most recent call last):
  File ".../test_example.py", line 21, in test_add_success_returns_five
    self.assertEqual(output["final_result"], 5)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 999 != 5

======================================================================
FAIL: test_intermediate_state_trace_structure (test_example.TypedToolDispatchTests.test_intermediate_state_trace_structure)
----------------------------------------------------------------------
Traceback (most recent call last):
  File ".../test_example.py", line 126, in test_intermediate_state_trace_structure
    self.assertEqual(step["result"], 5)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
AssertionError: 999 != 5

======================================================================
FAIL: test_pipeline_all_success_executes_all_steps_and_records_trace (test_example.TypedToolDispatchTests.test_pipeline_all_success_executes_all_steps_and_records_trace)
----------------------------------------------------------------------
Traceback (most recent call last):
  File ".../test_example.py", line 103, in test_pipeline_all_success_executes_all_steps_and_records_trace
    self.assertEqual(output["results"], [5, 6])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Lists differ: [999, 6] != [5, 6]

First differing element 0:
999
5

- [999, 6]
+ [5, 6]

----------------------------------------------------------------------
Ran 11 tests in 0.001s

FAILED (failures=3)
```
