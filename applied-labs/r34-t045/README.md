# Infrastructure security rubric with a local catalog

Vulnerability management and cloud security posture management both require a control that addresses a specific problem. These fictional answers let you check that link without a cloud account or a scanner.

Use Python 3 and its standard library. Run the example and the tests from the checkout root.

```sh
python3 applied-labs/r34-t045/example.py
python3 -m unittest discover -s ./applied-labs/r34-t045 -p "test_*.py"
```

| Case | Asset | Threat | Proposed control | Residual risk |
| --- | --- | --- | --- | --- |
| Public store | Report bucket | Public read access | Block public reads | An authorized account can still share a copy. |
| Missing asset | Omitted | Exploit a known service flaw | Patch the affected service | The flaw may have been exploited before the patch. |
| Wrong control | Remote access server | Exploit a known service flaw | Block public reads | The unpatched service can still be exploited. |

```text
public-store: PASS
missing-asset: FAIL (missing or invalid asset)
wrong-control: REVIEW (no matching control)
```

The checker takes an answer and a callable that looks up the expected control for a threat. The local adapter reads a fixed catalog. If the answer omits a required field, the checker stops before the lookup. If the catalog has no matching pair, a person reviews the proposed control.

The mock illustrates the lookup contract. It gives no evidence about service authentication, network failures, catalog freshness, or whether a control works on a real asset. A person checks the evidence and decides if the residual risk is acceptable.
