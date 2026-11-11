# AppSec rubric with a correction step

The AppSec lesson covers input validation and output encoding. Use this local exercise to check an answer for missing data and see why a control must match the threat.

Use Python 3 and its standard library. Run these commands from the checkout root.

```sh
python3 applied-labs/r34-t047/example.py
python3 -m unittest discover -s ./applied-labs/r34-t047 -p "test_*.py"
```

| Case | Asset | Threat | Control | Residual risk |
| --- | --- | --- | --- | --- |
| Missing asset | Omitted | Inject SQL through a search field | Use parameterized queries | Other query paths may still build SQL from raw input. |
| Corrected | Catalog search database | Inject SQL through a search field | Use parameterized queries | Other query paths may still build SQL from raw input. |
| Unrelated control | Product review page | Inject script through a review comment | Use parameterized queries | A review can still contain a script that runs in a browser. |

```text
missing-asset: FAIL (provide asset)
corrected: PASS
unrelated-control: REVIEW (check threat and control)
```

The first answer fails because it leaves out the asset. Add the database and send the corrected answer as the next input. The earlier failure has no effect on the new result. The third answer needs review because parameterized queries address SQL injection. Output encoding for the HTML context addresses the stated script injection case.

The checker reads fictional answers and checks a small list of threat and control pairs. It runs no SQL and renders no HTML. A person reviews the evidence, the control rationale, and the residual risk.
