import unittest

from example import MockExecutor, evaluate_action


class TestToolPolicy(unittest.TestCase):

    def setUp(self):
        self.executor = MockExecutor()

    def test_valid_read_is_allowed(self):
        result = evaluate_action({
            "tool": "read",
            "arguments": {"path": "notes.txt"}
        }, self.executor)

        self.assertEqual(result["status"], "ALLOWED")
        self.assertEqual(len(self.executor.calls), 1)

    def test_unknown_delete_is_rejected(self):
        result = evaluate_action({
            "tool": "delete",
            "arguments": {"path": "notes.txt"}
        }, self.executor)

        self.assertEqual(result["status"], "REJECTED")
        self.assertEqual(len(self.executor.calls), 0)

    def test_missing_path_is_rejected(self):
        result = evaluate_action({
            "tool": "read",
            "arguments": {}
        }, self.executor)

        self.assertEqual(result["status"], "REJECTED")
        self.assertEqual(len(self.executor.calls), 0)

    def test_empty_path_is_rejected(self):
        result = evaluate_action({
            "tool": "read",
            "arguments": {"path": ""}
        }, self.executor)

        self.assertEqual(result["status"], "REJECTED")
        self.assertEqual(len(self.executor.calls), 0)

    def test_invalid_path_type_is_rejected(self):
        result = evaluate_action({
            "tool": "read",
            "arguments": {"path": 123}
        }, self.executor)

        self.assertEqual(result["status"], "REJECTED")
        self.assertEqual(len(self.executor.calls), 0)


if __name__ == "__main__":
    unittest.main()
