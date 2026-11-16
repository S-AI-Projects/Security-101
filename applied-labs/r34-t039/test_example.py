import unittest

from example import MockExecutor, evaluate_action


class ToolPolicyTests(unittest.TestCase):

    def test_allowed_read_reaches_executor(self):
        executor = MockExecutor()
        result = evaluate_action(
            {"tool": "read", "arguments": {"path": "notes.txt"}},
            executor,
        )
        self.assertEqual(result["status"], "ALLOWED")
        self.assertEqual(len(executor.calls), 1)

    def test_unknown_delete_tool_is_rejected(self):
        executor = MockExecutor()
        result = evaluate_action(
            {"tool": "delete", "arguments": {"path": "notes.txt"}},
            executor,
        )
        self.assertEqual(result["status"], "REJECTED")
        self.assertEqual(len(executor.calls), 0)

    def test_missing_required_path_is_rejected(self):
        executor = MockExecutor()
        result = evaluate_action(
            {"tool": "read", "arguments": {}},
            executor,
        )
        self.assertEqual(result["status"], "REJECTED")
        self.assertEqual(len(executor.calls), 0)

    def test_empty_path_is_rejected(self):
        executor = MockExecutor()
        result = evaluate_action(
            {"tool": "read", "arguments": {"path": ""}},
            executor,
        )
        self.assertEqual(result["status"], "REJECTED")
        self.assertEqual(len(executor.calls), 0)

    def test_invalid_path_type_is_rejected(self):
        executor = MockExecutor()
        result = evaluate_action(
            {"tool": "read", "arguments": {"path": 123}},
            executor,
        )
        self.assertEqual(result["status"], "REJECTED")
        self.assertEqual(len(executor.calls), 0)


if __name__ == "__main__":
    unittest.main()
