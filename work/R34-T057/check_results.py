"""Assertion checks for R34-T057 typed tool dispatch."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "applied-labs/r34-t057"))

from example import dispatch_tool_call, get_scenario_assessment_questions


def main() -> int:
    res_add = dispatch_tool_call({"tool": "add", "arguments": {"a": 2, "b": 3}})
    assert res_add["status"] == "SUCCESS"
    assert res_add["result"] == 5

    res_mult = dispatch_tool_call({"tool": "multiply", "arguments": {"a": 2, "b": 3}})
    assert res_mult["status"] == "SUCCESS"
    assert res_mult["result"] == 6

    res_unk = dispatch_tool_call({"tool": "exec", "arguments": {"a": 1, "b": 2}})
    assert res_unk["status"] == "ERROR"
    assert res_unk["error_type"] == "UNKNOWN_TOOL"

    res_str = dispatch_tool_call({"tool": "add", "arguments": {"a": "2", "b": 3}})
    assert res_str["status"] == "ERROR"
    assert res_str["error_type"] == "INVALID_ARGUMENT"

    questions = get_scenario_assessment_questions()
    assert len(questions) == 3

    if "--deliberate-wrong-result" in sys.argv:
        assert res_add["result"] == 10, "Deliberate wrong result check"

    print("All R34-T057 checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
