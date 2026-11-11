import unittest

from example import SCENARIOS, check_scenario


class RubricTests(unittest.TestCase):
    def test_missing_asset_and_next_valid_input(self):
        invalid = SCENARIOS["missing-asset"]
        self.assertEqual(check_scenario(invalid), "FAIL (provide asset)")
        corrected = dict(invalid, asset="Catalog search database")
        self.assertEqual(corrected, SCENARIOS["corrected"])
        self.assertEqual(check_scenario(corrected), "PASS")
        self.assertNotIn("asset", invalid)

    def test_whitespace_only_asset_fails(self):
        answer = dict(SCENARIOS["corrected"], asset=" \t")
        self.assertEqual(check_scenario(answer), "FAIL (provide asset)")

    def test_unrelated_control_requires_review(self):
        self.assertEqual(check_scenario(SCENARIOS["unrelated-control"]),
                         "REVIEW (check threat and control)")

    def test_each_required_field_can_be_reported(self):
        for field in ("threat", "control", "residual_risk"):
            with self.subTest(field=field):
                answer = SCENARIOS["corrected"].copy()
                del answer[field]
                self.assertEqual(check_scenario(answer), f"FAIL (provide {field})")
