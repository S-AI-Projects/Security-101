# Infrastructure Scenario-Rubric Boundary Lab (R34-T022)

This local example extends
[6.2 Infrastructure security capabilities.md](../../6.2%20Infrastructure%20security%20capabilities.md).
It uses three fictional scenarios tied to named infrastructure sections:

- Vulnerability Management
- CSPM
- CNAPP

## Exact boundary decision

Required fields are `asset`, `threat`, `control`, and `residual_risk`.

1. **Smallest valid**: all fields are present and the control is relevant to the
   threat, so the result is `pass`.
2. **Boundary control**: all fields are present and non-empty, but the control
   is not relevant to the named threat, so the exact boundary result is
   `review`.
3. **Invalid missing asset**: an empty asset fails the completeness check,
   even though the remaining fields are present.

The automated checker does not judge whether the prose is technically correct
or persuasive. Human review is still required.

## Prerequisite and invocation

Prerequisite: Python 3 standard library; no external package or service.

```bash
python3 ./applied-labs/r34-t022/example.py --scenario normal
python3 -m unittest discover -s ./applied-labs/r34-t022 -p "test_*.py"
```

## Fixture output

```text
Smallest valid=pass
Boundary control=review
Missing asset=fail
Boundary decision=non-empty unrelated control is review; empty required field is fail
```
