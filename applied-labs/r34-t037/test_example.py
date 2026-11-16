import unittest
from example import check_scenario


class TestRiskChecker(unittest.TestCase):
    def test_complete_scenario_passes(self):
        result = check_scenario({
            "id": "test",
            "asset": "Customer records",
            "threat": "Phishing",
            "control": "Multi-factor authentication",
            "residual_risk": "Some users may still be deceived."
        })
        self.assertEqual(result["status"], "PASS")

    def test_missing_asset_fails(self):
        result = check_scenario({
            "id": "test",
            "asset": "",
            "threat": "Phishing",
            "control": "Multi-factor authentication",
            "residual_risk": "Some risk remains."
        })
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("asset", result["message"])

    def test_unrelated_control_needs_review(self):
        result = check_scenario({
            "id": "test",
            "asset": "Network",
            "threat": "Ransomware",
            "control": "Security awareness posters",
            "residual_risk": "Some risk remains."
        })
        self.assertEqual(result["status"], "REVIEW")

    def test_empty_residual_risk_fails(self):
        result = check_scenario({
            "id": "test",
            "asset": "Network",
            "threat": "Ransomware",
            "control": "Offline backups",
            "residual_risk": ""
        })
        self.assertEqual(result["status"], "FAIL")

    def test_unknown_threat_is_not_automatically_rejected(self):
        result = check_scenario({
            "id": "test",
            "asset": "Office computers",
            "threat": "Power failure",
            "control": "Generator maintenance",
            "residual_risk": "A prolonged outage remains possible."
        })
        self.assertEqual(result["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
