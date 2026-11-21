"""
Unit tests for SecOps Typed Tool Dispatcher (Task R34-T003)
"""
import unittest
from example import dispatch_tool, reference_calculator

class TestTypedToolDispatch(unittest.TestCase):
    def test_add_success(self):
        """add(2,3) -> 5"""
        req = {"tool": "add", "a": 2, "b": 3}
        res = dispatch_tool(req)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["result"], 5)
        self.assertEqual(res["result"], reference_calculator("add", 2, 3))

    def test_multiply_success(self):
        """multiply(2,3) -> 6"""
        req = {"tool": "multiply", "a": 2, "b": 3}
        res = dispatch_tool(req)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["result"], 6)
        self.assertEqual(res["result"], reference_calculator("multiply", 2, 3))

    def test_unknown_tool_structured_error(self):
        """unknown tool is a structured error"""
        req = {"tool": "delete_all", "a": 2, "b": 3}
        res = dispatch_tool(req)
        self.assertEqual(res["status"], "error")
        self.assertEqual(res["error_type"], "UNKNOWN_TOOL")

    def test_string_argument_structured_error(self):
        """string argument a produces a structured error"""
        req = {"tool": "add", "a": "invalid_string", "b": 3}
        res = dispatch_tool(req)
        self.assertEqual(res["status"], "error")
        self.assertEqual(res["error_type"], "INVALID_ARGUMENT")
        self.assertIn("numeric", res["message"])

    def test_failed_call_does_not_execute(self):
        """a failed call cannot execute another tool"""
        req = {"tool": "unknown_tool", "a": "text", "b": 10}
        res = dispatch_tool(req)
        self.assertEqual(res["status"], "error")
        self.assertNotIn("result", res)

if __name__ == "__main__":
    unittest.main()
