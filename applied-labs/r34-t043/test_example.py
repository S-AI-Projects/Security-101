"""Unit tests for CIA triad scenario classification and approach comparison."""

import unittest

from example import (
    AVAILABILITY,
    CONFIDENTIALITY,
    INTEGRITY,
    SCENARIOS,
    classify_direct,
    classify_reference,
    compare_approaches,
    run_all_scenarios,
)


class CIAScenarioClassificationTests(unittest.TestCase):
    def test_unauthorized_reading_yields_confidentiality(self):
        scenario = SCENARIOS["unauthorized-reading"]
        impacts = classify_direct(scenario)
        self.assertEqual(impacts, {CONFIDENTIALITY})
        self.assertNotIn(INTEGRITY, impacts)
        self.assertNotIn(AVAILABILITY, impacts)

    def test_altered_records_yields_integrity(self):
        scenario = SCENARIOS["altered-records"]
        impacts = classify_direct(scenario)
        self.assertEqual(impacts, {INTEGRITY})
        self.assertNotIn(CONFIDENTIALITY, impacts)
        self.assertNotIn(AVAILABILITY, impacts)

    def test_unavailable_service_yields_availability(self):
        scenario = SCENARIOS["unavailable-service"]
        impacts = classify_direct(scenario)
        self.assertEqual(impacts, {AVAILABILITY})
        self.assertNotIn(CONFIDENTIALITY, impacts)
        self.assertNotIn(INTEGRITY, impacts)

    def test_multi_impact_scenarios_retain_all_applicable_labels(self):
        # Scenario 1: Confidentiality + Integrity
        ci_scenario = SCENARIOS["multi-confidentiality-integrity"]
        ci_impacts = classify_direct(ci_scenario)
        self.assertEqual(ci_impacts, {CONFIDENTIALITY, INTEGRITY})

        # Scenario 2: Integrity + Availability
        ia_scenario = SCENARIOS["multi-integrity-availability"]
        ia_impacts = classify_direct(ia_scenario)
        self.assertEqual(ia_impacts, {INTEGRITY, AVAILABILITY})

        # Scenario 3: All three triad properties
        all_scenario = SCENARIOS["multi-all-triad"]
        all_impacts = classify_direct(all_scenario)
        self.assertEqual(all_impacts, {CONFIDENTIALITY, INTEGRITY, AVAILABILITY})

    def test_both_approaches_agree_across_all_fixtures(self):
        reports = run_all_scenarios()
        self.assertGreater(len(reports), 0)
        for report in reports:
            with self.subTest(scenario=report["scenario"]):
                self.assertTrue(report["agreed"])
                self.assertEqual(report["direct_impacts"], report["reference_impacts"])

    def test_benign_activity_yields_empty_set(self):
        scenario = SCENARIOS["benign-activity"]
        impacts = classify_direct(scenario)
        self.assertEqual(impacts, set())

    def test_case_and_whitespace_insensitivity(self):
        custom_scenario = {"events": ["  Unauthorized Reading  ", "\tAltered Records\n"]}
        impacts = classify_direct(custom_scenario)
        self.assertEqual(impacts, {CONFIDENTIALITY, INTEGRITY})

    def test_unknown_event_indicator_is_ignored(self):
        custom_scenario = {"events": ["unrelated audit note", "routine ping"]}
        impacts = classify_direct(custom_scenario)
        self.assertEqual(impacts, set())

    def test_comparison_detects_deliberate_divergence(self):
        scenario = {"events": ["unauthorized reading"]}
        direct_result = classify_direct(scenario)
        # Deliberately compare against a wrong expected label set
        wrong_reference = {INTEGRITY}
        self.assertNotEqual(direct_result, wrong_reference)


if __name__ == "__main__":
    unittest.main()
