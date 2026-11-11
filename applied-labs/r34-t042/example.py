"""Local contract fixture for typed tool dispatch with intermediate state trace and invariants."""

import json
from typing import Any, Callable

# Explicit allowlist mapping tool names to implementation functions
def tool_add(a: int | float, b: int | float) -> int | float:
    """Return the sum of two numbers."""
    result = a + b
    return int(result) if isinstance(result, float) and result.is_integer() else result


def tool_multiply(a: int | float, b: int | float) -> int | float:
    """Return the product of two numbers."""
    result = a * b
    return int(result) if isinstance(result, float) and result.is_integer() else result


ALLOWLIST: dict[str, Callable[[int | float, int | float], int | float]] = {
    "add": tool_add,
    "multiply": tool_multiply,
}


def parse_call_spec(spec: dict[str, Any] | str) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    """Parse a JSON string or dictionary into a call specification."""
    if isinstance(spec, str):
        try:
            parsed = json.loads(spec)
        except json.JSONDecodeError as exc:
            return None, {
                "code": "MALFORMED_JSON",
                "message": f"Invalid JSON string: {exc.msg}",
            }
    elif isinstance(spec, dict):
        parsed = spec
    else:
        return None, {
            "code": "INVALID_SPEC",
            "message": "Call specification must be a dictionary or JSON string",
        }

    if not isinstance(parsed, dict):
        return None, {
            "code": "INVALID_SPEC",
            "message": "Parsed call specification must be a JSON object",
        }

    return parsed, None


def validate_call(parsed: dict[str, Any]) -> tuple[str | None, dict[str, Any] | None, dict[str, str] | None]:
    """Validate tool name against allowlist and ensure numeric arguments."""
    tool_name = parsed.get("tool")
    if not isinstance(tool_name, str) or not tool_name:
        return None, None, {
            "code": "INVALID_SCHEMA",
            "message": "Field 'tool' must be a non-empty string",
        }

    if tool_name not in ALLOWLIST:
        return tool_name, None, {
            "code": "UNKNOWN_TOOL",
            "message": f"Tool '{tool_name}' is not in allowlist",
        }

    args = parsed.get("args")
    if not isinstance(args, dict):
        return tool_name, None, {
            "code": "INVALID_SCHEMA",
            "message": "Field 'args' must be a dictionary",
        }

    if "a" not in args or "b" not in args:
        return tool_name, None, {
            "code": "INVALID_ARGUMENT",
            "message": "Arguments 'a' and 'b' are required",
        }

    a = args["a"]
    b = args["b"]

    if not isinstance(a, (int, float)) or isinstance(a, bool):
        return tool_name, None, {
            "code": "INVALID_ARGUMENT",
            "message": "Argument 'a' must be a number",
        }

    if not isinstance(b, (int, float)) or isinstance(b, bool):
        return tool_name, None, {
            "code": "INVALID_ARGUMENT",
            "message": "Argument 'b' must be a number",
        }

    return tool_name, {"a": a, "b": b}, None


def execute_pipeline(call_specs: list[dict[str, Any] | str]) -> dict[str, Any]:
    """Execute a list of tool call specifications sequentially.

    Halts immediately upon encountering any error. Subsequent steps are blocked.
    Records intermediate state for every step.
    """
    trace: list[dict[str, Any]] = []
    accumulated_results: list[int | float] = []
    halted = False
    first_error: dict[str, str] | None = None

    for idx, spec in enumerate(call_specs, start=1):
        if halted:
            # Step blocked due to prior failure
            tool_name = "unknown"
            if isinstance(spec, dict):
                tool_name = str(spec.get("tool", "unknown"))
            elif isinstance(spec, str):
                try:
                    loaded = json.loads(spec)
                    if isinstance(loaded, dict):
                        tool_name = str(loaded.get("tool", "unknown"))
                except Exception:
                    pass

            step_record = {
                "step": idx,
                "tool": tool_name,
                "status": "BLOCKED",
                "result": None,
                "error": None,
                "halted": True,
            }
            trace.append(step_record)
            continue

        parsed, parse_error = parse_call_spec(spec)
        if parse_error:
            halted = True
            first_error = parse_error
            step_record = {
                "step": idx,
                "tool": "unknown",
                "status": "ERROR",
                "result": None,
                "error": parse_error,
                "halted": True,
            }
            trace.append(step_record)
            continue

        tool_name, validated_args, validation_error = validate_call(parsed)
        if validation_error:
            halted = True
            first_error = validation_error
            step_record = {
                "step": idx,
                "tool": tool_name or "unknown",
                "status": "ERROR",
                "result": None,
                "error": validation_error,
                "halted": True,
            }
            trace.append(step_record)
            continue

        # Execute tool function
        fn = ALLOWLIST[tool_name]
        try:
            res = fn(validated_args["a"], validated_args["b"])
            accumulated_results.append(res)
            step_record = {
                "step": idx,
                "tool": tool_name,
                "status": "SUCCESS",
                "result": res,
                "error": None,
                "halted": False,
            }
            trace.append(step_record)
        except Exception as exc:
            halted = True
            exec_error = {
                "code": "EXECUTION_ERROR",
                "message": f"Execution failed: {exc}",
            }
            first_error = exec_error
            step_record = {
                "step": idx,
                "tool": tool_name,
                "status": "ERROR",
                "result": None,
                "error": exec_error,
                "halted": True,
            }
            trace.append(step_record)

    steps_executed = sum(1 for s in trace if s["status"] in ("SUCCESS", "ERROR"))
    steps_blocked = sum(1 for s in trace if s["status"] == "BLOCKED")

    final_output = {
        "status": "ERROR" if halted else "SUCCESS",
        "final_result": accumulated_results[-1] if accumulated_results else None,
        "results": list(accumulated_results),
        "error": first_error,
        "steps_executed": steps_executed,
        "steps_blocked": steps_blocked,
        "trace": trace,
    }
    return final_output


def verify_pipeline_invariants(trace: list[dict[str, Any]], final_output: dict[str, Any]) -> tuple[bool, str]:
    """Verify invariants linking intermediate step state trace to final output.

    Invariants checked:
    1. Step count: len(trace) == steps_executed + steps_blocked.
    2. Fail-stop: If step i fails, all steps j > i are BLOCKED, and no tool executes after failure.
    3. Status consistency: Final status is ERROR if and only if any step is ERROR.
    4. Error propagation: Final error matches the error of the first failed step.
    5. Result consistency: Final results match exactly the results of SUCCESS steps.
    6. Monotonic halted state: Once halted is True, it remains True for all subsequent steps.
    """
    total_steps = len(trace)
    if total_steps != (final_output.get("steps_executed", 0) + final_output.get("steps_blocked", 0)):
        return False, "Total steps in trace does not match executed + blocked count"

    first_error_idx = None
    for idx, step in enumerate(trace):
        if step["status"] == "ERROR":
            first_error_idx = idx
            break

    if first_error_idx is not None:
        if final_output.get("status") != "ERROR":
            return False, "Final status must be ERROR when a step has failed"

        if final_output.get("error") != trace[first_error_idx]["error"]:
            return False, "Final error must match the first failed step error"

        # Verify all subsequent steps are BLOCKED
        for j in range(first_error_idx + 1, total_steps):
            if trace[j]["status"] != "BLOCKED":
                return False, f"Step {trace[j]['step']} after failure must be BLOCKED"
            if trace[j]["result"] is not None:
                return False, f"Blocked step {trace[j]['step']} must not have a result"
            if not trace[j]["halted"]:
                return False, f"Blocked step {trace[j]['step']} must have halted=True"

        # Verify halted monotonicity
        for j in range(first_error_idx, total_steps):
            if not trace[j]["halted"]:
                return False, f"Step {trace[j]['step']} must remain halted"
    else:
        if final_output.get("status") != "SUCCESS":
            return False, "Final status must be SUCCESS when all steps succeeded"
        if final_output.get("error") is not None:
            return False, "Final error must be None when all steps succeeded"
        for step in trace:
            if step["status"] != "SUCCESS":
                return False, f"Step {step['step']} must have SUCCESS status"
            if step["halted"]:
                return False, f"Successful step {step['step']} must not be halted"

    # Verify result sequence
    expected_results = [s["result"] for s in trace if s["status"] == "SUCCESS"]
    if final_output.get("results") != expected_results:
        return False, "Final results list does not match results in trace"

    if final_output.get("status") == "SUCCESS" and total_steps > 0:
        if final_output.get("final_result") != expected_results[-1]:
            return False, "Final result does not match last trace result"

    return True, "Invariants hold"


FIXTURES: dict[str, list[str]] = {
    "add-success": [
        json.dumps({"tool": "add", "args": {"a": 2, "b": 3}})
    ],
    "multiply-success": [
        json.dumps({"tool": "multiply", "args": {"a": 2, "b": 3}})
    ],
    "unknown-tool-error": [
        json.dumps({"tool": "quarantine_host", "args": {"a": 2, "b": 3}})
    ],
    "string-arg-error": [
        json.dumps({"tool": "add", "args": {"a": "2", "b": 3}})
    ],
    "pipeline-fail-stop": [
        json.dumps({"tool": "add", "args": {"a": "2", "b": 3}}),
        json.dumps({"tool": "multiply", "args": {"a": 2, "b": 3}}),
    ],
    "pipeline-all-success": [
        json.dumps({"tool": "add", "args": {"a": 2, "b": 3}}),
        json.dumps({"tool": "multiply", "args": {"a": 2, "b": 3}}),
    ],
}


def run_fixture(name: str, steps: list[str]) -> tuple[dict[str, Any], bool, str]:
    """Execute a fixture and verify its state invariants."""
    output = execute_pipeline(steps)
    valid, message = verify_pipeline_invariants(output["trace"], output)
    return output, valid, message


if __name__ == "__main__":
    for name, fixture in FIXTURES.items():
        output, valid, message = run_fixture(name, fixture)
        status = output["status"]
        inv_str = "OK" if valid else f"FAIL({message})"
        if status == "SUCCESS":
            if len(fixture) == 1:
                detail = f"result={output['final_result']}"
            else:
                detail = f"results={output['results']}"
            print(f"{name}: status={status}, {detail}, invariant={inv_str}")
        else:
            err = output["error"]["code"]
            exec_cnt = output["steps_executed"]
            block_cnt = output["steps_blocked"]
            print(f"{name}: status={status}, error={err}, executed={exec_cnt}, blocked={block_cnt}, invariant={inv_str}")
