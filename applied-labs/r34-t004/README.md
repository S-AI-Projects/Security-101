# Zero Trust Capability Negotiation (R34-T004)

This applied lab extends **3.2 Networking zero trust architecture** by implementing mutual capability negotiation:
- Client offers `{tools, resources}`.
- Server supports `{tools, prompts}`.
- Mutual negotiation results in `{tools}`.
- Invocations of unnegotiated capabilities (such as `resources`) are strictly rejected prior to dispatch.

## State Trace and Invariant
The intermediate state is recorded at each stage (`step_1_client_offered`, `step_2_server_supported`, `step_3_negotiated`), verifying the Zero Trust invariant:
$$\text{dispatched} \iff \text{capability} \in (\text{Client} \cap \text{Server})$$

## Running Unit Tests
```bash
python3 -m unittest discover -s ./applied-labs/r34-t004 -p "test_*.py"
```
