"""Unit and regression tests for Data Security Scenario Rubric (R34-T055)."""

import unittest
from example import (
    check_scenario,
    get_worked_example_scenarios,
    run_scenarios,
)


class TestDataSecurityRubric(unittest.TestCase):
    def setUp(self):
        self.scenarios = get_worked_example_scenarios()

    def test_complete_scenario_passes(self):
        status, msg = check_scenario(self.scenarios[0])
        self.assertEqual(status, "PASS")
        self.assertIn("meets structural rubric", msg)

    def test_missing_asset_fails(self):
        status, msg = check_scenario(self.scenarios[1])
        self.assertEqual(status, "FAIL")
        self.assertIn("asset", msg.lower())

    def test_mismatched_control_flagged_for_review(self):
        status, msg = check_scenario(self.scenarios[2])
        self.assertEqual(status, "FLAG_REVIEW")
        self.assertIn("flagged for human review", msg)

    def test_worked_example_exact_regression(self):
        """Regression test ensuring exact worked example matches expected contract."""
        results = run_scenarios(self.scenarios)
        self.assertEqual(len(results), 3)

        # 1. Customer PII Database
        self.assertEqual(results[0][0], "Customer PII Database")
        self.assertEqual(results[0][1], "PASS")

        # 2. Missing asset data scenario
        self.assertEqual(results[1][0], "Missing asset data scenario")
        self.assertEqual(results[1][1], "FAIL")
        self.assertEqual(results[1][2], "Missing required field: asset")

        # 3. Mismatched data protection control
        self.assertEqual(results[2][0], "Mismatched data protection control")
        self.assertEqual(results[2][1], "FLAG_REVIEW")

    def test_boundary_empty_scenarios(self):
        results = run_scenarios([])
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
