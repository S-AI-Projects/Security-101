# Network Security Scenario Rubric with Dual-Approach Comparison (R34-T060)

This applied lab extends **3.4 End of module quiz** by evaluating network security scenarios through two independent approaches: a programmatic direct evaluator and an explicit result-table lookup.

## Overview

In security rubric evaluation, comparing multiple implementation techniques helps eliminate implementation bugs and ensures deterministic grading.

### Evaluated Scenarios

1. **Corporate VLAN Gateway**: Complete segmentation scenario -> `[PASS]`.
2. **Missing Asset Scenario**: Omitted asset -> `[FAIL]`.
3. **Mismatched Control**: WAN BGP hijacking paired with Wi-Fi WPA3 Enterprise -> `[FLAG_REVIEW]`.

### Comparison of Two Approaches

- **Approach 1 (Direct Implementation)**: Parses field dictionaries dynamically, validates field non-emptiness, and checks threat keywords against control keywords.
- **Approach 2 (Independent Table Calculation)**: Uses an explicit declarative truth table to map inputs to expected outcomes.
- **Result**: Both approaches achieve 100% agreement on identical inputs.

## Invocation

```bash
python3 ./applied-labs/r34-t060/example.py
python3 ./applied-labs/r34-t060/example.py --scenario boundary
python3 ./applied-labs/r34-t060/example.py --scenario failure
```

## Running Tests

```bash
python3 -m unittest discover -s ./applied-labs/r34-t060 -p "test_*.py"
```

## Scope and Limitations

This script performs local structural checks on mock network security responses. It does not configure real routers, switches, or firewalls.
