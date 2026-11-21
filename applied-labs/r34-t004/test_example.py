"""
Unit tests for Zero Trust Capability Negotiation (Task R34-T004)
"""
import unittest
from example import negotiate_capabilities, invoke_capability

class TestCapabilityNegotiation(unittest.TestCase):
    def setUp(self):
        self.client_caps = {"tools", "resources"}
        self.server_caps = {"tools", "prompts"}
        self.negotiated, self.trace = negotiate_capabilities(self.client_caps, self.server_caps)

    def test_negotiation_intersection(self):
        """Client {tools,resources}, server {tools,prompts} negotiates {tools}"""
        self.assertEqual(self.negotiated, {"tools"})
        self.assertEqual(self.trace["step_3_negotiated"], ["tools"])

    def test_invoking_unnegotiated_resources_rejected(self):
        """Calling resources is rejected before dispatch"""
        res = invoke_capability(self.negotiated, "resources")
        self.assertEqual(res["status"], "REJECTED")
        self.assertFalse(res["dispatched"])
        self.assertIn("not negotiated", res["reason"])

    def test_invoking_negotiated_tools_dispatched(self):
        """Calling tools is dispatched"""
        res = invoke_capability(self.negotiated, "tools", {"cmd": "status"})
        self.assertEqual(res["status"], "DISPATCHED")
        self.assertTrue(res["dispatched"])

    def test_invoking_unoffered_prompts_rejected(self):
        """Calling prompts (not in client caps) is rejected"""
        res = invoke_capability(self.negotiated, "prompts")
        self.assertEqual(res["status"], "REJECTED")
        self.assertFalse(res["dispatched"])

    def test_invariant_trace(self):
        """Verify invariant: dispatched == (requested in client & server)"""
        for cap in ["tools", "resources", "prompts", "unknown"]:
            expected_dispatch = cap in (self.client_caps & self.server_caps)
            res = invoke_capability(self.negotiated, cap)
            self.assertEqual(res["dispatched"], expected_dispatch)

if __name__ == "__main__":
    unittest.main()
