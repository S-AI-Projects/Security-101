# AI-Security Scenario-Rubric Lab (R34-T021)

This local example extends
[8.4 End of module quiz.md](../../8.4%20End%20of%20module%20quiz.md)
and connects its public fields to named Module 8 concepts.

## Public contract

Every scenario contains:

- `section`: named lesson concept
- `asset`: protected AI or data asset
- `threat`: fictional threat
- `control`: claimed safeguard
- `residual_risk`: remaining uncertainty

The checker returns:

- `pass`: all fields are complete and the control belongs to the threat map.
- `fail`: an asset or another required field is empty.
- `review`: all fields are complete but the control is unrelated to the threat.

Human review judges the explanation and factual accuracy. The checker does
not infer or grade prose quality.

## Named fixtures

- `Data Integrity`: training dataset plus unauthorized modification threat;
  `data integrity validation` is relevant, so it passes.
- `Adversarial Attacks`: an adversarial-input threat with no asset; it fails.
- `Responsible AI`: biased automated decision plus `runtime model inventory`;
  the unrelated control is flagged for review.

## Prerequisite and invocation

Prerequisite: Python 3 standard library; no model, package, network, or device.

```bash
python3 ./applied-labs/r34-t021/example.py --scenario normal
python3 -m unittest discover -s ./applied-labs/r34-t021 -p "test_*.py"
```

## Mock boundary

This is fictional educational content. It does not evaluate a real model,
run red teaming, use cloud or hardware, or establish trained-model behavior.
