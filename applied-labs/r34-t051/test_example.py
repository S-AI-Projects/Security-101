"""Unit tests for Module 1 Security Scenario Rubric Checker (R34-T051)."""

import unittest
from example import check_scenario, get_default_scenarios, run_scenarios


class TestScenarioRubric(unittest.TestCase):
    def setUp(self):
        self.default_scenarios = get_default_scenarios()

    def test_complete_scenario_passes(self):
        complete = self.default_scenarios[0]
        status, msg = check_scenario(complete)
        self.assertEqual(status, "PASS")
        self.assertIn("meets structural rubric", msg)

    def test_missing_asset_fails(self):
        missing_asset = self.default_scenarios[1]
        status, msg = check_scenario(missing_asset)
        self.assertEqual(status, "FAIL")
        self.assertIn("asset", msg.lower())

    def test_unrelated_control_flagged_for_review(self):
        unrelated = self.default_scenarios[2]
        status, msg = check_scenario(unrelated)
        self.assertEqual(status, "FLAG_REVIEW")
        self.assertIn("flagged for human review", msg)

    def test_missing_other_required_fields_fails(self):
        scenario = {
            "asset": "Server",
            "threat": "DDoS",
            "control": "",
            "residual_risk": "None",
        }
        status, msg = check_scenario(scenario)
        self.assertEqual(status, "FAIL")
        self.assertIn("control", msg.lower())

    def test_run_scenarios_batch(self):
        results = run_scenarios(self.default_scenarios)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0][1], "PASS")
        self.assertEqual(results[1][1], "FAIL")
        self.assertEqual(results[2][1], "FLAG_REVIEW")

    def test_boundary_empty_scenarios(self):
        results = run_scenarios([])
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
