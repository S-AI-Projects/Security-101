"""Unit tests for Binary Classification Evaluation and Refactoring Equivalence (R34-T056)."""

import unittest
from example import (
    ConfusionMatrix,
    compute_confusion_matrix,
    compute_metrics_from_matrix,
    evaluate_binary_classification,
    evaluate_binary_classification_baseline,
    verify_refactoring_equivalence,
)


class TestBinaryClassificationEvaluation(unittest.TestCase):
    def test_standard_lesson_fixture(self):
        y_true = [1, 1, 0, 0]
        y_pred = [1, 0, 1, 0]
        res = evaluate_binary_classification(y_true, y_pred)
        self.assertEqual(res["tp"], 1)
        self.assertEqual(res["fn"], 1)
        self.assertEqual(res["fp"], 1)
        self.assertEqual(res["tn"], 1)
        self.assertEqual(res["precision"], 0.5)
        self.assertEqual(res["recall"], 0.5)

    def test_zero_denominator_policy_precision(self):
        # When no positive predictions are made, precision denominator (tp + fp) == 0
        y_true = [1, 0]
        y_pred = [0, 0]
        res = evaluate_binary_classification(y_true, y_pred)
        self.assertEqual(res["tp"], 0)
        self.assertEqual(res["fp"], 0)
        self.assertEqual(res["precision"], 0.0)

    def test_zero_denominator_policy_recall(self):
        # When no positive true labels exist, recall denominator (tp + fn) == 0
        y_true = [0, 0]
        y_pred = [1, 0]
        res = evaluate_binary_classification(y_true, y_pred)
        self.assertEqual(res["tp"], 0)
        self.assertEqual(res["fn"], 0)
        self.assertEqual(res["recall"], 0.0)

    def test_extracted_confusion_matrix_responsibility(self):
        cm = compute_confusion_matrix([1, 1, 0, 0], [1, 0, 1, 0])
        self.assertIsInstance(cm, ConfusionMatrix)
        self.assertEqual(cm.tp, 1)
        self.assertEqual(cm.fn, 1)
        self.assertEqual(cm.fp, 1)
        self.assertEqual(cm.tn, 1)

    def test_refactoring_equivalence_proof(self):
        fixtures = [
            ([1, 1, 0, 0], [1, 0, 1, 0]),
            ([1, 0], [0, 0]),
            ([0, 1], [0, 0]),
            ([1, 1], [1, 1]),
            ([0, 0], [0, 0]),
            ([1, 0, 1, 0, 1], [1, 1, 0, 0, 1]),
        ]
        self.assertTrue(verify_refactoring_equivalence(fixtures))

    def test_invalid_length_mismatch(self):
        with self.assertRaises(ValueError):
            evaluate_binary_classification([1, 0], [1])

    def test_invalid_label_values(self):
        with self.assertRaises(ValueError):
            evaluate_binary_classification([1, 2], [1, 0])


if __name__ == "__main__":
    unittest.main()
