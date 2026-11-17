# R34-T012: Allowlisted Tool Calls

This lab is a local mock fixture that demonstrates a narrow tool-dispatch security boundary. It uses Python 3 standard library only and has no external dependencies.

## Security boundary

`call_tool` accepts only the explicitly allowlisted names `add` and `multiply`. Before dispatch, it checks that the name is valid, that exactly two arguments were provided, and that both arguments are built-in integers or floats. Strings and booleans are rejected. Invalid calls return a structured error containing `ok: false`, an error code, and a message.

Validation happens before tool lookup and invocation. A failed call does not execute its requested function, fall through to a different tool, or trigger a retry. The tests replace allowed functions with spies and confirm neither is called for rejected input.

This is not a full MCP transport implementation. It does not implement protocol framing, sessions, discovery, authorization, or network transport. It is not integrated with real hardware, a cloud service, or a trained model, and its results do not demonstrate those systems' behavior.

## Run the example

From the repository root:

```bash
python3 applied-labs/r34-t012/example.py
```

The fixture prints successful calls (`add(2, 3) == 5`, `multiply(2, 3) == 6`), zero boundary cases, and structured errors for rejected calls.

## Run the tests

```bash
python3 -m unittest discover -s ./applied-labs/r34-t012 -p "test_*.py"
```

The standard-library `unittest` suite checks normal results, zero and negative boundaries, float inputs, invalid tool names, missing and extra arguments, strings, booleans, structured errors, and that a failed call cannot execute any tool.

## Deliberate wrong-result check

To confirm that the tests detect an incorrect result:

1. In `example.py`, temporarily change the body of `add` from `return first + second` to `return first - second`.
2. Run `python3 -m unittest discover -s ./applied-labs/r34-t012 -p "test_*.py"`.
3. Confirm that `test_add_returns_five` fails because it expected 5 but received -1.
4. Restore `return first + second` and rerun the same command; the suite should pass.

Do not leave the deliberate mutation in place. Evidence for the normal fixture and the test environment is stored under `work/R34-T012/`.
