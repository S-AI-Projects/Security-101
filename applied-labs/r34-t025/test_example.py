"""Regression tests for the R34-T025 IPv4 allowlist lab."""

import unittest

from example import (
    AddressAllowlist,
    CANONICAL_ADDRESS,
    DEFAULT_CIDR,
    LESSON_CITATION,
    MALFORMED_ADDRESS,
    OUTSIDE_ADDRESS,
    baseline_address_allowed,
    is_address_allowed,
    prove_fixture_equivalence,
    run_scenario,
)


class IPv4AllowlistTests(unittest.TestCase):
    def test_canonical_address_is_allowed(self):
        self.assertTrue(is_address_allowed(CANONICAL_ADDRESS, DEFAULT_CIDR))

    def test_outside_address_is_not_allowed(self):
        self.assertFalse(is_address_allowed(OUTSIDE_ADDRESS, DEFAULT_CIDR))

    def test_malformed_address_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Malformed IPv4 address"):
            is_address_allowed(MALFORMED_ADDRESS, DEFAULT_CIDR)

    def test_malformed_cidr_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Malformed CIDR"):
            is_address_allowed("192.0.2.1", "192.0.2.0/99")

    def test_network_address_is_inside(self):
        self.assertTrue(is_address_allowed("192.0.2.0"))

    def test_broadcast_address_is_inside_cidr_membership(self):
        self.assertTrue(is_address_allowed("192.0.2.255"))

    def test_first_outside_address_is_rejected(self):
        self.assertFalse(is_address_allowed("192.0.3.0"))

    def test_named_responsibility_class_contract(self):
        allowlist = AddressAllowlist(DEFAULT_CIDR)
        self.assertTrue(allowlist.contains(CANONICAL_ADDRESS))
        self.assertFalse(allowlist.contains(OUTSIDE_ADDRESS))

    def test_baseline_and_extracted_fixture_are_equivalent(self):
        fixture = [CANONICAL_ADDRESS, OUTSIDE_ADDRESS, "192.0.2.0", "192.0.2.255"]
        results, equivalent = prove_fixture_equivalence(fixture)
        for address in fixture:
            self.assertEqual(results[address], baseline_address_allowed(address))
        self.assertTrue(equivalent)

    def test_normal_scenario_exact_output(self):
        code, output = run_scenario("normal")
        expected = (
            f'Scenario: allowlist membership based on "{LESSON_CITATION}".\n'
            f"CIDR={DEFAULT_CIDR}\n"
            f"{CANONICAL_ADDRESS} allowed=true\n"
            f"{OUTSIDE_ADDRESS} allowed=false"
        )
        self.assertEqual(code, 0)
        self.assertEqual(output, expected)

    def test_boundary_scenario(self):
        code, output = run_scenario("boundary")
        self.assertEqual(code, 0)
        self.assertIn("192.0.2.0 allowed=true", output)
        self.assertIn("192.0.2.255 allowed=true", output)
        self.assertIn("192.0.3.0 allowed=false", output)

    def test_failure_scenario(self):
        code, output = run_scenario("failure")
        self.assertEqual(code, 1)
        self.assertIn("Malformed IPv4 address", output)

    def test_deliberate_wrong_result_fails(self):
        actual = is_address_allowed(CANONICAL_ADDRESS)
        with self.assertRaises(AssertionError):
            self.assertFalse(actual, "Deliberate wrong result: canonical address was asserted false")


if __name__ == "__main__":
    unittest.main()
