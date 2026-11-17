# Security Scenario Rubric Checker (R34-T051)

This applied lab extends **1.7 End of module quiz** by providing a local, offline structural rubric checker for cybersecurity scenarios.

## Overview

Cybersecurity assessments require structured, internally consistent threat modeling. Each scenario must capture:
- **Asset**: The resource being protected.
- **Threat**: The adversary goal or attack vector.
- **Control**: The technical or administrative safeguard.
- **Residual Risk**: The risk that remains after the control is in place.

The rubric checker verifies that answers are structurally complete and that nominated controls bear relevance to the specified threats.

## Execution and Scenarios

Run the example from the repository root:

```bash
python3 ./applied-labs/r34-t051/example.py
```

### Scenarios Evaluated

1. **Complete scenario** (`User credential store`): Passes rubric verification (`PASS`).
2. **Missing asset scenario**: Omits the asset field; verification fails immediately (`FAIL`).
3. **Mismatched control scenario**: Pairs SQL injection with offline data backup; flagged for human review (`FLAG_REVIEW`).

Run boundary or failure simulations:

```bash
python3 ./applied-labs/r34-t051/example.py --scenario boundary
python3 ./applied-labs/r34-t051/example.py --scenario failure
```

## Running Tests

Run the unit tests via unittest:

```bash
python3 -m unittest discover -s ./applied-labs/r34-t051 -p "test_*.py"
```

## Scope and Limitations

This implementation is a bounded, deterministic Python script using local data structures. It provides structural validation and keyword-based heuristic flagging only. Human review is required to evaluate qualitative soundness, control depth, and residual risk appropriateness. It does not interface with external services, cloud APIs, or machine learning models.
