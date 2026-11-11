# Capability negotiation for a SecOps tool

A client can ask for several capabilities when it connects to a security operations service. In this example, the service accepts only capabilities that both sides list. It checks the agreed list before it calls a handler.

## Run the exercise

Use Python 3 and its standard library. From the root of the checkout, run:

```sh
python3 applied-labs/r34-t044/example.py
python3 -m unittest discover -s ./applied-labs/r34-t044 -p "test_*.py"
```

The client lists `tools` and `resources`. The server lists `tools` and `prompts`. Only `tools` appears in both lists. A request to run the sample tool therefore reaches its handler. A request to read an audit log through `resources` stops at the gate.

```text
Negotiated capabilities: ['tools']
Call to 'tools': status=SUCCESS, output=Executed tool action: query_siem
Call to 'resources': status=REJECTED, error=UNNEGOTIATED_CAPABILITY
```

The tests compare the exact command output and verify that the resource handler received no calls. They also cover sessions with no overlap and full overlap.

The handlers return simulated responses. The exercise performs no SIEM query, reads no file, and sends no network request. A production service would also need to authenticate the client and authorize each operation.
