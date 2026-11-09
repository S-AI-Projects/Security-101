import unittest

from example import check_scenario, check_control_match


class TestScenarioChecker(unittest.TestCase):

    def test_complete_scenario_passes(self):
        scenario = {
            "asset": "Student records",
            "threat": "unauthorized access",
            "control": "access control and multi-factor authentication",
            "residual_risk": "An account could still be misused."
        }

        result = check_scenario(scenario)
        self.assertEqual(result["status"], "PASS")

    def test_missing_asset_fails(self):
        scenario = {
            "threat": "phishing",
            "control": "email filtering",
            "residual_risk": "Some emails may get through."
        }

        result = check_scenario(scenario)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("asset", result["missing_fields"])

    def test_matching_control(self):
        scenario = {
            "threat": "phishing",
            "control": "email filtering"
        }

        self.assertEqual(check_control_match(scenario), "MATCH")

    def test_unrelated_control_needs_review(self):
        scenario = {
            "threat": "physical theft",
            "control": "password awareness training"
        }

        self.assertEqual(check_control_match(scenario), "REVIEW")


if __name__ == "__main__":
    unittest.main()
    