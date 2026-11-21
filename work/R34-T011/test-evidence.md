# R34-T011 — Test Evidence

## Environment

- Python: 3.13.15
- Git: 2.55.0
- Operating system: macOS 27.2.0, arm64
- Test framework: Python standard-library `unittest`
- Dependencies: none beyond Python 3

## Zero Trust Capability Negotiation Example

Invocation:

```bash
python3 ./applied-labs/r34-t011/example.py
```

Input fixtures:
- Client capabilities: `{"tools", "resources"}`
- Server capabilities: `{"tools", "prompts"}`

Expected vs Actual Results:

| Scenario | Input / Action | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| Negotiation | `client & server` | Negotiated capabilities: `['tools']` | Negotiated capabilities: `['tools']` | MATCH |
| Normal | Dispatch `"tools"` | Handler executes: `"Tool executed successfully!"` | Handler executes: `"Tool executed successfully!"` | MATCH |
| Boundary / Failure | Dispatch `"resources"` | `PermissionError: Access denied: 'resources' was not negotiated` (handler not dispatched) | `PermissionError: Access denied: 'resources' was not negotiated` (handler not dispatched) | MATCH |

## Unit Tests

Command:

```bash
python3 -m unittest discover -s ./applied-labs/r34-t011 -p "test_*.py" -v
```

Output:

```text
test_only_common_capabilities_are_negotiated (test_example.TestZeroTrust.test_only_common_capabilities_are_negotiated) ... ok
test_resources_are_rejected_before_dispatch (test_example.TestZeroTrust.test_resources_are_rejected_before_dispatch) ... ok
test_tools_are_allowed (test_example.TestZeroTrust.test_tools_are_allowed) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

## Deliberately Wrong Expected Result

A deliberate test failure was executed asserting an invalid capability set:

```bash
python3 -c "import sys; sys.path.insert(0, 'applied-labs/r34-t011'); from example import negotiate_capabilities; assert negotiate_capabilities({'tools', 'resources'}, {'tools', 'prompts'}) == {'tools', 'resources'}, 'Deliberate test failure'"
```

Expected: Assertion failure and non-zero process exit.
Actual: `AssertionError: Deliberate test failure`; process exit code `1`.

## Scope and Limitations

This example is a local deterministic demonstration of capability negotiation and gating under Zero Trust (least privilege / explicit verification). It relies entirely on Python standard library data structures. It does not implement production authentication, cryptographic verification, network discovery protocols, cloud provider mechanisms, or physical hardware controls.
