import json
from pathlib import Path


ALLOWED_TOOLS = {
    "read": {
        "required": ["path"],
        "types": {"path": str},
    }
}


class MockExecutor:
    """A safe stand-in; it does not read, write, or delete real files."""

    def __init__(self):
        self.calls = []

    def execute(self, tool, arguments):
        self.calls.append({"tool": tool, "arguments": arguments})
        return f"MOCK_READ:{arguments['path']}"


def evaluate_action(action, executor):
    tool = action.get("tool")

    # Check 1: tool must be explicitly allowed.
    if tool not in ALLOWED_TOOLS:
        return {"status": "REJECTED", "reason": "Unknown or disallowed tool"}

    schema = ALLOWED_TOOLS[tool]
    arguments = action.get("arguments")

    # Check 2: arguments must be an object.
    if not isinstance(arguments, dict):
        return {"status": "REJECTED", "reason": "Arguments must be an object"}

    # Check 3: required arguments must exist and have the right type.
    for name in schema["required"]:
        if name not in arguments:
            return {"status": "REJECTED", "reason": f"Missing required argument: {name}"}

        if not isinstance(arguments[name], schema["types"][name]):
            return {"status": "REJECTED", "reason": f"Invalid type for argument: {name}"}

        if not arguments[name].strip():
            return {"status": "REJECTED", "reason": f"Empty argument: {name}"}

    # Execution happens only after every validation check passes.
    result = executor.execute(tool, arguments)
    return {"status": "ALLOWED", "reason": "Validation passed", "result": result}


def run_scenarios(fixture):
    results = []

    for group_name, actions in fixture.items():
        executor = MockExecutor()
        decisions = [evaluate_action(action, executor) for action in actions]

        results.append({
            "group": group_name,
            "input_count": len(actions),
            "allowed_count": sum(d["status"] == "ALLOWED" for d in decisions),
            "rejected_count": sum(d["status"] == "REJECTED" for d in decisions),
            "executor_calls": len(executor.calls),
            "decisions": decisions,
        })

    return results


def main():
    fixture_path = Path(__file__).with_name("scenarios.json")
    fixture = json.loads(fixture_path.read_text())
    for result in run_scenarios(fixture):
        print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
