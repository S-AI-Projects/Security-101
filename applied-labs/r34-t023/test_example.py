"""Regression tests for R34-T023 structural scenario rubric."""

import unittest

from example import (
    COMPLETE_SCENARIO,
    LESSON_CITATION,
    MISSING_ASSET_SCENARIO,
    UNRELATED_CONTROL_SCENARIO,
    check_scenario,
    compare_direct_and_table,
    independent_table_check,
    run_scenario,
)


class ScenarioRubricTests(unittest.TestCase):
    def test_complete_scenario_passes(self):
        self.assertEqual(check_scenario(COMPLETE_SCENARIO), "pass")

    def test_missing_asset_fails(self):
        self.assertEqual(check_scenario(MISSING_ASSET_SCENARIO), "fail")

    def test_unrelated_control_flags_review(self):
        self.assertEqual(check_scenario(UNRELATED_CONTROL_SCENARIO), "review")

    def test_human_explanation_is_not_automatically_judged(self):
        scenario = dict(COMPLETE_SCENARIO)
        scenario["residual_risk"] = ""
        self.assertEqual(check_scenario(scenario), "fail")

    def test_direct_and_independent_table_agree(self):
        fixtures = (
            COMPLETE_SCENARIO,
            MISSING_ASSET_SCENARIO,
            UNRELATED_CONTROL_SCENARIO,
        )
        direct, equivalent = compare_direct_and_table(fixtures)
        self.assertEqual(
            direct,
            {
                "Web input": "pass",
                "Missing asset": "fail",
                "Unrelated control": "review",
            },
        )
        self.assertTrue(equivalent)

    def test_independent_table_has_identical_inputs(self):
        self.assertEqual(independent_table_check(COMPLETE_SCENARIO), "pass")
        self.assertEqual(independent_table_check(MISSING_ASSET_SCENARIO), "fail")
        self.assertEqual(
            independent_table_check(UNRELATED_CONTROL_SCENARIO),
            "review",
        )

    def test_normal_scenario_exact_output(self):
        code, output = run_scenario("normal")
        expected = (
            f'Scenario: structural rubric based on "{LESSON_CITATION}".\n'
            "fixture=Web input\n"
            "asset=Customer-profile web form\n"
            "threat=malformed or malicious input\n"
            "control=server-side allowlist validation\n"
            "residual_risk=Unknown payloads may remain and require monitoring\n"
            "result=pass"
        )
        self.assertEqual(code, 0)
        self.assertEqual(output, expected)

    def test_boundary_scenario(self):
        code, output = run_scenario("boundary")
        self.assertEqual(code, 0)
        self.assertIn("Web input=pass", output)
        self.assertIn("Missing asset=fail", output)
        self.assertIn("Unrelated control=review", output)
        self.assertIn("direct_table_equivalent=true", output)

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
