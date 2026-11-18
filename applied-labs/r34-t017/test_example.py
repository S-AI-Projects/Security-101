import subprocess
import unittest
from pathlib import Path

from example import (
    RECOVERY_INPUTS,
    SCENARIOS,
    evaluate_recovery_inputs,
    evaluate_scenario,
)


ROOT = Path(__file__).resolve().parents[2]


class TestThreatScenarioRubric(unittest.TestCase):
    def test_complete_phishing_scenario_passes(self):
        result = evaluate_scenario(SCENARIOS["normal"])

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["missing_fields"], [])
        self.assertEqual(result["control_review"], "matched")

    def test_missing_asset_is_reported_as_invalid(self):
        result = evaluate_scenario(SCENARIOS["boundary"])

        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["missing_fields"], ["asset"])

    def test_unrelated_control_is_flagged_for_review(self):
        result = evaluate_scenario(SCENARIOS["failure"])

        self.assertEqual(result["status"], "REVIEW")
        self.assertEqual(result["control_review"], "review")
        self.assertTrue(result["review_reasons"])

    def test_next_valid_input_recovers_after_missing_asset(self):
        failed, recovered = evaluate_recovery_inputs()

        self.assertIs(RECOVERY_INPUTS[0], SCENARIOS["boundary"])
        self.assertIs(RECOVERY_INPUTS[1], SCENARIOS["normal"])
        self.assertEqual(failed["missing_fields"], ["asset"])
        self.assertEqual(failed["status"], "FAIL")
        self.assertEqual(recovered["status"], "PASS")

    def test_documented_example_command_output(self):
        result = subprocess.run(
            ["python3", "./applied-labs/r34-t017/example.py"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout,
            "\n".join(
                (
                    "Scenario: normal (local fictional mock)",
                    "Asset: Fictional employee mailbox credentials",
                    "Threat: A phishing message tricks an employee into disclosing a password.",
                    "Control: Verify unexpected sender requests and require multi-factor authentication for mailbox access.",
                    "Residual risk: A stolen active session may still be misused before it is revoked.",
                    "Missing fields: none",
                    "Control review: matched (none)",
                    "Rubric result: PASS",
                    "",
                )
            ),
        )
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
