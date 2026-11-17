# Test Evidence: R34-T051 Security Scenario Rubric Checker

## Environment and Tools

- Python: 3.9.6
- Git: git version 2.50.1 (Apple Git-155)
- Platform: Darwin arm64 (macOS)
- Runtime: Python standard library (`unittest`, `argparse`, `sys`, `typing`)

## Input Fixtures

Documented in `inputs/fixtures.json` and `applied-labs/r34-t051/example.py`:
1. **Scenario 1 (Normal)**:
   - Asset: Customer authentication database
   - Threat: Credential stuffing and unauthorized access
   - Control: Enforce multi-factor authentication and rate limiting
   - Residual Risk: Adversary session hijacking via phishing tokens
2. **Scenario 2 (Missing Asset)**:
   - Asset: `""` (empty)
   - Threat: Eavesdropping on network communication
   - Control: Implement TLS 1.3 encryption in transit
   - Residual Risk: Compromised endpoints could still expose plaintext
3. **Scenario 3 (Mismatched Control)**:
   - Asset: Public web portal
   - Threat: SQL injection via search input
   - Control: Deploy automated offline data backup service
   - Residual Risk: Backups do not prevent data exfiltration via active injection

## Expected vs Actual Results

| Scenario | Expected Status | Actual Status | Details |
|---|---|---|---|
| Complete scenario | `PASS` | `PASS` | All required fields populated; control matches threat keywords |
| Missing asset | `FAIL` | `FAIL` | Immediate rejection due to missing `asset` field |
| Mismatched control | `FLAG_REVIEW` | `FLAG_REVIEW` | Complete structure but control is unrelated to threat; flagged for human review |
| Empty list (boundary) | 0 results | 0 results | Returns empty list cleanly, exits 0 |
| Deliberate failure | Non-zero exit | Exit code 1 | Captured in `failure-output.txt` and `deliberate-failure-output.txt` |

## Test Suite Execution

Command:
```bash
python3 -m unittest discover -s ./applied-labs/r34-t051 -p "test_*.py"
```
Result: 6 tests passed in 0.000s (saved in `test-output.txt`).

## Deliberate Wrong Result Check

Command:
```bash
python3 ./work/R34-T051/check_results.py --deliberate-wrong-result
```
Result: Exits with status 1 and AssertionError (saved in `deliberate-failure-output.txt`).
