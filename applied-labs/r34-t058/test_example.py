"""Unit tests for Network Range Classification and Recovery (R34-T058)."""

import unittest
from example import classify_ip, process_ip_sequence


class TestNetworkRangeClassification(unittest.TestCase):
    def setUp(self):
        self.network = "192.0.2.0/24"

    def test_allowlisted_member(self):
        res = classify_ip("192.0.2.1", self.network)
        self.assertEqual(res["status"], "ALLOW")
        self.assertTrue(res["is_member"])
        self.assertEqual(res["ip"], "192.0.2.1")

    def test_non_member_denied(self):
        res = classify_ip("198.51.100.1", self.network)
        self.assertEqual(res["status"], "DENY")
        self.assertFalse(res["is_member"])

    def test_malformed_ip_error(self):
        res = classify_ip("999.999.999.999", self.network)
        self.assertEqual(res["status"], "ERROR")
        self.assertEqual(res["error_type"], "MALFORMED_IP")
        self.assertIn("Malformed IP address", res["message"])

    def test_missing_empty_ip_error(self):
        res = classify_ip("", self.network)
        self.assertEqual(res["status"], "ERROR")
        self.assertEqual(res["error_type"], "MISSING_DATA")

        res_none = classify_ip(None, self.network)
        self.assertEqual(res_none["status"], "ERROR")
        self.assertEqual(res_none["error_type"], "MISSING_DATA")

    def test_sequence_error_recovery(self):
        seq = ["192.0.2.1", "invalid_junk", "192.0.2.100"]
        results = process_ip_sequence(seq, self.network)
        self.assertEqual(results[0]["status"], "ALLOW")
        self.assertEqual(results[1]["status"], "ERROR")
        # Ensure third element recovers gracefully
        self.assertEqual(results[2]["status"], "ALLOW")
        self.assertEqual(results[2]["ip"], "192.0.2.100")

    def test_subnet_boundary_cases(self):
        # Network ID and broadcast address
        res_net = classify_ip("192.0.2.0", self.network)
        self.assertEqual(res_net["status"], "ALLOW")
        res_bcast = classify_ip("192.0.2.255", self.network)
        self.assertEqual(res_bcast["status"], "ALLOW")
        # Next adjacent subnet
        res_next = classify_ip("192.0.3.0", self.network)
        self.assertEqual(res_next["status"], "DENY")


if __name__ == "__main__":
    unittest.main()
