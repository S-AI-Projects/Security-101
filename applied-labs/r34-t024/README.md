# Capability Negotiation Lab (R34-T024)

This local example extends
[3.2 Networking zero trust architecture.md](../../3.2%20Networking%20zero%20trust%20architecture.md).
It demonstrates capability discovery, set intersection, and pre-dispatch
feature gating using a callable interface and deterministic local adapter.

## Contract

- Client capabilities: `{tools, resources}`
- Server capabilities: `{tools, prompts}`
- Negotiated capabilities: `{tools}`
- Calling `tools` is allowed and dispatches once.
- Calling `resources` raises `PermissionError` before dispatch.
- No external network, cloud, hardware, model, or package is required.

## Prerequisites and invocation

Prerequisite: Python 3 standard library.

```bash
python3 ./applied-labs/r34-t024/example.py --scenario normal
python3 -m unittest discover -s ./applied-labs/r34-t024 -p "test_*.py"
```

## Worked fixture

```text
client=['resources', 'tools']
server=['prompts', 'tools']
negotiated=['tools']
tools result=dispatched:tools
```

The same gate rejects `resources`; the local adapter's dispatch count remains
zero for that call.

## Mock boundary

`LocalCapabilityAdapter` deterministically implements the callable interface.
The mock establishes local intersection and gate behavior only. It does not
establish real protocol authentication, authorization, transport, discovery,
latency, retries, identity policy, or cloud/device behavior.
