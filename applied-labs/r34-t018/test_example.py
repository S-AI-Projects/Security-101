import unittest

from example import compute_metrics


class TestConfusionMetrics(unittest.TestCase):
    def test_fixed_binary_fixture(self):
        metrics = compute_metrics([1, 1, 0, 0], [1, 0, 1, 0])

        self.assertEqual((metrics.tp, metrics.fn, metrics.fp, metrics.tn), (1, 1, 1, 1))
        self.assertEqual(metrics.precision, 0.5)
        self.assertEqual(metrics.recall, 0.5)

    def test_precision_is_zero_when_there_are_no_positive_predictions(self):
        metrics = compute_metrics([1, 1, 0, 0], [0, 0, 0, 0])

        self.assertEqual((metrics.tp, metrics.fn, metrics.fp, metrics.tn), (0, 2, 0, 2))
        self.assertEqual(metrics.precision, 0.0)
        self.assertEqual(metrics.recall, 0.0)

    def test_recall_is_zero_when_there_are_no_positive_true_labels(self):
        metrics = compute_metrics([0, 0], [0, 1])

        self.assertEqual((metrics.tp, metrics.fn, metrics.fp, metrics.tn), (0, 0, 1, 1))
        self.assertEqual(metrics.precision, 0.0)
        self.assertEqual(metrics.recall, 0.0)

    def test_controlled_predictions_show_precision_recall_tradeoff(self):
        true_labels = [1, 1, 0, 0]
        recall_oriented = compute_metrics(true_labels, [1, 1, 1, 0])
        precision_oriented = compute_metrics(true_labels, [1, 0, 0, 0])

        self.assertEqual(recall_oriented.recall, 1.0)
        self.assertAlmostEqual(recall_oriented.precision, 2 / 3)
        self.assertEqual(precision_oriented.precision, 1.0)
        self.assertEqual(precision_oriented.recall, 0.5)

    def test_mismatched_label_lengths_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "same length"):
            compute_metrics([1, 0], [1])

    def test_non_binary_labels_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "integers 0 or 1"):
            compute_metrics([1, 2], [1, 0])

    def test_empty_label_sequences_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            compute_metrics([], [])


if __name__ == "__main__":
    unittest.main()
