"""Unit tests and evaluation experiment checks for Infrastructure Rubric (R34-T059)."""

import unittest
from example import (
    check_scenario,
    get_canonical_scenarios,
    run_evaluation_experiment,
)


class TestInfrastructureRubricExperiment(unittest.TestCase):
    def setUp(self):
        self.scenarios = get_canonical_scenarios()

    def test_complete_scenario_passes(self):
        status, msg = check_scenario(self.scenarios[0])
        self.assertEqual(status, "PASS")
        self.assertIn("meets structural rubric", msg)

    def test_missing_asset_fails(self):
        status, msg = check_scenario(self.scenarios[1])
        self.assertEqual(status, "FAIL")
        self.assertIn("asset", msg.lower())

    def test_mismatched_control_flagged_for_review(self):
        status, msg = check_scenario(self.scenarios[2])
        self.assertEqual(status, "FLAG_REVIEW")
        self.assertIn("flagged for human review", msg)

    def test_evaluation_experiment_metrics(self):
        exp = run_evaluation_experiment()
        self.assertEqual(len(exp), 3)
        self.assertIn("config_1_single", exp)
        self.assertIn("config_2_standard", exp)
        self.assertIn("config_3_extended", exp)

        for cfg_name, data in exp.items():
            # Correctness should be 100% across all configurations
            self.assertEqual(data["correctness_rate"], 1.0)
            self.assertGreater(data["avg_latency_us"], 0.0)

    def test_boundary_missing_fields(self):
        status, _ = check_scenario({})
        self.assertEqual(status, "FAIL")


if __name__ == "__main__":
    unittest.main()
