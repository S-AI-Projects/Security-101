"""Regression and unit tests for Zero Trust capability negotiation and dispatch gating."""

from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from example import (
    CAPABILITY_HANDLERS,
    FIXTURES,
    ZeroTrustSession,
    run_session_fixture,
)


class CapabilityNegotiationTests(unittest.TestCase):
    def test_standard_negotiation_intersects_capabilities(self):
        client_caps = {"tools", "resources"}
        server_caps = {"tools", "prompts"}
        session = ZeroTrustSession(client_caps, server_caps)
        self.assertEqual(session.negotiated, {"tools"})

    def test_calling_negotiated_capability_succeeds(self):
        session = ZeroTrustSession({"tools", "resources"}, {"tools", "prompts"})
        res = session.dispatch("tools", {"action": "query_siem"})
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["capability"], "tools")
        self.assertIn("query_siem", res["output"])

    def test_calling_unnegotiated_capability_is_rejected_before_dispatch(self):
        session = ZeroTrustSession({"tools", "resources"}, {"tools", "prompts"})

        # Mock handler to guarantee it is NEVER called
        with patch.dict(CAPABILITY_HANDLERS, {"resources": unittest.mock.MagicMock()}):
            res = session.dispatch("resources", {"uri": "file:///var/log/audit.log"})
            CAPABILITY_HANDLERS["resources"].assert_not_called()

        self.assertEqual(res["status"], "REJECTED")
        self.assertEqual(res["capability"], "resources")
        self.assertEqual(res["error"]["code"], "UNNEGOTIATED_CAPABILITY")

    def test_exact_issue_fixture_regression(self):
        # Exact issue contract:
        # Client {tools,resources}, server {tools,prompts} negotiates {tools}; calling resources is rejected before dispatch.
        report = run_session_fixture(FIXTURES["standard-negotiation"])
        self.assertEqual(report["negotiated"], ["tools"])
        self.assertEqual(len(report["results"]), 2)

        res_tools, res_resources = report["results"]
        self.assertEqual(res_tools["status"], "SUCCESS")
        self.assertEqual(res_tools["capability"], "tools")

        self.assertEqual(res_resources["status"], "REJECTED")
        self.assertEqual(res_resources["capability"], "resources")
        self.assertEqual(res_resources["error"]["code"], "UNNEGOTIATED_CAPABILITY")

    def test_documented_command_output(self):
        result = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("example.py"))],
            check=True, capture_output=True, text=True,
        )
        self.assertEqual(
            result.stdout.splitlines(),
            [
                "Negotiated capabilities: ['tools']",
                "Call to 'tools': status=SUCCESS, output=Executed tool action: query_siem",
                "Call to 'resources': status=REJECTED, error=UNNEGOTIATED_CAPABILITY",
            ],
        )

    def test_disjoint_capabilities_yields_empty_negotiation(self):
        session = ZeroTrustSession({"resources"}, {"tools", "prompts"})
        self.assertEqual(session.negotiated, set())
        res = session.dispatch("resources", {"uri": "file:///etc/hosts"})
        self.assertEqual(res["status"], "REJECTED")

    def test_full_intersection_allows_all_negotiated_capabilities(self):
        report = run_session_fixture(FIXTURES["full-intersection"])
        self.assertEqual(report["negotiated"], ["prompts", "resources", "tools"])
        for res in report["results"]:
            self.assertEqual(res["status"], "SUCCESS")


if __name__ == "__main__":
    unittest.main()
