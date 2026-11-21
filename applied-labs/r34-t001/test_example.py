"""
Unit tests for Infrastructure Security Rubric Checker (Task R34-T001)
"""
import unittest
from example import check_scenario, get_fictional_scenarios

class TestScenarioRubric(unittest.TestCase):
    def setUp(self):
        self.scenarios = get_fictional_scenarios()

    def test_complete_scenario_passes(self):
        """Test that a complete and consistent scenario passes."""
        res = check_scenario(self.scenarios["normal"])
        self.assertEqual(res["status"], "PASS")
        self.assertIn("complete", res["message"])

    def test_missing_asset_fails(self):
        """Test that a scenario missing an asset fails."""
        res = check_scenario(self.scenarios["missing_asset"])
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(res.get("missing_field"), "asset")

    def test_unrelated_control_flagged(self):
        """Test that a control unrelated to the named threat is flagged for review."""
        res = check_scenario(self.scenarios["unrelated_control"])
        self.assertEqual(res["status"], "FLAGGED_FOR_REVIEW")
        self.assertIn("Flagged for review", res["message"])

    def test_missing_threat_fails(self):
        """Test that missing threat fails rubric."""
        bad_scenario = {
            "asset": "Cloud Server",
            "threat": "",
            "control": "Firewall",
            "residual_risk": "Bypass"
        }
        res = check_scenario(bad_scenario)
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(res["missing_field"], "threat")

    def test_missing_control_fails(self):
        """Test that missing control fails rubric."""
        bad_scenario = {
            "asset": "Cloud Server",
            "threat": "DDoS",
            "control": "",
            "residual_risk": "Bypass"
        }
        res = check_scenario(bad_scenario)
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(res["missing_field"], "control")

    def test_missing_residual_risk_fails(self):
        """Test that missing residual risk fails rubric."""
        bad_scenario = {
            "asset": "Cloud Server",
            "threat": "DDoS",
            "control": "Rate limiting",
            "residual_risk": ""
        }
        res = check_scenario(bad_scenario)
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(res["missing_field"], "residual_risk")

if __name__ == "__main__":
    unittest.main()
