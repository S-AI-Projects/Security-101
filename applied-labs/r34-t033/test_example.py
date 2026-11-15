
import unittest

from example import check_scenario, local_relevance_adapter


class TestSecurityScenarioRubric(unittest.TestCase):

    def test_complete_scenario_passes(self):
        scenario = {
            "asset": "Customer records",
            "threat": "unauthorized access",
            "control": "Multi-factor authentication",
            "residual_risk": "A compromised account may still be misused."
        }

        result = check_scenario(scenario, local_relevance_adapter)
        self.assertEqual(result["status"], "PASS")

    def test_missing_asset_fails(self):
        scenario = {
            "asset": "",
            "threat": "ransomware",
            "control": "Offline backups",
            "residual_risk": "Some recent data may not be recovered."
        }

        result = check_scenario(scenario, local_relevance_adapter)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("asset", result["reason"])

    def test_unrelated_control_needs_review(self):
        scenario = {
            "asset": "Employee email accounts",
            "threat": "phishing",
            "control": "Physical server room locks",
            "residual_risk": "Employees may still respond to deceptive messages."
        }

        result = check_scenario(scenario, local_relevance_adapter)
        self.assertEqual(result["status"], "REVIEW")

    def test_missing_residual_risk_fails(self):
        scenario = {
            "asset": "Customer records",
            "threat": "unauthorized access",
            "control": "Multi-factor authentication",
            "residual_risk": ""
        }

        result = check_scenario(scenario, local_relevance_adapter)
        self.assertEqual(result["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
