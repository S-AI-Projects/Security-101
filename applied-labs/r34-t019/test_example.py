import json
import subprocess
import sys
import unittest
from pathlib import Path

import example


class ScenarioRubricTests(unittest.TestCase):
    def setUp(self):
        self.valid_scenario = {
            "asset": "Test server",
            "threat": "Known vulnerability exploitation",
            "control": "Apply the security patch",
            "residual_risk": "A newly disclosed issue may remain.",
            "control_matches_threat": True,
        }

    def test_complete_scenario_passes(self):
        self.assertEqual(example.check_scenario(self.valid_scenario)["status"], "PASS")

    def test_missing_required_field_fails(self):
        scenario = dict(self.valid_scenario)
        del scenario["asset"]
        result = example.check_scenario(scenario)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("Missing or invalid required field: asset", result["errors"])

    def test_blank_or_non_string_required_field_fails(self):
        for value in ("   ", 42, None):
            with self.subTest(value=value):
                scenario = dict(self.valid_scenario, control=value)
                self.assertEqual(example.check_scenario(scenario)["status"], "FAIL")

    def test_non_object_scenario_fails(self):
        result = example.check_scenario(["not", "an", "object"])
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("Scenario must be a JSON object.", result["errors"])

    def test_control_mismatch_requires_review(self):
        scenario = dict(self.valid_scenario, control_matches_threat=False)
        result = example.check_scenario(scenario)
        self.assertEqual(result["status"], "REVIEW")
        self.assertTrue(result["warnings"])

    def test_unconfirmed_control_fit_requires_review(self):
        scenario = dict(self.valid_scenario)
        del scenario["control_matches_threat"]
        self.assertEqual(example.check_scenario(scenario)["status"], "REVIEW")


class AppliedQuestionTests(unittest.TestCase):
    def test_correct_answer_passes_after_normalization(self):
        self.assertEqual(example.check_answer("Q1", " b ")["status"], "PASS")

    def test_incorrect_answer_fails_and_includes_rationale(self):
        result = example.check_answer("Q2", "C")
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(result["rationale"])

    def test_unknown_question_fails(self):
        self.assertEqual(example.check_answer("Q99", "A")["status"], "FAIL")

    def test_every_question_has_options_answer_and_rationale(self):
        for question_id, question in example.QUESTION_BANK.items():
            with self.subTest(question_id=question_id):
                self.assertIn(question["answer"], question["options"])
                self.assertTrue(question["rationale"])
                self.assertEqual(
                    example.check_answer(question_id, question["answer"])["status"],
                    "PASS",
                )


class FixtureAndCommandTests(unittest.TestCase):
    def test_fixtures_have_three_scenarios_and_three_answers(self):
        fixture_path = Path(__file__).with_name("fixtures.json")
        with fixture_path.open(encoding="utf-8") as fixture_file:
            fixtures = json.load(fixture_file)
        self.assertEqual(len(fixtures["scenarios"]), 3)
        self.assertEqual(len(fixtures["answers"]), 3)

    def test_command_outputs_expected_statuses(self):
        result = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("example.py"))],
            check=True,
            capture_output=True,
            text=True,
        )
        output = json.loads(result.stdout)
        self.assertEqual(
            [scenario["status"] for scenario in output["scenarios"]],
            ["PASS", "REVIEW", "PASS"],
        )
        self.assertEqual(
            [question["status"] for question in output["questions"]],
            ["PASS", "PASS", "PASS"],
        )
        self.assertEqual(output["summary"], {"PASS": 5, "REVIEW": 1, "FAIL": 0})


if __name__ == "__main__":
    unittest.main()