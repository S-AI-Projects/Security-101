"""
Unit tests for Task R34-T010
"""
import unittest
from example import evaluate_ai_action, StubActionExecutor, get_scenario_assessment_questions

class TestResponsibleAIPolicy(unittest.TestCase):
    def setUp(self):
        self.executor = StubActionExecutor()

    def test_allowed_read_with_valid_path_passes(self):
        act = {"tool": "read", "args": {"path": "document.txt"}}
        res = evaluate_ai_action(act, self.executor)
        self.assertEqual(res["status"], "ALLOWED")
        self.assertEqual(self.executor.call_count, 1)

    def test_unknown_delete_tool_rejected(self):
        act = {"tool": "delete", "args": {"path": "document.txt"}}
        res = evaluate_ai_action(act, self.executor)
        self.assertEqual(res["status"], "REJECTED")
        self.assertIn("not in the allowed-tool set", res["reason"])
        self.assertEqual(self.executor.call_count, 0)

    def test_missing_required_arg_rejected(self):
        act = {"tool": "read", "args": {}}
        res = evaluate_ai_action(act, self.executor)
        self.assertEqual(res["status"], "REJECTED")
        self.assertIn("Missing required argument", res["reason"])
        self.assertEqual(self.executor.call_count, 0)

    def test_scenario_assessment_questions(self):
        questions = get_scenario_assessment_questions()
        self.assertEqual(len(questions), 3)
        # Verify Q1
        q1_res = evaluate_ai_action({"tool": "read", "args": {"path": "data.csv"}}, StubActionExecutor())
        self.assertEqual(q1_res["status"], questions[0]["expected_status"])
        # Verify Q2
        q2_res = evaluate_ai_action({"tool": "delete", "args": {"path": "data.csv"}}, StubActionExecutor())
        self.assertEqual(q2_res["status"], questions[1]["expected_status"])
        # Verify Q3
        q3_res = evaluate_ai_action({"tool": "read", "args": {"path": ""}}, StubActionExecutor())
        self.assertEqual(q3_res["status"], questions[2]["expected_status"])

if __name__ == "__main__":
    unittest.main()
