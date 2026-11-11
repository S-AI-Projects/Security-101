# Typed tool dispatch and state invariant exercise

SecOps teams use Security Orchestration, Automation, and Response (SOAR) playbooks to automate incident response. Automated playbooks invoke containment and remediation tools. To prevent accidental damage or malicious input execution, playbooks must validate tool names, enforce strict parameter types, return structured error envelopes, and stop execution immediately when a step fails.

This exercise provides a local contract fixture that dispatches JSON tool calls with strict type validation, tracks the intermediate execution state at each step, and tests the invariant that links that state to the final output.

## Run the exercise

Use Python 3 with its standard library. Run both commands from the root of a local checkout:

```sh
python3 applied-labs/r34-t042/example.py
python3 -m unittest discover -s ./applied-labs/r34-t042 -p "test_*.py"
```

## Scenarios and expected results

`example.py` executes six fixtures and verifies state invariants after each run.

| Fixture | Tool Call / Input | Validation Rule | Expected Status | Final Result / Error | Invariant |
| --- | --- | --- | --- | --- | --- |
| `add-success` | `add(2, 3)` | Allowlisted tool; numbers `a` and `b` | `SUCCESS` | `5` | `OK` |
| `multiply-success` | `multiply(2, 3)` | Allowlisted tool; numbers `a` and `b` | `SUCCESS` | `6` | `OK` |
| `unknown-tool-error` | `quarantine_host(2, 3)` | Tool name not in allowlist | `ERROR` | `UNKNOWN_TOOL` | `OK` |
| `string-arg-error` | `add("2", 3)` | Parameter `a` must be numeric | `ERROR` | `INVALID_ARGUMENT` | `OK` |
| `pipeline-fail-stop` | `[add("2", 3), multiply(2, 3)]` | Step 1 fails; step 2 is blocked | `ERROR` | `INVALID_ARGUMENT` (executed=1, blocked=1) | `OK` |
| `pipeline-all-success` | `[add(2, 3), multiply(2, 3)]` | Both steps valid; sequential execution | `SUCCESS` | `results=[5, 6]` | `OK` |

Invocation output:

```text
add-success: status=SUCCESS, result=5, invariant=OK
multiply-success: status=SUCCESS, result=6, invariant=OK
unknown-tool-error: status=ERROR, error=UNKNOWN_TOOL, executed=1, blocked=0, invariant=OK
string-arg-error: status=ERROR, error=INVALID_ARGUMENT, executed=1, blocked=0, invariant=OK
pipeline-fail-stop: status=ERROR, error=INVALID_ARGUMENT, executed=1, blocked=1, invariant=OK
pipeline-all-success: status=SUCCESS, results=[5, 6], invariant=OK
```

## How the dispatcher decides

1. **Tool allowlist verification**: The dispatcher checks the `tool` field against `ALLOWLIST = {"add": tool_add, "multiply": tool_multiply}`. If the tool is missing from the allowlist, the dispatcher returns structured error code `UNKNOWN_TOOL` and stops further execution.
2. **Numeric argument validation**: The tool requires arguments `a` and `b`. The dispatcher verifies that both values are numbers (`int` or `float`) and rejects strings, booleans, or missing values with structured error code `INVALID_ARGUMENT`.
3. **Fail-stop pipeline protection**: When a tool call in a sequence fails, the dispatcher sets `halted = True`. It records subsequent calls as `BLOCKED` and does not call any tool function.
4. **Intermediate state trace**: After each step, the runner records a state object containing `step`, `tool`, `status`, `result`, `error`, and `halted`.
5. **State invariant verification**: The verifier checks that:
   - Total steps in the trace equal `steps_executed + steps_blocked`.
   - If any step fails with `ERROR`, all subsequent steps are `BLOCKED`, and the final status is `ERROR`.
   - The final error envelope matches the first failed step.
   - If all steps succeed, the final status is `SUCCESS`, and the final results match the intermediate trace results in exact order.

## Scope and limitations

This is a local contract fixture using the Python standard library. It does not implement remote network transport, the Model Context Protocol (MCP), cloud infrastructure, or trained AI models. It demonstrates the software invariants required for reliable, secure tool dispatch in automated security operations.
