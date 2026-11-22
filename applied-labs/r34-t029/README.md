# IAM Access Policy Evaluator & Configuration Comparison (R34-T029)

This applied lab extends **[2.3 IAM capabilities.md](../../2.3%20IAM%20capabilities.md)** by implementing a local, deterministic Role-Based Access Control (RBAC) policy evaluator and configuration comparison experiment.

## Overview

In modern identity and access management (IAM), authorization decisions govern access to protected systems. Two fundamental principles ensure least-privilege security:
1. **Default Deny**: Any role, action, or resource not explicitly permitted is blocked.
2. **Deny Overrides Allow**: When multiple policies match a request, an explicit `DENY` strictly overrides any matching `ALLOW`.

This lab evaluates access requests against a local policy matrix and compares three controlled configurations to evaluate policy inspection overhead versus correctness.

## Key Contract Requirements

- `reader` may read `public` (`ALLOW`).
- `reader` cannot write `public` (`DENY`).
- An explicit deny overrides a matching allow (`auditor` auditing `logs` evaluates to `DENY`).
- An unknown role is denied (`stranger` evaluates to `DENY`).
- Unspecified actions/resources evaluate to `DENY` under default-deny.

## Prerequisites and Invocation

- **Prerequisites**: Python 3 standard library and a local checkout. No external packages, cloud credentials, network access, GPUs, or physical devices are required.
- **Invocation**:

From the repository root:

```bash
# Run normal scenario (evaluates core contract requests)
python3 ./applied-labs/r34-t029/example.py

# Run boundary scenario (tests unlisted resources and empty fields)
python3 ./applied-labs/r34-t029/example.py --scenario boundary

# Run failure scenario (rejects malformed policy effect with exit code 1)
python3 ./applied-labs/r34-t029/example.py --scenario failure

# Run controlled configuration comparison experiment
python3 ./applied-labs/r34-t029/example.py --compare

# Evaluate a specific single request
python3 ./applied-labs/r34-t029/example.py --role reader --action read --resource public
```

## Standard Policy Matrix & Normal Output

The standard policy matrix consists of 6 rules:

| Role | Action | Resource | Effect |
| :--- | :--- | :--- | :--- |
| reader | read | public | ALLOW |
| reader | write | public | DENY |
| editor | read | public | ALLOW |
| editor | write | public | ALLOW |
| auditor | audit | logs | ALLOW |
| auditor | audit | logs | DENY |

### Expected Output (`--scenario normal`)

```text
Scenario: Illustrative IAM policy evaluation based on "2.3 IAM capabilities.md"; educational mock matrix, not real identity provider.
role | action | resource | decision | reason
reader | read | public | ALLOW | Permission granted for role 'reader' to 'read' on 'public'.
reader | write | public | DENY | Explicit DENY rule matched for role 'reader' on 'public'.
auditor | audit | logs | DENY | Explicit DENY overrides matching ALLOW for role 'auditor' on 'logs'.
stranger | read | public | DENY | Role 'stranger' is unknown or not recognized (default deny).
reader | delete | public | DENY | No policy grants role 'reader' permission to 'delete' on 'public' (default deny).
```

## Controlled Configuration Comparison Experiment

We compare three controlled rule-set configurations across a fixed benchmark request set:
- **Config 1 (Minimal)**: 3 rules (`reader` read/write, `editor` read).
- **Config 2 (Standard)**: 6 rules (Standard RBAC matrix with deny-override).
- **Config 3 (Comprehensive)**: 12 rules (adds administrative and visitor roles).

### Comparison Metric & Results

- **Correctness Rate**: Percentage of authorization requests correctly decided according to contract rules (100.0% across all configurations).
- **Rule Checks**: Total policy rule inspections required across the benchmark requests.

```text
Configuration Comparison Experiment (2.3 IAM capabilities.md)
================================================================================
Config                     | Rules (N) | Requests | Correctness | Total Checks | Checks/Req
--------------------------------------------------------------------------------
Config 1 (Minimal)         | 3         | 4        | 100.0%       | 12           | 3.0
Config 2 (Standard)        | 6         | 4        | 100.0%       | 24           | 6.0
Config 3 (Comprehensive)   | 12        | 4        | 100.0%       | 48           | 12.0
--------------------------------------------------------------------------------
Observed Trade-off: Expanding policy granularity increases evaluation checks linearly (O(N) search), maintaining 100.0% policy correctness with default-deny and deny-override guarantees.
```

### Observed Trade-off
- As policy sets grow in granularity and expressiveness from Minimal ($N=3$) to Comprehensive ($N=12$), rule evaluation checks scale linearly ($O(N)$ inspection per decision).
- Crucially, policy correctness remains 100.0% deterministic across all configurations because default-deny and deny-precedence are strictly maintained.

## Running the Automated Test Suite

Run unit tests via unittest discovery:

```bash
python3 -m unittest discover -s ./applied-labs/r34-t029 -p "test_*.py" -v
```

Expected result: 15 tests passing with zero failures.

## Scope and Limitations

This implementation is a local educational demonstration of RBAC semantics and deny-precedence rules. It evaluates in-memory rules and does not connect to enterprise directory services (such as Microsoft Active Directory, Microsoft Entra ID, or LDAP), does not evaluate network latency or physical hardware, and does not evaluate trained machine learning models.
