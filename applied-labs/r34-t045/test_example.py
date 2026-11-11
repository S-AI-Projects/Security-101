import unittest
from unittest.mock import Mock

from example import SCENARIOS, check_scenario, lookup_local_control


class RubricTests(unittest.TestCase):
    def test_public_access_control_passes(self):
        self.assertEqual(check_scenario(SCENARIOS["public-store"], lookup_local_control), "PASS")

    def test_missing_asset_skips_the_lookup(self):
        lookup = Mock()
        self.assertEqual(check_scenario(SCENARIOS["missing-asset"], lookup),
                         "FAIL (missing or invalid asset)")
        lookup.assert_not_called()

    def test_unrelated_control_requires_review(self):
        self.assertEqual(check_scenario(SCENARIOS["wrong-control"], lookup_local_control),
                         "REVIEW (no matching control)")

    def test_unknown_threat_requires_review(self):
        answer = dict(SCENARIOS["public-store"], threat="stolen administrator credentials")
        self.assertEqual(check_scenario(answer, lookup_local_control),
                         "REVIEW (no matching control)")

    def test_adapter_receives_the_named_threat(self):
        lookup = Mock(return_value="block public reads")
        self.assertEqual(check_scenario(SCENARIOS["public-store"], lookup), "PASS")
        lookup.assert_called_once_with("public read access")
