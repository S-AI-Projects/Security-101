"""
Unit tests for IAM Access Policy Evaluator (Task R34-T002)
"""
import unittest
from example import evaluate_access

class TestIAMPolicyEvaluation(unittest.TestCase):
    def test_reader_may_read_public(self):
        res = evaluate_access("reader", "read", "public")
        self.assertEqual(res["decision"], "ALLOW")

    def test_reader_cannot_write_public(self):
        res = evaluate_access("reader", "write", "public")
        self.assertEqual(res["decision"], "DENY")

    def test_explicit_deny_overrides_matching_allow(self):
        res = evaluate_access("auditor", "audit", "logs")
        self.assertEqual(res["decision"], "DENY")
        self.assertIn("Explicit DENY", res["reason"])

    def test_unknown_role_is_denied(self):
        res = evaluate_access("anonymous_guest", "read", "public")
        self.assertEqual(res["decision"], "DENY")
        self.assertIn("unknown", res["reason"].lower())

    def test_editor_may_write_public(self):
        res = evaluate_access("editor", "write", "public")
        self.assertEqual(res["decision"], "ALLOW")

    def test_unmatched_action_denied(self):
        res = evaluate_access("reader", "delete", "public")
        self.assertEqual(res["decision"], "DENY")

if __name__ == "__main__":
    unittest.main()
