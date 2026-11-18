import unittest

from example import (
    CLIENT_CAPABILITIES,
    SERVER_CAPABILITIES,
    dispatch_request,
    negotiate_capabilities,
)


class TestCapabilityNegotiation(unittest.TestCase):
    def test_negotiation_matches_explicit_expected_result(self):
        negotiated = negotiate_capabilities(
            CLIENT_CAPABILITIES,
            SERVER_CAPABILITIES,
        )

        self.assertEqual(negotiated, frozenset({"tools"}))

    def test_negotiated_tool_is_dispatched(self):
        calls = 0

        def handler() -> str:
            nonlocal calls
            calls += 1
            return "tools dispatched"

        result = dispatch_request("tools", frozenset({"tools"}), handler)

        self.assertEqual(result, "tools dispatched")
        self.assertEqual(calls, 1)

    def test_resources_are_rejected_before_dispatch(self):
        negotiated = negotiate_capabilities(
            CLIENT_CAPABILITIES,
            SERVER_CAPABILITIES,
        )
        handler_called = False

        def handler() -> str:
            nonlocal handler_called
            handler_called = True
            return "resources dispatched"

        with self.assertRaisesRegex(
            PermissionError,
            "capability 'resources' was not negotiated",
        ):
            dispatch_request("resources", negotiated, handler)

        self.assertFalse(handler_called)

    def test_empty_intersection_rejects_dispatch(self):
        negotiated = negotiate_capabilities(
            {"resources"},
            SERVER_CAPABILITIES,
        )
        handler_called = False

        def handler() -> str:
            nonlocal handler_called
            handler_called = True
            return "tools dispatched"

        self.assertEqual(negotiated, frozenset())
        with self.assertRaises(PermissionError):
            dispatch_request("tools", negotiated, handler)
        self.assertFalse(handler_called)


if __name__ == "__main__":
    unittest.main()
