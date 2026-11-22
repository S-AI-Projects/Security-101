# IPv4 Allowlist Classification Lab (R34-T025)

This local example extends
[3.3 Network security capabilities.md](../../3.3%20Network%20security%20capabilities.md).
It uses Python's standard `ipaddress` module to parse one IPv4 address and
test it against `192.0.2.0/24`. It performs no scanning or network requests.

## Contract

- `192.0.2.1` with `192.0.2.0/24` returns `True`.
- `198.51.100.1` with `192.0.2.0/24` returns `False`.
- Malformed addresses and malformed CIDRs raise `ValueError`.

## Prerequisite and invocation

Prerequisite: Python 3; no packages or external services are required.

```bash
python3 ./applied-labs/r34-t025/example.py --scenario normal
python3 -m unittest discover -s ./applied-labs/r34-t025 -p "test_*.py"
```

## Worked fixture

The fixture is a mock allowlist check, not an operating firewall or cloud
security group:

```text
CIDR=192.0.2.0/24
192.0.2.1 allowed=true
198.51.100.1 allowed=false
```

Boundary addresses `192.0.2.0` and `192.0.2.255` are in CIDR membership;
`192.0.3.0` is outside. `192.0.2.not-an-ip` is rejected.

## Baseline and extracted responsibility

The baseline and `AddressAllowlist` responsibility expose the same public
contract. `prove_fixture_equivalence` runs both implementations on the local
fixture and asserts that their result dictionaries are identical.
