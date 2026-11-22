# Application-Security Scenario Rubric Lab (R34-T023)

This local example extends
[5.3 End of module quiz.md](../../5.3%20End%20of%20module%20quiz.md)
and the Module 5 AppSec concepts. It encodes fictional scenarios with:

- `asset`
- `threat`
- `control`
- `residual_risk`
- A named lesson section

## Structural rubric

- Missing or empty required fields produce `fail`.
- A control absent from the named threat's relevance table produces `review`.
- A complete structurally relevant answer produces `pass`.

This checker does not judge the quality or truth of human prose. The
explanation and residual-risk rationale require human review.

## Prerequisite and invocation

Prerequisite: Python 3 standard library; no external service or package.

```bash
python3 ./applied-labs/r34-t023/example.py --scenario normal
python3 -m unittest discover -s ./applied-labs/r34-t023 -p "test_*.py"
```

## Fictional fixtures

1. `Web input`: asset, malformed-input threat, server-side allowlist control,
   and residual risk; result `pass`.
2. `Missing asset`: dependency threat and control exist, but the asset is
   empty; result `fail`.
3. `Unrelated control`: API threat with a dependency-scan control; result
   `review`.

## Direct-versus-table comparison

The direct checker and an independent explicit expected-result table receive
the identical three fixtures. The boundary invocation reports whether their
outputs match.

```text
Web input=pass
Missing asset=fail
Unrelated control=review
direct_table_equivalent=true
```
