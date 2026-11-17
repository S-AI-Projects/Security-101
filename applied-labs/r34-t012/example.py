import json


def add(first, second):
    return first + second


def multiply(first, second):
    return first * second


TOOL_ALLOWLIST = {
    "add": add,
    "multiply": multiply,
}

EXAMPLE_CALLS = [
    {"tool": "add", "arguments": [2, 3]},
    {"tool": "multiply", "arguments": [2, 3]},
    {"tool": "add", "arguments": [0, 0]},
    {"tool": "multiply", "arguments": [0, 7]},
    {"tool": "subtract", "arguments": [2, 3]},
    {"tool": "add", "arguments": ["2", 3]},
    {"tool": "add", "arguments": [True, 3]},
    {"tool": "add"},
]


def _error(code, message):
    return {
        "ok": False,
        "error": {"code": code, "message": message},
    }


def call_tool(tool_name=None, arguments=None):
    if not isinstance(tool_name, str) or tool_name not in TOOL_ALLOWLIST:
        return _error("INVALID_TOOL", "Tool is not in the allowed tool list.")

    if not isinstance(arguments, (list, tuple)) or len(arguments) != 2:
        return _error(
            "INVALID_ARGUMENTS",
            "Exactly two positional arguments are required.",
        )

    if any(type(value) not in (int, float) for value in arguments):
        return _error(
            "INVALID_ARGUMENT_TYPE",
            "Both arguments must be int or float values; strings and booleans are not accepted.",
        )

    result = TOOL_ALLOWLIST[tool_name](*arguments)
    return {"ok": True, "result": result}


def run_examples():
    results = []
    for call in EXAMPLE_CALLS:
        results.append(
            {
                "tool": call.get("tool"),
                "arguments": call.get("arguments"),
                "response": call_tool(call.get("tool"), call.get("arguments")),
            }
        )
    return results


if __name__ == "__main__":
    print(json.dumps(run_examples(), indent=2))
