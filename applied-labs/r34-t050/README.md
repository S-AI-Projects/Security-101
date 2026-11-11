# Identity and access management rubric

The IAM module covers authentication and authorization. A second factor helps prevent a sign-in with a stolen password. Removing an old role limits what a former contractor can access. Use the example to choose a control that addresses the stated threat.

Use Python 3 and its standard library. Run these commands from the checkout root.

```sh
python3 applied-labs/r34-t050/example.py
python3 -m unittest discover -s ./applied-labs/r34-t050 -p "test_*.py"
```

## Inputs

An `asset` names what you protect. A `threat` states what could go wrong. A `control` names the step that reduces the threat. The `residual_risk` states what could still go wrong after that step.

| Case | Asset | Threat | Control | Residual risk |
| --- | --- | --- | --- | --- |
| Stolen password | Help desk account | Sign in with a stolen password | Require phishing-resistant MFA | An attacker could still steal an active session token. |
| Missing asset | Omitted | Keep access after a contract ends | Remove stale role assignments | A separate account might still have access. |
| Stale access | Payroll reports | Keep access after a contract ends | Require phishing-resistant MFA | A former contractor can still use the assigned role. |

## Outputs

```text
stolen-password: PASS
missing-asset: FAIL (provide asset)
stale-access: REVIEW (control does not match the threat)
```

`PASS` means all fields have text and the control matches the fixture's rule. `FAIL` identifies a missing or invalid field. `REVIEW` sends a complete answer with a control mismatch to a person.

This example uses fictional answers and a fixed rule list. It does not sign in, change roles, or verify that a control works. A person checks the evidence and decides whether the remaining risk is acceptable.
