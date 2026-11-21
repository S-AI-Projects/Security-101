"""
Unit tests for Task R34-T009
"""
import unittest
from example import validate_and_redact_config, run_evaluation_experiment

class TestConfigValidator(unittest.TestCase):
    def test_valid_config_produces_redacted_summary(self):
        cfg = {
            "command": "python3",
            "args": ["-m", "http.server", "8000"],
            "env": {"DATABASE_PASSWORD": "SuperSecretPassword123"}
        }
        res = validate_and_redact_config(cfg)
        self.assertEqual(res["status"], "PASS")
        self.assertFalse(res["process_launched"])
        self.assertEqual(res["validated_configuration"]["redacted_env"]["DATABASE_PASSWORD"], "[REDACTED]")

    def test_missing_command_fails(self):
        cfg = {"command": "", "args": ["-v"]}
        res = validate_and_redact_config(cfg)
        self.assertEqual(res["status"], "FAIL")
        self.assertIn("Missing", res["error"])

    def test_string_args_fails(self):
        """single string where argument array required fails"""
        cfg = {"command": "python3", "args": "run server"}
        res = validate_and_redact_config(cfg)
        self.assertEqual(res["status"], "FAIL")
        self.assertIn("must be a list", res["error"])

    def test_evaluation_experiment(self):
        exp = run_evaluation_experiment()
        self.assertIn("small", exp)
        self.assertIn("medium", exp)
        self.assertIn("large", exp)
        for _, metrics in exp.items():
            self.assertEqual(metrics["status"], "PASS")
            self.assertFalse(metrics["process_launched"])

if __name__ == "__main__":
    unittest.main()
