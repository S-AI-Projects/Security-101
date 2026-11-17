"""Unit tests for Zero Trust Capability Negotiation (R34-T052)."""

import unittest
from example import (
    CapabilityNotNegotiatedError,
    dispatch_capability,
    negotiate_capabilities,
    safe_dispatch,
)


class TestCapabilityNegotiation(unittest.TestCase):
    def test_negotiation_intersection_normal(self):
        client = {"tools", "resources"}
        server = {"tools", "prompts"}
        negotiated = negotiate_capabilities(client, server)
        self.assertEqual(negotiated, {"tools"})

    def test_smallest_valid_case(self):
        client = {"tools"}
        server = {"tools"}
        negotiated = negotiate_capabilities(client, server)
        self.assertEqual(negotiated, {"tools"})
        result = dispatch_capability(negotiated, "tools")
        self.assertEqual(result["status"], "SUCCESS")

    def test_boundary_disjoint_capabilities(self):
        client = {"resources"}
        server = {"prompts"}
        negotiated = negotiate_capabilities(client, server)
        self.assertEqual(negotiated, set())
        with self.assertRaises(CapabilityNotNegotiatedError):
            dispatch_capability(negotiated, "resources")

    def test_unnegotiated_capability_rejected_before_dispatch(self):
        negotiated = {"tools"}
        # 'resources' was in client set but not negotiated with server
        with self.assertRaises(CapabilityNotNegotiatedError) as ctx:
            dispatch_capability(negotiated, "resources")
        self.assertIn("resources", str(ctx.exception))
        self.assertIn("not negotiated", str(ctx.exception))

    def test_safe_dispatch_structured_rejection(self):
        negotiated = {"tools"}
        status, res = safe_dispatch(negotiated, "resources")
        self.assertEqual(status, "REJECTED")
        self.assertIn("error", res)

    def test_negotiated_capability_dispatches_successfully(self):
        negotiated = {"tools"}
        status, res = safe_dispatch(negotiated, "tools")
        self.assertEqual(status, "SUCCESS")
        self.assertEqual(res["capability"], "tools")


if __name__ == "__main__":
    unittest.main()
