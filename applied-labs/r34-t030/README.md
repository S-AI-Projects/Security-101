# Shared Responsibility Matrix Assessment (R34-T030)

This applied lab extends **[1.6 Shared responsibility model.md](../../1.6%20Shared%20responsibility%20model.md)** by implementing a local, deterministic teaching responsibility matrix. It represents tasks across IaaS, PaaS, and SaaS, explicitly evaluating ownership (`customer`, `provider`, or `shared`) and flagging missing or unassigned ownership rather than assuming cloud provider coverage.

## Overview

In cloud security, assuming that a cloud service provider (CSP) automatically manages unassigned controls is a leading cause of misconfiguration and breaches. This lab encodes the principle of "trust but verify" through an explicit evaluation contract:
1. **Defined Cloud Models**: Tasks must belong to `IaaS`, `PaaS`, or `SaaS`.
2. **Explicit Responsibility**: Valid parties are `customer`, `provider`, or `shared`.
3. **No Assumed Coverage**: When ownership is omitted or blank, the system flags the task as `UNASSIGNED` rather than defaulting to provider responsibility.
4. **Invalid Input Detection**: Unrecognized service models raise errors, and unrecognized ownership parties are flagged as `INVALID`.

## Prerequisites and Invocation

- **Prerequisites**: Python 3 standard library and a local checkout. No external packages, cloud credentials, network access, GPUs, or physical devices are required.
- **Invocation**:

From the repository root:

```bash
# Run normal scenario (default)
python3 ./applied-labs/r34-t030/example.py

# Run boundary scenario (flags unassigned tasks)
python3 ./applied-labs/r34-t030/example.py --scenario boundary

# Run failure scenario (rejects invalid service model with exit code 1)
python3 ./applied-labs/r34-t030/example.py --scenario failure

# Display applied questions, answers, rationales, and executable checks
python3 ./applied-labs/r34-t030/example.py --questions
```

## Normal Fixture and Expected Output

The normal fixture contains 7 representative tasks covering IaaS, PaaS, and SaaS:

| Task | Service Model | Responsible Party |
| :--- | :--- | :--- |
| Patch guest operating system | IaaS | customer |
| Protect physical host | IaaS | provider |
| Secure application code | PaaS | customer |
| Patch managed runtime | PaaS | provider |
| Configure user access | SaaS | customer |
| Protect hosted application | SaaS | provider |
| Review data handling | PaaS | shared |

### Expected Output (`--scenario normal`)

```text
Scenario: Illustrative teaching responsibility matrix based on "1.6 Shared responsibility model.md"; these are educational mock records, not real provider policy.
task | service_model | responsible_party
Patch guest operating system | IaaS | customer
Protect physical host | IaaS | provider
Secure application code | PaaS | customer
Patch managed runtime | PaaS | provider
Configure user access | SaaS | customer
Protect hosted application | SaaS | provider
Review data handling | PaaS | shared
```

## Applied Scenario Assessment Questions

### Question 1: Predict an Output
- **Question**: What is the evaluated responsible party for the task `'Patch guest operating system'` under the `'IaaS'` service model?
- **Answer**: `customer`
- **Rationale**: Under Infrastructure as a Service (IaaS), the cloud provider manages the physical hosts and virtualization layer, but the customer retains full responsibility for the guest operating system, its security configuration, and routine patch management, as explained in `1.6 Shared responsibility model.md`.
- **Executable Check**: `test_question_1_predict_output` in `test_example.py` asserts that evaluating this entry produces `"customer"`.

### Question 2: Diagnose a Failure
- **Question**: Why does evaluating `{'task': 'Enforce MFA on user accounts', 'service_model': 'SaaS'}` fail to assign provider ownership, and how is it evaluated?
- **Answer**: `UNASSIGNED`
- **Rationale**: In Software as a Service (SaaS), user credential management and access controls remain the customer's duty. When `responsible_party` is omitted, our policy flags the ownership as `UNASSIGNED` rather than dangerously assuming the cloud provider covers it.
- **Executable Check**: `test_question_2_diagnose_failure` in `test_example.py` verifies that an omitted ownership field produces `"UNASSIGNED"` and status `"FLAGGED_UNASSIGNED"`.

### Question 3: Choose a Boundary Policy
- **Question**: When a workload security task has no assigned responsible party, what boundary policy must be applied: default-to-provider, default-to-customer, or flag as UNASSIGNED?
- **Answer**: `UNASSIGNED`
- **Rationale**: Defaulting to provider leads to false assumptions of protection ("trust without verify"), causing severe security gaps. Defaulting to customer can misclassify physical data center controls. The safe boundary policy is to flag unassigned tasks as `UNASSIGNED` to enforce explicit review and audit per `1.6 Shared responsibility model.md`.
- **Executable Check**: `test_question_3_choose_boundary_policy` in `test_example.py` asserts that boundary items without assigned parties strictly evaluate to `"UNASSIGNED"` and are never coerced to `"provider"`.

## Running the Automated Test Suite

Run the unit tests via unittest discovery:

```bash
python3 -m unittest discover -s ./applied-labs/r34-t030 -p "test_*.py" -v
```

Expected result: 14 tests passing with zero failures.

## Scope and Limitations

This implementation is a local educational model designed to illustrate the shared responsibility framework taught in Security 101. It uses deterministic in-memory fixtures. It does not interface with live cloud service provider APIs (such as AWS, Azure, or GCP), does not make claims about actual cloud service Level Agreements (SLAs) or hardware configurations, and does not evaluate trained machine learning models.
