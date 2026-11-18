import unittest

from example import SCENARIOS, evaluate_scenario, review_control_alignment


class TestScenarioRubric(unittest.TestCase):
    def evaluate(self, name):
        return evaluate_scenario(dict(SCENARIOS[name], scenario=name))

    def test_complete_scenario_passes(self):
        result = self.evaluate("normal")

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["missing_fields"], [])
        self.assertEqual(result["control_review"], "matched")

    def test_scenario_without_asset_fails(self):
        result = self.evaluate("boundary")

        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["missing_fields"], ["asset"])

    def test_unrelated_control_is_flagged_for_review(self):
        result = self.evaluate("failure")

        self.assertEqual(result["status"], "REVIEW")
        self.assertEqual(result["control_review"], "review")
        self.assertTrue(result["review_reasons"])

    def test_alignment_helper_matches_and_flags_categories(self):
        self.assertEqual(
            review_control_alignment("data_exfiltration", "data_exfiltration"),
            ("matched", []),
        )
        self.assertEqual(
            review_control_alignment("data_exfiltration", "availability"),
            (
                "review",
                ["control category does not match the stated threat category"],
            ),
        )


if __name__ == "__main__":
    unittest.main()
