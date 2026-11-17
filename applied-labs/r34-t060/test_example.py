"""Unit tests and dual-approach comparison checks for Network Rubric (R34-T060)."""

import unittest
from example import (
    check_scenario_direct,
    check_scenario_independent,
    compare_approaches,
    get_canonical_scenarios,
)


class TestNetworkRubricComparison(unittest.TestCase):
    def setUp(self):
        self.scenarios = get_canonical_scenarios()

    def test_complete_scenario_passes_direct(self):
        status, msg = check_scenario_direct(self.scenarios[0])
        self.assertEqual(status, "PASS")

    def test_missing_asset_fails_direct(self):
        status, msg = check_scenario_direct(self.scenarios[1])
        self.assertEqual(status, "FAIL")
        self.assertIn("asset", msg.lower())

    def test_mismatched_control_flagged_for_review_direct(self):
        status, msg = check_scenario_direct(self.scenarios[2])
        self.assertEqual(status, "FLAG_REVIEW")
        self.assertIn("flagged for human review", msg)

    def test_both_approaches_agree_identically(self):
        comp = compare_approaches(self.scenarios)
        self.assertEqual(len(comp), 3)
        for item in comp:
            self.assertTrue(item["matches"])
            self.assertEqual(item["direct_status"], item["independent_status"])

    def test_boundary_empty_scenario(self):
        self.assertEqual(check_scenario_direct({})[0], "FAIL")
        self.assertEqual(check_scenario_independent({})[0], "FAIL")


if __name__ == "__main__":
    unittest.main()
