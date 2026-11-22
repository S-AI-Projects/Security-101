"""Unit tests and regression checks for binary classification metrics (R34-T026)."""

import unittest

from example import (
    BOUNDARY_ZERO_PRED_PRED,
    BOUNDARY_ZERO_PRED_TRUE,
    BOUNDARY_ZERO_TRUE_PRED,
    BOUNDARY_ZERO_TRUE_TRUE,
    CANONICAL_Y_PRED,
    CANONICAL_Y_TRUE,
    FAILURE_MISMATCH_PRED,
    FAILURE_MISMATCH_TRUE,
    LESSON_CITATION,
    SCENARIO_EXPLANATIONS,
    compute_metrics,
    get_worked_explanation,
    run_scenario,
)


class ClassificationMetricsTests(unittest.TestCase):
    """Test suite verifying confusion matrix calculations, zero-denominator policy, and regression."""

    def test_canonical_fixture_counts_and_metrics(self):
        """Canonical test: y_true=[1,1,0,0], y_pred=[1,0,1,0] yields TP=1, FN=1, FP=1, TN=1, precision=recall=0.5."""
        m = compute_metrics(CANONICAL_Y_TRUE, CANONICAL_Y_PRED)
        self.assertEqual(m.tp, 1)
        self.assertEqual(m.fn, 1)
        self.assertEqual(m.fp, 1)
        self.assertEqual(m.tn, 1)
        self.assertEqual(m.precision, 0.5)
        self.assertEqual(m.recall, 0.5)

    def test_zero_positive_predictions_precision_is_zero(self):
        """No positive predictions yields precision=0.0 under the documented zero-denominator policy."""
        m = compute_metrics(BOUNDARY_ZERO_PRED_TRUE, BOUNDARY_ZERO_PRED_PRED)
        self.assertEqual((m.tp, m.fn, m.fp, m.tn), (0, 2, 0, 2))
        self.assertEqual(m.precision, 0.0)
        self.assertEqual(m.recall, 0.0)

    def test_zero_positive_true_labels_recall_is_zero(self):
        """No positive true labels yields recall=0.0 under the documented zero-denominator policy."""
        m = compute_metrics(BOUNDARY_ZERO_TRUE_TRUE, BOUNDARY_ZERO_TRUE_PRED)
        self.assertEqual((m.tp, m.fn, m.fp, m.tn), (0, 0, 1, 1))
        self.assertEqual(m.precision, 0.0)
        self.assertEqual(m.recall, 0.0)

    def test_all_correct_predictions(self):
        """Perfect classification yields precision=1.0 and recall=1.0."""
        m = compute_metrics([1, 0, 1, 0], [1, 0, 1, 0])
        self.assertEqual((m.tp, m.fn, m.fp, m.tn), (2, 0, 0, 2))
        self.assertEqual(m.precision, 1.0)
        self.assertEqual(m.recall, 1.0)

    def test_worked_explanation_contains_step_traces(self):
        """Focus: Worked input-to-output explanation details each index step and metric formula."""
        explanation = get_worked_explanation(CANONICAL_Y_TRUE, CANONICAL_Y_PRED)
        self.assertIn("Worked Input-to-Output Explanation:", explanation)
        self.assertIn("Index 0: actual=1, predicted=1 -> True Positive (TP)", explanation)
        self.assertIn("Index 1: actual=1, predicted=0 -> False Negative (FN)", explanation)
        self.assertIn("Index 2: actual=0, predicted=1 -> False Positive (FP)", explanation)
        self.assertIn("Index 3: actual=0, predicted=0 -> True Negative (TN)", explanation)
        self.assertIn("Final Confusion Matrix: TP=1, FN=1, FP=1, TN=1", explanation)
        self.assertIn("Precision calculation: TP / (TP + FP) = 1 / (1 + 1) = 0.500", explanation)
        self.assertIn("Recall calculation:    TP / (TP + FN) = 1 / (1 + 1) = 0.500", explanation)

    def test_exact_example_regression_output(self):
        """Focus: Regression test asserting exact CLI output matches documented text."""
        code, output = run_scenario("normal")
        self.assertEqual(code, 0)
        expected_lines = [
            f'Scenario: Canonical binary classification evaluation based on "{LESSON_CITATION}"; '
            "computes TP, FN, FP, TN, precision, and recall on balanced fixture.",
            "y_true=[1, 1, 0, 0], y_pred=[1, 0, 1, 0]",
            "Confusion matrix: TP=1, FN=1, FP=1, TN=1",
            "precision=0.500, recall=0.500",
            "Zero-denominator policy: explicit 0.0 fallback when denominator is 0.",
        ]
        self.assertEqual(output.strip(), "\n".join(expected_lines))

    def test_mismatched_sequence_lengths_rejected(self):
        """Mismatched sequence lengths raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Mismatched sequence lengths"):
            compute_metrics(FAILURE_MISMATCH_TRUE, FAILURE_MISMATCH_PRED)

    def test_non_binary_labels_rejected(self):
        """Non-binary labels raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Must be integer 0 or 1"):
            compute_metrics([1, 2], [1, 0])
        with self.assertRaisesRegex(ValueError, "Must be integer 0 or 1"):
            compute_metrics([1, 0], [1, "0"])  # type: ignore

    def test_empty_sequence_rejected(self):
        """Empty label sequences raise ValueError."""
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            compute_metrics([], [])

    def test_scenario_citations_cite_lesson(self):
        """Scenario explanations cite 7.1 Data security key concepts.md."""
        for name, explanation in SCENARIO_EXPLANATIONS.items():
            self.assertIn(
                LESSON_CITATION,
                explanation,
                f"Scenario '{name}' does not cite {LESSON_CITATION}",
            )

    def test_boundary_scenario_execution(self):
        """Boundary scenario runs with exit code 0."""
        code, output = run_scenario("boundary")
        self.assertEqual(code, 0)
        self.assertIn(LESSON_CITATION, output)
        self.assertIn("precision=0.000", output)
        self.assertIn("recall=0.000", output)

    def test_failure_scenario_execution(self):
        """Failure scenario runs with exit code 1 on mismatched input lengths."""
        code, output = run_scenario("failure")
        self.assertEqual(code, 1)
        self.assertIn("Error:", output)
        self.assertIn("Mismatched sequence lengths", output)

    def test_deliberate_wrong_result_fails(self):
        """Deliberate wrong result assertion fails with AssertionError."""
        m = compute_metrics(CANONICAL_Y_TRUE, CANONICAL_Y_PRED)
        # Intentionally wrong expectation (expecting TP=2 instead of TP=1)
        with self.assertRaises(AssertionError):
            self.assertEqual(m.tp, 2, "Deliberate wrong result check")


if __name__ == "__main__":
    unittest.main()
