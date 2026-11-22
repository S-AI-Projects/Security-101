# Test Evidence: R34-T030 Responsibility Matrix Validation

## Environment and Tool Versions

- **Python**: Python 3.9.6
- **Git**: git version 2.50.1 (Apple Git-155)
- **Operating System**: Darwin 27.2.0 arm64 (macOS)
- **Dependencies**: Python standard library only (no external packages or network needed)

## Input Fixtures Summary

1. **Normal Fixture (`NORMAL_FIXTURE`)**:
   - `Patch guest operating system` | `IaaS` | `customer`
   - `Protect physical host` | `IaaS` | `provider`
   - `Secure application code` | `PaaS` | `customer`
   - `Patch managed runtime` | `PaaS` | `provider`
   - `Configure user access` | `SaaS` | `customer`
   - `Protect hosted application` | `SaaS` | `provider`
   - `Review data handling` | `PaaS` | `shared`

2. **Boundary Fixture (`BOUNDARY_FIXTURE`)**:
   - `Configure network security groups` | `IaaS` | omitted -> flags `UNASSIGNED`
   - `Define API rate limits` | `PaaS` | `""` -> flags `UNASSIGNED`
   - `Enforce MFA on user accounts` | `SaaS` | `None` -> flags `UNASSIGNED`

3. **Failure Fixture (`FAILURE_FIXTURE`)**:
   - `Maintain server hardware` | `OnPremise` | `customer` -> raises `ValueError` (invalid service model)

## Expected vs Actual Results

| Check / Scenario | Command / Target | Expected Status / Value | Actual Status / Value | Details |
| :--- | :--- | :--- | :--- | :--- |
| Normal Scenario | `example.py --scenario normal` | Exit code 0, 7 rows formatted, cites lesson | Exit code 0, matches expected output | All tasks have explicit ownership (`customer`, `provider`, `shared`) across IaaS, PaaS, SaaS |
| Boundary Scenario | `example.py --scenario boundary` | Exit code 0, missing ownership flagged `UNASSIGNED` | Exit code 0, `UNASSIGNED` flagged | Does not default unassigned tasks to provider |
| Failure Scenario | `example.py --scenario failure` | Exit code 1, `ValueError` reported on stderr | Exit code 1, `Invalid service model 'OnPremise'` | Rejects invalid cloud service model |
| Question 1: Predict Output | `test_question_1_predict_output` | Evaluates to `"customer"` | `"customer"` | In IaaS, customer owns guest OS and patching |
| Question 2: Diagnose Failure | `test_question_2_diagnose_failure` | Evaluates to `"UNASSIGNED"` | `"UNASSIGNED"` | SaaS user access control omitted party flagged as UNASSIGNED |
| Question 3: Boundary Policy | `test_question_3_choose_boundary_policy` | Evaluates to `"UNASSIGNED"` | `"UNASSIGNED"` | Enforces no-assumed-coverage boundary policy |
| Unit Test Suite | `unittest discover` | 14 passed, exit code 0 | 14 passed in 0.001s, exit code 0 | Non-zero test count, green test suite |
| Deliberate Failure | `check_results.py --deliberate-wrong-result` | Exit code 1, `AssertionError` | Exit code 1, `AssertionError` | Confirms assertion check exits non-zero on mismatch |

## Fresh Process Execution Evidence

- `work/R34-T030/normal-output.txt`: Captured output from running `example.py --scenario normal`
- `work/R34-T030/boundary-output.txt`: Captured output from running `example.py --scenario boundary`
- `work/R34-T030/failure-output.txt`: Captured output from running `example.py --scenario failure`
- `work/R34-T030/test-output.txt`: Captured output from running unit tests (14 tests passed)
- `work/R34-T030/deliberate-failure-output.txt`: Captured output from deliberate wrong assertion (exit code 1)
- `work/R34-T030/tool-versions.txt`: Environment tool version strings
