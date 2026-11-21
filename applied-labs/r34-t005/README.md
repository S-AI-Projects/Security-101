# Data Security Scenario Rubric (R34-T005)

Extends **7.3 End of module quiz** using an Offline Service Adapter pattern.
Evaluates data security scenarios (`asset`, `threat`, `control`, `residual_risk`).

## Key Test Cases
1. Complete data security scenario -> `PASS`
2. Missing asset field -> `FAIL`
3. Physical control for digital data threat -> `FLAGGED_FOR_REVIEW`

## Running Tests
```bash
python3 -m unittest discover -s ./applied-labs/r34-t005 -p "test_*.py"
```
