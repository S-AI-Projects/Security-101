"""Unit tests for infrastructure security scenario rubric checker with state trace (R34-T027)."""

import unittest

from example import (
    BOUNDARY_SCENARIOS,
    LESSON_CITATION,
    SCENARIOS,
    SCENARIO_EXPLANATIONS,
    check_scenario,
    evaluate_scenario_with_trace,
    run_scenario,
    verify_state_invariants,
)


class InfrastructureRubricTests(unittest.TestCase):
    """Test suite verifying rubric evaluation, state trace recording, and invariants."""

    def test_complete_scenario_passes(self):
        """One complete scenario passes: kubernetes-host-patching returns PASS."""
        res = check_scenario(SCENARIOS["kubernetes-host-patching"])
        self.assertEqual(res, "PASS")

    def test_missing_asset_fails(self):
        """A scenario without an asset fails: missing-asset-image-scan returns FAIL (asset is required)."""
        res = check_scenario(SCENARIOS["missing-asset-image-scan"])
        self.assertEqual(res, "FAIL (asset is required)")

    def test_mismatched_control_flagged_for_review(self):
        """A control unrelated to the named threat is flagged for review."""
        res = check_scenario(SCENARIOS["mismatched-control-registry"])
        self.assertEqual(res, "REVIEW (control needs a rationale)")

    def test_intermediate_state_trace_recorded(self):
        """Focus: Intermediate state after each step is recorded in structured trace."""
        decision, trace = evaluate_scenario_with_trace(SCENARIOS["kubernetes-host-patching"])
        self.assertEqual(decision, "PASS")
        self.assertEqual(len(trace), 3)

        # Step 1: Ingestion & Field Presence
        self.assertEqual(trace[0]["step"], 1)
        self.assertEqual(trace[0]["name"], "FIELD_PRESENCE")
        self.assertEqual(trace[0]["missing_fields"], [])
        self.assertEqual(trace[0]["status_so_far"], "VALID_FIELDS")

        # Step 2: Semantic Alignment
        self.assertEqual(trace[1]["step"], 2)
        self.assertEqual(trace[1]["name"], "CONTROL_ALIGNMENT")
        self.assertTrue(trace[1]["is_aligned"])
        self.assertEqual(trace[1]["status_so_far"], "PASS")

        # Step 3: Final Disposition
        self.assertEqual(trace[2]["step"], 3)
        self.assertEqual(trace[2]["name"], "FINAL_DISPOSITION")
        self.assertEqual(trace[2]["final_decision"], "PASS")

    def test_invariant_linking_state_to_final_output_pass(self):
        """Test the invariant linking intermediate state to PASS output."""
        decision, trace = evaluate_scenario_with_trace(SCENARIOS["kubernetes-host-patching"])
        self.assertTrue(verify_state_invariants(trace, decision))

    def test_invariant_linking_state_to_final_output_fail(self):
        """Test the invariant linking missing field state to FAIL output."""
        decision, trace = evaluate_scenario_with_trace(SCENARIOS["missing-asset-image-scan"])
        self.assertTrue(verify_state_invariants(trace, decision))
        self.assertEqual(trace[0]["missing_fields"], ["asset"])
        self.assertTrue(decision.startswith("FAIL"))

    def test_invariant_linking_state_to_final_output_review(self):
        """Test the invariant linking unaligned control state to REVIEW output."""
        decision, trace = evaluate_scenario_with_trace(SCENARIOS["mismatched-control-registry"])
        self.assertTrue(verify_state_invariants(trace, decision))
        self.assertFalse(trace[1]["is_aligned"])
        self.assertTrue(decision.startswith("REVIEW"))

    def test_boundary_scenarios_missing_or_blank_fields(self):
        """Boundary inputs with blank fields fail gracefully."""
        self.assertEqual(
            check_scenario(BOUNDARY_SCENARIOS["blank-residual-risk"]),
            "FAIL (residual_risk is required)",
        )
        self.assertEqual(
            check_scenario(BOUNDARY_SCENARIOS["blank-control"]),
            "FAIL (control is required)",
        )

    def test_scenario_citations_cite_lesson(self):
        """Scenario explanations cite 6.1 Infrastructure security key concepts.md."""
        for name, explanation in SCENARIO_EXPLANATIONS.items():
            self.assertIn(
                LESSON_CITATION,
                explanation,
                f"Scenario '{name}' does not cite {LESSON_CITATION}",
            )

    def test_normal_scenario_execution(self):
        """Normal scenario runs with exit code 0."""
        code, output = run_scenario("normal")
        self.assertEqual(code, 0)
        self.assertIn(LESSON_CITATION, output)
        self.assertIn("kubernetes-host-patching: PASS", output)
        self.assertIn("missing-asset-image-scan: FAIL", output)
        self.assertIn("mismatched-control-registry: REVIEW", output)

    def test_boundary_scenario_execution(self):
        """Boundary scenario runs with exit code 0."""
        code, output = run_scenario("boundary")
        self.assertEqual(code, 0)
        self.assertIn(LESSON_CITATION, output)
        self.assertIn("blank-residual-risk: FAIL", output)

    def test_failure_scenario_execution(self):
        """Failure scenario runs with exit code 1 on non-dict input."""
        code, output = run_scenario("failure")
        self.assertEqual(code, 1)
        self.assertIn("Error:", output)
        self.assertIn("Scenario answer must be a dict", output)

    def test_deliberate_wrong_result_fails(self):
        """Deliberate wrong result assertion fails with AssertionError."""
        actual = check_scenario(SCENARIOS["mismatched-control-registry"])
        # Intentionally wrong expectation (expecting PASS on mismatched scenario)
        with self.assertRaises(AssertionError):
            self.assertEqual(actual, "PASS", "Deliberate wrong result check")


if __name__ == "__main__":
    unittest.main()
