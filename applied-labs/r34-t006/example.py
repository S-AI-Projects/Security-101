"""
AI Tool Allowlist & Policy Validator (Task R34-T006)
Extracted responsibility: separates PolicyValidator from ActionExecutor.
Enforces allowlist and argument schema before execution.
"""
import sys
import json
import argparse

ALLOWED_TOOLS = {
    "read_document": {
        "required_args": ["path"],
        "arg_types": {"path": str}
    }
}

class ActionExecutorStub:
    """Stub executor that only runs verified actions."""
    def __init__(self):
        self.executed_actions = []

    def execute(self, tool_name, args):
        self.executed_actions.append({"tool": tool_name, "args": args})
        return f"Executed {tool_name} successfully with path '{args.get('path')}'."

class PolicyValidator:
    """Extracted responsibility: validates tool allowlist and argument schemas."""
    @staticmethod
    def validate(tool_name, args):
        if tool_name not in ALLOWED_TOOLS:
            return False, f"Tool '{tool_name}' is not in the allowed tool set: {list(ALLOWED_TOOLS.keys())}."
        
        schema = ALLOWED_TOOLS[tool_name]
        for req in schema["required_args"]:
            if req not in args or not args[req]:
                return False, f"Missing required argument '{req}' for tool '{tool_name}'."
            if not isinstance(args[req], schema["arg_types"][req]):
                return False, f"Argument '{req}' must be of type {schema['arg_types'][req].__name__}."
        
        return True, "Validation successful."

# Baseline monolithic function for comparison and regression check
def baseline_execute(action, executor):
    tool = action.get("tool")
    args = action.get("args", {})
    if tool not in ALLOWED_TOOLS:
        return {"status": "REJECTED", "reason": "Unknown tool"}
    if "path" not in args or not args["path"]:
        return {"status": "REJECTED", "reason": "Missing required argument 'path'"}
    return {"status": "EXECUTED", "output": executor.execute(tool, args)}

# Refactored pipeline function
def refactored_execute(action, executor):
    tool = action.get("tool")
    args = action.get("args", {})
    is_valid, reason = PolicyValidator.validate(tool, args)
    if not is_valid:
        return {"status": "REJECTED", "reason": reason}
    output = executor.execute(tool, args)
    return {"status": "EXECUTED", "output": output}

def main():
    parser = argparse.ArgumentParser(description="AI Tool Allowlist Policy Checker")
    parser.add_argument("--action", choices=["read", "delete", "missing_arg"], default="read")
    args = parser.parse_args()

    executor = ActionExecutorStub()
    actions = {
        "read": {"tool": "read_document", "args": {"path": "/safe/data.txt"}},
        "delete": {"tool": "delete_document", "args": {"path": "/safe/data.txt"}},
        "missing_arg": {"tool": "read_document", "args": {}}
    }
    action = actions[args.action]
    res = refactored_execute(action, executor)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
