"""Unit tests for the teaching responsibility matrix example (R34-T030)."""

import unittest

from example import (
    APPLIED_QUESTIONS,
    BOUNDARY_FIXTURE,
    FAILURE_FIXTURE,
    LESSON_CITATION,
    NORMAL_FIXTURE,
    SCENARIO_EXPLANATIONS,
    VALID_RESPONSIBLE_PARTIES,
    VALID_SERVICE_MODELS,
    evaluate_matrix,
    evaluate_task_responsibility,
    format_matrix,
    run_scenario,
)


class ResponsibilityMatrixTests(unittest.TestCase):
    """Test suite for the shared responsibility matrix and scenario assessments."""

    def test_normal_fixture_all_tasks_have_explicit_ownership(self):
        """Every task in the normal fixture must have explicit customer/provider/shared ownership."""
        evaluated = evaluate_matrix(NORMAL_FIXTURE)
        self.assertEqual(len(evaluated), 7)

        observed_parties = {row["responsible_party"] for row in evaluated}
        observed_models = {row["service_model"] for row in evaluated}

        # Confirms customer, provider, and shared ownership are all present
        self.assertEqual(observed_parties, set(VALID_RESPONSIBLE_PARTIES))
        # Confirms all three cloud models (IaaS, PaaS, SaaS) are covered
        self.assertEqual(observed_models, set(VALID_SERVICE_MODELS))

        for row in evaluated:
            self.assertEqual(row["status"], "ASSIGNED")
            self.assertIn(row["responsible_party"], VALID_RESPONSIBLE_PARTIES)

    def test_missing_ownership_flagged_unassigned(self):
        """Missing or omitted ownership must be flagged UNASSIGNED, not assumed provider."""
        missing_party_entry = {
            "task": "Configure network security groups",
            "service_model": "IaaS",
        }
        result = evaluate_task_responsibility(missing_party_entry)
        self.assertEqual(result["responsible_party"], "UNASSIGNED")
        self.assertEqual(result["status"], "FLAGGED_UNASSIGNED")
        self.assertNotEqual(result["responsible_party"], "provider")

        empty_party_entry = {
            "task": "Define API rate limits",
            "service_model": "PaaS",
            "responsible_party": "   ",
        }
        result_empty = evaluate_task_responsibility(empty_party_entry)
        self.assertEqual(result_empty["responsible_party"], "UNASSIGNED")
        self.assertEqual(result_empty["status"], "FLAGGED_UNASSIGNED")

    def test_invalid_ownership_flagged_invalid(self):
        """An unrecognized responsible party must be flagged as INVALID."""
        invalid_party_entry = {
            "task": "Configure user access",
            "service_model": "SaaS",
            "responsible_party": "third_party_vendor",
        }
        result = evaluate_task_responsibility(invalid_party_entry)
        self.assertEqual(result["responsible_party"], "INVALID")
        self.assertEqual(result["status"], "FLAGGED_INVALID")

    def test_invalid_service_model_raises_value_error(self):
        """An unsupported service model must raise ValueError."""
        entry = {
            "task": "Maintain server hardware",
            "service_model": "OnPremise",
            "responsible_party": "customer",
        }
        with self.assertRaises(ValueError) as ctx:
            evaluate_task_responsibility(entry)
        self.assertIn("Invalid service model", str(ctx.exception))

    def test_blank_task_name_raises_value_error(self):
        """An empty or blank task name must raise ValueError."""
        with self.assertRaises(ValueError):
            evaluate_task_responsibility({"task": "", "service_model": "IaaS"})
        with self.assertRaises(ValueError):
            evaluate_task_responsibility({"task": "   ", "service_model": "IaaS"})

    def test_non_dict_entry_raises_type_error(self):
        """Non-dictionary items must raise TypeError."""
        with self.assertRaises(TypeError):
            evaluate_task_responsibility("not_a_dict")  # type: ignore

    def test_scenario_explanations_cite_lesson(self):
        """Scenario explanations must cite '1.6 Shared responsibility model.md'."""
        for name, explanation in SCENARIO_EXPLANATIONS.items():
            self.assertIn(
                LESSON_CITATION,
                explanation,
                f"Scenario '{name}' does not cite {LESSON_CITATION}",
            )

    def test_normal_scenario_execution(self):
        """Running the normal scenario returns code 0 and formatted matrix."""
        code, output = run_scenario("normal")
        self.assertEqual(code, 0)
        self.assertIn(LESSON_CITATION, output)
        self.assertIn("Patch guest operating system | IaaS | customer", output)
        self.assertIn("Protect physical host | IaaS | provider", output)
        self.assertIn("Review data handling | PaaS | shared", output)

    def test_boundary_scenario_execution(self):
        """Running the boundary scenario returns code 0 and flags unassigned tasks."""
        code, output = run_scenario("boundary")
        self.assertEqual(code, 0)
        self.assertIn("Configure network security groups | IaaS | UNASSIGNED", output)
        self.assertIn("Enforce MFA on user accounts | SaaS | UNASSIGNED", output)

    def test_failure_scenario_execution(self):
        """Running the failure scenario returns code 1 and error output."""
        code, output = run_scenario("failure")
        self.assertEqual(code, 1)
        self.assertIn("Error:", output)
        self.assertIn("Invalid service model 'OnPremise'", output)

    def test_question_1_predict_output(self):
        """Q1: Predict responsible party for IaaS guest operating system patching."""
        entry = {
            "task": "Patch guest operating system",
            "service_model": "IaaS",
            "responsible_party": "customer",
        }
        res = evaluate_task_responsibility(entry)
        self.assertEqual(res["responsible_party"], "customer")
        self.assertEqual(res["responsible_party"], APPLIED_QUESTIONS["question_1"]["expected_answer"])

    def test_question_2_diagnose_failure(self):
        """Q2: Diagnose why unassigned task is not assumed provider-managed."""
        entry = {
            "task": "Enforce MFA on user accounts",
            "service_model": "SaaS",
        }
        res = evaluate_task_responsibility(entry)
        self.assertEqual(res["responsible_party"], "UNASSIGNED")
        self.assertEqual(res["status"], "FLAGGED_UNASSIGNED")
        self.assertEqual(res["responsible_party"], APPLIED_QUESTIONS["question_2"]["expected_answer"])

    def test_question_3_choose_boundary_policy(self):
        """Q3: Boundary policy must flag unassigned ownership rather than defaulting to provider."""
        boundary_entries = evaluate_matrix(BOUNDARY_FIXTURE)
        for row in boundary_entries:
            self.assertEqual(row["responsible_party"], "UNASSIGNED")
            self.assertNotEqual(row["responsible_party"], "provider")
        self.assertEqual("UNASSIGNED", APPLIED_QUESTIONS["question_3"]["expected_answer"])

    def test_deliberate_wrong_result_fails(self):
        """Confirm that an erroneous expectation raises AssertionError."""
        entry = {
            "task": "Patch guest operating system",
            "service_model": "IaaS",
            "responsible_party": "customer",
        }
        actual = evaluate_task_responsibility(entry)["responsible_party"]
        # Intentionally wrong assertion
        with self.assertRaises(AssertionError):
            self.assertEqual(actual, "provider", "Deliberate wrong result check")


if __name__ == "__main__":
    unittest.main()
