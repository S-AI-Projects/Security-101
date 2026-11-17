"""Typed Tool Dispatch with Allowlist and Argument Validation (R34-T057).

Extends 8.2 AI security capabilities.
Dispatches local JSON calls for add(a, b) and multiply(a, b) through an explicit allowlist
and strict numeric argument validation. Unknown tools and non-numeric arguments return
structured errors; failed calls abort immediately and cannot chain or execute another tool.
Includes applied scenario assessment questions with executable checks.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Dict, Optional, Tuple

ALLOWLISTED_TOOLS = {"add", "multiply"}


def execute_add(a: float, b: float) -> float:
    return a + b


def execute_multiply(a: float, b: float) -> float:
    return a * b


def dispatch_tool_call(call: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and dispatch a tool call JSON object.

    Expected format:
      {"tool": "add" | "multiply", "arguments": {"a": number, "b": number}}
    """
    tool_name = call.get("tool")
    arguments = call.get("arguments")

    # 1. Tool Allowlist Validation
    if tool_name not in ALLOWLISTED_TOOLS:
        return {
            "status": "ERROR",
            "error_type": "UNKNOWN_TOOL",
            "message": f"Tool '{tool_name}' is not in the allowlist. Allowed tools: {sorted(list(ALLOWLISTED_TOOLS))}",
        }

    # 2. Arguments Structure Validation
    if not isinstance(arguments, dict):
        return {
            "status": "ERROR",
            "error_type": "INVALID_ARGUMENT",
            "message": f"Arguments must be a JSON dictionary, received {type(arguments).__name__}",
        }

    for param in ("a", "b"):
        if param not in arguments:
            return {
                "status": "ERROR",
                "error_type": "MISSING_ARGUMENT",
                "message": f"Missing required parameter '{param}'",
            }
        val = arguments[param]
        # In Python, bool is a subclass of int (isinstance(True, int) is True), so check bool explicitly
        if isinstance(val, bool) or not isinstance(val, (int, float)):
            return {
                "status": "ERROR",
                "error_type": "INVALID_ARGUMENT",
                "message": f"Parameter '{param}' must be numeric (int or float), received {type(val).__name__}",
            }

    a = arguments["a"]
    b = arguments["b"]

    # 3. Execution (Single call; no secondary fallback execution allowed)
    if tool_name == "add":
        result = execute_add(a, b)
    elif tool_name == "multiply":
        result = execute_multiply(a, b)
    else:
        # Defensive fallback
        return {
            "status": "ERROR",
            "error_type": "UNKNOWN_TOOL",
            "message": "Tool execution rejected",
        }

    return {
        "status": "SUCCESS",
        "tool": tool_name,
        "result": result,
    }


def get_scenario_assessment_questions() -> Dict[str, Dict[str, Any]]:
    """Three applied questions about the local example with rationale and expected answers."""
    return {
        "question_1_predict_output": {
            "question": "What is the exact output of dispatching add(2, 3)?",
            "input": {"tool": "add", "arguments": {"a": 2, "b": 3}},
            "expected_output": {"status": "SUCCESS", "tool": "add", "result": 5},
            "rationale": "'add' is allowlisted and both parameters are valid integers; output is 5.",
        },
        "question_2_diagnose_failure": {
            "question": "Why does dispatching multiply('2', 3) fail?",
            "input": {"tool": "multiply", "arguments": {"a": "2", "b": 3}},
            "expected_error_type": "INVALID_ARGUMENT",
            "rationale": "String '2' violates numeric type contract and is rejected during pre-execution schema check.",
        },
        "question_3_choose_boundary_policy": {
            "question": "What boundary policy governs an unlisted tool call (e.g. 'system_exec')?",
            "input": {"tool": "system_exec", "arguments": {"cmd": "id"}},
            "expected_error_type": "UNKNOWN_TOOL",
            "rationale": "Strict allowlisting rejects unknown tools before invocation, preventing unauthorized tool execution.",
        },
    }


def run_demonstration(scenario: str) -> int:
    print(f"Scenario: {scenario}")

    if scenario == "normal":
        # 1. Normal valid calls
        call_add = {"tool": "add", "arguments": {"a": 2, "b": 3}}
        res_add = dispatch_tool_call(call_add)
        print(f"Dispatch add(2, 3): {res_add}")
        assert res_add["status"] == "SUCCESS"
        assert res_add["result"] == 5

        call_mult = {"tool": "multiply", "arguments": {"a": 2, "b": 3}}
        res_mult = dispatch_tool_call(call_mult)
        print(f"Dispatch multiply(2, 3): {res_mult}")
        assert res_mult["status"] == "SUCCESS"
        assert res_mult["result"] == 6

        # 2. Unknown tool
        call_unknown = {"tool": "system_exec", "arguments": {"a": 1, "b": 2}}
        res_unknown = dispatch_tool_call(call_unknown)
        print(f"Dispatch unknown tool: {res_unknown}")
        assert res_unknown["status"] == "ERROR"
        assert res_unknown["error_type"] == "UNKNOWN_TOOL"

        # 3. String argument error
        call_str = {"tool": "add", "arguments": {"a": "2", "b": 3}}
        res_str = dispatch_tool_call(call_str)
        print(f"Dispatch invalid arg type: {res_str}")
        assert res_str["status"] == "ERROR"
        assert res_str["error_type"] == "INVALID_ARGUMENT"

        return 0

    elif scenario == "boundary":
        # Boundary: Float values and empty arguments dict
        call_float = {"tool": "add", "arguments": {"a": 2.5, "b": 1.5}}
        res_float = dispatch_tool_call(call_float)
        print(f"Boundary float: {res_float}")
        assert res_float["result"] == 4.0

        call_empty = {"tool": "add", "arguments": {}}
        res_empty = dispatch_tool_call(call_empty)
        print(f"Boundary missing args: {res_empty}")
        assert res_empty["status"] == "ERROR"
        return 0

    elif scenario == "failure":
        print("Failure simulation: Attempting to assert success on invalid string input...", file=sys.stderr)
        call_str = {"tool": "add", "arguments": {"a": "2", "b": 3}}
        res = dispatch_tool_call(call_str)
        try:
            assert res["status"] == "SUCCESS", "Expected call to fail due to string argument"
            return 0
        except AssertionError as err:
            print(f"Expected failure caught: {err}", file=sys.stderr)
            return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Typed Tool Dispatch Example")
    parser.add_argument(
        "--scenario",
        choices=["normal", "boundary", "failure"],
        default="normal",
        help="Scenario mode to execute",
    )
    args = parser.parse_args()
    return run_demonstration(args.scenario)


if __name__ == "__main__":
    sys.exit(main())
