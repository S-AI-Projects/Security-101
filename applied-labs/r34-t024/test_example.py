"""Regression tests for R34-T024 capability negotiation."""

import unittest

from example import (
    CLIENT_CAPABILITIES,
    LESSON_CITATION,
    SERVER_CAPABILITIES,
    CapabilityGate,
    LocalCapabilityAdapter,
    negotiate,
    run_scenario,
)


class CapabilityNegotiationTests(unittest.TestCase):
    def test_fixture_negotiates_tools_only(self):
        negotiated = negotiate(CLIENT_CAPABILITIES, SERVER_CAPABILITIES)
        self.assertEqual(negotiated, frozenset({"tools"}))

    def test_tools_can_be_dispatched(self):
        adapter = LocalCapabilityAdapter(SERVER_CAPABILITIES)
        gate = CapabilityGate(adapter)
        result = gate.negotiate_and_call(CLIENT_CAPABILITIES, "tools")
        self.assertEqual(result, "dispatched:tools")
        self.assertEqual(adapter.dispatch_count, 1)

    def test_resources_are_rejected_before_dispatch(self):
        adapter = LocalCapabilityAdapter(SERVER_CAPABILITIES)
        gate = CapabilityGate(adapter)
        with self.assertRaisesRegex(PermissionError, "not negotiated"):
            gate.negotiate_and_call(CLIENT_CAPABILITIES, "resources")
        self.assertEqual(adapter.dispatch_count, 0)

    def test_boundary_empty_overlap(self):
        self.assertEqual(
            negotiate(frozenset({"resources"}), frozenset({"prompts"})),
            frozenset(),
        )

    def test_local_adapter_is_callable_and_deterministic(self):
        adapter = LocalCapabilityAdapter(SERVER_CAPABILITIES)
        self.assertEqual(
            adapter.negotiate(CLIENT_CAPABILITIES),
            frozenset({"tools"}),
        )
        self.assertEqual(adapter.dispatch("tools"), "dispatched:tools")

    def test_normal_scenario_exact_output(self):
        code, output = run_scenario("normal")
        expected = (
            f'Scenario: capability intersection based on "{LESSON_CITATION}".\n'
            "client=['resources', 'tools']\n"
            "server=['prompts', 'tools']\n"
            "negotiated=['tools']\n"
            "tools result=dispatched:tools"
        )
        self.assertEqual(code, 0)
        self.assertEqual(output, expected)

    def test_boundary_scenario(self):
        code, output = run_scenario("boundary")
        self.assertEqual(code, 0)
        self.assertIn("fixture_overlap=['tools']", output)
        self.assertIn("empty_overlap=[]", output)

    def test_failure_scenario_rejects_before_dispatch(self):
        code, output = run_scenario("failure")
        self.assertEqual(code, 1)
        self.assertIn("resources", output)
        self.assertIn("not negotiated", output)

    def test_explain_scenario_reports_no_dispatch(self):
        code, output = run_scenario("explain")
        self.assertEqual(code, 0)
        self.assertIn("negotiated=['tools']", output)
        self.assertIn("resources result=rejected_before_dispatch", output)
        self.assertIn("dispatch_count=0", output)

    def test_deliberate_wrong_result_fails(self):
        negotiated = negotiate(CLIENT_CAPABILITIES, SERVER_CAPABILITIES)
        with self.assertRaises(AssertionError):
            self.assertEqual(
                negotiated,
                frozenset({"tools", "resources"}),
                "Deliberate wrong negotiation",
            )


if __name__ == "__main__":
    unittest.main()
