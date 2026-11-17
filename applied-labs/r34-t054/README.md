# Infrastructure Security Scenario Rubric with Service Adapter (R34-T054)

This applied lab extends **6.1 Infrastructure security key concepts** by decoupling scenario sourcing from evaluation through an adapter interface.

## Overview

In infrastructure security auditing, policies must evaluate threat scenarios independently of how data is retrieved (e.g., local configuration, cloud provider APIs, or configuration management databases). This project introduces:
- `ScenarioSourceAdapter`: An abstract callable interface for scenario ingestion.
- `LocalInfrastructureAdapter`: A deterministic local mock adapter providing offline fixtures.
- Decoupled rubric verification checking completeness and threat-control consistency.

## Scenarios in Local Adapter

1. **Cloud compute cluster**: Complete specification with patching/scanning control -> `[PASS]`.
2. **Missing asset scenario**: Omitted asset -> `[FAIL]`.
3. **Mismatched control**: Pairs ransomware encryption with server room physical badge readers -> `[FLAG_REVIEW]`.

## Invocation

```bash
python3 ./applied-labs/r34-t054/example.py
python3 ./applied-labs/r34-t054/example.py --scenario boundary
python3 ./applied-labs/r34-t054/example.py --scenario failure
```

## Running Tests

```bash
python3 -m unittest discover -s ./applied-labs/r34-t054 -p "test_*.py"
```

## Scope and Limitations

The `LocalInfrastructureAdapter` supplies deterministic local Python dictionaries. It does **not** establish real cloud service behavior (such as AWS EC2 or Azure VM resource graphs), live hypervisor instrumentation, physical data center badge reader telemetry, or real-world vulnerability assessment scanning.
