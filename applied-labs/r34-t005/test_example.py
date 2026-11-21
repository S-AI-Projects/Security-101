"""
Unit tests for Task R34-T005
"""
import unittest
from example import LocalOfflineSecurityAdapter, get_fictional_scenarios

class TestDataSecurityRubric(unittest.TestCase):
    def setUp(self):
        self.adapter = LocalOfflineSecurityAdapter()
        self.scenarios = get_fictional_scenarios()

    def test_complete_scenario_passes(self):
        res = self.adapter.evaluate(self.scenarios["normal"])
        self.assertEqual(res["status"], "PASS")

    def test_missing_asset_fails(self):
        res = self.adapter.evaluate(self.scenarios["missing_asset"])
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(res["missing_field"], "asset")

    def test_unrelated_control_flagged(self):
        res = self.adapter.evaluate(self.scenarios["unrelated_control"])
        self.assertEqual(res["status"], "FLAGGED_FOR_REVIEW")
        self.assertIn("Flagged for review", res["message"])

if __name__ == "__main__":
    unittest.main()
