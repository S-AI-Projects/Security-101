"""Unit tests and applied scenario assessments for Typed Tool Dispatch (R34-T057)."""

import unittest
from example import (
    dispatch_tool_call,
    get_scenario_assessment_questions,
)


class TestTypedToolDispatch(unittest.TestCase):
    def test_valid_add(self):
        call = {"tool": "add", "arguments": {"a": 2, "b": 3}}
        res = dispatch_tool_call(call)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["result"], 5)

    def test_valid_multiply(self):
        call = {"tool": "multiply", "arguments": {"a": 2, "b": 3}}
        res = dispatch_tool_call(call)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["result"], 6)

    def test_unknown_tool_structured_error(self):
        call = {"tool": "shell_command", "arguments": {"a": 1, "b": 2}}
        res = dispatch_tool_call(call)
        self.assertEqual(res["status"], "ERROR")
        self.assertEqual(res["error_type"], "UNKNOWN_TOOL")
        self.assertIn("not in the allowlist", res["message"])

    def test_string_argument_rejected(self):
        call = {"tool": "add", "arguments": {"a": "2", "b": 3}}
        res = dispatch_tool_call(call)
        self.assertEqual(res["status"], "ERROR")
        self.assertEqual(res["error_type"], "INVALID_ARGUMENT")
        self.assertIn("must be numeric", res["message"])

    def test_boolean_argument_rejected(self):
        # In Python, True is an instance of int; our validator must explicitly reject bool
        call = {"tool": "add", "arguments": {"a": True, "b": 3}}
        res = dispatch_tool_call(call)
        self.assertEqual(res["status"], "ERROR")
        self.assertEqual(res["error_type"], "INVALID_ARGUMENT")

    def test_missing_argument(self):
        call = {"tool": "add", "arguments": {"a": 2}}
        res = dispatch_tool_call(call)
        self.assertEqual(res["status"], "ERROR")
        self.assertEqual(res["error_type"], "MISSING_ARGUMENT")

    # Applied Scenario Assessment Executable Checks
    def test_question_1_predict_output(self):
        q = get_scenario_assessment_questions()["question_1_predict_output"]
        res = dispatch_tool_call(q["input"])
        self.assertEqual(res, q["expected_output"])

    def test_question_2_diagnose_failure(self):
        q = get_scenario_assessment_questions()["question_2_diagnose_failure"]
        res = dispatch_tool_call(q["input"])
        self.assertEqual(res["status"], "ERROR")
        self.assertEqual(res["error_type"], q["expected_error_type"])

    def test_question_3_choose_boundary_policy(self):
        q = get_scenario_assessment_questions()["question_3_choose_boundary_policy"]
        res = dispatch_tool_call(q["input"])
        self.assertEqual(res["status"], "ERROR")
        self.assertEqual(res["error_type"], q["expected_error_type"])


if __name__ == "__main__":
    unittest.main()
