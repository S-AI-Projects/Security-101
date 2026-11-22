"""Unit tests for offline network range classification and error recovery (R34-T028)."""

import unittest

from example import (
    BOUNDARY_SAMPLES,
    DEFAULT_ALLOWLIST_CIDR,
    FAILURE_CIDR_FIXTURE,
    LESSON_CITATION,
    NORMAL_SAMPLES,
    SCENARIO_EXPLANATIONS,
    classify_address,
    classify_sequence,
    run_scenario,
)


class NetworkClassificationTests(unittest.TestCase):
    """Test suite verifying CIDR containment contract and error recovery behavior."""

    def test_in_network_member_belongs(self):
        """192.0.2.1 belongs to 192.0.2.0/24: evaluates to ALLOW and is_member=True."""
        res = classify_address("192.0.2.1", DEFAULT_ALLOWLIST_CIDR)
        self.assertEqual(res["status"], "ALLOW")
        self.assertTrue(res["is_member"])
        self.assertIsNone(res["error_type"])
        self.assertIn("belongs to allowlisted network", res["message"])

    def test_out_of_network_non_member(self):
        """198.51.100.1 does not belong to 192.0.2.0/24: evaluates to DENY and is_member=False."""
        res = classify_address("198.51.100.1", DEFAULT_ALLOWLIST_CIDR)
        self.assertEqual(res["status"], "DENY")
        self.assertFalse(res["is_member"])
        self.assertIsNone(res["error_type"])
        self.assertIn("does not belong to allowlisted network", res["message"])

    def test_malformed_ip_rejected(self):
        """Malformed IP strings are rejected with structured MALFORMED_IP error."""
        for malformed in ("invalid-ip-string", "999.999.999.999", "192.0.2.300", "1.2.3.4.5"):
            res = classify_address(malformed, DEFAULT_ALLOWLIST_CIDR)
            self.assertEqual(res["status"], "ERROR")
            self.assertIsNone(res["is_member"])
            self.assertEqual(res["error_type"], "MALFORMED_IP")
            self.assertIn("Malformed input", res["message"])

    def test_missing_data_rejected(self):
        """Empty strings, whitespace, or None are rejected with MISSING_DATA error."""
        for empty_val in ("", "   ", None):
            res = classify_address(empty_val, DEFAULT_ALLOWLIST_CIDR)
            self.assertEqual(res["status"], "ERROR")
            self.assertIsNone(res["is_member"])
            self.assertEqual(res["error_type"], "MISSING_DATA")
            self.assertIn("Missing data", res["message"])

    def test_error_explanation_and_recovery(self):
        """Exercise invalid/missing data, verify error explanation, and prove recovery on next valid input."""
        sequence = ["invalid-syntax-ip", "", "192.0.2.42"]
        results = classify_sequence(sequence, DEFAULT_ALLOWLIST_CIDR)

        # Step 1: Malformed input generates explanation
        self.assertEqual(results[0]["status"], "ERROR")
        self.assertEqual(results[0]["error_type"], "MALFORMED_IP")
        self.assertIn("Malformed input", results[0]["message"])

        # Step 2: Missing data generates explanation
        self.assertEqual(results[1]["status"], "ERROR")
        self.assertEqual(results[1]["error_type"], "MISSING_DATA")
        self.assertIn("Missing data", results[1]["message"])

        # Step 3: Demonstrates recovery on subsequent valid input without state corruption
        self.assertEqual(results[2]["status"], "ALLOW")
        self.assertTrue(results[2]["is_member"])
        self.assertIsNone(results[2]["error_type"])

    def test_network_boundary_addresses(self):
        """Network address and broadcast address evaluate to ALLOW; adjacent subnet to DENY."""
        res_net = classify_address("192.0.2.0", DEFAULT_ALLOWLIST_CIDR)
        self.assertEqual(res_net["status"], "ALLOW")
        self.assertTrue(res_net["is_member"])

        res_bcast = classify_address("192.0.2.255", DEFAULT_ALLOWLIST_CIDR)
        self.assertEqual(res_bcast["status"], "ALLOW")
        self.assertTrue(res_bcast["is_member"])

        res_adjacent = classify_address("192.0.3.1", DEFAULT_ALLOWLIST_CIDR)
        self.assertEqual(res_adjacent["status"], "DENY")
        self.assertFalse(res_adjacent["is_member"])

    def test_scenario_citations_cite_lesson(self):
        """Scenario explanations must cite 3.3 Network security capabilities.md."""
        for name, explanation in SCENARIO_EXPLANATIONS.items():
            self.assertIn(
                LESSON_CITATION,
                explanation,
                f"Scenario '{name}' does not cite {LESSON_CITATION}",
            )

    def test_normal_scenario_execution(self):
        """Normal scenario runs with code 0 and contains allow, deny, error, and recovery."""
        code, output = run_scenario("normal")
        self.assertEqual(code, 0)
        self.assertIn(LESSON_CITATION, output)
        self.assertIn("[ALLOW] IP: 192.0.2.1", output)
        self.assertIn("[DENY]  IP: 198.51.100.1", output)
        self.assertIn("MALFORMED_IP", output)
        self.assertIn("MISSING_DATA", output)
        self.assertIn("Recovery:", output)

    def test_boundary_scenario_execution(self):
        """Boundary scenario runs with code 0."""
        code, output = run_scenario("boundary")
        self.assertEqual(code, 0)
        self.assertIn(LESSON_CITATION, output)
        self.assertIn("[ALLOW] IP: 192.0.2.0", output)
        self.assertIn("[ALLOW] IP: 192.0.2.255", output)
        self.assertIn("[DENY]  IP: 192.0.3.1", output)

    def test_failure_scenario_execution(self):
        """Failure scenario runs with code 1 and outputs error for invalid network CIDR."""
        code, output = run_scenario("failure")
        self.assertEqual(code, 1)
        self.assertIn("Error:", output)
        self.assertIn("Invalid network CIDR", output)

    def test_invalid_cidr_raises_value_error(self):
        """Invalid network CIDR definition raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            classify_address("192.0.2.1", network_cidr=FAILURE_CIDR_FIXTURE)
        self.assertIn("Invalid network CIDR", str(ctx.exception))

    def test_deliberate_wrong_result_fails(self):
        """A deliberate wrong result assertion fails with AssertionError."""
        res = classify_address("198.51.100.1", DEFAULT_ALLOWLIST_CIDR)
        # Intentionally wrong expectation (expecting ALLOW for non-member)
        with self.assertRaises(AssertionError):
            self.assertEqual(res["status"], "ALLOW", "Deliberate wrong result check")


if __name__ == "__main__":
    unittest.main()
