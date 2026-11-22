# R34-T024 Verification Evidence

## Environment

- Python `3.9.6`
- Standard library only
- Command:
  `python3 -m unittest discover -s ./applied-labs/r34-t024 -p "test_*.py"`

## Normal Fixture

- Client: `{tools, resources}`
- Server: `{tools, prompts}`
- Expected negotiated: `{tools}`
- Actual negotiated: `{tools}`
- Calling `tools` expected: one local dispatch
- Actual: `dispatched:tools`, dispatch count `1`

## Failure Fixture

- Call: `resources`
- Expected: `PermissionError` and dispatch count `0`
- Actual: `Capability 'resources' was not negotiated; allowed=['tools']`;
  dispatch count `0`
- Scenario exit: `1`

## Boundary Fixture

- `{resources}` intersect `{prompts}` expected `{}`; actual `{}`
- Main fixture intersect expected `{tools}`; actual `{tools}`

## Regression Suite

- Expected: 10 tests run, zero failures
- Actual: `Ran 10 tests in 0.000s`, `OK`
