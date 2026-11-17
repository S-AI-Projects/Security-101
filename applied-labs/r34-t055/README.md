# Data Security Scenario Rubric Checker with Worked Regression Example (R34-T055)

This applied lab extends **7.3 End of module quiz** by providing a local, offline structural rubric checker with an explicit worked regression example for data security scenarios.

## Overview and Worked Explanation

Evaluating data security scenarios requires assessing assets, data-in-transit/data-at-rest threats, cryptographic and masking controls, and residual risks.

### Worked Input-to-Output Walkthrough

| Field | Scenario 1 (Complete) | Scenario 2 (Missing Asset) | Scenario 3 (Mismatched Control) |
|---|---|---|---|
| **Asset** | PostgreSQL database containing customer financial and PII records | *(omitted/empty)* | Analytics data warehouse tables |
| **Threat** | Exfiltration of sensitive plaintext records during database backup | Unauthorized data alteration in transit | Re-identification of anonymized patient health records |
| **Control** | Implement transparent database encryption (TDE) and encrypted backup exports | Enforce TLS 1.3 with mutual authentication | Deploy storage volume snapshot replication to secondary region |
| **Residual Risk** | Key compromise if master encryption keys are improperly stored | Man-in-the-middle if root CA certificates are untrusted | Replication copies anonymized data without mitigating re-identification risk |
| **Checker Outcome** | `PASS` | `FAIL` | `FLAG_REVIEW` |
| **Rationale** | All fields populated; TDE encryption addresses backup exfiltration threat. | Field `asset` is blank; rejected immediately. | Snapshot replication creates regional copies but does not address record re-identification. Requires human review. |

## Invocation

```bash
python3 ./applied-labs/r34-t055/example.py
python3 ./applied-labs/r34-t055/example.py --scenario boundary
python3 ./applied-labs/r34-t055/example.py --scenario failure
```

## Running Tests

```bash
python3 -m unittest discover -s ./applied-labs/r34-t055 -p "test_*.py"
```

## Scope and Limitations

The rubric checker operates entirely locally as a deterministic Python script. It verifies structural fields and basic heuristic alignment. It makes no claims of cryptanalysis or automated verification of encryption algorithms, and requires human review for qualitative risk validation.
