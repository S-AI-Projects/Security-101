import unittest

from example import SCENARIOS, check_scenario


class ScenarioRubricTests(unittest.TestCase):
    def test_smallest_valid_scenario_passes(self):
        self.assertEqual(check_scenario(SCENARIOS["smallest-valid"]), "PASS")

    def test_complete_scenario_with_unrelated_control_needs_review(self):
        scenario = SCENARIOS["review-boundary"]
        self.assertEqual(
            check_scenario(scenario),
            "REVIEW (threat and control do not match the rubric)",
        )
        self.assertEqual(
            check_scenario({**scenario, "control": "restrict public access"}), "PASS"
        )

    def test_missing_asset_fails(self):
        self.assertEqual(
            check_scenario(SCENARIOS["missing-asset"]),
            "FAIL (asset must be non-blank text)",
        )

    def test_blank_or_non_text_values_fail_in_each_required_field(self):
        for field in SCENARIOS["smallest-valid"]:
            for value in (" \t", None, 0):
                with self.subTest(field=field, value=value):
                    scenario = {**SCENARIOS["smallest-valid"], field: value}
                    self.assertEqual(
                        check_scenario(scenario), f"FAIL ({field} must be non-blank text)"
                    )

    def test_pair_matching_ignores_surrounding_whitespace(self):
        scenario = {
            **SCENARIOS["smallest-valid"],
            "threat": " exploit unpatched service ",
            "control": " apply security patch ",
        }
        self.assertEqual(check_scenario(scenario), "PASS")
