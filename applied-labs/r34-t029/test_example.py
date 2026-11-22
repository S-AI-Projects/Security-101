"""Unit tests for IAM access policy evaluator and configuration comparison (R34-T029)."""

import unittest

from example import (
    CONFIG_COMPREHENSIVE,
    CONFIG_MINIMAL,
    CONFIG_STANDARD,
    CONTROLLED_CONFIGS,
    FAILURE_POLICY_FIXTURE,
    LESSON_CITATION,
    SCENARIO_EXPLANATIONS,
    STANDARD_POLICY_MATRIX,
    compare_configurations,
    evaluate_access,
    run_scenario,
    validate_policies,
)


class IAMPolicyEvaluatorTests(unittest.TestCase):
    """Test suite verifying IAM policy evaluation contract and configuration comparison."""

    def test_reader_may_read_public(self):
        """reader may read public: evaluates to ALLOW."""
        res = evaluate_access("reader", "read", "public")
        self.assertEqual(res["decision"], "ALLOW")
        self.assertIn("Permission granted", res["reason"])

    def test_reader_cannot_write_public(self):
        """reader cannot write: evaluates to DENY."""
        res = evaluate_access("reader", "write", "public")
        self.assertEqual(res["decision"], "DENY")
        self.assertIn("Explicit DENY", res["reason"])

    def test_explicit_deny_overrides_matching_allow(self):
        """An explicit deny overrides a matching allow: evaluates to DENY."""
        # 'auditor' has both ALLOW and DENY rules for 'audit' on 'logs'
        res = evaluate_access("auditor", "audit", "logs")
        self.assertEqual(res["decision"], "DENY")
        self.assertIn("Explicit DENY overrides matching ALLOW", res["reason"])

    def test_unknown_role_is_denied(self):
        """An unknown role is denied under default-deny: evaluates to DENY."""
        res = evaluate_access("stranger", "read", "public")
        self.assertEqual(res["decision"], "DENY")
        self.assertIn("unknown or not recognized", res["reason"])

        res2 = evaluate_access("hacker", "write", "public")
        self.assertEqual(res2["decision"], "DENY")

    def test_unspecified_action_default_deny(self):
        """Unlisted actions for a known role evaluate to DENY under default-deny."""
        res = evaluate_access("reader", "delete", "public")
        self.assertEqual(res["decision"], "DENY")
        self.assertIn("default deny", res["reason"])

    def test_unspecified_resource_default_deny(self):
        """Unlisted resources evaluate to DENY under default-deny."""
        res = evaluate_access("reader", "read", "classified")
        self.assertEqual(res["decision"], "DENY")
        self.assertIn("default deny", res["reason"])

    def test_empty_or_blank_attributes_denied(self):
        """Empty, whitespace, or missing request attributes evaluate to DENY."""
        res1 = evaluate_access("", "read", "public")
        self.assertEqual(res1["decision"], "DENY")

        res2 = evaluate_access("reader", "   ", "public")
        self.assertEqual(res2["decision"], "DENY")

        res3 = evaluate_access("reader", "read", "")
        self.assertEqual(res3["decision"], "DENY")

    def test_scenario_citations_cite_lesson(self):
        """All scenario explanation headers must cite 2.3 IAM capabilities.md."""
        for name, explanation in SCENARIO_EXPLANATIONS.items():
            self.assertIn(
                LESSON_CITATION,
                explanation,
                f"Scenario '{name}' does not cite {LESSON_CITATION}",
            )

    def test_normal_scenario_execution(self):
        """Normal scenario runs with code 0 and formats decisions."""
        code, output = run_scenario("normal")
        self.assertEqual(code, 0)
        self.assertIn(LESSON_CITATION, output)
        self.assertIn("reader | read | public | ALLOW", output)
        self.assertIn("reader | write | public | DENY", output)
        self.assertIn("auditor | audit | logs | DENY", output)
        self.assertIn("stranger | read | public | DENY", output)

    def test_boundary_scenario_execution(self):
        """Boundary scenario runs with code 0 and evaluates edge requests."""
        code, output = run_scenario("boundary")
        self.assertEqual(code, 0)
        self.assertIn(LESSON_CITATION, output)
        self.assertIn("reader | read | private | DENY", output)
        self.assertIn("auditor | delete | logs | DENY", output)

    def test_failure_scenario_execution(self):
        """Failure scenario runs with code 1 and outputs error for invalid policy effect."""
        code, output = run_scenario("failure")
        self.assertEqual(code, 1)
        self.assertIn("Error:", output)
        self.assertIn("Invalid policy effect 'PERMIT'", output)

    def test_invalid_policy_effect_raises_value_error(self):
        """validate_policies raises ValueError on invalid effect."""
        bad_policy = [{"role": "user", "action": "read", "resource": "file", "effect": "GRANT"}]
        with self.assertRaises(ValueError) as ctx:
            validate_policies(bad_policy)
        self.assertIn("Invalid policy effect 'GRANT'", str(ctx.exception))

    def test_missing_policy_field_raises_value_error(self):
        """validate_policies raises ValueError on missing fields."""
        incomplete = [{"role": "user", "action": "read", "resource": ""}]
        with self.assertRaises(ValueError):
            validate_policies(incomplete)

    def test_configuration_comparison_trade_off(self):
        """Compare three controlled configurations: verify 100% correctness and linear check scaling."""
        results = compare_configurations()
        self.assertEqual(len(results), 3)

        # All configurations maintain 100% policy contract correctness
        for r in results:
            self.assertEqual(r["correctness_rate"], 100.0)
            self.assertEqual(r["requests_count"], 4)

        # Rule checks scale linearly with rule count (3 -> 6 -> 12)
        min_res, std_res, comp_res = results[0], results[1], results[2]
        self.assertEqual(min_res["rules_count"], 3)
        self.assertEqual(std_res["rules_count"], 6)
        self.assertEqual(comp_res["rules_count"], 12)

        self.assertLess(min_res["total_checks"], std_res["total_checks"])
        self.assertLess(std_res["total_checks"], comp_res["total_checks"])
        self.assertEqual(min_res["total_checks"], 12)
        self.assertEqual(std_res["total_checks"], 24)
        self.assertEqual(comp_res["total_checks"], 48)

    def test_deliberate_wrong_result_fails(self):
        """A deliberate wrong result assertion fails with AssertionError."""
        res = evaluate_access("reader", "write", "public")
        # Intentionally wrong expectation (expecting ALLOW for reader write)
        with self.assertRaises(AssertionError):
            self.assertEqual(res["decision"], "ALLOW", "Deliberate wrong result check")


if __name__ == "__main__":
    unittest.main()
