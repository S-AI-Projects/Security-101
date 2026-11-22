"""Regression tests for R34-T021 AI-security scenario rubric."""

import unittest

from example import (
    COMPLETE_SCENARIO,
    LESSON_CITATION,
    MISSING_ASSET_SCENARIO,
    UNRELATED_CONTROL_SCENARIO,
    check_scenario,
    run_scenario,
)


class AIScenarioRubricTests(unittest.TestCase):
    def test_complete_scenario_passes(self):
        self.assertEqual(check_scenario(COMPLETE_SCENARIO), "pass")

    def test_scenario_without_asset_fails(self):
        self.assertEqual(check_scenario(MISSING_ASSET_SCENARIO), "fail")

    def test_unrelated_control_flags_review(self):
        self.assertEqual(check_scenario(UNRELATED_CONTROL_SCENARIO), "review")

    def test_empty_residual_risk_fails(self):
        scenario = dict(COMPLETE_SCENARIO)
        scenario["residual_risk"] = ""
        self.assertEqual(check_scenario(scenario), "fail")

    def test_named_lesson_section_is_preserved(self):
        self.assertEqual(COMPLETE_SCENARIO["section"], "Data Integrity")
        self.assertEqual(MISSING_ASSET_SCENARIO["section"], "Adversarial Attacks")
        self.assertEqual(UNRELATED_CONTROL_SCENARIO["section"], "Responsible AI")

    def test_public_inputs_and_outputs_are_connected_to_fixture(self):
        self.assertIn(COMPLETE_SCENARIO["asset"], "Training dataset")
        self.assertIn(COMPLETE_SCENARIO["threat"], "unauthorized data modification")
        self.assertIn(COMPLETE_SCENARIO["control"], "data integrity validation")

    def test_normal_scenario_exact_output(self):
        code, output = run_scenario("normal")
        expected = (
            f'Scenario: AI-security rubric based on "{LESSON_CITATION}".\n'
            "section=Data Integrity\n"
            "asset=Training dataset\n"
            "threat=unauthorized data modification\n"
            "control=data integrity validation\n"
            "residual_risk=Novel manipulation patterns may remain\n"
            "result=pass"
        )
        self.assertEqual(code, 0)
        self.assertEqual(output, expected)

    def test_boundary_scenario(self):
        code, output = run_scenario("boundary")
        self.assertEqual(code, 0)
        self.assertIn("complete=pass", output)
        self.assertIn("missing_asset=fail", output)
        self.assertIn("unrelated_control=review", output)

    def test_failure_scenario(self):
        code, output = run_scenario("failure")
        self.assertEqual(code, 1)
        self.assertIn("Missing asset result=fail", output)
        self.assertIn("Unrelated control result=review", output)

    def test_deliberate_wrong_result_fails(self):
        actual = check_scenario(COMPLETE_SCENARIO)
        with self.assertRaises(AssertionError):
            self.assertEqual(actual, "fail", "Deliberate wrong rubric result")


if __name__ == "__main__":
    unittest.main()
