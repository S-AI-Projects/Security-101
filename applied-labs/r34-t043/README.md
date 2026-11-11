# CIA triad scenario classification and comparison exercise

The CIA triad forms the core foundation of information security: confidentiality, integrity, and availability. Real-world security incidents frequently affect more than one pillar simultaneously. Security analysts must accurately classify observed security events and preserve all applicable impact labels.

This exercise implements two independent approaches to classify incident scenarios:
1. **Direct indicator classifier**: Analyzes observed incident events against security indicators and extracts all matching CIA impacts.
2. **Reference ground-truth table**: An independent benchmark lookup that defines expected impact labels for identical inputs.

## Run the exercise

Use Python 3 with its standard library. Run both commands from the root of a local checkout:

```sh
python3 applied-labs/r34-t043/example.py
python3 -m unittest discover -s ./applied-labs/r34-t043 -p "test_*.py"
```

## Scenarios and classification results

`example.py` processes seven fixtures and compares both evaluation approaches:

| Scenario | Incident Description / Event | Classification Rule | Direct Impacts | Reference Impacts | Match |
| --- | --- | --- | --- | --- | --- |
| `unauthorized-reading` | Unauthorized reading | Confidentiality breach | `confidentiality` | `confidentiality` | `AGREED` |
| `altered-records` | Altered records | Integrity violation | `integrity` | `integrity` | `AGREED` |
| `unavailable-service` | Unavailable service | Availability outage | `availability` | `availability` | `AGREED` |
| `multi-confidentiality-integrity` | Unauthorized reading + altered records | Multi-label preservation | `confidentiality, integrity` | `confidentiality, integrity` | `AGREED` |
| `multi-integrity-availability` | File corruption + system outage | Multi-label preservation | `availability, integrity` | `availability, integrity` | `AGREED` |
| `multi-all-triad` | Data exfiltration + altered records + unavailable service | Complete triad impact | `availability, confidentiality, integrity` | `availability, confidentiality, integrity` | `AGREED` |
| `benign-activity` | Routine maintenance without impact | No violation | `none` | `none` | `AGREED` |

Invocation output:

```text
unauthorized-reading: direct=confidentiality, reference=confidentiality, match=AGREED
altered-records: direct=integrity, reference=integrity, match=AGREED
unavailable-service: direct=availability, reference=availability, match=AGREED
multi-confidentiality-integrity: direct=confidentiality,integrity, reference=confidentiality,integrity, match=AGREED
multi-integrity-availability: direct=availability,integrity, reference=availability,integrity, match=AGREED
multi-all-triad: direct=availability,confidentiality,integrity, reference=availability,confidentiality,integrity, match=AGREED
benign-activity: direct=none, reference=none, match=AGREED
```

## How the two approaches compare

1. **Direct Indicator Classification**: The direct implementation scans the scenario events and identifies matching indicators across confidentiality, integrity, and availability. It aggregates all matches into a Python set to avoid dropping multi-vector impacts.
2. **Independent Reference Ground-Truth**: The reference implementation reads directly from an independent benchmark ground-truth definition.
3. **Equivalence Verification**: The comparison function evaluates identical inputs through both paths and verifies that `direct_impacts == reference_impacts`.

## Scope and limitations

This is a local contract fixture using the Python standard library. It does not connect to live SIEM tools, network sensors, or cloud APIs. The exercise demonstrates the multi-label classification logic required to assess security incidents under the CIA triad framework.
