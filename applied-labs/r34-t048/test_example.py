import unittest

from example import SCENARIOS, check_scenario


class AssessmentTests(unittest.TestCase):
    def test_predict_the_guest_segment_result(self):
        self.assertEqual(check_scenario(SCENARIOS["guest-segment"]), "PASS")

    def test_diagnose_and_repair_missing_asset(self):
        answer = SCENARIOS["missing-asset"]
        self.assertEqual(check_scenario(answer), "FAIL (asset is required)")
        self.assertEqual(check_scenario(dict(answer, asset="Inventory app traffic")), "PASS")

    def test_route_complete_control_mismatch_to_review(self):
        answer = SCENARIOS["mismatched-control"]
        self.assertEqual(check_scenario(answer), "REVIEW (control needs a rationale)")
        self.assertEqual(check_scenario(dict(answer, control="use end-to-end encryption")),
                         "PASS")

    def test_blank_field_is_still_incomplete(self):
        answer = dict(SCENARIOS["guest-segment"], residual_risk="   ")
        self.assertEqual(check_scenario(answer), "FAIL (residual_risk is required)")
