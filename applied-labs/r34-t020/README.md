# Shared responsibility matrix example

This offline teaching example passes a callable service-adapter interface to a
separate responsibility evaluator. Its deterministic local adapter returns a
small fixture for IaaS, PaaS, and SaaS. Valid owners are `customer`, `provider`,
and `shared`; missing ownership is shown as `UNASSIGNED`, and any other owner
value is shown as `INVALID`.

## Prerequisites and invocation

Requires Python 3 and uses only the Python standard library. No installation,
credentials, network access, model download, GPU, or hardware is needed.

From the repository root, run:

```bash
python3 ./applied-labs/r34-t020/example.py
```

The fixture gives customer, provider, or shared ownership explicitly for each
row. The command prints a deterministic matrix. The optional `--scenario`
argument can run the normal fixture, an empty boundary fixture, or a simulated
adapter failure:

```bash
python3 ./applied-labs/r34-t020/example.py --scenario boundary
python3 ./applied-labs/r34-t020/example.py --scenario failure
```

For the normal fixture, the output contains these seven task/model/owner rows:

```text
Patch guest operating system | IaaS | customer
Protect physical host | IaaS | provider
Secure application code | PaaS | customer
Patch managed runtime | PaaS | provider
Configure user access | SaaS | customer
Protect hosted application | SaaS | provider
Review data handling | PaaS | shared
```

The boundary scenario prints only the matrix header. The failure scenario
writes an error to standard error and exits with status 1.

## Tests

Run the tests from the repository root:

```bash
python3 -m unittest discover -s ./applied-labs/r34-t020 -p "test_*.py"
```

## Limitations

The adapter is a local mock that returns fixed example records. It does not
establish real cloud-provider behavior, actual hardware behavior, security
guarantees, or the behavior of any trained model. In a real deployment, verify
responsibilities using the specific provider's current service documentation
and your organization's configuration.
