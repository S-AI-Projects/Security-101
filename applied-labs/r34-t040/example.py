import json
from pathlib import Path


ALLOWED_TOOLS = {
    "read": {
        "required": {
            "path": str
        }
    }
}


class MockExecutor:
    """Simulates tool execution; it does not read real files."""

    def __init__(self):
        self.calls = []

    def execute(self, tool, arguments):
        self.calls.append({
            "tool": tool,
            "arguments": arguments
        })
        return f"MOCK_READ:{arguments['path']}"


def evaluate_action(action, executor):
    """Validate an action before allowing mock execution."""

    tool = action.get("tool")
    arguments = action.get("arguments")

    # 1. Check whether the tool is explicitly allowed.
    if tool not in ALLOWED_TOOLS:
        return {
            "status": "REJECTED",
            "reason": "Tool is not allowed.",
            "executor_called": False
        }

    # 2. Check that arguments are an object.
    if not isinstance(arguments, dict):
        return {
            "status": "REJECTED",
            "reason": "Arguments must be an object.",
            "executor_called": False
        }

    # 3. Check required arguments and their types.
    schema = ALLOWED_TOOLS[tool]["required"]

    for name, expected_type in schema.items():
        if name not in arguments:
            return {
                "status": "REJECTED",
                "reason": f"Missing required argument: {name}.",
                "executor_called": False
            }

        if not isinstance(arguments[name], expected_type):
            return {
                "status": "REJECTED",
                "reason": f"Invalid type for argument: {name}.",
                "executor_called": False
            }

        if not arguments[name].strip():
            return {
                "status": "REJECTED",
                "reason": f"Argument cannot be empty: {name}.",
                "executor_called": False
            }

    # 4. Execute only after every validation passes.
    result = executor.execute(tool, arguments)

    return {
        "status": "ALLOWED",
        "reason": "Policy and argument validation passed.",
        "executor_called": True,
        "result": result
    }


def main():
    fixture = Path(__file__).with_name("scenarios.json")
    scenarios = json.loads(fixture.read_text())

    executor = MockExecutor()

    for scenario in scenarios:
        decision = evaluate_action(scenario, executor)
        print(json.dumps({
            "input": scenario,
            "decision": decision
        }))

    print(json.dumps({
        "total_executor_calls": len(executor.calls)
    }))


if __name__ == "__main__":
    main()
