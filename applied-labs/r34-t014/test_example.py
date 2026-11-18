import unittest

from example import (
    SCENARIOS,
    evaluate_scenario,
    final_matches_recorded_state,
)


class TestScenarioRubric(unittest.TestCase):
    def evaluate(self, name):
        return evaluate_scenario(dict(SCENARIOS[name], scenario=name))

    def test_complete_scenario_passes(self):
        result = self.evaluate("normal")

        self.assertEqual(result["final"]["status"], "PASS")
        self.assertEqual(result["final"]["missing_fields"], [])
        self.assertEqual(result["final"]["control_review"], "matched")

    def test_scenario_without_asset_fails_completeness(self):
        result = self.evaluate("boundary")

        self.assertEqual(result["final"]["status"], "FAIL")
        self.assertEqual(result["final"]["missing_fields"], ["asset"])

    def test_unrelated_control_is_flagged_for_human_review(self):
        result = self.evaluate("failure")

        self.assertEqual(result["final"]["status"], "REVIEW")
        self.assertEqual(result["final"]["control_review"], "review")
        self.assertTrue(result["final"]["review_reasons"])

    def test_final_output_matches_each_recorded_step(self):
        for name in SCENARIOS:
            with self.subTest(scenario=name):
                result = self.evaluate(name)

                self.assertEqual(
                    [state["stage"] for state in result["states"]],
                    ["received", "normalized", "completeness", "control_review", "final"],
                )
                self.assertTrue(final_matches_recorded_state(result))

    def test_invariant_detects_a_changed_final_result(self):
        result = self.evaluate("normal")
        result["final"]["status"] = "FAIL"

        self.assertFalse(final_matches_recorded_state(result))

    def test_invariant_detects_a_changed_intermediate_state(self):
        result = self.evaluate("normal")
        result["states"][1]["fields"]["asset"] = "different asset"

        self.assertFalse(final_matches_recorded_state(result))


if __name__ == "__main__":
    unittest.main()
