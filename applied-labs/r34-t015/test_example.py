import unittest

from example import SCENARIOS, evaluate_scenario


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


if __name__ == "__main__":
    unittest.main()
