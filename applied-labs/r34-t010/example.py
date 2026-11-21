"""
Responsible AI Tool Policy & Scenario Assessment (Task R34-T010)
Enforces allowed tools and per-tool argument schema before execution.
Includes scenario assessment answering three applied security questions.
"""
import sys
import json
import argparse

ALLOWED_TOOLS = {
    "read": {
        "required_args": ["path"],
        "schema": {"path": str}
    }
}

class StubActionExecutor:
    """Stub executor that only processes validated calls."""
    def __init__(self):
        self.call_count = 0

    def execute(self, tool, args):
        self.call_count += 1
        return f"Tool '{tool}' executed with path='{args.get('path')}'."

def evaluate_ai_action(action, executor):
    """
    Evaluates action against tool allowlist and argument schema.
    Returns status: ALLOWED or REJECTED.
    """
    if not isinstance(action, dict):
        return {"status": "REJECTED", "reason": "Action must be a dictionary object."}

    tool = action.get("tool")
    if tool not in ALLOWED_TOOLS:
        return {"status": "REJECTED", "reason": f"Tool '{tool}' is not in the allowed-tool set."}

    args = action.get("args")
    if not isinstance(args, dict):
        return {"status": "REJECTED", "reason": "Arguments must be provided in an 'args' dictionary."}

    spec = ALLOWED_TOOLS[tool]
    for req in spec["required_args"]:
        if req not in args or not args[req]:
            return {"status": "REJECTED", "reason": f"Missing required argument '{req}' for tool '{tool}'."}
        if not isinstance(args[req], spec["schema"][req]):
            return {"status": "REJECTED", "reason": f"Argument '{req}' has invalid type."}

    # Action is allowed -> proceed to execution
    result = executor.execute(tool, args)
    return {"status": "ALLOWED", "execution_result": result}

def get_scenario_assessment_questions():
    """
    Three applied scenario assessment questions with rationales and checks.
    """
    return [
        {
            "id": "Q1_PREDICT_OUTPUT",
            "question": "What is the policy evaluation result for action {'tool': 'read', 'args': {'path': 'data.csv'}}?",
            "expected_status": "ALLOWED",
            "rationale": "Tool 'read' is allowed and argument 'path' is a valid non-empty string."
        },
        {
            "id": "Q2_DIAGNOSE_FAILURE",
            "question": "Why is action {'tool': 'delete', 'args': {'path': 'data.csv'}} rejected?",
            "expected_status": "REJECTED",
            "rationale": "Tool 'delete' is not present in the allowed-tool set (strict allowlist enforcement)."
        },
        {
            "id": "Q3_BOUNDARY_POLICY",
            "question": "What is the policy decision when 'read' is invoked with an empty path {'tool': 'read', 'args': {'path': ''}}?",
            "expected_status": "REJECTED",
            "rationale": "An empty string fails the non-empty path requirement under the argument schema."
        }
    ]

def main():
    parser = argparse.ArgumentParser(description="Responsible AI Tool Policy Checker")
    parser.add_argument("--action", choices=["read", "delete", "missing_arg", "assessment"], default="read")
    args = parser.parse_args()

    executor = StubActionExecutor()
    if args.action == "assessment":
        print(json.dumps(get_scenario_assessment_questions(), indent=2))
    elif args.action == "read":
        res = evaluate_ai_action({"tool": "read", "args": {"path": "/safe/data.txt"}}, executor)
        print(json.dumps(res, indent=2))
    elif args.action == "delete":
        res = evaluate_ai_action({"tool": "delete", "args": {"path": "/safe/data.txt"}}, executor)
        print(json.dumps(res, indent=2))
    elif args.action == "missing_arg":
        res = evaluate_ai_action({"tool": "read", "args": {}}, executor)
        print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
