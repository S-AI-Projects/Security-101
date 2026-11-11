"""Unit tests for typed tool dispatch, fail-stop behavior, and invariant verification."""

import json
import unittest
from unittest.mock import patch

from example import (
    ALLOWLIST,
    FIXTURES,
    execute_pipeline,
    run_fixture,
    verify_pipeline_invariants,
)


class TypedToolDispatchTests(unittest.TestCase):
    def test_add_success_returns_five(self):
        output, valid, message = run_fixture("add-success", FIXTURES["add-success"])
        self.assertTrue(valid, message)
        self.assertEqual(output["status"], "SUCCESS")
        self.assertEqual(output["final_result"], 5)
        self.assertEqual(output["results"], [5])
        self.assertIsNone(output["error"])
        self.assertEqual(output["steps_executed"], 1)
        self.assertEqual(output["steps_blocked"], 0)

    def test_multiply_success_returns_six(self):
        output, valid, message = run_fixture("multiply-success", FIXTURES["multiply-success"])
        self.assertTrue(valid, message)
        self.assertEqual(output["status"], "SUCCESS")
        self.assertEqual(output["final_result"], 6)
        self.assertEqual(output["results"], [6])
        self.assertIsNone(output["error"])
        self.assertEqual(output["steps_executed"], 1)
        self.assertEqual(output["steps_blocked"], 0)

    def test_unknown_tool_returns_structured_error(self):
        output, valid, message = run_fixture("unknown-tool-error", FIXTURES["unknown-tool-error"])
        self.assertTrue(valid, message)
        self.assertEqual(output["status"], "ERROR")
        self.assertIsNone(output["final_result"])
        self.assertIsNotNone(output["error"])
        self.assertEqual(output["error"]["code"], "UNKNOWN_TOOL")
        self.assertIn("Tool 'quarantine_host' is not in allowlist", output["error"]["message"])

    def test_string_argument_a_returns_structured_error(self):
        output, valid, message = run_fixture("string-arg-error", FIXTURES["string-arg-error"])
        self.assertTrue(valid, message)
        self.assertEqual(output["status"], "ERROR")
        self.assertIsNone(output["final_result"])
        self.assertIsNotNone(output["error"])
        self.assertEqual(output["error"]["code"], "INVALID_ARGUMENT")
        self.assertEqual(output["error"]["message"], "Argument 'a' must be a number")

    def test_argument_validation_rejects_booleans_and_missing_keys(self):
        invalid_calls = [
            ({"tool": "add", "args": {"a": True, "b": 3}}, "Argument 'a' must be a number"),
            ({"tool": "add", "args": {"a": 2, "b": False}}, "Argument 'b' must be a number"),
            ({"tool": "add", "args": {"a": 2, "b": "3"}}, "Argument 'b' must be a number"),
            ({"tool": "add", "args": {"a": 2}}, "Arguments 'a' and 'b' are required"),
            ({"tool": "add", "args": "not-a-dict"}, "Field 'args' must be a dictionary"),
            ({"args": {"a": 2, "b": 3}}, "Field 'tool' must be a non-empty string"),
        ]
        for spec, expected_msg in invalid_calls:
            with self.subTest(spec=spec):
                output = execute_pipeline([spec])
                self.assertEqual(output["status"], "ERROR")
                self.assertIn(output["error"]["code"], ("INVALID_ARGUMENT", "INVALID_SCHEMA"))
                self.assertEqual(output["error"]["message"], expected_msg)

    def test_failed_call_cannot_execute_subsequent_tool(self):
        call_fail = {"tool": "add", "args": {"a": "2", "b": 3}}
        call_next = {"tool": "multiply", "args": {"a": 2, "b": 3}}

        # Use mock to prove ALLOWLIST['multiply'] is never executed
        with patch.dict(ALLOWLIST, {"multiply": unittest.mock.MagicMock()}):
            output = execute_pipeline([call_fail, call_next])
            ALLOWLIST["multiply"].assert_not_called()

        self.assertEqual(output["status"], "ERROR")
        self.assertEqual(output["steps_executed"], 1)
        self.assertEqual(output["steps_blocked"], 1)
        self.assertEqual(len(output["trace"]), 2)

        # Inspect intermediate trace states
        step1, step2 = output["trace"]
        self.assertEqual(step1["status"], "ERROR")
        self.assertEqual(step1["error"]["code"], "INVALID_ARGUMENT")
        self.assertTrue(step1["halted"])

        self.assertEqual(step2["status"], "BLOCKED")
        self.assertIsNone(step2["result"])
        self.assertIsNone(step2["error"])
        self.assertTrue(step2["halted"])

        valid, msg = verify_pipeline_invariants(output["trace"], output)
        self.assertTrue(valid, msg)

    def test_pipeline_all_success_executes_all_steps_and_records_trace(self):
        output, valid, message = run_fixture("pipeline-all-success", FIXTURES["pipeline-all-success"])
        self.assertTrue(valid, message)
        self.assertEqual(output["status"], "SUCCESS")
        self.assertEqual(output["results"], [5, 6])
        self.assertEqual(output["final_result"], 6)
        self.assertEqual(output["steps_executed"], 2)
        self.assertEqual(output["steps_blocked"], 0)

        step1, step2 = output["trace"]
        self.assertEqual(step1["status"], "SUCCESS")
        self.assertEqual(step1["result"], 5)
        self.assertFalse(step1["halted"])

        self.assertEqual(step2["status"], "SUCCESS")
        self.assertEqual(step2["result"], 6)
        self.assertFalse(step2["halted"])

    def test_intermediate_state_trace_structure(self):
        output = execute_pipeline([{"tool": "add", "args": {"a": 2, "b": 3}}])
        self.assertEqual(len(output["trace"]), 1)
        step = output["trace"][0]
        required_keys = {"step", "tool", "status", "result", "error", "halted"}
        self.assertTrue(required_keys.issubset(step.keys()))
        self.assertEqual(step["step"], 1)
        self.assertEqual(step["tool"], "add")
        self.assertEqual(step["status"], "SUCCESS")
        self.assertEqual(step["result"], 5)
        self.assertIsNone(step["error"])
        self.assertFalse(step["halted"])

    def test_invariant_checker_catches_tampered_final_status(self):
        output = execute_pipeline([{"tool": "add", "args": {"a": "2", "b": 3}}])
        # Corrupt final status to SUCCESS while step was ERROR
        corrupted_output = dict(output)
        corrupted_output["status"] = "SUCCESS"
        valid, msg = verify_pipeline_invariants(corrupted_output["trace"], corrupted_output)
        self.assertFalse(valid)
        self.assertIn("Final status must be ERROR", msg)

    def test_invariant_checker_catches_unblocked_step_after_failure(self):
        output = execute_pipeline([
            {"tool": "add", "args": {"a": "2", "b": 3}},
            {"tool": "multiply", "args": {"a": 2, "b": 3}},
        ])
        corrupted_trace = [dict(s) for s in output["trace"]]
        # Corrupt second step status to SUCCESS
        corrupted_trace[1]["status"] = "SUCCESS"
        corrupted_trace[1]["result"] = 6
        valid, msg = verify_pipeline_invariants(corrupted_trace, output)
        self.assertFalse(valid)
        self.assertIn("after failure must be BLOCKED", msg)

    def test_malformed_json_string_returns_structured_error(self):
        bad_json = '{"tool": "add", "args":'
        output = execute_pipeline([bad_json])
        self.assertEqual(output["status"], "ERROR")
        self.assertEqual(output["error"]["code"], "MALFORMED_JSON")
        self.assertTrue(output["trace"][0]["halted"])
        valid, msg = verify_pipeline_invariants(output["trace"], output)
        self.assertTrue(valid, msg)


if __name__ == "__main__":
    unittest.main()
