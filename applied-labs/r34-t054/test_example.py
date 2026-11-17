"""Unit tests for Infrastructure Security Rubric with Adapter (R34-T054)."""

import unittest
from example import (
    LocalInfrastructureAdapter,
    ScenarioSourceAdapter,
    check_scenario,
    evaluate_adapter,
)


class TestInfrastructureRubricAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = LocalInfrastructureAdapter()

    def test_complete_scenario_passes(self):
        scenarios = self.adapter.fetch_scenarios()
        status, msg = check_scenario(scenarios[0])
        self.assertEqual(status, "PASS")

    def test_missing_asset_fails(self):
        scenarios = self.adapter.fetch_scenarios()
        status, msg = check_scenario(scenarios[1])
        self.assertEqual(status, "FAIL")
        self.assertIn("asset", msg.lower())

    def test_mismatched_control_flagged_for_review(self):
        scenarios = self.adapter.fetch_scenarios()
        status, msg = check_scenario(scenarios[2])
        self.assertEqual(status, "FLAG_REVIEW")
        self.assertIn("flagged for human review", msg)

    def test_custom_mock_adapter(self):
        class MockCustomAdapter(ScenarioSourceAdapter):
            def fetch_scenarios(self):
                return [
                    {
                        "name": "Custom",
                        "asset": "Edge router",
                        "threat": "Unauthorized access",
                        "control": "Enforce MFA and RBAC",
                        "residual_risk": "Local console access",
                    }
                ]

        results = evaluate_adapter(MockCustomAdapter())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "PASS")

    def test_boundary_empty_adapter(self):
        class EmptyAdapter(ScenarioSourceAdapter):
            def fetch_scenarios(self):
                return []

        results = evaluate_adapter(EmptyAdapter())
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
