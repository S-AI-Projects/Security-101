# R34-T043 check evidence

Tools used are Python 3.14.6, its bundled `unittest` module, and 2.56.0 of Git. Each command ran in a fresh Python process.

## Fixture inputs

```json
{
  "unauthorized-reading": {
    "title": "Exposure of customer records",
    "events": ["unauthorized reading"],
    "expected": ["confidentiality"]
  },
  "altered-records": {
    "title": "Modification of financial transaction database",
    "events": ["altered records"],
    "expected": ["integrity"]
  },
  "unavailable-service": {
    "title": "Distributed network flood causing portal downtime",
    "events": ["unavailable service"],
    "expected": ["availability"]
  },
  "multi-confidentiality-integrity": {
    "title": "Attacker exfiltrates patient history and modifies prescription records",
    "events": ["unauthorized reading", "altered records"],
    "expected": ["confidentiality", "integrity"]
  },
  "multi-integrity-availability": {
    "title": "Ransomware corrupts critical configuration files and halts billing service",
    "events": ["file corruption", "system outage"],
    "expected": ["availability", "integrity"]
  },
  "multi-all-triad": {
    "title": "Total compromise: data breach, database tampering, and server shutdown",
    "events": ["data exfiltration", "altered records", "unavailable service"],
    "expected": ["availability", "confidentiality", "integrity"]
  },
  "benign-activity": {
    "title": "Scheduled maintenance and routine audit read",
    "events": [],
    "expected": []
  }
}
```

## Scenario run

```sh
python3 applied-labs/r34-t043/example.py
```

Expected output:

```text
unauthorized-reading: direct=confidentiality, reference=confidentiality, match=AGREED
altered-records: direct=integrity, reference=integrity, match=AGREED
unavailable-service: direct=availability, reference=availability, match=AGREED
multi-confidentiality-integrity: direct=confidentiality,integrity, reference=confidentiality,integrity, match=AGREED
multi-integrity-availability: direct=availability,integrity, reference=availability,integrity, match=AGREED
multi-all-triad: direct=availability,confidentiality,integrity, reference=availability,confidentiality,integrity, match=AGREED
benign-activity: direct=none, reference=none, match=AGREED
```

Actual output (exit code 0):

```text
unauthorized-reading: direct=confidentiality, reference=confidentiality, match=AGREED
altered-records: direct=integrity, reference=integrity, match=AGREED
unavailable-service: direct=availability, reference=availability, match=AGREED
multi-confidentiality-integrity: direct=confidentiality,integrity, reference=confidentiality,integrity, match=AGREED
multi-integrity-availability: direct=availability,integrity, reference=availability,integrity, match=AGREED
multi-all-triad: direct=availability,confidentiality,integrity, reference=availability,confidentiality,integrity, match=AGREED
benign-activity: direct=none, reference=none, match=AGREED
```

The commands and expected outputs in `1.1 The CIA triad and other key concepts.md` and the lab guide match this run.

## Automated check

```sh
python3 -m unittest discover -s ./applied-labs/r34-t043 -p "test_*.py"
```

Expected 9 passing tests and exit code 0. Actual output (exit code 0):

```text
.........
----------------------------------------------------------------------
Ran 9 tests in 0.000s

OK
```

The test suite validates:
1. `unauthorized reading` classifies strictly as `confidentiality`.
2. `altered records` classifies strictly as `integrity`.
3. `unavailable service` classifies strictly as `availability`.
4. Multi-impact scenarios preserve all applicable labels without loss.
5. Direct indicator classification and independent reference lookup agree across all fixtures.
6. Empty scenario yields an empty set.
7. Whitespace trimming and case insensitivity are enforced.
8. Comparison logic correctly detects divergence when direct and reference results disagree.

## Deliberate failure

In a temporary directory copy of `applied-labs/r34-t043/`, change the `classify_direct` return value to `return set()`. Run the automated check command in that directory.

Expected 9 tests, 11 failures (including subtests), and non-zero exit code (exit 1). Actual result (exit code 1):

```text
F.FFFFFFF.FFF.
======================================================================
FAIL: test_altered_records_yields_integrity (test_example.CIAScenarioClassificationTests.test_altered_records_yields_integrity)
----------------------------------------------------------------------
Traceback (most recent call last):
  File ".../test_example.py", line 28, in test_altered_records_yields_integrity
    self.assertEqual(impacts, {INTEGRITY})
AssertionError: Items in the second set but not the first:
'integrity'

======================================================================
FAIL: test_both_approaches_agree_across_all_fixtures (test_example.CIAScenarioClassificationTests.test_both_approaches_agree_across_all_fixtures) (scenario='unauthorized-reading')
----------------------------------------------------------------------
Traceback (most recent call last):
  File ".../test_example.py", line 60, in test_both_approaches_agree_across_all_fixtures
    self.assertTrue(report["agreed"])
AssertionError: False is not true

======================================================================
FAIL: test_multi_impact_scenarios_retain_all_applicable_labels (test_example.CIAScenarioClassificationTests.test_multi_impact_scenarios_retain_all_applicable_labels)
----------------------------------------------------------------------
Traceback (most recent call last):
  File ".../test_example.py", line 43, in test_multi_impact_scenarios_retain_all_applicable_labels
    self.assertEqual(ci_impacts, {CONFIDENTIALITY, INTEGRITY})
AssertionError: Items in the second set but not the first:
'confidentiality'
'integrity'

======================================================================
FAIL: test_unauthorized_reading_yields_confidentiality (test_example.CIAScenarioClassificationTests.test_unauthorized_reading_yields_confidentiality)
----------------------------------------------------------------------
Traceback (most recent call last):
  File ".../test_example.py", line 21, in test_unauthorized_reading_yields_confidentiality
    self.assertEqual(impacts, {CONFIDENTIALITY})
AssertionError: Items in the second set but not the first:
'confidentiality'

======================================================================
FAIL: test_unavailable_service_yields_availability (test_example.CIAScenarioClassificationTests.test_unavailable_service_yields_availability)
----------------------------------------------------------------------
Traceback (most recent call last):
  File ".../test_example.py", line 35, in test_unavailable_service_yields_availability
    self.assertEqual(impacts, {AVAILABILITY})
AssertionError: Items in the second set but not the first:
'availability'

----------------------------------------------------------------------
Ran 9 tests in 0.001s

FAILED (failures=11)
```
