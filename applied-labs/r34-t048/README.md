# Network security scenario assessment

Use what you learned about network segmentation and end-to-end encryption to explain these fictional answers.

Use Python 3 and its standard library. Run these commands from the checkout root.

```sh
python3 applied-labs/r34-t048/example.py
python3 -m unittest discover -s ./applied-labs/r34-t048 -p "test_*.py"
```

| Case | Asset | Threat | Control | Residual risk |
| --- | --- | --- | --- | --- |
| Guest segment | Switch admin interface | Guest network reaches the admin interface | Block guest-to-admin traffic | An admin-network device can still reach the interface. |
| Missing asset | Omitted | Intercept traffic in transit | Use end-to-end encryption | A compromised endpoint can still read the data. |
| Mismatched control | Inventory app traffic | Intercept traffic in transit | Block guest-to-admin traffic | Traffic on an allowed path can still be intercepted. |

```text
guest-segment: PASS
missing-asset: FAIL (asset is required)
mismatched-control: REVIEW (control needs a rationale)
```

## Questions

1. What does the checker print for the guest segment case?
2. Why does the encryption answer with a missing asset fail? What is the smallest repair?
3. A complete answer uses a guest network rule to address interception in transit. Should this checker return `FAIL`, `PASS`, or `REVIEW`?

## Answers and checks

1. `PASS`. All fields have text and the traffic rule addresses the stated path. The test `test_predict_the_guest_segment_result` checks this output.
2. `FAIL (asset is required)`. The answer leaves out what the control protects. Add `Inventory app traffic` and the answer passes. The test `test_diagnose_and_repair_missing_asset` checks both inputs.
3. `REVIEW`. This policy reserves `FAIL` for incomplete answers. The guest network rule does not protect traffic on other allowed paths. A person can assess the reasoning behind a complete answer. The test `test_route_complete_control_mismatch_to_review` checks the decision and verifies that the fixture accepts end-to-end encryption.

The local checker uses a fixed rubric and has no network access. A person evaluates the explanation and residual risk.
