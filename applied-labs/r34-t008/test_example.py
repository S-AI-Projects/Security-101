"""
Unit tests for Task R34-T008
"""
import unittest
from example import evaluate_scenario, process_scenario_stream, get_scenarios

class TestSecOpsRecovery(unittest.TestCase):
    def setUp(self):
        self.scenarios = get_scenarios()

    def test_complete_scenario_passes(self):
        res = evaluate_scenario(self.scenarios["normal"])
        self.assertEqual(res["status"], "PASS")

    def test_missing_asset_fails(self):
        res = evaluate_scenario(self.scenarios["missing_asset"])
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(res["missing_field"], "asset")

    def test_unrelated_control_flagged(self):
        res = evaluate_scenario(self.scenarios["unrelated_control"])
        self.assertEqual(res["status"], "FLAGGED_FOR_REVIEW")

    def test_failure_and_recovery_on_next_input(self):
        """Demonstrate recovery: after invalid input fails, next valid input succeeds."""
        stream = [self.scenarios["missing_asset"], self.scenarios["normal"]]
        results = process_scenario_stream(stream)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["status"], "FAIL")
        self.assertEqual(results[1]["status"], "PASS")

if __name__ == "__main__":
    unittest.main()
