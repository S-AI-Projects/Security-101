# Infrastructure Scenario Rubric with Evaluation Experiment (R34-T059)

This applied lab extends **6.3 End of module quiz** by evaluating infrastructure security scenarios through a structural rubric and benchmarking three controlled configurations.

## Overview

In infrastructure security assessments (such as cluster hardening, container network security, and firmware posture), rubric checkers must evaluate candidate responses deterministically.

### Evaluated Scenarios

1. **Kubernetes API Server**: Complete specification with mTLS and RBAC -> `[PASS]`.
2. **Missing Asset Scenario**: Blank asset -> `[FAIL]`.
3. **Mismatched Control**: Volumetric DDoS paired with BIOS passwords -> `[FLAG_REVIEW]`.

### Evaluation Experiment: Controlled Configurations

The project measures structural correctness rate and per-scenario processing latency across three input sizes:
- **Config 1 (Single)**: $N = 1$ scenario.
- **Config 2 (Standard)**: $N = 3$ scenarios.
- **Config 3 (Extended)**: $N = 6$ scenarios.

Observed Trade-off: Correctness remains 100% across all batch sizes, while per-scenario latency remains sub-millisecond, demonstrating that the structural heuristic scales linearly without performance degradation.

## Invocation

```bash
python3 ./applied-labs/r34-t059/example.py
python3 ./applied-labs/r34-t059/example.py --scenario boundary
python3 ./applied-labs/r34-t059/example.py --scenario failure
```

## Running Tests

```bash
python3 -m unittest discover -s ./applied-labs/r34-t059 -p "test_*.py"
```

## Scope and Limitations

The evaluation experiment measures local Python execution latency on deterministic mock data. It makes no claims of real-world machine learning model accuracy or cloud infrastructure performance.
