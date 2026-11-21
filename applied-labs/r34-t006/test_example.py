"""
Unit tests for Task R34-T006
"""
import unittest
from example import PolicyValidator, ActionExecutorStub, baseline_execute, refactored_execute

class TestAIToolPolicy(unittest.TestCase):
    def setUp(self):
        self.executor = ActionExecutorStub()

    def test_allowed_read_with_valid_path_passes(self):
        action = {"tool": "read_document", "args": {"path": "/docs/plan.md"}}
        res = refactored_execute(action, self.executor)
        self.assertEqual(res["status"], "EXECUTED")
        self.assertEqual(len(self.executor.executed_actions), 1)

    def test_unknown_delete_tool_rejected(self):
        action = {"tool": "delete_document", "args": {"path": "/docs/plan.md"}}
        res = refactored_execute(action, self.executor)
        self.assertEqual(res["status"], "REJECTED")
        self.assertIn("not in the allowed tool set", res["reason"])
        self.assertEqual(len(self.executor.executed_actions), 0)  # Never reaches executor

    def test_missing_required_arg_rejected(self):
        action = {"tool": "read_document", "args": {}}
        res = refactored_execute(action, self.executor)
        self.assertEqual(res["status"], "REJECTED")
        self.assertIn("Missing required argument", res["reason"])
        self.assertEqual(len(self.executor.executed_actions), 0)

    def test_baseline_and_refactored_equivalence(self):
        test_actions = [
            {"tool": "read_document", "args": {"path": "/docs/test.txt"}},
            {"tool": "delete_document", "args": {"path": "/docs/test.txt"}},
            {"tool": "read_document", "args": {}},
            {"tool": "unknown_cmd", "args": {"x": 1}}
        ]
        for act in test_actions:
            e1 = ActionExecutorStub()
            e2 = ActionExecutorStub()
            b_res = baseline_execute(act, e1)
            r_res = refactored_execute(act, e2)
            self.assertEqual(b_res["status"], r_res["status"])
            self.assertEqual(len(e1.executed_actions), len(e2.executed_actions))

if __name__ == "__main__":
    unittest.main()
