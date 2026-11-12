
import unittest

from example import (
    negotiate_capabilities,
    invoke_capability
)


class TestCapabilityNegotiation(unittest.TestCase):

    def setUp(self):
        self.client = {"tools", "resources"}
        self.server = {"tools", "prompts"}
        self.negotiated = negotiate_capabilities(
            self.client, self.server
        )

    # Normal case: common capability is allowed
    def test_tools_is_negotiated(self):
        self.assertEqual(self.negotiated, {"tools"})

    # Boundary case: only one capability is common
    def test_only_common_capability_is_allowed(self):
        self.assertIn("tools", self.negotiated)
        self.assertNotIn("resources", self.negotiated)

    # Invalid case: resources must be rejected
    def test_resources_is_rejected(self):
        result = invoke_capability(
            "resources", self.negotiated,
            lambda capability: "DISPATCHED"
        )
        self.assertEqual(result, "REJECTED")

    # Invalid case: unknown capability is rejected
    def test_unknown_capability_is_rejected(self):
        result = invoke_capability(
            "unknown", self.negotiated,
            lambda capability: "DISPATCHED"
        )
        self.assertEqual(result, "REJECTED")

    # Security case: rejected requests never reach dispatch
    def test_rejected_request_never_reaches_dispatch(self):
        dispatch_calls = []

        def fake_dispatch(capability):
            dispatch_calls.append(capability)
            return "DISPATCHED"

        result = invoke_capability(
            "resources", self.negotiated, fake_dispatch
        )

        self.assertEqual(result, "REJECTED")
        self.assertEqual(dispatch_calls, [])


if __name__ == "__main__":
    unittest.main()
