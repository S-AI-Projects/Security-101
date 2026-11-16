import unittest
from example import classify_address


class TestAddressClassifier(unittest.TestCase):

    def test_allowlisted_address(self):
        result = classify_address("192.0.2.1")
        self.assertEqual(result["status"], "ALLOWED")

    def test_address_outside_allowlist(self):
        result = classify_address("198.51.100.1")
        self.assertEqual(result["status"], "DENIED")

    def test_malformed_address(self):
        result = classify_address("192.0.2.999")
        self.assertEqual(result["status"], "REJECTED")

    def test_boundary_address(self):
        result = classify_address("192.0.2.255")
        self.assertEqual(result["status"], "ALLOWED")


if __name__ == "__main__":
    unittest.main()
