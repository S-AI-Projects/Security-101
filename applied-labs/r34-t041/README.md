# Infrastructure security rubric exercise

The infrastructure security module covers patching known flaws and fixing insecure cloud settings. In this exercise, use the facts in each fictional case to identify the asset, the threat, the control, and the risk that remains after the control.

## Run the exercise

Use Python 3 with its standard library. Run both commands from the root of a local checkout.

```sh
python3 applied-labs/r34-t041/example.py
python3 -m unittest discover -s ./applied-labs/r34-t041 -p "test_*.py"
```

`example.py` contains the three inputs. The program prints the result for each input.

| Case | Asset | Threat | Control | Residual risk |
| --- | --- | --- | --- | --- |
| Smallest valid | Remote access server | exploit unpatched service | apply security patch | A different flaw could still expose the server. |
| Review boundary | Internal reports file store | read public files | apply security patch | Anyone can still read files while public access is open. |
| Invalid | Missing | exploit unpatched service | apply security patch | An attacker may have gained access before the patch. |

```text
smallest-valid: PASS
review-boundary: REVIEW (threat and control do not match the rubric)
missing-asset: FAIL (asset must be non-blank text)
```

## How the checker decides

1. The smallest valid answer has all four required fields and a threat and control pair listed in the rubric. In this case, the patch addresses the flaw in the remote access service. The checker returns `PASS`.
2. The boundary answer has all four fields, but a patch leaves the public read setting open. The checker returns `REVIEW`. Change only the control to `restrict public access` to get `PASS`.
3. The invalid answer gives a threat and a matching control, but it omits the asset. The checker returns `FAIL` before it checks the pair. A field with only whitespace also fails.

The checker removes surrounding whitespace and compares the threat and control text with two pairs defined in the fixture. An unlisted pair needs review.

A reviewer checks the evidence, the choice of control, and the risk that remains. For example, a service version report can show which patch is missing. A storage access policy can show who can read the files. If the control changes, reassess the residual risk.

This local simulation checks text fields only. It uses fictional data and does not scan a system, change a setting, or measure how well a control works.
