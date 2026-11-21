# Infrastructure Security Scenario Rubric Checker (R34-T001)

This applied lab extends **6.3 End of module quiz** by providing a local, deterministic evaluation rubric for infrastructure security risk assessments.

## Lesson Connection
In Module 6 (*Infrastructure Security*), securing IT infrastructure requires identifying assets (servers, clusters, cloud VMs), threats (unpatched CVEs, runtime escapes), controls (vulnerability scanning, patch management), and acknowledging residual risk.

This lab provides an automated structural rubric checker that verifies:
1. All four components (`asset`, `threat`, `control`, `residual_risk`) are defined.
2. Controls logically address cybersecurity infrastructure threats rather than unrelated measures (e.g. physical building turnstiles for network buffer overflows).

## Scope and Limitations
- **Scope**: Structural validation and basic threat-control correlation using deterministic keyword heuristics.
- **Limitations**: Automated grading cannot replace qualitative human judgment regarding control effectiveness or the nuances of residual risk.

## Invocation and Examples
```bash
# Evaluate complete scenario (Expected: PASS)
python3 applied-labs/r34-t001/example.py --scenario normal

# Evaluate scenario with missing asset (Expected: FAIL)
python3 applied-labs/r34-t001/example.py --scenario missing_asset

# Evaluate scenario with unrelated control (Expected: FLAGGED_FOR_REVIEW)
python3 applied-labs/r34-t001/example.py --scenario unrelated_control
```

## Running Unit Tests
```bash
python3 -m unittest discover -s ./applied-labs/r34-t001 -p "test_*.py"
```
