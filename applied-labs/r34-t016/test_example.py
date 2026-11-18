import subprocess
import unittest
from pathlib import Path

from example import is_allowlisted


ROOT = Path(__file__).resolve().parents[2]


class TestCIDRAllowlist(unittest.TestCase):
    def test_address_inside_allowlisted_network(self):
        self.assertTrue(is_allowlisted("192.0.2.1"))

    def test_address_outside_allowlisted_network(self):
        self.assertFalse(is_allowlisted("198.51.100.1"))

    def test_malformed_address_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid IP address 'not-an-ip'"):
            is_allowlisted("not-an-ip")

    def test_documented_example_command_output(self):
        result = subprocess.run(
            ["python3", "./applied-labs/r34-t016/example.py"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout,
            "\n".join(
                (
                    "Scenario: normal (local fixture; no network traffic)",
                    "Allowlist: 192.0.2.0/24",
                    "Input address: 192.0.2.1",
                    "Allowlisted: yes",
                    "",
                )
            ),
        )
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
