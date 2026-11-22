"""Regression tests for R34-T022 infrastructure rubric boundaries."""

import unittest

from example import (
    BOUNDARY_CONTROL,
    INVALID_NO_ASSET,
    LESSON_CITATION,
    SMALLEST_VALID,
    check_scenario,
    run_scenario,
)


class InfrastructureRubricTests(unittest.TestCase):
    def test_smallest_valid_scenario_passes(self):
        self.assertEqual(check_scenario(SMALLEST_VALID), "pass")

    def test_missing_asset_fails(self):
        self.assertEqual(check_scenario(INVALID_NO_ASSET), "fail")

    def test_nonempty_unrelated_control_is_review(self):
        self.assertEqual(check_scenario(BOUNDARY_CONTROL), "review")

    def test_smallest_valid_has_only_required_fields(self):
        self.assertEqual(set(SMALLEST_VALID), {
            "name", "section", "asset", "threat", "control", "residual_risk"
        })
        self.assertTrue(all(SMALLEST_VALID[key].strip() for key in
                            ("asset", "threat", "control", "residual_risk")))

    def test_exact_boundary_empty_vs_unrelated(self):
        self.assertEqual(check_scenario({"name": "Whitespace asset", "section": "CSPM",
                                         "asset": "   ", "threat": "public cloud misconfiguration",
                                         "control": "remediate insecure cloud configuration",
                                         "residual_risk": "policy drift"}), "fail")
        self.assertEqual(check_scenario(BOUNDARY_CONTROL), "review")

    def test_human_explanation_limit(self):
        human_copy = dict(SMALLEST_VALID)
        human_copy["residual_risk"] = ""
        self.assertEqual(check_scenario(human_copy), "fail")

    def test_normal_scenario_exact_output(self):
        code, output = run_scenario("normal")
        expected = (
            f'Scenario: smallest-valid rubric based on "{LESSON_CITATION}".\n'
            "fixture=Smallest valid\n"
            "asset=Server\n"
            "threat=known server vulnerability\n"
            "control=apply vendor patch\n"
            "residual_risk=zero-day risk remains\n"
            "result=pass"
        )
        self.assertEqual(code, 0)
        self.assertEqual(output, expected)

    def test_boundary_scenario_exact_decisions(self):
        code, output = run_scenario("boundary")
        self.assertEqual(code, 0)
        self.assertIn("Smallest valid=pass", output)
        self.assertIn("Boundary control=review", output)
        self.assertIn("Missing asset=fail", output)
        self.assertIn("empty required field is fail", output)

    def test_failure_scenario_reports_invalid_and_boundary(self):
        code, output = run_scenario("failure")
        self.assertEqual(code, 1)
        self.assertIn("Missing asset result=fail", output)
        self.assertIn("Boundary control result=review", output)

    def test_deliberate_wrong_result_fails(self):
        actual = check_scenario(SMALLEST_VALID)
        with self.assertRaises(AssertionError):
            self.assertEqual(actual, "fail", "Deliberate wrong rubric result")


if __name__ == "__main__":
    unittest.main()
