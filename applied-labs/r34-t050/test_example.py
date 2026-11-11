import unittest

from example import SCENARIOS, check_scenario


class RubricTests(unittest.TestCase):
    def test_complete_stolen_password_answer_passes(self):
        self.assertEqual(check_scenario(SCENARIOS["stolen-password"]), "PASS")

    def test_missing_or_blank_asset_fails(self):
        for answer in (SCENARIOS["missing-asset"], dict(SCENARIOS["stolen-password"], asset=" ")):
            with self.subTest(answer=answer):
                self.assertEqual(check_scenario(answer), "FAIL (provide asset)")

    def test_authentication_control_does_not_remove_an_old_role(self):
        answer = SCENARIOS["stale-access"]
        self.assertEqual(check_scenario(answer), "REVIEW (control does not match the threat)")
        corrected = dict(answer, control="remove stale role assignments",
                         residual_risk="A separate account might still have access.")
        self.assertEqual(check_scenario(corrected), "PASS")
