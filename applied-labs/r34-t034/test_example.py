
import unittest

from example import evaluate_scenario


class TestScenarioChecker(unittest.TestCase):

    def test_complete_scenario_passes(self):
        scenario = {
            "id": "TEST-01",
            "lesson_section": "5.1 Input Validation",
            "asset": "Customer records",
            "threat": "SQL injection",
            "control": "Parameterized queries",
            "residual_risk": "Other risks may remain"
        }

        result = evaluate_scenario(scenario)
        self.assertEqual(result["status"], "PASS")

    def test_missing_asset_fails(self):
        scenario = {
            "id": "TEST-02",
            "lesson_section": "5.1 Output Encoding",
            "asset": "",
            "threat": "Cross-site scripting",
            "control": "Output encoding",
            "residual_risk": "Other risks may remain"
        }

        result = evaluate_scenario(scenario)
        self.assertEqual(result["status"], "FAIL")

    def test_unrelated_control_needs_review(self):
        scenario = {
            "id": "TEST-03",
            "lesson_section": "5.2 AppSec",
            "asset": "Payment records",
            "threat": "SQL injection",
            "control": "Secure development training",
            "residual_risk": "Other risks may remain"
        }

        result = evaluate_scenario(scenario)
        self.assertEqual(result["status"], "REVIEW")

    def test_final_output_matches_last_recorded_state(self):
        scenario = {
            "id": "TEST-04",
            "lesson_section": "5.1 Input Validation",
            "asset": "Customer records",
            "threat": "SQL injection",
            "control": "Parameterized queries",
            "residual_risk": "Other risks may remain"
        }

        result = evaluate_scenario(scenario)
        final_state = result["trace"][-1]

        self.assertEqual(result["status"], final_state["status"])
        self.assertEqual(result["reason"], final_state["reason"])
        self.assertEqual(final_state["stage"], "finalized")

    def test_whitespace_only_asset_fails(self):
        scenario = {
            "id": "TEST-05",
            "lesson_section": "5.1 Input Validation",
            "asset": "   ",
            "threat": "SQL injection",
            "control": "Parameterized queries",
            "residual_risk": "Other risks may remain"
        }

        result = evaluate_scenario(scenario)
        self.assertEqual(result["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
