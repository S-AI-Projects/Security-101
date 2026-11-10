
import unittest

from example import (
    client_capabilities,
    server_capabilities,
    negotiate_capabilities,
    dispatch_request,
)


class TestZeroTrust(unittest.TestCase):

    # Test 1: Normal scenario
    def test_tools_are_allowed(self):
        negotiated = negotiate_capabilities(
            client_capabilities,
            server_capabilities
        )

        self.assertEqual(negotiated, {"tools"})

        result = dispatch_request(
            "tools", negotiated, lambda: "success"
        )

        self.assertEqual(result, "success")

    # Test 2: Boundary scenario
    def test_only_common_capabilities_are_negotiated(self):
        negotiated = negotiate_capabilities(
            {"tools", "resources"},
            {"tools", "prompts"}
        )

        self.assertEqual(negotiated, {"tools",})
        self.assertNotIn("resources", negotiated)
        self.assertNotIn("prompts", negotiated)

    # Test 3: Failure scenario
    def test_resources_are_rejected_before_dispatch(self):
        negotiated = negotiate_capabilities(
            client_capabilities,
            server_capabilities
        )

        handler_called = False

        def handler():
            nonlocal handler_called
            handler_called = True
            return "executed"

        with self.assertRaises(PermissionError):
            dispatch_request("resources", negotiated, handler)

        self.assertFalse(handler_called)


if __name__ == "__main__":
    unittest.main()
