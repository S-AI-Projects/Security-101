import unittest
from example import classify

class TestCIAClassification(unittest.TestCase):
    def test_confidentiality(self):
        self.assertEqual(classify({"unauthorized_reading": True}), ["confidentiality"])

    def test_integrity(self):
        self.assertEqual(classify({"altered_records": True}), ["integrity"])

    def test_availability(self):
        self.assertEqual(classify({"service_unavailable": True}), ["availability"])

    def test_multiple_impacts(self):
        self.assertEqual(
            classify({"unauthorized_reading": True, "altered_records": True, "service_unavailable": True}),
            ["confidentiality", "integrity", "availability"]
        )

    def test_no_impact(self):
        self.assertEqual(classify({}), [])

if __name__ == "__main__":
    unittest.main()
