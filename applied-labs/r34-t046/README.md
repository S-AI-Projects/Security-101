# Capability negotiation before dispatch

The identity lesson explains why a service checks each request. This simulation adds a separate feature check. A client and a service must both offer a capability before the mock service sends the request to a handler.

Use Python 3 and its standard library. Run these commands from the checkout root.

```sh
python3 applied-labs/r34-t046/example.py
python3 -m unittest discover -s ./applied-labs/r34-t046 -p "test_*.py"
```

The client offers `tools` and `resources`. The service offers `tools` and `prompts`. Try `tools` first, then `resources`.

```text
Negotiated: ['tools']
tools: ACCEPTED (mock tools handler)
resources: REJECTED (unnegotiated capability)
```

The original version in the tests calculates the overlap inside dispatch. The refactor moves this step to `negotiate`, so the example can also report the agreed list. Tests run both versions with the same requests and compare their results and handler calls. They cover partial, full, and empty overlap.

The mock checks feature availability only. A real service also needs to verify identity and authorize the operation and target resource.
