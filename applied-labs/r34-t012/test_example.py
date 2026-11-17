import unittest
from unittest.mock import Mock, patch

import example
from example import call_tool


class TestAllowlistedToolCalls(unittest.TestCase):
    def assert_tool_error(self, response, code):
        self.assertFalse(response["ok"])
        self.assertEqual(response["error"]["code"], code)
        self.assertTrue(response["error"]["message"])

    def test_add_returns_five(self):
        self.assertEqual(call_tool("add", [2, 3]), {"ok": True, "result": 5})

    def test_multiply_returns_six(self):
        self.assertEqual(call_tool("multiply", [2, 3]), {"ok": True, "result": 6})

    def test_zero_boundary_cases(self):
        self.assertEqual(call_tool("add", [0, 0])["result"], 0)
        self.assertEqual(call_tool("multiply", [0, 1])["result"], 0)

    def test_small_and_negative_numeric_values(self):
        self.assertEqual(call_tool("add", [-1, 1])["result"], 0)
        self.assertEqual(call_tool("multiply", [-1, 2])["result"], -2)

    def test_float_arguments_are_numeric(self):
        self.assertEqual(call_tool("add", [0.5, 1.5])["result"], 2.0)

    def test_invalid_tool_names_return_structured_errors(self):
        for tool_name in ("subtract", "", None, 7):
            with self.subTest(tool_name=tool_name):
                self.assert_tool_error(
                    call_tool(tool_name, [2, 3]), "INVALID_TOOL"
                )

    def test_string_arguments_are_rejected(self):
        for arguments in (["2", 3], [2, "3"]):
            with self.subTest(arguments=arguments):
                self.assert_tool_error(
                    call_tool("add", arguments), "INVALID_ARGUMENT_TYPE"
                )

    def test_boolean_arguments_are_rejected(self):
        for boolean in (True, False):
            with self.subTest(boolean=boolean):
                self.assert_tool_error(
                    call_tool("add", [boolean, 3]), "INVALID_ARGUMENT_TYPE"
                )

    def test_missing_arguments_are_rejected(self):
        self.assert_tool_error(call_tool("add"), "INVALID_ARGUMENTS")
        self.assert_tool_error(call_tool("add", [2]), "INVALID_ARGUMENTS")

    def test_extra_arguments_are_rejected(self):
        self.assert_tool_error(
            call_tool("add", [2, 3, 4]), "INVALID_ARGUMENTS"
        )

    def test_failed_call_does_not_execute_any_tool(self):
        add_spy = Mock(return_value=999)
        multiply_spy = Mock(return_value=999)
        with patch.dict(
            example.TOOL_ALLOWLIST,
            {"add": add_spy, "multiply": multiply_spy},
            clear=True,
        ):
            response = call_tool("add", ["2", 3])

        self.assert_tool_error(response, "INVALID_ARGUMENT_TYPE")
        add_spy.assert_not_called()
        multiply_spy.assert_not_called()

    def test_invalid_tool_does_not_fall_through_to_an_allowed_tool(self):
        add_spy = Mock(return_value=999)
        multiply_spy = Mock(return_value=999)
        with patch.dict(
            example.TOOL_ALLOWLIST,
            {"add": add_spy, "multiply": multiply_spy},
            clear=True,
        ):
            response = call_tool("divide", [6, 2])

        self.assert_tool_error(response, "INVALID_TOOL")
        add_spy.assert_not_called()
        multiply_spy.assert_not_called()


if __name__ == "__main__":
    unittest.main()
