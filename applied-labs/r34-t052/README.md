# Zero Trust Capability Negotiation (R34-T052)

This applied lab extends **3.2 Networking zero trust architecture** by demonstrating Zero Trust capability negotiation and feature gating.

## Overview

In Zero Trust network architectures, entities must verify explicitly and enforce least privilege. When two components (such as a client and a server, or microservices) establish communication, they declare supported capabilities. The active session is restricted strictly to the **intersection** of capabilities supported by both parties. Any invocation of a feature outside the negotiated set is rejected immediately prior to dispatch.

## Contract and Scenarios

- **Client set**: `{"tools", "resources"}`
- **Server set**: `{"tools", "prompts"}`
- **Negotiated set**: `{"tools"}`
- **Dispatch 'tools'**: Negotiated -> succeeds.
- **Dispatch 'resources'**: Not in negotiated set -> rejected before dispatch.

### Smallest Valid, Boundary, and Invalid Cases

1. **Smallest Valid Case**: Client `{"tools"}`, Server `{"tools"}` -> Negotiated `{"tools"}`.
2. **Normal Case**: Client `{"tools", "resources"}`, Server `{"tools", "prompts"}` -> Negotiated `{"tools"}`.
3. **Boundary Case**: Client `{"resources"}`, Server `{"prompts"}` -> Empty intersection `set()`. No capability can be invoked.
4. **Invalid Case**: Attempting to invoke unnegotiated `resources` raises `CapabilityNotNegotiatedError` and yields structured rejection.

## Invocation

Run from the repository root:

```bash
python3 ./applied-labs/r34-t052/example.py
python3 ./applied-labs/r34-t052/example.py --scenario boundary
python3 ./applied-labs/r34-t052/example.py --scenario failure
```

## Running Tests

```bash
python3 -m unittest discover -s ./applied-labs/r34-t052 -p "test_*.py"
```

## Scope and Limitations

This script is a deterministic local Python demonstration. It does not implement a full transport layer, cryptographic TLS handshake, or network proxy. It illustrates the fundamental Zero Trust policy check of explicit capability gating.
