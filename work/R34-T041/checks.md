# R34-T041 check evidence

Tools used are Python 3.14.6, its bundled `unittest` module, and 2.56.0 of Git. Each command ran in a fresh Python process.

## Fixture inputs

```json
{
  "smallest-valid": {
    "asset": "Remote access server",
    "threat": "exploit unpatched service",
    "control": "apply security patch",
    "residual_risk": "A different flaw could still expose the server."
  },
  "review-boundary": {
    "asset": "Internal reports file store",
    "threat": "read public files",
    "control": "apply security patch",
    "residual_risk": "Anyone can still read files while public access is open."
  },
  "missing-asset": {
    "threat": "exploit unpatched service",
    "control": "apply security patch",
    "residual_risk": "An attacker may have gained access before the patch."
  }
}
```

## Scenario run

```sh
python3 applied-labs/r34-t041/example.py
```

Expected output

```text
smallest-valid: PASS
review-boundary: REVIEW (threat and control do not match the rubric)
missing-asset: FAIL (asset must be non-blank text)
```

Actual output (exit 0)

```text
smallest-valid: PASS
review-boundary: REVIEW (threat and control do not match the rubric)
missing-asset: FAIL (asset must be non-blank text)
```

The commands and expected output in the quiz and lab guide match the run. The quiz link resolves to the lab guide.

## Automated check

```sh
python3 -m unittest discover -s ./applied-labs/r34-t041 -p "test_*.py"
```

Expected five passing tests and exit 0. Actual output (exit 0)

```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
```

The boundary test also changes only the control to `restrict public access` and checks that the result becomes `PASS`.

## Deliberate failure

In a temporary copy, change the mismatch result from `REVIEW (threat and control do not match the rubric)` to `PASS`. Run the same test command in that copy.

Expected five tests, one failure in the boundary test, and exit 1. Actual result (exit 1)

```text
FAIL: test_complete_scenario_with_unrelated_control_needs_review (test_example.ScenarioRubricTests.test_complete_scenario_with_unrelated_control_needs_review)
AssertionError: 'PASS' != 'REVIEW (threat and control do not match the rubric)'
Ran 5 tests in 0.001s
FAILED (failures=1)
```
