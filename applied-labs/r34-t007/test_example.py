"""
Unit tests for Task R34-T007
"""
import unittest
from example import evaluate_threat_scenario, get_scenarios

class TestThreatScenarioRubric(unittest.TestCase):
    def setUp(self):
        self.scenarios = get_scenarios()

    def test_complete_scenario_passes(self):
        res = evaluate_threat_scenario(self.scenarios["normal"])
        self.assertEqual(res["status"], "PASS")

    def test_missing_asset_fails(self):
        res = evaluate_threat_scenario(self.scenarios["missing_asset"])
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(res["missing_field"], "asset")

    def test_unrelated_control_flagged(self):
        res = evaluate_threat_scenario(self.scenarios["unrelated_control"])
        self.assertEqual(res["status"], "FLAGGED_FOR_REVIEW")

if __name__ == "__main__":
    unittest.main()
