import unittest

from example import SCENARIOS, classify, evaluate


class ClassificationTests(unittest.TestCase):
    def test_every_scenario_matches_the_expected_set(self):
        for name, events, expected in SCENARIOS:
            with self.subTest(name=name):
                self.assertEqual(classify(events), expected)

    def test_three_controlled_batch_sizes(self):
        for size, expected in ((1, (1, 1)), (3, (3, 3)), (6, (6, 9))):
            with self.subTest(size=size):
                self.assertEqual(evaluate(SCENARIOS[:size]), expected)

    def test_empty_and_repeated_indicators(self):
        self.assertEqual(classify(()), set())
        self.assertEqual(classify(("altered records", "altered records")), {"integrity"})

    def test_partial_label_set_does_not_count_as_an_exact_match(self):
        case = ("partial evidence", ("altered records",), {"integrity", "availability"})
        self.assertEqual(evaluate((case,)), (0, 1))
