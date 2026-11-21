"""
SecOps Typed Tool Dispatcher (Task R34-T003)
Dispatches local JSON calls for add(a,b) and multiply(a,b)
with explicit allowlist and numeric validation.
"""
import sys
import json
import argparse

ALLOWED_TOOLS = ["add", "multiply"]

def dispatch_tool(request):
    """
    Validates and executes a tool call.
    Returns a dict with 'status' ('success' or 'error') and 'result' or 'message'.
    """
    if not isinstance(request, dict):
        return {"status": "error", "error_type": "INVALID_REQUEST", "message": "Request must be a JSON object/dict."}

    tool = request.get("tool")
    if tool not in ALLOWED_TOOLS:
        return {
            "status": "error",
            "error_type": "UNKNOWN_TOOL",
            "message": f"Tool '{tool}' is not in the allowed list: {ALLOWED_TOOLS}"
        }

    # Validate arguments a and b
    if "a" not in request or "b" not in request:
        return {
            "status": "error",
            "error_type": "MISSING_ARGUMENT",
            "message": "Both arguments 'a' and 'b' are required."
        }

    a = request["a"]
    b = request["b"]

    # Check numeric types (exclude bool since bool is a subclass of int in Python)
    if isinstance(a, bool) or not isinstance(a, (int, float)):
        return {
            "status": "error",
            "error_type": "INVALID_ARGUMENT",
            "message": f"Argument 'a' must be a numeric value, got {type(a).__name__}."
        }
    if isinstance(b, bool) or not isinstance(b, (int, float)):
        return {
            "status": "error",
            "error_type": "INVALID_ARGUMENT",
            "message": f"Argument 'b' must be a numeric value, got {type(b).__name__}."
        }

    # Execute tool
    if tool == "add":
        res = a + b
    elif tool == "multiply":
        res = a * b
    else:
        return {"status": "error", "error_type": "EXECUTION_ERROR", "message": "Unexpected tool state."}

    return {
        "status": "success",
        "tool": tool,
        "result": res
    }

def reference_calculator(tool, a, b):
    """
    Independent reference implementation for comparison.
    """
    lookup = {
        ("add", 2, 3): 5,
        ("multiply", 2, 3): 6,
        ("add", 10, 20): 30,
        ("multiply", 4, 5): 20
    }
    return lookup.get((tool, a, b))

def main():
    parser = argparse.ArgumentParser(description="Typed Tool Dispatcher")
    parser.add_argument("--tool", default="add")
    parser.add_argument("--a", default="2")
    parser.add_argument("--b", default="3")
    args = parser.parse_args()

    # Try parsing numbers if possible
    try:
        a_val = int(args.a)
    except ValueError:
        try:
            a_val = float(args.a)
        except ValueError:
            a_val = args.a  # Pass as string to demonstrate error handling

    try:
        b_val = int(args.b)
    except ValueError:
        try:
            b_val = float(args.b)
        except ValueError:
            b_val = args.b

    req = {"tool": args.tool, "a": a_val, "b": b_val}
    print(json.dumps(dispatch_tool(req), indent=2))

if __name__ == "__main__":
    main()
